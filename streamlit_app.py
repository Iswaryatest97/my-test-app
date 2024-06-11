# import altair as alt
# import numpy as np
# import pandas as pd
# import streamlit as st

# """
# # Welcome to Streamlit!

# Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
# If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
# forums](https://discuss.streamlit.io).

# In the meantime, below is an example of what you can do with just a few lines of code:
# """

# num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
# num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

# indices = np.linspace(0, 1, num_points)
# theta = 2 * np.pi * num_turns * indices
# radius = indices

# x = radius * np.cos(theta)
# y = radius * np.sin(theta)

# df = pd.DataFrame({
#     "x": x,
#     "y": y,
#     "idx": indices,
#     "rand": np.random.randn(num_points),
# })

# st.altair_chart(alt.Chart(df, height=700, width=700)
#     .mark_point(filled=True)
#     .encode(
#         x=alt.X("x", axis=None),
#         y=alt.Y("y", axis=None),
#         color=alt.Color("idx", legend=None, scale=alt.Scale()),
#         size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
#     ))


# import streamlit as st
# from openai_App import ask_gpt 
# #import simpleCalc
# # Custom CSS to style the chat input
# custom_css = """
# <style>
# /* Example of customizing input boxes */
# .st-emotion-cache-arzcut {
#     padding-bottom : 15px;
# }
# </style>
# """

# # Inject the custom CSS into the Streamlit app
# st.markdown(custom_css, unsafe_allow_html=True)

# # message = st.chat_message("assistant")
# # message.write("Hello human")

# prompt = st.chat_input("Say something")

# messages=[
#     {"role": "system", "content": "Hi, How can I assist you?"},
# ]

# reply = ask_gpt(prompt, messages)
# messages.append({
#     "role": "assistant", "content": reply
# })
# print(reply)

import streamlit as st
from openai_App import getEnvironmentDataByKey
import requests

from simple_salesforce import Salesforce, SalesforceAuthenticationFailed

consumer_key = getEnvironmentDataByKey("CONSUMER_KEY")
consumer_secret = getEnvironmentDataByKey("CONSUMER_SECRET")
token_url = getEnvironmentDataByKey("AUTH_TOKEN_URL") # OAuth 2.0 token endpoint
grant_type = getEnvironmentDataByKey("GRANT_TYPE")

print("consumer_key***"+consumer_key)
print("consumer_secret***"+consumer_secret)
print("token_url***"+token_url)

if not consumer_key or not consumer_secret or not token_url:
    raise ValueError("Salesforce credentials are not set in environment variables")

# Payload for token request
payload = {
    'grant_type': grant_type,
    'client_id': consumer_key,
    'client_secret': consumer_secret
}

# Request the access token
response = requests.post(token_url, data=payload)
response_data = response.json()

if response.status_code != 200:
    raise Exception(f"Error obtaining access token: {response_data}")

# Access token
access_token = response_data['access_token']
instance_url = response_data['instance_url']

try:
    # Authenticate with Salesforce
    sf = Salesforce(instance_url=instance_url, session_id=access_token)
    # sf = Salesforce(username=username, password=password, consumer_key=consumer_key, consumer_secret=consumer_secret)
    #sf = Salesforce(username=username, password=combined_password_token, security_token=security_token)
    print("Authentication successful")
except SalesforceAuthenticationFailed as e:
    print(f"***Authentication failed: {e}")
    raise

# Function to create a case in Salesforce
def create_salesforce_case(subject, description, origin, status):
    case_data = {
        'Subject': subject,
        'Description': description,
        'Origin': origin,
        'Status': status,
    }
    case = sf.Case.create(case_data)
    return case

# Streamlit app
st.title('Salesforce Case Creation App')

# Form to enter case details
with st.form('case_form'):
    subject = st.text_input('Subject')
    description = st.text_area('Description')
    origin = st.selectbox('Origin', ['Web', 'Phone', 'Email'])
    status = st.selectbox('Status', ['New', 'Working', 'Closed'])
    
    # Submit button
    submitted = st.form_submit_button('Create Case')

# Handle form submission
if submitted:
    if subject and description:
        try:
            case = create_salesforce_case(subject, description, origin, status)
            st.success(f"Case created successfully! Case ID: {case['id']}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error('Please fill in all required fields.')

