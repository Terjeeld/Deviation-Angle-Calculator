import streamlit as st
import pandas as pd
import math

st.title("Deviation Angle Calculator from MD and TVD")

st.markdown("""
Upload a XLSX file with two columns:
- **MD** (Measured Depth in meters)
- **TVD** (True Vertical Depth in meters)

The app will calculate the deviation angle between each consecutive pair of points.
""")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    st.write("📥 File uploaded!")

    try:
        df = pd.read_excel(uploaded_file)
        st.write("✅ Excel file read successfully!")
        st.write("Columns detected:", df.columns.tolist())
        st.dataframe(df.head())

        if "MD" not in df.columns or "TVD" not in df.columns:
            st.error("❌ Excel file must contain columns 'MD' and 'TVD'")
        else:
            df = df.sort_values("MD").reset_index(drop=True)
            results = []

            for i in range(1, len(df)):
                md1, tvd1 = df.loc[i - 1, "MD"], df.loc[i - 1, "TVD"]
                md2, tvd2 = df.loc[i, "MD"], df.loc[i, "TVD"]
                delta_md = md2 - md1
                delta_tvd = tvd2 - tvd1
                if delta_md != 0:
                    cos_theta = delta_tvd / delta_md
                    cos_theta = max(-1.0, min(1.0, cos_theta))
                    deviation_deg = math.degrees(math.acos(cos_theta))
                else:
                    deviation_deg = None
                results.append({
                    "Sample 1 MD": md1,
                    "Sample 1 TVD": tvd1,
                    "Sample 2 MD": md2,
                    "Sample 2 TVD": tvd2,
                    "ΔMD": delta_md,
                    "ΔTVD": delta_tvd,
                    "Deviation Angle (°)": round(deviation_deg, 2) if deviation_deg is not None else "Undefined"
                })

            results_df = pd.DataFrame(results)
            st.success("✅ Deviation angles calculated!")
            st.dataframe(results_df)

            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "deviation_results.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Error reading Excel file: {e}")
