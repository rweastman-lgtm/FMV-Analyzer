import streamlit as st
import pandas as pd
import datetime

# ----------------------------- #
# Real Builder Cost Table
# ----------------------------- #
builder_cost_table = {
    "Cresswind": (175, 250), "Windward": (165, 240), "Indigo": (170, 225),
    "Grand Park": (170, 240), "Savanna": (170, 230), "Arbor Grande": (170, 245),
    "Palm Grove": (175, 230), "Star Farms": (175, 240), "Del Webb LWR": (180, 260),
    "Catalina": (185, 245), "Mallory Park": (185, 265), "Greenbrook": (165, 215),
    "Sweetwater": (170, 230), "Esplanade at Azario": (185, 275), "Skye Ranch": (185, 265),
    "Rosedale": (175, 240), "Greyhawk Landing": (175, 235), "Stillwater": (160, 210),
    "Lakewood National": (170, 225)
}

def get_cost_per_sq_ft(community, level):
    low, high = builder_cost_table.get(community, (190, 190))
    if level == "Lower":
        return low
    elif level == "Upper":
        return high
    else:
        return round((low + high) / 2)

# ----------------------------- #
# FMV Calculation Logic
# ----------------------------- #
def calculate_fmv(address, sq_ft, build_year, is_builder_origin, fmv_method, community, cost_level, sold_price=None):
    cost_per_sq_ft = get_cost_per_sq_ft(community, cost_level)
    base_cost = sq_ft * cost_per_sq_ft

    covid_stripout = {
        2020: 1.08, 2021: 1.22, 2022: 1.34, 2023: 1.42, 2024: 1.47, 2025: 1.00
    }
    growth_multiplier = {
        2015: 1.7908, 2016: 1.6870, 2017: 1.5927, 2018: 1.5061, 2019: 1.4185,
        2020: 1.3382, 2021: 1.2625, 2022: 1.1910, 2023: 1.1236, 2024: 1.06, 2025: 1.00
    }
    builder_multiplier = {
        2020: 1.239, 2021: 1.035, 2022: 0.889, 2023: 0.791, 2024: 0.721, 2025: 1.00
    }

    if fmv_method == "Sold Price-Based Estimate" and sold_price:
        if build_year <= 2019:
            fmv = sold_price * growth_multiplier.get(build_year, 1.00)
        else:
            strip = covid_stripout.get(build_year, 1.00)
            adjusted_price = sold_price / strip
            fmv = adjusted_price * growth_multiplier.get(build_year, 1.00)
    else:
        if build_year in [2024, 2025] and is_builder_origin:
            fmv = base_cost * 1.15
        elif is_builder_origin:
            fmv = base_cost * builder_multiplier.get(build_year, 1.00)
        else:
            strip = covid_stripout.get(build_year, 1.00)
            adjusted_price = base_cost / strip
            fmv = adjusted_price * growth_multiplier.get(build_year, 1.00)

    risk_flag = "⚠️" if fmv < 275000 else ""
    return round(fmv, -3), risk_flag

# ----------------------------- #
# Single Address Mode
# ----------------------------- #
def single_address_mode():
    st.subheader("🔍 Single Address FMV Analysis")
    address = st.text_input("Enter Property Address")
    sq_ft = st.number_input("Square Footage", min_value=500, max_value=10000)
    build_year = st.selectbox("Build Year", list(range(2015, 2026)))
    is_builder_origin = st.checkbox("Builder-Originated Listing")
    community = st.selectbox("Community", list(builder_cost_table.keys()))
    cost_level = st.radio("Cost Level", ["Lower", "Midpoint", "Upper"])
    fmv_method = st.radio("Choose FMV Method", ["Cost-Based Estimate", "Sold Price-Based Estimate"])
    sold_price = None
    if fmv_method == "Sold Price-Based Estimate":
        sold_price = st.number_input("Enter Most Recent Sold Price", min_value=50000)

    if st.button("Analyze"):
        if address and sq_ft:
            fmv, risk = calculate_fmv(address, sq_ft, build_year, is_builder_origin, fmv_method, community, cost_level, sold_price)
            st.success(f"Corrected FMV: ${fmv:,.0f} {risk}")
        else:
            st.warning("Please enter all required fields.")

# ----------------------------- #
# Batch Upload Mode
# ----------------------------- #
def batch_upload_mode():
    st.subheader("📂 Batch FMV Analysis via CSV")
    uploaded_file = st.file_uploader("Upload CSV with columns: Address, SqFt, BuildYear, BuilderOrigin, FMVMethod, SoldPrice, Community, CostLevel", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        required_cols = {"Address", "SqFt", "BuildYear", "BuilderOrigin", "FMVMethod", "SoldPrice", "Community", "CostLevel"}
        if not required_cols.issubset(df.columns):
            st.error(f"CSV must contain columns: {', '.join(required_cols)}")
            return

        results = []
        for _, row in df.iterrows():
            fmv, risk = calculate_fmv(
                row["Address"], row["SqFt"], row["BuildYear"], row["BuilderOrigin"],
                row["FMVMethod"], row["Community"], row["CostLevel"], row["SoldPrice"]
            )
            results.append({"Address": row["Address"], "Corrected FMV": fmv, "Risk Flag": risk})

        result_df = pd.DataFrame(results)
        st.dataframe(result_df)
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results as CSV", data=csv, file_name="fmv_results.csv", mime="text/csv")

# ----------------------------- #
# Main App Layout
# ----------------------------- #
def main():
    st.set_page_config(page_title="FMV Analyzer", layout="centered")
    st.title("🏠 FMV Analyzer")
    st.markdown("Analyze property values stripped of inflation and builder distortion.")
    mode = st.radio("Choose Mode", ["Single Address", "Batch Upload"])
    if mode == "Single Address":
        single_address_mode()
    else:
        batch_upload_mode()
    st.markdown("---")
    st.caption(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
