import streamlit as st
import yfinance as yf
import pandas as pd
from io import StringIO

st.title("멀티 티커 주가 다운로드 (공통 보유기간 제한 적용)")

st.markdown("여러 티커에 대해 공통된 주가 보유 기간 내에서 데이터를 다운로드할 수 있습니다.")

# 티커 입력
tickers_input = st.text_input("티커 입력 (쉼표로 구분):")
if tickers_input:
    tickers = tickers_input.replace(" ", "").split(",")
    available_periods = {}
    all_data = {}

    # 개별 티커의 데이터 보유 범위 확인
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

    if available_periods:
        # 공통 검색 가능 기간 계산
        common_start = max(v[0] for v in available_periods.values())
        common_end = min(v[1] for v in available_periods.values())

        st.success(f"공통 검색 가능 기간: {common_start.date()} ~ {common_end.date()}")

        # 날짜 선택
        start_date = st.date_input("시작일", min_value=common_start.date(), max_value=common_end.date(), value=common_start.date())
        end_date = st.date_input("종료일", min_value=common_start.date(), max_value=common_end.date(), value=common_end.date())

        if start_date < end_date:
            # 데이터 다운로드 및 병합
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
                st.error("선택한 구간에 다운로드할 데이터가 없습니다.")
        else:
            st.warning("종료일은 시작일보다 이후여야 합니다.")
