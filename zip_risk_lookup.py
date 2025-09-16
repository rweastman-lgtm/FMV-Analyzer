import pandas as pd
import streamlit as st
import requests

# -----------------------------
# ZIP-Level Risk Tables
# -----------------------------
def scrape_risk_data():
    flood_df = pd.DataFrame({
        "ZIP": ["34202", "34211", "34212"],
        "FloodZone": ["AE", "X", "VE"]
    })
    wind_df = pd.DataFrame({
        "ZIP": ["34202", "34211", "34212"],
        "WindZone": ["Zone III", "Zone IV", "Zone II"]
    })
    fire_df = pd.DataFrame({
        "ZIP": ["34202", "34211", "34212"],
        "FireRiskScore": [3, 2, 4]
    })
    return flood_df, wind_df, fire_df

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

# -----------------------------
# Parcel-Level Flood Zone Lookup
# -----------------------------

def address_to_flood_zone_nfd(address, api_key):
    url = "https://api.nationalflooddata.com/v3/flood-zone"
    headers = {"X-API-KEY": "lwrhuFpefpCkMusBQIFC8X7yltzED9kkD3zgS2i0"}
    payload = {"address": address}

    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code != 200:
        raise ValueError(f"NFD API failed with status {resp.status_code}")

    try:
        data = resp.json()
    except ValueError:
        raise ValueError("NFD API returned invalid JSON.")

    flood_zone = data.get("fld_zone", "X")  # Default fallback
    return flood_zone

