from query_classification import classify_query
from extraction import segment_document
from process_section import refined_prompting_system

def advanced_prompting_system(query, document_text):
    # Step 1: Preprocess the query (optional but helpful for more complex queries)
    query = preprocess_query(query)  # Function for lowercasing, removing special chars, etc.

    # Step 2: Identify Query Type
    query_type = classify_query(query)

    # Step 3: Segment Document into Sections
    document_sections = segment_document(document_text)

    # Step 4: Process the query and document sections through refined_prompting_system
    results = refined_prompting_system(query, document_sections)

    # Step 5: Query-type specific handling
    results = handle_query_type_specific(results, query_type)  # Modify this function to adjust based on query type

    return results

def preprocess_query(query):
    # Example preprocessing: lowercasing, trimming, removing special characters
    return query.strip().lower()

def handle_query_type_specific(results, query_type):
    """
    Customizes the response based on the type of query.
    
    Args:
        results: A dictionary containing responses for each section.
        query_type: The type of query ('factual', 'comparative', 'inferential').

    Returns:
        Updated results based on query type.
    """
    # Prioritize sections based on query type
    if query_type == 'factual':
        # For factual queries, return the section with the highest consistency score
        best_section = max(results, key=lambda sec: results[sec]['consistency_score'])
        return {best_section: results[best_section]}
    
    elif query_type == 'comparative':
        # For comparative queries, prioritize sections like "Results" or "Adverse Events"
        comparison_sections = ["Results", "Adverse Events"]
        selected_results = {sec: res for sec, res in results.items() if sec in comparison_sections}
        
        # If no relevant sections are found, fall back to the highest consistency score
        if not selected_results:
            best_section = max(results, key=lambda sec: results[sec]['consistency_score'])
            return {best_section: results[best_section]}
        return selected_results

    elif query_type == 'inferential':
        # For inferential queries, combine responses from relevant sections like "Discussion", "Results"
        inferential_sections = ["Discussion", "Results"]
        selected_results = {sec: res for sec, res in results.items() if sec in inferential_sections}
        
        # Combine multiple sections if necessary
        combined_response = " ".join(res['response'] for res in selected_results.values())
        combined_consistency_score = sum(res['consistency_score'] for res in selected_results.values()) / len(selected_results)
        
        return {
            'combined': {
                'query_type': query_type,
                'consistency_score': combined_consistency_score,
                'response': combined_response
            }
        }
    
    # If no specific handling is required, return all results
    return results

