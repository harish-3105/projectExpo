#import streamlit as st
import pandas as pd
import re
#import openpyxl as XL
import PIL.Image
import google.generativeai as genai
genai.configure(api_key="AIzaSyDfWc6N20t1uUayDWEjHae1c75428eyqIU")
# Choose a Gemini model.
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

##################################################################################################################################################################################################

df = pd.read_excel("fsUP.xlsx")

sample_file = PIL.Image.open('withMarksBothTable.png')
#prompt2 = "just return the alpha numeric REGISTER NUMBER"
prompt = "extract the marks only and also exclude total but also combine the PART A & PART B marks but in PART B consider total only, exclude everything else and give me raw text"
response1 = model.generate_content([sample_file, prompt])

#Markdown(response.text)
raw_text = response1.text
#print(raw_text)
########################################################################################################################################################################################################################################################
# Process the raw text to extract marks
marks_list = []
for line in raw_text.splitlines():
    line = line.strip()
    if line:
        # If there is a comma, sum the values and add the result
        if "," in line:
            marks_list.append(sum(int(mark) for mark in line.split(",")))
        else:
            marks_list.append(int(line))

# Output the list
print(marks_list)
#marks_list
def search_register_number_substring():
    """
    Asks the user for text input, extracts the substring 'AMR003',
    and searches for it in the 'Register Number' column.
    Returns the integer-based index of the matching row if found, otherwise -1.
    """

    user_input = input("Enter the text to search for in the 'Register Number' column: ")
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

# Call the function to search and get the index
result_index = search_register_number_substring()
df.iloc[result_index, 3:] = marks_list
print(df)
