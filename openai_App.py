from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
client = OpenAI(
    # This is the default and can be omitted
    api_key = os.environ.get("OPENAI_API_KEY"),
)

def getEnvironmentDataByKey(key):
    return os.environ.get(key)

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