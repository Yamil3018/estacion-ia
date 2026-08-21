import streamlit as st
import sqlite3
from datetime import datetime
import os

# Configuración de la página
st.set_page_title_config = st.set_page_config(
    page_title="Humano Digital - Estación IA",
    page_icon="🤖",
    layout="wide"
)

# --- 1. CONFIGURACIÓN DE LA BASE DE DATOS ---
def inicializar_bd():
    conn = sqlite3.connect("estacion_ia.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            fecha_hora TEXT
        )
    """)
    conn.commit()
    conn.close()

inicializar_bd()

def guardar_visita(nombre):
    conn = sqlite3.connect("estacion_ia.db")
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO visitas (nombre, fecha_hora) VALUES (?, ?)", (nombre, fecha))
    conn.commit()
    conn.close()

# --- 2. INTERFAZ VISUAL ---
st.title("🤖 HUMANO DIGITAL — ESTACIÓN DE INTELIGENCIA ARTIFICIAL")
st.markdown("---")

# Menú lateral para alternar entre la Estación Interactiva y el Panel de Control
menu = st.sidebar.selectbox("Navegación", ["Estación de Recepción", "Panel de Consultas (Base de Datos)"])

if menu == "Estación de Recepción":
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Visualización del Avatar & Detección")
        
        # Avatar animado mediante GIF integrado (reemplaza al emoji por un asistente visual animado)
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHp1dzg5c2FobGNxcm5wMG1vYXZhZWlsOG5ucmlwcWZ6bXoxdmpsOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L1R1tvI9svkIWwpVYr/giphy.gif" width="300" style="border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.2);">
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.info("👀 Estado: Monitoreando presencia... (El avatar digital se encuentra activo)")

    with col2:
        st.subheader("Interacción por Voz y Registro")
        
        # Saludo inicial simulado con síntesis de voz nativa del navegador vía HTML/JS
        saludo_texto = "¡Hola! Bienvenido a nuestra estación de tecnología."
        st.markdown(f"**🤖 Avatar dice:** *\"{saludo_texto}\"*")
        
        # Componente JavaScript para reproducir audio con la voz del navegador automáticamente al cargar
        js_voz = f"""
        <script>
            function hablar() {{
                const utterance = new SpeechSynthesisUtterance("{saludo_texto}");
                utterance.lang = 'es-ES';
                window.speechSynthesis.speak(utterance);
            }}
            window.onload = hablar;
        </script>
        """
        st.components.v1.html(js_voz, height=0)

        st.markdown("### Registro de Visitante")
        
        # Captura de nombre (Permite simular respuesta por voz o entrada directa por campo optimizado)
        nombre_visitante = st.text_input("❓ Por favor, ingresa o dicta tu nombre:")
        
        if st.button("Registrar Visita y Despedir"):
            if nombre_visitante.strip() != "":
                guardar_visita(nombre_visitante.strip())
                st.success(f"¡Registro exitoso! Guardado en la base de datos.")
                
                # Despedida por voz
                despedida = f"Fue un placer atenderte, {nombre_visitante}. ¡Hasta pronto!"
                st.markdown(f"**🤖 Avatar dice:** *\"{despedida}\"*")
                
                js_despedida = f"""
                <script>
                    const utterance = new SpeechSynthesisUtterance("{despedida}");
                    utterance.lang = 'es-ES';
                    window.speechSynthesis.speak(utterance);
                </script>
                """
                st.components.v1.html(js_despedida, height=0)
            else:
                st.warning("Por favor, ingresa un nombre válido antes de registrar.")

else:
    # --- 3. PANEL DE CONTROL / CONSULTAS ---
    st.subheader("📊 Panel de Control y Estadísticas de Visitas")
    
    conn = sqlite3.connect("estacion_ia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, fecha_hora FROM visitas ORDER BY id DESC")
    registros = cursor.fetchall()
    conn.close()

    # Métricas rápidas
    total_visitas = len(registros)
    st.metric(label="Total de Personas Atendidas", value=total_visitas)
    
    st.markdown("### Historial de Ingresos")
    if total_visitas > 0:
        # Mostrar tabla organizada de registros
        import pandas as pd
        df = pd.DataFrame(registros, columns=["ID", "Nombre", "Fecha y Hora"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay registros guardados en la base de datos.")