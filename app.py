import streamlit as st
import random
import string
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Generador de Contraseñas", layout="wide")

# ---------------- ESTADOS ----------------
if "password" not in st.session_state:
    st.session_state.password = ""

if "lista" not in st.session_state:
    st.session_state.lista = []

if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = False

if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if "apellido" not in st.session_state:
    st.session_state.apellido = ""

if "extra" not in st.session_state:
    st.session_state.extra = 2


# ---------------- FUNCIONES ----------------

def transformar_texto(texto):
    nuevo = ""
    for letra in texto:
        if letra == "a" and random.random() < 0.5:
            nuevo += "4"
        elif letra == "e" and random.random() < 0.5:
            nuevo += "3"
        elif letra == "i" and random.random() < 0.5:
            nuevo += "1"
        elif letra == "o" and random.random() < 0.5:
            nuevo += "0"
        else:
            nuevo += letra
    return nuevo


def evaluar_seguridad(password):
    puntuacion = 0
    if len(password) >= 8:
        puntuacion += 25
    if any(c.isdigit() for c in password):
        puntuacion += 25
    if any(c.isalpha() for c in password):
        puntuacion += 25
    if any(c in "!@#$%^&*" for c in password):
        puntuacion += 25
    return puntuacion


# ---------------- MODO OSCURO ----------------

if st.session_state.modo_oscuro:
    st.markdown("""
        <style>
        .stApp {
            background-color: #0F172A;
            color: #E5E7EB;
        }

        input {
            color: white !important;
            background-color: #1E293B !important;
        }

        label {
            color: #E5E7EB !important;
        }

        div.stButton > button {
            background-color: #334155;
            color: white;
            border-radius: 8px;
        }

        div.stButton > button:hover {
            background-color: #475569;
        }
        </style>
    """, unsafe_allow_html=True)


# ---------------- UI ----------------

st.markdown("<h1 style='text-align:center;'>🔐 GENERADOR DE CONTRASEÑAS</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])

# ----------- IZQUIERDA -----------
with col1:
    st.subheader("DATOS PERSONALES")

    nombre = st.text_input("Nombre", value=st.session_state.nombre)
    apellido = st.text_input("Apellido", value=st.session_state.apellido)

    st.subheader("CONFIGURACIÓN")

    extra = st.number_input("Cantidad de símbolos", 1, 10, value=st.session_state.extra)

    # GENERAR
    if st.button("🔑 Generar contraseña"):
        base = transformar_texto((nombre + apellido).lower())
        simbolos = "0123456789!@#$%^&*"
        extra_sim = "".join(random.choice(simbolos) for _ in range(extra))
        st.session_state.password = base + extra_sim
        st.session_state.lista = []

    # GENERAR 5 (usa última contraseña si existe)
    if st.button("📑 Generar 5 contraseñas"):
        if st.session_state.password:
            base = st.session_state.password
        else:
            base = (nombre + apellido).lower()

        lista = []
        for _ in range(5):
            texto = transformar_texto(base)
            simbolos = "0123456789!@#$%^&*"
            lista.append(texto + random.choice(simbolos))

        st.session_state.lista = lista

    # ALEATORIA
    if st.button("🎲 Contraseña aleatoria"):
        caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
        st.session_state.password = "".join(random.choice(caracteres) for _ in range(12))
        st.session_state.lista = []

    # LIMPIAR (SIN ERRORES)
    if st.button("🧹 Limpiar"):
        st.session_state.password = ""
        st.session_state.lista = []
        st.session_state.nombre = ""
        st.session_state.apellido = ""
        st.session_state.extra = 2

    # MODO OSCURO
    if st.button("🌙 Modo oscuro / claro"):
        st.session_state.modo_oscuro = not st.session_state.modo_oscuro


# ----------- CENTRO -----------
with col2:
    st.subheader("RESULTADO")

    st.text_input("Contraseña", st.session_state.password)

    # COPIAR (forma segura)
    if st.session_state.password:
        st.code(st.session_state.password)
        st.write("📋 Copia manualmente la contraseña")

        score = evaluar_seguridad(st.session_state.password)
        st.progress(score)

        if score <= 25:
            st.error("Seguridad: Muy baja")
        elif score <= 50:
            st.warning("Seguridad: Baja")
        elif score <= 75:
            st.warning("Seguridad: Media")
        else:
            st.success("Seguridad: Alta")

    # LISTA EN CUADRO
    if st.session_state.lista:
        st.subheader("📦 Lista de contraseñas")
        with st.container(border=True):
            for p in st.session_state.lista:
                st.write("🔐", p)


# ----------- DERECHA -----------
with col3:
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

    if os.path.exists("logo.png"):
        st.image("logo.png", width=350)
    else:
        st.write("Logo no disponible")

    st.markdown("</div>", unsafe_allow_html=True)