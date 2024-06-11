import streamlit as st
import requests

from simple_salesforce import Salesforce, SalesforceAuthenticationFailed
from openai_App import getEnvironmentDataByKey

username = getEnvironmentDataByKey("USERNAME")
password = getEnvironmentDataByKey("PASSWORD")
security_token = getEnvironmentDataByKey("SECURITY_TOKEN")
consumer_key = getEnvironmentDataByKey("CONSUMER_KEY")
consumer_secret = getEnvironmentDataByKey("CONSUMER_SECRET")

# Combine password and security token
combined_password_token = password + security_token
print('toke**'+combined_password_token)
if not username or not password or not security_token:
    raise ValueError("Salesforce credentials are not set in environment variables")

# OAuth 2.0 token endpoint
token_url = 'https://examtestorg-dev-ed.my.salesforce.com/services/oauth2/token'

# Payload for token request
payload = {
    'grant_type': 'client_credentials',
    'client_id': consumer_key,
    'client_secret': consumer_secret,
    'username': username,
    'password': combined_password_token
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
