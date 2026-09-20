import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

API_BASE = "https://v3.football.api-sports.io"
LALIGA_ID = 140
TZ = ZoneInfo("Atlantic/Canary")
GRUPO_PRINCIPAL_ID = -1003634987823
DATA_FILE = Path("/data/porras_futbol.json")
PUBLICAR_HORAS_ANTES = 36
ESTADOS_FINAL = {"FT", "AET", "PEN"}
ESTADOS_CANCELADOS = {"PST", "CANC", "ABD", "AWD", "WO"}
PATRON = re.compile(r"^\s*(\d{1,2})\s*[-–—]\s*(\d{1,2})\s*$")


def _api_key():
    # Admite varios nombres por si Railway se creó con una variante.
    return (
        os.getenv("API_FOOTBALL_KEY")
        or os.getenv("API_FOOTBALLK")
        or os.getenv("API_FOOTBALL_K")
        or os.getenv("API_FOOTBALL")
    )


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


def _get(endpoint, params):
    key = _api_key()
    if not key:
        raise RuntimeError("Falta la variable API_FOOTBALL_KEY en Railway")
    url = f"{API_BASE}/{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"x-apisports-key": key})
    with urllib.request.urlopen(req, timeout=20) as r:
        payload = json.loads(r.read().decode("utf-8"))
    if payload.get("errors"):
        raise RuntimeError(f"API-Football: {payload['errors']}")
    return payload.get("response", [])


def _temporada(ahora):
    # En ligas europeas la temporada se identifica por el año en que comienza.
    return ahora.year if ahora.month >= 7 else ahora.year - 1


def _fecha_humana(dt):
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{dias[dt.weekday()].capitalize()} {dt.day} de {meses[dt.month - 1]} · {dt:%H:%M} h"


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
    """Una sola consulta periódica: publica próximas porras y resuelve finalizadas."""
    ahora = datetime.now(TZ)
    try:
        partidos = _get(
            "fixtures",
            {
                "league": LALIGA_ID,
                "season": _temporada(ahora),
                "from": ahora.date().isoformat(),
                "to": (ahora.date() + timedelta(days=2)).isoformat(),
                "timezone": "Atlantic/Canary",
            },
        )
    except Exception as e:
        print("PORRAS: error consultando API-Football:", e)
        return

    datos = _cargar()
    cambiado = False

    for item in partidos:
        fixture = item.get("fixture", {})
        teams = item.get("teams", {})
        goals = item.get("goals", {})
        fid = str(fixture.get("id"))
        if not fid or fid == "None":
            continue

        try:
            inicio = datetime.fromisoformat(fixture["date"]).astimezone(TZ)
        except Exception:
            continue

        estado = (fixture.get("status") or {}).get("short", "")
        local = (teams.get("home") or {}).get("name", "Local")
        visitante = (teams.get("away") or {}).get("name", "Visitante")
        registro = datos["partidos"].get(fid)

        # Publicar entre 36 h antes y el comienzo. Si el bot estuvo apagado, lo publica al volver.
        if registro is None and timedelta(0) < (inicio - ahora) <= timedelta(hours=PUBLICAR_HORAS_ANTES) and estado == "NS":
            try:
                msg = await context.bot.send_message(
                    chat_id=GRUPO_PRINCIPAL_ID,
                    text=_texto_porra(local, visitante, inicio),
                )
                datos["partidos"][fid] = {
                    "fixture_id": int(fid),
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
                print(f"PORRAS: publicada {local} - {visitante}")
                registro = datos["partidos"][fid]
            except Exception as e:
                print("PORRAS: error publicando porra:", e)
                continue

        if not registro:
            continue

        # Cerrar al comenzar o si deja de estar NS.
        if registro.get("estado") == "abierta" and (ahora >= inicio or estado != "NS"):
            registro["estado"] = "cerrada"
            cambiado = True

        # Resolver cuando API-Football marque el partido como terminado.
        if estado in ESTADOS_FINAL and not registro.get("resuelta"):
            gh, ga = goals.get("home"), goals.get("away")
            if gh is None or ga is None:
                continue
            await _resolver(context, datos, registro, int(gh), int(ga))
            registro["resuelta"] = True
            registro["estado"] = "resuelta"
            registro["resultado"] = f"{gh}-{ga}"
            cambiado = True

        if estado in ESTADOS_CANCELADOS and registro.get("estado") not in {"cancelada", "resuelta"}:
            registro["estado"] = "cancelada"
            cambiado = True
            try:
                await context.bot.send_message(
                    chat_id=registro["chat_id"],
                    reply_to_message_id=registro["message_id"],
                    text=f"⚠️ La porra {local} - {visitante} queda anulada porque el partido figura como {estado}.",
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
            rank = datos["ranking"].setdefault(uid, {"nombre": pred.get("nombre", "Alguien"), "puntos": 0, "aciertos": 0})
            rank["nombre"] = pred.get("nombre", rank.get("nombre", "Alguien"))
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
            await msg.reply_text("🔒 El partido ya ha empezado. Esta porra está cerrada.")
            return True
    except Exception:
        pass

    goles_local, goles_visitante = int(match.group(1)), int(match.group(2))
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
        await msg.reply_text(f"🔄 {nombre}, predicción actualizada: {resultado} ⚽")
    else:
        await msg.reply_text(f"✅ {nombre}, predicción guardada: {resultado} ⚽")
    return True


async def ranking_porras(update, context):
    datos = _cargar()
    ranking = sorted(datos.get("ranking", {}).values(), key=lambda x: (-int(x.get("puntos", 0)), x.get("nombre", "")))
    if not ranking:
        await update.message.reply_text("⚽ Todavía no hay puntos en la porra de LaLiga.")
        return
    texto = "🏆 RANKING DE LA PORRA · LALIGA\n\n"
    medallas = ["🥇", "🥈", "🥉"]
    for i, fila in enumerate(ranking[:15], start=1):
        icono = medallas[i - 1] if i <= 3 else f"{i}."
        texto += f"{icono} {fila.get('nombre', 'Alguien')} — {fila.get('puntos', 0)} punto(s)\n"
    await update.message.reply_text(texto)


async def estado_porras(update, context):
    """Comando admin de diagnóstico, útil para comprobar la API sin esperar."""
    key = _api_key()
    if not key:
        await update.message.reply_text("❌ No encuentro API_FOOTBALL_KEY en Railway.")
        return
    ahora = datetime.now(TZ)
    try:
        partidos = _get("fixtures", {
            "league": LALIGA_ID,
            "season": _temporada(ahora),
            "from": ahora.date().isoformat(),
            "to": (ahora.date() + timedelta(days=2)).isoformat(),
            "timezone": "Atlantic/Canary",
        })
    except Exception as e:
        await update.message.reply_text(f"❌ API-Football responde con error:\n{e}")
        return
    if not partidos:
        await update.message.reply_text("✅ API-Football conecta bien. No hay partidos de LaLiga en las próximas 48 horas.")
        return
    lineas = ["✅ API-Football conecta bien.\n", "Próximos partidos detectados:"]
    for item in partidos[:10]:
        f = item["fixture"]
        dt = datetime.fromisoformat(f["date"]).astimezone(TZ)
        lineas.append(f"• {item['teams']['home']['name']} - {item['teams']['away']['name']} · {dt:%d/%m %H:%M} · {f['status']['short']}")
    await update.message.reply_text("\n".join(lineas))
