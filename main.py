import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="글로벌 주식 비교 대시보드",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');

/* Root theme */
:root {
    --bg-primary: #0a0e1a;
    --bg-card: #111827;
    --bg-card2: #1a2235;
    --accent-green: #00e676;
    --accent-red: #ff4d6d;
    --accent-blue: #4facfe;
    --accent-gold: #ffd166;
    --text-primary: #f0f4ff;
    --text-muted: #7a8ab0;
    --border: rgba(255,255,255,0.07);
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

/* Main container */
.main .block-container {
    padding: 1.5rem 2rem 3rem 2rem;
    max-width: 1400px;
}

/* Header */
.dashboard-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 1.5rem 0 0.5rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.header-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}
.header-subtitle {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-top: 2px;
}
.live-badge {
    background: rgba(0,230,118,0.12);
    color: var(--accent-green);
    border: 1px solid rgba(0,230,118,0.3);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 1px;
}

/* Metric cards */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: rgba(79,172,254,0.3); }
.metric-ticker {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 1px;
    margin-bottom: 4px;
}
.metric-name {
    font-size: 0.85rem;
    color: var(--text-primary);
    font-weight: 500;
    margin-bottom: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.metric-price {
    font-family: 'Space Mono', monospace;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
}
.metric-change-pos {
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    color: var(--accent-green);
    font-weight: 700;
}
.metric-change-neg {
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    color: var(--accent-red);
    font-weight: 700;
}

/* Section headers */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 2px;
    color: var(--text-muted);
    text-transform: uppercase;
    margin: 1.6rem 0 0.8rem 0;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border);
}

/* Country flags */
.flag-tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-left: 6px;
}
.flag-kr { background: rgba(0,114,255,0.15); color: #4facfe; border: 1px solid rgba(79,172,254,0.3); }
.flag-us { background: rgba(255,65,54,0.12); color: #ff6b6b; border: 1px solid rgba(255,107,107,0.3); }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0d1322 !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

/* Plotly chart background */
.js-plotly-plot .plotly .bg { fill: transparent !important; }

/* Streamlit overrides */
div[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
}
label[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 0.78rem; }
div[data-testid="stMetricValue"] { color: var(--text-primary) !important; font-family: 'Space Mono', monospace; }

.stSelectbox > div > div { background-color: var(--bg-card2) !important; }
.stMultiSelect > div > div { background-color: var(--bg-card2) !important; }

/* Tabs */
div[data-testid="stTabs"] button {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.5px;
}

/* Info box */
.info-box {
    background: rgba(79,172,254,0.07);
    border: 1px solid rgba(79,172,254,0.2);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: #8ab4f8;
    margin-bottom: 1rem;
}

/* Performance bar */
.perf-bar-container { margin-bottom: 10px; }
.perf-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    margin-bottom: 4px;
}
.perf-bar-bg {
    background: rgba(255,255,255,0.07);
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
}
.perf-bar-fill-pos {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #00e676, #69f0ae);
}
.perf-bar-fill-neg {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #ff4d6d, #ff8a9a);
}
</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
KR_STOCKS = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "LG에너지솔루션": "373220.KS",
    "현대차": "005380.KS",
    "기아": "000270.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "셀트리온": "068270.KS",
    "포스코홀딩스": "005490.KS",
    "KB금융": "105560.KS",
    "신한지주": "055550.KS",
    "LG화학": "051910.KS",
    "삼성SDI": "006400.KS",
    "SK이노베이션": "096770.KS",
    "하이브": "352820.KS",
}

US_STOCKS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Meta": "META",
    "Tesla": "TSLA",
    "Berkshire Hathaway": "BRK-B",
    "JPMorgan Chase": "JPM",
    "Visa": "V",
    "Johnson & Johnson": "JNJ",
    "ExxonMobil": "XOM",
    "UnitedHealth": "UNH",
    "Walmart": "WMT",
    "Netflix": "NFLX",
}

INDICES = {
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Dow Jones": "^DJI",
}

PERIOD_OPTIONS = {
    "1개월": "1mo",
    "3개월": "3mo",
    "6개월": "6mo",
    "1년": "1y",
    "2년": "2y",
    "5년": "5y",
}

# ─── Data Helpers ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_price_data(tickers: list, period: str) -> dict:
    result = {}
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period=period)
            if not hist.empty:
                result[ticker] = hist["Close"]
        except Exception:
            pass
    return result

@st.cache_data(ttl=300)
def fetch_current_info(ticker: str) -> dict:
    try:
        t = yf.Ticker(ticker)
        info = t.info
        hist = t.history(period="2d")
        if len(hist) >= 2:
            prev_close = hist["Close"].iloc[-2]
            curr_price = hist["Close"].iloc[-1]
            chg = curr_price - prev_close
            chg_pct = (chg / prev_close) * 100
        elif len(hist) == 1:
            curr_price = hist["Close"].iloc[-1]
            chg, chg_pct = 0, 0
        else:
            curr_price, chg, chg_pct = None, 0, 0
        return {
            "price": curr_price,
            "change": chg,
            "change_pct": chg_pct,
            "name": info.get("shortName", ticker),
            "currency": info.get("currency", ""),
            "market_cap": info.get("marketCap"),
            "pe": info.get("trailingPE"),
            "volume": info.get("volume"),
        }
    except Exception:
        return {"price": None, "change": 0, "change_pct": 0, "name": ticker, "currency": ""}

def compute_returns(price_series: pd.Series) -> dict:
    if price_series.empty or len(price_series) < 2:
        return {}
    first = price_series.iloc[0]
    last = price_series.iloc[-1]
    total_ret = ((last - first) / first) * 100
    normalized = (price_series / first) * 100
    return {"total_return": total_ret, "normalized": normalized, "first": first, "last": last}

def format_price(price, currency):
    if price is None:
        return "N/A"
    if currency == "KRW":
        return f"₩{price:,.0f}"
    return f"${price:,.2f}"

def format_change(chg, chg_pct):
    sign = "+" if chg >= 0 else ""
    return f"{sign}{chg_pct:.2f}%"

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ 설정")
    st.markdown("---")

    period_label = st.selectbox("📅 기간", list(PERIOD_OPTIONS.keys()), index=3)
    period = PERIOD_OPTIONS[period_label]

    st.markdown("#### 🇰🇷 한국 주식")
    kr_selected_names = st.multiselect(
        "종목 선택",
        list(KR_STOCKS.keys()),
        default=["삼성전자", "SK하이닉스", "현대차", "NAVER"],
        key="kr_select"
    )
    kr_selected = {n: KR_STOCKS[n] for n in kr_selected_names}

    st.markdown("#### 🇺🇸 미국 주식")
    us_selected_names = st.multiselect(
        "종목 선택",
        list(US_STOCKS.keys()),
        default=["Apple", "NVIDIA", "Tesla", "Microsoft"],
        key="us_select"
    )
    us_selected = {n: US_STOCKS[n] for n in us_selected_names}

    st.markdown("#### 📊 지수")
    idx_selected_names = st.multiselect(
        "지수 선택",
        list(INDICES.keys()),
        default=["KOSPI", "S&P 500"],
        key="idx_select"
    )
    idx_selected = {n: INDICES[n] for n in idx_selected_names}

    st.markdown("---")
    show_volume = st.checkbox("거래량 표시", value=True)
    show_ma = st.checkbox("이동평균선 (20/60일)", value=False)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;color:#4a5a80;'>데이터: Yahoo Finance<br>5분마다 자동 갱신</div>",
        unsafe_allow_html=True
    )

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dashboard-header">
  <div>
    <div class="header-title">📈 글로벌 주식 비교 대시보드</div>
    <div class="header-subtitle">한국 · 미국 주요 종목 수익률 & 차트 비교 분석</div>
  </div>
  <div class="live-badge">● LIVE</div>
</div>
""", unsafe_allow_html=True)

# ─── All tickers ──────────────────────────────────────────────────────────────
all_selected = {**kr_selected, **us_selected}
all_tickers = list(all_selected.values()) + list(idx_selected.values())

if not all_selected and not idx_selected:
    st.info("사이드바에서 종목을 선택해 주세요.")
    st.stop()

# ─── Fetch Data ───────────────────────────────────────────────────────────────
with st.spinner("데이터 불러오는 중..."):
    price_data = fetch_price_data(all_tickers, period)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 수익률 비교", "📈 차트 분석", "🏆 성과 랭킹", "🔍 종목 상세"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – 수익률 비교
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    # ── Current Price Cards ──
    st.markdown('<div class="section-header">실시간 시세</div>', unsafe_allow_html=True)

    all_card_items = [(n, t, "KR") for n, t in kr_selected.items()] + \
                     [(n, t, "US") for n, t in us_selected.items()]

    if all_card_items:
        cols = st.columns(min(len(all_card_items), 4))
        for i, (name, ticker, region) in enumerate(all_card_items):
            info = fetch_current_info(ticker)
            col_idx = i % 4
            with cols[col_idx]:
                chg_class = "metric-change-pos" if info["change_pct"] >= 0 else "metric-change-neg"
                arrow = "▲" if info["change_pct"] >= 0 else "▼"
                flag = '<span class="flag-tag flag-kr">KR</span>' if region == "KR" else '<span class="flag-tag flag-us">US</span>'
                price_str = format_price(info["price"], info["currency"]) if info["price"] else "N/A"
                chg_str = f"{arrow} {abs(info['change_pct']):.2f}%"
                st.markdown(f"""
                <div class="metric-card">
                  <div class="metric-ticker">{ticker} {flag}</div>
                  <div class="metric-name">{name}</div>
                  <div class="metric-price">{price_str}</div>
                  <div class="{chg_class}">{chg_str}</div>
                </div>
                """, unsafe_allow_html=True)
            if col_idx == 3 and i < len(all_card_items) - 1:
                cols = st.columns(min(len(all_card_items) - i - 1, 4))

    # ── Normalized Return Chart ──
    st.markdown('<div class="section-header">정규화 수익률 비교 (시작일 = 100)</div>', unsafe_allow_html=True)

    fig_norm = go.Figure()
    color_palette_kr = ["#4facfe", "#00f2fe", "#a8edea", "#81ecec", "#74b9ff", "#0984e3", "#6c5ce7", "#00cec9"]
    color_palette_us = ["#fd79a8", "#ff6b6b", "#ffd166", "#f9ca24", "#e17055", "#d63031", "#fab1a0", "#ff7675"]
    color_idx = ["#a29bfe", "#b2bec3"]

    kr_cnt = us_cnt = idx_cnt = 0

    for name, ticker in kr_selected.items():
        if ticker in price_data:
            ret = compute_returns(price_data[ticker])
            if ret:
                fig_norm.add_trace(go.Scatter(
                    x=ret["normalized"].index,
                    y=ret["normalized"].values,
                    name=f"🇰🇷 {name}",
                    line=dict(color=color_palette_kr[kr_cnt % len(color_palette_kr)], width=2),
                    hovertemplate=f"<b>{name}</b><br>%{{x|%Y-%m-%d}}<br>수익률: %{{y:.1f}}<extra></extra>"
                ))
                kr_cnt += 1

    for name, ticker in us_selected.items():
        if ticker in price_data:
            ret = compute_returns(price_data[ticker])
            if ret:
                fig_norm.add_trace(go.Scatter(
                    x=ret["normalized"].index,
                    y=ret["normalized"].values,
                    name=f"🇺🇸 {name}",
                    line=dict(color=color_palette_us[us_cnt % len(color_palette_us)], width=2),
                    hovertemplate=f"<b>{name}</b><br>%{{x|%Y-%m-%d}}<br>수익률: %{{y:.1f}}<extra></extra>"
                ))
                us_cnt += 1

    for name, ticker in idx_selected.items():
        if ticker in price_data:
            ret = compute_returns(price_data[ticker])
            if ret:
                fig_norm.add_trace(go.Scatter(
                    x=ret["normalized"].index,
                    y=ret["normalized"].values,
                    name=f"📊 {name}",
                    line=dict(color=color_idx[idx_cnt % 2], width=2, dash="dot"),
                    hovertemplate=f"<b>{name}</b><br>%{{x|%Y-%m-%d}}<br>수익률: %{{y:.1f}}<extra></extra>"
                ))
                idx_cnt += 1

    fig_norm.add_hline(y=100, line_dash="dash", line_color="rgba(255,255,255,0.2)", line_width=1)

    fig_norm.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.8)",
        font=dict(family="Noto Sans KR, sans-serif", color="#c0cce0"),
        height=450,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            bgcolor="rgba(13,19,34,0.85)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1,
            font=dict(size=11),
            orientation="v",
            x=1.01, y=1,
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)", ticksuffix=""),
        hovermode="x unified",
    )
    st.plotly_chart(fig_norm, use_container_width=True)

    # ── Return Summary Table ──
    st.markdown('<div class="section-header">기간 수익률 요약</div>', unsafe_allow_html=True)

    summary_rows = []
    for name, ticker in {**kr_selected, **us_selected, **idx_selected}.items():
        if ticker in price_data:
            ret = compute_returns(price_data[ticker])
            if ret:
                region = "🇰🇷 한국" if ticker in kr_selected.values() else ("🇺🇸 미국" if ticker in us_selected.values() else "📊 지수")
                info = fetch_current_info(ticker)
                summary_rows.append({
                    "종목명": name,
                    "지역": region,
                    "현재가": format_price(info["price"], info["currency"]),
                    "전일대비": format_change(info["change"], info["change_pct"]),
                    f"{period_label} 수익률": f"{ret['total_return']:+.2f}%",
                    "시작가": format_price(ret["first"], info["currency"]),
                    "현재가(기간)": format_price(ret["last"], info["currency"]),
                })

    if summary_rows:
        df_summary = pd.DataFrame(summary_rows)
        st.dataframe(
            df_summary,
            use_container_width=True,
            hide_index=True,
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – 차트 분석
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">개별 주가 차트</div>', unsafe_allow_html=True)

    chart_items = [(n, t, "KR") for n, t in kr_selected.items()] + \
                  [(n, t, "US") for n, t in us_selected.items()]

    if not chart_items:
        st.info("사이드바에서 종목을 선택해 주세요.")
    else:
        selected_chart = st.selectbox(
            "차트 볼 종목 선택",
            [f"{'🇰🇷' if r == 'KR' else '🇺🇸'} {n}" for n, _, r in chart_items],
        )
        sel_idx_chart = [f"{'🇰🇷' if r == 'KR' else '🇺🇸'} {n}" for n, _, r in chart_items].index(selected_chart)
        sel_name, sel_ticker, sel_region = chart_items[sel_idx_chart]

        if sel_ticker in price_data:
            series = price_data[sel_ticker]
            info = fetch_current_info(sel_ticker)

            # Candle data
            t_obj = yf.Ticker(sel_ticker)
            hist_full = t_obj.history(period=period)

            rows_count = 2 if show_volume else 1
            row_heights = [0.75, 0.25] if show_volume else [1.0]
            fig_candle = make_subplots(
                rows=rows_count, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=row_heights,
            )

            # Candlestick
            fig_candle.add_trace(go.Candlestick(
                x=hist_full.index,
                open=hist_full["Open"],
                high=hist_full["High"],
                low=hist_full["Low"],
                close=hist_full["Close"],
                name="OHLC",
                increasing_line_color="#00e676",
                decreasing_line_color="#ff4d6d",
                increasing_fillcolor="#00e676",
                decreasing_fillcolor="#ff4d6d",
            ), row=1, col=1)

            # Moving Averages
            if show_ma:
                for ma, color in [(20, "#ffd166"), (60, "#a29bfe")]:
                    if len(hist_full) >= ma:
                        ma_series = hist_full["Close"].rolling(ma).mean()
                        fig_candle.add_trace(go.Scatter(
                            x=ma_series.index, y=ma_series.values,
                            name=f"MA{ma}",
                            line=dict(color=color, width=1.5),
                        ), row=1, col=1)

            # Volume
            if show_volume and "Volume" in hist_full.columns:
                colors_vol = ["#00e676" if c >= o else "#ff4d6d"
                              for c, o in zip(hist_full["Close"], hist_full["Open"])]
                fig_candle.add_trace(go.Bar(
                    x=hist_full.index,
                    y=hist_full["Volume"],
                    name="거래량",
                    marker_color=colors_vol,
                    opacity=0.7,
                ), row=2, col=1)

            fig_candle.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(17,24,39,0.8)",
                font=dict(family="Noto Sans KR", color="#c0cce0"),
                height=500,
                margin=dict(l=10, r=10, t=30, b=10),
                xaxis_rangeslider_visible=False,
                showlegend=True,
                legend=dict(bgcolor="rgba(13,19,34,0.85)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
                title=dict(
                    text=f"{sel_name} ({sel_ticker}) — {period_label} 캔들 차트",
                    font=dict(size=14, color="#f0f4ff"),
                    x=0.01,
                ),
            )
            for r in range(1, rows_count + 1):
                fig_candle.update_xaxes(gridcolor="rgba(255,255,255,0.05)", row=r, col=1)
                fig_candle.update_yaxes(gridcolor="rgba(255,255,255,0.05)", row=r, col=1)

            st.plotly_chart(fig_candle, use_container_width=True)

            # Stats row
            c1, c2, c3, c4 = st.columns(4)
            ret = compute_returns(series)
            with c1:
                st.metric("현재가", format_price(info["price"], info["currency"]))
            with c2:
                st.metric("전일대비", format_change(info["change"], info["change_pct"]),
                          delta=f"{info['change_pct']:.2f}%")
            with c3:
                st.metric(f"{period_label} 수익률", f"{ret.get('total_return', 0):+.2f}%" if ret else "N/A")
            with c4:
                high = hist_full["High"].max()
                low = hist_full["Low"].min()
                st.metric(f"{period_label} 고/저",
                          format_price(high, info["currency"]),
                          delta=f"저: {format_price(low, info['currency'])}")

        # Index Chart
        if idx_selected:
            st.markdown('<div class="section-header">지수 차트</div>', unsafe_allow_html=True)
            fig_idx = go.Figure()
            for i, (name, ticker) in enumerate(idx_selected.items()):
                if ticker in price_data:
                    fig_idx.add_trace(go.Scatter(
                        x=price_data[ticker].index,
                        y=price_data[ticker].values,
                        name=name,
                        fill="tozeroy",
                        fillcolor=f"rgba(79,172,254,{0.05 + i * 0.03})",
                        line=dict(color=color_idx[i % 2], width=2),
                    ))
            fig_idx.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(17,24,39,0.8)",
                font=dict(family="Noto Sans KR", color="#c0cce0"),
                height=300,
                margin=dict(l=10, r=10, t=20, b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                legend=dict(bgcolor="rgba(13,19,34,0.85)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1),
            )
            st.plotly_chart(fig_idx, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – 성과 랭킹
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">수익률 랭킹</div>', unsafe_allow_html=True)

    ranking = []
    for name, ticker in {**kr_selected, **us_selected}.items():
        if ticker in price_data:
            ret = compute_returns(price_data[ticker])
            if ret:
                info = fetch_current_info(ticker)
                region = "🇰🇷" if ticker in kr_selected.values() else "🇺🇸"
                ranking.append({
                    "name": name,
                    "ticker": ticker,
                    "region": region,
                    "return": ret["total_return"],
                    "currency": info["currency"],
                    "price": info["price"],
                })

    if ranking:
        ranking.sort(key=lambda x: x["return"], reverse=True)

        # Bar chart
        fig_bar = go.Figure()
        colors_bar = ["#00e676" if r["return"] >= 0 else "#ff4d6d" for r in ranking]
        fig_bar.add_trace(go.Bar(
            x=[r["return"] for r in ranking],
            y=[f"{r['region']} {r['name']}" for r in ranking],
            orientation="h",
            marker_color=colors_bar,
            text=[f"{r['return']:+.2f}%" for r in ranking],
            textposition="outside",
            textfont=dict(size=11, family="Space Mono"),
        ))
        fig_bar.add_vline(x=0, line_color="rgba(255,255,255,0.3)", line_width=1)
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.8)",
            font=dict(family="Noto Sans KR", color="#c0cce0"),
            height=max(300, len(ranking) * 42),
            margin=dict(l=10, r=80, t=20, b=10),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", ticksuffix="%"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            showlegend=False,
            title=dict(text=f"{period_label} 수익률 순위", font=dict(size=13, color="#f0f4ff"), x=0.01),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Scatter: Return vs Volatility
        st.markdown('<div class="section-header">리스크-수익률 분포</div>', unsafe_allow_html=True)

        scatter_data = []
        for r in ranking:
            if r["ticker"] in price_data:
                series = price_data[r["ticker"]]
                daily_ret = series.pct_change().dropna()
                vol = daily_ret.std() * np.sqrt(252) * 100  # annualized vol %
                scatter_data.append({**r, "volatility": vol})

        if scatter_data:
            fig_scatter = go.Figure()
            for item in scatter_data:
                color = "#4facfe" if item["region"] == "🇰🇷" else "#fd79a8"
                fig_scatter.add_trace(go.Scatter(
                    x=[item["volatility"]],
                    y=[item["return"]],
                    mode="markers+text",
                    marker=dict(size=14, color=color, opacity=0.85,
                                line=dict(width=1, color="rgba(255,255,255,0.3)")),
                    text=[item["name"]],
                    textposition="top center",
                    textfont=dict(size=10),
                    name=f"{item['region']} {item['name']}",
                    showlegend=False,
                    hovertemplate=f"<b>{item['region']} {item['name']}</b><br>수익률: {item['return']:+.2f}%<br>변동성: {item['volatility']:.1f}%<extra></extra>"
                ))
            fig_scatter.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)")
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(17,24,39,0.8)",
                font=dict(family="Noto Sans KR", color="#c0cce0"),
                height=420,
                margin=dict(l=10, r=10, t=30, b=10),
                xaxis=dict(title="연환산 변동성 (%)", gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(title=f"{period_label} 수익률 (%)", gridcolor="rgba(255,255,255,0.05)"),
                title=dict(text="리스크(변동성) vs 수익률", font=dict(size=13, color="#f0f4ff"), x=0.01),
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        # KR vs US comparison
        col_kr, col_us = st.columns(2)
        kr_rets = [r for r in ranking if r["region"] == "🇰🇷"]
        us_rets = [r for r in ranking if r["region"] == "🇺🇸"]

        with col_kr:
            st.markdown('<div class="section-header">🇰🇷 한국 수익률 순위</div>', unsafe_allow_html=True)
            for i, r in enumerate(sorted(kr_rets, key=lambda x: x["return"], reverse=True)):
                medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"
                color = "#00e676" if r["return"] >= 0 else "#ff4d6d"
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);'>"
                    f"<span>{medal} {r['name']}</span>"
                    f"<span style='color:{color};font-family:Space Mono;font-weight:700;'>{r['return']:+.2f}%</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        with col_us:
            st.markdown('<div class="section-header">🇺🇸 미국 수익률 순위</div>', unsafe_allow_html=True)
            for i, r in enumerate(sorted(us_rets, key=lambda x: x["return"], reverse=True)):
                medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"
                color = "#00e676" if r["return"] >= 0 else "#ff4d6d"
                st.markdown(
                    f"<div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);'>"
                    f"<span>{medal} {r['name']}</span>"
                    f"<span style='color:{color};font-family:Space Mono;font-weight:700;'>{r['return']:+.2f}%</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 – 종목 상세
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">종목 상세 정보</div>', unsafe_allow_html=True)

    all_detail = {**kr_selected, **us_selected}
    if not all_detail:
        st.info("사이드바에서 종목을 선택해 주세요.")
    else:
        detail_name = st.selectbox("종목 선택", list(all_detail.keys()), key="detail_sel")
        detail_ticker = all_detail[detail_name]
        detail_region = "KR" if detail_ticker in kr_selected.values() else "US"

        info = fetch_current_info(detail_ticker)
        try:
            t_obj = yf.Ticker(detail_ticker)
            full_info = t_obj.info
        except Exception:
            full_info = {}

        col_a, col_b = st.columns([2, 1])

        with col_a:
            flag_html = '<span class="flag-tag flag-kr">KR</span>' if detail_region == "KR" else '<span class="flag-tag flag-us">US</span>'
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:1rem;">
              <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-family:Space Mono;font-size:1rem;font-weight:700;">{detail_ticker}</span>
                {flag_html}
              </div>
              <div style="font-size:1.5rem;font-weight:700;margin-bottom:4px;">{info['name']}</div>
              <div style="font-size:2rem;font-family:Space Mono;font-weight:700;">{format_price(info['price'], info['currency'])}</div>
              <div class="{'metric-change-pos' if info['change_pct'] >= 0 else 'metric-change-neg'}" style="font-size:1rem;margin-top:4px;">
                {'▲' if info['change_pct'] >= 0 else '▼'} {abs(info['change_pct']):.2f}%
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Metrics grid
            mc = full_info.get("marketCap")
            pe = full_info.get("trailingPE")
            pb = full_info.get("priceToBook")
            div_yield = full_info.get("dividendYield")
            beta = full_info.get("beta")
            week52_high = full_info.get("fiftyTwoWeekHigh")
            week52_low = full_info.get("fiftyTwoWeekLow")
            avg_vol = full_info.get("averageVolume")

            def fmt_num(v, suffix="", prefix="", decimals=2):
                if v is None: return "N/A"
                if v >= 1e12: return f"{prefix}{v/1e12:.1f}T{suffix}"
                if v >= 1e9: return f"{prefix}{v/1e9:.1f}B{suffix}"
                if v >= 1e6: return f"{prefix}{v/1e6:.1f}M{suffix}"
                return f"{prefix}{v:,.{decimals}f}{suffix}"

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("시가총액", fmt_num(mc))
            m2.metric("P/E (TTM)", f"{pe:.1f}x" if pe else "N/A")
            m3.metric("P/B", f"{pb:.2f}x" if pb else "N/A")
            m4.metric("배당수익률", f"{div_yield*100:.2f}%" if div_yield else "N/A")

            m5, m6, m7, m8 = st.columns(4)
            m5.metric("베타", f"{beta:.2f}" if beta else "N/A")
            m6.metric("52주 최고", format_price(week52_high, info["currency"]))
            m7.metric("52주 최저", format_price(week52_low, info["currency"]))
            m8.metric("평균거래량", fmt_num(avg_vol, decimals=0))

        with col_b:
            # Sector / Industry
            sector = full_info.get("sector", "")
            industry = full_info.get("industry", "")
            country = full_info.get("country", "")
            exchange = full_info.get("exchange", "")
            employees = full_info.get("fullTimeEmployees")
            website = full_info.get("website", "")

            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-ticker">기업 정보</div>
              <div style="margin-top: 10px; font-size: 0.85rem; line-height: 2;">
                {'<div><span style="color:#7a8ab0;">섹터</span> &nbsp; ' + sector + '</div>' if sector else ''}
                {'<div><span style="color:#7a8ab0;">업종</span> &nbsp; ' + industry + '</div>' if industry else ''}
                {'<div><span style="color:#7a8ab0;">국가</span> &nbsp; ' + country + '</div>' if country else ''}
                {'<div><span style="color:#7a8ab0;">거래소</span> &nbsp; ' + exchange + '</div>' if exchange else ''}
                {'<div><span style="color:#7a8ab0;">직원수</span> &nbsp; ' + f"{employees:,}" + '명</div>' if employees else ''}
                {'<div style="margin-top:8px;"><a href="' + website + '" target="_blank" style="color:#4facfe;font-size:0.8rem;">🔗 공식 웹사이트</a></div>' if website else ''}
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Business summary
            summary = full_info.get("longBusinessSummary", "")
            if summary:
                st.markdown(f"""
                <div class="metric-card" style="margin-top:0.8rem;">
                  <div class="metric-ticker">사업 개요</div>
                  <div style="font-size:0.78rem;color:#9aa8c0;line-height:1.6;margin-top:8px;max-height:200px;overflow-y:auto;">
                    {summary[:500]}{'...' if len(summary) > 500 else ''}
                  </div>
                </div>
                """, unsafe_allow_html=True)

        # Correlation heatmap
        if len(all_selected) >= 2:
            st.markdown('<div class="section-header">상관관계 히트맵</div>', unsafe_allow_html=True)

            returns_df = pd.DataFrame()
            for name, ticker in all_selected.items():
                if ticker in price_data:
                    returns_df[name] = price_data[ticker].pct_change()

            if len(returns_df.columns) >= 2:
                corr = returns_df.corr()
                fig_corr = go.Figure(data=go.Heatmap(
                    z=corr.values,
                    x=corr.columns.tolist(),
                    y=corr.index.tolist(),
                    colorscale=[[0, "#ff4d6d"], [0.5, "#1a2235"], [1, "#4facfe"]],
                    zmin=-1, zmax=1,
                    text=[[f"{v:.2f}" for v in row] for row in corr.values],
                    texttemplate="%{text}",
                    textfont=dict(size=10),
                    hovertemplate="%{y} vs %{x}: %{z:.3f}<extra></extra>",
                ))
                fig_corr.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(17,24,39,0.8)",
                    font=dict(family="Noto Sans KR", color="#c0cce0"),
                    height=max(350, len(corr) * 50),
                    margin=dict(l=10, r=10, t=20, b=10),
                    title=dict(text=f"{period_label} 일간 수익률 기준 상관관계", font=dict(size=13, color="#f0f4ff"), x=0.01),
                )
                st.plotly_chart(fig_corr, use_container_width=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:0.75rem;color:#4a5a80;padding:0.5rem 0;'>"
    "📊 데이터 출처: Yahoo Finance (yfinance) &nbsp;|&nbsp; "
    "본 대시보드는 투자 참고용이며 투자 권유가 아닙니다. "
    "</div>",
    unsafe_allow_html=True
)
