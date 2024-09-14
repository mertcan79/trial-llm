import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key and MODEL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_model_response(prompt, max_tokens=500, temperature=0.5):
    """
    Function to get a response from the appropriate model based on the MODEL environment variable.

    :param prompt: The input prompt for the model
    :param max_tokens: Maximum number of tokens in the response (default: 500)
    :param temperature: Temperature setting for response generation (default: 0.5)
    :return: The model's response
    """
    # Check if the MODEL is set to "gpt" (for paid GPT-3.5-turbo model)
    if MODEL.lower() == "o1":
        # Use the GPT-3.5-turbo model for chat completions
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a medical AI assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        # Extract and return the content of the response
        return response.choices[0].message.content.strip()
    
    # Check if the MODEL is set to "free" (for free text-davinci-003 model)
    elif MODEL.lower() == "gpt3":
        # Use the GPT-3.5-turbo model for chat completions (updated from text-davinci-003)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical AI assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        # Extract and return the content of the response
        return response.choices[0].message.content.strip()
    
    # Raise an error if an unsupported MODEL is specified
    else:
        raise ValueError(f"Unsupported MODEL: {MODEL}. Please use 'gpt' or 'free'.")
