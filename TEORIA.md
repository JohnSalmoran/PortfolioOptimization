# 🎓 Portfolio Analyzer - Guía Educativa

## Teoría Financiera Implementada

### 1. Teoría Moderna de Portafolios (Markowitz, 1952)

**Concepto Clave:** Asumir riesgo adicional solo si se obtiene rendimiento adicional.

#### Frontera Eficiente

Es el conjunto de portafolios que:
- Maximizan rendimiento esperado para un nivel de riesgo dado
- Minimizan riesgo para un rendimiento objetivo

**Fórmula:**

Minimizar: $\sigma_p^2 = w^T \Sigma w$

Sujeto a: $\sum w_i = 1$ y $w^T \mu = r_p$

Donde:
- $w$ = vector de pesos
- $\Sigma$ = matriz de covarianza
- $\mu$ = vector de rendimientos esperados
- $r_p$ = rendimiento objetivo

### 2. Ratio de Sharpe

**Definición:** Rendimiento por unidad de riesgo tomado

$$S = \frac{\mu_p - r_f}{\sigma_p}$$

Donde:
- $\mu_p$ = rendimiento del portafolio
- $r_f$ = tasa libre de riesgo
- $\sigma_p$ = volatilidad del portafolio

**Interpretación:**
- Sharpe > 1.0 → Excelente
- 0.5-1.0 → Bueno
- < 0.5 → Mediocre
- < 0 → Peor que activo libre de riesgo

### 3. Capital Asset Pricing Model (CAPM)

**Rendimiento Esperado:**

$$E[R_i] = r_f + \beta_i(E[R_m] - r_f)$$

Donde:
- $r_f$ = tasa libre de riesgo
- $\beta_i$ = sensibilidad sistemática
- $E[R_m] - r_f$ = prima de mercado

### 4. Medidas de Riesgo

#### Volatilidad (Desviación Estándar)

$$\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^n (r_i - \bar{r})^2}$$

#### Downside Volatility

$$\sigma_d = \sqrt{\frac{1}{n}\sum_{r_i < r_t} (r_i - r_t)^2}$$

Solo considera pérdidas (mejor que volatilidad para inversores)

#### Value at Risk (VaR)

$$VaR_{\alpha} = F^{-1}(\alpha)$$

Ejemplo: VaR 95% = "Con 95% confianza, no perderé más del X% en 1 día"

#### Conditional VaR (CVaR)

Promedio de pérdidas más extremas que el VaR

$$CVaR_{\alpha} = E[r | r \leq VaR_{\alpha}]$$

### 5. Correlación y Diversificación

$$\rho_{ij} = \frac{\text{Cov}(r_i, r_j)}{\sigma_i \sigma_j}$$

**Matriz de Covarianza:**

$$\Sigma_{ij} = \text{Cov}(r_i, r_j)$$

**Beneficio de Diversificación:**

Cuando $\rho < 1$, se reduce riesgo sin reducir rendimiento

$$\sigma_p = \sqrt{w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2w_1 w_2 \rho_{12} \sigma_1 \sigma_2}$$

### 6. Simulación de Montecarlo

**Proceso:**
1. Generar pesos aleatorios para N portafolios
2. Calcular rendimiento y riesgo de cada uno
3. Visualizar distribución
4. Comparar con portafolios óptimos

**Ventaja:** Aproximar frontera eficiente sin resolver numéricamente

---

## Métricas Calculadas

| Métrica | Fórmula | Interpretación |
|---------|---------|-----------------|
| Media | $\mu = \frac{1}{n}\sum r_i$ | Rendimiento promedio |
| Desv. Est. | $\sigma = \sqrt{\frac{1}{n}\sum(r_i-\mu)^2}$ | Volatilidad |
| Asimetría | $\frac{E[(r-\mu)^3]}{\sigma^3}$ | Sesgo de distribución |
| Curtosis | $\frac{E[(r-\mu)^4]}{\sigma^4} - 3$ | Colas gruesas |
| Sharpe | $\frac{\mu - r_f}{\sigma}$ | Retorno/riesgo |
| Sortino | $\frac{\mu - r_f}{\sigma_d}$ | Retorno/riesgo downside |
| VaR 95% | Percentil 5% | Pérdida máxima 95% confianza |
| CVaR 95% | Media < VaR | Pérdida condicional |

---

## Supuestos del Modelo

### ✅ Asumimos:
1. Rendimientos distribuidos normalmente
2. Mercados eficientes
3. Sin costos de transacción
4. Sin impuestos
5. Correlaciones históricas = futuras
6. Datos limpios y confiables

### ❌ NO Asumimos:
- Short selling ilimitado (permitimos límites)
- Liquidez infinita (OK para activos populares)
- Información perfecta

---

## Limitaciones Prácticas

### 1. No-Normalidad

Datos reales tienen:
- **Colas Gruesas (Fat Tails):** Probabilidad > 3σ mayor que normal
- **Asimetría:** Distribuciones sesgadas
- **Varianza Condicional:** Volatilidad cambia en el tiempo

**Alternativas:** GARCH, EVT, Non-parametric methods

### 2. Estimación de Parámetros

- **Problema:** Con 100 activos necesitas estimar ~5,050 parámetros
- **Riesgo:** Overfitting con datos limitados
- **Solución:** Shrinkage estimators, Factor models

### 3. Rebalanceo

- Modelo assume "buy and hold"
- Real: Necesita rebalanceo periódico
- Costo: Comisiones que reducen rendimiento

### 4. Datos Históricos

- **Pasado ≠ Futuro**
- Correlaciones cambian en crisis
- Beta puede ser inestable

---

## Casos de Uso

### Caso 1: Inversor Conservador

```
Objetivo: Mínimo riesgo, rendimiento aceptable
Solución: Portafolio MR (Mínimo Riesgo)
```

### Caso 2: Inversor Balanceado

```
Objetivo: Balance riesgo-rendimiento
Solución: Portafolio M (Máximo Sharpe) ✅ RECOMENDADO
```

### Caso 3: Inversor Agresivo

```
Objetivo: Maximizar rendimiento
Solución: Simular portafolios M + RD con rendimiento > 10%
```

### Caso 4: Gestor de Fondos

```
Objetivo: Cumplir restricciones (sin short, límites por sector)
Solución: Portafolio A (Ajustado) + custom constraints
```

---

## Ejercicios Prácticos

### Ejercicio 1: Diversificación

**Pregunta:** ¿Cuántos activos necesito para reducir riesgo específico?

**Respuesta:** ~20-30 activos (cubiertos en el código)

**Verificar:**
1. Corro análisis con 3 activos
2. Luego con 10 activos
3. Comparo volatilidad → debería bajar

### Ejercicio 2: Correlación

**Pregunta:** ¿Qué pasa si correlación = 1 (activos idénticos)?

**Respuesta:** Sin diversificación, riesgo no se reduce

**Verificar:**
1. Ingreso activos altamente correlacionados (ej: AAPL, MSFT)
2. Verifico matriz de correlación
3. Observo que Mínimo Riesgo es prácticamente un activo

### Ejercicio 3: Tasa RF

**Pregunta:** ¿Cómo afecta tasa RF a Sharpe?

**Respuesta:** Mayor RF → menor Sharpe (más exigente)

**Verificar:**
1. Análisis con RF = 0%
2. Luego con RF = 5%
3. Observo que Sharpe disminuye

---

## Referencias Académicas

### Papers Fundacionales

1. **Markowitz, H. (1952)**
   - "Portfolio Selection"
   - *Journal of Finance*
   - Teoría de Portafolios

2. **Sharpe, W. F. (1964)**
   - "Capital Asset Prices: A Theory of Market Equilibrium"
   - CAPM

3. **Fama, E. F., & French, K. R. (1992)**
   - "The Cross-Section of Expected Stock Returns"
   - Factores de riesgo

### Libros Recomendados

- **"Modern Portfolio Theory and Investment Analysis"** - Elton et al.
- **"The Intelligent Investor"** - Graham (clásico)
- **"Quantitative Portfolio Management"** - Chincarini & Kim

### Online

- Khan Academy - Portfolio Theory
- Investopedia - Risk Metrics
- CFA Institute - Quantitative Methods

---

## Preguntas Frecuentes (FAQ)

**P: ¿Por qué Sharpe es mejor que Rendimiento?**
R: Porque ajusta por riesgo. Dos portafolios pueden tener 10% rendimiento, pero diferentes riesgos.

**P: ¿Correlación histórica = futuro?**
R: No, puede cambiar. En crisis, correlaciones suben. Usar ventanas móviles es mejor.

**P: ¿Cuántos datos históricos necesito?**
R: Mínimo 100 observaciones (5 meses). Ideal 3-5 años. Más datos no siempre es mejor (estacionariedad).

**P: ¿Es mejor Black-Litterman que Markowitz puro?**
R: Sí, incorpora creencias del inversor. Pero es más complejo.

**P: ¿Debo usar este modelo para dinero real?**
R: Úsalo como herramienta educativa y de apoyo, no como única decisión.

---

**Última Actualización:** 10 Abril 2024
