from openai import OpenAI
import os
import streamlit as st

try:
    from dotenv import load_dotenv
    dotenv_available = True
except ImportError:
    dotenv_available = False

# Use dotenv if it's available
if dotenv_available:
    print("dotenv is available")
    load_dotenv()  # Load environment variables from .env file
else:
    os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]
    print("dotenv is not available")
    
# Set your OpenAI API key
client = OpenAI(
    # This is the default and can be omitted
    api_key = os.environ.get("OPENAI_API_KEY") if dotenv_available else st.secrets["OPENAI_API_KEY"]
)

def getEnvironmentDataByKey(key):
    if dotenv_available:
        return os.environ.get(key)
    else:
        return st.secrets[key]
    
def ask_gpt(prompt, messages):    
    
    if prompt:
        messages.append({
            "role": "user", "content": prompt
        })

    response = client.chat.completions.create(
        model= "gpt-3.5-turbo", #"gpt-3.5-turbo-0301",
        messages = messages
    )
    return response.choices[0].message