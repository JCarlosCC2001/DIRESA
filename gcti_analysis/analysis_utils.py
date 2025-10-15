# gcti_analysis/analysis_utils.py
import pandas as pd
import numpy as np
import random
import uuid
from datetime import date, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st # Usamos st.cache_data, aunque el archivo no es de streamlit

# --- Configuración global para los análisis ---
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
# Nota: Streamlit maneja la presentación de las figuras generadas.

# -----------------------------------------------------------------
# 1. FUNCIÓN DE GENERACIÓN DE DATOS (GENERATOR)
# -----------------------------------------------------------------

@st.cache_data 
def generar_dataset_simulado(n_eventos=2500):
    """Genera el DataFrame con las métricas GCTI simuladas."""
    
    np.random.seed(42)
    random.seed(42)
    # [... CÓDIGO COMPLETO DE GENERACIÓN DE DATOS AQUÍ ...]
    
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
    INCUMPLIMIENTOS_BAI06 = ['Cambio No Autorizado en HCE', 'Problema de Infraestructura (por cambio no aprobado)', 'Error en Plataforma Cloud (sin control)']
    EVENTOS_DSS02 = ['Falla de Hardware', 'Problema de Red/Conectividad', 'Error de Aplicación', 'Petición de Servicio', 'Incidente de Seguridad Menor']
    
    tipo_evento_final = []
    for autorizado in es_autorizado:
        if autorizado == 0:
            tipo_evento_final.append(random.choice(INCUMPLIMIENTOS_BAI06))
        else:
            tipo_evento_final.append(random.choice(EVENTOS_DSS02))
            
    riesgo_criticidad = []
    for autorizado, prioridad in zip(es_autorizado, prioridades):
        if autorizado == 0:
            riesgo_criticidad.append(np.random.choice(['Crítico', 'Alto']))
        elif prioridad == 'Alta':
            riesgo_criticidad.append('Alto')
        elif prioridad == 'Media':
            riesgo_criticidad.append('Medio')
        else:
            riesgo_criticidad.append('Bajo')

    nivel_madurez_riesgo = np.full(n_eventos, 'Nivel 3') 

    start_date = date.today() - timedelta(days=180)
    date_range = [start_date + timedelta(days=i) for i in range(180)]
    fechas_registro = np.random.choice(date_range, size=n_eventos)
    
    data = {
        'ID_INCIDENTE': ids_incidentes,
        'PRIORIDAD': prioridades,
        'TIEMPO_RESOLUCION_MIN': tiempos_resolucion,
        'TIPO_EVENTO': tipo_evento_final,
        'ES_CAMBIO_AUTORIZADO': es_autorizado,
        'RIESGO_CRITICIDAD': riesgo_criticidad,
        'NIVEL_MADUREZ': nivel_madurez_riesgo,
        'FECHA_REGISTRO': fechas_registro
    }

    return pd.DataFrame(data)

# -----------------------------------------------------------------
# 2. FUNCIÓN DE ANÁLISIS 1: TMTI (DSS02) - COB02
# -----------------------------------------------------------------
def analizar_tmti(df):
    """Genera la visualización interactiva del TMTI para Alta Prioridad en Streamlit."""
    # (El código es idéntico al de la función en Interfaz_Analisis_GCTI_Streamlit.py)
    # ... (Se mantiene el código de Streamlit aquí para la visualización) ...
    st.header("📉 1. Eficiencia Operativa (DSS02)")
    st.markdown("🎯 **Métrica Clave:** **TMTI** para Alta Prioridad (Reducción de la Variabilidad)")
    st.markdown("---")
    
    df_alta = df[df['PRIORIDAD'] == 'Alta']['TIEMPO_RESOLUCION_MIN']
    estadisticos_tmt = df_alta.describe().round(2)
    media_tmt = estadisticos_tmt.loc['mean']
    std_tmt = estadisticos_tmt.loc['std']
    p90 = df_alta.quantile(0.9).round(2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Media TMTI (Minutos)", f"{media_tmt:.2f}")
    col2.metric("Desviación Estándar (σ)", f"{std_tmt:.2f}", help="Indica la baja variabilidad del servicio TO-BE.")
    col3.metric("Percentil 90 (P90)", f"{p90:.2f} min", help="El tiempo máximo de resolución para el 90% de los incidentes.")

    st.subheader("Distribución de Frecuencias:")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df_alta, kde=True, bins=30, color='#007ACC', edgecolor='black', ax=ax)
    ax.axvline(media_tmt, color='red', linestyle='--', linewidth=2, label=f'Media ({media_tmt:.2f} min)')
    ax.axvline(p90, color='green', linestyle='-', linewidth=2, label=f'P90 ({p90:.2f} min)')
    ax.set_title('Distribución del TMTI para Incidentes de ALTA Prioridad (Proceso DSS02)')
    ax.set_xlabel('Tiempo de Resolución (Minutos)')
    ax.legend()
    st.pyplot(fig)
    st.markdown(f"**Conclusión Proyectada:** La Desviación Estándar ($\sigma = {std_tmt:.2f}$) confirma la **estandarización** del proceso DSS02, eliminando el estancamiento operativo AS-IS.")


# -----------------------------------------------------------------
# 3. FUNCIÓN DE ANÁLISIS 2: CUMPLIMIENTO Y RIESGO (BAI06 / APO12 / MEA01) - COB03
# -----------------------------------------------------------------
def analizar_cumplimiento_riesgo(df):
    """Genera la visualización interactiva de Cumplimiento y Riesgo en Streamlit."""
    # (El código es idéntico al de la función en Interfaz_Analisis_GCTI_Streamlit.py)
    # ... (Se mantiene el código de Streamlit aquí para la visualización) ...
    st.header("🛡️ 2. Cumplimiento y Gobernanza (BAI06, APO12, MEA01)")
    st.markdown("---")

    # --- CUMPLIMIENTO BAI06 ---
    st.subheader("2.1 Índice de Incumplimiento de Cambios (BAI06)")
    conteo_cambios = df['ES_CAMBIO_AUTORIZADO'].value_counts()
    total_cambios = conteo_cambios.sum()
    cambios_no_autorizados = conteo_cambios.get(0, 0) 
    indice_incumplimiento = (cambios_no_autorizados / total_cambios) * 100
    
    estado = "✅ Cumple la Meta" if indice_incumplimiento < 5 else "⚠️ NO Cumple la Meta"
    st.metric("ÍNDICE DE INCUMPLIMIENTO", f"{indice_incumplimiento:.2f}%", delta=f"{estado}", delta_color="inverse")

    col_pie, col_bar = st.columns(2)
    
    # Gráfico 1: Proporción General
    with col_pie:
        fig_pie, ax_pie = plt.subplots()
        etiquetas = ['Autorizados', 'NO Autorizados']
        colores = ['#4CAF50', '#F44336']
        ax_pie.pie(conteo_cambios, labels=etiquetas, autopct='%1.2f%%', startangle=90, colors=colores)
        ax_pie.set_title('Proporción de Cumplimiento BAI06')
        st.pyplot(fig_pie)
    
    # Gráfico 2: Desglose de Incumplimientos
    with col_bar:
        df_incumplimiento = df[df['ES_CAMBIO_AUTORIZADO'] == 0]
        if not df_incumplimiento.empty:
            fig_bar, ax_bar = plt.subplots()
            sns.countplot(y='TIPO_EVENTO', data=df_incumplimiento, 
                          order=df_incumplimiento['TIPO_EVENTO'].value_counts().index, 
                          palette='Reds_d', ax=ax_bar)
            ax_bar.set_title('Desglose de Tipos de Incumplimientos')
            ax_bar.set_xlabel('Frecuencia')
            st.pyplot(fig_bar)
    
    # --- RIESGO APO12 Y MADUREZ MEA01 ---
    st.markdown("---")
    st.subheader("2.2 Nivel de Riesgo (APO12) y Madurez (MEA01)")
    st.markdown("**Meta TO-BE:** Nivel 3: Definido")
    
    col_risk, col_mat = st.columns(2)
    
    # Riesgo APO12
    with col_risk:
        orden_riesgo = ['Crítico', 'Alto', 'Medio', 'Bajo']
        conteo_riesgo = df['RIESGO_CRITICIDAD'].value_counts().reindex(orden_riesgo, fill_value=0)
        fig_risk, ax_risk = plt.subplots()
        sns.barplot(x=conteo_riesgo.index, y=conteo_riesgo.values, palette='viridis', ax=ax_risk)
        ax_risk.set_title('Distribución de Eventos por Nivel de Riesgo (APO12)')
        ax_risk.set_xlabel('Criticidad')
        st.pyplot(fig_risk)

    # Madurez MEA01
    with col_mat:
        conteo_madurez = df['NIVEL_MADUREZ'].value_counts()
        madurez_presente = conteo_madurez[conteo_madurez > 0] 
        fig_mat, ax_mat = plt.subplots()
        ax_mat.pie(madurez_presente.values, labels=madurez_presente.index, autopct='%1.1f%%', startangle=90, colors=['#4CAF50'])
        ax_mat.set_title('Nivel de Madurez Proyectado (MEA01 - Meta Nivel 3)')
        st.pyplot(fig_mat)