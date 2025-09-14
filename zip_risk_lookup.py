import pandas as pd

def load_risk_tables():
    flood_df = pd.read_csv("data/fema_flood_zones_by_zip.csv")      # Zone X, AE, VE
    wind_df = pd.read_csv("data/noaa_wind_zones_by_zip.csv")        # Zone II–IV
    fire_df = pd.read_csv("data/wildfire_risk_scores_by_zip.csv")   # Score 1–5

    return flood_df, wind_df, fire_df

def zip_to_risk(zip_code):
    flood_df, wind_df, fire_df = load_risk_tables()

    flood_zone = flood_df.loc[flood_df["ZIP"] == zip_code, "FloodZone"].values[0]
    wind_zone = wind_df.loc[wind_df["ZIP"] == zip_code, "WindZone"].values[0]
    fire_score = fire_df.loc[fire_df["ZIP"] == zip_code, "FireRiskScore"].values[0]

    return {
        "flood_zone": flood_zone,
        "wind_zone": wind_zone,
        "fire_risk_score": fire_score
    }
