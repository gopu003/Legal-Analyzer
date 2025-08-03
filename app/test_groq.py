import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key found: {api_key is not None}")

# Initialize Groq client
client = Groq(api_key=api_key)

# Test API connection
try:
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello, are you working?"}],
        model="llama3-70b-8192"
    )
    print("API Connection Successful!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Error: {str(e)}")