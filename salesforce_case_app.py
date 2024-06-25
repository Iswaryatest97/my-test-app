import streamlit as st
import streamlit.components.v1 as components
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

# custom_css = """
# <style>
# .embeddedServiceHelpButton .helpButton .uiButton {
#     background-color: #005290;
#     font-family: "Arial", sans-serif;
# }
# .embeddedServiceHelpButton .helpButton .uiButton:focus {
#     outline: 1px solid #005290;
# }
# </style>
# """
# # Inject the custom CSS into the Streamlit app
# st.markdown(custom_css, unsafe_allow_html=True)

# # Set page configuration
# st.set_page_config(
#     page_title="My App",
#     page_icon="🚀",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

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
    if subject:
        try:
            case = create_salesforce_case(subject, description, origin, status)
            st.success(f"Case created successfully! Case ID: {case['id']}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error('Please fill in all required fields.')

html_content = """
<!DOCTYPE html>
<html>
<head>
  <title>My Website with Salesforce Chat</title>
</head>
<body>
    <div id="embedded-messaging" class="embedded-messaging"></div>
  <script type="text/javascript">
    window._snapinsSnippetSettings = {
      // Embedded Service settings
    };
    (function() {
      var script = document.createElement('script');
      script.src = 'https://so1714738901949.my.site.com/ESWCustomMessageInApp1719136220263/assets/js/bootstrap.min.js';
      script.onload = function() {
        try {
            embeddedservice_bootstrap.settings.language = 'en_US'; // For example, enter 'en' or 'en-US'

            embeddedservice_bootstrap.init(
                '00DHu000003oiq4',
                'Custom_Message_In_App',
                'https://so1714738901949.my.site.com/ESWCustomMessageInApp1719136220263',
                {
                    scrt2URL: 'https://so1714738901949.my.salesforce-scrt.com'
                }
            );
        } catch (err) {
            console.error('Error loading Embedded Messaging: ', err);
        }
      };
      document.body.appendChild(script);
    })();
  </script>
</body>
</html>

"""

# Use Streamlit to display the HTML content
st.components.v1.html(html_content, height=600)