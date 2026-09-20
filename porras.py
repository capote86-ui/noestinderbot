import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

# football-data.org API v4
API_BASE = "https://api.football-data.org/v4"
LALIGA_CODE = "PD"

TZ = ZoneInfo("Atlantic/Canary")
GRUPO_PRINCIPAL_ID = -1003634987823
DATA_FILE = Path("/data/porras_futbol.json")
PUBLICAR_HORAS_ANTES = 36

ESTADOS_PROGRAMADOS = {"SCHEDULED", "TIMED"}
ESTADOS_FINAL = {"FINISHED", "AWARDED"}
ESTADOS_CANCELADOS = {"POSTPONED", "CANCELLED", "SUSPENDED"}

PATRON = re.compile(r"^\s*(\d{1,2})\s*[-–—]\s*(\d{1,2})\s*$")


def _api_token():
    return os.getenv("FOOTBALL_DATA_TOKEN")


def _vacio():
    return {"partidos": {}, "ranking": {}}


def _cargar():
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                datos = json.load(f)
                datos.setdefault("partidos", {})
                datos.setdefault("ranking", {})
                return datos
    except Exception as e:
        print("PORRAS: no se pudo cargar el JSON:", e)
    return _vacio()


def _guardar(datos):
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = DATA_FILE.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        tmp.replace(DATA_FILE)
    except Exception as e:
        print("PORRAS: no se pudo guardar el JSON:", e)


def _get(endpoint, params=None):
    token = _api_token()
    if not token:
        raise RuntimeError("Falta la variable FOOTBALL_DATA_TOKEN en Railway")

    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(
        url,
        headers={
            "X-Auth-Token": token,
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            cuerpo = e.read().decode("utf-8")
            detalle = json.loads(cuerpo)
        except Exception:
            detalle = str(e)
        raise RuntimeError(f"football-data.org HTTP {e.code}: {detalle}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"No se pudo conectar con football-data.org: {e.reason}") from e


def _parsear_fecha_utc(fecha):
    # football-data.org devuelve fechas tipo 2026-09-20T19:00:00Z
    return datetime.fromisoformat(fecha.replace("Z", "+00:00")).astimezone(TZ)


def _fecha_humana(dt):
    dias = [
        "lunes", "martes", "miércoles", "jueves",
        "viernes", "sábado", "domingo"
    ]
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    return (
        f"{dias[dt.weekday()].capitalize()} {dt.day} "
        f"de {meses[dt.month - 1]} · {dt:%H:%M} h"
    )


def _texto_porra(local, visitante, inicio):
    return (
        "⚽ 🏆 PORRA DE LALIGA 🏆 ⚽\n\n"
        f"🔴 {local}\n"
        "🆚\n"
        f"🔵 {visitante}\n\n"
        f"📅 {_fecha_humana(inicio)} (hora canaria)\n\n"
        "💬 Responde A ESTE MENSAJE con tu predicción en formato X-X.\n"
        "Ejemplos: 2-1, 0-0, 1-3…\n\n"
        "⏳ Puedes cambiar tu resultado hasta que empiece el partido."
    )


def _nombre(user):
    if user.username:
        return f"@{user.username}"
    return user.first_name or "Alguien"


async def revisar_porras(context):
    """Publica próximas porras y resuelve las ya finalizadas."""
    ahora = datetime.now(TZ)

    try:
        payload = _get(
            f"competitions/{LALIGA_CODE}/matches",
            {
                "dateFrom": ahora.date().isoformat(),
                "dateTo": (ahora.date() + timedelta(days=2)).isoformat(),
            },
        )
        partidos = payload.get("matches", [])
    except Exception as e:
        print("PORRAS: error consultando football-data.org:", e)
        return

    datos = _cargar()
    cambiado = False

    for item in partidos:
        fid = str(item.get("id"))
        if not fid or fid == "None":
            continue

        try:
            inicio = _parsear_fecha_utc(item["utcDate"])
        except Exception:
            continue

        estado = item.get("status", "")
        local = (item.get("homeTeam") or {}).get("name", "Local")
        visitante = (item.get("awayTeam") or {}).get("name", "Visitante")
        registro = datos["partidos"].get(fid)

        # Publica desde 36 horas antes hasta el comienzo.
        if (
            registro is None
            and timedelta(0) < (inicio - ahora) <= timedelta(hours=PUBLICAR_HORAS_ANTES)
            and estado in ESTADOS_PROGRAMADOS
        ):
            try:
                msg = await context.bot.send_message(
                    chat_id=GRUPO_PRINCIPAL_ID,
                    text=_texto_porra(local, visitante, inicio),
                )

                datos["partidos"][fid] = {
                    "match_id": int(fid),
                    "message_id": msg.message_id,
                    "chat_id": GRUPO_PRINCIPAL_ID,
                    "local": local,
                    "visitante": visitante,
                    "inicio": inicio.isoformat(),
                    "estado": "abierta",
                    "predicciones": {},
                    "resuelta": False,
                }

                cambiado = True
                registro = datos["partidos"][fid]
                print(f"PORRAS: publicada {local} - {visitante}")

            except Exception as e:
                print("PORRAS: error publicando porra:", e)
                continue

        if not registro:
            continue

        # Cierra cuando empieza o cuando la API deja de considerarlo programado.
        if (
            registro.get("estado") == "abierta"
            and (ahora >= inicio or estado not in ESTADOS_PROGRAMADOS)
        ):
            registro["estado"] = "cerrada"
            cambiado = True

        # Resuelve cuando football-data.org lo marca como finalizado/adjudicado.
        if estado in ESTADOS_FINAL and not registro.get("resuelta"):
            score = item.get("score") or {}
            full_time = score.get("fullTime") or {}
            gh = full_time.get("home")
            ga = full_time.get("away")

            if gh is None or ga is None:
                continue

            await _resolver(context, datos, registro, int(gh), int(ga))
            registro["resuelta"] = True
            registro["estado"] = "resuelta"
            registro["resultado"] = f"{gh}-{ga}"
            cambiado = True

        # Anula si el partido se aplaza, cancela o suspende.
        if (
            estado in ESTADOS_CANCELADOS
            and registro.get("estado") not in {"cancelada", "resuelta"}
        ):
            registro["estado"] = "cancelada"
            cambiado = True

            try:
                await context.bot.send_message(
                    chat_id=registro["chat_id"],
                    reply_to_message_id=registro["message_id"],
                    text=(
                        f"⚠️ La porra {local} - {visitante} queda anulada "
                        f"porque el partido figura como {estado}."
                    ),
                )
            except Exception as e:
                print("PORRAS: error avisando cancelación:", e)

    if cambiado:
        _guardar(datos)


async def _resolver(context, datos, registro, gh, ga):
    resultado = f"{gh}-{ga}"
    acertantes = []

    for uid, pred in registro.get("predicciones", {}).items():
        if pred.get("resultado") == resultado:
            acertantes.append((uid, pred.get("nombre", "Alguien")))

            rank = datos["ranking"].setdefault(
                uid,
                {
                    "nombre": pred.get("nombre", "Alguien"),
                    "puntos": 0,
                    "aciertos": 0,
                },
            )

            rank["nombre"] = pred.get(
                "nombre",
                rank.get("nombre", "Alguien")
            )
            rank["puntos"] = int(rank.get("puntos", 0)) + 1
            rank["aciertos"] = int(rank.get("aciertos", 0)) + 1

    if acertantes:
        nombres = "\n".join(f"🏆 {nombre}" for _, nombre in acertantes)
        texto = (
            f"🏁 FINAL: {registro['local']} {gh}-{ga} {registro['visitante']}\n\n"
            "🎯 ¡Resultado clavado!\n"
            f"{nombres}\n\n"
            "Cada acertante suma 1 punto en el ranking de la porra. ⚽"
        )
    else:
        texto = (
            f"🏁 FINAL: {registro['local']} {gh}-{ga} {registro['visitante']}\n\n"
            "😭 Nadie clavó el resultado esta vez. La porra queda desierta."
        )

    try:
        await context.bot.send_message(
            chat_id=registro["chat_id"],
            reply_to_message_id=registro["message_id"],
            text=texto,
        )
    except Exception as e:
        print("PORRAS: error publicando resultado:", e)


async def procesar_prediccion_porra(update, context):
    """Guarda X-X solo cuando el usuario responde al mensaje de una porra."""
    msg = update.message

    if not msg or not msg.text or not msg.reply_to_message:
        return False

    match = PATRON.match(msg.text)
    if not match:
        return False

    datos = _cargar()
    reply_id = msg.reply_to_message.message_id
    chat_id = update.effective_chat.id
    registro = None

    for p in datos["partidos"].values():
        if p.get("message_id") == reply_id and p.get("chat_id") == chat_id:
            registro = p
            break

    if not registro:
        return False

    if registro.get("estado") != "abierta":
        await msg.reply_text("🔒 Esta porra ya está cerrada.")
        return True

    try:
        inicio = datetime.fromisoformat(registro["inicio"])
        if datetime.now(TZ) >= inicio:
            registro["estado"] = "cerrada"
            _guardar(datos)
            await msg.reply_text(
                "🔒 El partido ya ha empezado. Esta porra está cerrada."
            )
            return True
    except Exception:
        pass

    goles_local = int(match.group(1))
    goles_visitante = int(match.group(2))
    resultado = f"{goles_local}-{goles_visitante}"

    uid = str(update.effective_user.id)
    nombre = _nombre(update.effective_user)
    anterior = registro.setdefault("predicciones", {}).get(uid)

    registro["predicciones"][uid] = {
        "nombre": nombre,
        "resultado": resultado,
        "fecha": datetime.now(TZ).isoformat(),
    }

    _guardar(datos)

    if anterior:
        await msg.reply_text(
            f"🔄 {nombre}, predicción actualizada: {resultado} ⚽"
        )
    else:
        await msg.reply_text(
            f"✅ {nombre}, predicción guardada: {resultado} ⚽"
        )

    return True


async def ranking_porras(update, context):
    datos = _cargar()

    ranking = sorted(
        datos.get("ranking", {}).values(),
        key=lambda x: (
            -int(x.get("puntos", 0)),
            x.get("nombre", "")
        ),
    )

    if not ranking:
        await update.message.reply_text(
            "⚽ Todavía no hay puntos en la porra de LaLiga."
        )
        return

    texto = "🏆 RANKING DE LA PORRA · LALIGA\n\n"
    medallas = ["🥇", "🥈", "🥉"]

    for i, fila in enumerate(ranking[:15], start=1):
        icono = medallas[i - 1] if i <= 3 else f"{i}."
        texto += (
            f"{icono} {fila.get('nombre', 'Alguien')} — "
            f"{fila.get('puntos', 0)} punto(s)\n"
        )

    await update.message.reply_text(texto)


async def estado_porras(update, context):
    """Comando admin para comprobar token y conexión sin esperar."""
    token = _api_token()

    if not token:
        await update.message.reply_text(
            "❌ No encuentro FOOTBALL_DATA_TOKEN en Railway."
        )
        return

    ahora = datetime.now(TZ)

    try:
        payload = _get(
            f"competitions/{LALIGA_CODE}/matches",
            {
                "dateFrom": ahora.date().isoformat(),
                "dateTo": (ahora.date() + timedelta(days=2)).isoformat(),
            },
        )
        partidos = payload.get("matches", [])

    except Exception as e:
        await update.message.reply_text(
            f"❌ football-data.org responde con error:\n{e}"
        )
        return

    if not partidos:
        await update.message.reply_text(
            "✅ football-data.org conecta bien. "
            "No hay partidos de LaLiga en las próximas 48 horas."
        )
        return

    lineas = [
        "✅ football-data.org conecta bien.\n",
        "Próximos partidos detectados:"
    ]

    for item in partidos[:10]:
        try:
            dt = _parsear_fecha_utc(item["utcDate"])
        except Exception:
            continue

        local = (item.get("homeTeam") or {}).get("name", "Local")
        visitante = (item.get("awayTeam") or {}).get("name", "Visitante")
        estado = item.get("status", "?")

        lineas.append(
            f"• {local} - {visitante} · {dt:%d/%m %H:%M} · {estado}"
        )

    await update.message.reply_text("\n".join(lineas))
