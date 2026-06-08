import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
 
st.set_page_config(page_title="StockAnalyzer Pro", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main-header { background: linear-gradient(135deg, #1A1D2E 0%, #16213E 100%); border: 1px solid #2D3561; border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; }
.metric-card { background: #1A1D2E; border: 1px solid #2D3561; border-radius: 12px; padding: 1rem 1.25rem; text-align: center; }
.metric-card .label { font-size: 11px; color: #8892B0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.metric-card .value { font-size: 20px; font-weight: 600; color: #E6F1FF; }
.metric-card .sub { font-size: 11px; color: #8892B0; margin-top: 4px; }
.score-card { background: #1A1D2E; border: 1px solid #2D3561; border-radius: 16px; padding: 2rem; text-align: center; }
</style>
""", unsafe_allow_html=True)
 
try:
    AV_KEY = st.secrets["AV_API_KEY"]
except Exception:
    AV_KEY = "demo"
 
AV_BASE = "https://www.alphavantage.co/query"
 
def av_get(params):
    params["apikey"] = AV_KEY
    try:
        r = requests.get(AV_BASE, params=params, timeout=15)
        data = r.json()
        if "Error Message" in str(data) or "Information" in str(data):
            return {}
        return data
    except Exception:
        return {}
 
@st.cache_data(ttl=900)
def get_quote(ticker):
    return av_get({"function": "GLOBAL_QUOTE", "symbol": ticker})
 
@st.cache_data(ttl=3600)
def get_overview(ticker):
    return av_get({"function": "OVERVIEW", "symbol": ticker})
 
@st.cache_data(ttl=3600)
def get_history(ticker):
    return av_get({"function": "TIME_SERIES_WEEKLY", "symbol": ticker})
 
@st.cache_data(ttl=3600)
def get_cashflow(ticker):
    return av_get({"function": "CASH_FLOW", "symbol": ticker})
 
@st.cache_data(ttl=3600)
def search_ticker(query):
    return av_get({"function": "SYMBOL_SEARCH", "keywords": query})
 
if "ticker_seleccionado" not in st.session_state:
    st.session_state.ticker_seleccionado = "AAPL"
 
st.markdown("""
<div style='display:flex;align-items:center;gap:12px;margin-bottom:0.25rem'>
    <span style='font-size:28px;font-weight:700;color:#E6F1FF;letter-spacing:-0.5px'>Stock</span>
    <span style='font-size:28px;font-weight:300;color:#6C63FF'>Analyzer</span>
    <span style='background:#6C63FF;color:white;font-size:10px;padding:3px 8px;border-radius:20px;font-weight:600;letter-spacing:1px'>PRO</span>
</div>
<p style='color:#8892B0;font-size:13px;margin-bottom:1.5rem'>Analisis fundamental + tecnico · Alertas inteligentes · Cobertura global</p>
""", unsafe_allow_html=True)
 
col_search, col_ticker, col_btn = st.columns([2.5, 1.5, 0.8])
with col_search:
    busqueda = st.text_input("", placeholder="Buscar empresa: Apple, Inditex, LVMH...", label_visibility="collapsed")
with col_ticker:
    ticker_input = st.text_input("", value=st.session_state.ticker_seleccionado,
                                  placeholder="AAPL · ITX.MC · VSURE.ST", label_visibility="collapsed").upper()
    st.session_state.ticker_seleccionado = ticker_input
with col_btn:
    analizar = st.button("Analizar", type="primary", use_container_width=True)
 
if busqueda:
    with st.spinner("Buscando..."):
        data = search_ticker(busqueda)
        matches = data.get("bestMatches", [])
        if matches:
            st.markdown("**Resultados:**")
            cols = st.columns(4)
            idx = 0
            for m in matches[:8]:
                sym = m.get("1. symbol", "")
                nombre_q = m.get("2. name", "")
                region = m.get("4. region", "")
                tipo = m.get("3. type", "")
                if tipo != "Equity":
                    continue
                with cols[idx % 4]:
                    st.markdown(
                        "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:10px;padding:0.6rem 0.8rem;margin-bottom:8px'>"
                        "<div style='font-size:14px;font-weight:600;color:#6C63FF'>" + sym + "</div>"
                        "<div style='font-size:11px;color:#CCD6F6;margin-top:2px'>" + nombre_q[:28] + "</div>"
                        "<div style='font-size:10px;color:#8892B0;margin-top:2px'>" + region + "</div>"
                        "</div>", unsafe_allow_html=True)
                    if st.button("Usar", key="btn_" + sym, use_container_width=True):
                        st.session_state.ticker_seleccionado = sym
                        st.rerun()
                idx += 1
        else:
            st.warning("Sin resultados. Prueba el ticker directamente.")
 
with st.expander("Guia de sufijos por mercado"):
    st.markdown("""
| Mercado | Sufijo | Ejemplo |
|---------|--------|---------|
| Espana (BME) | `.MC` | `ITX.MC` Inditex |
| Alemania | `.DE` | `BMW.DE` |
| Francia | `.PA` | `MC.PA` LVMH |
| Reino Unido | `.L` | `HSBA.L` |
| Italia | `.MI` | `ENI.MI` |
| Suecia | `.ST` | `VSURE.ST` Verisure |
| Suiza | `.SW` | `NESN.SW` Nestle |
| Japon | `.T` | `7203.T` Toyota |
| Hong Kong | `.HK` | `0700.HK` Tencent |
    """)
 
with st.expander("Como funciona este analizador"):
    st.markdown("""
Este analizador compara **dos tipos de valor** de una accion:
 
- **Valor fundamental**: lo que la empresa *realmente vale* segun sus numeros reales (beneficios, deuda, crecimiento).
- **Valor de mercado**: lo que la gente *esta dispuesta a pagar* ahora mismo en bolsa.
 
**La oportunidad esta en la diferencia:**
- Precio muy por debajo del fundamental → accion barata → senal de compra
- Precio muy por encima del fundamental → accion cara → senal de venta
- Cerca → situacion neutra, esperar
 
El sistema puntua la accion de 0 a 100 y genera alertas automaticas explicando exactamente que hacer y por que.
    """)
 
if not analizar:
    st.markdown("""
    <div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:16px;padding:3rem;text-align:center;margin-top:2rem'>
        <div style='font-size:48px;margin-bottom:1rem'>📊</div>
        <div style='font-size:18px;font-weight:600;color:#E6F1FF;margin-bottom:0.5rem'>Introduce un ticker y pulsa Analizar</div>
        <div style='font-size:13px;color:#8892B0;margin-bottom:1.5rem'>Datos en tiempo real via Alpha Vantage · Cobertura global</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
 
with st.spinner("Cargando datos de mercado..."):
    quote_data    = get_quote(ticker_input)
    overview_data = get_overview(ticker_input)
    history_data  = get_history(ticker_input)
    cashflow_data = get_cashflow(ticker_input)
 
q  = quote_data.get("Global Quote", {})
ov = overview_data
 
if not q or not q.get("05. price"):
    st.error("No se encontraron datos para **" + ticker_input + "**. Verifica el ticker.")
    st.stop()
 
def sf(val, default=None):
    try:
        v = float(val)
        return v if v != 0 else default
    except Exception:
        return default
 
precio       = sf(q.get("05. price"), 0)
cambio_pct   = sf(q.get("09. % change", "0").replace("%", ""), 0)
nombre       = ov.get("Name", ticker_input)
sector       = ov.get("Sector", "")
pais         = ov.get("Country", "")
moneda       = ov.get("Currency", "USD")
per          = sf(ov.get("PERatio"))
per_fwd      = sf(ov.get("ForwardPE"))
pb           = sf(ov.get("PriceToBookRatio"))
ps           = sf(ov.get("PriceToSalesRatioTTM"))
roe          = sf(ov.get("ReturnOnEquityTTM"))
roa          = sf(ov.get("ReturnOnAssetsTTM"))
margen       = sf(ov.get("ProfitMargin"))
margen_bruto = sf(ov.get("GrossProfitTTM"))
deuda_cap    = sf(ov.get("DebtToEquityRatio"))
beta         = sf(ov.get("Beta"))
cap          = sf(ov.get("MarketCapitalization"))
w52h         = sf(ov.get("52WeekHigh"))
w52l         = sf(ov.get("52WeekLow"))
eps          = sf(ov.get("EPS"))
target       = sf(ov.get("AnalystTargetPrice"))
media50      = sf(ov.get("50DayMovingAverage"))
media200     = sf(ov.get("200DayMovingAverage"))
crec_ing     = sf(ov.get("QuarterlyRevenueGrowthYOY"))
crec_ben     = sf(ov.get("QuarterlyEarningsGrowthYOY"))
vol          = sf(q.get("06. volume"))
prev_vol     = sf(ov.get("SharesFloat"))
 
weekly = history_data.get("Weekly Time Series", {})
hist_dates  = sorted(weekly.keys())[-52:]
hist_prices = [sf(weekly[d]["4. close"], 0) for d in hist_dates]
 
cf_annual = cashflow_data.get("annualReports", [])
fcf_hist = []
for rep in cf_annual[:5]:
    try:
        op   = sf(rep.get("operatingCashflow"), 0)
        capex = sf(rep.get("capitalExpenditures"), 0)
        fcf  = op - abs(capex)
        yr   = rep.get("fiscalDateEnding", "")[:4]
        fcf_hist.append({"year": yr, "fcf": fcf, "op": op})
    except Exception:
        pass
 
if eps and eps > 0 and per_fwd and per:
    g = max(0.03, min(0.25, (per - per_fwd) / per * 0.5 + 0.05))
else:
    g = 0.07
intrinseco = eps * (8.5 + 2 * g * 100) if eps and eps > 0 else None
diff_pct   = ((precio - intrinseco) / intrinseco * 100) if intrinseco else None
 
def sc_valoracion(per, pb):
    pts = 10
    if per:
        if per < 12: pts += 10
        elif per < 20: pts += 6
        elif per < 30: pts += 3
        else: pts -= 5
    if pb:
        if pb < 1.5: pts += 5
        elif pb < 3: pts += 2
        elif pb > 6: pts -= 3
    return max(0, min(20, pts))
 
def sc_calidad(roe, margen):
    pts = 10
    if roe:
        if roe > 0.20: pts += 7
        elif roe > 0.12: pts += 4
        elif roe < 0.05: pts -= 4
    if margen:
        if margen > 0.20: pts += 5
        elif margen > 0.10: pts += 2
        elif margen < 0: pts -= 5
    return max(0, min(20, pts))
 
def sc_financiera(deuda_cap):
    pts = 10
    if deuda_cap:
        if deuda_cap < 0.5: pts += 10
        elif deuda_cap < 1.5: pts += 5
        elif deuda_cap < 3: pts += 1
        else: pts -= 5
    return max(0, min(20, pts))
 
def sc_momentum(precio, w52h, w52l, target, media50, media200):
    pts = 10
    if w52h and w52l and w52h > w52l:
        pos = (precio - w52l) / (w52h - w52l)
        if pos < 0.35: pts += 8
        elif pos < 0.55: pts += 4
        elif pos > 0.85: pts -= 4
    if target:
        if precio < target * 0.9: pts += 4
        elif precio > target * 1.1: pts -= 4
    if media50 and media200:
        if media50 > media200: pts += 2
        else: pts -= 2
    return max(0, min(20, pts))
 
def sc_dcf(precio, intrinseco):
    pts = 10
    if intrinseco and intrinseco > 0:
        gap = (intrinseco - precio) / intrinseco
        if gap > 0.30: pts += 10
        elif gap > 0.15: pts += 6
        elif gap > 0: pts += 3
        elif gap > -0.15: pts -= 2
        else: pts -= 7
    return max(0, min(20, pts))
 
s1 = sc_valoracion(per, pb)
s2 = sc_calidad(roe, margen)
s3 = sc_financiera(deuda_cap)
s4 = sc_momentum(precio, w52h, w52l, target, media50, media200)
s5 = sc_dcf(precio, intrinseco)
total = s1 + s2 + s3 + s4 + s5
 
if total >= 65:
    rec = "COMPRAR"; color_final = "#4ADE80"; bg_final = "rgba(74,222,128,0.1)"; border_final = "#4ADE80"
elif total >= 40:
    rec = "MANTENER"; color_final = "#FBBF24"; bg_final = "rgba(251,191,36,0.1)"; border_final = "#FBBF24"
else:
    rec = "VENDER"; color_final = "#F87171"; bg_final = "rgba(248,113,113,0.1)"; border_final = "#F87171"
 
alertas = []
if intrinseco and diff_pct is not None:
    if diff_pct < -30:
        alertas.append({"tipo": "OPORTUNIDAD FUERTE", "color": "#4ADE80", "bg": "rgba(74,222,128,0.08)", "icono": "🟢",
            "titulo": "Precio " + str(round(abs(diff_pct))) + "% por debajo del valor fundamental",
            "que_hacer": "Considera comprar. El precio ofrece un margen de seguridad significativo respecto al valor real del negocio.",
            "por_que": "Valor intrinseco: " + moneda + " " + str(round(intrinseco, 2)) + " — Precio actual: " + moneda + " " + str(round(precio, 2)) + ". El mercado infravalora la empresa."})
    elif diff_pct < -15:
        alertas.append({"tipo": "POSIBLE OPORTUNIDAD", "color": "#34D399", "bg": "rgba(52,211,153,0.08)", "icono": "🟡",
            "titulo": "Precio " + str(round(abs(diff_pct))) + "% por debajo del valor fundamental",
            "que_hacer": "Hay margen de seguridad. Considera una posicion parcial y espera confirmacion de tendencia.",
            "por_que": "Intrinseco (" + moneda + " " + str(round(intrinseco, 2)) + ") supera al precio (" + moneda + " " + str(round(precio, 2)) + "). Descuento real pero moderado."})
    elif diff_pct > 30:
        alertas.append({"tipo": "PRECIO MUY ELEVADO", "color": "#F87171", "bg": "rgba(248,113,113,0.08)", "icono": "🔴",
            "titulo": "Precio " + str(round(diff_pct)) + "% por encima del valor fundamental",
            "que_hacer": "Si tienes la accion considera reducir posicion. Si no la tienes, evita entrar ahora.",
            "por_que": "Precio (" + moneda + " " + str(round(precio, 2)) + ") muy por encima del intrinseco (" + moneda + " " + str(round(intrinseco, 2)) + "). Diferencia es euforia o narrativa."})
    elif diff_pct > 15:
        alertas.append({"tipo": "PRECIO ELEVADO", "color": "#FBBF24", "bg": "rgba(251,191,36,0.08)", "icono": "🟠",
            "titulo": "Precio " + str(round(diff_pct)) + "% por encima del valor fundamental",
            "que_hacer": "No es el mejor momento de entrada. Vigila con stop-loss si ya tienes posicion.",
            "por_que": "Prima del " + str(round(diff_pct)) + "% sobre el intrinseco (" + moneda + " " + str(round(intrinseco, 2)) + ")."})
 
if crec_ben and crec_ben > 0.10 and cambio_pct < -2:
    alertas.append({"tipo": "SENAL CLASICA DE VALOR", "color": "#4ADE80", "bg": "rgba(74,222,128,0.08)", "icono": "🟢",
        "titulo": "Beneficios creciendo pero precio cayendo hoy",
        "que_hacer": "Situacion que buscan los inversores de valor. El mercado reacciona con miedo mientras el negocio mejora.",
        "por_que": "Crecimiento de beneficios: +" + str(round(crec_ben*100, 1)) + "% · Caida de precio hoy: " + str(round(cambio_pct, 1)) + "%. Posible sobrerreaccion del mercado."})
 
if w52h and precio > w52h * 0.95:
    alertas.append({"tipo": "PRECIO EN MAXIMOS ANUALES", "color": "#F87171", "bg": "rgba(248,113,113,0.08)", "icono": "🔴",
        "titulo": "Precio cerca del maximo de 52 semanas",
        "que_hacer": "Prudencia. No es buen momento de entrada salvo que el fundamental lo justifique claramente.",
        "por_que": "A " + moneda + " " + str(round(precio, 2)) + " solo queda un " + str(round((w52h-precio)/w52h*100, 1)) + "% para el maximo anual (" + moneda + " " + str(round(w52h, 2)) + ")."})
 
if w52l and precio < w52l * 1.10 and s2 >= 14:
    alertas.append({"tipo": "MINIMOS CON NEGOCIO SOLIDO", "color": "#4ADE80", "bg": "rgba(74,222,128,0.08)", "icono": "🟢",
        "titulo": "Precio en minimos anuales pero el negocio es de calidad",
        "que_hacer": "Interesante para acumular gradualmente. El mercado castiga el precio pero los fundamentos son buenos.",
        "por_que": "Precio cerca del minimo (" + moneda + " " + str(round(w52l, 2)) + ") con calidad de negocio de " + str(s2) + "/20."})
 
if deuda_cap and deuda_cap > 3:
    alertas.append({"tipo": "RIESGO FINANCIERO ELEVADO", "color": "#F87171", "bg": "rgba(248,113,113,0.08)", "icono": "🔴",
        "titulo": "Nivel de deuda muy por encima de la media",
        "que_hacer": "Incorpora este riesgo en tu decision. La deuda alta es un multiplicador de riesgos en entornos de tipos altos.",
        "por_que": "Deuda/Capital: " + str(round(deuda_cap, 2)) + "x. Por encima de 2x empieza a ser preocupante."})
 
if media50 and media200:
    if media50 > media200 * 1.02:
        alertas.append({"tipo": "GOLDEN CROSS — TENDENCIA ALCISTA", "color": "#34D399", "bg": "rgba(52,211,153,0.08)", "icono": "🟡",
            "titulo": "Media 50d supera a media 200d",
            "que_hacer": "Senal tecnica positiva. El momentum de medio plazo es favorable.",
            "por_que": "MA50 (" + str(round(media50, 2)) + ") > MA200 (" + str(round(media200, 2)) + "). Inicio de tendencia alcista consolidada."})
    elif media50 < media200 * 0.98:
        alertas.append({"tipo": "DEATH CROSS — TENDENCIA BAJISTA", "color": "#FBBF24", "bg": "rgba(251,191,36,0.08)", "icono": "🟠",
            "titulo": "Media 50d por debajo de media 200d",
            "que_hacer": "Senal tecnica negativa. Espera confirmacion de giro antes de entrar.",
            "por_que": "MA50 (" + str(round(media50, 2)) + ") < MA200 (" + str(round(media200, 2)) + "). Tendencia bajista de fondo."})
 
color_cambio = "#4ADE80" if cambio_pct >= 0 else "#F87171"
signo = "+" if cambio_pct >= 0 else ""
cambio_arrow = "▲" if cambio_pct >= 0 else "▼"
 
st.markdown(
    "<div class='main-header'>"
    "<div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem'>"
    "<div><div style='font-size:24px;font-weight:700;color:#E6F1FF;margin-bottom:4px'>" + nombre + "</div>"
    "<div style='display:flex;gap:8px;align-items:center;flex-wrap:wrap'>"
    "<span style='background:#16213E;border:1px solid #2D3561;border-radius:20px;padding:3px 12px;font-size:12px;color:#8892B0'>" + ticker_input + "</span>"
    + ("<span style='background:#16213E;border:1px solid #2D3561;border-radius:20px;padding:3px 12px;font-size:12px;color:#8892B0'>" + sector + "</span>" if sector else "")
    + ("<span style='background:#16213E;border:1px solid #2D3561;border-radius:20px;padding:3px 12px;font-size:12px;color:#8892B0'>" + pais + "</span>" if pais else "")
    + "</div></div>"
    "<div style='text-align:right'>"
    "<div style='font-size:36px;font-weight:700;color:#E6F1FF'>" + moneda + " " + str(round(precio, 2)) + "</div>"
    "<div style='font-size:16px;font-weight:500;color:" + color_cambio + "'>" + cambio_arrow + " " + signo + str(round(cambio_pct, 2)) + "% hoy</div>"
    "</div></div></div>", unsafe_allow_html=True)
 
if alertas:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#8892B0;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.75rem'>⚡ " + str(len(alertas)) + " Alerta" + ("s" if len(alertas) > 1 else "") + " detectada" + ("s" if len(alertas) > 1 else "") + "</div>", unsafe_allow_html=True)
    for a in alertas:
        st.markdown(
            "<div style='background:" + a["bg"] + ";border-left:3px solid " + a["color"] + ";border-radius:0 12px 12px 0;padding:1rem 1.5rem;margin-bottom:0.5rem'>"
            "<div style='font-size:10px;font-weight:700;color:" + a["color"] + ";letter-spacing:1.5px;margin-bottom:6px'>" + a["icono"] + "  " + a["tipo"] + "</div>"
            "<div style='font-size:15px;font-weight:600;color:#E6F1FF;margin-bottom:8px'>" + a["titulo"] + "</div>"
            "<div style='font-size:13px;color:#CCD6F6;margin-bottom:4px'><span style='color:" + a["color"] + ";font-weight:600'>QUE HACER:</span>  " + a["que_hacer"] + "</div>"
            "<div style='font-size:12px;color:#8892B0'><span style='font-weight:600'>POR QUE:</span>  " + a["por_que"] + "</div>"
            "</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.3);border-radius:12px;padding:1rem 1.5rem;color:#8892B0;font-size:13px'>Sin alertas destacadas. La accion se encuentra en zona de valoracion neutra.</div>", unsafe_allow_html=True)
 
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["📊  Resumen", "🔬  Valor fundamental", "📈  Valor de mercado", "🎯  Puntuacion"])
 
with tab1:
    metrics = [
        ("Precio actual", moneda + " " + str(round(precio, 2)), ""),
        ("Valor intrinseco est.", moneda + " " + str(round(intrinseco, 2)) if intrinseco else "N/D", "Formula Graham adaptada"),
        ("Diferencia", (("+" if diff_pct >= 0 else "") + str(round(diff_pct, 1)) + "%") if diff_pct is not None else "N/D", "Precio vs fundamental"),
        ("PER", str(round(per, 1)) + "x" if per else "N/D", "< 15 barato  > 30 caro"),
        ("Cap. bursatil", moneda + " " + str(round(cap/1e9, 1)) + "B" if cap else "N/D", ""),
        ("Obj. analistas", moneda + " " + str(round(target, 2)) if target else "N/D",
         (("+" if target >= precio else "") + str(round((target-precio)/precio*100, 1)) + "% potencial") if target else ""),
    ]
    cols = st.columns(6)
    for i, (label, value, sub) in enumerate(metrics):
        with cols[i]:
            st.markdown(
                "<div class='metric-card'><div class='label'>" + label + "</div>"
                "<div class='value'>" + value + "</div>"
                + ("<div class='sub'>" + sub + "</div>" if sub else "")
                + "</div>", unsafe_allow_html=True)
 
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div style='font-size:14px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Evolucion del precio — 52 semanas</div>", unsafe_allow_html=True)
        if hist_prices:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hist_dates, y=hist_prices,
                line=dict(color="#6C63FF", width=2), fill="tozeroy",
                fillcolor="rgba(108,99,255,0.06)", name="Precio",
                hovertemplate=moneda + " %{y:.2f}<extra></extra>"))
            if intrinseco:
                fig.add_hline(y=intrinseco, line_dash="dash", line_color="#4ADE80", line_width=1,
                              annotation_text="Intrinseco " + str(round(intrinseco, 0)),
                              annotation_font_color="#4ADE80", annotation_font_size=11)
            if target:
                fig.add_hline(y=target, line_dash="dot", line_color="#FBBF24", line_width=1,
                              annotation_text="Objetivo " + str(round(target, 0)),
                              annotation_font_color="#FBBF24", annotation_font_size=11)
            if media200:
                fig.add_hline(y=media200, line_dash="dot", line_color="#8892B0", line_width=1,
                              annotation_text="MA200 " + str(round(media200, 0)),
                              annotation_font_color="#8892B0", annotation_font_size=11)
            fig.update_layout(height=360, margin=dict(l=0, r=80, t=10, b=0),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              xaxis=dict(showgrid=False, color="#8892B0"),
                              yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#8892B0", title=moneda),
                              hovermode="x unified", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with st.expander("Como leer este grafico"):
            st.markdown("""
- **Linea morada**: precio real de la accion en bolsa cada semana
- **Linea verde discontinua**: valor intrinseco estimado (lo que deberia valer segun sus numeros)
- **Linea amarilla punteada**: precio objetivo medio de los analistas profesionales
- **Linea gris punteada**: media movil de 200 dias (tendencia de largo plazo)
 
**La clave esta en la relacion entre la linea morada y la verde:**
- Precio muy por DEBAJO de la verde → el mercado infravalora la empresa → posible oportunidad
- Precio muy por ENCIMA de la verde → el mercado sobrevalora la empresa → precaucion
 
Si el precio cruza la MA200 al alza con volumen → senal alcista de largo plazo.
            """)
 
    with col2:
        st.markdown("<div style='font-size:14px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Posicion en rango anual</div>", unsafe_allow_html=True)
        if w52h and w52l and w52h != w52l:
            pos_pct = max(0, min(100, round((precio - w52l) / (w52h - w52l) * 100)))
            color_pos = "#4ADE80" if pos_pct < 40 else "#F87171" if pos_pct > 80 else "#FBBF24"
            st.markdown(
                "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:12px;padding:1.25rem'>"
                "<div style='font-size:11px;color:#8892B0;margin-bottom:8px'>POSICION EN RANGO 52 SEMANAS</div>"
                "<div style='font-size:32px;font-weight:700;color:" + color_pos + ";text-align:center'>" + str(pos_pct) + "%</div>"
                "<div style='background:#0F1117;border-radius:4px;height:8px;margin:8px 0'>"
                "<div style='background:" + color_pos + ";width:" + str(pos_pct) + "%;height:8px;border-radius:4px'></div>"
                "</div>"
                "<div style='display:flex;justify-content:space-between;font-size:10px;color:#8892B0'>"
                "<span>Min " + str(round(w52l, 1)) + "</span><span>Max " + str(round(w52h, 1)) + "</span>"
                "</div>"
                "<div style='font-size:11px;color:#475569;margin-top:8px;text-align:center'>"
                + ("Cerca de minimos — margen de subida" if pos_pct < 30 else "Cerca de maximos — poco margen" if pos_pct > 80 else "Zona media del rango") +
                "</div></div>", unsafe_allow_html=True)
 
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:14px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Comparativa de precios clave</div>", unsafe_allow_html=True)
    labels_bar = ["Min 52s", "Precio actual", "Intrinseco", "Obj. analistas", "Max 52s"]
    values_bar = [w52l, precio, intrinseco, target, w52h]
    colors_bar = ["#475569", "#6C63FF", "#4ADE80", "#FBBF24", "#F87171"]
    fig2 = go.Figure(go.Bar(x=labels_bar, y=values_bar, marker_color=colors_bar,
        text=[str(round(v, 1)) if v else "N/D" for v in values_bar],
        textposition="outside", textfont=dict(color="#CCD6F6", size=12)))
    fig2.update_layout(height=260, margin=dict(l=0, r=0, t=20, b=0),
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       xaxis=dict(showgrid=False, color="#8892B0"),
                       yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#8892B0", title=moneda),
                       showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
 
with tab2:
    st.markdown("<div style='background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.2);border-radius:10px;padding:0.75rem 1rem;font-size:13px;color:#8892B0;margin-bottom:1rem'>El valor fundamental mide la salud REAL del negocio. Estos numeros cambian trimestralmente, no cada dia.</div>", unsafe_allow_html=True)
 
    with st.expander("Que es el valor fundamental y por que importa"):
        st.markdown("""
Mientras el precio de mercado sube y baja cada segundo segun el humor de los inversores,
el valor fundamental cambia lentamente y refleja la realidad del negocio.
 
**La idea clave de Benjamin Graham** (mentor de Warren Buffett):
> "A corto plazo el mercado es una maquina de votar. A largo plazo es una maquina de pesar."
 
Es decir: a corto plazo gana la popularidad y el miedo. A largo plazo lo que pesa de verdad son los numeros reales.
 
**Cuando el precio esta muy por debajo del fundamental** → el mercado esta siendo irracional y hay una oportunidad de compra con margen de seguridad.
 
**Cuando el precio esta muy por encima** → el mercado descuenta demasiado optimismo y el riesgo de correccion es alto.
        """)
 
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Valoracion</div>", unsafe_allow_html=True)
        with st.expander("Que mide la valoracion"):
            st.markdown("""
- **PER (Precio/Beneficio)**: cuantos anos de beneficios pagas por la accion. Menos de 15x suele ser barato. Mas de 30x suele ser caro. Un PER alto puede estar justificado si la empresa crece muy rapido.
- **P/Book (Precio/Valor contable)**: cuanto pagas vs lo que valen los activos netos. Si P/Book es menor que 1, pagas menos que el valor real de los activos.
- **P/Ventas**: cuantas veces pagas los ingresos anuales. Util para empresas sin beneficios todavia.
- **Regla general**: estos ratios solo tienen sentido comparados con el sector.
            """)
        df_val = pd.DataFrame({
            "Metrica": ["PER trailing", "PER forward", "P / Book", "P / Ventas"],
            "Valor": [
                str(round(per, 2)) + "x" if per else "N/D",
                str(round(per_fwd, 2)) + "x" if per_fwd else "N/D",
                str(round(pb, 2)) + "x" if pb else "N/D",
                str(round(ps, 2)) + "x" if ps else "N/D",
            ],
            "Referencia": ["< 15 barato · > 30 caro", "< 15 barato · > 30 caro", "< 1.5 barato · > 6 caro", "Depende del sector"],
            "Senal": [
                "Barato" if per and per < 15 else ("Caro" if per and per > 30 else "Normal") if per else "—",
                "Barato" if per_fwd and per_fwd < 15 else ("Caro" if per_fwd and per_fwd > 30 else "Normal") if per_fwd else "—",
                "Barato" if pb and pb < 1.5 else ("Caro" if pb and pb > 6 else "Normal") if pb else "—",
                "—"
            ]
        })
        st.dataframe(df_val, hide_index=True, use_container_width=True)
 
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin:1rem 0 0.5rem'>Rentabilidad</div>", unsafe_allow_html=True)
        with st.expander("Que mide la rentabilidad"):
            st.markdown("""
- **ROE**: beneficio que genera por cada euro de capital propio. Por encima del 15% indica negocio eficiente.
- **ROA**: beneficio sobre el total de activos. Por encima del 10% es bueno.
- **Margen neto**: de cada 100 euros ingresados, cuanto queda como beneficio final. Un margen del 20% significa que de 100 euros vendidos, 20 son beneficio neto.
- **Margen bruto**: rentabilidad antes de gastos generales. Un margen bruto alto (>40%) suele indicar ventaja competitiva.
            """)
        df_rent = pd.DataFrame({
            "Metrica": ["ROE", "ROA", "Margen neto"],
            "Valor": [
                str(round(roe*100, 1)) + "%" if roe else "N/D",
                str(round(roa*100, 1)) + "%" if roa else "N/D",
                str(round(margen*100, 1)) + "%" if margen else "N/D",
            ],
            "Referencia": ["> 15% bueno", "> 10% bueno", "> 15% bueno"],
            "Senal": [
                "Bueno" if roe and roe > 0.15 else ("Bajo" if roe and roe < 0.05 else "Normal") if roe else "—",
                "Bueno" if roa and roa > 0.10 else ("Bajo" if roa and roa < 0.03 else "Normal") if roa else "—",
                "Bueno" if margen and margen > 0.15 else ("Bajo" if margen and margen < 0.05 else "Normal") if margen else "—",
            ]
        })
        st.dataframe(df_rent, hide_index=True, use_container_width=True)
 
    with col2:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Salud financiera</div>", unsafe_allow_html=True)
        with st.expander("Que es la salud financiera"):
            st.markdown("""
- **Deuda/Capital**: cuanta deuda tiene en relacion a su capital propio. Por debajo de 0.5x es comoda. Por encima de 3x es preocupante. Una empresa muy endeudada es fragil: si sube los tipos de interes o flojea el negocio puede tener serios problemas.
- **Beta**: mide la volatilidad respecto al mercado. Beta 1.5 significa que si el mercado cae 10%, esta accion tiende a caer 15%.
- **Medias moviles**: la MA50 mide tendencia a corto plazo, la MA200 a largo plazo. Si la MA50 supera a la MA200 es una senal alcista (Golden Cross).
            """)
        df_fin = pd.DataFrame({
            "Metrica": ["Deuda/Capital", "Beta", "Max 52s", "Min 52s", "MA 50d", "MA 200d"],
            "Valor": [
                str(round(deuda_cap, 2)) + "x" if deuda_cap else "N/D",
                str(round(beta, 2)) if beta else "N/D",
                moneda + " " + str(round(w52h, 2)) if w52h else "N/D",
                moneda + " " + str(round(w52l, 2)) if w52l else "N/D",
                moneda + " " + str(round(media50, 2)) if media50 else "N/D",
                moneda + " " + str(round(media200, 2)) if media200 else "N/D",
            ],
            "Senal": [
                "Baja" if deuda_cap and deuda_cap < 0.5 else ("Alta" if deuda_cap and deuda_cap > 3 else "Media") if deuda_cap else "—",
                "Menos volatil" if beta and beta < 1 else ("Mas volatil" if beta else "—"),
                "—", "—",
                "Por encima" if media50 and precio > media50 else "Por debajo" if media50 else "—",
                "Por encima" if media200 and precio > media200 else "Por debajo" if media200 else "—"
            ]
        })
        st.dataframe(df_fin, hide_index=True, use_container_width=True)
 
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin:1rem 0 0.5rem'>Valor intrinseco estimado</div>", unsafe_allow_html=True)
        with st.expander("Como se calcula el valor intrinseco"):
            st.markdown("""
El valor intrinseco es lo que deberia valer la empresa segun sus numeros reales, sin tener en cuenta el humor del mercado.
 
**Formula de Benjamin Graham adaptada:**
`Valor = BPA x (8.5 + 2 x Crecimiento estimado)`
 
Donde BPA es el beneficio por accion y el crecimiento se estima a partir de la diferencia entre PER actual y forward.
 
**Si el precio esta por debajo del intrinseco** → hay margen de seguridad → posible oportunidad.
**Si esta por encima** → el mercado descuenta crecimiento optimista que puede o no materializarse.
            """)
        if intrinseco:
            diff_color = "#4ADE80" if diff_pct and diff_pct < 0 else "#F87171"
            st.markdown(
                "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:12px;padding:1.25rem'>"
                "<div style='display:grid;grid-template-columns:1fr 1fr;gap:1rem;text-align:center'>"
                "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>INTRINSECO (GRAHAM)</div>"
                "<div style='font-size:22px;font-weight:700;color:#4ADE80'>" + moneda + " " + str(round(intrinseco, 2)) + "</div></div>"
                "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>DIFERENCIA</div>"
                "<div style='font-size:22px;font-weight:700;color:" + diff_color + "'>"
                + (("+" if diff_pct >= 0 else "") + str(round(diff_pct, 1)) + "%") + "</div></div>"
                "</div>"
                "<div style='margin-top:1rem;font-size:12px;color:#8892B0;border-top:1px solid #2D3561;padding-top:0.75rem'>"
                + ("Precio por DEBAJO del valor real — posible oportunidad" if diff_pct and diff_pct < 0 else "Precio por ENCIMA del valor real — mercado lo sobrevalora") +
                "</div></div>", unsafe_allow_html=True)
        else:
            st.info("EPS no disponible para calcular el valor intrinseco.")
 
    if fcf_hist:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin:1.5rem 0 0.5rem'>Flujo de caja historico</div>", unsafe_allow_html=True)
        with st.expander("Por que es el flujo de caja el dato mas importante"):
            st.markdown("""
El **Free Cash Flow (FCF)** es el dinero real que genera la empresa despues de pagar todas sus inversiones. Es mas dificil de manipular que el beneficio contable.
 
- FCF **creciente ano a ano**: el negocio se fortalece y genera cada vez mas caja real
- FCF **estable y positivo**: negocio solido y predecible, ideal para inversores de valor
- FCF **negativo**: la empresa quema caja. Puede ser normal en fases de inversion fuerte
- FCF **negativo sin crecer**: senal de alerta seria
 
Un FCF alto con poco capex indica un negocio que no necesita reinvertir mucho para seguir creciendo → maxima eficiencia.
            """)
        fig3 = go.Figure()
        anos = [d["year"] for d in fcf_hist]
        fcfs = [d["fcf"]/1e9 for d in fcf_hist]
        ops  = [d["op"]/1e9 for d in fcf_hist]
        fig3.add_trace(go.Bar(x=anos, y=fcfs, name="Free Cash Flow", marker_color="#6C63FF", opacity=0.9))
        fig3.add_trace(go.Bar(x=anos, y=ops, name="Cash Flow Operativo", marker_color="#34D399", opacity=0.7))
        fig3.update_layout(height=280, barmode="group", margin=dict(l=0, r=0, t=10, b=0),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           xaxis=dict(showgrid=False, color="#8892B0"),
                           yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#8892B0", title="Miles de millones " + moneda),
                           legend=dict(font=dict(color="#8892B0"), bgcolor="rgba(0,0,0,0)"),
                           hovermode="x unified")
        st.plotly_chart(fig3, use_container_width=True)
 
with tab3:
    st.markdown("<div style='background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.2);border-radius:10px;padding:0.75rem 1rem;font-size:13px;color:#8892B0;margin-bottom:1rem'>El valor de mercado cambia cada segundo. Esta influido por emociones, noticias y rumores — no siempre por los numeros reales.</div>", unsafe_allow_html=True)
 
    with st.expander("Valor de mercado vs valor fundamental: la diferencia clave"):
        st.markdown("""
**El valor de mercado** es simplemente lo que alguien esta dispuesto a pagar ahora mismo. Sube cuando hay optimismo, baja cuando hay miedo. No siempre refleja la realidad del negocio.
 
**Por que se separan precio y valor fundamental:**
- Noticias puntuales (resultados, cambios de CEO, regulacion)
- Cambios en el sentimiento general (subidas de tipos, recesion, guerra)
- Modas y narrativas (la IA, las energias renovables...)
- Ventas forzadas por fondos que necesitan liquidez
 
**Lo que debes vigilar:**
- Donde esta el precio respecto a su rango de 52 semanas
- Si esta por encima o debajo de sus medias moviles (tendencia)
- El volumen: un movimiento con mucho volumen es mas significativo
- Las posiciones cortas: si muchos profesionales apuestan a la baja, hay que ser cauteloso
        """)
 
    with st.expander("Que son la beta y las medias moviles"):
        st.markdown("""
- **Beta**: mide cuanto se mueve esta accion en relacion al mercado general. Beta 1.5 significa que si el mercado sube 10%, esta accion tiende a subir 15% (y viceversa al bajar). Beta por debajo de 1 es menos volatil.
- **Media 50 dias (MA50)**: precio promedio de los ultimos 50 dias. Si el precio actual esta por encima → tendencia alcista a corto plazo.
- **Media 200 dias (MA200)**: tendencia de largo plazo. La mas importante para inversores. Precio por encima → tendencia alcista de fondo.
- **Golden Cross**: cuando la MA50 supera a la MA200 → senal alcista fuerte.
- **Death Cross**: cuando la MA50 cae por debajo de la MA200 → senal bajista.
        """)
 
    metrics_mkt = [
        ("Precio actual", moneda + " " + str(round(precio, 2)), signo + str(round(cambio_pct, 2)) + "% hoy", "#4ADE80" if cambio_pct >= 0 else "#F87171"),
        ("Max 52 semanas", moneda + " " + str(round(w52h, 2)) if w52h else "N/D", str(round((precio-w52h)/w52h*100, 1)) + "% desde max" if w52h else "", "#F87171"),
        ("Min 52 semanas", moneda + " " + str(round(w52l, 2)) if w52l else "N/D", "+" + str(round((precio-w52l)/w52l*100, 1)) + "% desde min" if w52l else "", "#4ADE80"),
        ("Beta", str(round(beta, 2)) if beta else "N/D", "Menos volatil" if beta and beta < 1 else "Mas volatil" if beta else "", "#FBBF24" if beta and beta > 1.3 else "#4ADE80"),
        ("Media 50d", moneda + " " + str(round(media50, 2)) if media50 else "N/D", str(round((precio-media50)/media50*100, 1)) + "% vs precio" if media50 else "", "#4ADE80" if media50 and precio > media50 else "#F87171"),
        ("Media 200d", moneda + " " + str(round(media200, 2)) if media200 else "N/D", str(round((precio-media200)/media200*100, 1)) + "% vs precio" if media200 else "", "#4ADE80" if media200 and precio > media200 else "#F87171"),
    ]
    cols = st.columns(6)
    for i, (label, value, sub, color_sub) in enumerate(metrics_mkt):
        with cols[i]:
            st.markdown(
                "<div class='metric-card'><div class='label'>" + label + "</div>"
                "<div class='value'>" + value + "</div>"
                + ("<div style='font-size:11px;color:" + color_sub + ";margin-top:4px'>" + sub + "</div>" if sub else "")
                + "</div>", unsafe_allow_html=True)
 
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Volumen de negociacion</div>", unsafe_allow_html=True)
        with st.expander("Por que importa el volumen"):
            st.markdown("""
El volumen es el numero de acciones que se compran y venden. Mide la conviccion detras de un movimiento de precio.
 
- **Precio sube + volumen alto**: mucha gente comprando con conviccion → senal fuerte alcista
- **Precio sube + volumen bajo**: pocos compradores → movimiento debil, puede revertir
- **Precio baja + volumen alto**: ventas masivas, puede indicar panico o salida institucional
- **Precio baja + volumen bajo**: pocos vendedores, caida sin conviccion → puede recuperar
 
Un ratio mayor de 2x respecto al volumen medio indica algo inusual: noticias importantes o movimiento de un fondo grande.
            """)
        vol_ratio = round(vol / sf(ov.get("SharesFloat"), 1), 2) if vol else 0
        st.markdown(
            "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:12px;padding:1.25rem'>"
            "<div style='text-align:center'>"
            "<div style='font-size:11px;color:#8892B0;margin-bottom:4px'>VOLUMEN HOY</div>"
            "<div style='font-size:28px;font-weight:700;color:#E6F1FF'>" + (str(round(vol/1e6, 1)) + "M" if vol else "N/D") + "</div>"
            "</div></div>", unsafe_allow_html=True)
 
    with col2:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Crecimiento del negocio</div>", unsafe_allow_html=True)
        with st.expander("Por que importa el crecimiento"):
            st.markdown("""
Una empresa que crece justifica pagar un precio mas alto.
 
- **Crecimiento de ingresos > 15%**: empresa en expansion fuerte
- **Crecimiento negativo**: el negocio se contrae, senal de alerta
- **EPS forward > EPS trailing**: se esperan mejores beneficios el proximo ano, el negocio mejora
- **Crecimiento de beneficios sin crecimiento de ingresos**: puede ser mejora de eficiencia o recorte de costes (positivo a corto plazo pero insostenible a largo)
            """)
        df_crec = pd.DataFrame({
            "Metrica": ["Crec. ingresos (YoY)", "Crec. beneficios (YoY)", "EPS actual"],
            "Valor": [
                str(round(crec_ing*100, 1)) + "%" if crec_ing else "N/D",
                str(round(crec_ben*100, 1)) + "%" if crec_ben else "N/D",
                moneda + " " + str(round(eps, 2)) if eps else "N/D",
            ],
            "Senal": [
                "Fuerte" if crec_ing and crec_ing > 0.15 else ("Negativo" if crec_ing and crec_ing < 0 else "Moderado") if crec_ing else "—",
                "Fuerte" if crec_ben and crec_ben > 0.15 else ("Negativo" if crec_ben and crec_ben < 0 else "Moderado") if crec_ben else "—",
                "—"
            ]
        })
        st.dataframe(df_crec, hide_index=True, use_container_width=True)
 
    alertas_mkt = [a for a in alertas if any(x in a["tipo"] for x in ["MAXIMOS", "MINIMOS", "CROSS", "CAIDA", "SENAL"])]
    if alertas_mkt:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin:1rem 0 0.5rem'>Alertas de mercado</div>", unsafe_allow_html=True)
        for a in alertas_mkt:
            st.markdown(
                "<div style='background:" + a["bg"] + ";border-left:3px solid " + a["color"] + ";border-radius:0 10px 10px 0;padding:0.75rem 1rem;margin-bottom:0.5rem'>"
                "<div style='font-size:10px;color:" + a["color"] + ";font-weight:700;letter-spacing:1px'>" + a["icono"] + " " + a["tipo"] + "</div>"
                "<div style='font-size:13px;color:#E6F1FF;margin-top:4px'>" + a["titulo"] + "</div>"
                "<div style='font-size:12px;color:#8892B0;margin-top:4px'>" + a["que_hacer"] + "</div>"
                "</div>", unsafe_allow_html=True)
 
with tab4:
    with st.expander("Como funciona el sistema de puntuacion"):
        st.markdown("""
El sistema evalua la accion en **5 dimensiones**, cada una con un maximo de 20 puntos.
 
**1. Valoracion relativa (PER/P/B)**: estas pagando un precio razonable? Un PER bajo y P/Book bajo suman puntos.
 
**2. Calidad del negocio (ROE/margen)**: es un buen negocio? Un ROE alto y margen neto solido indican ventaja competitiva.
 
**3. Salud financiera (deuda)**: puede aguantar una crisis? Poca deuda suma puntos. Mucha deuda resta.
 
**4. Momentum y precio relativo**: como esta el precio respecto a sus niveles historicos? Cerca de minimos con buenos fundamentales suma puntos.
 
**5. Brecha DCF (precio vs intrinseco)**: esta es la dimension mas importante. Si el precio esta por debajo del valor intrinseco hay margen de seguridad → suma muchos puntos.
 
**Escala:** 65-100 → COMPRAR · 40-64 → MANTENER · 0-39 → VENDER
 
Esta herramienta es de apoyo. Siempre combina este analisis con tu propio juicio y contexto del sector.
        """)
 
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            "<div class='score-card'>"
            "<div style='font-size:11px;color:#8892B0;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px'>Puntuacion total</div>"
            "<div style='font-size:72px;font-weight:700;color:" + color_final + ";line-height:1'>" + str(total) + "</div>"
            "<div style='font-size:12px;color:#8892B0;margin-bottom:16px'>/ 100 puntos</div>"
            "<div style='background:" + bg_final + ";border:1px solid " + border_final + ";border-radius:20px;padding:8px 20px;display:inline-block'>"
            "<span style='font-size:18px;font-weight:700;color:" + color_final + "'>" + rec + "</span>"
            "</div>"
            "<div style='margin-top:1.5rem;padding-top:1rem;border-top:1px solid #2D3561;font-size:12px;color:#8892B0;line-height:1.8;text-align:left'>"
            "<span style='color:#4ADE80'>●</span>  65–100 &nbsp; Comprar<br>"
            "<span style='color:#FBBF24'>●</span>  40–64 &nbsp; Mantener<br>"
            "<span style='color:#F87171'>●</span>  0–39 &nbsp;&nbsp; Vender"
            "</div></div>", unsafe_allow_html=True)
 
    with col2:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:1rem'>Desglose por criterio</div>", unsafe_allow_html=True)
        criterios = [
            ("Valoracion relativa", "PER y P/Book vs referencias de mercado", s1,
             "PER: " + str(round(per, 1)) + "x · P/B: " + str(round(pb, 1)) + "x" if per and pb else "Datos insuficientes"),
            ("Calidad del negocio", "ROE y margen neto como indicadores de eficiencia", s2,
             "ROE: " + str(round(roe*100, 1)) + "% · Margen: " + str(round(margen*100, 1)) + "%" if roe and margen else "Datos insuficientes"),
            ("Salud financiera", "Nivel de deuda y apalancamiento financiero", s3,
             "Deuda/Capital: " + str(round(deuda_cap, 2)) + "x" if deuda_cap else "Datos insuficientes"),
            ("Momentum de precio", "Posicion en rango 52s y vs objetivo analistas", s4,
             "Rango 52s: " + str(round(w52l, 0)) + " — " + str(round(w52h, 0)) if w52l and w52h else "Datos insuficientes"),
            ("Brecha precio vs intrinseco", "Diferencia entre precio de mercado y valor calculado", s5,
             "Intrinseco: " + moneda + " " + str(round(intrinseco, 2)) + " · Precio: " + moneda + " " + str(round(precio, 2)) if intrinseco else "EPS no disponible"),
        ]
        for nombre_c, descripcion, pts, detalle in criterios:
            pct = pts / 20 * 100
            color_barra = "#4ADE80" if pts >= 14 else "#FBBF24" if pts >= 8 else "#F87171"
            st.markdown(
                "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:10px;padding:1rem 1.25rem;margin-bottom:8px'>"
                "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:4px'>"
                "<div><div style='font-size:13px;font-weight:600;color:#E6F1FF'>" + nombre_c + "</div>"
                "<div style='font-size:11px;color:#8892B0'>" + descripcion + "</div></div>"
                "<div style='font-size:20px;font-weight:700;color:" + color_barra + ";min-width:50px;text-align:right'>"
                + str(pts) + "<span style='font-size:12px;color:#8892B0'>/20</span></div>"
                "</div>"
                "<div style='background:#0F1117;border-radius:4px;height:6px;margin:8px 0'>"
                "<div style='background:" + color_barra + ";width:" + str(pct) + "%;height:6px;border-radius:4px'></div>"
                "</div>"
                "<div style='font-size:11px;color:#475569'>" + detalle + "</div>"
                "</div>", unsafe_allow_html=True)
 
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:#475569;text-align:center'>StockAnalyzer Pro · Datos via Alpha Vantage · Solo fines educativos · No constituye asesoramiento financiero</div>", unsafe_allow_html=True)
