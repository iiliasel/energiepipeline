import requests
import pandas as pd
import snowflake.connector
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, UTC

# --- ENTSO-E API ---
TOKEN = "e975acd6-663a-4e71-a270-e5e239ee2c36"
URL = "https://web-api.tp.entsoe.eu/api"

# --- Zeitraum: heute 00:00 – morgen 00:00 (UTC) ---
today = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
tomorrow = today + timedelta(days=1)

# --- Bidding Zone: Deutschland-Luxemburg ---
DOMAIN = "10Y1001A1001A83F"

def fetch_entsoe_forecast(start, end, domain):
    """ Holt Day-Ahead Total Load Forecast (A65) """
    params = {
        "securityToken": TOKEN,
        "documentType": "A65",
        "processType": "A01",  # Day-ahead
        "outBiddingZone_Domain": domain,
        "periodStart": start.strftime("%Y%m%d%H%M"),
        "periodEnd": end.strftime("%Y%m%d%H%M"),
    }

    response = requests.get(URL, params=params)
    print("➡️ Request URL:", response.url)
    response.raise_for_status()

    root = ET.fromstring(response.text)

    # Prüfen ob nur Acknowledgement zurückkommt
    if "Acknowledgement_MarketDocument" in root.tag:
        print(f"⚠️ Keine Daten im Zeitraum {start} - {end}")
        print(response.text[:500])
        return pd.DataFrame()

    records = []
    for ts in root.findall(".//{*}TimeSeries"):
        for period in ts.findall(".//{*}Period"):
            start_time = period.find(".//{*}start").text
            for point in period.findall(".//{*}Point"):
                position = int(point.find(".//{*}position").text)
                value = float(point.find(".//{*}quantity").text)
                # 15-Minuten-Raster
                timestamp = datetime.fromisoformat(start_time) + timedelta(minutes=15*(position-1))
                records.append((timestamp, value, "A65"))

    df = pd.DataFrame(records, columns=["DATETIME", "VALUE", "TYPE"])
    print(f"✅ A65: {len(df)} Datensätze geladen")
    return df


# --- Forecast für heute laden ---
df = fetch_entsoe_forecast(today, tomorrow, DOMAIN)
print(df.head(20))

# --- Upload nach Snowflake ---
if not df.empty:
    # Zeitstempel als String für sicheren Upload
    df["DATETIME"] = df["DATETIME"].astype(str)

    conn = snowflake.connector.connect(
        user="iiliasel",
        password="Marokko.030285",
        account="zvadzkt-jt47151",
        warehouse="COMPUTE_WH",
        database="ENERGIEPIPELINE",
        schema="RAW_DATA"
    )
    cur = conn.cursor()

    insert_sql = "INSERT INTO LOAD_DATA (DATETIME, VALUE, TYPE) VALUES (%s, %s, %s)"
    cur.executemany(insert_sql, df.values.tolist())

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Upload nach Snowflake erfolgreich!")
else:
    print("⚠️ Keine Daten zum Hochladen gefunden.")
