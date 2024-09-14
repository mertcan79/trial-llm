import openai
import json
import os
from dotenv import load_dotenv
from model import get_model_response


def generate_questions(current_answer, original_question):
    """
    Generates follow-up questions based on missing or insufficient information
    in the current answer, but only if truly necessary.

    Args:
        current_answer (str): The current extracted answer from the clinical trial data.
        original_question (str): The original question asked about the clinical trial.

    Returns:
        list: A list of generated follow-up questions, if any are necessary.
    """
    # Construct the prompt for the AI model
    prompt = f"""
    You are an AI assistant helping to analyze clinical trials, focusing on immunology.
    
    The current extracted answer is:
    {current_answer}
    
    The original question is:
    {original_question}
    
    Based on the extracted answer, assess whether there is critical missing information necessary to answer the original question.
    Only generate follow-up questions if essential clinical trial data is missing (e.g., study outcomes, statistical significance, adverse events). 
    Avoid generating redundant or unnecessary questions.
    """

    # Get the response from the AI model
    response = get_model_response(prompt)

    # Extract and parse the generated questions from the model's response
    generated_questions = response.choices[0].message["content"].strip()
    return json.loads(generated_questions)
