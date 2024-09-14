import openai
import json
import jinja2
import os
from dotenv import load_dotenv
from model import get_model_response


def get_prompt_template():
    template_str = """You are a medical AI assistant.
    
    Perform a detailed extraction from the following clinical trial document to answer the user’s query.
    
    Document:
    {{ document }}
    
    User Query:
    {{ query }}
    
    Extract the following information:
    - Study design
    - Number of participants
    - Interventions (detailed)
    - Outcomes (primary and secondary)
    - Statistical significance (p-values, confidence intervals)
    - Adverse events
    - Metadata (authors, publication date, journal)
    
    Provide the output in this JSON format:
    {
      "description": "<summary>",
      "metadata": {
        "authors": ["<author1>", "<author2>"],
        "publication_date": "<date>",
        "journal": "<journal_name>"
      },
      "extracted_features": [
        {
          "description": "<feature_description>",
          "value": "<value>"
        }
      ]
    }
    Ensure the output is valid JSON and includes all required fields."""
    return template_str

def initial_extraction(document, query):
    template_str = get_prompt_template()
    template = jinja2.Template(template_str)
    prompt = template.render(document=document, query=query)


    response = get_model_response(prompt)

    output_text = response.choices[0].message.content.strip()
    try:
        output_json = json.loads(output_text)
        return output_json
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
