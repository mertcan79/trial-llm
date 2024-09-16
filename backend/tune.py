import torch
from transformers import BertForMaskedLM, BertTokenizer, AdamW
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
import pandas as pd

class ClinicalTrialDataset(torch.utils.data.Dataset):
    def __init__(self, texts, tokenizer, max_len=512):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        inputs = self.tokenizer.encode_plus(
            text,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding="max_length",
            return_token_type_ids=False,
            truncation=True
        )
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']
        return {
            'input_ids': torch.tensor(input_ids, dtype=torch.long),
            'attention_mask': torch.tensor(attention_mask, dtype=torch.long)
        }

# Load your data
df = pd.read_csv('backend/data/trials/immunology_clinical_trial_data.csv')
df = df[df['text'].str.len() > 100]  # Filter out very short entries

# Split the data
train_texts, val_texts = train_test_split(df['text'].tolist(), test_size=0.2)

# Tokenizer
tokenizer = BertTokenizer.from_pretrained('dmis-lab/biobert-base-cased-v1.1')

# Create datasets
train_dataset = ClinicalTrialDataset(train_texts, tokenizer)
val_dataset = ClinicalTrialDataset(val_texts, tokenizer)

# DataLoaders
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)

# Model and optimizer
model = BertForMaskedLM.from_pretrained('dmis-lab/biobert-base-cased-v1.1')

# Move model to GPU if available
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

# Set up optimizer
optimizer = AdamW(model.parameters(), lr=2e-5)

# Training loop
def train_epoch(loader, model, optimizer):
    model.train()
    total_loss = 0
    for batch in loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        
        outputs = model(input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
    
    return total_loss / len(loader)

# Validation loop
def eval_epoch(loader, model):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch in loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            
            outputs = model(input_ids, attention_mask=attention_mask, labels=input_ids)
            loss = outputs.loss

            total_loss += loss.item()
    
    return total_loss / len(loader)

# Train the model for several epochs
for epoch in range(3):
    train_loss = train_epoch(train_loader, model, optimizer)
    val_loss = eval_epoch(val_loader, model)
    print(f"Epoch {epoch+1}, Train Loss: {train_loss}, Validation Loss: {val_loss}")
    
# Save the fine-tuned model
model.save_pretrained('finetuned_biobert_model')
tokenizer.save_pretrained('finetuned_biobert_model')
