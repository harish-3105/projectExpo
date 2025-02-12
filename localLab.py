
import time
import streamlit as st
import pandas as pd
import re
import openpyxl as XL
import io
from PIL import Image
import google.generativeai as genai

# Configure API Key (Ensure secrets are set up)
#api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else st.text_input("Enter API Key", type="password")

genai.configure(api_key="GOOGLE_API")

# Choose Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# Streamlit UI
st.title("Student Marks Extraction & Update")
# Get number of absentees
absentees = st.number_input("Enter No of Absentees", min_value=0, max_value=59, value=0, key="unique_number_input_key")
# Calculate total students present
total = 59 - int(absentees)
# Initialize session state for progress tracking
if "progress" not in st.session_state:
    st.session_state.progress = 0

# Upload Excel File
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        if "df" not in st.session_state:
            df = pd.read_excel(uploaded_file)
            st.session_state.df = df  # Store in session_state
        else:
            df = st.session_state.df  # Retrieve stored DataFrame

        # Display uploaded data
        st.write("### Preview of Uploaded File:")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error reading file: {e}")

# Function to search for register number
def search_register_number(user_input):
    user_input = user_input.strip().upper()
    match = re.search(r'\d+AMR\d+', user_input)  # Extract alphanumeric register number
    if match:
        substring = match.group(0)
        try:
            index = df[df['Register Number'].astype(str).str.contains(substring, na=False)].index[0]
            return index
        except IndexError:
            return -1
    return -1
# Display progress bar
progress_bar = st.progress(st.session_state.progress / total)
if st.button("NEXT"):
    if st.session_state.progress < total:
        st.session_state.progress += 1  # Increase progress
        progress_bar.progress(st.session_state.progress / total)  # Update bar
    else:
        st.success("Process Completed! ✅")
# Camera Capture
st.write("### Capture Photo:")
#captured_image = st.camera_input("Take a picture", key="unique_camera_input_key")
captured_image = st.file_uploader("Choose a file", type=["jpg", "png"])
if captured_image:
    Cimage = Image.open(captured_image)
    st.image(Cimage, caption="Captured Image")

    # Convert image to byte buffer
    img_buffer = io.BytesIO()
    Cimage.save(img_buffer, format="JPEG")
    img_bytes = img_buffer.getvalue()

    # Send image to Gemini API
    response1 = model.generate_content([Cimage, "Extract only the marks. Exclude total. Combine PART A & PART B marks, but in PART B consider total only. Provide raw text and return integers only like (eg: '2\n2\n2\n2\n2\n2\n2\n2\n2\n2\n2\n15\n15')"])
    response2 = model.generate_content([Cimage, "Just return the alphanumeric register number(e.g., 732923AMR003)"])

    raw_text = response1.text.strip()
    register_number = response2.text.strip()
    register_number = register_number[4:]
    # Display extracted results
    st.write("### Extracted Marks:")
    st.write(raw_text)
    st.write("### Extracted Register Number:")
    st.write(register_number)

    if register_number:
        index = search_register_number(register_number)

        if index != -1:
            # Process marks into a list
            marks_list = []
            for line in raw_text.splitlines():
                line = line.strip()
                if line:
                    if "," in line:
                        marks_list.append(sum(int(mark) for mark in line.split(",")))
                    else:
                        marks_list.append(int(line))

            # Update DataFrame
            df.iloc[index, 3:] = marks_list
            st.session_state.df = df  # Save updated DataFrame

            st.success(f"Marks updated for {register_number}!")
            progress_bar = st.progress(st.session_state.progress / total)
            if st.session_state.progress < total:
                st.session_state.progress += 1  # Increase progress
                progress_bar.progress(st.session_state.progress / total)  # Update bar
            else:
                st.success("Process Completed! ✅")
            st.dataframe(df)
        else:
            st.error("Register number not found in uploaded Excel file.")

# Download Updated Excel
if "df" in st.session_state:
    output = io.BytesIO()
    st.session_state.df.to_excel(output, index=False, engine='openpyxl')
    st.download_button(
        label="Download Updated File",
        data=output.getvalue(),
        file_name="Updated_Marks.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
