# 📈 Portfolio Analyzer Pro

**Análisis Cuantitativo de Portafolios con Optimización de Markowitz**

Una aplicación profesional basada en **Streamlit** para seleccionar activos, ajustar parámetros en tiempo real y visualizar resultados de análisis financieros instantáneamente.

---

## 🎯 Características Principales

✅ **Selección Dinámica de Activos** - Ingresa tickers y carga datos en tiempo real  
✅ **Optimización de Portafolios** - 4 estrategias optimizadas (Markowitz)  
✅ **Visualizaciones Interactivas** - Gráficos profesionales con Plotly  
✅ **Análisis de Correlaciones** - Matriz de correlación y estadísticas  
✅ **Simulación Montecarlo** - 10,000+ portafolios aleatorios  
✅ **Reporte Ejecutivo** - Resumen completo con recomendaciones  
✅ **Exportación de Resultados** - Descarga CSV con análisis  
✅ **Interfaz Responsive** - Funciona en desktop y tablet  

---

## 📁 Estructura del Proyecto

```
📁 Portafolio_Analyzer/
├── 📄 app.py                    # Aplicación principal Streamlit
├── 📄 requirements.txt          # Dependencias Python
├── 📁 modules/
│   ├── __init__.py
│   ├── data_loader.py           # Descarga de datos (Yahoo Finance)
│   ├── estadisticas.py          # Cálculos estadísticos
│   ├── optimizacion.py          # Optimización Markowitz
│   ├── visualizaciones.py       # Gráficos Plotly
│   └── simulacion.py            # Montecarlo
├── 📁 config/
│   ├── parametros_default.json  # Configuración por defecto
│   └── estilos.css              # Estilos personalizados
└── 📋 README.md                 # Esta documentación
```

---

## 🚀 Instalación y Ejecución

### Prerequisitos
- **Python 3.12.10** (recomendado)
- **pip** (gestor de paquetes)

### Paso 1: Crear Entorno Virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 2: Instalar Dependencias

```bash
cd Portafolio_Analyzer
pip install -r requirements.txt
```

### Paso 3: Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en: **http://localhost:8501**

---

## 📊 Guía de Uso

### 1️⃣ Seleccionar Activos (Sidebar)

```
📌 Seleccionar Activos
├─ Ingresa tickers separados por comas
│  Ejemplo: AAPL,MSFT,GOOGL,TSLA,AMZN
└─ Clickea "✅" si tienes 5 activos
```

**Tickers Populares:**
- Tech: AAPL, MSFT, GOOGL, NVDA, AMD
- Financiero: JPM, BAC, GS, WFC
- Industrial: BA, CAT, GE
- Energía: XOM, CVX, MPC

### 2️⃣ Configurar Período de Datos

```
📅 Período de Datos
├─ Período predefinido: 1y, 2y, 5y, 10y, max
└─ Fechas personalizadas: (día inicial - día final)
```

**Recomendación:** Usar 2-5 años para análisis sólido

### 3️⃣ Parámetros de Inversión

```
💰 Parámetros
├─ Monto a invertir: $100,000 (por defecto)
├─ Tasa RF (Tasa Libre de Riesgo): 3.0% (bonos de gobierno)
└─ Capital disponible total
```

### 4️⃣ Ejecutar Análisis

```
🚀 EJECUTAR
```

La aplicación:
1. Descarga datos históricos de Yahoo Finance
2. Calcula rendimientos logarítmicos
3. Construye 4 portafolios óptimos
4. Simula 10,000 portafolios aleatorios
5. Genera visualizaciones

---

## 📖 Pestañas Principales

### 📊 Tab 1: Datos & Estadísticas

**Muestra:**
- Número de activos y observaciones
- Estadísticas por activo (Media, Volatilidad, Asimetría, Curtosis)
- Prueba de Jarque-Bera (normalidad)
- Distribución de rendimientos

**Utilidad:** Validar calidad de datos y detectar anomalías

---

### 🎯 Tab 2: Portafolios Óptimos

**Cuatro Estrategias:**

1. **🎯 Mínimo Riesgo (MR)**
   - Minimiza volatilidad global
   - Mejor para inversores conservadores
   - Sharpe: Medio

2. **📈 Máximo Sharpe (M)**
   - Mejor relación riesgo-rendimiento
   - Usa frontera eficiente
   - Sharpe: Máximo ✅

3. **🎪 Rendimiento Deseado (RD)**
   - Alcanza rendimiento objetivo
   - Mínimo riesgo para ese rendimiento
   - Sharpe: Variable

4. **✅ Ajustado sin Short (A)**
   - Sin ventas en corto
   - Todos los pesos ≥ 0
   - Restricción realista

**Tabla de Pesos:** Comparativa de asignación entre portafolios

**Valuación:** Posiciones en $ para inversión de $100,000

---

### 🔗 Tab 3: Correlaciones

**Visualizaciones:**
- Matriz de correlación (heatmap)
- Estadísticas agregadas (media, máx, mín)
- Pares más correlacionados

**Interpretación:**
- **Correlación > 0.7:** Alta (poco diversificado)
- **0.3 - 0.7:** Moderada (diversificación adecuada)
- **< 0.3:** Baja (bien diversificado) ✅

---

### 📈 Tab 4: Visualizaciones

**6 Gráficos Disponibles:**

1. **📈 Precios Históricos** - Evolución normalizada a 100
2. **📊 Rendimientos Diarios** - Scatter temporal
3. **📉 Frontera Eficiente** - Curva + portafolios óptimos
4. **🎒 Asignación de Pesos** - Gráfico de pastel
5. **📏 Retorno vs Riesgo** - Scatter por activo
6. **📊 Comparativa** - Barras de pesos

---

### 🎲 Tab 5: Simulación Montecarlo

**Genera y visualiza:**
- 10,000 portafolios aleatorios
- Distribución riesgo-rendimiento
- Frontera eficiente superpuesta
- Portafolios óptimos destacados

**Estadísticas:**
- Riesgo promedio / mín / máx
- Rendimiento promedio
- Máximo Sharpe encontrado

---

### 📋 Tab 6: Reporte Ejecutivo

**Incluye:**
- Resumen del análisis
- Portafolio recomendado
- Análisis de correlaciones
- Riesgos identificados
- Recomendaciones de inversión
- Descarga CSV

---

## 🔧 Opciones Avanzadas (⚠️ Restricciones)

```
⚠️ Restricciones y Simulación
├─ ✅ Permitir ventas en corto
│  └─ Si: Pesos pueden ser negativos
│  └─ No: Todos los pesos ≥ 0
├─ Límite de riesgo máximo (%)
│  └─ Filtra portafolios de simulación
└─ N° de simulaciones Montecarlo (1K-100K)
   └─ Más simulaciones = más precisión (más lento)
```

---

## 📐 Teoría: Optimización de Markowitz

### Frontera Eficiente

La frontera eficiente es el conjunto de portafolios que:
- **Maximizan rendimiento** para un nivel de riesgo dado, O
- **Minimizan riesgo** para un rendimiento objetivo

### Ratio de Sharpe

$$\text{Sharpe} = \frac{E[R_p] - R_f}{\sigma_p}$$

Donde:
- $E[R_p]$ = Rendimiento esperado del portafolio
- $R_f$ = Tasa libre de riesgo
- $\sigma_p$ = Volatilidad del portafolio

**Interpretación:** Mayor Sharpe = mejor relación riesgo-rendimiento

### Correlación

$$\rho_{ij} = \frac{\text{Cov}(R_i, R_j)}{\sigma_i \sigma_j}$$

- **ρ = 1:** Perfectamente correlacionados (sin diversificación)
- **ρ = 0:** Independientes (diversificación ideal)
- **ρ = -1:** Inversamente correlacionados (cobertura perfecta)

---

## 💾 Descarga de Datos

Los datos se descargan desde **Yahoo Finance** con la librería `yfinance`:

```python
import yfinance as yf

datos = yf.download(
    ['AAPL', 'MSFT'],
    start='2022-01-01',
    end='2024-12-31'
)
```

---

## ⚠️ Limitaciones y Advertencias

1. **Modelo Normal:** Asume rendimientos normales (en realidad tienen colas gruesas)
2. **Datos Históricos:** Pasado no garantiza futuro
3. **Correlaciones:** Pueden cambiar en crisis de mercado
4. **Comisiones:** No incluye costos de transacción
5. **Rebalanceo:** No modela rebalanceo periódico

---

## 🔗 Referencias y Recursos

### Librerías Utilizadas

| Librería | Propósito |
|----------|-----------|
| `streamlit` | Interfaz gráfica interactiva |
| `pandas` | Manipulación de datos |
| `numpy` | Cálculos matemáticos |
| `scipy` | Optimización y estadísticas |
| `plotly` | Gráficos interactivos |
| `yfinance` | Datos financieros |

### Lecturas Recomendadas

- **"Modern Portfolio Theory"** - Harry Markowitz (1952)
- **"The Intelligent Investor"** - Benjamin Graham
- **"A Random Walk Down Wall Street"** - Burton Malkiel

---

## 🐛 Troubleshooting

### Error: "yfinance.data.DownloadError"

**Solución:**
```bash
pip install --upgrade yfinance
```

### Error: "Module 'modules' not found"

**Solución:**
- Asegúrate que estés en la carpeta `Portafolio_Analyzer`
- Verifica que exista la carpeta `modules/`

### La app va lenta

**Soluciones:**
- Reduce número de simulaciones (5,000 en lugar de 10,000)
- Usa período más corto (1-2 años)
- Reduce el navegador web

---

## 💡 Tips y Mejores Prácticas

✅ **Usa 3-5 activos** para análisis inicial  
✅ **Período mínimo: 1 año** para datos significativos  
✅ **Verifica correlaciones** antes de invertir  
✅ **Diversifica** entre sectores (tech, financiero, industrial)  
✅ **Rebalancea** trimestralmente  
✅ **No confíes 100%** en modelos matemáticos  
✅ **Consulta asesor financiero** antes de invertir dinero real

---

## 📞 Soporte

Para reportar errores o sugerir mejoras:
1. Verifica que tengas la última versión de las librerías
2. Intenta con diferentes tickers
3. Consulta la documentación de `yfinance`

---

## 📄 Licencia

**Propósitos Educativos** - Uso libre sin garantías comerciales

---

**Última Actualización:** Abril 2024  
**Versión:** 1.0  
**Autor:** Jonathan Ivan Salmoran Acuña
