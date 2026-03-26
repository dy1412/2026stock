import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="한/미 주식 비교 대시보드", layout="wide")

st.title("📈 한/미 주요 주식 수익률 비교")
st.sidebar.header("설정")

# 1. 주식 선택 (사용자가 직접 입력하거나 리스트에서 선택)
default_tickers = ["AAPL", "TSLA", "005930.KS", "000660.KS", "NVDA", "035420.KS"]
tickers = st.sidebar.text_input(
    "티커 입력 (쉼표로 구분, 한국은 .KS 또는 .KQ 포함)", 
    value=", ".join(default_tickers)
).split(",")

tickers = [t.strip().upper() for t in tickers]

# 2. 기간 설정
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("시작일", datetime.now() - timedelta(days=365))
end_date = col2.date_input("종료일", datetime.now())

if st.sidebar.button("데이터 불러오기"):
    try:
        # 데이터 다운로드
        data = yf.download(tickers, start=start_date, end=end_date)['Close']
        
        if data.empty:
            st.error("데이터를 불러오지 못했습니다. 티커를 확인해주세요.")
        else:
            # 수익률 계산 (누적 수익률)
            returns = (data / data.iloc[0] - 1) * 100

            # 메트릭 섹션 (최신 종가 및 전일 대비)
            st.subheader("📍 실시간 주요 지표")
            cols = st.columns(len(tickers))
            for i, ticker in enumerate(tickers):
                if ticker in data.columns:
                    current_price = data[ticker].iloc[-1]
                    prev_price = data[ticker].iloc[-2]
                    delta = ((current_price - prev_price) / prev_price) * 100
                    cols[i].metric(ticker, f"{current_price:,.2f}", f"{delta:.2f}%")

            # 차트 섹션
            st.subheader("📊 누적 수익률 비교 (%)")
            fig = go.Figure()
            for ticker in returns.columns:
                fig.add_trace(go.Scatter(x=returns.index, y=returns[ticker], name=ticker, mode='lines'))
            
            fig.update_layout(
                hovermode="x unified",
                xaxis_title="날짜",
                yaxis_title="수익률 (%)",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)

            # 데이터 테이블
            with st.expander("데이터 상세보기"):
                st.dataframe(data.tail())

    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.info("왼쪽 사이드바에서 설정을 완료하고 '데이터 불러오기' 버튼을 눌러주세요.")
