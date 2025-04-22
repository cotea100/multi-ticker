import streamlit as st
import yfinance as yf
import pandas as pd
from io import StringIO

st.title("멀티 티커 주가 다운로드 (공통 기간 필터 강제 적용)")

st.markdown("입력한 티커들의 공통 데이터 기간 내에서만 다운로드가 가능합니다.")

tickers_input = st.text_input("티커 입력 (쉼표로 구분):")
if tickers_input:
    tickers = tickers_input.replace(" ", "").split(",")
    available_periods = {}
    all_data = {}

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker)
            hist = info.history(period="max")
            if hist.empty:
                st.warning(f"{ticker} 데이터가 없습니다.")
                continue
            available_periods[ticker] = (hist.index.min(), hist.index.max())
            all_data[ticker] = hist
        except Exception as e:
            st.error(f"{ticker} 처리 중 오류: {e}")

    if len(available_periods) < len(tickers):
        st.warning("일부 티커는 데이터를 가져올 수 없어 제외되었습니다.")

    if available_periods:
        common_start = max(v[0] for v in available_periods.values())
        common_end = min(v[1] for v in available_periods.values())
        st.success(f"공통 검색 가능 기간: {common_start.date()} ~ {common_end.date()}")

        start_date = st.date_input("시작일", min_value=common_start.date(), max_value=common_end.date(), value=common_start.date())
        end_date = st.date_input("종료일", min_value=common_start.date(), max_value=common_end.date(), value=common_end.date())

        if start_date >= common_start.date() and end_date <= common_end.date() and start_date < end_date:
            combined = []
            for ticker in tickers:
                df = all_data[ticker].loc[str(start_date):str(end_date)]
                df = df[["Close"]].rename(columns={"Close": ticker})
                combined.append(df)

            if combined:
                result = pd.concat(combined, axis=1).dropna()
                result = result.reset_index().rename(columns={"Date": "Date"})

                csv = result.to_csv(index=False).encode("utf-8-sig")
                file_name = f"{'_'.join(tickers)}_{start_date}_{end_date}.csv"
                st.download_button("CSV 다운로드", data=csv, file_name=file_name, mime="text/csv")
            else:
                st.error("선택한 구간에 병합 가능한 데이터가 없습니다.")
        else:
            st.error("시작일과 종료일은 공통 보유기간 내에 있어야 하며, 종료일은 시작일보다 늦어야 합니다.")
