import openai
import json
import os
from dotenv import load_dotenv
from model import get_model_response



def generate_questions(current_answer, original_question):
    """
    Generates follow-up questions based on missing or insufficient information 
    in the current answer, but only if truly necessary.
    """
    
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
    
    response = get_model_response(prompt)
    
    generated_questions = response.choices[0].message['content'].strip()
    return json.loads(generated_questions)
