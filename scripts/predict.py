#!/usr/bin/env python3
import csv
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

MODEL_DIR = 'outputs/quick_distilbert'
INPUT = 'data/val.csv'
OUT = 'outputs/predictions.csv'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device', device)

if not os.path.isdir(MODEL_DIR):
    raise SystemExit(f'Model dir {MODEL_DIR} not found. Run quick_train.py first.')

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.to(device)
model.eval()

rows = []
with open(INPUT, newline='', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        rows.append(row)

with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['text','label'])
    for r in rows:
        text = r.get('text','').strip()
        enc = tokenizer(text, truncation=True, padding=True, return_tensors='pt').to(device)
        with torch.no_grad():
            out = model(**enc)
            pred = out.logits.argmax(dim=-1).item()
        # map id->label using model config
        id2label = {int(v):k for k,v in model.config.label2id.items()} if hasattr(model.config,'label2id') and model.config.label2id else None
        if id2label:
            label = id2label.get(pred, str(pred))
        else:
            # fallback: use numeric
            label = str(pred)
        w.writerow([text, label])

print('Wrote predictions to', OUT)
