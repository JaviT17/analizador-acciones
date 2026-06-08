import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
 
st.set_page_config(
    page_title="StockAnalyzer Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main-header { background: linear-gradient(135deg, #1A1D2E 0%, #16213E 100%); border: 1px solid #2D3561; border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; }
.metric-card { background: #1A1D2E; border: 1px solid #2D3561; border-radius: 12px; padding: 1rem 1.25rem; text-align: center; }
.metric-card .label { font-size: 11px; color: #8892B0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.metric-card .value { font-size: 22px; font-weight: 600; color: #E6F1FF; }
.metric-card .sub { font-size: 11px; color: #8892B0; margin-top: 4px; }
.score-card { background: #1A1D2E; border: 1px solid #2D3561; border-radius: 16px; padding: 2rem; text-align: center; }
[data-testid="stMetricValue"] { font-size: 20px !important; font-weight: 600 !important; }
[data-testid="stMetricLabel"] { font-size: 11px !important; color: #8892B0 !important; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)
 
try:
    FMP_KEY = st.secrets["FMP_API_KEY"]
except Exception as e:
    FMP_KEY = "demo"
 
FMP_BASE = "https://financialmodelingprep.com/api/v3"
 
def fmp_get(endpoint, params={}):
    params["apikey"] = FMP_KEY
    try:
        r = requests.get(FMP_BASE + endpoint, params=params, timeout=15)
        data = r.json()
        if isinstance(data, dict) and "Error Message" in data:
            return None
        return data
    except:
        return None
 
@st.cache_data(ttl=900)
def get_quote(ticker):
    return fmp_get("/quote/" + ticker)
 
@st.cache_data(ttl=3600)
def get_profile(ticker):
    return fmp_get("/profile/" + ticker)
 
@st.cache_data(ttl=3600)
def get_ratios(ticker):
    return fmp_get("/ratios-ttm/" + ticker)
 
@st.cache_data(ttl=3600)
def get_cashflow(ticker):
    return fmp_get("/cash-flow-statement/" + ticker, {"limit": 5})
 
@st.cache_data(ttl=3600)
def get_income(ticker):
    return fmp_get("/income-statement/" + ticker, {"limit": 5})
 
@st.cache_data(ttl=3600)
def get_balance(ticker):
    return fmp_get("/balance-sheet-statement/" + ticker, {"limit": 1})
 
@st.cache_data(ttl=3600)
def get_history(ticker):
    return fmp_get("/historical-price-full/" + ticker, {"serietype": "line"})
 
@st.cache_data(ttl=3600)
def get_analyst(ticker):
    return fmp_get("/analyst-stock-recommendations/" + ticker, {"limit": 1})
 
@st.cache_data(ttl=3600)
def search_company(query):
    return fmp_get("/search", {"query": query, "limit": 10})
 
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
        results = search_company(busqueda)
        if results:
            st.markdown("**Resultados:**")
            cols = st.columns(4)
            for i, m in enumerate(results[:8]):
                sym = m.get("symbol", "")
                nombre_q = m.get("name", "")
                exchange = m.get("stockExchange", "")
                with cols[i % 4]:
                    st.markdown(
                        "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:10px;padding:0.6rem 0.8rem;margin-bottom:8px'>"
                        "<div style='font-size:14px;font-weight:600;color:#6C63FF'>" + sym + "</div>"
                        "<div style='font-size:11px;color:#CCD6F6;margin-top:2px'>" + nombre_q[:28] + "</div>"
                        "<div style='font-size:10px;color:#8892B0;margin-top:2px'>" + exchange + "</div>"
                        "</div>", unsafe_allow_html=True)
                    if st.button("Usar", key="btn_" + sym, use_container_width=True):
                        st.session_state.ticker_seleccionado = sym
                        st.rerun()
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
 
with st.expander("Debug — Estado de la API (quitar cuando funcione)"):
    st.write("Clave cargada:", FMP_KEY[:8] + "..." if FMP_KEY and FMP_KEY != "demo" else "DEMO — no configurada")
    test = fmp_get("/quote/AAPL")
    st.write("Test AAPL:", test)
 
if not analizar:
    st.markdown("""
    <div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:16px;padding:3rem;text-align:center;margin-top:2rem'>
        <div style='font-size:48px;margin-bottom:1rem'>📊</div>
        <div style='font-size:18px;font-weight:600;color:#E6F1FF;margin-bottom:0.5rem'>Introduce un ticker y pulsa Analizar</div>
        <div style='font-size:13px;color:#8892B0;margin-bottom:1.5rem'>Datos en tiempo real via Financial Modeling Prep · 50+ bolsas mundiales</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
 
with st.spinner("Cargando datos..."):
    quote_list  = get_quote(ticker_input)
    profile_list = get_profile(ticker_input)
    ratios_list  = get_ratios(ticker_input)
    cf_list      = get_cashflow(ticker_input)
    inc_list     = get_income(ticker_input)
    bal_list     = get_balance(ticker_input)
    hist_data    = get_history(ticker_input)
    analyst_list = get_analyst(ticker_input)
 
if not quote_list or not profile_list:
    st.error("No se encontraron datos para **" + ticker_input + "**. Verifica el ticker.")
    if FMP_KEY == "demo":
        st.warning("Estas usando la clave demo. Registrate en financialmodelingprep.com para obtener tu clave gratuita.")
    st.stop()
 
q  = quote_list[0] if quote_list else {}
p  = profile_list[0] if profile_list else {}
r  = ratios_list[0] if ratios_list else {}
an = analyst_list[0] if analyst_list else {}
 
def safe_float(val, default=None):
    try:
        v = float(val)
        return v if v != 0 else default
    except:
        return default
 
precio        = safe_float(q.get("price"), 0)
cambio_pct    = safe_float(q.get("changesPercentage"), 0)
nombre        = p.get("companyName", ticker_input)
sector        = p.get("sector", "")
pais          = p.get("country", "")
moneda        = p.get("currency", "USD")
per           = safe_float(r.get("peRatioTTM"))
pb            = safe_float(r.get("priceToBookRatioTTM"))
ps            = safe_float(r.get("priceToSalesRatioTTM"))
roe           = safe_float(r.get("returnOnEquityTTM"))
roa           = safe_float(r.get("returnOnAssetsTTM"))
margen        = safe_float(r.get("netProfitMarginTTM"))
margen_bruto  = safe_float(r.get("grossProfitMarginTTM"))
deuda_cap     = safe_float(r.get("debtEquityRatioTTM"))
beta          = safe_float(p.get("beta"))
cap           = safe_float(q.get("marketCap"))
w52h          = safe_float(q.get("yearHigh"))
w52l          = safe_float(q.get("yearLow"))
eps           = safe_float(q.get("eps"))
target        = safe_float(p.get("dcfDiff")) 
price_target  = safe_float(an.get("priceTarget")) if an else None
media50       = safe_float(p.get("priceAvg50") or q.get("priceAvg50"))
media200      = safe_float(p.get("priceAvg200") or q.get("priceAvg200"))
vol           = safe_float(q.get("volume"))
avg_vol       = safe_float(q.get("avgVolume"))
fcf_company   = safe_float(p.get("lastDiv"))
 
hist_prices = []
hist_dates  = []
if hist_data and "historical" in hist_data:
    historical = hist_data["historical"][:52]
    historical = list(reversed(historical))
    hist_dates  = [h["date"] for h in historical]
    hist_prices = [h["close"] for h in historical]
 
fcf_hist = []
if cf_list:
    for rep in cf_list[:5]:
        try:
            fcf = safe_float(rep.get("freeCashFlow"))
            op  = safe_float(rep.get("operatingCashFlow"))
            yr  = rep.get("date", "")[:4]
            if fcf is not None:
                fcf_hist.append({"year": yr, "fcf": fcf, "op": op or 0})
        except:
            pass
 
if eps and eps > 0:
    g = 0.07
    if per:
        fwd_per_est = per * 0.9
        g = max(0.03, min(0.25, (per - fwd_per_est) / per * 0.5 + 0.05))
    intrinseco = eps * (8.5 + 2 * g * 100)
else:
    intrinseco = None
 
dcf_value = safe_float(p.get("dcf"))
if dcf_value and dcf_value > 0:
    intrinseco = dcf_value
 
diff_pct = ((precio - intrinseco) / intrinseco * 100) if intrinseco and precio else None
 
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
s4 = sc_momentum(precio, w52h, w52l, price_target, media50, media200)
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
            "que_hacer": "Considera comprar. El precio ofrece un margen de seguridad significativo.",
            "por_que": "Valor intrinseco: " + moneda + " " + str(round(intrinseco, 2)) + " — Precio: " + moneda + " " + str(round(precio, 2)) + "."})
    elif diff_pct < -15:
        alertas.append({"tipo": "POSIBLE OPORTUNIDAD", "color": "#34D399", "bg": "rgba(52,211,153,0.08)", "icono": "🟡",
            "titulo": "Precio " + str(round(abs(diff_pct))) + "% por debajo del valor fundamental",
            "que_hacer": "Hay margen de seguridad. Considera una posicion parcial y espera confirmacion.",
            "por_que": "Intrinseco (" + moneda + " " + str(round(intrinseco, 2)) + ") supera al precio (" + moneda + " " + str(round(precio, 2)) + ")."})
    elif diff_pct > 30:
        alertas.append({"tipo": "PRECIO MUY ELEVADO", "color": "#F87171", "bg": "rgba(248,113,113,0.08)", "icono": "🔴",
            "titulo": "Precio " + str(round(diff_pct)) + "% por encima del valor fundamental",
            "que_hacer": "Si tienes la accion considera reducir. Si no, evita entrar ahora.",
            "por_que": "Precio (" + moneda + " " + str(round(precio, 2)) + ") muy por encima del intrinseco (" + moneda + " " + str(round(intrinseco, 2)) + ")."})
    elif diff_pct > 15:
        alertas.append({"tipo": "PRECIO ELEVADO", "color": "#FBBF24", "bg": "rgba(251,191,36,0.08)", "icono": "🟠",
            "titulo": "Precio " + str(round(diff_pct)) + "% por encima del valor fundamental",
            "que_hacer": "No es el mejor momento de entrada. Vigila con stop-loss si ya tienes posicion.",
            "por_que": "Prima del " + str(round(diff_pct)) + "% sobre el intrinseco (" + moneda + " " + str(round(intrinseco, 2)) + ")."})
 
if w52h and precio > w52h * 0.95:
    alertas.append({"tipo": "PRECIO EN MAXIMOS ANUALES", "color": "#F87171", "bg": "rgba(248,113,113,0.08)", "icono": "🔴",
        "titulo": "Precio cerca del maximo de 52 semanas",
        "que_hacer": "Prudencia. No es buen momento de entrada salvo que el fundamental lo justifique.",
        "por_que": "A " + moneda + " " + str(round(precio, 2)) + " solo queda un " + str(round((w52h-precio)/w52h*100, 1)) + "% para el maximo anual."})
 
if w52l and precio < w52l * 1.10 and s2 >= 14:
    alertas.append({"tipo": "MINIMOS CON NEGOCIO SOLIDO", "color": "#4ADE80", "bg": "rgba(74,222,128,0.08)", "icono": "🟢",
        "titulo": "Precio en minimos anuales pero el negocio es de calidad",
        "que_hacer": "Interesante para acumular gradualmente.",
        "por_que": "Precio cerca del minimo (" + moneda + " " + str(round(w52l, 2)) + ") con calidad de negocio " + str(s2) + "/20."})
 
if deuda_cap and deuda_cap > 3:
    alertas.append({"tipo": "RIESGO FINANCIERO ELEVADO", "color": "#F87171", "bg": "rgba(248,113,113,0.08)", "icono": "🔴",
        "titulo": "Nivel de deuda muy por encima de la media",
        "que_hacer": "Incorpora este riesgo. La deuda alta es un multiplicador de riesgos en entornos de tipos altos.",
        "por_que": "Deuda/Capital: " + str(round(deuda_cap, 2)) + "x. Por encima de 2x empieza a ser preocupante."})
 
if media50 and media200:
    if media50 > media200 * 1.02:
        alertas.append({"tipo": "GOLDEN CROSS — TENDENCIA ALCISTA", "color": "#34D399", "bg": "rgba(52,211,153,0.08)", "icono": "🟡",
            "titulo": "Media 50d supera a media 200d",
            "que_hacer": "Senal tecnica positiva. El momentum de medio plazo es favorable.",
            "por_que": "MA50 (" + str(round(media50, 2)) + ") > MA200 (" + str(round(media200, 2)) + ")."})
    elif media50 < media200 * 0.98:
        alertas.append({"tipo": "DEATH CROSS — TENDENCIA BAJISTA", "color": "#FBBF24", "bg": "rgba(251,191,36,0.08)", "icono": "🟠",
            "titulo": "Media 50d por debajo de media 200d",
            "que_hacer": "Senal tecnica negativa. Espera confirmacion de giro antes de entrar.",
            "por_que": "MA50 (" + str(round(media50, 2)) + ") < MA200 (" + str(round(media200, 2)) + ")."})
 
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
 
tab1, tab2, tab3, tab4 = st.tabs(["Resumen", "Valor fundamental", "Valor de mercado", "Puntuacion"])
 
with tab1:
    metrics = [
        ("Precio actual", moneda + " " + str(round(precio, 2)), ""),
        ("Valor intrinseco", moneda + " " + str(round(intrinseco, 2)) if intrinseco else "N/D", "DCF / Graham"),
        ("Diferencia", (("+" if diff_pct >= 0 else "") + str(round(diff_pct, 1)) + "%") if diff_pct is not None else "N/D", "Precio vs fundamental"),
        ("PER", str(round(per, 1)) + "x" if per else "N/D", "< 15 barato  > 30 caro"),
        ("Cap. bursatil", moneda + " " + str(round(cap/1e9, 1)) + "B" if cap else "N/D", ""),
        ("Obj. analistas", moneda + " " + str(round(price_target, 2)) if price_target else "N/D",
         (("+" if price_target >= precio else "") + str(round((price_target-precio)/precio*100, 1)) + "% potencial") if price_target else ""),
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
            fig.add_trace(go.Scatter(
                x=hist_dates, y=hist_prices,
                line=dict(color="#6C63FF", width=2),
                fill="tozeroy", fillcolor="rgba(108,99,255,0.06)",
                name="Precio", hovertemplate=moneda + " %{y:.2f}<extra></extra>"
            ))
            if intrinseco:
                fig.add_hline(y=intrinseco, line_dash="dash", line_color="#4ADE80", line_width=1,
                              annotation_text="Intrinseco " + str(round(intrinseco, 0)),
                              annotation_font_color="#4ADE80", annotation_font_size=11)
            if price_target:
                fig.add_hline(y=price_target, line_dash="dot", line_color="#FBBF24", line_width=1,
                              annotation_text="Objetivo " + str(round(price_target, 0)),
                              annotation_font_color="#FBBF24", annotation_font_size=11)
            if media200:
                fig.add_hline(y=media200, line_dash="dot", line_color="#8892B0", line_width=1,
                              annotation_text="MA200 " + str(round(media200, 0)),
                              annotation_font_color="#8892B0", annotation_font_size=11)
            fig.update_layout(
                height=360, margin=dict(l=0, r=80, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, color="#8892B0"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#8892B0", title=moneda),
                hovermode="x unified", showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        with st.expander("Como leer este grafico"):
            st.markdown("""
- **Linea morada**: precio real de la accion en bolsa cada semana
- **Linea verde discontinua**: valor intrinseco estimado por DCF/Graham (lo que deberia valer)
- **Linea amarilla punteada**: precio objetivo medio de los analistas profesionales
- **Linea gris punteada**: media movil de 200 dias (tendencia de largo plazo)
 
**La clave esta en la relacion entre la linea morada y la verde:**
- Precio muy por DEBAJO de la verde → el mercado infravalora la empresa → posible oportunidad
- Precio muy por ENCIMA de la verde → el mercado sobrevalora la empresa → precaucion
- Precio cerca de la verde → valoracion justa
 
Si el precio cruza la MA200 al alza con volumen → señal alcista de largo plazo.
Si la cruza a la baja → señal bajista de largo plazo.
            """)
 
    with col2:
        st.markdown("<div style='font-size:14px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Posicion en rango anual</div>", unsafe_allow_html=True)
        if w52h and w52l and w52h != w52l:
            pos_pct = round((precio - w52l) / (w52h - w52l) * 100)
            pos_pct = max(0, min(100, pos_pct))
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
    values_bar = [w52l, precio, intrinseco, price_target, w52h]
    colors_bar = ["#475569", "#6C63FF", "#4ADE80", "#FBBF24", "#F87171"]
    fig2 = go.Figure(go.Bar(
        x=labels_bar, y=values_bar, marker_color=colors_bar,
        text=[str(round(v, 1)) if v else "N/D" for v in values_bar],
        textposition="outside", textfont=dict(color="#CCD6F6", size=12)
    ))
    fig2.update_layout(
        height=260, margin=dict(l=0, r=0, t=20, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, color="#8892B0"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#8892B0", title=moneda),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)
 
with tab2:
    st.markdown("<div style='background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.2);border-radius:10px;padding:0.75rem 1rem;font-size:13px;color:#8892B0;margin-bottom:1rem'>El valor fundamental mide la salud REAL del negocio. Estos numeros cambian trimestralmente, no cada dia. Son los que importan para saber si una empresa vale lo que cuesta.</div>", unsafe_allow_html=True)
 
    with st.expander("Que es el valor fundamental y por que importa"):
        st.markdown("""
Mientras el precio de mercado sube y baja cada segundo segun el humor de los inversores,
el valor fundamental cambia lentamente y refleja la realidad del negocio.
 
**La idea clave de Benjamin Graham** (mentor de Warren Buffett):
> "A corto plazo el mercado es una maquina de votar. A largo plazo es una maquina de pesar."
 
Es decir: a corto plazo gana la popularidad y el miedo. A largo plazo, lo que pesa de verdad
son los numeros reales. Por eso comparar precio vs fundamental es tan util.
 
**Cuando el precio esta muy por debajo del fundamental** → el mercado esta siendo irracional
y hay una oportunidad de compra con margen de seguridad.
 
**Cuando el precio esta muy por encima** → el mercado descuenta demasiado optimismo
y el riesgo de correccion es alto.
        """)
 
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Valoracion</div>", unsafe_allow_html=True)
        with st.expander("Que mide la valoracion"):
            st.markdown("""
- **PER (Precio/Beneficio)**: cuantos años de beneficios pagas por la accion.
  Si el PER es 20x significa que pagas 20 años de beneficios actuales.
  Menos de 15x suele ser barato. Mas de 30x suele ser caro.
  Ojo: un PER alto puede estar justificado si la empresa crece muy rapido.
 
- **P/Book (Precio/Valor contable)**: cuanto pagas vs lo que valen los activos netos.
  Si P/Book es menor que 1, pagas menos que el valor de los activos → muy barato.
  Por encima de 6x el mercado paga una prima muy alta sobre los activos reales.
 
- **P/Ventas**: cuantas veces pagas los ingresos anuales de la empresa.
  Util para empresas que aun no tienen beneficios (startups, empresas en crecimiento).
 
- **Regla general**: estos ratios solo tienen sentido comparados con el sector.
  Un PER de 30x es caro para un banco pero puede ser normal para una tecnologica.
            """)
        df_val = pd.DataFrame({
            "Metrica": ["PER", "P / Book", "P / Ventas"],
            "Valor": [
                str(round(per, 2)) + "x" if per else "N/D",
                str(round(pb, 2)) + "x" if pb else "N/D",
                str(round(ps, 2)) + "x" if ps else "N/D",
            ],
            "Referencia": ["< 15 barato · > 30 caro", "< 1.5 barato · > 6 caro", "Depende del sector"],
            "Senal": [
                "Barato" if per and per < 15 else ("Caro" if per and per > 30 else "Normal") if per else "—",
                "Barato" if pb and pb < 1.5 else ("Caro" if pb and pb > 6 else "Normal") if pb else "—",
                "—"
            ]
        })
        st.dataframe(df_val, hide_index=True, use_container_width=True)
 
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin:1rem 0 0.5rem'>Rentabilidad</div>", unsafe_allow_html=True)
        with st.expander("Que mide la rentabilidad"):
            st.markdown("""
- **ROE (Return on Equity)**: beneficio que genera la empresa por cada euro de capital propio.
  Por encima del 15% indica que el negocio es eficiente generando valor para el accionista.
  Por debajo del 5% es una señal de negocio debil o con mucho capital ocioso.
 
- **ROA (Return on Assets)**: beneficio sobre el total de activos. Mide la eficiencia global.
  Por encima del 10% es bueno. Muy util para comparar empresas del mismo sector.
 
- **Margen neto**: de cada 100 euros que ingresa la empresa, cuanto queda como beneficio final.
  Un margen del 20% significa que de 100 euros vendidos, 20 son beneficio neto.
  Margenes negativos indican que la empresa pierde dinero con su actividad principal.
 
- **Margen bruto**: rentabilidad antes de gastos generales. Indica la fortaleza del negocio central.
  Un margen bruto alto (>40%) suele indicar un negocio con ventaja competitiva (pricing power).
            """)
        df_rent = pd.DataFrame({
            "Metrica": ["ROE", "ROA", "Margen neto", "Margen bruto"],
            "Valor": [
                str(round(roe*100, 1)) + "%" if roe else "N/D",
                str(round(roa*100, 1)) + "%" if roa else "N/D",
                str(round(margen*100, 1)) + "%" if margen else "N/D",
                str(round(margen_bruto*100, 1)) + "%" if margen_bruto else "N/D",
            ],
            "Referencia": ["> 15% bueno", "> 10% bueno", "> 15% bueno", "> 30% solido"],
            "Senal": [
                "Bueno" if roe and roe > 0.15 else ("Bajo" if roe and roe < 0.05 else "Normal") if roe else "—",
                "Bueno" if roa and roa > 0.10 else ("Bajo" if roa and roa < 0.03 else "Normal") if roa else "—",
                "Bueno" if margen and margen > 0.15 else ("Bajo" if margen and margen < 0.05 else "Normal") if margen else "—",
                "—"
            ]
        })
        st.dataframe(df_rent, hide_index=True, use_container_width=True)
 
    with col2:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Salud financiera</div>", unsafe_allow_html=True)
        with st.expander("Que es la salud financiera"):
            st.markdown("""
- **Deuda/Capital**: cuanta deuda tiene la empresa en relacion a su capital propio.
  Por debajo de 0.5x es baja y comoda. Por encima de 3x empieza a ser preocupante.
  Una empresa muy endeudada es fragil: si el negocio flojea o suben los tipos de interes,
  puede tener serios problemas para pagar sus deudas.
 
- **Quick Ratio**: capacidad de pagar deudas a corto plazo con activos liquidos.
  Por encima de 1 significa que puede cubrir sus deudas inmediatas sin problemas.
  Por debajo de 1 puede tener tension de liquidez.
 
- **Current Ratio**: similar al Quick Ratio pero incluyendo inventario.
  Por encima de 1.5 es una posicion comoda. Por debajo de 1 es señal de alerta.
 
- **Efectivo vs Deuda**: comparar ambos es clave. Una empresa con mucha deuda pero mas
  efectivo todavia tiene margen. El problema es cuando la deuda supera ampliamente al efectivo.
            """)
        bal = bal_list[0] if bal_list else {}
        total_debt = safe_float(bal.get("totalDebt"))
        total_cash = safe_float(bal.get("cashAndCashEquivalents"))
        current_ratio = safe_float(bal.get("currentRatio") or r.get("currentRatioTTM"))
        quick_ratio = safe_float(r.get("quickRatioTTM"))
        df_fin = pd.DataFrame({
            "Metrica": ["Deuda/Capital", "Quick Ratio", "Current Ratio", "Deuda total", "Efectivo"],
            "Valor": [
                str(round(deuda_cap, 2)) + "x" if deuda_cap else "N/D",
                str(round(quick_ratio, 2)) if quick_ratio else "N/D",
                str(round(current_ratio, 2)) if current_ratio else "N/D",
                moneda + " " + str(round(total_debt/1e9, 1)) + "B" if total_debt else "N/D",
                moneda + " " + str(round(total_cash/1e9, 1)) + "B" if total_cash else "N/D",
            ],
            "Senal": [
                "Baja" if deuda_cap and deuda_cap < 0.5 else ("Alta" if deuda_cap and deuda_cap > 3 else "Media") if deuda_cap else "—",
                "OK" if quick_ratio and quick_ratio > 1 else ("Bajo" if quick_ratio else "—"),
                "OK" if current_ratio and current_ratio > 1.5 else ("Bajo" if current_ratio else "—"),
                "—", "—"
            ]
        })
        st.dataframe(df_fin, hide_index=True, use_container_width=True)
 
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin:1rem 0 0.75rem'>Valor intrinseco (DCF)</div>", unsafe_allow_html=True)
        if intrinseco:
            diff_color = "#4ADE80" if diff_pct and diff_pct < 0 else "#F87171"
            st.markdown(
                "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:12px;padding:1.25rem'>"
                "<div style='display:grid;grid-template-columns:1fr 1fr;gap:1rem;text-align:center'>"
                "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>VALOR DCF</div>"
                "<div style='font-size:22px;font-weight:700;color:#4ADE80'>" + moneda + " " + str(round(intrinseco, 2)) + "</div></div>"
                "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>DIFERENCIA</div>"
                "<div style='font-size:22px;font-weight:700;color:" + diff_color + "'>"
                + (("+" if diff_pct >= 0 else "") + str(round(diff_pct, 1)) + "%") + "</div></div>"
                "</div>"
                "<div style='margin-top:1rem;font-size:12px;color:#8892B0;border-top:1px solid #2D3561;padding-top:0.75rem'>"
                + ("Precio por DEBAJO del valor real — posible oportunidad" if diff_pct and diff_pct < 0 else "Precio por ENCIMA del valor real — mercado lo sobrevalora") +
                "</div></div>", unsafe_allow_html=True)
        else:
            st.info("Datos insuficientes para calcular el valor intrinseco.")
 
    if fcf_hist:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin:1.5rem 0 0.5rem'>Flujo de caja historico</div>", unsafe_allow_html=True)
        with st.expander("Por que es el flujo de caja el dato mas importante"):
            st.markdown("""
El **Free Cash Flow (FCF)** es el dinero real que genera la empresa despues de pagar
todas sus inversiones en activos (maquinaria, tecnologia, infraestructura).
 
**Por que importa mas que el beneficio contable:**
El beneficio neto puede manipularse con criterios contables (amortizaciones, provisiones...).
El flujo de caja es mucho mas dificil de falsear porque es dinero que entra y sale de verdad.
 
**Como leer el grafico:**
- FCF **creciente año a año**: el negocio se fortalece y genera cada vez mas caja real
- FCF **estable y positivo**: negocio solido y predecible, ideal para inversores de valor
- FCF **negativo**: la empresa quema caja. Puede ser normal en fases de inversion fuerte
  (Amazon durante años tuvo FCF negativo mientras construia su infraestructura)
- FCF **negativo y sin crecer**: señal de alerta seria
 
**La diferencia entre FCF y Cash Flow Operativo:**
El operativo es el dinero generado por el negocio antes de inversiones.
El FCF descuenta las inversiones (capex). Un FCF alto con poco capex indica un negocio
que no necesita reinvertir mucho para seguir creciendo → maxima eficiencia.
            """)
        fig3 = go.Figure()
        anos = [d["year"] for d in fcf_hist]
        fcfs = [d["fcf"]/1e9 for d in fcf_hist]
        ops  = [d["op"]/1e9 for d in fcf_hist]
        fig3.add_trace(go.Bar(x=anos, y=fcfs, name="Free Cash Flow", marker_color="#6C63FF", opacity=0.9))
        fig3.add_trace(go.Bar(x=anos, y=ops, name="Cash Flow Operativo", marker_color="#34D399", opacity=0.7))
        fig3.update_layout(
            height=280, barmode="group", margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, color="#8892B0"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#8892B0", title="Miles de millones " + moneda),
            legend=dict(font=dict(color="#8892B0"), bgcolor="rgba(0,0,0,0)"),
            hovermode="x unified"
        )
        st.plotly_chart(fig3, use_container_width=True)
 
with tab3:
    st.markdown("<div style='background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.2);border-radius:10px;padding:0.75rem 1rem;font-size:13px;color:#8892B0;margin-bottom:1rem'>El valor de mercado cambia cada segundo. Esta influido por emociones, noticias y rumores — no siempre por los numeros reales.</div>", unsafe_allow_html=True)
 
    with st.expander("Valor de mercado vs valor fundamental: la diferencia clave"):
        st.markdown("""
**El valor de mercado** es simplemente lo que alguien esta dispuesto a pagar ahora mismo.
Sube cuando hay optimismo, baja cuando hay miedo. No siempre refleja la realidad del negocio.
 
**Por que se separan precio y valor fundamental:**
- Noticias puntuales (buenos o malos resultados, cambios de CEO, regulacion)
- Cambios en el sentimiento general del mercado (subidas de tipos, recesion)
- Modas y narrativas (la IA, las energias renovables, el metaverso...)
- Ventas forzadas por fondos que necesitan liquidez
 
**Lo que debes vigilar en el valor de mercado:**
- Donde esta el precio respecto a su rango de 52 semanas
- Si el precio esta por encima o debajo de sus medias moviles (tendencia)
- El volumen: un movimiento con mucho volumen es mas significativo que uno con poco
- Las posiciones cortas: si muchos profesionales apuestan a la baja, hay que ser cauteloso
        """)
 
    with st.expander("Que son la beta y las medias moviles"):
        st.markdown("""
- **Beta**: mide cuanto se mueve esta accion en relacion al mercado general (S&P 500).
  Beta 1.0 = se mueve igual que el mercado.
  Beta 1.5 = si el mercado sube 10%, esta accion tiende a subir 15% (y viceversa al bajar).
  Beta 0.5 = menos volatil, se mueve la mitad que el mercado.
  Beta negativa = se mueve en direccion opuesta al mercado (raro, tipico del oro o bonos).
 
- **Media 50 dias (MA50)**: precio promedio de los ultimos 50 dias de trading.
  Si el precio actual esta por encima → tendencia alcista a corto plazo.
  Si esta por debajo → tendencia bajista a corto plazo.
 
- **Media 200 dias (MA200)**: tendencia de largo plazo. La mas importante para inversores.
  Precio por encima de la MA200 → el activo esta en tendencia alcista de fondo.
  Precio por debajo → tendencia bajista de fondo.
 
- **Golden Cross**: cuando la MA50 supera a la MA200 → senal alcista fuerte de medio plazo.
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
El volumen es el numero de acciones que se compran y venden en un periodo.
Es la forma de medir la **conviccion** detras de un movimiento de precio.
 
- **Precio sube + volumen alto**: mucha gente comprando con conviccion → senal fuerte alcista
- **Precio sube + volumen bajo**: pocos compradores → movimiento debil, puede revertir
- **Precio baja + volumen alto**: ventas masivas, puede indicar panico o salida institucional
- **Precio baja + volumen bajo**: pocos vendedores, caida sin conviccion → puede recuperar
 
Un **ratio > 2x** respecto al volumen medio indica algo inusual: noticias importantes,
entrada o salida de un fondo grande, o un evento corporativo relevante.
            """)
 
        vol_ratio = round(vol / avg_vol, 2) if avg_vol and vol else 0
        vol_color = "#4ADE80" if vol_ratio > 1.5 else "#FBBF24" if vol_ratio > 0.8 else "#F87171"
        st.markdown(
            "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:12px;padding:1.25rem'>"
            "<div style='display:grid;grid-template-columns:1fr 1fr;gap:1rem;text-align:center'>"
            "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>VOLUMEN HOY</div>"
            "<div style='font-size:20px;font-weight:600;color:#E6F1FF'>" + (str(round(vol/1e6, 1)) + "M" if vol else "N/D") + "</div></div>"
            "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>VOLUMEN MEDIO</div>"
            "<div style='font-size:20px;font-weight:600;color:#E6F1FF'>" + (str(round(avg_vol/1e6, 1)) + "M" if avg_vol else "N/D") + "</div></div>"
            "</div>"
            "<div style='margin-top:1rem;font-size:12px;color:#8892B0;border-top:1px solid #2D3561;padding-top:0.75rem'>"
            "Ratio vs media: <span style='color:" + vol_color + ";font-weight:600'>" + str(vol_ratio) + "x</span>"
            + (" — Volumen inusualmente alto" if vol_ratio > 2 else " — Volumen normal" if vol_ratio > 0.8 else " — Volumen bajo") +
            "</div></div>", unsafe_allow_html=True)
 
    with col2:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.75rem'>Descripcion de la empresa</div>", unsafe_allow_html=True)
        desc = p.get("description", "")
        if desc:
            st.markdown(
                "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:12px;padding:1.25rem;font-size:12px;color:#8892B0;line-height:1.7;max-height:150px;overflow:hidden'>"
                + desc[:400] + "..."
                + "</div>", unsafe_allow_html=True)
 
    alertas_mkt = [a for a in alertas if any(x in a["tipo"] for x in ["MAXIMOS", "MINIMOS", "CROSS", "CAIDA"])]
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
 
**1. Valoracion relativa (PER/P/B)** — Estas pagando un precio razonable?
Compara el precio actual con los beneficios y activos de la empresa.
Un precio bajo respecto a los beneficios (PER bajo) suma puntos. Uno muy alto los resta.
 
**2. Calidad del negocio (ROE/margen)** — Es un buen negocio?
Mide si la empresa genera dinero de verdad y con eficiencia.
Un ROE alto y margen neto solido indican un negocio con ventaja competitiva.
 
**3. Salud financiera (deuda)** — Puede aguantar una crisis?
Una empresa con poca deuda es resiliente. Con mucha deuda es fragil ante adversidades.
En entornos de tipos de interes altos, la deuda alta puede volverse un problema grave.
 
**4. Momentum y precio relativo** — Como esta el precio respecto a sus niveles historicos?
Si el precio esta cerca de minimos anuales con buenos fundamentales, suma puntos.
Si esta en maximos historicos con poco margen, resta puntos.
 
**5. Brecha DCF (precio vs intrinseco)** — Cuanto vale realmente vs cuanto cuesta?
Esta es la dimension mas importante. Si el precio esta por debajo del valor intrinseco
calculado por DCF/Graham, hay margen de seguridad → suma muchos puntos.
 
**Escala final:**
- 65-100 puntos → COMPRAR: hay margen de seguridad claro
- 40-64 puntos → MANTENER: valoracion justa, sin ventaja clara
- 0-39 puntos → VENDER: precio significativamente por encima del valor real
 
**Importante**: este sistema es una herramienta de apoyo, no una recomendacion financiera.
Siempre combina este analisis con tu propio juicio y contexto del sector.
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
            ("Salud financiera", "Nivel de deuda y apalancamiento", s3,
             "Deuda/Capital: " + str(round(deuda_cap, 2)) + "x" if deuda_cap else "Datos insuficientes"),
            ("Momentum de precio", "Posicion en rango 52s y vs objetivo analistas", s4,
             "Rango 52s: " + str(round(w52l, 0)) + " — " + str(round(w52h, 0)) if w52l and w52h else "Datos insuficientes"),
            ("Brecha precio vs intrinseco", "Diferencia entre precio de mercado y valor DCF", s5,
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
    st.markdown("<div style='font-size:11px;color:#475569;text-align:center'>StockAnalyzer Pro · Datos via Financial Modeling Prep · Solo fines educativos · No constituye asesoramiento financiero</div>", unsafe_allow_html=True)
