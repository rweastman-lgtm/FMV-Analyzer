import streamlit as st
import pandas as pd
import datetime
import random

# -----------------------------
# Simulated FMV Calculation Logic
# -----------------------------
def calculate_fmv(address):
    # Placeholder logic for demonstration
    base_price = random.randint(250000, 450000)
    inflation_adjustment = -0.12  # stripping COVID-era inflation
    builder_markup = -0.08        # correcting builder distortion
    corrected_price = base_price * (1 + inflation_adjustment + builder_markup)
    risk_flag = "⚠️" if corrected_price < 275000 else ""
    return round(corrected_price, -3), risk_flag

# -----------------------------
# Single Address Input
# -----------------------------
def single_address_mode():
    st.subheader("🔍 Single Address FMV Analysis")
    address = st.text_input("Enter Property Address")
    if st.button("Analyze"):
        if address:
            fmv, risk = calculate_fmv(address)
            st.success(f"Corrected FMV: ${fmv:,.0f} {risk}")
        else:
            st.warning("Please enter a valid address.")

# -----------------------------
# Batch Upload Mode
# -----------------------------
def batch_upload_mode():
    st.subheader("📂 Batch FMV Analysis via CSV")
    uploaded_file = st.file_uploader("Upload CSV with 'Address' column", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "Address" not in df.columns:
            st.error("CSV must contain an 'Address' column.")
            return
        results = []
        for addr in df["Address"]:
            fmv, risk = calculate_fmv(addr)
            results.append({"Address": addr, "Corrected FMV": fmv, "Risk Flag": risk})
        result_df = pd.DataFrame(results)
        st.dataframe(result_df)

        # CSV Export
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Results as CSV", data=csv, file_name="fmv_results.csv", mime="text/csv")

# -----------------------------
# Main App Layout
# -----------------------------
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
