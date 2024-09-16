import numpy as np
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
# Load GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Add padding token for GPT-2 (use the same as EOS token)
tokenizer.pad_token = tokenizer.eos_token

model = GPT2LMHeadModel.from_pretrained('gpt2')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

def generate_responses_batch(prompts, batch_size=8, max_length=512):
    model.eval()
    responses = []

    # Batch processing
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"].to(device),
                attention_mask=inputs["attention_mask"].to(device),
                max_length=max_length,
                num_return_sequences=1
            )

        for output in outputs:
            response = tokenizer.decode(output, skip_special_tokens=True)
            responses.append(response)
    
    return responses

def calculate_consistency(responses):
    """
    Calculate the consistency of responses by comparing their cosine similarity.
    """
    # Remove empty or duplicate responses
    unique_responses = list(set([resp for resp in responses if resp.strip()]))
    
    if len(unique_responses) <= 1:
        return 0  # If all responses are identical or there’s only one response
    
    # Vectorize the unique responses
    vectorizer = TfidfVectorizer().fit_transform(unique_responses)
    vectors = vectorizer.toarray()
    
    # Calculate the cosine similarity between response vectors
    cosine_matrix = cosine_similarity(vectors)
    
    # Calculate the average consistency score (cosine similarity between pairs)
    avg_consistency = np.mean([cosine_matrix[i, j] for i in range(len(unique_responses)) for j in range(i + 1, len(unique_responses))])
    
    return avg_consistency

def select_best_response(responses):
    """
    Select the most consistent response based on frequency or similarity.
    """
    from collections import Counter
    response_counts = Counter(responses)
    best_response = response_counts.most_common(1)[0][0]
    return best_response

