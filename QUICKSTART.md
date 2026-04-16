# 🚀 INICIO RÁPIDO - Portfolio Analyzer Pro

## ⚡ 5 Minutos para Empezar

### 1️⃣ Clonar/Descargar

```bash
# Si está en Git
git clone <tu-repo>
cd Portafolio_Analyzer

# O simplemente entra a la carpeta
cd Portafolio_Analyzer
```

### 2️⃣ Instalar (Opción A - Automático)

**Windows:**
```bash
install.bat
```

**Mac/Linux:**
```bash
chmod +x install.sh
./install.sh
```

### 2️⃣ Instalar (Opción B - Manual)

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Mac/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Verificar Installation

```bash
python test.py
```

Deberías ver:
```
✅ streamlit
✅ pandas
✅ numpy
...
✅ INSTALACIÓN VERIFICADA
```

### 4️⃣ Ejecutar Aplicación

```bash
streamlit run app.py
```

Abre tu navegador en: **http://localhost:8501**

---

## 🎯 Ejemplos Rápidos

### Opción 1: GUI Interactiva (RECOMENDADO)

```bash
streamlit run app.py
```

✅ Interfaz completa  
✅ Gráficos interactivos  
✅ Exportar resultados  

### Opción 2: Script Python

```bash
python ejemplo_uso.py
```

✅ Análisis rápido en terminal  
✅ No necesita navegador  

---

## 📋 Checklist Inicial

- [ ] Python 3.12+ instalado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] `test.py` pasa
- [ ] `streamlit run app.py` funciona

---

## 🔗 Tickers Iniciales Recomendados

**Tech (Default):**
```
AAPL,MSFT,GOOGL,TSLA,AMZN
```

**Diversificado:**
```
SPY,QQQ,IWM,TLT,GLD
```

**ETFs Internacionales:**
```
EWJ,EWG,IEUR,FXI,EWY
```

---

## 💡 Primer Análisis Sugerido

1. **Mantén** activos por defecto: AAPL,MSFT,GOOGL,TSLA,AMZN
2. **Selecciona** período: **2y** (2 años)
3. **Clickea** 🚀 EJECUTAR
4. **Explora** cada pestaña
5. **Descarga** CSV con resultados

---

## ❓ FAQ

### P: ¿Necesito dinero real para probar?
**A:** No, es simulación. Todos los números son teóricos.

### P: ¿Qué significa cada portafolio?
- **MR:** Menor riesgo pero menor rendimiento
- **M:** Balance riesgo-rendimiento (RECOMENDADO)
- **RD:** Rendimiento objetivo específico
- **A:** Sin ventas en corto (más realista)

### P: ¿De dónde vienen los datos?
**A:** Yahoo Finance (gratuito, actualizado)

### P: ¿Se conecta a internet?
**A:** Sí, solo para descargar precios históricos

### P: ¿Cada cuánto actualizar?
**A:** Mensual o trimestralmente recomendado

---

## 🆘 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### Error: "No data found, symbol [TICKER] is invalid"
- Verifica que el ticker sea válido en Yahoo Finance
- Prueba con AAPL, MSFT, GOOGL

### La app va lenta
- Reduce simulaciones a 5,000
- Usa período de 1-2 años

### Port 8501 ya en uso
```bash
streamlit run app.py --server.port 8502
```

---

## 📚 Documentación Completa

Ver [README.md](README.md) para:
- Teoría de Markowitz
- Explicación de cada métrica
- Referencias académicas
- Limitaciones del modelo

---

## 🎓 Aprende Mientras Usas

1. **Pestaña 1:** Entiende la volatilidad y correlación
2. **Pestaña 2:** Ve cómo se optimizan portafolios
3. **Pestaña 3:** Aprende sobre diversificación
4. **Pestaña 4:** Visualiza frontera eficiente
5. **Pestaña 5:** Comprende simulación Montecarlo

---

**¿Listo?** 🚀 Ejecuta `streamlit run app.py`
