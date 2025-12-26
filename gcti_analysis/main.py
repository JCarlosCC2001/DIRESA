import os
import sys
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analysis_utils import (
    generar_dataset_simulado,
    analizar_tmti,
    analizar_cumplimiento_riesgo,
    cargar_datos_reales,
    mostrar_impacto_anemia,
    mostrar_analisis_geografico
)

def main():
    st.set_page_config(page_title="GCTI DIRESA Junín", layout="wide", page_icon="📊")

    st.title("📈 Sistema de Métricas GCTI (DIRESA Junín) 🇵🇪")
    st.markdown("---")
    
    df = generar_dataset_simulado()

    # Barra Lateral
    st.sidebar.title("Menú de Control")
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    if st.sidebar.button("📉 Eficiencia Operativa (TMTI)"):
        st.session_state.page = 'tmti'

    if st.sidebar.button("🛡️ Cumplimiento y Riesgos"):
        st.session_state.page = 'compliance'

    st.sidebar.markdown("---")
    st.sidebar.subheader("📂 Cargar Datos de Anemia")
    archivo_real = st.sidebar.file_uploader("Archivo CSV/Excel (Junín)", type=["xlsx", "csv"])

    df_real = None
    if archivo_real:
        df_real = cargar_datos_reales(archivo_real)
        if df_real is not None:
            st.sidebar.success("✅ Dataset real vinculado")

    # Contenido Principal
    if st.session_state.page == 'tmti':
        tab_tec, tab_soc = st.tabs(["📊 Métricas Técnicas", "🏥 Impacto Social"])
        
        with tab_tec:
            analizar_tmti(df)
            
        with tab_soc:
            mostrar_impacto_anemia(df)
            if df_real is not None:
                st.markdown("---")
                mostrar_analisis_geografico(df_real)

    elif st.session_state.page == 'compliance':
        analizar_cumplimiento_riesgo(df)
        
    else:
        st.info("👈 Seleccione una métrica en la barra lateral para comenzar.")

if __name__ == "__main__":
    main()