import pandas as pd

def transform_generation_data(input_path="C:/Users/ilias/OneDrive/Desktop/ProjektData/data/Realisierte_Erzeugung_202509030000_202509140000_Stunde.csv",
                              output_path="../data/cleaned_generation.csv"):
    # CSV einlesen
    df = pd.read_csv(input_path, sep=";", encoding="utf-8")

    # Datum-Spalten umwandeln
    df["Datum von"] = pd.to_datetime(df["Datum von"], dayfirst=True, errors="coerce")
    df["Datum bis"] = pd.to_datetime(df["Datum bis"], dayfirst=True, errors="coerce")

    # Alle Spalten mit "MWh" bereinigen
    for col in df.columns:
        if "MWh" in col:
            df[col] = (df[col].astype(str)
                                .str.replace(".", "", regex=False)  # Punkte (Tausender) raus
                                .str.replace(",", ".", regex=False)  # Komma → Punkt
                                .str.replace("-", "0", regex=False) # "-" → 0
                                .astype(float))

    # Neue CSV speichern
    df.to_csv(output_path, index=False, sep=";")
    print(f"✅ Daten bereinigt und gespeichert: {output_path}")

if __name__ == "__main__":
    transform_generation_data()
