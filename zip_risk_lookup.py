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
import requests

def address_to_flood_zone_free(address):
    # Step 1: Geocode using US Census
    geo_url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    geo_params = {
        "address": address,
        "benchmark": "Public_AR_Current",
        "format": "json"
    }

    geo_resp = requests.get(geo_url, params=geo_params)
    if geo_resp.status_code != 200:
        raise ValueError(f"Census geocoder failed with status {geo_resp.status_code}")

    try:
        geo_data = geo_resp.json()
        coords = geo_data["result"]["addressMatches"][0]["coordinates"]
        lat = coords["y"]
        lon = coords["x"]
    except (IndexError, KeyError, ValueError):
        raise ValueError("Geocoding failed for address.")

    # Step 2: Query FEMA NFHL
    fema_url = "https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer/28/query"
    fema_params = {
        "geometry": f"{lon},{lat}",
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "FLD_ZONE",
        "returnGeometry": "false",
        "f": "json"
    }

    fema_resp = requests.get(fema_url, params=fema_params)
    if fema_resp.status_code != 200:
        raise ValueError(f"FEMA NFHL query failed with status {fema_resp.status_code}")

    try:
        fema_data = fema_resp.json()
        flood_zone = fema_data["features"][0]["attributes"]["FLD_ZONE"]
    except (IndexError, KeyError, ValueError):
        flood_zone = "X"  # Default fallback

    return flood_zone
