"""
ejemplo_uso.py
Ejemplo de uso del proyecto sin Streamlit (script standalone)
"""

import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from modules import (
    descargar_datos,
    calcular_rendimientos,
    validar_datos,
    calcular_metricas_activos,
    prueba_normalidad,
    matriz_correlacion,
    OptimizadorPortafolios,
    simular_portafolios_montecarlo,
    calcular_estadisticas_simulacion
)

def main():
    """
    Script ejemplo: Análisis completo de portafolio
    """
    
    print("=" * 80)
    print("PORTFOLIO ANALYZER - EJEMPLO STANDALONE")
    print("=" * 80)
    
    # ============================================
    # 1. CONFIGURACIÓN
    # ============================================
    
    activos = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
    periodo = "2y"
    tasa_rf = 0.03  # 3% anualizado
    n_simulaciones = 10000
    
    print(f"\n✅ Activos: {', '.join(activos)}")
    print(f"✅ Período: {periodo}")
    print(f"✅ Tasa RF: {tasa_rf*100:.1f}%")
    
    # ============================================
    # 2. DESCARGA Y VALIDACIÓN
    # ============================================
    
    print("\n" + "-" * 80)
    print("DESCARGANDO DATOS...")
    print("-" * 80)
    
    try:
        precios = descargar_datos(activos, periodo=periodo, progress=False)
        print(f"✅ Datos descargados: {len(precios)} observaciones")
        print(f"   Período: {precios.index[0].date()} a {precios.index[-1].date()}")
        
        # Validar
        validar_datos(precios)
        print("✅ Datos validados correctamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # ============================================
    # 3. CALCULAR RENDIMIENTOS
    # ============================================
    
    print("\n" + "-" * 80)
    print("CALCULANDO RENDIMIENTOS...")
    print("-" * 80)
    
    rendimientos = calcular_rendimientos(precios)
    print(f"✅ Rendimientos calculados (logarítmicos)")
    print(f"   Forma: {rendimientos.shape}")
    
    # ============================================
    # 4. ESTADÍSTICAS POR ACTIVO
    # ============================================
    
    print("\n" + "-" * 80)
    print("ESTADÍSTICAS POR ACTIVO (Anualizadas)")
    print("-" * 80)
    
    stats = calcular_metricas_activos(rendimientos)
    print("\n", stats)
    
    # ============================================
    # 5. PRUEBA DE NORMALIDAD
    # ============================================
    
    print("\n" + "-" * 80)
    print("PRUEBA DE NORMALIDAD (Jarque-Bera)")
    print("-" * 80)
    
    normalidad = prueba_normalidad(rendimientos)
    print("\n", normalidad)
    print("\n💡 Nota: La mayoría de activos reales no son normales (p-value < 0.05)")
    
    # ============================================
    # 6. MATRIZ DE CORRELACIÓN
    # ============================================
    
    print("\n" + "-" * 80)
    print("MATRIZ DE CORRELACIÓN")
    print("-" * 80)
    
    corr = matriz_correlacion(rendimientos)
    print("\n", corr.round(3))
    
    # Estadísticas de correlación
    corr_array = corr.values
    np.fill_diagonal(corr_array, np.nan)
    
    print(f"\nCorrelación Media: {np.nanmean(corr_array):.3f}")
    print(f"Correlación Máxima: {np.nanmax(corr_array):.3f}")
    print(f"Correlación Mínima: {np.nanmin(corr_array):.3f}")
    
    # ============================================
    # 7. OPTIMIZACIÓN DE PORTAFOLIOS
    # ============================================
    
    print("\n" + "-" * 80)
    print("OPTIMIZACIÓN DE PORTAFOLIOS (Markowitz)")
    print("-" * 80)
    
    # Crear optimizador
    opt = OptimizadorPortafolios(rendimientos, tasa_rf=tasa_rf)
    
    # Obtener portafolios óptimos
    portafolios = opt.obtener_resumen_portafolios(permitir_short=True)
    
    # Mostrar resultados
    print("\n📊 PORTAFOLIOS ÓPTIMOS:\n")
    
    for nombre, pf in portafolios.items():
        print(f"\n{nombre}:")
        print(f"  Rendimiento: {pf['rendimiento']*100:7.2f}%")
        print(f"  Riesgo:      {pf['riesgo']*100:7.2f}%")
        print(f"  Sharpe:      {pf['sharpe']:7.4f}")
        print(f"  Pesos: {', '.join([f'{activos[i]}={pf['pesos'][i]*100:.1f}%' for i in range(len(activos))])}")
    
    # ============================================
    # 8. TABLA DE PESOS
    # ============================================
    
    print("\n" + "-" * 80)
    print("TABLA COMPARATIVA DE PESOS (%)")
    print("-" * 80)
    
    tabla_pesos = opt.tabla_pesos_portafolios(permitir_short=True)
    print("\n", tabla_pesos.round(2))
    
    # ============================================
    # 9. FRONTERA EFICIENTE
    # ============================================
    
    print("\n" + "-" * 80)
    print("FRONTERA EFICIENTE")
    print("-" * 80)
    
    frontera = opt.frontera_eficiente(n_puntos=30)
    print(f"\n✅ Generados {len(frontera)} puntos en la frontera eficiente")
    print("\nPrimeros 5 puntos:")
    print(frontera.head().round(4))
    
    # ============================================
    # 10. SIMULACIÓN MONTECARLO
    # ============================================
    
    print("\n" + "-" * 80)
    print(f"SIMULACIÓN MONTECARLO ({n_simulaciones:,} portafolios)")
    print("-" * 80)
    
    simulaciones = simular_portafolios_montecarlo(
        rendimientos,
        n_simulaciones=n_simulaciones,
        permitir_short=True,
        limites_riesgo=None,
        tasa_rf=tasa_rf
    )
    
    stats_sim = calcular_estadisticas_simulacion(simulaciones)
    
    print(f"\n✅ Portafolios simulados: {stats_sim['N_Simulaciones']:,}")
    print(f"\nEstadísticas:")
    print(f"  Riesgo Promedio:      {stats_sim['Riesgo_Promedio']*100:7.2f}%")
    print(f"  Riesgo Mínimo:        {stats_sim['Riesgo_Min']*100:7.2f}%")
    print(f"  Riesgo Máximo:        {stats_sim['Riesgo_Max']*100:7.2f}%")
    print(f"  Rendimiento Promedio: {stats_sim['Rendimiento_Promedio']*100:7.2f}%")
    print(f"  Rendimiento Mínimo:   {stats_sim['Rendimiento_Min']*100:7.2f}%")
    print(f"  Rendimiento Máximo:   {stats_sim['Rendimiento_Max']*100:7.2f}%")
    print(f"  Máximo Sharpe:        {stats_sim['Sharpe_Max']:7.4f}")
    print(f"  Sharpe Promedio:      {stats_sim['Sharpe_Promedio']:7.4f}")
    
    # ============================================
    # 11. VALUACIÓN
    # ============================================
    
    print("\n" + "-" * 80)
    print("VALUACIÓN CON INVERSIÓN DE $100,000")
    print("-" * 80)
    
    monto = 100_000
    precios_actuales = precios.iloc[-1]
    
    # Usar portafolio de máximo Sharpe
    pf_m = portafolios['M']
    
    print(f"\nPortafolio: MÁXIMO SHARPE")
    print(f"Monto Total: ${monto:,.2f}\n")
    
    for i, activo in enumerate(activos):
        peso = pf_m['pesos'][i]
        monto_activo = monto * peso
        precio = precios_actuales[activo]
        cantidad = monto_activo / precio
        
        print(f"{activo:6} | Peso: {peso*100:6.2f}% | Monto: ${monto_activo:>12,.2f} | "
              f"Precio: ${precio:>8.2f} | Qty: {cantidad:>10.4f}")
    
    print(f"\nTotal: ${monto:,.2f}")
    
    # ============================================
    # 12. RESUMEN FINAL
    # ============================================
    
    print("\n" + "=" * 80)
    print("RESUMEN FINAL")
    print("=" * 80)
    
    mejor_pf_nombre = max(portafolios.items(), key=lambda x: x[1]['sharpe'])[0]
    mejor_pf = portafolios[mejor_pf_nombre]
    
    print(f"""
✅ PORTAFOLIO RECOMENDADO: {mejor_pf_nombre}
   Rendimiento: {mejor_pf['rendimiento']*100:.2f}%
   Riesgo:      {mejor_pf['riesgo']*100:.2f}%
   Sharpe:      {mejor_pf['sharpe']:.4f}

📊 ESTRATEGIA DE ACTIVOS:
   {', '.join(activos)}

🔗 DIVERSIFICACIÓN:
   Correlación Media: {np.nanmean(corr_array):.3f}
   Status: {'✅ Bien diversificado' if np.nanmean(corr_array) < 0.5 else '⚠️ Correlaciones altas'}

🎲 SIMULACIÓN:
   {stats_sim['N_Simulaciones']:,} portafolios aleatorios
   Máximo Sharpe encontrado: {stats_sim['Sharpe_Max']:.4f}

💡 PRÓXIMOS PASOS:
   1. Validar supuestos con asesor financiero
   2. Considerar costos de transacción
   3. Rebalancear periódicamente
   4. Monitorear cambios de correlación
    """)
    
    print("=" * 80)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 80)


if __name__ == "__main__":
    main()
