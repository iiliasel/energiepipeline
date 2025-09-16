import requests
import pandas as pd
import snowflake.connector
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Dein Token
TOKEN = "e975acd6-663a-4e71-a270-e5e239ee2c36"

# API URL
URL = "https://web-api.tp.entsoe.eu/api"

# Zeitraum: heute bis morgen (UTC)
# Beispiel: 1 Tag (15. Sept 2025)
yesterday = "202409010000"
today = "202409020000"


params = {
    "securityToken": TOKEN,
    "documentType": "A44",
    "in_Domain": "10Y1001A1001A83F",
    "out_Domain": "10Y1001A1001A83F",
    "periodStart": "202509150000",
    "periodEnd": "202509160000"
}

# API Request
response = requests.get(URL, params=params)
response.raise_for_status()

# XML parsen
root = ET.fromstring(response.text)
ns = {"ns": "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0"}

records = []
for ts in root.findall(".//ns:TimeSeries", ns):
    for period in ts.findall(".//ns:Period", ns):
        start = period.find("ns:timeInterval/ns:start", ns).text
        for point in period.findall("ns:Point", ns):
            position = int(point.find("ns:position", ns).text)
            price = float(point.find("ns:price.amount", ns).text)
            timestamp = datetime.fromisoformat(start) + timedelta(hours=position-1)
            records.append((timestamp, price, "ENTSO-E"))

df = pd.DataFrame(records, columns=["DATETIME", "VALUE", "SOURCE"])

print(df.head())  # Kontrolle

# --- Snowflake Upload ---
conn = snowflake.connector.connect(
    user="iiliasel",
    password="Marokko.030285",
    account="zvadzkt-jt47151",   # z. B. ab12345.eu-central-1
    warehouse="COMPUTE_WH",
    database="ENERGIEPIPELINE",
    schema="RAW_DATA"
)
cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO PRICES (DATETIME, VALUE, SOURCE) VALUES (%s, %s, %s)",
        (row["DATETIME"], row["VALUE"], row["SOURCE"])
    )

conn.commit()
cur.close()
conn.close()

print(response.url)
print(response.text[:500])

