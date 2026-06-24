#!/usr/bin/env python3
import argparse
import csv
from collections import Counter
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
import json
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--preds', required=True, help='CSV with columns text,label (predicted)')
parser.add_argument('--gold', required=True, help='Gold CSV with header text,label,...')
parser.add_argument('--out', default='results/metrics.json')
args = parser.parse_args()

# read preds
preds = []
with open(args.preds, newline='', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        preds.append((row.get('text','').strip(), row.get('label','').strip()))

# read gold, map by text
gold_map = {}
with open(args.gold, newline='', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        gold_map[row.get('text','').strip()] = row.get('label','').strip()

y_true = []
y_pred = []
texts = []
for t,p in preds:
    if t in gold_map:
        y_true.append(gold_map[t])
        y_pred.append(p)
        texts.append(t)

labels = sorted(list(set(y_true) | set(y_pred)))
if len(labels)==0:
    print('No overlapping texts between preds and gold. Ensure your preds file uses the same text as gold.')
    exit(1)

precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
cm = confusion_matrix(y_true, y_pred, labels=labels)

metrics = {'labels': labels, 'precision': dict(zip(labels, precision.tolist())), 'recall': dict(zip(labels, recall.tolist())), 'f1': dict(zip(labels, f1.tolist())), 'support': dict(zip(labels, support.tolist()))}

# ensure results dir
import os
os.makedirs(os.path.dirname(args.out), exist_ok=True)
with open(args.out, 'w', encoding='utf-8') as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)
print('Wrote metrics to', args.out)

# plot confusion matrix
fig, ax = plt.subplots(figsize=(6,6))
im = ax.imshow(cm, cmap='Blues')
ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_yticklabels(labels)
for i in range(len(labels)):
    for j in range(len(labels)):
        ax.text(j, i, cm[i,j], ha='center', va='center', color='black')
fig.tight_layout()
plt.xlabel('predicted')
plt.ylabel('true')
plt.title('Confusion Matrix')
plt.savefig(os.path.join(os.path.dirname(args.out), 'confusion_matrix.png'))
print('Wrote confusion matrix plot')
