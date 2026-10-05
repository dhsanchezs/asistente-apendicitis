import streamlit as st

st.set_page_config(
    page_title="Asistente Virtual de Dolor de Barriga",
    page_icon="🩺",
    layout="wide"
)

# Encabezado para el usuario común
st.title("🩺 Asistente Virtual: ¿Podría ser Apendicitis?")
st.markdown("""
**¡Hola!** Este sistema te hará 5 preguntas sencillas sobre tu dolor de barriga para recomendarte qué hacer. 
""")

st.divider()

col_input, col_output = st.columns([1, 1])

with col_input:
    st.header("Tus Síntomas")
    st.info("Responde estas preguntas según lo que sientes en este momento:")

    localizacion_dolor = st.radio(
        "1. ¿Dónde sientes el dolor más fuerte?",
        options=["fosa_iliaca_derecha", "difuso_otro"],
        format_func=lambda x: "Abajo a la derecha (cerca de la ingle)" if x == "fosa_iliaca_derecha" else "En toda la barriga, arriba o en otra parte",
        index=0
    )

    migracion_dolor = st.radio(
        "2. ¿El dolor empezó cerca del ombligo (o en la boca del estómago) y luego bajó hacia la derecha?",
        options=["si", "no"],
        format_func=lambda x: "Sí, se movió hacia abajo a la derecha" if x == "si" else "No, siempre ha dolido en el mismo lugar",
        index=0
    )

    signos_peritoneales = st.radio(
        "3. Haz esta prueba con cuidado: presiona tu barriga con los dedos y suelta de golpe. ¿Te duele más al presionar o al soltar?",
        options=["blumberg_positivo", "negativo"],
        format_func=lambda x: "¡Me duele como una punzada fuerte justo al SOLTAR!" if x == "blumberg_positivo" else "No hay un dolor fuerte al soltar",
        index=0
    )

    laboratorio_leucocitos = st.radio(
        "4. ¿Te han hecho un análisis de sangre hoy que diga que tienes infección (defensas altas)?",
        options=["leucocitosis", "normal"],
        format_func=lambda x: "Sí, el doctor me dijo que hay infección en la sangre" if x == "leucocitosis" else "No me he hecho análisis / Todo salió normal",
        index=1 # Por defecto en normal, ya que el usuario común no suele tenerlo
    )

    temperatura = st.radio(
        "5. ¿Te has medido la temperatura con un termómetro?",
        options=["fiebre", "normal"],
        format_func=lambda x: "Sí, tengo fiebre (más de 37.8 °C) o escalofríos" if x == "fiebre" else "No, mi temperatura es normal",
        index=1
    )

# Motor de Inferencia del Sistema Experto
def evaluar_apendicitis(loc_dolor, mig_dolor, sig_periton, leucos, temp):
    reglas_ejecutadas = []

    # Nodo 1: Evaluando sospecha del dolor
    if loc_dolor == "fosa_iliaca_derecha" or mig_dolor == "si":
        sospecha_dolor = "alta_sospecha"
        reglas_ejecutadas.append("Regla 6: Dolor en zona baja derecha o que se mueve hacia allá = Sospecha Alta")
    else:
        sospecha_dolor = "baja_sospecha"
        reglas_ejecutadas.append("Regla 7: Dolor en otro lado sin movimiento = Sospecha Baja")

    # Nodo 2: Evaluando inflamación interna (Irritación)
    if sig_periton == "blumberg_positivo" or leucos == "leucocitosis":
        irritacion_peritoneal = "presente"
        reglas_ejecutadas.append("Regla 8: Dolor al soltar la barriga o examen con infección = Hay inflamación interna")
    else:
        irritacion_peritoneal = "ausente"
        reglas_ejecutadas.append("Regla 9: Sin dolor al soltar y sin infección en sangre = No hay inflamación interna evidente")

    # Nodo 3: Decisión Final
    if sospecha_dolor == "alta_sospecha" and irritacion_peritoneal == "presente":
        conducta = "Cirugia_Inmediata"
        reglas_ejecutadas.append("Regla 1: Sospecha Alta + Inflamación Interna -> Riesgo crítico de Apendicitis")
    elif sospecha_dolor == "alta_sospecha" and irritacion_peritoneal == "ausente":
        conducta = "Observacion_Hospitalaria"
        reglas_ejecutadas.append("Regla 2: Sospecha Alta pero sin inflamación clara -> Necesita chequeo médico")
    elif sospecha_dolor == "baja_sospecha" and irritacion_peritoneal == "presente":
        conducta = "Observacion_Hospitalaria"
        reglas_ejecutadas.append("Regla 3: Sospecha Baja pero CON inflamación interna -> Necesita chequeo médico")
    elif sospecha_dolor == "baja_sospecha" and irritacion_peritoneal == "ausente" and temp == "fiebre":
        conducta = "Observacion_Hospitalaria"
        reglas_ejecutadas.append("Regla 4: Sospecha Baja sin inflamación, pero tiene FIEBRE -> Revisión por seguridad")
    else:
        conducta = "Alta_Manejo_Ambulatorio"
        reglas_ejecutadas.append("Regla 5: Sospecha Baja + Sin inflamación + Sin fiebre -> Riesgo muy bajo de Apendicitis")

    return sospecha_dolor, irritacion_peritoneal, conducta, reglas_ejecutadas


with col_output:
    st.header("Resultados y Qué hacer")

    sospecha, irritacion, conducta, trazabilidad = evaluar_apendicitis(
        localizacion_dolor, migracion_dolor, signos_peritoneales, laboratorio_leucocitos, temperatura
    )

    st.subheader("Tu recomendación:")

    if conducta == "Cirugia_Inmediata":
        st.error("🚨 **VE INMEDIATAMENTE A EMERGENCIAS**")
        st.write("Tus síntomas son **muy parecidos a los de una apendicitis**. No comas ni bebas nada, y dirígete al hospital más cercano para que un cirujano te evalúe de inmediato.")
    elif conducta == "Observacion_Hospitalaria":
        st.warning("⚠️ **DEBES IR AL MÉDICO HOY**")
        st.write("Tus síntomas son dudosos. Podría ser el inicio de una apendicitis o alguna otra infección. Ve a urgencias o a un médico general pronto para que te hagan una ecografía o análisis.")
    else:
        st.success("✅ **RIESGO BAJO (QUÉDATE TRANQUILO POR AHORA)**")
        st.write("Tus síntomas **no parecen ser apendicitis**. Probablemente sea un malestar estomacal común. Descansa, mantente hidratado. Si el dolor empeora de golpe o te da fiebre alta, ve al médico.")

    st.markdown("---")
    st.subheader("💡 ¿Cómo llegó el sistema a esta conclusión?")
    st.write("El sistema experto aplicó estas reglas automáticas basadas en tus respuestas:")
    for r in trazabilidad:
        st.info(r)