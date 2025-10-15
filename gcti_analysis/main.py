# gcti_analysis/main.py
import os
import sys
import streamlit as st

# Asegura que el paquete se pueda importar si se ejecuta directamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analysis_utils import (
    generar_dataset_simulado,
    analizar_tmti,
    analizar_cumplimiento_riesgo
)

# -----------------------------------------------------------------
# FUNCIÓN PRINCIPAL DE STREAMLIT (MAIN)
# -----------------------------------------------------------------
def main():
    st.set_page_config(
        page_title="GCTI DIRESA - Análisis Estadístico",
        layout="wide",
        page_icon="📊"
    )

    st.title("📈 Sistema Interactivo de Análisis de Métricas GCTI (DIRESA Junín) 🇵🇪")
    st.markdown("---")
    
    # Generar el DataFrame simulado llamando a la función del módulo utils
    df = generar_dataset_simulado()

    # --------------------------
    # Barra lateral
    # --------------------------
    st.sidebar.title("Métricas de Gobierno TI (COBIT 2019)")
    st.sidebar.markdown("### Seleccione el Eje de Análisis:")

    # Estado de la página
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    if st.sidebar.button("📉 Eficiencia Operativa (TMTI)", key="tmti"):
        st.session_state.page = 'tmti'

    if st.sidebar.button("🛡️ Cumplimiento y Gobernanza", key="compliance"):
        st.session_state.page = 'compliance'

    st.sidebar.markdown("---")

    if st.sidebar.checkbox("🧾 Ver Data Simulada (Head)"):
        st.sidebar.dataframe(df.head())

    # --------------------------
    # Contenido principal
    # --------------------------
    if st.session_state.page == 'tmti':
        analizar_tmti(df)
    elif st.session_state.page == 'compliance':
        analizar_cumplimiento_riesgo(df)
    else:
        st.info(
            "👈 Utilice los botones de la barra lateral para ver el análisis estadístico "
            "proyectado de las métricas clave del GCTI."
        )


# -----------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# -----------------------------------------------------------------
if __name__ == "__main__":
    main()
