import os
import pandas as pd

# Cache the scraped data once per session
@st.cache_data
def get_risk_tables():
    return scrape_risk_data()

def zip_to_risk(zip_code):
    flood_df, wind_df, fire_df = get_risk_tables()

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

