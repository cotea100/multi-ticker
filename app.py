import streamlit as st
import yfinance as yf
import pandas as pd
from io import StringIO

st.title("Yahoo Finance 멀티 티커 주가 다운로드")

st.markdown("""
- 쉼표(,)로 구분된 여러 티커를 입력하세요. (예: AAPL,MSFT,GOOGL)
- 시작일과 종료일을 선택하세요.
- 주가를 병합해서 하나의 CSV 파일로 다운로드할 수 있습니다.
""")

tickers_input = st.text_input("티커 입력 (쉼표로 구분):")
start_date = st.date_input("시작일")
end_date = st.date_input("종료일")

if st.button("데이터 다운로드"):
    if not tickers_input:
        st.warning("티커를 입력해주세요.")
    else:
        tickers = tickers_input.replace(" ", "").split(",")
        all_data = []
        for ticker in tickers:
            try:
                df = yf.download(ticker, start=start_date, end=end_date)
                if df.empty:
                    st.warning(f"{ticker} 데이터가 없습니다.")
                    continue
                df = df[['Close']].rename(columns={'Close': ticker})
                all_data.append(df)
            except Exception as e:
                st.error(f"{ticker} 다운로드 오류: {e}")

        if all_data:
            merged = pd.concat(all_data, axis=1).reset_index()
            merged = merged.rename(columns={'Date': 'Date'})
            # 다운로드 버튼
            csv = merged.to_csv(index=False).encode('utf-8-sig')
            file_name = f"{'_'.join(tickers)}_{start_date}_{end_date}.csv"
            st.download_button(
                label="CSV 다운로드",
                data=csv,
                file_name=file_name,
                mime="text/csv"
            )
        else:
            st.error("다운로드 가능한 데이터가 없습니다.")
