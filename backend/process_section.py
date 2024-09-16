from query_classification import classify_query
from extraction import segment_document
from question_generation import construct_prompt
from self_consistency import generate_responses_batch, calculate_consistency, select_best_response

def process_section(section_name, section_text, query):
    # Step 1: Identify Query Type
    query_type = classify_query(query)
    
    # Step 2: Construct the prompt for this section
    prompt = construct_prompt(query, query_type, section_text, section_name)
    
    # Step 3: Generate responses using batch processing
    responses = generate_responses_batch([prompt], batch_size=1)
    
    # Step 4: Calculate the consistency of the responses
    consistency_score = calculate_consistency(responses)
    
    # Step 5: Select the most consistent response
    best_response = select_best_response(responses)
    
    return {
        'section': section_name,
        'query_type': query_type,
        'consistency_score': consistency_score,
        'response': best_response
    }

def refined_prompting_system(query, clinical_trial_text):
    # Step 1: Segment the clinical trial text into sections
    document_sections = segment_document(clinical_trial_text)
    
    results = {}
    
    # Step 2: Iterate over sections and process each one
    for section_name, section_text in document_sections.items():
        response_data = process_section(section_name, section_text, query)
        results[section_name] = response_data
    
    return results