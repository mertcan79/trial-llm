import os
import json
import pdfplumber
from dotenv import load_dotenv
from iterative_questioning import iterative_extraction_with_confidence, evaluate_confidence
from extraction import initial_extraction
from question_generation import generate_questions

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Directory where articles are stored
ARTICLES_DIR = "data/articles"
QUESTIONS_FILE = "data/questions.json"
OUTPUT_DIR = "data/outputs"

def extract_text_from_pdf(pdf_file_path):
    """
    Extract text content from the provided PDF file.
    """
    with pdfplumber.open(pdf_file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def process_question_on_articles(question, articles):
    """
    Process a single question by looping through all articles to find the best answer.
    """
    steps = 0
    related_article = None
    final_answer = None
    confidence_score = 0
    follow_up_questions = []

    # Loop through each article to find the best answer
    for article_path in articles:
        article_name = os.path.basename(article_path)
        article_text = extract_text_from_pdf(article_path)

        # Perform initial extraction
        extracted_data = initial_extraction(article_text, question)
        confidence_score = evaluate_confidence(extracted_data, question)

        # If confident enough, we stop the search
        if confidence_score >= 0.8:
            final_answer = extracted_data
            related_article = article_name
            break
        
        # If not confident, generate follow-up questions and refine the answer
        follow_up_questions = generate_questions(extracted_data, question)
        final_data, final_confidence_score = iterative_extraction_with_confidence(
            article_text, extracted_data, follow_up_questions
        )

        # If this article provides a better answer, update the final answer
        if final_confidence_score > confidence_score:
            final_answer = final_data
            confidence_score = final_confidence_score
            related_article = article_name
        
        steps += 1
    
    # If we fail to find an adequate answer, return the best attempt
    return {
        "related_article": related_article,
        "steps": steps,
        "confidence_score": confidence_score,
        "final_answer": final_answer,
        "follow_up_questions": follow_up_questions
    }

def main():
    """
    Main function to process all questions and loop through articles.
    """
    # Load questions from the questions.json file
    with open(QUESTIONS_FILE, 'r') as q_file:
        questions = json.load(q_file)
    
    # List all articles in the directory
    articles = [os.path.join(ARTICLES_DIR, f) for f in os.listdir(ARTICLES_DIR) if f.endswith('.pdf')]
    
    for question in questions:
        question_id = question['id']
        question_text = question['question']

        print(f"Processing Question ID: {question_id}, Question: {question_text}")
        
        # Process the question and get the result
        result = process_question_on_articles(question_text, articles)

        # Save the result as a JSON file
        output_file = os.path.join(OUTPUT_DIR, f"output_question_{question_id}.json")
        with open(output_file, 'w') as out_file:
            json.dump({
                "question_id": question_id,
                "question_text": question_text,
                "related_article": result["related_article"],
                "steps_taken": result["steps"],
                "confidence_score": result["confidence_score"],
                "final_answer": result["final_answer"],
                "follow_up_questions": result["follow_up_questions"]
            }, out_file, indent=4)
        
        print(f"Question {question_id} processed. Result saved to {output_file}")

if __name__ == "__main__":
    main()
