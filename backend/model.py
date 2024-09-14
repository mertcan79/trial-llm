import os
from openai import OpenAI
from dotenv import load_dotenv
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

# Load environment variables
load_dotenv()

# Get the API key and MODEL from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")
os.environ['MODEL'] = 'biobert'

client = OpenAI(api_key=OPENAI_API_KEY)

def get_model_response(prompt, max_tokens=500, temperature=0.5):
    """
    Function to get a response from the appropriate model based on the MODEL environment variable.

    :param prompt: The input prompt for the model
    :param max_tokens: Maximum number of tokens in the response (default: 500)
    :param temperature: Temperature setting for response generation (default: 0.5)
    :return: The model's response
    """

    print(f"Current MODEL: {MODEL}")  # Debug print
    print(f"MODEL environment variable: {os.getenv('MODEL')}")  # Debug print

    if MODEL.lower() == "biobert":
        # Use the BioBERT model for question answering
        model_name = "dmis-lab/biobert-v1.1"
        model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model(**inputs)
        # Extract the answer from the model outputs
        answer_start = outputs.start_logits.argmax()
        answer_end = outputs.end_logits.argmax()
        answer = tokenizer.decode(inputs.input_ids[0][answer_start:answer_end+1])
        return answer.strip()

    elif MODEL.lower() == "gpt" or MODEL.lower() == "gpt3":
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
        raise ValueError(f"Unsupported MODEL: {MODEL}.")

# Example usage
if __name__ == "__main__":
    prompt = "Analyze the following clinical trial paper: [insert paper text here]"
    response = get_model_response(prompt)
    print(response)
