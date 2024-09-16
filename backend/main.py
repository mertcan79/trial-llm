import os
import json
import pdfplumber
from advanced_prompting_system import advanced_prompting_system

ARTICLES_DIR = "backend/data/articles"
QUESTIONS_FILE = "backend/data/questions.json"
OUTPUT_DIR = "backend/data/outputs"

def extract_text_from_pdf(pdf_file_path):
    with pdfplumber.open(pdf_file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def process_question_on_articles(question, articles):
    steps = 0
    related_article = None
    final_answer = None
    confidence_score = 0

    for article_path in articles:
        article_name = os.path.basename(article_path)
        article_text = extract_text_from_pdf(article_path)

        # Perform the advanced prompting process
        result = advanced_prompting_system(question, article_text)
        confidence_score = result['consistency_score']
        final_answer = result['response']
        
        if confidence_score >= 0.8:
            related_article = article_name
            break
        
        steps += 1

    return {
        'related_article': related_article,
        'steps': steps,
        'confidence_score': confidence_score,
        'final_answer': final_answer
    }

def main():
    with open(QUESTIONS_FILE, "r") as q_file:
        questions = json.load(q_file)

    articles = [os.path.join(ARTICLES_DIR, f) for f in os.listdir(ARTICLES_DIR) if f.endswith(".pdf")]

    for question_id, question in questions.items():
        result = process_question_on_articles(question, articles)

        output_file = os.path.join(OUTPUT_DIR, f"result_{question_id}.json")
        with open(output_file, "w") as f:
            json.dump(result, f, indent=4)

        print(f"Question {question_id} processed. Result saved to {output_file}")

if __name__ == "__main__":
    main()
