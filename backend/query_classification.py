from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load BioBERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('dmis-lab/biobert-base-cased-v1.1')
model = BertForSequenceClassification.from_pretrained('dmis-lab/biobert-base-cased-v1.1')

def classify_query(query):
    """
    Classify the query as factual, comparative, or inferential.
    """
    inputs = tokenizer(query, return_tensors='pt', truncation=True, max_length=512)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    classes = {0: 'factual', 1: 'comparative', 2: 'inferential'}
    return classes[predicted_class]
