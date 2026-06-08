import streamlit as st
import yfinance as yf
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

.main-header {
    background: linear-gradient(135deg, #1A1D2E 0%, #16213E 100%);
    border: 1px solid #2D3561;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #1A1D2E;
    border: 1px solid #2D3561;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    text-align: center;
}
.metric-card .label {
    font-size: 11px;
    color: #8892B0;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.metric-card .value {
    font-size: 22px;
    font-weight: 600;
    color: #E6F1FF;
}
.metric-card .sub {
    font-size: 11px;
    color: #8892B0;
    margin-top: 4px;
}
.alert-card {
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    border-left: 4px solid;
}
.score-card {
    background: #1A1D2E;
    border: 1px solid #2D3561;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}
.tag {
    display: inline-block;
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 500;
    letter-spacing: 0.5px;
}
.divider {
    border: none;
    border-top: 1px solid #2D3561;
    margin: 1.5rem 0;
}
[data-testid="stMetricValue"] { font-size: 20px !important; font-weight: 600 !important; }
[data-testid="stMetricLabel"] { font-size: 11px !important; color: #8892B0 !important; text-transform: uppercase; letter-spacing: 1px; }
div[data-testid="stTabs"] button { font-size: 13px; font-weight: 500; }
.stDataFrame { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

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
    busqueda = st.text_input("", placeholder="🔍  Buscar empresa: Inditex, Verisure, LVMH...", label_visibility="collapsed")
with col_ticker:
    ticker_input = st.text_input("", value=st.session_state.ticker_seleccionado,
                                  placeholder="AAPL · ITX.MC · VSURE.ST", label_visibility="collapsed").upper()
    st.session_state.ticker_seleccionado = ticker_input
with col_btn:
    analizar = st.button("Analizar →", type="primary", use_container_width=True)

if busqueda:
    with st.spinner("Buscando..."):
        try:
            resultados = yf.Search(busqueda, max_results=15)
            quotes = resultados.quotes
            if quotes:
                exchange_map = {
                    "NMS": "NASDAQ", "NYQ": "NYSE", "NGM": "NASDAQ",
                    "STO": "Stockholm", "FRA": "Frankfurt", "PAR": "Paris",
                    "LSE": "London", "MIL": "Milan", "MCE": "Madrid",
                    "AMS": "Amsterdam", "EPA": "Paris", "EBS": "Swiss",
                    "TYO": "Tokyo", "HKG": "HK", "ASX": "ASX", "TSX": "TSX"
                }
                cols = st.columns(4)
                idx = 0
                for q in quotes:
                    sym = q.get("symbol", "")
                    nombre_q = q.get("longname") or q.get("shortname", "")
                    exchange = q.get("exchange", "")
                    tipo = q.get("quoteType", "")
                    if tipo != "EQUITY" or not nombre_q:
                        continue
                    exchange_nombre = exchange_map.get(exchange, exchange)
                    with cols[idx % 4]:
                        st.markdown(
                            "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:10px;padding:0.6rem 0.8rem;margin-bottom:8px'>"
                            "<div style='font-size:14px;font-weight:600;color:#6C63FF'>" + sym + "</div>"
                            "<div style='font-size:11px;color:#CCD6F6;margin-top:2px'>" + nombre_q[:28] + "</div>"
                            "<div style='font-size:10px;color:#8892B0;margin-top:2px'>" + exchange_nombre + "</div>"
                            "</div>", unsafe_allow_html=True)
                        if st.button("↗", key="btn_" + sym, use_container_width=True):
                            st.session_state.ticker_seleccionado = sym
                            st.rerun()
                    idx += 1
                    if idx >= 8:
                        break
        except Exception:
            pass

with st.expander("📖  Sufijos por mercado"):
    st.markdown("""
<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px;font-size:13px'>
<div><strong style='color:#6C63FF'>.MC</strong> Madrid · ITX.MC</div>
<div><strong style='color:#6C63FF'>.DE</strong> Frankfurt · BMW.DE</div>
<div><strong style='color:#6C63FF'>.PA</strong> Paris · MC.PA</div>
<div><strong style='color:#6C63FF'>.L</strong> Londres · HSBA.L</div>
<div><strong style='color:#6C63FF'>.ST</strong> Estocolmo · VSURE.ST</div>
<div><strong style='color:#6C63FF'>.MI</strong> Milan · ENI.MI</div>
<div><strong style='color:#6C63FF'>.AS</strong> Amsterdam · ASML.AS</div>
<div><strong style='color:#6C63FF'>.SW</strong> Suiza · NESN.SW</div>
<div><strong style='color:#6C63FF'>.T</strong> Tokyo · 7203.T</div>
<div><strong style='color:#6C63FF'>.HK</strong> HK · 0700.HK</div>
<div><strong style='color:#6C63FF'>.TO</strong> Toronto · RY.TO</div>
<div><strong style='color:#6C63FF'>.AX</strong> Australia · BHP.AX</div>
</div>
    """, unsafe_allow_html=True)

if not analizar:
    st.markdown("""
    <div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:16px;padding:3rem;text-align:center;margin-top:2rem'>
        <div style='font-size:48px;margin-bottom:1rem'>📊</div>
        <div style='font-size:18px;font-weight:600;color:#E6F1FF;margin-bottom:0.5rem'>Introduce un ticker y pulsa Analizar</div>
        <div style='font-size:13px;color:#8892B0;margin-bottom:1.5rem'>Cobertura de mas de 50 bolsas mundiales · Datos en tiempo real via Yahoo Finance</div>
        <div style='display:flex;justify-content:center;gap:12px;flex-wrap:wrap'>
    """ + "".join([
        "<span style='background:#16213E;border:1px solid #2D3561;border-radius:20px;padding:6px 16px;font-size:12px;color:#CCD6F6'>" + t + "</span>"
        for t in ["AAPL", "MSFT", "NVDA", "ITX.MC", "SAN.MC", "VSURE.ST", "ASML.AS", "MC.PA", "NESN.SW", "7203.T"]
    ]) + """
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

with st.spinner("Cargando datos de mercado..."):
    ticker = yf.Ticker(ticker_input)
    info = ticker.info
    hist = ticker.history(period="1y")
    cashflow = ticker.cashflow

if not info or "currentPrice" not in info:
    st.error("No se encontraron datos para **" + ticker_input + "**. Verifica el ticker o prueba con el sufijo del mercado.")
    st.stop()

precio        = info.get("currentPrice", 0)
nombre        = info.get("longName", ticker_input)
sector        = info.get("sector", "")
pais          = info.get("country", "")
cambio_pct    = info.get("regularMarketChangePercent", 0)
per           = info.get("trailingPE")
per_fwd       = info.get("forwardPE")
pb            = info.get("priceToBook")
ps            = info.get("priceToSalesTrailing12Months")
roe           = info.get("returnOnEquity")
roa           = info.get("returnOnAssets")
margen        = info.get("profitMargins")
margen_bruto  = info.get("grossMargins")
deuda_cap     = info.get("debtToEquity")
beta          = info.get("beta")
cap           = info.get("marketCap")
w52h          = info.get("fiftyTwoWeekHigh")
w52l          = info.get("fiftyTwoWeekLow")
eps           = info.get("trailingEps")
eps_fwd       = info.get("forwardEps")
fcf           = info.get("freeCashflow")
target        = info.get("targetMedianPrice")
rec_analistas = info.get("recommendationKey", "")
num_analistas = info.get("numberOfAnalystOpinions", 0)
crec_ing      = info.get("revenueGrowth")
crec_ben      = info.get("earningsGrowth")
media50       = info.get("fiftyDayAverage")
media200      = info.get("twoHundredDayAverage")
moneda        = info.get("currency", "USD")

if eps and eps > 0 and per_fwd and per:
    g = max(0.03, min(0.25, (per - per_fwd) / per * 0.5 + 0.05))
else:
    g = 0.07
intrinseco = eps * (8.5 + 2 * g * 100) if eps and eps > 0 else None
diff_pct = ((precio - intrinseco) / intrinseco * 100) if intrinseco else None

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
        if deuda_cap < 50: pts += 10
        elif deuda_cap < 150: pts += 5
        elif deuda_cap < 300: pts += 1
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
    rec = "COMPRAR"
    color_final = "#4ADE80"
    bg_final = "rgba(74,222,128,0.1)"
    border_final = "#4ADE80"
elif total >= 40:
    rec = "MANTENER"
    color_final = "#FBBF24"
    bg_final = "rgba(251,191,36,0.1)"
    border_final = "#FBBF24"
else:
    rec = "VENDER"
    color_final = "#F87171"
    bg_final = "rgba(248,113,113,0.1)"
    border_final = "#F87171"

alertas = []

if intrinseco and diff_pct is not None:
    if diff_pct < -30:
        alertas.append({
            "tipo": "OPORTUNIDAD FUERTE", "color": "#4ADE80", "bg": "rgba(74,222,128,0.08)",
            "icono": "🟢",
            "titulo": "Precio " + str(round(abs(diff_pct))) + "% por debajo del valor fundamental",
            "que_hacer": "Considera comprar. El precio ofrece un margen de seguridad significativo respecto al valor real del negocio.",
            "por_que": "Valor intrinseco estimado: " + moneda + " " + str(round(intrinseco, 2)) + " — Precio actual: " + moneda + " " + str(round(precio, 2)) + ". El mercado infravalora la empresa respecto a sus numeros reales."
        })
    elif diff_pct < -15:
        alertas.append({
            "tipo": "POSIBLE OPORTUNIDAD", "color": "#34D399", "bg": "rgba(52,211,153,0.08)",
            "icono": "🟡",
            "titulo": "Precio " + str(round(abs(diff_pct))) + "% por debajo del valor fundamental",
            "que_hacer": "Hay margen de seguridad. Considera una posicion parcial y espera confirmacion de tendencia.",
            "por_que": "El valor intrinseco (" + moneda + " " + str(round(intrinseco, 2)) + ") supera al precio actual (" + moneda + " " + str(round(precio, 2)) + "). Descuento real pero moderado."
        })
    elif diff_pct > 30:
        alertas.append({
            "tipo": "PRECIO MUY ELEVADO", "color": "#F87171", "bg": "rgba(248,113,113,0.08)",
            "icono": "🔴",
            "titulo": "Precio " + str(round(diff_pct)) + "% por encima del valor fundamental",
            "que_hacer": "Si tienes la accion considera reducir posicion. Si no la tienes, evita entrar ahora.",
            "por_que": "El mercado paga " + moneda + " " + str(round(precio, 2)) + " por algo valorado fundamentalmente en " + moneda + " " + str(round(intrinseco, 2)) + ". La diferencia es euforia o narrativa de mercado."
        })
    elif diff_pct > 15:
        alertas.append({
            "tipo": "PRECIO ELEVADO", "color": "#FBBF24", "bg": "rgba(251,191,36,0.08)",
            "icono": "🟠",
            "titulo": "Precio " + str(round(diff_pct)) + "% por encima del valor fundamental",
            "que_hacer": "No es el mejor momento de entrada. Si ya tienes posicion, vigila de cerca con un stop-loss.",
            "por_que": "Prima del " + str(round(diff_pct)) + "% sobre el valor intrinseco (" + moneda + " " + str(round(intrinseco, 2)) + "). El mercado descuenta crecimiento optimista."
        })

if crec_ben and crec_ben > 0.10 and cambio_pct < -2:
    alertas.append({
        "tipo": "SENAL CLASICA DE VALOR", "color": "#4ADE80", "bg": "rgba(74,222,128,0.08)",
        "icono": "🟢",
        "titulo": "Beneficios creciendo pero precio cayendo hoy",
        "que_hacer": "Situacion que buscan los inversores de valor. El mercado reacciona con miedo mientras el negocio mejora.",
        "por_que": "Crecimiento de beneficios: +" + str(round(crec_ben*100, 1)) + "% · Caida de precio hoy: " + str(round(cambio_pct, 1)) + "%. Posible sobrerreaccion del mercado (Mr. Market siendo irracional)."
    })

if w52h and precio > w52h * 0.95:
    alertas.append({
        "tipo": "PRECIO EN MAXIMOS ANUALES", "color": "#F87171", "bg": "rgba(248,113,113,0.08)",
        "icono": "🔴",
        "titulo": "Precio cerca del maximo de 52 semanas",
        "que_hacer": "Prudencia. No es momento de entrada salvo que el fundamental justifique claramente el precio.",
        "por_que": "A " + moneda + " " + str(round(precio, 2)) + " el precio esta a solo un " + str(round((w52h-precio)/w52h*100, 1)) + "% del maximo anual (" + moneda + " " + str(round(w52h, 2)) + "). Poco margen de seguridad."
    })

if w52l and precio < w52l * 1.10 and s2 >= 14:
    alertas.append({
        "tipo": "MINIMOS CON NEGOCIO SOLIDO", "color": "#4ADE80", "bg": "rgba(74,222,128,0.08)",
        "icono": "🟢",
        "titulo": "Precio en minimos anuales pero el negocio es de calidad alta",
        "que_hacer": "Interesante para acumular gradualmente. El mercado castiga el precio pero los fundamentos son buenos.",
        "por_que": "Precio actual (" + moneda + " " + str(round(precio, 2)) + ") cerca del minimo de 52s (" + moneda + " " + str(round(w52l, 2)) + ") con calidad de negocio de " + str(s2) + "/20."
    })

if deuda_cap and deuda_cap > 300:
    alertas.append({
        "tipo": "RIESGO FINANCIERO ELEVADO", "color": "#F87171", "bg": "rgba(248,113,113,0.08)",
        "icono": "🔴",
        "titulo": "Nivel de deuda muy por encima de la media",
        "que_hacer": "Incorpora este riesgo en tu decision. La deuda alta es un multiplicador de riesgos en entornos de tipos altos.",
        "por_que": "Deuda/Capital: " + str(round(deuda_cap)) + "%. El umbral de preocupacion esta en 200%. Una empresa endeudada tiene menos margen de maniobra ante adversidades."
    })

if media50 and media200:
    if media50 > media200 * 1.02:
        alertas.append({
            "tipo": "GOLDEN CROSS — TENDENCIA ALCISTA", "color": "#34D399", "bg": "rgba(52,211,153,0.08)",
            "icono": "🟡",
            "titulo": "Media 50d supera a media 200d",
            "que_hacer": "Senal tecnica positiva. El momentum de medio plazo es favorable.",
            "por_que": "Media 50d (" + moneda + " " + str(round(media50, 2)) + ") > Media 200d (" + moneda + " " + str(round(media200, 2)) + "). Cuando la media corta supera a la larga es senal de tendencia alcista consolidada."
        })
    elif media50 < media200 * 0.98:
        alertas.append({
            "tipo": "DEATH CROSS — TENDENCIA BAJISTA", "color": "#FBBF24", "bg": "rgba(251,191,36,0.08)",
            "icono": "🟠",
            "titulo": "Media 50d por debajo de media 200d",
            "que_hacer": "Senal tecnica negativa. Si no tienes posicion, espera confirmacion de giro antes de entrar.",
            "por_que": "Media 50d (" + moneda + " " + str(round(media50, 2)) + ") < Media 200d (" + moneda + " " + str(round(media200, 2)) + "). Indica tendencia bajista de fondo."
        })

if rec_analistas in ["buy", "strongbuy"] and cambio_pct < -3:
    txt_target = moneda + " " + str(round(target, 2)) if target else "N/D"
    alertas.append({
        "tipo": "CAIDA CON CONSENSO COMPRADOR", "color": "#4ADE80", "bg": "rgba(74,222,128,0.08)",
        "icono": "🟢",
        "titulo": "Caida del " + str(round(abs(cambio_pct), 1)) + "% con " + str(num_analistas) + " analistas recomendando compra",
        "que_hacer": "La caida puede ser una oportunidad. Investiga el motivo antes de actuar.",
        "por_que": "Consenso de analistas: comprar. Precio objetivo: " + txt_target + ". Una caida puntual en un valor con buen consenso puede ser una entrada interesante."
    })

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

color_cambio = "#4ADE80" if cambio_pct >= 0 else "#F87171"
signo = "+" if cambio_pct >= 0 else ""
cambio_arrow = "▲" if cambio_pct >= 0 else "▼"

st.markdown(
    "<div class='main-header'>"
    "<div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem'>"
    "<div>"
    "<div style='font-size:24px;font-weight:700;color:#E6F1FF;margin-bottom:4px'>" + nombre + "</div>"
    "<div style='display:flex;gap:8px;align-items:center;flex-wrap:wrap'>"
    "<span style='background:#16213E;border:1px solid #2D3561;border-radius:20px;padding:3px 12px;font-size:12px;color:#8892B0'>" + ticker_input + "</span>"
    + ("<span style='background:#16213E;border:1px solid #2D3561;border-radius:20px;padding:3px 12px;font-size:12px;color:#8892B0'>" + sector + "</span>" if sector else "") +
    ("<span style='background:#16213E;border:1px solid #2D3561;border-radius:20px;padding:3px 12px;font-size:12px;color:#8892B0'>" + pais + "</span>" if pais else "") +
    "</div>"
    "</div>"
    "<div style='text-align:right'>"
    "<div style='font-size:36px;font-weight:700;color:#E6F1FF'>" + moneda + " " + str(round(precio, 2)) + "</div>"
    "<div style='font-size:16px;font-weight:500;color:" + color_cambio + "'>" + cambio_arrow + " " + signo + str(round(cambio_pct, 2)) + "% hoy</div>"
    "</div>"
    "</div>"
    "</div>", unsafe_allow_html=True)

if alertas:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#8892B0;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.75rem'>⚡ " + str(len(alertas)) + " Alerta" + ("s" if len(alertas) > 1 else "") + " detectada" + ("s" if len(alertas) > 1 else "") + "</div>", unsafe_allow_html=True)
    for a in alertas:
        st.markdown(
            "<div style='background:" + a["bg"] + ";border-left:3px solid " + a["color"] + ";border-radius:0 12px 12px 0;padding:1rem 1.5rem;margin-bottom:0.5rem'>"
            "<div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:0.5rem'>"
            "<div style='flex:1'>"
            "<div style='font-size:10px;font-weight:700;color:" + a["color"] + ";letter-spacing:1.5px;margin-bottom:6px'>" + a["icono"] + "  " + a["tipo"] + "</div>"
            "<div style='font-size:15px;font-weight:600;color:#E6F1FF;margin-bottom:8px'>" + a["titulo"] + "</div>"
            "<div style='font-size:13px;color:#CCD6F6;margin-bottom:4px'><span style='color:" + a["color"] + ";font-weight:600'>QUE HACER:</span>  " + a["que_hacer"] + "</div>"
            "<div style='font-size:12px;color:#8892B0'><span style='font-weight:600'>POR QUE:</span>  " + a["por_que"] + "</div>"
            "</div>"
            "</div>"
            "</div>", unsafe_allow_html=True)
else:
    st.markdown(
        "<div style='background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.3);border-radius:12px;padding:1rem 1.5rem;color:#8892B0;font-size:13px'>"
        "✓  Sin alertas destacadas. La accion se encuentra en zona de valoracion neutra."
        "</div>", unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊  Resumen", "🔬  Valor fundamental", "📈  Valor de mercado", "🎯  Puntuacion"])

with tab1:
    metrics = [
        ("Precio actual", moneda + " " + str(round(precio, 2)), ""),
        ("Valor intrinseco est.", moneda + " " + str(round(intrinseco, 2)) if intrinseco else "N/D", "Formula Graham adaptada"),
        ("Diferencia", (("+" if diff_pct >= 0 else "") + str(round(diff_pct, 1)) + "%") if diff_pct is not None else "N/D", "Precio vs fundamental"),
        ("PER", str(round(per, 1)) + "x" if per else "N/D", "< 15 barato  >30 caro"),
        ("Cap. bursatil", moneda + " " + str(round(cap/1e9, 1)) + "B" if cap else "N/D", ""),
        ("Free Cash Flow", moneda + " " + str(round(fcf/1e9, 1)) + "B" if fcf else "N/D", "Dinero real generado"),
    ]
    cols = st.columns(6)
    for i, (label, value, sub) in enumerate(metrics):
        with cols[i]:
            st.markdown(
                "<div class='metric-card'>"
                "<div class='label'>" + label + "</div>"
                "<div class='value'>" + value + "</div>"
                + ("<div class='sub'>" + sub + "</div>" if sub else "") +
                "</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div style='font-size:14px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Evolucion del precio — 12 meses</div>", unsafe_allow_html=True)
        if not hist.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hist.index, y=hist["Close"],
                line=dict(color="#6C63FF", width=2),
                fill="tozeroy", fillcolor="rgba(108,99,255,0.06)",
                name="Precio", hovertemplate=moneda + " %{y:.2f}<extra></extra>"
            ))
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
            fig.update_layout(
                height=360, margin=dict(l=0, r=60, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, color="#8892B0", showline=False),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#8892B0", title=moneda),
                hovermode="x unified", showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div style='font-size:14px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Analistas</div>", unsafe_allow_html=True)
        rec_map = {"strongbuy": "Compra fuerte", "buy": "Comprar", "hold": "Mantener",
                   "sell": "Vender", "strongsell": "Venta fuerte"}
        rec_texto = rec_map.get(rec_analistas, "N/D")
        color_rec = {"Compra fuerte": "#4ADE80", "Comprar": "#34D399", "Mantener": "#FBBF24",
                     "Vender": "#F87171", "Venta fuerte": "#EF4444"}.get(rec_texto, "#8892B0")
        potencial_txt = (("+" if target >= precio else "") + str(round((target-precio)/precio*100, 1)) + "%") if target else "N/D"
        st.markdown(
            "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:12px;padding:1.5rem;text-align:center;height:100%'>"
            "<div style='font-size:22px;font-weight:700;color:" + color_rec + ";margin-bottom:8px'>" + rec_texto + "</div>"
            "<div style='font-size:11px;color:#8892B0;margin-bottom:12px'>" + str(num_analistas) + " analistas</div>"
            "<div style='border-top:1px solid #2D3561;padding-top:12px'>"
            "<div style='font-size:11px;color:#8892B0;margin-bottom:4px'>PRECIO OBJETIVO</div>"
            "<div style='font-size:18px;font-weight:600;color:#E6F1FF'>" + (moneda + " " + str(round(target, 2)) if target else "N/D") + "</div>"
            "<div style='font-size:13px;color:" + color_rec + ";margin-top:4px'>Potencial: " + potencial_txt + "</div>"
            "</div>"
            "</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:14px;font-weight:600;color:#CCD6F6;margin-bottom:0.5rem'>Comparativa de precios clave</div>", unsafe_allow_html=True)
    labels = ["Min 52s", "Precio actual", "Intrinseco", "Obj. analistas", "Max 52s"]
    values = [w52l, precio, intrinseco, target, w52h]
    colors_bar = ["#475569", "#6C63FF", "#4ADE80", "#FBBF24", "#F87171"]
    fig2 = go.Figure(go.Bar(
        x=labels, y=values, marker_color=colors_bar,
        text=[str(round(v, 1)) if v else "N/D" for v in values],
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
    st.markdown("<div style='background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.2);border-radius:10px;padding:0.75rem 1rem;font-size:13px;color:#8892B0;margin-bottom:1rem'>El valor fundamental mide la salud REAL del negocio. Estos numeros cambian trimestralmente, no cada dia.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.75rem'>Valoracion</div>", unsafe_allow_html=True)
        senal_color = {"Barato": "#4ADE80", "Normal": "#FBBF24", "Caro": "#F87171", "—": "#475569"}
        df_val = pd.DataFrame({
            "Metrica": ["PER trailing", "PER forward", "P / Book", "P / Ventas", "PEG Ratio"],
            "Valor": [
                str(round(per, 2)) + "x" if per else "N/D",
                str(round(per_fwd, 2)) + "x" if per_fwd else "N/D",
                str(round(pb, 2)) + "x" if pb else "N/D",
                str(round(ps, 2)) + "x" if ps else "N/D",
                str(round(info.get("pegRatio"), 2)) if info.get("pegRatio") else "N/D",
            ],
            "Referencia": ["< 15 barato · > 30 caro", "< 15 barato · > 30 caro", "< 1.5 barato · > 6 caro", "Depende del sector", "< 1 ideal"],
            "Senal": [
                "Barato" if per and per < 15 else ("Caro" if per and per > 30 else "Normal") if per else "—",
                "Barato" if per_fwd and per_fwd < 15 else ("Caro" if per_fwd and per_fwd > 30 else "Normal") if per_fwd else "—",
                "Barato" if pb and pb < 1.5 else ("Caro" if pb and pb > 6 else "Normal") if pb else "—",
                "—", "—"
            ]
        })
        st.dataframe(df_val, hide_index=True, use_container_width=True)

        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin:1rem 0 0.75rem'>Rentabilidad</div>", unsafe_allow_html=True)
        df_rent = pd.DataFrame({
            "Metrica": ["ROE", "ROA", "Margen neto", "Margen bruto", "Margen EBITDA"],
            "Valor": [
                str(round(roe*100, 1)) + "%" if roe else "N/D",
                str(round(roa*100, 1)) + "%" if roa else "N/D",
                str(round(margen*100, 1)) + "%" if margen else "N/D",
                str(round(margen_bruto*100, 1)) + "%" if margen_bruto else "N/D",
                str(round(info.get("ebitdaMargins", 0)*100, 1)) + "%" if info.get("ebitdaMargins") else "N/D",
            ],
            "Referencia": ["> 15% bueno", "> 10% bueno", "> 15% bueno", "> 30% solido", "> 20% saludable"],
            "Senal": [
                "Bueno" if roe and roe > 0.15 else ("Bajo" if roe and roe < 0.05 else "Normal") if roe else "—",
                "Bueno" if roa and roa > 0.10 else ("Bajo" if roa and roa < 0.03 else "Normal") if roa else "—",
                "Bueno" if margen and margen > 0.15 else ("Bajo" if margen and margen < 0.05 else "Normal") if margen else "—",
                "—", "—"
            ]
        })
        st.dataframe(df_rent, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.75rem'>Salud financiera</div>", unsafe_allow_html=True)
        df_fin = pd.DataFrame({
            "Metrica": ["Deuda / Capital", "Quick Ratio", "Current Ratio", "Deuda total", "Efectivo"],
            "Valor": [
                str(round(deuda_cap, 1)) + "%" if deuda_cap else "N/D",
                str(round(info.get("quickRatio"), 2)) if info.get("quickRatio") else "N/D",
                str(round(info.get("currentRatio"), 2)) if info.get("currentRatio") else "N/D",
                moneda + " " + str(round(info.get("totalDebt", 0)/1e9, 1)) + "B" if info.get("totalDebt") else "N/D",
                moneda + " " + str(round(info.get("totalCash", 0)/1e9, 1)) + "B" if info.get("totalCash") else "N/D",
            ],
            "Referencia": ["< 100% bajo · > 300% alto", "> 1 correcto", "> 1.5 comodo", "Ver vs efectivo", "Ver vs deuda"],
            "Senal": [
                "Baja" if deuda_cap and deuda_cap < 100 else ("Alta" if deuda_cap and deuda_cap > 300 else "Media") if deuda_cap else "—",
                "OK" if info.get("quickRatio") and info.get("quickRatio") > 1 else ("Bajo" if info.get("quickRatio") else "—"),
                "OK" if info.get("currentRatio") and info.get("currentRatio") > 1.5 else ("Bajo" if info.get("currentRatio") else "—"),
                "—", "—"
            ]
        })
        st.dataframe(df_fin, hide_index=True, use_container_width=True)

        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin:1rem 0 0.75rem'>Crecimiento</div>", unsafe_allow_html=True)
        df_crec = pd.DataFrame({
            "Metrica": ["Crec. ingresos YoY", "Crec. beneficios YoY", "EPS actual", "EPS estimado proximo ano"],
            "Valor": [
                str(round(crec_ing*100, 1)) + "%" if crec_ing else "N/D",
                str(round(crec_ben*100, 1)) + "%" if crec_ben else "N/D",
                moneda + " " + str(round(eps, 2)) if eps else "N/D",
                moneda + " " + str(round(eps_fwd, 2)) if eps_fwd else "N/D",
            ],
            "Senal": [
                "Fuerte" if crec_ing and crec_ing > 0.15 else ("Negativo" if crec_ing and crec_ing < 0 else "Moderado") if crec_ing else "—",
                "Fuerte" if crec_ben and crec_ben > 0.15 else ("Negativo" if crec_ben and crec_ben < 0 else "Moderado") if crec_ben else "—",
                "—",
                "Mejora" if eps and eps_fwd and eps_fwd > eps else ("Empeora" if eps and eps_fwd and eps_fwd < eps else "—")
            ]
        })
        st.dataframe(df_crec, hide_index=True, use_container_width=True)

    st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin:1.5rem 0 0.75rem'>Flujo de caja historico</div>", unsafe_allow_html=True)
    if cashflow is not None and not cashflow.empty:
        try:
            fcf_hist = cashflow.loc["Free Cash Flow"] if "Free Cash Flow" in cashflow.index else None
            op_hist = cashflow.loc["Operating Cash Flow"] if "Operating Cash Flow" in cashflow.index else None
            if fcf_hist is not None:
                fig3 = go.Figure()
                anos = [str(d.year) for d in fcf_hist.index]
                fig3.add_trace(go.Bar(x=anos, y=fcf_hist.values/1e9, name="Free Cash Flow",
                                      marker_color="#6C63FF", opacity=0.9))
                if op_hist is not None:
                    fig3.add_trace(go.Bar(x=anos, y=op_hist.values/1e9, name="Cash Flow Operativo",
                                         marker_color="#34D399", opacity=0.7))
                fig3.update_layout(
                    height=280, barmode="group", margin=dict(l=0, r=0, t=10, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(showgrid=False, color="#8892B0"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", color="#8892B0", title="Miles de millones"),
                    legend=dict(font=dict(color="#8892B0"), bgcolor="rgba(0,0,0,0)"),
                    hovermode="x unified"
                )
                st.plotly_chart(fig3, use_container_width=True)
        except Exception:
            st.info("Datos de flujo de caja no disponibles para este ticker.")

with tab3:
    st.markdown("<div style='background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.2);border-radius:10px;padding:0.75rem 1rem;font-size:13px;color:#8892B0;margin-bottom:1rem'>El valor de mercado cambia cada segundo. Esta influido por emociones, noticias y rumores — no siempre por los numeros reales.</div>", unsafe_allow_html=True)

    metrics_mkt = [
        ("Precio actual", moneda + " " + str(round(precio, 2)), (("+" if cambio_pct >= 0 else "") + str(round(cambio_pct, 2)) + "% hoy"), "#4ADE80" if cambio_pct >= 0 else "#F87171"),
        ("Max 52 semanas", moneda + " " + str(round(w52h, 2)) if w52h else "N/D", (str(round((precio-w52h)/w52h*100, 1)) + "% desde max") if w52h else "", "#F87171"),
        ("Min 52 semanas", moneda + " " + str(round(w52l, 2)) if w52l else "N/D", ("+" + str(round((precio-w52l)/w52l*100, 1)) + "% desde min") if w52l else "", "#4ADE80"),
        ("Beta", str(round(beta, 2)) if beta else "N/D", "Menos volatil" if beta and beta < 1 else "Mas volatil", "#FBBF24" if beta and beta > 1.3 else "#4ADE80"),
        ("Media 50d", moneda + " " + str(round(media50, 2)) if media50 else "N/D", (str(round((precio-media50)/media50*100, 1)) + "% vs precio") if media50 else "", "#4ADE80" if media50 and precio > media50 else "#F87171"),
        ("Media 200d", moneda + " " + str(round(media200, 2)) if media200 else "N/D", (str(round((precio-media200)/media200*100, 1)) + "% vs precio") if media200 else "", "#4ADE80" if media200 and precio > media200 else "#F87171"),
    ]
    cols = st.columns(6)
    for i, (label, value, sub, color_sub) in enumerate(metrics_mkt):
        with cols[i]:
            st.markdown(
                "<div class='metric-card'>"
                "<div class='label'>" + label + "</div>"
                "<div class='value'>" + value + "</div>"
                + ("<div style='font-size:11px;color:" + color_sub + ";margin-top:4px'>" + sub + "</div>" if sub else "") +
                "</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.75rem'>Volumen de negociacion</div>", unsafe_allow_html=True)
        vol_hoy = info.get("volume", 0)
        vol_10d = info.get("averageVolume10days", 0)
        vol_3m = info.get("averageVolume", 0)
        vol_ratio = round(vol_hoy / vol_3m, 2) if vol_3m else 0
        vol_color = "#4ADE80" if vol_ratio > 1.5 else "#FBBF24" if vol_ratio > 0.8 else "#F87171"
        st.markdown(
            "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:12px;padding:1.25rem'>"
            "<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;text-align:center'>"
            "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>HOY</div><div style='font-size:18px;font-weight:600;color:#E6F1FF'>" + str(round(vol_hoy/1e6, 1)) + "M</div></div>"
            "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>MEDIA 10D</div><div style='font-size:18px;font-weight:600;color:#E6F1FF'>" + str(round(vol_10d/1e6, 1)) + "M</div></div>"
            "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>MEDIA 3M</div><div style='font-size:18px;font-weight:600;color:#E6F1FF'>" + str(round(vol_3m/1e6, 1)) + "M</div></div>"
            "</div>"
            "<div style='margin-top:1rem;padding-top:1rem;border-top:1px solid #2D3561;font-size:12px;color:#8892B0'>"
            "Ratio volumen hoy vs media 3m: <span style='color:" + vol_color + ";font-weight:600'>" + str(vol_ratio) + "x</span>"
            + (" — Volumen inusualmente alto, atencion" if vol_ratio > 2 else " — Volumen normal" if vol_ratio > 0.8 else " — Volumen bajo") +
            "</div>"
            "</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:0.75rem'>Posicionamiento institucional</div>", unsafe_allow_html=True)
        inst = info.get("heldPercentInstitutions", 0) * 100
        cortos = info.get("shortPercentOfFloat", 0) * 100
        ratio_cortos = info.get("shortRatio", 0)
        st.markdown(
            "<div style='background:#1A1D2E;border:1px solid #2D3561;border-radius:12px;padding:1.25rem'>"
            "<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;text-align:center'>"
            "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>INSTITUCIONAL</div><div style='font-size:18px;font-weight:600;color:" + ("#4ADE80" if inst > 60 else "#FBBF24") + "'>" + str(round(inst, 1)) + "%</div></div>"
            "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>POSICIONES CORTAS</div><div style='font-size:18px;font-weight:600;color:" + ("#F87171" if cortos > 10 else "#4ADE80") + "'>" + str(round(cortos, 2)) + "%</div></div>"
            "<div><div style='font-size:11px;color:#8892B0;margin-bottom:4px'>RATIO CORTOS</div><div style='font-size:18px;font-weight:600;color:#E6F1FF'>" + (str(round(ratio_cortos, 1)) if ratio_cortos else "N/D") + "</div></div>"
            "</div>"
            "<div style='margin-top:1rem;padding-top:1rem;border-top:1px solid #2D3561;font-size:12px;color:#8892B0'>"
            + ("Institucional alto: los grandes fondos confian en la empresa. " if inst > 60 else "") +
            ("Posiciones cortas elevadas: atencion, muchos profesionales apuestan a la baja." if cortos > 10 else "Posiciones cortas en nivel normal.")
            + "</div>"
            "</div>", unsafe_allow_html=True)

    alertas_mkt = [a for a in alertas if any(x in a["tipo"] for x in ["MAXIMOS", "MINIMOS", "CROSS", "CAIDA", "SENAL CLASICA"])]
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
            "<span style='color:#4ADE80'>●</span>  65 – 100 &nbsp; Comprar<br>"
            "<span style='color:#FBBF24'>●</span>  40 – 64 &nbsp; Mantener<br>"
            "<span style='color:#F87171'>●</span>  0 – 39 &nbsp;&nbsp; Vender"
            "</div>"
            "</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='font-size:13px;font-weight:600;color:#CCD6F6;margin-bottom:1rem'>Desglose por criterio</div>", unsafe_allow_html=True)
        criterios = [
            ("Valoracion relativa", "PER y P/Book vs referencias de mercado", s1,
             "PER: " + str(round(per, 1)) + "x · P/B: " + str(round(pb, 1)) + "x" if per and pb else "Datos insuficientes"),
            ("Calidad del negocio", "ROE y margen neto como indicadores de eficiencia", s2,
             "ROE: " + str(round(roe*100, 1)) + "% · Margen: " + str(round(margen*100, 1)) + "%" if roe and margen else "Datos insuficientes"),
            ("Salud financiera", "Nivel de deuda y capacidad de pago", s3,
             "Deuda/Capital: " + str(round(deuda_cap, 1)) + "%" if deuda_cap else "Datos insuficientes"),
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
                "<div>"
                "<div style='font-size:13px;font-weight:600;color:#E6F1FF'>" + nombre_c + "</div>"
                "<div style='font-size:11px;color:#8892B0'>" + descripcion + "</div>"
                "</div>"
                "<div style='font-size:20px;font-weight:700;color:" + color_barra + ";min-width:50px;text-align:right'>" + str(pts) + "<span style='font-size:12px;color:#8892B0'>/20</span></div>"
                "</div>"
                "<div style='background:#0F1117;border-radius:4px;height:6px;margin:8px 0'>"
                "<div style='background:" + color_barra + ";width:" + str(pct) + "%;height:6px;border-radius:4px;transition:width 0.5s'></div>"
                "</div>"
                "<div style='font-size:11px;color:#475569'>" + detalle + "</div>"
                "</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:#475569;text-align:center'>StockAnalyzer Pro · Datos via Yahoo Finance · Solo fines educativos · No constituye asesoramiento financiero</div>", unsafe_allow_html=True)
