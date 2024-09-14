# Clinical Trial Data Extraction and Analysis System

## Project Overview

This project focuses on building a robust system to extract, analyze, and validate clinical trial data, with a particular focus on immunology. The system automates the process of extracting key clinical data points from PDF documents related to immunological treatments and trials (e.g., rheumatoid arthritis), generating insights, and answering specific queries. The entire system leverages Large Language Models (LLMs) to enhance the extraction process through iterative questioning, dynamic question generation, and validation.

## Objectives

1. **Automated Clinical Trial Data Extraction**: Extract critical trial outcomes, adverse events, statistical significance, and safety data from clinical trials.
2. **Question-Answering System**: Use a dynamic question-generation and iterative-questioning process to refine the extraction of data in response to specific queries.
3. **Validation and Accuracy**: Implement robust validation using Pydantic models to ensure the structure and integrity of extracted data.

## Why This Approach?

The methodology is designed to handle complex clinical trials by focusing on:

- **Structured Data Extraction**: Automatically extracting outcomes and adverse events is critical for medical research, particularly in immunology, where trials are highly complex and involve long-term efficacy and safety analysis.
- **Iterative Querying**: This system improves on traditional extraction methods by iterating over documents multiple times, ensuring higher accuracy for difficult-to-locate data points.
- **LLM-Assisted Refinement**: The use of LLMs allows for enhanced understanding and querying of the clinical trial data, making this approach uniquely suited for highly technical domains such as immunology.

## Unique Advantages

1. **Immunology Focus**: This system has been specifically designed to address immunology-related clinical trials, with tailored question sets and templates designed for trials involving diseases like rheumatoid arthritis and lupus.

2. **Dynamic Iterative Questioning**: Traditional extraction methods fail when data is scattered or difficult to interpret. The iterative approach allows the system to refine its extraction based on intermediate feedback and follow-up questions, ensuring a complete and accurate dataset.

3. **LLM-Powered**: Leveraging LLMs enables the system to ask relevant follow-up questions and extract insights that are often missed in manual reviews, making it both efficient and scalable.

4. **Validation with Pydantic**: The system uses Pydantic to validate data structures, ensuring both the correctness of the extracted content and its conformity to predefined models. This helps in improving the reliability and robustness of the outputs.

![Process Flow Diagram](img/img.png)

## Example Workflow

### Input:

Clinical trial documents are provided as PDF files, stored in `data/articles/`. Example trials include:

- Assessment of Clinical Analgesic Levels and Serum Biomarkers in Patients with Rheumatoid Arthritis
- Efficacy and safety of upadacitinib in patients with rheumatoid arthritis

### Questions:

The system processes specific questions, which are stored in `data/questions.json`. Example questions include:

```
[
{
"id": 1,
"difficulty": "easy",
"question": "What were the primary outcomes of the clinical trial for lupus?"
},
{
"id": 2,
"difficulty": "complicated",
"question": "Compare the adverse event profiles and statistical outcomes of immunotherapy treatments in clinical trials for rheumatoid arthritis."
}
]
```

### Process:

1. **Extract Text from PDF**: The system extracts the raw text from the PDF files using pdfplumber.
2. **Initial Extraction**: The system extracts key features from the text, including outcomes, adverse events, and statistical details, using the `initial_extraction` function.
3. **Iterative Questioning**: If the answer to the query is incomplete or not satisfactory, the system generates follow-up questions and performs additional extractions until it reaches a satisfactory confidence score.
4. **Question Generation**: Follow-up questions are dynamically generated to refine the query process.
5. **Validation**: The output is validated using custom validations, ensuring the integrity and structure of the data.

### Example Output:

Here is an example JSON output from a processed question:
```
{
"question_id": 2,
"question_text": "Compare the adverse event profiles and statistical outcomes of immunotherapy treatments in clinical trials for rheumatoid arthritis.",
"related_article": "Efficacy and safety of upadacitinib in patients with rheumatoid arthritis",
"steps_taken": 3,
"confidence_score": 0.85,
"final_answer": {
"description": "The trial compared the adverse events between upadacitinib and other immunotherapies. Upadacitinib showed a lower rate of serious adverse events (2%) compared to other treatments.",
"metadata": {
"authors": ["Dr. John Doe", "Dr. Jane Smith"],
"publication_date": "2023-04-10",
"journal": "Immunology Research"
},
"extracted_features": [
{"description": "Adverse Events", "value": "Common: Nausea, Headache; Serious: 2% serious infections"}
]
},
"follow_up_questions": [
{"question": "What are the secondary outcomes?"},
{"question": "What is the confidence interval for serious adverse events?"}
]
}
```


## Technical Process Description

1. **PDF Extraction**
   The clinical trial documents are first parsed using pdfplumber to extract raw text. This is critical in converting the often scattered and complex structure of clinical trial documents into analyzable text.

2. **Initial Data Extraction**
   Once the text is extracted, the `initial_extraction` function processes the text based on the user's query. It looks for predefined key features such as:
   - Primary and Secondary Outcomes
   - Adverse Events
   - Statistical Significance
   This is done using a combination of prompt engineering and parsing rules to extract the relevant content.

3. **Iterative Questioning**
   The system doesn't stop at the first attempt to extract data. If it detects that a question hasn't been fully answered (based on a confidence scoring mechanism), it generates follow-up questions using the `question_generation.py` script. These follow-up questions help in refining the answer until a satisfactory result is reached.

4. **Validation with Pydantic**
   After data extraction, the system validates the structure and content of the extracted data using Pydantic models. This ensures that:
   - All expected fields are present.
   - Data like publication dates follow the correct format (YYYY-MM-DD).
   - Answers and metadata conform to the expected structure.

5. **JSON Output Generation**
   Once the extraction, refinement, and validation are complete, the final results are saved as JSON files, which include detailed responses to the questions, metadata, and confidence scores.