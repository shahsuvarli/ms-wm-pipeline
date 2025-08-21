import yfinance as yf
import pandas as pd
import boto3
from io import StringIO
from datetime import datetime

# --- CONFIG ---
BUCKET_NAME = "ms-market-risk-bucket"
TICKERS = ["AAPL", "MSFT", "EURUSD=X"]
REGION = "eu-central-1"

session = boto3.Session(
    region_name=REGION,
    aws_access_key_id=env.ACCESS_KEY,
    aws_secret_access_key=env.SECRET_KEY
)
s3 = session.client("s3")


def fetch_data():
    data = {}
    for ticker in TICKERS:
        df = yf.download(ticker, period="5d")
        df.reset_index(inplace=True)

        # Flattened output
        df_out = pd.DataFrame({
            "SYMBOL": [ticker] * len(df),
            "DT": df["Date"].values.flatten(),
            "CLOSE": df["Close"].values.flatten(),
            "CURRENCY": ["USD"] * len(df),
            "SOURCE": ["yfinance"] * len(df),
            "_INGESTED_AT": [datetime.utcnow()] * len(df)
        })

        data[ticker] = df_out
    return data


def upload_to_s3(data):
    today = datetime.today().strftime("%Y/%m/%d")
    for ticker, df in data.items():
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        key = f"prices/{ticker}/{today}/data.csv"
        s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=csv_buffer.getvalue())
        print(f"Uploaded {ticker} → s3://{BUCKET_NAME}/{key}")


if __name__ == "__main__":
    data = fetch_data()
    upload_to_s3(data)
