#import google.generativeai as genai
#from IPython.display import Markdown
import time
import streamlit as st
import pandas as pd
import re
import openpyxl as XL
import PIL.Image
from PIL import Image

#sample_file_2 = PIL.Image.open('withMarksBothTable.png')
user_input=""
import google.generativeai as genai
genai.configure(api_key="your_api")
# Choose a Gemini model.
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
#prompt2 = "just return the alpha numeric REGISTER NUMBER"
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        # Display the dataframe
        st.write("### Preview of Uploaded File:")
        st.dataframe(df)

        # Display basic statistics
        st.write("### Basic Statistics:")
        st.write(df.describe())

    except Exception as e:
        st.error(f"Error reading file: {e}")
####################################################PREPARING THE PROMPT#################################################################
prompt = "extract the marks only and also exclude total but also combine the PART A & PART B marks but in PART B consider total only, exclude everything else and give me raw text"
#response1 = model.generate_content([sample_file_2, prompt])
#response2 = model.generate_content([sample_file_2, prompt2])
#####################################################################################################################################################################################
#Markdown(response.text)
cond = True
while cond:
    # Capture photo
    st.write("### Capture Photo:")
    captured_image = st.camera_input("Take a picture")
    if captured_image:
        Cimage = Image.open(captured_image)
        st.image(Cimage, caption="Captured Image")
        response1 = model.generate_content([Cimage, prompt])
        time.sleep(3)
        response2 = model.generate_content([Cimage,"just return the alpha numeric register number, it would be like 732923AMR003"])
        raw_text = response1.text
        st.write(raw_text)
        st.write(response2.text)
        print(response2.text)
        marks_list = []
        for line in raw_text.splitlines():
            line = line.strip()
            if line:
                # If there is a comma, sum the values and add the result
                if "," in line:
                    marks_list.append(sum(int(mark) for mark in line.split(",")))
                else:
                    marks_list.append(int(line))

        user_input = response2.text
        print(user_input)

    def search_register_number_substring(user_input):
        """
        Asks the user for text input, extracts the substring 'AMR003',
        and searches for it in the 'Register Number' column.
        Returns the integer-based index of the matching row if found, otherwise -1.
        """

        user_input = user_input.strip()
        #user_input = input("Enter the text to search for in the 'Register Number' column: ")
        user_input = user_input.upper()
        # Extract the relevant substring (e.g., 'AMR003') using regular expressions
        match = re.search(r'AMR\d+', user_input)  # Assuming 'AMR' followed by digits is the key part
        if match:
            substring = match.group(0)
            try:
                # Find the index using 'str.contains' to check for substring presence
                index = df[df['Register Number'].str.contains(substring, na=False)].index[0]
                print(f"{index}")
                return index
            except IndexError:
                print(f"Register number containing '{substring}' not found.")
                return -1

        else:
            print("Invalid register number format. Please include 'AMR' followed by digits.")
        return -1


    result_index = search_register_number_substring(user_input)
    df.iloc[result_index, 3:] = marks_list
# Output the list
    #print(marks_list)
    if st.button("END"):
        cond = False
#print(raw_text)
# Process the raw text to extract marks
######################################################################################################################################################################################

#marks_list



################ Call the function to search and get the index


print(df)
print("*"*19)
