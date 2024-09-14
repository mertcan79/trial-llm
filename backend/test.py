import os
from dotenv import load_dotenv
from model import get_model_response

# Load environment variables
load_dotenv()

# Simple prompt
prompt = "What are the common side effects of aspirin?"

# Get the response from the model
response = get_model_response(prompt)

# Print the response
print("Model Response:")
print(response)
