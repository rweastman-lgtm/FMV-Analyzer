import os
import pandas as pd

def scrape_and_cache_risk_data():
    os.makedirs("data", exist_ok=True)

    # Replace this with real scraping logic later
    flood_data = pd.DataFrame({
        "ZIP": ["34202", "34211", "34212"],
        "FloodZone": ["AE", "X", "VE"]
    })
    wind_data = pd.DataFrame({
        "ZIP": ["34202", "34211", "34212"],
        "WindZone": ["Zone III", "Zone IV", "Zone II"]
    })
    fire_data = pd.DataFrame({
        "ZIP": ["34202", "34211", "34212"],
        "FireRiskScore": [3, 2, 4]
    })

    flood_data.to_csv("data/fema_flood_zones_by_zip.csv", index=False)
    wind_data.to_csv("data/noaa_wind_zones_by_zip.csv", index=False)
    fire_data.to_csv("data/wildfire_risk_scores_by_zip.csv", index=False)def load_risk_tables():
    flood_df = pd.read_csv("data/fema_flood_zones_by_zip.csv")
    wind_df = pd.read_csv("data/noaa_wind_zones_by_zip.csv")
    fire_df = pd.read_csv("data/wildfire_risk_scores_by_zip.csv")
    return flood_df, wind_df, fire_df

def zip_to_risk(zip_code):
    if not zip_code:
        return {"flood_zone": "X", "wind_zone": "Zone III", "fire_risk_score": 3}

    flood_df, wind_df, fire_df = load_risk_tables()
    flood_match = flood_df.loc[flood_df["ZIP"] == zip_code, "FloodZone"]
    wind_match = wind_df.loc[wind_df["ZIP"] == zip_code, "WindZone"]
    fire_match = fire_df.loc[fire_df["ZIP"] == zip_code, "FireRiskScore"]

    flood_zone = flood_match.values[0] if not flood_match.empty else "X"
    wind_zone = wind_match.values[0] if not wind_match.empty else "Zone III"
    fire_score = fire_match.values[0] if not fire_match.empty else 3

    return {
        "flood_zone": flood_zone,
        "wind_zone": wind_zone,
        "fire_risk_score": fire_score
    }


