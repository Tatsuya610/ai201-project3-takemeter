#!/usr/bin/env python3
import csv
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
import math

TRAIN_CSV = 'data/train.csv'
VAL_CSV = 'data/val.csv'
MODEL_NAME = 'distilbert-base-uncased'
OUT_DIR = 'outputs/quick_distilbert'
BATCH_SIZE = 8
EPOCHS = 1
MAX_LEN = 128
LR = 5e-5

class TextDataset(Dataset):
    def __init__(self, path, label2id=None):
        self.rows = []
        with open(path, newline='', encoding='utf-8') as f:
            r = csv.DictReader(f)
            for row in r:
                text = row.get('text','').strip()
                label = row.get('label','').strip()
                if text:
                    self.rows.append((text, label))
        self.label2id = label2id

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        text, label = self.rows[idx]
        return {'text': text, 'label': label}


def build_label_map(datasets):
    labels = set()
    for ds in datasets:
        for _, label in ds.rows:
            labels.add(label)
    labels = sorted(labels)
    label2id = {l:i for i,l in enumerate(labels)}
    return label2id


def collate_fn(batch, tokenizer, label2id):
    texts = [b['text'] for b in batch]
    labels = [label2id[b['label']] for b in batch]
    enc = tokenizer(texts, padding=True, truncation=True, max_length=MAX_LEN, return_tensors='pt')
    enc['labels'] = torch.tensor(labels, dtype=torch.long)
    return enc


def evaluate(model, dataloader, device):
    model.eval()
    total = 0
    correct = 0
    losses = []
    with torch.no_grad():
        for batch in dataloader:
            batch = {k:v.to(device) for k,v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss.item() if outputs.loss is not None else 0.0
            logits = outputs.logits
            preds = logits.argmax(dim=-1)
            correct += (preds == batch['labels']).sum().item()
            total += batch['labels'].size(0)
            losses.append(loss)
    acc = correct/total if total>0 else 0.0
    avg_loss = sum(losses)/len(losses) if losses else 0.0
    return avg_loss, acc


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Using device:', device)

    train_ds = TextDataset(TRAIN_CSV)
    val_ds = TextDataset(VAL_CSV)
    label2id = build_label_map([train_ds, val_ds])
    print('Labels:', label2id)
    # attach map to datasets
    train_ds.label2id = label2id
    val_ds.label2id = label2id

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=len(label2id))
    model.to(device)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, collate_fn=lambda b: collate_fn(b, tokenizer, label2id))
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, collate_fn=lambda b: collate_fn(b, tokenizer, label2id))

    optimizer = AdamW(model.parameters(), lr=LR)

    global_step = 0
    model.train()
    for epoch in range(EPOCHS):
        running_loss = 0.0
        for step, batch in enumerate(train_loader):
            batch = {k:v.to(device) for k,v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            running_loss += loss.item()
            global_step += 1
            if global_step % 10 == 0:
                print(f"Epoch {epoch+1} step {global_step} loss {running_loss/global_step:.4f}")
        avg_train_loss = running_loss / max(1, global_step)
        print(f"Epoch {epoch+1} finished. avg loss {avg_train_loss:.4f}")
        # eval
        val_loss, val_acc = evaluate(model, val_loader, device)
        print(f"Validation loss: {val_loss:.4f}, acc: {val_acc:.4f}")

    # save model
    model.save_pretrained(OUT_DIR)
    tokenizer.save_pretrained(OUT_DIR)
    print('Saved model to', OUT_DIR)

if __name__ == '__main__':
    main()
