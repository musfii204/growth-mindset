import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import io

# Setup Streamlit app
st.set_page_config(page_title="Data Sweeper", layout='wide')
st.title("📂 Data Sweeper")
st.write("🔄 Transform your files between CSV and Excel format with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("📤 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"🚨 Unsupported file type: {file_ext}")
            continue

        # Show uploaded file details
        st.write(f"**📁 Uploaded File:** {file.name} ({file.size} bytes)")
        
        # Preview of DataFrame
        st.write("👀 **Preview of Data:**")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠️ Data Cleaning")
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"🗑 Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates removed successfully!")

        with col2:
            if st.button(f"📌 Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing values filled with column mean!")

        # Column selection
        st.subheader("📋 Select Columns to Convert")
        selected_columns = st.multiselect("📌 Choose columns to keep", df.columns, default=df.columns)

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox("📉 Show Visualization"):
            numeric_cols = df.select_dtypes(include="number").columns
            if len(numeric_cols) >= 2:
                fig, ax = plt.subplots()
                df[numeric_cols].hist(ax=ax)
                st.pyplot(fig)
            else:
                st.warning("⚠️ Not enough numerical columns to visualize.")

        # Conversion options
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio("🔁 Convert file to:", ["📄 CSV", "📊 Excel"])

        if st.button("🚀 Convert & Download"):
            buffer = io.BytesIO()
            df_selected = df[selected_columns]

            if conversion_type == "📊 Excel":
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df_selected.to_excel(writer, index=False, sheet_name="Sheet1")
                buffer.seek(0)
                st.download_button(label="⬇️ Download Excel File", data=buffer, file_name="converted_file.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            elif conversion_type == "📄 CSV":
                csv_data = df_selected.to_csv(index=False).encode("utf-8")
                st.download_button(label="⬇️ Download CSV File", data=csv_data, file_name="converted_file.csv", mime="text/csv")

