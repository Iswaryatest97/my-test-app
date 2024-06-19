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

# Set page configuration
st.set_page_config(
    page_title="My App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

html_code = """
<style type='text/css'>
	.embeddedServiceHelpButton .helpButton .uiButton {
		background-color: #005290;
		font-family: "Arial", sans-serif;
	}
	.embeddedServiceHelpButton .helpButton .uiButton:focus {
		outline: 1px solid #005290;
	}
</style>
<script type='text/javascript' src='https://service.force.com/embeddedservice/5.0/esw.min.js'></script>
<script type='text/javascript'>
	var initESW = function(gslbBaseURL) {
		embedded_svc.settings.displayHelpButton = true; //Or false
		embedded_svc.settings.language = ''; //For example, enter 'en' or 'en-US'

		//embedded_svc.settings.defaultMinimizedText = '...'; //(Defaults to Chat with an Expert)
		//embedded_svc.settings.disabledMinimizedText = '...'; //(Defaults to Agent Offline)

		//embedded_svc.settings.loadingText = ''; //(Defaults to Loading)
		//embedded_svc.settings.storageDomain = 'yourdomain.com'; //(Sets the domain for your deployment so that visitors can navigate subdomains during a chat session)

		// Settings for Chat
		//embedded_svc.settings.directToButtonRouting = function(prechatFormData) {
			// Dynamically changes the button ID based on what the visitor enters in the pre-chat form.
			// Returns a valid button ID.
		//};
		//embedded_svc.settings.prepopulatedPrechatFields = {}; //Sets the auto-population of pre-chat form fields
		//embedded_svc.settings.fallbackRouting = []; //An array of button IDs, user IDs, or userId_buttonId
		//embedded_svc.settings.offlineSupportMinimizedText = '...'; //(Defaults to Contact Us)

		embedded_svc.settings.enabledFeatures = ['LiveAgent'];
		embedded_svc.settings.entryFeature = 'LiveAgent';

		embedded_svc.init(
			'https://examtestorg-dev-ed.my.salesforce.com',
			'https://examtestorg-dev-ed.my.site.com/test',
			gslbBaseURL,
			'00D2v000002HFkK',
			'BotWebSupportGrp',
			{
				baseLiveAgentContentURL: 'https://c.la1-c1-it3.salesforceliveagent.com/content',
				deploymentId: '572GC000000Dk8I',
				buttonId: '573GC0000009ZAC',
				baseLiveAgentURL: 'https://d.la1-c1-it3.salesforceliveagent.com/chat',
				eswLiveAgentDevName: 'BotWebSupportGrp',
				isOfflineSupportEnabled: false
			}
		);
	};

	if (!window.embedded_svc) {
		var s = document.createElement('script');
		s.setAttribute('src', 'https://examtestorg-dev-ed.my.salesforce.com/embeddedservice/5.0/esw.min.js');
		s.onload = function() {
			initESW(null);
		};
		document.body.appendChild(s);
	} else {
		initESW('https://service.force.com');
	}
</script>
"""

st.markdown(html_code, unsafe_allow_html=True)


