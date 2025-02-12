import streamlit as st
import pandas as pd


def main():
    st.title("Excel File Uploader")

    # File uploader
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            # Read the Excel file
            df = pd.read_excel(uploaded_file)

            # Display the dataframe
            st.write("### Preview of Uploaded File:")
            st.dataframe(df)

            # Display basic statistics
            st.write("### Basic Statistics:")
            st.write(df.describe())

        except Exception as e:
            st.error(f"Error reading file: {e}")


if __name__ == "__main__":
    main()
