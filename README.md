# ⚡ Energiepipeline – ENTSO-E → Snowflake

Dieses Projekt demonstriert eine **End-to-End Data Engineering Pipeline** mit direktem Praxisbezug zur Energiebranche.  
Die Pipeline lädt Daten von der **ENTSO-E Transparency Platform API** (Stromnetz-Daten Europa), transformiert sie in Python und speichert sie in **Snowflake**, einem modernen Cloud Data Warehouse.  

Damit lassen sich **tägliche Energieprognosen und -verbräuche** automatisiert analysieren – ein Szenario, wie es in Energieunternehmen real zum Einsatz kommt.

---

## 🎯 Zielsetzung

- Aufbau einer **ETL-Pipeline**: *Extract → Transform → Load*  
- Datenquelle: **ENTSO-E Transparency Platform API** (Day-Ahead Total Load Forecast für DE-LU)  
- Speicherung: **Snowflake Data Warehouse**  
- Möglichkeit zu **Monitoring, Reporting und Dashboards**  
- Praxisnaher **Cloud Data Engineering Use Case**  

---

## 🛠️ Technologien

- **Python** (requests, pandas, ElementTree, snowflake-connector, python-dotenv)  
- **Snowflake** (Cloud Data Warehouse)  
- **SQL** (Analysen und Aggregationen)  
- **GitHub** (Versionierung & Projekt-Doku)  

---

## ✅ Aktueller Stand

- Erfolgreiche Verbindung zur **ENTSO-E API** (Dokumenttyp A65: Day-Ahead Load Forecast).  
- Daten im **15-Minuten-Raster (MW)** werden in **Pandas DataFrames** transformiert.  
- Automatischer Upload nach **Snowflake** in Tabelle `RAW_DATA.LOAD_DATA`.  
- Erste SQL-Abfragen möglich: **Tagesdurchschnitt, Peak-Load, Zeitreihen**.  

---

## 📊 Praxisbezug

Energieversorger und Netzbetreiber müssen täglich **Prognosen (Forecast)** und **tatsächliche Lastwerte (Actual Load)** vergleichen, um:  
- die **Netzstabilität** sicherzustellen,  
- **Beschaffungsstrategien** am Strommarkt zu optimieren,  
- **Erzeugung & Verbrauch** in Einklang zu bringen.  

Dieses Projekt bildet genau diesen realen Use Case ab – mit **Cloud-Technologien**, wie sie auch in Unternehmen eingesetzt werden.  

---

## 🚀 Nächste Schritte

- Integration von **Actual Load (A63)** für Forecast-vs-Actual-Vergleiche  
- Automatisierung (Task Scheduler oder Airflow)  
- Logging & Monitoring  
- Visualisierung als **Streamlit Dashboard**  
- Abweichungsanalyse Forecast vs. Actual  

---

👤 Author: **iliasel**
