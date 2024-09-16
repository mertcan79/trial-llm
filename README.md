# Clinical Trial Document Analysis with Iterative Questioning

## Project Overview

This project provides a powerful framework for analyzing clinical trial documents using a combination of **BioBERT** and **GPT-4** models. The goal is to automate the process of extracting relevant information, answering questions, and evaluating the consistency of responses from clinical trial data, such as drug comparisons, adverse events, and study design.

The system implements **iterative questioning** to refine responses, ensuring that the model not only answers questions based on the clinical trial text but also cross-validates the answers for consistency and accuracy.

### Key Advantages

- **Combines GPT-4 and BioBERT**: Leverages the domain-specific knowledge of **BioBERT** for processing medical text, while utilizing the advanced reasoning capabilities of **GPT-4** for generating, refining, and validating answers.
- **Iterative Questioning**: Each query undergoes multiple rounds of question-answer generation and validation, ensuring that the most consistent and accurate responses are selected.
- **Section-Specific Prompting**: The system segments clinical trial documents into sections (e.g., "INTRODUCTION", "METHODS", "RESULTS") and customizes the responses based on each section's relevance to the query.
- **Batch Processing**: Efficient batch processing of queries and responses ensures scalability across large documents and multiple sections.
- **Consistency Checking**: Ensures that answers across sections of a document are consistent, improving reliability.

## Example Workflow

1. **Query Classification**: The input query is first classified (e.g., factual, comparative, inferential) to determine the type of response needed.
2. **Document Segmentation**: The clinical trial document is segmented into meaningful sections (e.g., "INTRODUCTION", "METHODS", "RESULTS", "ADVERSE EVENTS").
3. **Iterative Questioning**:
    - **First Pass**: The query is passed to both **BioBERT** and **GPT-4**, where initial responses are generated based on the segmented sections of the document.
    - **Consistency Evaluation**: Responses are checked for consistency across multiple iterations.
    - **Refinement**: GPT-4 iteratively refines the answers, taking into account both previous responses and cross-validation from different sections.
4. **Final Answer Generation**: A final, consistent answer is provided based on the section-specific iterations and refinements.

## Example Use Case

Let’s assume a query asks, "Compare the adverse event rates between Drug X and Drug Y in elderly patients."

1. **Input**:
    ```json
    {
      "query": "Compare the adverse event rates between Drug X and Drug Y in elderly patients.",
      "clinical_trial_text": "INTRODUCTION: This study examines the efficacy and safety of Drug X and Drug Y in treating elderly patients with diabetes. METHODS: Drug X was administered to 200 patients, while Drug Y was administered to 150 patients over a 12-month period. RESULTS: Drug X resulted in 15% adverse events, while Drug Y resulted in 20% adverse events. ADVERSE EVENTS: Both drugs caused mild gastrointestinal issues in 5% of patients. Serious adverse events, including liver toxicity, occurred in 10% of Drug Y patients, compared to 5% in Drug X patients."
    }
    ```

2. **Iterative Questioning Process**:
    - **First Pass**: Both **BioBERT** and **GPT-4** generate responses based on each section of the clinical trial document.
    - **Section-Specific Prompting**: Answers related to adverse events are refined based on relevant sections like "RESULTS" and "ADVERSE EVENTS".
    - **Consistency Check**: The system compares the responses across sections to ensure that the answers are logically consistent.
    - **Refinement**: GPT-4 refines the responses to clarify any ambiguities or contradictions.

3. **Output**:
    ```json
    {
      "INTRODUCTION": {
        "query_type": "comparative",
        "consistency_score": 0.85,
        "response": "This study examines the efficacy and safety of Drug X and Drug Y in elderly patients with diabetes."
      },
      "METHODS": {
        "query_type": "comparative",
        "consistency_score": 0.82,
        "response": "Drug X was administered to 200 patients, while Drug Y was administered to 150 patients over a 12-month period."
      },
      "RESULTS": {
        "query_type": "comparative",
        "consistency_score": 0.88,
        "response": "Drug X resulted in 15% adverse events, while Drug Y resulted in 20% adverse events."
      },
      "ADVERSE EVENTS": {
        "query_type": "comparative",
        "consistency_score": 0.90,
        "response": "Serious adverse events, including liver toxicity, occurred in 10% of Drug Y patients, compared to 5% in Drug X patients."
      },
      "final_answer": {
        "response": "Drug X resulted in fewer adverse events (15%) compared to Drug Y (20%). Additionally, serious adverse events were more common with Drug Y (10%) compared to Drug X (5%)."
      }
    }
    ```

## Iterative Questioning: How It Works

- **First Iteration**: Both **BioBERT** and **GPT-4** generate initial responses to the query based on segmented sections.
- **Second Iteration**: GPT-4 refines the response by considering inconsistencies or gaps in the first-round answers.
- **Further Iterations**: The process repeats, iterating through section-specific prompting and cross-validating responses to ensure the highest consistency score.
  
The **iterative process** enables the system to handle complex questions by considering all possible responses, refining them iteratively, and selecting the best answer through consistency checks.

## Advantages of Using GPT-4 and BioBERT Together

- **BioBERT** excels in domain-specific text comprehension (medical, biomedical), providing the most relevant sections of clinical trials.
- **GPT-4** brings reasoning and language-generation capabilities to refine answers and handle complex queries that require broader context.
- The combination of both models ensures that answers are both medically accurate and logically consistent.
