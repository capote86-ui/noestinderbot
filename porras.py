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
COMPETICIONES = [
    {"nombre": "LaLiga", "codigo": "PD", "busqueda": None},
    {"nombre": "Champions League", "codigo": "CL", "busqueda": None},
    {"nombre": "UEFA Nations League", "codigo": None, "busqueda": "UEFA Nations League"},
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
