"""
Portfolio Analyzer Pro - Aplicación Principal Streamlit
Análisis cuantitativo de portafolios con optimización de Markowitz
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import plotly.graph_objects as go
import plotly.express as px
import warnings
import os

# Importar módulos personalizados
from modules import (
    descargar_datos,
    calcular_rendimientos,
    validar_datos,
    calcular_metricas_activos,
    prueba_normalidad,
    matriz_correlacion,
    OptimizadorPortafolios,
    plot_precios_historicos,
    plot_frontera_eficiente,
    plot_correlacion_heatmap,
    plot_asignacion_pesos,
    plot_rendimientos_diarios,
    plot_retorno_riesgo,
    plot_comparativa_portafolios,
    plot_simulacion_montecarlo,
    simular_portafolios_montecarlo,
    calcular_estadisticas_simulacion
)

warnings.filterwarnings('ignore')

# ============================================
# CONFIGURACIÓN INICIAL
# ============================================

st.set_page_config(
    page_title="Portfolio Analyzer Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Obtener directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config", "parametros_default.json")

# Cargar configuración
with open(config_path, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

# Estilos CSS
st.markdown("""
    <style>
    .titulo-principal {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .subtitulo {
        text-align: center;
        font-size: 16px;
        color: #666;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .portafolio-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# INICIALIZAR SESSION STATE
# ============================================

if 'datos_cargados' not in st.session_state:
    st.session_state.datos_cargados = False
if 'precios' not in st.session_state:
    st.session_state.precios = None
if 'rendimientos' not in st.session_state:
    st.session_state.rendimientos = None
if 'optimizador' not in st.session_state:
    st.session_state.optimizador = None
if 'portafolios' not in st.session_state:
    st.session_state.portafolios = None
if 'simulaciones' not in st.session_state:
    st.session_state.simulaciones = None

# ============================================
# INTERFAZ PRINCIPAL
# ============================================

st.markdown('<div class="titulo-principal">📈 PORTFOLIO ANALYZER PRO</div>', 
            unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Análisis Cuantitativo de Portafolios con Optimización de Markowitz</div>',
            unsafe_allow_html=True)

# ============================================
# SIDEBAR - CONFIGURACIÓN
# ============================================

st.sidebar.title("⚙️ CONFIGURACIÓN")

# Selección de activos
with st.sidebar.expander("📌 Seleccionar Activos", expanded=True):
    
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker_input = st.text_input(
            "Ingresa tickers separados por comas",
            value="AAPL,MSFT,GOOGL,TSLA,AMZN",
            help="Usa tickers válidos de Yahoo Finance"
        )
    
    activos = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
    
    if activos:
        st.sidebar.success(f"✅ {len(activos)} activos seleccionados: {', '.join(activos)}")
    else:
        st.sidebar.error("⚠️ Ingresa al menos un activo")
        activos = ["AAPL"]

# Período de datos
with st.sidebar.expander("📅 Período de Datos", expanded=True):
    
    tipoPeriodo = st.radio(
        "Selecciona opciones:",
        ["Período predefinido", "Fechas personalizadas"],
        key="tipo_periodo"
    )
    
    if tipoPeriodo == "Período predefinido":
        periodo = st.selectbox(
            "Rango histórico:",
            ["1y", "2y", "5y", "10y", "max"],
            index=1
        )
        fecha_inicio = None
    else:
        fecha_inicio = st.date_input(
            "Desde:",
            value=datetime.now() - timedelta(days=365*2)
        )
        fecha_fin = st.date_input("Hasta:", value=datetime.now())
        periodo = None

# Parámetros de inversión
with st.sidebar.expander("💰 Parámetros de Inversión", expanded=True):
    
    col_monto, col_tasa, col_rd = st.columns(3)
    with col_monto:
        monto_inversion = st.number_input(
            "Monto a invertir ($):",
            min_value=1000,
            value=100_000,
            step=10_000
        )
    
    with col_tasa:
        tasa_rf_anual = st.number_input(
            "Tasa RF anual (%):",
            min_value=0.0,
            max_value=20.0,
            value=3.0,
            step=0.0001,
            format="%.4f",
            help="⏪ Tasa ANUALIZADA (ej: 3% anual = 3). Se divide automáticamente por 100 internamente."
        )
    
    with col_rd:
        rend_deseado_pct = st.number_input(
            "Rendimiento deseado (%):",
            min_value=0.0,
            max_value=100.0,
            value=8.0,
            step=0.0001,
            format="%.4f",
            help="⏪ Rendimiento ANUALIZADO (ej: 8% anual = 8). Se divide automáticamente por 100 internamente."
        )

# Restricciones
with st.sidebar.expander("⚠️ Restricciones y Simulación", expanded=False):
    
    permitir_short = st.checkbox("Permitir ventas en corto", value=True)
    
    aplicar_limite = st.checkbox("Aplicar límite de riesgo máximo", value=False)
    
    if aplicar_limite:
        limite_riesgo = st.number_input(
            "Límite de riesgo máximo (%):",
            min_value=0.1,
            max_value=100.0,
            value=50.0,
            step=1.0,
            help="Solo mostrará portafolios simulados con riesgo ≤ este valor"
        )
        limites_riesgo_tuple = (0, limite_riesgo/100)
    else:
        limites_riesgo_tuple = None
    
    n_simulaciones = st.number_input(
        "N° de simulaciones Montecarlo:",
        min_value=1000,
        max_value=100_000,
        value=10_000,
        step=1000
    )

# Botón de procesamiento
col_btn1, col_btn2, col_btn3 = st.sidebar.columns(3)

with col_btn1:
    if st.button("🚀 EJECUTAR", use_container_width=True):
        st.session_state.ejecutar = True

with col_btn2:
    if st.button("🔄 RESETEAR", use_container_width=True):
        st.session_state.datos_cargados = False
        st.rerun()

with col_btn3:
    st.write("")

# ============================================
# PROCESAMIENTO PRINCIPAL
# ============================================

if 'ejecutar' in st.session_state or st.session_state.datos_cargados:
    
    with st.spinner("⏳ Descargando y procesando datos..."):
        try:
            # Descargar datos
            if not st.session_state.datos_cargados:
                if tipoPeriodo == "Período predefinido":
                    st.session_state.precios = descargar_datos(activos, periodo=periodo, progress=False)
                else:
                    st.session_state.precios = descargar_datos(
                        activos,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        progress=False
                    )
                
                # Calcular rendimientos
                st.session_state.rendimientos = calcular_rendimientos(st.session_state.precios)
                
                # Validar datos
                validar_datos(st.session_state.precios, min_observaciones=100)
                
                # Crear optimizador
                st.session_state.optimizador = OptimizadorPortafolios(
                    st.session_state.rendimientos,
                    tasa_rf=tasa_rf_anual/100,
                    monto_inversion=monto_inversion,
                    precios=st.session_state.precios.iloc[-1]
                )
                
                # Obtener rendimiento deseado (50% del portafolio de mercado por defecto)
                rend_mercado = st.session_state.optimizador.portafolio_mercado()['rendimiento']
                rend_deseado_default = rend_mercado * 0.8
                
                # Obtener portafolios óptimos con rendimiento deseado
                st.session_state.portafolios = st.session_state.optimizador.obtener_resumen_portafolios(
                    rend_deseado=rend_deseado_default
                )
                
                # Simular portafolios
                st.session_state.simulaciones = simular_portafolios_montecarlo(
                    st.session_state.rendimientos,
                    n_simulaciones=n_simulaciones,
                    permitir_short=permitir_short,
                    limites_riesgo=limites_riesgo_tuple,
                    tasa_rf=tasa_rf_anual/100
                )
                
                st.session_state.datos_cargados = True
            
            st.success("✅ Datos procesados correctamente")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()

# ============================================
# SECCIONES PRINCIPALES (TABS)
# ============================================

if st.session_state.datos_cargados:
    
    tabs = st.tabs([
        "📊 Datos & Estadísticas",
        "🎯 Portafolios Óptimos", 
        "🔗 Correlaciones",
        "📈 Visualizaciones",
        "🎲 Simulación Montecarlo",
        "📋 Reporte Ejecutivo"
    ])
    
    # ============================================
    # TAB 1: DATOS Y ESTADÍSTICAS
    # ============================================
    
    with tabs[0]:
        st.subheader("📊 Análisis de Datos Históricos")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Activos", len(activos))
        with col2:
            st.metric("Observaciones", len(st.session_state.precios))
        with col3:
            dias = len(st.session_state.precios)
            st.metric("Período", f"{dias} días")
        with col4:
            st.metric("Inversión", f"${monto_inversion:,.0f}")
        
        st.divider()
        
        col_stats, col_dist = st.columns([1.5, 1])
        
        with col_stats:
            st.write("**Estadísticas por Activo (Anualizadas)**")
            stats_df = calcular_metricas_activos(st.session_state.rendimientos)
            st.dataframe(stats_df, use_container_width=True)
        
        with col_dist:
            st.write("**Distribuciones**")
            activo_sel = st.selectbox("Activo:", activos, key="dist_select")
            
            rend_sel = st.session_state.rendimientos[activo_sel] * 100
            
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=rend_sel,
                nbinsx=50,
                name=activo_sel,
                marker_color='#1f77b4'
            ))
            fig_hist.update_layout(
                title=f"Distribución: {activo_sel}",
                xaxis_title="Retorno (%)",
                yaxis_title="Frecuencia",
                height=400,
                template="plotly_white"
            )
            st.plotly_chart(fig_hist, use_container_width=True, key="hist_activos")
        
        st.divider()
        
        st.write("**Prueba de Normalidad (Jarque-Bera)**")
        prueba_df = prueba_normalidad(st.session_state.rendimientos)
        st.dataframe(prueba_df, use_container_width=True)
        
        st.info("""
        💡 **Interpretación**: 
        - Si **P-value > 0.05**: No rechazamos normalidad
        - Si **P-value < 0.05**: Rechazamos normalidad
        - Activos reales generalmente fallan normalidad por colas gruesas y asimetría
        """)
    
    # ============================================
    # TAB 2: PORTAFOLIOS ÓPTIMOS
    # ============================================
    
    with tabs[1]:
        st.subheader("🎯 Portafolios Óptimos Construidos")
        
        # Mostrar 4 tarjetas de portafolios
        col_mr, col_m, col_rd, col_a = st.columns(4)
        
        nombres_portafolios = {
            'MR': ('🎯 Mínimo Riesgo', '#2ecc71'),
            'M': ('📈 Máximo Sharpe', '#e74c3c'),
            'RD': ('🎪 Rendimiento Deseado', '#f39c12'),
            'A': ('✅ Ajustado (No Short)', '#9b59b6')
        }
        
        cols_pf = [col_mr, col_m, col_rd, col_a]
        
        for col, (key, (label, color)) in zip(cols_pf, nombres_portafolios.items()):
            with col:
                pf = st.session_state.portafolios[key]
                
                st.markdown(f"""
                ### {label}
                - **Riesgo**: {pf['riesgo']*100:.2f}%
                - **Rendimiento**: {pf['rendimiento']*100:.2f}%
                - **Sharpe**: {pf['sharpe']:.3f}
                """)
        
        st.divider()
        
        # Tabla comparativa
        st.write("**📋 Comparativa de Pesos por Activo (%)**")
        tabla_pesos = st.session_state.optimizador.tabla_pesos_portafolios(
            rend_deseado=rend_deseado_pct/100
        )
        st.dataframe(tabla_pesos, use_container_width=True)
        
        st.divider()
        
        # Valuación
        st.write("**💰 Valuación y Posiciones**")
        
        col_val1, col_val2 = st.columns(2)
        
        with col_val1:
            portafolio_sel = st.selectbox(
                "Selecciona portafolio:",
                list(st.session_state.portafolios.keys()),
                key="portafolio_select"
            )
            
            pf_sel = st.session_state.portafolios[portafolio_sel]
            precios_actuales = st.session_state.precios.iloc[-1]
            
            valuacion = []
            for i, activo in enumerate(activos):
                peso = pf_sel['pesos'][i]
                monto = monto_inversion * peso
                precio = precios_actuales[activo]
                cantidad = monto / precio
                
                valuacion.append({
                    'Activo': activo,
                    'Peso (%)': peso * 100,
                    'Monto ($)': f"{monto:,.2f}",
                    'Precio ($)': f"{precio:.2f}",
                    'Cantidad': f"{cantidad:.4f}"
                })
            
            val_df = pd.DataFrame(valuacion)
            st.dataframe(val_df, use_container_width=True)
        
        with col_val2:
            st.write("**Gráfico de Asignación**")
            fig_asig = plot_asignacion_pesos(
                pf_sel['pesos'],
                activos,
                titulo=f"Asignación: {portafolio_sel}"
            )
            st.plotly_chart(fig_asig, use_container_width=True, key="pf_asignacion")
        
        st.divider()
        
        # Descarga de resultados
        st.write("**📥 Descargar Resultados**")
        
        csv = tabla_pesos.to_csv()
        st.download_button(
            label="📊 Descargar CSV (Pesos)",
            data=csv,
            file_name=f"portafolios_pesos_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # ============================================
    # TAB 3: CORRELACIONES
    # ============================================
    
    with tabs[2]:
        st.subheader("🔗 Análisis de Correlaciones")
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.write("**Matriz de Correlación**")
            corr_matrix = matriz_correlacion(st.session_state.rendimientos)
            
            fig_corr = plot_correlacion_heatmap(st.session_state.rendimientos)
            st.plotly_chart(fig_corr, use_container_width=True, key="viz_correlacion")
        
        with col2:
            st.write("**Estadísticas de Correlación**")
            
            # Convertir a array para análisis
            corr_array = corr_matrix.values.copy()
            np.fill_diagonal(corr_array, np.nan)
            
            corr_media = np.nanmean(corr_array)
            corr_max = np.nanmax(corr_array)
            corr_min = np.nanmin(corr_array)
            
            st.metric("Correlación Media", f"{corr_media:.3f}")
            st.metric("Correlación Máxima", f"{corr_max:.3f}")
            st.metric("Correlación Mínima", f"{corr_min:.3f}")
            
            # Pares más correlacionados
            st.write("**Pares Más Correlacionados**")
            
            pares = []
            for i in range(len(activos)):
                for j in range(i+1, len(activos)):
                    corr_val = corr_matrix.iloc[i, j]
                    pares.append({
                        'Par': f"{activos[i]}-{activos[j]}",
                        'Correlación': corr_val
                    })
            
            pares_df = pd.DataFrame(pares).sort_values('Correlación', ascending=False)
            st.dataframe(pares_df.head(5), use_container_width=True, hide_index=True)
    
    # ============================================
    # TAB 4: VISUALIZACIONES
    # ============================================
    
    with tabs[3]:
        st.subheader("📈 Gráficas Interactivas")
        
        viz_options = st.selectbox(
            "Selecciona visualización:",
            [
                "📈 Precios Históricos",
                "📊 Rendimientos Diarios",
                "📉 Frontera Eficiente",
                "🎒 Asignación de Pesos",
                "📏 Retorno vs Riesgo (por activo)",
                "📊 Comparativa de Portafolios"
            ],
            key="viz_select"
        )
        
        if viz_options == "📈 Precios Históricos":
            fig = plot_precios_historicos(st.session_state.precios)
            st.plotly_chart(fig, use_container_width=True, key="viz_precios")
        
        elif viz_options == "📊 Rendimientos Diarios":
            fig = plot_rendimientos_diarios(st.session_state.rendimientos)
            st.plotly_chart(fig, use_container_width=True, key="viz_rendimientos")
        
        elif viz_options == "📉 Frontera Eficiente":
            frontera = st.session_state.optimizador.frontera_eficiente(n_puntos=50)
            fig = plot_frontera_eficiente(frontera, st.session_state.portafolios)
            st.plotly_chart(fig, use_container_width=True, key="viz_frontera")
        
        elif viz_options == "🎒 Asignación de Pesos":
            portafolio_viz = st.selectbox("Portafolio:", 
                                          list(st.session_state.portafolios.keys()),
                                          key="viz_pf")
            pf_viz = st.session_state.portafolios[portafolio_viz]
            fig = plot_asignacion_pesos(pf_viz['pesos'], activos, f"Asignación: {portafolio_viz}")
            st.plotly_chart(fig, use_container_width=True, key="viz_pesos")
        
        elif viz_options == "📏 Retorno vs Riesgo (por activo)":
            activos_stats = []
            for activo in activos:
                rend = st.session_state.rendimientos[activo]
                activos_stats.append({
                    'Activo': activo,
                    'Riesgo': rend.std() * np.sqrt(252) * 100,
                    'Rendimiento': rend.mean() * 252 * 100
                })
            
            activos_df = pd.DataFrame(activos_stats)
            fig = plot_retorno_riesgo(activos_df)
            st.plotly_chart(fig, use_container_width=True, key="viz_riesgo")
        
        elif viz_options == "📊 Comparativa de Portafolios":
            tabla_pesos = st.session_state.optimizador.tabla_pesos_portafolios(
                rend_deseado=rend_deseado_pct/100
            )
            fig = plot_comparativa_portafolios(tabla_pesos)
            st.plotly_chart(fig, use_container_width=True, key="viz_comparativa")
    
    # ============================================
    # TAB 5: SIMULACIÓN MONTECARLO
    # ============================================
    
    with tabs[4]:
        st.subheader("🎲 Simulación de Portafolios Aleatorios")
        
        # Obtener frontera eficiente para la visualización
        with st.spinner("⏳ Generando frontera eficiente..."):
            frontera_eficiente = st.session_state.optimizador.frontera_eficiente(
                n_puntos=100
            )
            print(f"✅ Frontera eficiente generada: {len(frontera_eficiente)} puntos" if frontera_eficiente is not None and len(frontera_eficiente) > 0 else "❌ Frontera eficiente vacía")
            if frontera_eficiente is not None and len(frontera_eficiente) > 0:
                print(f"   Riesgo min/max: {frontera_eficiente['riesgo'].min():.6f} - {frontera_eficiente['riesgo'].max():.6f}")
                print(f"   Return min/max: {frontera_eficiente['rendimiento'].min():.6f} - {frontera_eficiente['rendimiento'].max():.6f}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**{len(st.session_state.simulaciones):,} Portafolios Simulados**")
            fig_sim = plot_simulacion_montecarlo(
                st.session_state.simulaciones,
                st.session_state.portafolios,
                "Simulación Montecarlo",
                frontiera_ef=frontera_eficiente,
                tasa_rf=tasa_rf_anual/100
            )
            st.plotly_chart(fig_sim, use_container_width=True, key="viz_simulacion")
        
        with col2:
            st.write("**Estadísticas de Simulación**")
            stats_sim = calcular_estadisticas_simulacion(st.session_state.simulaciones)
            
            st.metric("Riesgo Promedio", f"{stats_sim['Riesgo_Promedio']*100:.2f}%")
            st.metric("Rendimiento Promedio", f"{stats_sim['Rendimiento_Promedio']*100:.2f}%")
            st.metric("Máx Sharpe", f"{stats_sim['Sharpe_Max']:.3f}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Riesgo Mín", f"{stats_sim['Riesgo_Min']*100:.2f}%")
            with col_b:
                st.metric("Riesgo Máx", f"{stats_sim['Riesgo_Max']*100:.2f}%")
    
    # ============================================
    # TAB 6: REPORTE EJECUTIVO
    # ============================================
    
    with tabs[5]:
        st.subheader("📋 Reporte Ejecutivo")
        
        col_d1, col_d2, col_d3 = st.columns(3)
        
        with col_d1:
            # Crear CSV para descargar
            resumen_csv = "Portafolio,Riesgo (%),Rendimiento (%),Sharpe\n"
            for nombre, pf in st.session_state.portafolios.items():
                resumen_csv += f"{nombre},{pf['riesgo']*100:.4f},{pf['rendimiento']*100:.4f},{pf['sharpe']:.4f}\n"
            
            st.download_button(
                label="📊 Descargar CSV",
                data=resumen_csv,
                file_name=f"reporte_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col_d2:
            st.write("📥 Opciones de exportación")
        
        with col_d3:
            st.write("")
        
        st.divider()
        
        st.markdown("""
        ## 📌 Resumen Ejecutivo
        
        ### Análisis Realizado
        """)
        
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.write(f"""
            ✅ **Activos Analizados**: {len(activos)}
            - {', '.join(activos)}
            
            ✅ **Período**: {len(st.session_state.precios)} observaciones
            
            ✅ **Portafolios Óptimos**: 4 estrategias construidas
            - Mínimo Riesgo (MR)
            - Máximo Sharpe (M)
            - Rendimiento Deseado (RD)
            - Ajustado sin Short (A)
            """)
        
        with col_info2:
            st.write(f"""
            ✅ **Simulación Montecarlo**: {len(st.session_state.simulaciones):,} portafolios
            
            ✅ **Parámetros**:
            - Tasa RF: {tasa_rf_anual:.1f}%
            - Inversión: ${monto_inversion:,.0f}
            - Short Selling: {'Permitido' if permitir_short else 'No permitido'}
            """)
        
        st.divider()
        
        st.markdown("### 📊 Hallazgos Principales")
        
        # Análisis de correlaciones
        corr_array = matriz_correlacion(st.session_state.rendimientos).values.copy()
        np.fill_diagonal(corr_array, np.nan)
        corr_media = np.nanmean(corr_array)
        
        # Mejor portafolio
        mejor_pf_nombre = max(st.session_state.portafolios.items(), key=lambda x: x[1]['sharpe'])[0]
        mejor_pf = st.session_state.portafolios[mejor_pf_nombre]
        
        col_hall1, col_hall2 = st.columns(2)
        
        with col_hall1:
            st.success(f"""
            **🎯 Portafolio Recomendado: {mejor_pf_nombre}**
            - Rendimiento: {mejor_pf['rendimiento']*100:.2f}%
            - Riesgo: {mejor_pf['riesgo']*100:.2f}%
            - Ratio Sharpe: {mejor_pf['sharpe']:.4f}
            """)
        
        with col_hall2:
            st.info(f"""
            **📈 Correlaciones**
            - Media: {corr_media:.3f}
            - Los activos están {'moderadamente' if 0.3 < corr_media < 0.7 else 'altamente' if corr_media > 0.7 else 'débilmente'} correlacionados
            """)
        
        st.warning(f"""
        **⚠️ Riesgos Identificados**
        1. Correlaciones: Diversificación {'insuficiente' if corr_media > 0.7 else 'adecuada'}
        2. Data: {len(st.session_state.precios)} observaciones - Base {'sólida' if len(st.session_state.precios) > 500 else 'limitada'}
        3. Supuestos: Modelo asume rendimientos normales (verificar en Datos & Estadísticas)
        """)
        
        st.info("""
        **💡 Recomendaciones**
        1. Rebalancear portafolio mensualmente/trimestralmente
        2. Monitorear correlaciones en períodos de estrés de mercado
        3. Considerar factores externos (macroeconómicos, políticos)
        4. Ajustar asignación según cambios en objetivos de inversión
        """)

# ============================================
# PIE DE PÁGINA
# ============================================

st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
        <p>Portfolio Analyzer Pro | Powered by Streamlit & Plotly | © 2024</p>
        <p>Análisis CAPM Markowitz - Propósitos Educativos</p>
    </div>
""", unsafe_allow_html=True)
