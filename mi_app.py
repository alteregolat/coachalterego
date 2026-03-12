import streamlit as st
import datetime
import json
import os
import re
import hashlib
from garminconnect import Garmin
import google.generativeai as genai

# ================= TUS DATOS GLOBALES =================
GEMINI_API_KEY = "AIzaSyBzlm9iPGojsmPTnlXK1B3qq4_W9FpVnOQ" # (Asegúrate de ponerla)
# Ya no ponemos nombres de archivos fijos aquí.
# ======================================================

# --- FUNCIÓN PARA SEPARAR USUARIOS ---
def obtener_archivos_usuario(email):
    # Esto crea un código único basado en el correo (ej. rafa@mail.com -> rafa_123)
    # Así, tú tienes tus archivos y tu amigo tiene los suyos.
    id_usuario = hashlib.md5(email.encode()).hexdigest()[:8]
    return f"historial_{id_usuario}.json", f"semana_{id_usuario}.json"

st.set_page_config(page_title="Coach Alter Ego", page_icon="🧠", layout="wide")

# --- SISTEMA DE LOGIN ---
if "logueado" not in st.session_state: st.session_state.logueado = False

if not st.session_state.logueado:
    st.title("🔐 Acceso a Alter Ego")
    with st.form("login_form"):
        email = st.text_input("Correo Garmin")
        password = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Conectar Reloj ⌚"):
            if email and password:
                try:
                    with st.spinner("Conectando con Garmin..."):
                        api_test = Garmin(email, password)
                        api_test.login()
                    st.session_state.email = email
                    st.session_state.password = password
                    # Aquí generamos los archivos únicos para la persona que acaba de entrar
                    hist, sem = obtener_archivos_usuario(email)
                    st.session_state.archivo_historial = hist
                    st.session_state.archivo_semana = sem
                    st.session_state.logueado = True
                    st.rerun()
                except: st.error("❌ Credenciales incorrectas.")
    st.stop()
# ------------------------
