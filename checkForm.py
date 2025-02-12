import streamlit as st

# Create a form with st.form
with st.form(key='my_form'):
    # Add text input box for name (compulsory field)
    name = st.text_input('Enter your name:')
    if not name:
        st.error('Please enter your name')

    # Add number input box for age
    age = st.number_input('Enter your age:', min_value=0)

    # Add radio buttons for selecting a gender
    gender = st.radio('Select your gender:', ('Male', 'Female', 'Other'))

    # Add a submit button
    submit_button = st.form_submit_button(label='Submit')

# Check if the form was submitted
if submit_button:
    # Validate if name is provided
    if not name:
        st.error('Name is a required field!')  # Show error if name is empty
    else:
        st.write(f'Name: {name}')
        st.write(f'Age: {age}')
        st.write(f'Gender: {gender}')
