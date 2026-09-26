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
API_FOOTBALL_BASE = "https://v3.football.api-sports.io"
NATIONS_LEAGUE_ID = 5
COMPETICIONES = [
    {"nombre": "LaLiga", "codigo": "PD", "busqueda": None},
    {"nombre": "Champions League", "codigo": "CL", "busqueda": None},
]

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


def _api_football_key():
    return (
        os.getenv("API_FOOTBALL_KEY")
        or os.getenv("APISPORTS_KEY")
        or os.getenv("API_SPORTS_KEY")
        or os.getenv("X_APISPORTS_KEY")
    )


def _get_api_football(endpoint, params=None):
    key = _api_football_key()
    if not key:
        raise RuntimeError("Falta API_FOOTBALL_KEY en Railway")

    url = f"{API_FOOTBALL_BASE}/{endpoint.lstrip('/')}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(
        url,
        headers={
            "x-apisports-key": key,
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            payload = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            cuerpo = e.read().decode("utf-8")
        except Exception:
            cuerpo = str(e)
        raise RuntimeError(f"API-Football HTTP {e.code}: {cuerpo}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"No se pudo conectar con API-Football: {e.reason}") from e

    if payload.get("errors"):
        raise RuntimeError(f"API-Football: {payload['errors']}")

    return payload.get("response", [])


def _temporada_nations(ahora):
    # Nations League 2026/27 se identifica como season=2026.
    return ahora.year if ahora.month >= 7 else ahora.year - 1


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



def _resolver_competicion(config):
    """Devuelve código/id utilizable o None si la competición no está disponible."""
    if config.get("codigo"):
        return config["codigo"]

    nombre_buscado = (config.get("busqueda") or config.get("nombre") or "").lower()

    try:
        payload = _get("competitions")
    except Exception as e:
        print(f"PORRAS: no se pudo listar competiciones: {e}")
        return None

    for comp in payload.get("competitions", []):
        nombre = (comp.get("name") or "").lower()
        if nombre == nombre_buscado or nombre_buscado in nombre:
            return comp.get("code") or comp.get("id")

    return None


def _es_recurso_restringido(error):
    texto = str(error)
    return "HTTP 403" in texto or "Restricted Resource" in texto


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


def _texto_porra(local, visitante, inicio, competicion="FÚTBOL"):
    return (
        f"⚽ 🏆 PORRA · {competicion.upper()} 🏆 ⚽\n\n"
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


async def _procesar_partido(context, datos, item, permitir_publicar=True, competicion='Fútbol'):
    """Sincroniza un partido de football-data.org con el estado persistido."""
    ahora = datetime.now(TZ)

    fid = str(item.get("id"))
    if not fid or fid == "None":
        return False

    try:
        inicio = _parsear_fecha_utc(item["utcDate"])
    except Exception:
        return False

    estado = item.get("status", "")
    local = (item.get("homeTeam") or {}).get("name", "Local")
    visitante = (item.get("awayTeam") or {}).get("name", "Visitante")
    registro = datos["partidos"].get(fid)
    cambiado = False

    # Publica desde 36 horas antes hasta el comienzo.
    if (
        permitir_publicar
        and registro is None
        and timedelta(0) < (inicio - ahora) <= timedelta(hours=PUBLICAR_HORAS_ANTES)
        and estado in ESTADOS_PROGRAMADOS
    ):
        try:
            msg = await context.bot.send_message(
                chat_id=GRUPO_PRINCIPAL_ID,
                text=_texto_porra(local, visitante, inicio, competicion),
            )

            datos["partidos"][fid] = {
                "match_id": int(fid),
                "message_id": msg.message_id,
                "chat_id": GRUPO_PRINCIPAL_ID,
                "local": local,
                "visitante": visitante,
                "inicio": inicio.isoformat(),
                "competicion": competicion,
                "estado": "abierta",
                "predicciones": {},
                "resuelta": False,
            }

            cambiado = True
            registro = datos["partidos"][fid]
            print(f"PORRAS: publicada {local} - {visitante}")

        except Exception as e:
            print("PORRAS: error publicando porra:", e)
            return cambiado

    if not registro:
        return cambiado

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

        if gh is not None and ga is not None:
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

    return cambiado


async def _procesar_partido_api_football(context, datos, item, permitir_publicar=True):
    ahora = datetime.now(TZ)

    fixture = item.get("fixture") or {}
    teams = item.get("teams") or {}
    goals = item.get("goals") or {}

    fid = fixture.get("id")
    if fid is None:
        return False

    clave = f"api-football:{fid}"

    try:
        inicio = datetime.fromisoformat(fixture["date"]).astimezone(TZ)
    except Exception:
        return False

    estado = (fixture.get("status") or {}).get("short", "")
    local = (teams.get("home") or {}).get("name", "Local")
    visitante = (teams.get("away") or {}).get("name", "Visitante")
    registro = datos["partidos"].get(clave)
    cambiado = False

    if (
        permitir_publicar
        and registro is None
        and timedelta(0) < (inicio - ahora) <= timedelta(hours=PUBLICAR_HORAS_ANTES)
        and estado == "NS"
    ):
        try:
            msg = await context.bot.send_message(
                chat_id=GRUPO_PRINCIPAL_ID,
                text=_texto_porra(local, visitante, inicio, "UEFA Nations League"),
            )

            datos["partidos"][clave] = {
                "provider": "api-football",
                "fixture_id": int(fid),
                "message_id": msg.message_id,
                "chat_id": GRUPO_PRINCIPAL_ID,
                "local": local,
                "visitante": visitante,
                "inicio": inicio.isoformat(),
                "competicion": "UEFA Nations League",
                "estado": "abierta",
                "predicciones": {},
                "resuelta": False,
            }
            registro = datos["partidos"][clave]
            cambiado = True
            print(f"PORRAS: publicada Nations League {local} - {visitante}")
        except Exception as e:
            print("PORRAS: error publicando Nations League:", e)
            return cambiado

    if not registro:
        return cambiado

    if registro.get("estado") == "abierta" and (ahora >= inicio or estado != "NS"):
        registro["estado"] = "cerrada"
        cambiado = True

    if estado in {"FT", "AET", "PEN"} and not registro.get("resuelta"):
        gh = goals.get("home")
        ga = goals.get("away")
        if gh is not None and ga is not None:
            await _resolver(context, datos, registro, int(gh), int(ga))
            registro["resuelta"] = True
            registro["estado"] = "resuelta"
            registro["resultado"] = f"{gh}-{ga}"
            cambiado = True

    if estado in {"PST", "CANC", "ABD", "AWD", "WO"} and registro.get("estado") not in {"cancelada", "resuelta"}:
        registro["estado"] = "cancelada"
        cambiado = True
        try:
            await context.bot.send_message(
                chat_id=registro["chat_id"],
                reply_to_message_id=registro["message_id"],
                text=f"⚠️ La porra {local} - {visitante} queda anulada porque el partido figura como {estado}.",
            )
        except Exception as e:
            print("PORRAS: error avisando cancelación Nations League:", e)

    return cambiado


async def revisar_porras(context):
    """Consulta LaLiga, Champions y, si hay acceso, Nations League."""
    ahora = datetime.now(TZ)
    datos = _cargar()
    cambiado = False

    for config in COMPETICIONES:
        identificador = _resolver_competicion(config)

        if not identificador:
            print(f"PORRAS: no se encontró {config['nombre']}")
            continue

        try:
            payload = _get(
                f"competitions/{identificador}/matches",
                {
                    "dateFrom": ahora.date().isoformat(),
                    "dateTo": (ahora.date() + timedelta(days=2)).isoformat(),
                },
            )
            partidos = payload.get("matches", [])
        except Exception as e:
            if _es_recurso_restringido(e):
                print(f"PORRAS: {config['nombre']} no está disponible con el plan actual; se omite.")
                continue
            print(f"PORRAS: error consultando {config['nombre']}: {e}")
            continue

        for item in partidos:
            if await _procesar_partido(
                context,
                datos,
                item,
                permitir_publicar=True,
                competicion=config["nombre"],
            ):
                cambiado = True

    # UEFA Nations League usa API-Football como segunda fuente.
    try:
        partidos_nations = _get_api_football(
            "fixtures",
            {
                "league": NATIONS_LEAGUE_ID,
                "season": _temporada_nations(ahora),
                "from": ahora.date().isoformat(),
                "to": (ahora.date() + timedelta(days=2)).isoformat(),
                "timezone": "Atlantic/Canary",
            },
        )
        for item in partidos_nations:
            if await _procesar_partido_api_football(
                context,
                datos,
                item,
                permitir_publicar=True,
            ):
                cambiado = True
    except Exception as e:
        print(f"PORRAS: Nations League no disponible en API-Football: {e}")

    if cambiado:
        _guardar(datos)


async def restaurar_porras_pendientes(application) -> None:
    """
    Restaura la porra después de un reinicio o redeploy de Railway.

    - Conserva predicciones y ranking desde /data/porras_futbol.json.
    - Revisa cada partido ya publicado aunque el bot haya estado apagado varios días.
    - Cierra o resuelve los partidos que hayan empezado/terminado durante el reinicio.
    - Busca también próximas jornadas para publicar una porra si el bot vuelve
      dentro de la ventana de 36 horas.
    """
    if not DATA_FILE.parent.exists():
        print(
            "AVISO PORRAS: /data no existe. Para sobrevivir a redeploys "
            "de Railway necesitas un Volume persistente montado en /data."
        )

    datos = _cargar()
    cambiado = False

    # Primero recupera cualquier partido persistido que estuviera pendiente.
    for fid, registro in list(datos.get("partidos", {}).items()):
        if registro.get("resuelta") or registro.get("estado") == "cancelada":
            continue

        match_id = registro.get("match_id") or registro.get("fixture_id") or fid

        if registro.get("provider") == "api-football":
            try:
                items = _get_api_football("fixtures", {"id": int(match_id)})
                if not items:
                    continue
                item = items[0]
            except Exception as e:
                print(f"PORRAS: no se pudo restaurar Nations League {match_id}: {e}")
                continue

            if await _procesar_partido_api_football(
                application,
                datos,
                item,
                permitir_publicar=False,
            ):
                cambiado = True
            continue

        try:
            item = _get(f"matches/{int(match_id)}")
        except Exception as e:
            print(
                f"PORRAS: no se pudo restaurar el partido {match_id}: {e}"
            )
            continue

        if await _procesar_partido(
            application,
            datos,
            item,
            permitir_publicar=False,
            competicion=registro.get("competicion", "Fútbol"),
        ):
            cambiado = True

    if cambiado:
        _guardar(datos)

    # Después comprueba próximos partidos por si el bot se reinició justo
    # cuando debía publicar una porra.
    await revisar_porras(application)


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
    """Diagnóstico de las competiciones configuradas."""
    token = _api_token()
    if not token:
        await update.message.reply_text("❌ No encuentro FOOTBALL_DATA_TOKEN en Railway.")
        return

    ahora = datetime.now(TZ)
    lineas = ["⚽ ESTADO DE LAS PORRAS\n"]

    for config in COMPETICIONES:
        identificador = _resolver_competicion(config)

        if not identificador:
            lineas.append(f"⚠️ {config['nombre']}: no localizada por la API.")
            continue

        try:
            payload = _get(
                f"competitions/{identificador}/matches",
                {
                    "dateFrom": ahora.date().isoformat(),
                    "dateTo": (ahora.date() + timedelta(days=2)).isoformat(),
                },
            )
            partidos = payload.get("matches", [])
        except Exception as e:
            if _es_recurso_restringido(e):
                lineas.append(f"🔒 {config['nombre']}: no incluida en tu plan actual.")
            else:
                lineas.append(f"❌ {config['nombre']}: {e}")
            continue

        if not partidos:
            lineas.append(f"✅ {config['nombre']}: conecta bien; sin partidos en 48 h.")
            continue

        lineas.append(f"✅ {config['nombre']}:")
        for item in partidos[:6]:
            try:
                dt = _parsear_fecha_utc(item["utcDate"])
            except Exception:
                continue

            local = (item.get("homeTeam") or {}).get("name", "Local")
            visitante = (item.get("awayTeam") or {}).get("name", "Visitante")
            estado = item.get("status", "?")
            lineas.append(f"• {local} - {visitante} · {dt:%d/%m %H:%M} · {estado}")

    # Nations League: segunda API.
    key_nations = _api_football_key()
    if not key_nations:
        lineas.append("🔑 UEFA Nations League: falta API_FOOTBALL_KEY en Railway.")
    else:
        try:
            partidos_nations = _get_api_football(
                "fixtures",
                {
                    "league": NATIONS_LEAGUE_ID,
                    "season": _temporada_nations(ahora),
                    "from": ahora.date().isoformat(),
                    "to": (ahora.date() + timedelta(days=2)).isoformat(),
                    "timezone": "Atlantic/Canary",
                },
            )

            if not partidos_nations:
                lineas.append("✅ UEFA Nations League: conecta bien; sin partidos en 48 h.")
            else:
                lineas.append("✅ UEFA Nations League:")
                for item in partidos_nations[:8]:
                    fixture = item.get("fixture") or {}
                    teams = item.get("teams") or {}
                    try:
                        dt = datetime.fromisoformat(fixture["date"]).astimezone(TZ)
                    except Exception:
                        continue
                    local = (teams.get("home") or {}).get("name", "Local")
                    visitante = (teams.get("away") or {}).get("name", "Visitante")
                    estado = (fixture.get("status") or {}).get("short", "?")
                    lineas.append(f"• {local} - {visitante} · {dt:%d/%m %H:%M} · {estado}")
        except Exception as e:
            lineas.append(f"❌ UEFA Nations League (API-Football): {e}")

    await update.message.reply_text("\n".join(lineas))

