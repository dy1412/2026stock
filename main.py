import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="글로벌 주식 비교 대시보드",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Sky Blue Theme CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,500;0,9..40,700&family=DM+Mono:wght@400;500&display=swap');

/* ── Palette ────────────────────────────────────────────── */
:root {
    --sky-50:  #f0f9ff;
    --sky-100: #e0f2fe;
    --sky-200: #bae6fd;
    --sky-300: #7dd3fc;
    --sky-400: #38bdf8;
    --sky-500: #0ea5e9;
    --sky-600: #0284c7;
    --sky-700: #0369a1;
    --sky-900: #0c4a6e;

    --bg:        #f0f9ff;
    --bg-card:   #ffffff;
    --bg-card2:  #e8f5fd;

    --green:  #10b981;
    --red:    #ef4444;
    --gold:   #f59e0b;
    --violet: #8b5cf6;

    --text:       #0c2340;
    --text-mid:   #334e68;
    --text-muted: #6b90b0;
    --border:     #bae6fd;
    --shadow:     0 2px 16px rgba(14,165,233,0.10);
    --shadow-lg:  0 8px 32px rgba(14,165,233,0.18);
}

/* ── Global ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', 'Noto Sans KR', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Main block ─────────────────────────────────────────── */
.main .block-container {
    padding: 1.8rem 2.2rem 4rem 2.2rem !important;
    max-width: 1440px;
}
.main {
    background: linear-gradient(155deg, #e0f2fe 0%, #f0f9ff 55%, #e8f5fd 100%) !important;
    min-height: 100vh;
}

/* ── Animated header ────────────────────────────────────── */
.dash-header {
    background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 55%, #38bdf8 100%);
    border-radius: 22px;
    padding: 2.2rem 2.6rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(2,132,199,0.28);
    position: relative;
    overflow: hidden;
}
.dash-header::before {
    content: "";
    position: absolute;
    top: -80px; right: -80px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.10);
    pointer-events: none;
}
.dash-header::after {
    content: "";
    position: absolute;
    bottom: -50px; left: 28%;
    width: 190px; height: 190px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
    pointer-events: none;
}
.dash-header-inner { position: relative; z-index: 1; }
.dash-header-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.dash-header-sub {
    font-size: 0.92rem;
    color: rgba(255,255,255,0.80);
    margin-top: 8px;
    font-weight: 400;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(255,255,255,0.18);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.38);
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 1.2px;
    margin-top: 14px;
    width: fit-content;
    backdrop-filter: blur(6px);
}
.live-dot-circle {
    width: 7px; height: 7px;
    background: #a7f3d0;
    border-radius: 50%;
    box-shadow: 0 0 7px #6ee7b7;
    animation: blink 1.8s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── Section label ──────────────────────────────────────── */
.sec-hd {
    display: flex;
    align-items: center;
    gap: 9px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--sky-600);
    margin: 1.9rem 0 0.9rem 0;
    padding-bottom: 9px;
    border-bottom: 2px solid var(--sky-200);
}
.sec-hd-bar {
    width: 4px; height: 15px;
    background: linear-gradient(180deg, var(--sky-500), var(--sky-300));
    border-radius: 2px;
    flex-shrink: 0;
}

/* ── Price cards ─────────────────────────────────────────── */
.pcard {
    background: var(--bg-card);
    border: 1.5px solid var(--border);
    border-radius: 18px;
    padding: 1.25rem 1.4rem;
    box-shadow: var(--shadow);
    transition: box-shadow .22s, transform .22s, border-color .22s;
    position: relative;
    overflow: hidden;
}
.pcard::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--sky-400), var(--sky-300));
    border-radius: 18px 18px 0 0;
}
.pcard:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-3px);
    border-color: var(--sky-400);
}
.pcard-ticker {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    color: var(--sky-500);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.pcard-name {
    font-size: 0.86rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 9px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.pcard-price {
    font-family: 'DM Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.5px;
}
.pcard-up   { font-family:'DM Mono',monospace; font-size:.82rem; color:var(--green); font-weight:700; margin-top:5px; }
.pcard-down { font-family:'DM Mono',monospace; font-size:.82rem; color:var(--red);   font-weight:700; margin-top:5px; }

/* ── Badges ──────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-left: 6px;
    vertical-align: middle;
}
.badge-kr { background:#dbeafe; color:#1d4ed8; border:1px solid #93c5fd; }
.badge-us { background:#fce7f3; color:#be185d; border:1px solid #f9a8d4; }

/* ── Info card ───────────────────────────────────────────── */
.icard {
    background: var(--bg-card);
    border: 1.5px solid var(--border);
    border-radius: 18px;
    padding: 1.3rem 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 0.85rem;
}
.icard-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 0.66rem;
    color: var(--sky-500);
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 10px;
    font-weight: 500;
}

/* ── Ranking rows ────────────────────────────────────────── */
.rank-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 9px 0;
    border-bottom: 1px solid var(--sky-100);
    font-size: 0.86rem;
    color: var(--text-mid);
}
.rank-row:last-child { border-bottom: none; }

/* ── Sidebar ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #dbeafe 0%, #e0f2fe 40%, #f0f9ff 100%) !important;
    border-right: 1.5px solid var(--border) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.6rem 1.2rem !important;
}

/* ── Streamlit metric ────────────────────────────────────── */
div[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1rem 1.2rem !important;
    box-shadow: var(--shadow) !important;
}
label[data-testid="stMetricLabel"] { color:var(--text-muted)!important; font-size:.76rem!important; }
div[data-testid="stMetricValue"]   { color:var(--text)!important; font-family:'DM Mono',monospace!important; font-weight:700!important; }

/* ── Form elements ───────────────────────────────────────── */
.stSelectbox label, .stMultiSelect label {
    color: var(--text-mid) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
}
.stSelectbox > div > div, .stMultiSelect > div > div {
    background:#ffffff!important;
    border: 1.5px solid var(--border)!important;
    border-radius: 10px!important;
    color: var(--text)!important;
}

/* ── Tabs ────────────────────────────────────────────────── */
div[data-testid="stTabs"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--sky-600) !important;
    border-bottom: 2.5px solid var(--sky-500) !important;
}

/* ── Checkbox ────────────────────────────────────────────── */
.stCheckbox label { color:var(--text-mid)!important; font-weight:500!important; font-size:.84rem!important; }

/* ── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:var(--sky-50); }
::-webkit-scrollbar-thumb { background:var(--sky-300); border-radius:3px; }

/* ── Plotly transparent bg ───────────────────────────────── */
.js-plotly-plot .plotly .bg { fill:transparent!important; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
KR_STOCKS = {
    "삼성전자": "005930.KS", "SK하이닉스": "000660.KS", "LG에너지솔루션": "373220.KS",
    "현대차": "005380.KS", "기아": "000270.KS", "NAVER": "035420.KS",
    "카카오": "035720.KS", "셀트리온": "068270.KS", "포스코홀딩스": "005490.KS",
    "KB금융": "105560.KS", "신한지주": "055550.KS", "LG화학": "051910.KS",
    "삼성SDI": "006400.KS", "SK이노베이션": "096770.KS", "하이브": "352820.KS",
}
US_STOCKS = {
    "Apple": "AAPL", "Microsoft": "MSFT", "NVIDIA": "NVDA", "Amazon": "AMZN",
    "Alphabet": "GOOGL", "Meta": "META", "Tesla": "TSLA", "Berkshire Hathaway": "BRK-B",
    "JPMorgan Chase": "JPM", "Visa": "V", "Johnson & Johnson": "JNJ",
    "ExxonMobil": "XOM", "UnitedHealth": "UNH", "Walmart": "WMT", "Netflix": "NFLX",
}
INDICES = {
    "KOSPI": "^KS11", "KOSDAQ": "^KQ11",
    "S&P 500": "^GSPC", "NASDAQ": "^IXIC", "Dow Jones": "^DJI",
}
PERIOD_OPTIONS = {
    "1개월": "1mo", "3개월": "3mo", "6개월": "6mo",
    "1년": "1y", "2년": "2y", "5년": "5y",
}
KR_COLORS  = ["#0284c7","#0ea5e9","#38bdf8","#7dd3fc","#0369a1","#075985","#bae6fd","#0c4a6e"]
US_COLORS  = ["#f59e0b","#d97706","#fbbf24","#b45309","#fcd34d","#92400e","#fde68a","#78350f"]
IDX_COLORS = ["#8b5cf6","#6d28d9"]

# ─── Helpers ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_price_data(tickers: list, period: str) -> dict:
    out = {}
    for t in tickers:
        try:
            h = yf.Ticker(t).history(period=period)
            if not h.empty:
                out[t] = h["Close"]
        except Exception:
            pass
    return out

@st.cache_data(ttl=300)
def fetch_current_info(ticker: str) -> dict:
    try:
        obj  = yf.Ticker(ticker)
        info = obj.info
        hist = obj.history(period="2d")
        if len(hist) >= 2:
            prev, curr = hist["Close"].iloc[-2], hist["Close"].iloc[-1]
            chg = curr - prev; pct = chg / prev * 100
        elif len(hist) == 1:
            curr = hist["Close"].iloc[-1]; chg = pct = 0
        else:
            curr = chg = pct = None
        return {"price": curr, "change": chg or 0, "change_pct": pct or 0,
                "name": info.get("shortName", ticker), "currency": info.get("currency", "")}
    except Exception:
        return {"price": None, "change": 0, "change_pct": 0, "name": ticker, "currency": ""}

def compute_returns(s):
    if s is None or len(s) < 2: return {}
    f, l = s.iloc[0], s.iloc[-1]
    return {"total_return": (l-f)/f*100, "normalized": s/f*100, "first": f, "last": l}

def fmt_price(p, cur):
    if p is None: return "N/A"
    return f"₩{p:,.0f}" if cur == "KRW" else f"${p:,.2f}"

def fmt_chg(pct):
    return ("▲", f"{abs(pct):.2f}%") if pct >= 0 else ("▼", f"{abs(pct):.2f}%")

def fmt_num(v, dec=1):
    if v is None: return "N/A"
    if v >= 1e12: return f"{v/1e12:.{dec}f}T"
    if v >= 1e9:  return f"{v/1e9:.{dec}f}B"
    if v >= 1e6:  return f"{v/1e6:.{dec}f}M"
    return f"{v:,.0f}"

def base_layout(h=430, title=""):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(240,249,255,0.55)",
        font=dict(family="DM Sans, Noto Sans KR, sans-serif", color="#334e68", size=12),
        height=h,
        margin=dict(l=8, r=8, t=40 if title else 18, b=8),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(255,255,255,0.88)", bordercolor="#bae6fd",
                    borderwidth=1, font=dict(size=11)),
        xaxis=dict(gridcolor="rgba(186,230,253,0.55)", linecolor="#bae6fd"),
        yaxis=dict(gridcolor="rgba(186,230,253,0.55)", linecolor="#bae6fd"),
        title=dict(text=title, font=dict(size=13, color="#0c4a6e"), x=0.01) if title else {},
    )

def sec(label):
    st.markdown(
        f'<div class="sec-hd"><span class="sec-hd-bar"></span>{label}</div>',
        unsafe_allow_html=True
    )

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:.5rem 0 1.4rem;">
      <div style="font-size:2.2rem;line-height:1.1;">☀️</div>
      <div style="font-size:1.05rem;font-weight:700;color:#0369a1;letter-spacing:-.3px;margin-top:4px;">
        주식 대시보드
      </div>
      <div style="font-size:.74rem;color:#6b90b0;margin-top:3px;">글로벌 마켓 한눈에</div>
    </div>
    """, unsafe_allow_html=True)

    period_label = st.selectbox("📅 조회 기간", list(PERIOD_OPTIONS.keys()), index=3)
    period = PERIOD_OPTIONS[period_label]

    st.markdown("---")
    st.markdown("**🇰🇷 한국 주식**")
    kr_names = st.multiselect("종목 선택", list(KR_STOCKS.keys()),
                               default=["삼성전자","SK하이닉스","현대차","NAVER"])
    kr_selected = {n: KR_STOCKS[n] for n in kr_names}

    st.markdown("**🇺🇸 미국 주식**")
    us_names = st.multiselect("종목 선택", list(US_STOCKS.keys()),
                               default=["Apple","NVIDIA","Tesla","Microsoft"], key="us_s")
    us_selected = {n: US_STOCKS[n] for n in us_names}

    st.markdown("**📊 시장 지수**")
    idx_names = st.multiselect("지수 선택", list(INDICES.keys()),
                                default=["KOSPI","S&P 500"], key="idx_s")
    idx_selected = {n: INDICES[n] for n in idx_names}

    st.markdown("---")
    show_volume = st.checkbox("거래량 표시", value=True)
    show_ma     = st.checkbox("이동평균선 (20/60일)", value=False)

    st.markdown("""
    <div style="margin-top:1.4rem;font-size:.73rem;color:#7ab3cc;line-height:1.9;
                background:rgba(14,165,233,.07);border-radius:12px;padding:11px 14px;
                border:1px solid rgba(186,230,253,.6);">
      📡 데이터: Yahoo Finance<br>
      🔄 5분 간격 자동 갱신<br>
      ⚠️ 투자 참고용 / 권유 아님
    </div>
    """, unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div class="dash-header-inner">
    <div class="dash-header-title">📈 글로벌 주식 비교 대시보드</div>
    <div class="dash-header-sub">한국 · 미국 주요 종목의 수익률과 차트를 실시간으로 비교합니다</div>
    <div class="live-badge">
      <span class="live-dot-circle"></span>LIVE DATA
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Guard ────────────────────────────────────────────────────────────────────
all_selected = {**kr_selected, **us_selected}
all_tickers  = list(all_selected.values()) + list(idx_selected.values())
if not all_tickers:
    st.info("👈 사이드바에서 종목을 선택해 주세요.")
    st.stop()

with st.spinner("📡 시세 데이터 불러오는 중..."):
    price_data = fetch_price_data(all_tickers, period)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 수익률 비교", "📈 차트 분석", "🏆 성과 랭킹", "🔍 종목 상세"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – 수익률 비교
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    sec("실시간 시세")
    cards = [(n,t,"KR") for n,t in kr_selected.items()] + \
            [(n,t,"US") for n,t in us_selected.items()]
    COLS = 4
    for row_s in range(0, len(cards), COLS):
        chunk = cards[row_s:row_s+COLS]
        cols  = st.columns(len(chunk))
        for col, (name, ticker, region) in zip(cols, chunk):
            info = fetch_current_info(ticker)
            arrow, pct_s = fmt_chg(info["change_pct"])
            cls   = "pcard-up" if info["change_pct"] >= 0 else "pcard-down"
            badge = f'<span class="badge badge-kr">KR</span>' if region=="KR" \
                    else f'<span class="badge badge-us">US</span>'
            with col:
                st.markdown(f"""
                <div class="pcard">
                  <div class="pcard-ticker">{ticker}{badge}</div>
                  <div class="pcard-name">{name}</div>
                  <div class="pcard-price">{fmt_price(info['price'],info['currency'])}</div>
                  <div class="{cls}">{arrow} {pct_s}</div>
                </div>""", unsafe_allow_html=True)

    sec("정규화 수익률 비교 — 시작일 = 100")
    fig = go.Figure()
    for i,(n,t) in enumerate(kr_selected.items()):
        if t in price_data:
            r = compute_returns(price_data[t])
            if r:
                fig.add_trace(go.Scatter(
                    x=r["normalized"].index, y=r["normalized"].values,
                    name=f"🇰🇷 {n}",
                    line=dict(color=KR_COLORS[i%len(KR_COLORS)], width=2.5),
                    hovertemplate=f"<b>{n}</b><br>%{{x|%Y-%m-%d}}<br>%{{y:.1f}}<extra></extra>",
                ))
    for i,(n,t) in enumerate(us_selected.items()):
        if t in price_data:
            r = compute_returns(price_data[t])
            if r:
                fig.add_trace(go.Scatter(
                    x=r["normalized"].index, y=r["normalized"].values,
                    name=f"🇺🇸 {n}",
                    line=dict(color=US_COLORS[i%len(US_COLORS)], width=2.5),
                    hovertemplate=f"<b>{n}</b><br>%{{x|%Y-%m-%d}}<br>%{{y:.1f}}<extra></extra>",
                ))
    for i,(n,t) in enumerate(idx_selected.items()):
        if t in price_data:
            r = compute_returns(price_data[t])
            if r:
                fig.add_trace(go.Scatter(
                    x=r["normalized"].index, y=r["normalized"].values,
                    name=f"📊 {n}",
                    line=dict(color=IDX_COLORS[i%2], width=2, dash="dot"),
                    hovertemplate=f"<b>{n}</b><br>%{{x|%Y-%m-%d}}<br>%{{y:.1f}}<extra></extra>",
                ))
    fig.add_hline(y=100, line_dash="dash", line_color="rgba(14,165,233,0.35)", line_width=1.5)
    lay = base_layout(h=460)
    lay["legend"]["x"] = 1.01; lay["legend"]["y"] = 1
    fig.update_layout(**lay)
    st.plotly_chart(fig, use_container_width=True)

    sec("기간 수익률 요약")
    rows = []
    for name, ticker in {**kr_selected,**us_selected,**idx_selected}.items():
        if ticker in price_data:
            r = compute_returns(price_data[ticker])
            if r:
                info = fetch_current_info(ticker)
                region = "🇰🇷 한국" if ticker in kr_selected.values() \
                         else ("🇺🇸 미국" if ticker in us_selected.values() else "📊 지수")
                a, p = fmt_chg(info["change_pct"])
                rows.append({
                    "종목명": name, "지역": region,
                    "현재가": fmt_price(info["price"],info["currency"]),
                    "전일대비": f"{a} {p}",
                    f"{period_label} 수익률": f"{r['total_return']:+.2f}%",
                    "시작가": fmt_price(r["first"],info["currency"]),
                    "기말가": fmt_price(r["last"], info["currency"]),
                })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – 차트 분석
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    sec("개별 주가 차트")
    chart_items = [(n,t,"KR") for n,t in kr_selected.items()] + \
                  [(n,t,"US") for n,t in us_selected.items()]
    if not chart_items:
        st.info("사이드바에서 종목을 선택해 주세요.")
    else:
        labels    = [f"{'🇰🇷' if r=='KR' else '🇺🇸'} {n}" for n,_,r in chart_items]
        sel_label = st.selectbox("종목 선택", labels, key="chart_sel")
        idx_c     = labels.index(sel_label)
        sel_name, sel_ticker, sel_region = chart_items[idx_c]

        if sel_ticker in price_data:
            info      = fetch_current_info(sel_ticker)
            hist_full = yf.Ticker(sel_ticker).history(period=period)
            rn        = 2 if show_volume else 1
            fig_c     = make_subplots(
                rows=rn, cols=1, shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.75,0.25] if show_volume else [1.0],
            )
            fig_c.add_trace(go.Candlestick(
                x=hist_full.index,
                open=hist_full["Open"], high=hist_full["High"],
                low=hist_full["Low"],   close=hist_full["Close"],
                name="OHLC",
                increasing_line_color="#10b981", decreasing_line_color="#ef4444",
                increasing_fillcolor="#10b981",  decreasing_fillcolor="#ef4444",
            ), row=1, col=1)
            if show_ma:
                for ma, color in [(20,"#f59e0b"),(60,"#8b5cf6")]:
                    if len(hist_full) >= ma:
                        ms = hist_full["Close"].rolling(ma).mean()
                        fig_c.add_trace(go.Scatter(
                            x=ms.index, y=ms.values,
                            name=f"MA{ma}", line=dict(color=color, width=1.8),
                        ), row=1, col=1)
            if show_volume and "Volume" in hist_full.columns:
                vc = ["#10b981" if c>=o else "#ef4444"
                      for c,o in zip(hist_full["Close"],hist_full["Open"])]
                fig_c.add_trace(go.Bar(
                    x=hist_full.index, y=hist_full["Volume"],
                    name="거래량", marker_color=vc, opacity=0.6,
                ), row=2, col=1)
            lay_c = base_layout(h=520, title=f"{sel_name} ({sel_ticker}) — {period_label} 캔들 차트")
            lay_c["xaxis_rangeslider_visible"] = False
            fig_c.update_layout(**lay_c)
            for rx in range(1, rn+1):
                fig_c.update_xaxes(gridcolor="rgba(186,230,253,.55)", linecolor="#bae6fd", row=rx, col=1)
                fig_c.update_yaxes(gridcolor="rgba(186,230,253,.55)", linecolor="#bae6fd", row=rx, col=1)
            st.plotly_chart(fig_c, use_container_width=True)

            ret = compute_returns(price_data[sel_ticker])
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("현재가",         fmt_price(info["price"],info["currency"]))
            c2.metric("전일대비",        f"{info['change_pct']:+.2f}%")
            c3.metric(f"{period_label} 수익률", f"{ret.get('total_return',0):+.2f}%" if ret else "N/A")
            high = hist_full["High"].max(); low = hist_full["Low"].min()
            c4.metric(f"{period_label} 최고가", fmt_price(high,info["currency"]),
                      delta=f"최저 {fmt_price(low,info['currency'])}")

    if idx_selected:
        sec("시장 지수 차트")
        fig_i = go.Figure()
        for i,(n,t) in enumerate(idx_selected.items()):
            if t in price_data:
                s = price_data[t]
                fig_i.add_trace(go.Scatter(
                    x=s.index, y=s.values, name=n,
                    fill="tozeroy",
                    fillcolor=f"rgba(56,189,248,{0.07+i*0.04})",
                    line=dict(color=IDX_COLORS[i%2], width=2.5),
                ))
        fig_i.update_layout(**base_layout(h=300))
        st.plotly_chart(fig_i, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – 성과 랭킹
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    sec("수익률 랭킹")
    ranking = []
    for name, ticker in all_selected.items():
        if ticker in price_data:
            r = compute_returns(price_data[ticker])
            if r:
                info   = fetch_current_info(ticker)
                region = "🇰🇷" if ticker in kr_selected.values() else "🇺🇸"
                ranking.append({"name":name,"ticker":ticker,"region":region,
                                 "return":r["total_return"],"currency":info["currency"]})

    if ranking:
        ranking.sort(key=lambda x: x["return"], reverse=True)
        bc = ["#10b981" if r["return"]>=0 else "#ef4444" for r in ranking]
        fig_b = go.Figure(go.Bar(
            x=[r["return"] for r in ranking],
            y=[f"{r['region']} {r['name']}" for r in ranking],
            orientation="h",
            marker=dict(color=bc, opacity=0.82, line=dict(width=0)),
            text=[f"{r['return']:+.2f}%" for r in ranking],
            textposition="outside",
            textfont=dict(size=11, family="DM Mono"),
        ))
        fig_b.add_vline(x=0, line_color="rgba(14,165,233,.5)", line_width=1.5)
        lb = base_layout(h=max(280, len(ranking)*44), title=f"{period_label} 수익률 순위")
        lb["yaxis"]["autorange"]  = "reversed"
        lb["xaxis"]["ticksuffix"] = "%"
        lb["showlegend"]          = False
        lb["margin"]["r"]         = 80
        fig_b.update_layout(**lb)
        st.plotly_chart(fig_b, use_container_width=True)

        sec("리스크 · 수익률 분포")
        sd = []
        for r in ranking:
            if r["ticker"] in price_data:
                vol = price_data[r["ticker"]].pct_change().dropna().std() * np.sqrt(252) * 100
                sd.append({**r, "vol": vol})
        if sd:
            fig_s = go.Figure()
            for item in sd:
                color = "#0ea5e9" if item["region"]=="🇰🇷" else "#f59e0b"
                fig_s.add_trace(go.Scatter(
                    x=[item["vol"]], y=[item["return"]],
                    mode="markers+text",
                    marker=dict(size=15, color=color, opacity=0.82,
                                line=dict(width=2.5, color="white")),
                    text=[item["name"]],
                    textposition="top center",
                    textfont=dict(size=10, color="#334e68"),
                    showlegend=False,
                    hovertemplate=(f"<b>{item['region']} {item['name']}</b><br>"
                                   f"수익률: {item['return']:+.2f}%<br>"
                                   f"변동성: {item['vol']:.1f}%<extra></extra>"),
                ))
            fig_s.add_hline(y=0, line_dash="dash", line_color="rgba(14,165,233,.4)")
            ls = base_layout(h=420, title="리스크(연환산 변동성) vs 수익률")
            ls["xaxis"]["title"] = "연환산 변동성 (%)"
            ls["yaxis"]["title"] = f"{period_label} 수익률 (%)"
            fig_s.update_layout(**ls)
            st.plotly_chart(fig_s, use_container_width=True)

        col_kr, col_us = st.columns(2)
        kr_r = sorted([r for r in ranking if r["region"]=="🇰🇷"], key=lambda x:x["return"],reverse=True)
        us_r = sorted([r for r in ranking if r["region"]=="🇺🇸"], key=lambda x:x["return"],reverse=True)

        for col, items, label in [(col_kr, kr_r, "🇰🇷 한국 순위"), (col_us, us_r, "🇺🇸 미국 순위")]:
            with col:
                sec(label)
                st.markdown('<div class="icard">', unsafe_allow_html=True)
                for i, r in enumerate(items):
                    medal = ["🥇","🥈","🥉"][i] if i<3 else f"#{i+1}"
                    color = "#10b981" if r["return"]>=0 else "#ef4444"
                    st.markdown(
                        f'<div class="rank-row"><span>{medal} {r["name"]}</span>'
                        f'<span style="color:{color};font-family:DM Mono,monospace;font-weight:700;">'
                        f'{r["return"]:+.2f}%</span></div>',
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 – 종목 상세
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    sec("종목 상세 정보")
    if not all_selected:
        st.info("사이드바에서 종목을 선택해 주세요.")
    else:
        detail_name   = st.selectbox("종목 선택", list(all_selected.keys()), key="det_sel")
        detail_ticker = all_selected[detail_name]
        detail_region = "KR" if detail_ticker in kr_selected.values() else "US"

        info = fetch_current_info(detail_ticker)
        try:
            full = yf.Ticker(detail_ticker).info
        except Exception:
            full = {}

        arrow, pct_s = fmt_chg(info["change_pct"])
        chg_color = "#10b981" if info["change_pct"]>=0 else "#ef4444"
        badge_html = ('<span class="badge badge-kr">KR</span>' if detail_region=="KR"
                      else '<span class="badge badge-us">US</span>')

        col_a, col_b = st.columns([2,1])
        with col_a:
            st.markdown(f"""
            <div class="icard" style="margin-bottom:1rem;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                <span style="font-family:DM Mono,monospace;font-size:.95rem;
                             font-weight:600;color:#0369a1;">{detail_ticker}</span>
                {badge_html}
              </div>
              <div style="font-size:1.4rem;font-weight:700;color:#0c2340;margin-bottom:6px;">
                {info['name']}
              </div>
              <div style="font-family:DM Mono,monospace;font-size:2.1rem;
                          font-weight:700;color:#0c2340;letter-spacing:-1px;">
                {fmt_price(info['price'],info['currency'])}
              </div>
              <div style="color:{chg_color};font-family:DM Mono,monospace;
                          font-size:1rem;font-weight:600;margin-top:6px;">
                {arrow} {pct_s}
              </div>
            </div>
            """, unsafe_allow_html=True)

            mc=full.get("marketCap"); pe=full.get("trailingPE"); pb=full.get("priceToBook")
            dy=full.get("dividendYield"); beta=full.get("beta")
            w52h=full.get("fiftyTwoWeekHigh"); w52l=full.get("fiftyTwoWeekLow")
            avol=full.get("averageVolume")

            m1,m2,m3,m4 = st.columns(4)
            m1.metric("시가총액",   fmt_num(mc))
            m2.metric("P/E (TTM)", f"{pe:.1f}x"      if pe   else "N/A")
            m3.metric("P/B",       f"{pb:.2f}x"      if pb   else "N/A")
            m4.metric("배당수익률", f"{dy*100:.2f}%"  if dy   else "N/A")
            m5,m6,m7,m8 = st.columns(4)
            m5.metric("베타",       f"{beta:.2f}"     if beta else "N/A")
            m6.metric("52주 최고",  fmt_price(w52h, info["currency"]))
            m7.metric("52주 최저",  fmt_price(w52l, info["currency"]))
            m8.metric("평균 거래량", fmt_num(avol, 0))

        with col_b:
            sector   = full.get("sector","");   industry = full.get("industry","")
            country  = full.get("country","");  exchange = full.get("exchange","")
            emp      = full.get("fullTimeEmployees"); website = full.get("website","")
            rows_h = ""
            if sector:   rows_h += f'<div><span style="color:#6b90b0;">섹터</span> &nbsp; {sector}</div>'
            if industry: rows_h += f'<div><span style="color:#6b90b0;">업종</span> &nbsp; {industry}</div>'
            if country:  rows_h += f'<div><span style="color:#6b90b0;">국가</span> &nbsp; {country}</div>'
            if exchange: rows_h += f'<div><span style="color:#6b90b0;">거래소</span> &nbsp; {exchange}</div>'
            if emp:      rows_h += f'<div><span style="color:#6b90b0;">직원수</span> &nbsp; {emp:,}명</div>'
            if website:  rows_h += f'<div style="margin-top:8px;"><a href="{website}" target="_blank" style="color:#0ea5e9;font-size:.8rem;">🔗 공식 웹사이트</a></div>'
            st.markdown(f"""
            <div class="icard">
              <div class="icard-lbl">기업 정보</div>
              <div style="font-size:.84rem;line-height:2.1;color:#334e68;">{rows_h}</div>
            </div>
            """, unsafe_allow_html=True)
            summary = full.get("longBusinessSummary","")
            if summary:
                st.markdown(f"""
                <div class="icard">
                  <div class="icard-lbl">사업 개요</div>
                  <div style="font-size:.78rem;color:#6b90b0;line-height:1.7;
                              max-height:200px;overflow-y:auto;">
                    {summary[:500]}{'...' if len(summary)>500 else ''}
                  </div>
                </div>
                """, unsafe_allow_html=True)

        if len(all_selected) >= 2:
            sec("상관관계 히트맵")
            ret_df = pd.DataFrame({
                n: price_data[t].pct_change()
                for n,t in all_selected.items() if t in price_data
            })
            if len(ret_df.columns) >= 2:
                corr  = ret_df.corr()
                fig_h = go.Figure(go.Heatmap(
                    z=corr.values,
                    x=corr.columns.tolist(),
                    y=corr.index.tolist(),
                    colorscale=[[0,"#ef4444"],[0.5,"#e0f2fe"],[1,"#0ea5e9"]],
                    zmin=-1, zmax=1,
                    text=[[f"{v:.2f}" for v in row] for row in corr.values],
                    texttemplate="%{text}",
                    textfont=dict(size=10, color="#0c2340"),
                    hovertemplate="%{y} vs %{x}: %{z:.3f}<extra></extra>",
                ))
                lh = base_layout(h=max(320, len(corr)*50),
                                  title=f"{period_label} 일간 수익률 기준 상관관계")
                fig_h.update_layout(**lh)
                st.plotly_chart(fig_h, use_container_width=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:3rem;padding:1.4rem 2rem;
            background:linear-gradient(135deg,#e0f2fe,#f0f9ff);
            border-radius:18px;border:1.5px solid #bae6fd;
            text-align:center;font-size:.78rem;color:#6b90b0;line-height:2.2;
            box-shadow:0 2px 12px rgba(14,165,233,.08);">
  <span style="font-weight:700;color:#0369a1;font-size:.9rem;">☀️ 글로벌 주식 비교 대시보드</span><br>
  데이터 출처: Yahoo Finance (yfinance) &nbsp;·&nbsp; 5분 간격 갱신
  &nbsp;·&nbsp; 본 대시보드는 투자 참고용이며 투자 권유가 아닙니다.
</div>
""", unsafe_allow_html=True)
