import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="StockAnalyzer Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background-color: #060a0f;
    color: #CCD6F6;
}
.block-container { padding: 0.5rem 1rem !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

.terminal-header {
    background: #060a0f;
    border-bottom: 1px solid #1a2332;
    padding: 0.4rem 0;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
}
.panel {
    background: #0a0f18;
    border: 1px solid #1a2332;
    border-radius: 4px;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    height: 100%;
}
.panel-title {
    font-size: 10px;
    color: #4a6080;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1a2332;
}
.watchlist-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 8px;
    border-radius: 3px;
    cursor: pointer;
    margin-bottom: 2px;
    border: 1px solid transparent;
    transition: all 0.1s;
}
.watchlist-row:hover { background: #111827; border-color: #2D3561; }
.watchlist-row.active { background: #0d1929; border-color: #3B82F6; }
.ticker-sym { font-size: 13px; font-weight: 600; color: #E6F1FF; letter-spacing: 1px; }
.ticker-name { font-size: 10px; color: #4a6080; margin-top: 1px; }
.ticker-price { font-size: 13px; font-weight: 600; text-align: right; }
.ticker-chg { font-size: 10px; text-align: right; margin-top: 1px; }
.signal-badge {
    font-size: 9px;
    padding: 2px 6px;
    border-radius: 2px;
    font-weight: 700;
    letter-spacing: 1px;
}
.sig-buy { background: rgba(74,222,128,0.15); color: #4ADE80; border: 1px solid rgba(74,222,128,0.3); }
.sig-sell { background: rgba(248,113,113,0.15); color: #F87171; border: 1px solid rgba(248,113,113,0.3); }
.sig-hold { background: rgba(251,191,36,0.15); color: #FBBF24; border: 1px solid rgba(251,191,36,0.3); }

.price-main { font-size: 42px; font-weight: 700; color: #E6F1FF; line-height: 1; letter-spacing: -1px; }
.price-chg-pos { color: #4ADE80; font-size: 16px; }
.price-chg-neg { color: #F87171; font-size: 16px; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.4rem; margin-bottom: 0.5rem; }
.kpi-box {
    background: #060a0f;
    border: 1px solid #1a2332;
    border-radius: 3px;
    padding: 0.5rem 0.75rem;
}
.kpi-label { font-size: 9px; color: #4a6080; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 3px; }
.kpi-value { font-size: 16px; font-weight: 600; color: #E6F1FF; }
.kpi-sub { font-size: 9px; color: #4a6080; margin-top: 2px; }

.alert-row {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.5rem 0.75rem;
    border-radius: 3px;
    margin-bottom: 0.4rem;
    border-left: 3px solid;
}
.alert-type { font-size: 9px; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 3px; }
.alert-title { font-size: 12px; font-weight: 500; color: #CCD6F6; }
.alert-body { font-size: 11px; color: #4a6080; margin-top: 2px; }

.score-ring {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    border: 3px solid;
}
.score-num { font-size: 32px; font-weight: 700; line-height: 1; }
.score-label { font-size: 9px; letter-spacing: 1px; margin-top: 2px; }

.criteria-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0;
    border-bottom: 1px solid #0d1929;
    font-size: 11px;
}
.criteria-name { flex: 1; color: #8892B0; }
.criteria-bar-wrap { width: 80px; background: #060a0f; border-radius: 2px; height: 4px; }
.criteria-bar { height: 4px; border-radius: 2px; }
.criteria-pts { width: 35px; text-align: right; font-weight: 600; }

.data-table { width: 100%; font-size: 11px; border-collapse: collapse; }
.data-table tr { border-bottom: 1px solid #0d1929; }
.data-table tr:last-child { border-bottom: none; }
.data-table td { padding: 5px 4px; }
.data-table td:first-child { color: #4a6080; }
.data-table td:last-child { text-align: right; color: #CCD6F6; font-weight: 500; }
.data-table .senal-pos { color: #4ADE80; }
.data-table .senal-neg { color: #F87171; }
.data-table .senal-neu { color: #FBBF24; }

.status-dot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; margin-right: 4px; }
.dot-green { background: #4ADE80; box-shadow: 0 0 6px #4ADE80; }
.dot-red { background: #F87171; }

[data-testid="stButton"] button {
    background: transparent;
    border: 1px solid #1a2332;
    color: #8892B0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 3px;
    width: 100%;
    text-align: left;
}
[data-testid="stButton"] button:hover { border-color: #3B82F6; color: #E6F1FF; background: #0d1929; }
[data-testid="stTextInput"] input {
    background: #0a0f18;
    border: 1px solid #1a2332;
    color: #E6F1FF;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    border-radius: 3px;
}
[data-testid="stTextInput"] input:focus { border-color: #3B82F6; box-shadow: none; }
div[data-testid="stExpander"] { background: #0a0f18; border: 1px solid #1a2332; border-radius: 3px; }
.stDataFrame { font-size: 11px; }
</style>
""", unsafe_allow_html=True)

try:
    POLY_KEY = st.secrets["POLYGON_API_KEY"]
    AV_KEY   = st.secrets["AV_API_KEY"]
except Exception:
    POLY_KEY = "BUzVdky9K3UEg1HXMZLoS7QWisWFlnMy"
    AV_KEY   = "1P9IE94SAPGR4J6M"

POLY_BASE = "https://api.polygon.io"
AV_BASE   = "https://www.alphavantage.co/query"

def poly_get(endpoint, params={}):
    params["apiKey"] = POLY_KEY
    try:
        r = requests.get(POLY_BASE + endpoint, params=params, timeout=15)
        data = r.json()
        if data.get("status") == "ERROR":
            return None
        return data
    except Exception:
        return None

def av_get(params):
    params["apikey"] = AV_KEY
    try:
        r = requests.get(AV_BASE, params=params, timeout=15)
        data = r.json()
        if isinstance(data, dict) and "Error Message" in data:
            return {}
        return data
    except Exception:
        return {}

@st.cache_data(ttl=60)
def get_snapshot(ticker):
    return poly_get("/v2/snapshot/locale/us/markets/stocks/tickers/" + ticker)

@st.cache_data(ttl=3600)
def get_details(ticker):
    return poly_get("/v3/reference/tickers/" + ticker)

@st.cache_data(ttl=3600)
def get_financials(ticker):
    return poly_get("/vX/reference/financials", {"ticker": ticker, "limit": 5, "sort": "filing_date", "order": "desc"})

@st.cache_data(ttl=3600)
def get_history(ticker):
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    return poly_get("/v2/aggs/ticker/" + ticker + "/range/1/week/" + start + "/" + end,
                    {"adjusted": "true", "sort": "asc", "limit": 52})

@st.cache_data(ttl=3600)
def get_av_overview(ticker):
    return av_get({"function": "OVERVIEW", "symbol": ticker})

def sf(val, default=None):
    try:
        v = float(val)
        return v if v != 0 else default
    except Exception:
        return default

def compute_scores(per, pb, roe, margen, deuda_cap, precio, w52h, w52l, target, media50, media200, intrinseco):
    def sc_val(per, pb):
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

    def sc_cal(roe, margen):
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

    def sc_fin(d):
        pts = 10
        if d:
            if d < 50: pts += 10
            elif d < 150: pts += 5
            elif d < 300: pts += 1
            else: pts -= 5
        return max(0, min(20, pts))

    def sc_mom(precio, w52h, w52l, target, media50, media200):
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

    s1 = sc_val(per, pb)
    s2 = sc_cal(roe, margen)
    s3 = sc_fin(deuda_cap)
    s4 = sc_mom(precio, w52h, w52l, target, media50, media200)
    s5 = sc_dcf(precio, intrinseco)
    return s1, s2, s3, s4, s5, s1+s2+s3+s4+s5

DEFAULT_WATCHLIST = ["AAPL", "MSFT", "NVDA", "GOOGL", "TSLA", "META", "AMZN", "JPM", "MSTR", "NFLX"]

if "watchlist" not in st.session_state:
    st.session_state.watchlist = DEFAULT_WATCHLIST.copy()
if "selected" not in st.session_state:
    st.session_state.selected = "AAPL"
if "detail_data" not in st.session_state:
    st.session_state.detail_data = {}

now = datetime.now()
st.markdown(
    "<div class='terminal-header'>"
    "<span style='font-size:15px;font-weight:700;color:#E6F1FF;letter-spacing:2px'>STOCK<span style='color:#3B82F6'>ANALYZER</span></span>"
    "<span style='font-size:9px;color:#4a6080;letter-spacing:1px'>PRO TERMINAL</span>"
    "<span style='margin-left:auto;font-size:10px;color:#4a6080'>" + now.strftime("%a %b %d %Y  %H:%M") + "</span>"
    "<span><span class='status-dot dot-green'></span><span style='font-size:10px;color:#4ADE80'>LIVE</span></span>"
    "</div>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 3])

with left_col:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>Watchlist</div>", unsafe_allow_html=True)

    new_ticker = st.text_input("", placeholder="Añadir ticker...", key="new_ticker", label_visibility="collapsed")
    if new_ticker:
        t = new_ticker.strip().upper()
        if t and t not in st.session_state.watchlist:
            st.session_state.watchlist.append(t)
            st.session_state.selected = t
            st.rerun()

    for ticker in st.session_state.watchlist:
        snap = get_snapshot(ticker)
        if snap and "ticker" in snap:
            s = snap["ticker"]
            p = sf(s.get("lastTrade", {}).get("p")) or sf(s.get("day", {}).get("c"), 0)
            prev = sf(s.get("prevDay", {}).get("c"), p)
            chg = ((p - prev) / prev * 100) if prev else 0
            chg_color = "#4ADE80" if chg >= 0 else "#F87171"
            signo = "+" if chg >= 0 else ""
            is_active = ticker == st.session_state.selected
            active_class = "active" if is_active else ""

            ov_quick = get_av_overview(ticker)
            per_q = sf(ov_quick.get("PERatio")) if ov_quick else None
            pb_q  = sf(ov_quick.get("PriceToBookRatio")) if ov_quick else None
            roe_q = sf(ov_quick.get("ReturnOnEquityTTM")) if ov_quick else None
            mrg_q = sf(ov_quick.get("ProfitMargin")) if ov_quick else None
            dbt_q = sf(ov_quick.get("DebtToEquityRatio")) if ov_quick else None
            eps_q = sf(ov_quick.get("EPS")) if ov_quick else None
            w52h_q = sf(ov_quick.get("52WeekHigh")) if ov_quick else None
            w52l_q = sf(ov_quick.get("52WeekLow")) if ov_quick else None
            tgt_q  = sf(ov_quick.get("AnalystTargetPrice")) if ov_quick else None
            m50_q  = sf(ov_quick.get("50DayMovingAverage")) if ov_quick else None
            m200_q = sf(ov_quick.get("200DayMovingAverage")) if ov_quick else None
            per_fwd_q = sf(ov_quick.get("ForwardPE")) if ov_quick else None
            if eps_q and eps_q > 0:
                g = 0.07
                if per_fwd_q and per_q:
                    g = max(0.03, min(0.25, (per_q - per_fwd_q) / per_q * 0.5 + 0.05))
                intr_q = eps_q * (8.5 + 2 * g * 100)
            else:
                intr_q = None
            _, _, _, _, _, total_q = compute_scores(per_q, pb_q, roe_q, mrg_q, dbt_q, p, w52h_q, w52l_q, tgt_q, m50_q, m200_q, intr_q)
            if total_q >= 65: sig = "BUY"; sig_class = "sig-buy"
            elif total_q >= 40: sig = "HOLD"; sig_class = "sig-hold"
            else: sig = "SELL"; sig_class = "sig-sell"

            st.markdown(
                "<div class='watchlist-row " + active_class + "'>"
                "<div>"
                "<div class='ticker-sym'>" + ticker + "</div>"
                "<div class='ticker-name'>" + (s.get("ticker", ticker)) + "</div>"
                "</div>"
                "<div style='text-align:right'>"
                "<div class='ticker-price' style='color:" + chg_color + "'>$" + str(round(p, 2)) + "</div>"
                "<div class='ticker-chg' style='color:" + chg_color + "'>" + signo + str(round(chg, 2)) + "%</div>"
                "</div>"
                "<div style='margin-left:8px'><span class='signal-badge " + sig_class + "'>" + sig + "</span></div>"
                "</div>", unsafe_allow_html=True)

            if st.button(ticker, key="sel_" + ticker):
                st.session_state.selected = ticker
                st.rerun()
        else:
            st.markdown(
                "<div class='watchlist-row'>"
                "<div><div class='ticker-sym' style='color:#4a6080'>" + ticker + "</div>"
                "<div class='ticker-name'>Sin datos</div></div>"
                "</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    ticker_input = st.session_state.selected

    with st.spinner(""):
        snap     = get_snapshot(ticker_input)
        det_data = get_details(ticker_input)
        fins     = get_financials(ticker_input)
        hist     = get_history(ticker_input)
        ov       = get_av_overview(ticker_input)

    if not snap or "ticker" not in snap:
        st.markdown("<div class='panel'><div style='color:#4a6080;font-size:12px;padding:2rem;text-align:center'>Sin datos para " + ticker_input + "</div></div>", unsafe_allow_html=True)
    else:
        s    = snap["ticker"]
        day  = s.get("day", {})
        prev = s.get("prevDay", {})

        precio      = sf(s.get("lastTrade", {}).get("p")) or sf(day.get("c")) or sf(prev.get("c"), 0)
        precio_prev = sf(prev.get("c"), precio)
        cambio_pct  = ((precio - precio_prev) / precio_prev * 100) if precio_prev else 0
        vol         = sf(day.get("v"))
        avg_vol     = sf(prev.get("v"))
        vwap        = sf(day.get("vw"))

        det  = det_data.get("results", {}) if det_data else {}
        nombre = det.get("name", ticker_input)
        sector = det.get("sic_description", "")
        cap    = sf(det.get("market_cap"))

        per          = sf(ov.get("PERatio")) if ov else None
        per_fwd      = sf(ov.get("ForwardPE")) if ov else None
        pb           = sf(ov.get("PriceToBookRatio")) if ov else None
        ps           = sf(ov.get("PriceToSalesRatioTTM")) if ov else None
        roe          = sf(ov.get("ReturnOnEquityTTM")) if ov else None
        roa          = sf(ov.get("ReturnOnAssetsTTM")) if ov else None
        margen       = sf(ov.get("ProfitMargin")) if ov else None
        margen_bruto = sf(ov.get("GrossProfitTTM")) if ov else None
        deuda_cap    = sf(ov.get("DebtToEquityRatio")) if ov else None
        beta         = sf(ov.get("Beta")) if ov else None
        w52h         = sf(ov.get("52WeekHigh")) if ov else None
        w52l         = sf(ov.get("52WeekLow")) if ov else None
        eps          = sf(ov.get("EPS")) if ov else None
        eps_fwd      = sf(ov.get("ForwardEPS")) if ov else None
        target       = sf(ov.get("AnalystTargetPrice")) if ov else None
        media50      = sf(ov.get("50DayMovingAverage")) if ov else None
        media200     = sf(ov.get("200DayMovingAverage")) if ov else None
        crec_ing     = sf(ov.get("QuarterlyRevenueGrowthYOY")) if ov else None
        crec_ben     = sf(ov.get("QuarterlyEarningsGrowthYOY")) if ov else None

        fins_list = fins.get("results", []) if fins else []
        fcf_hist = []
        for rep in fins_list[:5]:
            try:
                cf  = rep.get("financials", {}).get("cash_flow_statement", {})
                op  = sf(cf.get("net_cash_flow_from_operating_activities", {}).get("value"))
                inv = sf(cf.get("net_cash_flow_from_investing_activities", {}).get("value"), 0)
                if op:
                    fcf_hist.append({"year": str(rep.get("fiscal_year", "")), "fcf": op + inv, "op": op})
            except Exception:
                pass

        hist_dates  = []
        hist_prices = []
        hist_vols   = []
        if hist and "results" in hist:
            for bar in hist["results"]:
                hist_dates.append(datetime.fromtimestamp(bar["t"]/1000).strftime("%Y-%m-%d"))
                hist_prices.append(bar["c"])
                hist_vols.append(bar.get("v", 0))

        if eps and eps > 0 and per_fwd and per:
            g = max(0.03, min(0.25, (per - per_fwd) / per * 0.5 + 0.05))
        else:
            g = 0.07
        intrinseco = eps * (8.5 + 2 * g * 100) if eps and eps > 0 else None
        diff_pct   = ((precio - intrinseco) / intrinseco * 100) if intrinseco else None

        s1, s2, s3, s4, s5, total = compute_scores(per, pb, roe, margen, deuda_cap, precio, w52h, w52l, target, media50, media200, intrinseco)

        if total >= 65: rec = "BUY"; rc = "#4ADE80"; rb = "rgba(74,222,128,0.1)"
        elif total >= 40: rec = "HOLD"; rc = "#FBBF24"; rb = "rgba(251,191,36,0.1)"
        else: rec = "SELL"; rc = "#F87171"; rb = "rgba(248,113,113,0.1)"

        chg_color = "#4ADE80" if cambio_pct >= 0 else "#F87171"
        signo = "+" if cambio_pct >= 0 else ""

        # HEADER DE LA EMPRESA
        header_col1, header_col2, header_col3 = st.columns([2, 1, 1])
        with header_col1:
            st.markdown(
                "<div style='padding:0.5rem 0'>"
                "<div style='font-size:22px;font-weight:700;color:#E6F1FF;letter-spacing:1px'>" + ticker_input + " <span style='font-size:14px;color:#4a6080;font-weight:400'>" + nombre[:40] + "</span></div>"
                "<div style='font-size:10px;color:#4a6080;margin-top:2px'>" + sector[:50] + " · " + ("$" + str(round(cap/1e9, 1)) + "B market cap" if cap else "") + "</div>"
                "<div style='margin-top:8px'>"
                "<span class='price-main'>$" + str(round(precio, 2)) + "</span>"
                "<span style='margin-left:12px;font-size:16px;color:" + chg_color + "'>" + signo + str(round(cambio_pct, 2)) + "%</span>"
                "<span style='margin-left:8px;font-size:11px;color:#4a6080'>" + signo + "$" + str(round(abs(precio - precio_prev), 2)) + "</span>"
                "</div>"
                "</div>", unsafe_allow_html=True)

        with header_col2:
            st.markdown(
                "<div style='padding:0.5rem 0'>"
                "<div style='font-size:9px;color:#4a6080;letter-spacing:1px;margin-bottom:4px'>PUNTUACION</div>"
                "<div style='background:" + rb + ";border:2px solid " + rc + ";border-radius:50%;width:80px;height:80px;display:flex;flex-direction:column;align-items:center;justify-content:center'>"
                "<div style='font-size:28px;font-weight:700;color:" + rc + ";line-height:1'>" + str(total) + "</div>"
                "<div style='font-size:8px;color:" + rc + ";letter-spacing:1px'>" + rec + "</div>"
                "</div>"
                "</div>", unsafe_allow_html=True)

        with header_col3:
            if intrinseco:
                diff_c = "#4ADE80" if diff_pct and diff_pct < 0 else "#F87171"
                st.markdown(
                    "<div style='padding:0.5rem 0'>"
                    "<div style='font-size:9px;color:#4a6080;letter-spacing:1px;margin-bottom:4px'>VALOR INTRINSECO</div>"
                    "<div style='font-size:20px;font-weight:700;color:#4ADE80'>$" + str(round(intrinseco, 2)) + "</div>"
                    "<div style='font-size:11px;color:" + diff_c + ";margin-top:2px'>"
                    + (("+" if diff_pct >= 0 else "") + str(round(diff_pct, 1)) + "% vs precio") +
                    "</div>"
                    "<div style='font-size:9px;color:#4a6080;margin-top:4px'>Graham Formula</div>"
                    "</div>", unsafe_allow_html=True)

        st.markdown("<div style='border-bottom:1px solid #1a2332;margin:0.25rem 0 0.5rem'></div>", unsafe_allow_html=True)

        # KPIs
        kpis = [
            ("PER", str(round(per, 1)) + "x" if per else "N/D", "< 15 barato"),
            ("P/BOOK", str(round(pb, 1)) + "x" if pb else "N/D", "< 1.5 barato"),
            ("ROE", str(round(roe*100, 1)) + "%" if roe else "N/D", "> 15% bueno"),
            ("MARGEN NETO", str(round(margen*100, 1)) + "%" if margen else "N/D", "> 15% bueno"),
            ("DEUDA/CAP", str(round(deuda_cap, 1)) + "%" if deuda_cap else "N/D", "< 100% ok"),
            ("BETA", str(round(beta, 2)) if beta else "N/D", "vs S&P500"),
            ("EPS", "$" + str(round(eps, 2)) if eps else "N/D", "trailing"),
            ("OBJ ANALISTAS", "$" + str(round(target, 2)) if target else "N/D",
             (("+" if target >= precio else "") + str(round((target-precio)/precio*100, 1)) + "%") if target else ""),
        ]
        st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
        for label, value, sub in kpis:
            st.markdown(
                "<div class='kpi-box'>"
                "<div class='kpi-label'>" + label + "</div>"
                "<div class='kpi-value'>" + value + "</div>"
                "<div class='kpi-sub'>" + sub + "</div>"
                "</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # PANELES PRINCIPALES
        main_left, main_right = st.columns([3, 2])

        with main_left:
            # GRAFICO
            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>Price Chart — 52 weeks</div>", unsafe_allow_html=True)
            if hist_prices:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=hist_dates, y=hist_prices,
                    line=dict(color="#3B82F6", width=1.5),
                    fill="tozeroy", fillcolor="rgba(59,130,246,0.05)",
                    name="Price", hovertemplate="$%{y:.2f}<extra></extra>"
                ))
                if intrinseco:
                    fig.add_hline(y=intrinseco, line_dash="dash", line_color="#4ADE80",
                                  line_width=1, annotation_text="IV $" + str(round(intrinseco, 0)),
                                  annotation_font_color="#4ADE80", annotation_font_size=10)
                if target:
                    fig.add_hline(y=target, line_dash="dot", line_color="#FBBF24",
                                  line_width=1, annotation_text="PT $" + str(round(target, 0)),
                                  annotation_font_color="#FBBF24", annotation_font_size=10)
                if media200:
                    fig.add_hline(y=media200, line_dash="dot", line_color="#4a6080",
                                  line_width=1, annotation_text="MA200 $" + str(round(media200, 0)),
                                  annotation_font_color="#4a6080", annotation_font_size=10)
                if media50:
                    fig.add_hline(y=media50, line_dash="dot", line_color="#6B7280",
                                  line_width=1, annotation_text="MA50 $" + str(round(media50, 0)),
                                  annotation_font_color="#6B7280", annotation_font_size=10)
                fig.update_layout(
                    height=280, margin=dict(l=0, r=80, t=10, b=30),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(showgrid=False, color="#4a6080", tickfont=dict(size=9)),
                    yaxis=dict(gridcolor="rgba(26,35,50,0.8)", color="#4a6080",
                               tickfont=dict(size=9), tickprefix="$"),
                    hovermode="x unified", showlegend=False,
                    font=dict(family="JetBrains Mono")
                )
                st.plotly_chart(fig, use_container_width=True)

                # VOLUMEN
                if hist_vols:
                    fig_vol = go.Figure()
                    vol_colors = ["#3B82F6" if i == 0 or hist_prices[i] >= hist_prices[i-1] else "#F87171"
                                  for i in range(len(hist_prices))]
                    fig_vol.add_trace(go.Bar(x=hist_dates, y=[v/1e6 for v in hist_vols],
                                             marker_color=vol_colors, opacity=0.7, name="Vol"))
                    fig_vol.update_layout(
                        height=60, margin=dict(l=0, r=80, t=0, b=0),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        xaxis=dict(showgrid=False, showticklabels=False),
                        yaxis=dict(showgrid=False, color="#4a6080", tickfont=dict(size=8), title="M"),
                        showlegend=False, font=dict(family="JetBrains Mono")
                    )
                    st.plotly_chart(fig_vol, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ALERTAS
            alertas = []
            if intrinseco and diff_pct is not None:
                if diff_pct < -20:
                    alertas.append({"tipo": "OPORTUNIDAD", "color": "#4ADE80", "bg": "rgba(74,222,128,0.05)",
                        "titulo": "Precio " + str(round(abs(diff_pct))) + "% por debajo del valor intrinseco",
                        "body": "Margen de seguridad significativo. Valor intrinseco $" + str(round(intrinseco, 2)) + " vs precio $" + str(round(precio, 2)) + "."})
                elif diff_pct > 25:
                    alertas.append({"tipo": "SOBREVALUADO", "color": "#F87171", "bg": "rgba(248,113,113,0.05)",
                        "titulo": "Precio " + str(round(diff_pct)) + "% por encima del valor intrinseco",
                        "body": "El mercado paga $" + str(round(precio, 2)) + " por algo valorado en $" + str(round(intrinseco, 2)) + "."})
            if w52h and precio > w52h * 0.95:
                alertas.append({"tipo": "MAXIMOS ANUALES", "color": "#F87171", "bg": "rgba(248,113,113,0.05)",
                    "titulo": "Precio a " + str(round((w52h-precio)/w52h*100, 1)) + "% del maximo de 52 semanas",
                    "body": "Poco margen de seguridad. Maximo anual: $" + str(round(w52h, 2)) + "."})
            if w52l and precio < w52l * 1.08 and s2 >= 14:
                alertas.append({"tipo": "MINIMOS + CALIDAD", "color": "#4ADE80", "bg": "rgba(74,222,128,0.05)",
                    "titulo": "Precio en minimos anuales con negocio de calidad alta",
                    "body": "Posible oportunidad de acumulacion. Calidad: " + str(s2) + "/20."})
            if media50 and media200:
                if media50 > media200 * 1.02:
                    alertas.append({"tipo": "GOLDEN CROSS", "color": "#4ADE80", "bg": "rgba(74,222,128,0.05)",
                        "titulo": "MA50 ($" + str(round(media50, 0)) + ") > MA200 ($" + str(round(media200, 0)) + ")",
                        "body": "Senal tecnica alcista de medio plazo confirmada."})
                elif media50 < media200 * 0.98:
                    alertas.append({"tipo": "DEATH CROSS", "color": "#F87171", "bg": "rgba(248,113,113,0.05)",
                        "titulo": "MA50 ($" + str(round(media50, 0)) + ") < MA200 ($" + str(round(media200, 0)) + ")",
                        "body": "Senal tecnica bajista. Espera confirmacion de giro."})
            if deuda_cap and deuda_cap > 300:
                alertas.append({"tipo": "RIESGO DEUDA", "color": "#FBBF24", "bg": "rgba(251,191,36,0.05)",
                    "titulo": "Deuda/Capital elevado: " + str(round(deuda_cap, 0)) + "%",
                    "body": "Nivel de apalancamiento por encima del umbral de riesgo (200%)."})

            if alertas:
                st.markdown("<div class='panel'>", unsafe_allow_html=True)
                st.markdown("<div class='panel-title'>Signals & Alerts</div>", unsafe_allow_html=True)
                for a in alertas:
                    st.markdown(
                        "<div class='alert-row' style='background:" + a["bg"] + ";border-left-color:" + a["color"] + "'>"
                        "<div>"
                        "<div class='alert-type' style='color:" + a["color"] + "'>" + a["tipo"] + "</div>"
                        "<div class='alert-title'>" + a["titulo"] + "</div>"
                        "<div class='alert-body'>" + a["body"] + "</div>"
                        "</div></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with main_right:
            # PUNTUACION
            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>Score Breakdown</div>", unsafe_allow_html=True)
            criterios = [
                ("Valoracion", s1, "PER: " + str(round(per, 1)) + "x" if per else "N/D"),
                ("Calidad", s2, "ROE: " + str(round(roe*100, 1)) + "%" if roe else "N/D"),
                ("Financiero", s3, "D/E: " + str(round(deuda_cap, 0)) + "%" if deuda_cap else "N/D"),
                ("Momentum", s4, "Rango 52s: " + str(round(w52l, 0)) + "-" + str(round(w52h, 0)) if w52l and w52h else "N/D"),
                ("DCF Gap", s5, "IV: $" + str(round(intrinseco, 0)) if intrinseco else "N/D"),
            ]
            for nombre_c, pts, detalle in criterios:
                pct = pts / 20 * 100
                bc = "#4ADE80" if pts >= 14 else "#FBBF24" if pts >= 8 else "#F87171"
                st.markdown(
                    "<div class='criteria-row'>"
                    "<span class='criteria-name'>" + nombre_c + "</span>"
                    "<div class='criteria-bar-wrap'><div class='criteria-bar' style='width:" + str(pct) + "%;background:" + bc + "'></div></div>"
                    "<span class='criteria-pts' style='color:" + bc + "'>" + str(pts) + "/20</span>"
                    "</div>"
                    "<div style='font-size:9px;color:#4a6080;padding-left:4px;margin-bottom:4px'>" + detalle + "</div>",
                    unsafe_allow_html=True)
            st.markdown(
                "<div style='border-top:1px solid #1a2332;margin-top:8px;padding-top:8px;display:flex;justify-content:space-between;align-items:center'>"
                "<span style='font-size:10px;color:#4a6080'>TOTAL</span>"
                "<span style='font-size:22px;font-weight:700;color:" + rc + "'>" + str(total) + "/100</span>"
                "<span style='background:" + rb + ";border:1px solid " + rc + ";color:" + rc + ";font-size:11px;font-weight:700;padding:3px 10px;border-radius:2px;letter-spacing:1px'>" + rec + "</span>"
                "</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # FUNDAMENTALES
            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>Fundamentals</div>", unsafe_allow_html=True)
            rows = [
                ("PER trailing", str(round(per, 2)) + "x" if per else "—",
                 "senal-pos" if per and per < 15 else "senal-neg" if per and per > 30 else ""),
                ("PER forward", str(round(per_fwd, 2)) + "x" if per_fwd else "—", ""),
                ("P/Book", str(round(pb, 2)) + "x" if pb else "—",
                 "senal-pos" if pb and pb < 1.5 else "senal-neg" if pb and pb > 6 else ""),
                ("P/Ventas", str(round(ps, 2)) + "x" if ps else "—", ""),
                ("ROE", str(round(roe*100, 1)) + "%" if roe else "—",
                 "senal-pos" if roe and roe > 0.15 else "senal-neg" if roe and roe < 0.05 else ""),
                ("ROA", str(round(roa*100, 1)) + "%" if roa else "—",
                 "senal-pos" if roa and roa > 0.10 else ""),
                ("Margen neto", str(round(margen*100, 1)) + "%" if margen else "—",
                 "senal-pos" if margen and margen > 0.15 else "senal-neg" if margen and margen < 0.05 else ""),
                ("Margen bruto", str(round(margen_bruto*100, 1)) + "%" if margen_bruto else "—", ""),
                ("Deuda/Capital", str(round(deuda_cap, 1)) + "%" if deuda_cap else "—",
                 "senal-pos" if deuda_cap and deuda_cap < 100 else "senal-neg" if deuda_cap and deuda_cap > 300 else ""),
                ("EPS actual", "$" + str(round(eps, 2)) if eps else "—", ""),
                ("Crec. ingresos", str(round(crec_ing*100, 1)) + "%" if crec_ing else "—",
                 "senal-pos" if crec_ing and crec_ing > 0.10 else "senal-neg" if crec_ing and crec_ing < 0 else ""),
                ("Crec. beneficios", str(round(crec_ben*100, 1)) + "%" if crec_ben else "—",
                 "senal-pos" if crec_ben and crec_ben > 0.10 else "senal-neg" if crec_ben and crec_ben < 0 else ""),
            ]
            table_html = "<table class='data-table'>"
            for label, value, cls in rows:
                table_html += "<tr><td>" + label + "</td><td class='" + cls + "'>" + value + "</td></tr>"
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # MERCADO
            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>Market Data</div>", unsafe_allow_html=True)
            mrows = [
                ("Precio actual", "$" + str(round(precio, 2)), ""),
                ("VWAP", "$" + str(round(vwap, 2)) if vwap else "—", ""),
                ("Max 52s", "$" + str(round(w52h, 2)) if w52h else "—", ""),
                ("Min 52s", "$" + str(round(w52l, 2)) if w52l else "—", ""),
                ("MA 50d", "$" + str(round(media50, 2)) if media50 else "—",
                 "senal-pos" if media50 and precio > media50 else "senal-neg" if media50 else ""),
                ("MA 200d", "$" + str(round(media200, 2)) if media200 else "—",
                 "senal-pos" if media200 and precio > media200 else "senal-neg" if media200 else ""),
                ("Beta", str(round(beta, 2)) if beta else "—", ""),
                ("Volumen", str(round(vol/1e6, 1)) + "M" if vol else "—", ""),
                ("Vol medio", str(round(avg_vol/1e6, 1)) + "M" if avg_vol else "—", ""),
                ("Market cap", "$" + str(round(cap/1e9, 1)) + "B" if cap else "—", ""),
            ]
            table_html2 = "<table class='data-table'>"
            for label, value, cls in mrows:
                table_html2 += "<tr><td>" + label + "</td><td class='" + cls + "'>" + value + "</td></tr>"
            table_html2 += "</table>"
            st.markdown(table_html2, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # FLUJO DE CAJA
            if fcf_hist:
                st.markdown("<div class='panel'>", unsafe_allow_html=True)
                st.markdown("<div class='panel-title'>Cash Flow History</div>", unsafe_allow_html=True)
                fig4 = go.Figure()
                anos = [d["year"] for d in fcf_hist]
                fcfs = [d["fcf"]/1e9 for d in fcf_hist]
                ops  = [d["op"]/1e9 for d in fcf_hist]
                fig4.add_trace(go.Bar(x=anos, y=fcfs, name="FCF", marker_color="#3B82F6", opacity=0.8))
                fig4.add_trace(go.Bar(x=anos, y=ops, name="Op CF", marker_color="#4ADE80", opacity=0.5))
                fig4.update_layout(
                    height=150, barmode="group", margin=dict(l=0, r=0, t=5, b=20),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(showgrid=False, color="#4a6080", tickfont=dict(size=9)),
                    yaxis=dict(gridcolor="rgba(26,35,50,0.5)", color="#4a6080",
                               tickfont=dict(size=8), title="B"),
                    legend=dict(font=dict(color="#4a6080", size=9), bgcolor="rgba(0,0,0,0)",
                                orientation="h", y=1.1),
                    font=dict(family="JetBrains Mono")
                )
                st.plotly_chart(fig4, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
