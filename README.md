# Clinical Trial Analysis System with Iterative Questioning

## Project Overview

This project is designed to process and analyze clinical trial documents using an advanced **language model** pipeline, based on **BioBERT**. The system takes user queries about clinical trials and generates accurate responses by segmenting the document, classifying the query type, constructing prompts, and ensuring consistency in responses across different sections.

The system supports **iterative questioning**, which enables it to refine responses over multiple iterations. This is particularly useful for complex queries or situations where relevant information is scattered across sections of the document.

## Key Features

### Iterative Questioning

Iterative questioning is a key feature that allows the system to refine its responses based on previous outputs. It adjusts the query after each response iteration, enhancing the relevance and precision of the answers. This feedback loop continues until the system produces a satisfactory response, improving overall clarity and accuracy.

### Section-Specific Querying

The system segments clinical trial documents into key sections like **Introduction**, **Methods**, **Results**, and **Adverse Events**. By processing each section individually, it ensures that the query is matched with the most relevant content, yielding more accurate and context-aware responses.

### Query Type Classification

Queries are classified into different types—**factual**, **comparative**, or **inferential**. This classification helps the system decide how to generate responses, whether it needs to extract direct facts, compare elements, or infer insights.

### Consistency Scoring

The system employs **self-consistency scoring** to evaluate multiple responses and select the most coherent answer. This is particularly useful when multiple responses are generated for a single section, ensuring that the best and most consistent answer is returned to the user.

Example JSON Input:
```json
{
  "query": "Compare the adverse event rates between Drug X and Drug Y in elderly patients.",
  "clinical_trial_text": "INTRODUCTION: This study examines the efficacy and safety of Drug X and Drug Y in treating elderly patients with diabetes. METHODS: Drug X was administered to 200 patients, while Drug Y was administered to 150 patients over a 12-month period. RESULTS: Drug X resulted in 15% adverse events, while Drug Y resulted in 20% adverse events. ADVERSE EVENTS: Both drugs caused mild gastrointestinal issues in 5% of patients. Serious adverse events, including liver toxicity, occurred in 10% of Drug Y patients, compared to 5% in Drug X patients."
}
```

Example JSON Output:

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

## Advantages

- **Enhanced Accuracy**: By segmenting the clinical trial document and matching each query with relevant sections, the system achieves high accuracy in its responses.
- **Iterative Refinement**: The iterative questioning methodology ensures that even complex queries get more accurate and refined responses over multiple iterations.
- **Scalability**: The system supports batch processing, enabling the analysis of large datasets efficiently, making it suitable for extensive clinical trials data.
- **Context-Aware Responses**: The model is able to deliver contextually accurate responses specific to the clinical trial domain by using **BioBERT**, which is pre-trained on biomedical text.

## Process Flow

1. **Input**: The user inputs a query along with the full clinical trial document.
2. **Query Classification**: The system classifies the input query (e.g., factual, comparative, inferential).
3. **Document Segmentation**: The clinical trial document is segmented into relevant sections (Introduction, Methods, Results, Adverse Events).
4. **Prompt Construction**: Prompts are generated based on the query type and corresponding section.
5. **Batch Response Generation**: The system generates multiple responses for each section using batch processing.
6. **Consistency Calculation**: Consistency of the generated responses is calculated, and the best response is selected.
7. **Iterative Questioning**: If the system detects any uncertainty or if the initial response is incomplete, the query is refined, and the process repeats until satisfactory results are obtained.
8. **Output**: The system returns the best possible answer, along with consistency scores, providing a comprehensive response.

## Example Usage

Given the following input:

```text
Query: "How does Drug A compare to Drug B in terms of adverse events in elderly patients?"
Clinical Trial Document: Full text of a clinical trial.
```

The system would:

1. Classify the query as comparative.
2. Segment the clinical trial document into sections.
3. Construct a prompt tailored for the Methods and Adverse Events sections.
4. Generate multiple responses using batch processing.
5. Calculate consistency scores and select the best response:

   ```text
   "Drug A had fewer adverse events compared to Drug B, especially in patients over 65."
   ```

6. If necessary, the system will iterate by refining the question or focusing on other sections to improve the response.

### Advantages of Iterative Questioning

The iterative questioning process refines the responses by:

- Repeating the querying process with refined prompts.
- Adjusting focus based on inconsistencies or incomplete answers.
- Ensuring that even scattered information across multiple sections is captured accurately.

This method is particularly beneficial for complex clinical queries, where direct answers may not always be available, and additional context or refinement is necessary.

## Conclusion

This system provides a robust, scalable, and efficient method for answering complex clinical queries from trial documents. With the inclusion of iterative questioning, it ensures high accuracy and relevance in its responses, making it ideal for healthcare and research professionals needing in-depth clinical insights.
