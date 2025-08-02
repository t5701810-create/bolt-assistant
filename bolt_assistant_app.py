import streamlit as st
import pandas as pd
import re

# Load the bolt database
@st.cache_data
def load_data():
    df = pd.read_excel("Screw_Assembly_User 1 (2) (1).xlsx", sheet_name="Screw_Table_User", skiprows=3)
    df = df.dropna(subset=["Screw diameter (mm)", "Quality class"])
    df["Screw diameter (mm)"] = df["Screw diameter (mm)"].astype(str).str.strip()
    df["Quality class"] = df["Quality class"].astype(str).str.strip()
    return df

df = load_data()

st.title("🔩 Bolt AI Assistant")
st.write("Ask a question like: `Torque for M8 bolt, class 8.8`")

query = st.text_input("Your question")

if query:
    # Simple regex to extract diameter and class
    match = re.search(r"M?(\d+(\.\d+)?)\D+?(6\.8|8\.8|10\.9|12\.9)", query)
    if match:
        diameter = match.group(1)
        quality = match.group(3)

        filtered = df[(df["Screw diameter (mm)"].astype(str) == diameter) &
                      (df["Quality class"].astype(str) == quality)]

        if not filtered.empty:
            row = filtered.iloc[0]
            st.success(f"Results for M{diameter}, class {quality}:")
            st.write(f"**Thread:** {row['Thread (mm)']}")
            st.write(f"**Traction Force:** {row['Traction']} N")
            st.write(f"**Shear Force:** {row['Shear']} N")
            st.write(f"**Torque:** Min {row['Min torque from Norm']} Nm | Nominal {row['Nominal (used for database)']} Nm | Max {row['Max torque from Norm']} Nm")
            st.write(f"**Nominal Force:** {row['Nominal (CONLO database)']} N")
        else:
            st.error("No matching data found for that size and class.")
    else:
        st.warning("Please enter a valid query like: 'Torque for M10, class 10.9'")
