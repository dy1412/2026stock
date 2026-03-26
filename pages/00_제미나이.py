import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="Stock Insight Lite", layout="wide", initial_sidebar_state="expanded")

# 라이트 모드 전용 CSS (깔끔한 카드 스타일 및 폰트 설정)
st.markdown("""
    <style>
    /* 전체 배경색 및 폰트 */
    .main { background-color: #f8f9fa; color: #1e1e1e; }
    
    /* 메트릭 카드 스타일 */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #edf2f7;
    }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #edf2f7;
    }
    
    /* 제목 스타일 */
    h1 { color: #1a73e8; font-weight: 800; }
    h3 { color: #444746; font-weight: 600; }
    
    /* 버튼 스타일 커스텀 */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #1a73e8;
        color: white;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 메인 헤더
st.title("📊 Global Stock Monitor")
st.caption("한국 및 미국 주요 주식의 수익률을 실시간으로 비교합니다.")
st.write("---")

# 사이드바 설정
with st.sidebar:
    st.subheader("⚙️ 분석 설정")
    ticker_input = st.text_input("종목 입력 (쉼표 구분)", "AAPL, NVDA, 005930.KS, 000660.KS")
    tickers = [t.strip().upper() for t in ticker_input.split(",")]
    
    period = st.select_slider(
        "분석 기간 선택",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        value="1y"
    )
    
    show_spy = st.toggle("S&P 500 지수와 비교", value=True)
    st.divider()
    st.info("💡 팁: 한국 주식은 종목코드 뒤에 .KS(코스피)나 .KQ(코스닥)를 붙여주세요.")

# 데이터 로딩 함수 (캐싱)
@st.cache_data
def get_stock_data(ticker_list, period_str, add_spy):
    target_list = ticker_list.copy()
    if add_spy:
        target_list.append("SPY")
    
    df = yf.download(target_list, period=period_str)['Close']
    return df

try:
    with st.spinner('데이터를 불러오는 중입니다...'):
        raw_data = get_stock_data(tickers, period, show_spy)
        
    # 누적 수익률 계산
    returns_df = (raw_data / raw_data.iloc[0] - 1) * 100

    # 1. 상단 요약 정보 (Metrics)
    st.subheader("✨ Today's Market")
    cols = st.columns(len(tickers))
    
    for i, ticker in enumerate(tickers):
        with cols[i]:
            current_val = raw_data[ticker].iloc[-1]
            prev_val = raw_data[ticker].iloc[-2]
            change_pct = ((current_val - prev_val) / prev_val) * 100
            
            unit = "₩" if ".KS" in ticker or ".KQ" in ticker else "$"
            st.metric(
                label=ticker, 
                value=f"{unit}{current_val:,.0f}" if unit == "₩" else f"{unit}{current_val:,.2f}", 
                delta=f"{change_pct:.2f}%"
            )

    st.markdown("###")

    # 2. 메인 수익률 차트
    c1, c2 = st.columns([4, 1])
    
    with c1:
        st.subheader("📈 수익률 추이")
        fig = go.Figure()
        
        for col in returns_df.columns:
            # S&P 500은 강조되지 않게 회색 점선으로 처리
            if col == "SPY":
                fig.add_trace(go.Scatter(x=returns_df.index, y=returns_df[col], name="S&P 500", 
                                         line=dict(color='#bdc3c7', width=2, dash='dot')))
            else:
                fig.add_trace(go.Scatter(x=returns_df.index, y=returns_df[col], name=col, 
                                         line=dict(width=3), hovertemplate='%{y:.2f}%'))

        fig.update_layout(
            hovermode="x unified",
            plot_bgcolor='white',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=True, gridcolor='#f0f2f6'),
            yaxis=dict(showgrid=True, gridcolor='#f0f2f6', ticksuffix="%")
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("🏆 순위")
        # 마지막 수익률 기준 내림차순 정렬
        final_rets = returns_df.iloc[-1].sort_values(ascending=False)
        for rank, (name, val) in enumerate(final_rets.items(), 1):
            color = "#e74c3c" if val < 0 else "#2ecc71"
            st.markdown(f"**{rank}. {name}**")
            st.markdown(f"<h4 style='color:{color}; margin-top:-10px;'>{val:.1f}%</h4>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"데이터를 불러올 수 없습니다. 티커 명칭을 확인해 주세요! (오류: {e})")
