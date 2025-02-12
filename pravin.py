import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io
import base64

# Configure Gemini API
genai.configure(api_key="AIzaSyDfWc6N20t1uUayDWEjHae1c75428eyqIU")
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

st.title("Excel File & Camera Input Processing")

# Upload Excel File
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("### Preview of Uploaded File:")
    st.dataframe(df)

st.write("### Capture Photo:")
captured_image = st.camera_input("Take a picture")

if captured_image:
    image = Image.open(captured_image)

    # Convert Image to Bytes for Gemini API
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()

    # Send to Gemini Model
    response1 = model.generate_content([img_bytes, "extract the marks only and combine PART A & PART B"])
    response2 = model.generate_content([img_bytes, "just return the alphanumeric register number"])

    # Display results
    st.image(image, caption="Captured Image")
    st.write("### Extracted Marks:")
    st.write(response1.text)

    st.write("### Extracted Register Number:")
    st.write(response2.text)
