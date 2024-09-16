import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber

def segment_document(document_text):
    """
    Segment the clinical trial document into sections based on typical headers.
    """
    section_headers = ["INTRODUCTION", "METHODS", "RESULTS", "DISCUSSION", "CONCLUSION", "ADVERSE EVENTS"]
    sections = {}
    current_section = None
    header_pattern = re.compile(r"^\s*(" + "|".join(section_headers) + r")\s*$", re.IGNORECASE)
    
    for line in document_text.split('\n'):
        line = line.strip()
        if header_pattern.match(line):
            current_section = line.upper()
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)
    
    for section in sections:
        sections[section] = ' '.join(sections[section])
    
    return sections

def find_relevant_section(query, sections):
    """
    Use TF-IDF to match the query to the most relevant section in the document.
    """
    vectorizer = TfidfVectorizer()
    section_texts = list(sections.values())
    tfidf_matrix = vectorizer.fit_transform(section_texts + [query])
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    most_relevant_index = similarities.argmax()
    most_relevant_section = list(sections.keys())[most_relevant_index]
    return most_relevant_section, sections[most_relevant_section]