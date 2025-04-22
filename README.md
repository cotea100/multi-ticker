# multi_ticker_downloader

Yahoo Finance에서 여러 티커의 주가를 병합해 CSV로 다운로드하는 Streamlit 앱입니다.

## 사용 방법

1. Streamlit Cloud에 이 저장소를 배포하세요.
2. 티커를 쉼표로 구분하여 입력 (예: AAPL,MSFT,GOOGL)
3. 날짜 선택 후 다운로드 버튼을 클릭하면 병합된 CSV 파일을 받을 수 있습니다.

## 필요 라이브러리

- streamlit
- yfinance
- pandas
