![Morgan Stanley Cover](https://media.licdn.com/dms/image/v2/D5616AQFBZXDmf40rOg/profile-displaybackgroundimage-shrink_350_1400/profile-displaybackgroundimage-shrink_350_1400/0/1722446660917?e=1758758400&v=beta&t=2q8YYMculjvT4o4QI7uvKRLmmTXJnDa7hAMv5W-FbIc)



# 📈 Market Risk Price Ingestion Pipeline

A cloud-native, multi-cloud data ingestion pipeline designed to extract financial market data from public APIs, store them in AWS S3, and load them into Snowflake via Azure Data Factory (ADF).

---

## 🧭 Architecture Overview

**Data Flow:**

```
[Python Script] → [AWS S3] → [Azure Data Factory] → [Snowflake Table: STG_PRICES]
```

---

## ⚙️ Technologies Used

| Component         | Tech                     |
|------------------|--------------------------|
| Ingestion Script | Python, yFinance         |
| Cloud Storage    | AWS S3                   |
| Orchestration    | Azure Data Factory       |
| Data Warehouse   | Snowflake                |
| IAM Integration  | AWS IAM Role + Snowflake |
| Security         | External ID, Role Trust  |

---

## 🗂 Repository Structure

```
ms-mrisk/

├── scripts/                      # Python script (ETL)
│   └── extract_to_s3.py
│
├── architecture_diagram.png
│
├── sql/                          # Snowflake DDLs
│   ├── create_stg_prices.sql
│   └── integration_setup.sql
│
├── .env                          # Local credentials (excluded from git)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── .gitignore
```

---

## 📁 S3 File Structure

Example path for `AAPL` on 2025-08-20:
```
s3://ms-market-risk-bucket/prices/AAPL/2025/08/20/data.csv
```

**Sample CSV:**
```csv
SYMBOL,DT,CLOSE,CURRENCY,SOURCE,_INGESTED_AT
AAPL,2025-08-19,233.33,USD,yfinance,2025-08-20 13:00:00
```

---

## ❄️ Snowflake Table Schema

```sql
CREATE OR REPLACE TABLE STG_PRICES (
  SYMBOL VARCHAR,
  DT DATE,
  CLOSE FLOAT,
  CURRENCY VARCHAR,
  SOURCE VARCHAR,
  _INGESTED_AT TIMESTAMP_NTZ
);
```

---

## 🛡 Security Setup

- **AWS IAM Role**: Custom role with `s3:GetObject` and trust policy
- **Snowflake External Integration**: Secure access to S3 using IAM role and external ID
- **ADF**: Uses managed identity or access key to bridge Snowflake with S3

---

## 🚀 How to Run

### Step 1: Extract and Upload to S3

```bash
cd scripts/
python extract_to_s3.py
```

### Step 2: Load via Azure Data Factory

- Trigger ADF pipeline manually or on schedule.
- ADF copies data from S3 to `STG_PRICES`.

### Step 3: Verify in Snowflake

```sql
SELECT * FROM STG_PRICES WHERE SYMBOL = 'AAPL';
```

---

## 🔍 Future Enhancements

- Parameterize extract script with `--symbol` and `--date`
- Add unit tests and logging
- Add dbt transformations after staging
- Add retry & alerting to ADF
- Add dashboards (e.g., Streamlit or Looker Studio)

---

## 📎 Credits

Built by **Elvin Shahsuvarli**  
For: Morgan Stanley Data Engineering Evaluation  
Project: Real-time Market Risk Data Platform
