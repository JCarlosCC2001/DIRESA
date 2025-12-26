import pandas as pd
import numpy as np
import random
import uuid
from datetime import date, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Configuración estética para los gráficos
sns.set_style("whitegrid")

@st.cache_data 
def generar_dataset_simulado(n_eventos=2500):
    """Genera el DataFrame con las métricas GCTI simuladas."""
    np.random.seed(42)
    random.seed(42)
    
    ids_incidentes = [f"INC-{uuid.uuid4().hex[:8].upper()}" for _ in range(n_eventos)]
    prioridades = np.random.choice(['Alta', 'Media', 'Baja'], size=n_eventos, p=[0.25, 0.45, 0.30])
    
    tiempos_resolucion = []
    for p in prioridades:
        if p == 'Alta':
            tiempos_resolucion.append(round(np.random.uniform(30.0, 480.0), 2))
        elif p == 'Media':
            tiempos_resolucion.append(round(np.random.uniform(60.0, 1440.0), 2))
        else:
            tiempos_resolucion.append(round(np.random.uniform(120.0, 4320.0), 2))

    es_autorizado = np.random.choice([1, 0], size=n_eventos, p=[0.95, 0.05])
    INCUMPLIMIENTOS_BAI06 = ['Cambio No Autorizado en HCE', 'Problema de Infraestructura', 'Error en Plataforma Cloud']
    EVENTOS_DSS02 = ['Falla de Hardware', 'Problema de Red', 'Error de Aplicación', 'Petición de Servicio']
    
    tipo_evento_final = [random.choice(INCUMPLIMIENTOS_BAI06) if a == 0 else random.choice(EVENTOS_DSS02) for a in es_autorizado]
    
    riesgo_criticidad = []
    for a, p in zip(es_autorizado, prioridades):
        if a == 0: riesgo_criticidad.append(np.random.choice(['Crítico', 'Alto']))
        elif p == 'Alta': riesgo_criticidad.append('Alto')
        elif p == 'Media': riesgo_criticidad.append('Medio')
        else: riesgo_criticidad.append('Bajo')

    fechas = [date.today() - timedelta(days=random.randint(0, 180)) for _ in range(n_eventos)]
    
    return pd.DataFrame({
        'ID_INCIDENTE': ids_incidentes, 'PRIORIDAD': prioridades,
        'TIEMPO_RESOLUCION_MIN': tiempos_resolucion, 'TIPO_EVENTO': tipo_evento_final,
        'ES_CAMBIO_AUTORIZADO': es_autorizado, 'RIESGO_CRITICIDAD': riesgo_criticidad,
        'NIVEL_MADUREZ': 'Nivel 3', 'FECHA_REGISTRO': fechas
    })

def analizar_tmti(df):
    """Visualización técnica del TMTI."""
    st.subheader("📊 Análisis Estadístico de Tiempos (DSS02)")
    df_alta = df[df['PRIORIDAD'] == 'Alta']['TIEMPO_RESOLUCION_MIN']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Media TMTI", f"{df_alta.mean():.2f} min")
    col2.metric("Desviación (σ)", f"{df_alta.std():.2f} min")
    col3.metric("Percentil 90", f"{df_alta.quantile(0.9):.2f} min")

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(df_alta, kde=True, color='#007ACC', ax=ax)
    ax.set_title('Distribución de Resolución - Prioridad Alta')
    st.pyplot(fig)

def analizar_cumplimiento_riesgo(df):
    """Visualización de Gobernanza."""
    st.subheader("🛡️ Cumplimiento BAI06 y Riesgos APO12")
    col1, col2 = st.columns(2)
    with col1:
        conteo = df['ES_CAMBIO_AUTORIZADO'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(conteo, labels=['Autorizado', 'No Autorizado'], autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
        st.pyplot(fig)
    with col2:
        conteo_r = df['RIESGO_CRITICIDAD'].value_counts()
        st.bar_chart(conteo_r)

# --- NUEVAS FUNCIONES DE IMPACTO REAL ---

def cargar_datos_reales(uploaded_file):
    """Carga el dataset de anemia detectando el separador ';' de Junín."""
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file, sep=';', encoding='latin-1')
        else:
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error al cargar: {e}")
        return None

def mostrar_impacto_anemia(df_simulado):
    """Traduce métricas técnicas a impacto social."""
    st.subheader("🏥 Impacto en el Programa de Anemia - Junín")
    tiempos_altos = df_simulado[df_simulado['PRIORIDAD'] == 'Alta']['TIEMPO_RESOLUCION_MIN'].sum()
    horas_caidas = tiempos_altos / 60
    niños_afectados = int(horas_caidas * 40) # Estimación regional

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Horas de Sistema Inactivo", f"{horas_caidas:.1f} hrs", delta="Riesgo de Continuidad", delta_color="inverse")
    with col2:
        st.metric("Niños con atención en riesgo", f"{niños_afectados}", help="Niños menores de 36 meses afectados")
    
    st.info("💡 El Gobierno de TI asegura que el personal de salud tenga acceso constante a estos registros críticos.")

def mostrar_analisis_geografico(df_real):
    """Desglose por provincias del archivo real de la DIRESA."""
    if 'Provincia' in df_real.columns:
        st.write("### 📍 Cobertura por Provincias (Datos Reales)")
        conteo = df_real['Provincia'].value_counts()
        st.bar_chart(conteo)
        
        if 'hb_dx' in df_real.columns:
            st.write(f"**Media de Hemoglobina detectada en la muestra:** {df_real['hb_dx'].mean():.2f}")