import torch
from transformers import BertForMaskedLM, BertTokenizer, AdamW
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
import pandas as pd
from tqdm import tqdm
from torch.cuda.amp import autocast, GradScaler
import gc

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
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)

# Model and optimizer
model = BertForMaskedLM.from_pretrained('dmis-lab/biobert-base-cased-v1.1')
model.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

optimizer = AdamW(model.parameters(), lr=2e-5)

accumulation_steps = 4  # Simulate larger batches

def train_epoch(loader, model, optimizer, device):
    model.train()
    total_loss = 0
    optimizer.zero_grad()
    for i, batch in enumerate(tqdm(loader)):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)

        outputs = model(input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss
        loss = loss / accumulation_steps  # Normalize loss to account for accumulation

        loss.backward()

        if (i + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()

        total_loss += loss.item() * accumulation_steps  # Scale back up the loss
    return total_loss / len(loader)

scaler = GradScaler()

def train_epoch(loader, model, optimizer, device):
    model.train()
    total_loss = 0
    scaler = GradScaler()  # For mixed precision

    for batch in tqdm(loader):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)

        with autocast(enabled=True):  # Enables mixed precision
            outputs = model(input_ids, attention_mask=attention_mask, labels=input_ids)
            loss = outputs.loss

        optimizer.zero_grad()
        scaler.scale(loss).backward()  # Scale the loss for mixed precision
        scaler.step(optimizer)
        scaler.update()

        total_loss += loss.item()
    return total_loss / len(loader)

def eval_epoch(loader, model, device):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch in loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            outputs = model(input_ids, attention_mask=attention_mask, labels=input_ids)
            total_loss += outputs.loss.item()
    return total_loss / len(loader)

# Training
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

epochs = 3
for epoch in range(epochs):
    print(f'Epoch {epoch+1}/{epochs}')
    train_loss = train_epoch(train_loader, model, optimizer, device)
    val_loss = eval_epoch(val_loader, model, device)
    print(f'Training Loss: {train_loss}, Validation Loss: {val_loss}')
    
    # Clear memory after each epoch
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

# Save the fine-tuned model
model.save_pretrained('finetuned_biobert_model')
tokenizer.save_pretrained('finetuned_biobert_model')
