import openai
import json
import os
from dotenv import load_dotenv
from model import get_model_response

MAX_ITERATIONS = 5

def answer_question(data, question):
    """
    Attempts to answer the given question based on the previously extracted data.
    
    Args:
    data (dict): The extracted data containing features.
    question (str): The question to be answered.
    
    Returns:
    str or None: The answer if found, None otherwise.
    """
    for feature in data.get("extracted_features", []):
        if question.lower() in feature["description"].lower():
            return feature["value"]
    return None

def is_satisfactory(answer):
    """
    Assesses whether the answer adequately addresses the question.
    
    Args:
    answer: The answer to be evaluated.
    
    Returns:
    bool: True if the answer is not None, False otherwise.
    """
    return answer is not None

def perform_llm_extraction(document, data, question):
    """
    Performs LLM extraction to get more data if the current answer is not satisfactory.
    
    Args:
    document (str): The document to extract information from.
    data (dict): Previously extracted data.
    question (str): The question to focus on for extraction.
    
    Returns:
    dict: Updated data with newly extracted information.
    """
    prompt = f"""
    You are a medical AI assistant.

    The question is: {question}
    
    Previously extracted data: {json.dumps(data, indent=2)}

    The document is:
    \"\"\"{document}\"\"\"

    Use the information to extract missing data and update the extracted features in the same JSON format.
    """

    response = get_model_response(prompt)

    updated_data_text = response.choices[0].message["content"].strip()

    try:
        updated_data = json.loads(updated_data_text)
        return updated_data
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return data

def evaluate_confidence(extracted_data, question):
    """
    Evaluate confidence based on completeness, relevance, and accuracy of extracted data.
    
    Args:
    extracted_data (dict): The data extracted from the document.
    question (str): The question being answered.
    
    Returns:
    float: A confidence score between 0 and 1.
    """
    required_fields = {
        "study design": 0.2,
        "outcomes": 0.4,
        "statistical significance": 0.3,
        "adverse events": 0.1,
    }

    score = 0
    for field, weight in required_fields.items():
        if any(
            field in feature["description"].lower()
            for feature in extracted_data.get("extracted_features", [])
        ):
            score += weight

    # Check if the question is directly related to the field (higher importance)
    if (
        "outcomes" in question.lower()
        and "outcomes" in extracted_data.get("description", "").lower()
    ):
        score += 0.1  # Bonus points for direct relevance

    score = max(0, min(1, score))  # Ensure the score is between 0 and 1
    return score

def iterative_extraction_with_confidence(document, data, questions):
    """
    Performs iterative extraction and stops when the confidence score is high enough or iterations reach the max limit.
    
    Args:
    document (str): The document to extract information from.
    data (dict): Initial extracted data.
    questions (list): List of questions to be answered.
    
    Returns:
    tuple: Updated data and final confidence score.
    """
    confidence_threshold = 0.8
    iteration_count = 0
    confidence_score = 0

    while iteration_count < MAX_ITERATIONS and confidence_score < confidence_threshold:
        for question in questions:
            answer = answer_question(data, question)
            if not is_satisfactory(answer):
                # Perform further extraction if the answer is not satisfactory
                updated_data = perform_llm_extraction(document, data, question)
                data = updated_data

            # Recalculate the confidence score after each iteration
            confidence_score = evaluate_confidence(data, question)
            iteration_count += 1

            if confidence_score >= confidence_threshold:
                break

    return data, confidence_score
