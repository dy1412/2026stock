import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="글로벌 주식 비교 앱", layout="wide")

st.title("📈 한국 vs 미국 주식 수익률 비교")
st.markdown("원하는 주식을 선택하면 수익률과 차트를 한눈에 비교할 수 있습니다.")

# 주요 주식 리스트
stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA"
}

selected = st.multiselect("비교할 주식을 선택하세요", list(stocks.keys()), default=["삼성전자", "Apple"])

# 기간 선택
period = st.selectbox("기간 선택", ["1mo", "3mo", "6mo", "1y", "3y", "5y"], index=3)

if selected:
    df = pd.DataFrame()

    for name in selected:
        ticker = stocks[name]
        data = yf.download(ticker, period=period)

        if not data.empty:
            df[name] = data["Close"]

    if not df.empty:
        # 수익률 계산
        returns = (df / df.iloc[0] - 1) * 100

        # 📊 차트
        st.subheader("📊 가격 추이")
        fig, ax = plt.subplots()
        df.plot(ax=ax)
        ax.set_ylabel("가격")
        ax.grid()
        st.pyplot(fig)

        # 📈 수익률 차트
        st.subheader("📈 수익률 (%)")
        fig2, ax2 = plt.subplots()
        returns.plot(ax=ax2)
        ax2.set_ylabel("수익률 (%)")
        ax2.grid()
        st.pyplot(fig2)

        # 📋 수익률 표
        st.subheader("📋 최종 수익률 비교")
        final_returns = returns.iloc[-1].sort_values(ascending=False)
        st.dataframe(final_returns.to_frame(name="수익률 (%)"))

    else:
        st.warning("데이터를 불러오지 못했습니다.")
else:
    st.info("주식을 선택해주세요.")
