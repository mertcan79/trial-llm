import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key and MODEL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

def get_model_response(prompt, max_tokens=500, temperature=0.5):
    """
    Function to get a response from the appropriate model based on the MODEL environment variable.
    
    :param prompt: The input prompt for the model
    :param max_tokens: Maximum number of tokens in the response (default: 500)
    :param temperature: Temperature setting for response generation (default: 0.7)
    :return: The model's response
    """
    if MODEL.lower() == "gpt":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            api_key=OPENAI_API_KEY
        )
        return response.choices[0].message['content'].strip()
    elif MODEL.lower() == "free":
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            api_key=OPENAI_API_KEY
        )
        return response.choices[0].text.strip()
    else:
        raise ValueError(f"Unsupported MODEL: {MODEL}. Please use 'gpt' or 'free'.")
