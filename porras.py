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
