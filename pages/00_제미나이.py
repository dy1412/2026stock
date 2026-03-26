import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. 페이지 설정
st.set_page_config(page_title="Stock Insight Pro", layout="wide")

# 2. 클린 라이트 테마 CSS
st.markdown("""
    <style>
    .main { background-color: #f9fbfd; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e6ed;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .stPlotlyChart { background-color: #ffffff; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Global Stock Comparison")
st.caption("실시간 주가 데이터 기반 수익률 분석 대시보드")

# 3. 사이드바 구성
with st.sidebar:
    st.header("🔍 분석 설정")
    # 기본 종목 설정 (한국/미국 혼합)
    default_tickers = "AAPL, NVDA, 005930.KS, 000660.KS"
    input_tickers = st.text_input("종목 티커 (쉼표 구분)", default_tickers)
    
    # 공백 제거 및 리스트 변환
    tickers = [t.strip().upper() for t in input_tickers.split(",") if t.strip()]
    
    period = st.selectbox("조회 기간", ["3mo", "6mo", "1y", "2y", "5y"], index=2)
    st.divider()
    st.write("📌 **Tip**")
    st.caption("KOSPI: .KS (예: 005930.KS)")
    st.caption("KOSDAQ: .KQ (예: 247540.KQ)")

# 4. 데이터 로드 및 오류 방지 처리
@st.cache_data(ttl=3600)
def fetch_data(ticker_list, p):
    # group_by='column'을 사용하여 멀티인덱스 구조를 안정화
    df = yf.download(ticker_list, period=p, interval='1d')['Close']
    
    # 종목이 1개일 경우 Series로 반환될 수 있어 DataFrame으로 변환
    if isinstance(df, pd.Series):
        df = df.to_frame()
        df.columns = ticker_list
        
    # 데이터가 비어있는 컬럼 제거
    df = df.dropna(how='all', axis=1)
    return df

if tickers:
    try:
        data = fetch_data(tickers, period)
        
        if data.empty:
            st.warning("데이터를 가져오지 못했습니다. 티커명을 확인해주세요.")
        else:
            # 수익률 계산 (NaN 제거 후 첫 번째 유효값 기준)
            returns = (data / data.iloc[0] - 1) * 100

            # --- 레이아웃 배치 ---
            
            # 상단 메트릭
            st.subheader("📍 현재가 요약")
            m_cols = st.columns(len(data.columns))
            for i, col in enumerate(data.columns):
                current_price = data[col].iloc[-1]
                prev_price = data[col].iloc[-2]
                change = ((current_price - prev_price) / prev_price) * 100
                
                # 한국 주식은 ₩, 미국 주식은 $ 표시
                symbol = "₩" if ".K" in col else "$"
                m_cols[i].metric(label=col, value=f"{symbol}{current_price:,.2f}", delta=f"{change:.2f}%")

            st.write("---")

            # 하단 차트 및 순위
            col_left, col_right = st.columns([3, 1])

            with col_left:
                st.subheader("📊 누적 수익률 비교")
                fig = go.Figure()
                for col in returns.columns:
                    fig.add_trace(go.Scatter(
                        x=returns.index, 
                        y=returns[col], 
                        name=col,
                        line=dict(width=2.5),
                        hovertemplate=f'<b>{col}</b><br>수익률: %{{y:.2f}}%<extra></extra>'
                    ))
                
                fig.update_layout(
                    hovermode="x unified",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    xaxis=dict(showgrid=True, gridcolor='#f0f2f6'),
                    yaxis=dict(showgrid=True, gridcolor='#f0f2f6', ticksuffix="%"),
                    margin=dict(l=20, r=20, t=20, b=20),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_right:
                st.subheader("🏆 Performance Rank")
                latest_ret = returns.iloc[-1].sort_values(ascending=False)
                for rank, (name, val) in enumerate(latest_ret.items(), 1):
                    color = "#d63031" if val < 0 else "#00b894"
                    st.markdown(f"**{rank}. {name}**")
                    st.markdown(f"<span style='color:{color}; font-size: 20px; font-weight: bold;'>{val:.2f}%</span>", unsafe_allow_html=True)
                    st.write("")

    except Exception as e:
        st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")
else:
    st.info("비교할 주식 티커를 입력해주세요.")
