#!/usr/bin/env python3
import csv
import re
import random
from collections import defaultdict

IN = "data/takemeter_synthetic_200.csv"
OUT_TRAIN = "data/train.csv"
OUT_VAL = "data/val.csv"
HEADER = ["text","label","notes","source_community"]

random.seed(42)

def clean_text(s):
    if s is None:
        return ""
    s = s.strip()
    # collapse whitespace
    s = re.sub(r"\s+", " ", s)
    return s

rows = []
with open(IN, newline='', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for i, row in enumerate(r):
        text = clean_text(row.get('text',''))
        label = (row.get('label') or '').strip()
        notes = (row.get('notes') or '').strip()
        src = (row.get('source_community') or '').strip()
        if not text:
            continue
        rows.append({'text': text, 'label': label, 'notes': notes, 'source_community': src})

orig_count = len(rows)
# deduplicate by lowercased text
seen = set()
unique = []
for r in rows:
    key = r['text'].lower()
    if key in seen:
        continue
    seen.add(key)
    unique.append(r)

after_dedup = len(unique)

# Optionally drop very short texts (<3 tokens)
cleaned = []
for r in unique:
    if len(r['text'].split()) < 2:
        continue
    cleaned.append(r)

after_clean = len(cleaned)

# group by label (empty label allowed)
groups = defaultdict(list)
for r in cleaned:
    groups[r['label']].append(r)

train_rows = []
val_rows = []
for label, items in groups.items():
    random.shuffle(items)
    n = len(items)
    n_val = max(1, int(round(n * 0.2)))
    val = items[:n_val]
    train = items[n_val:]
    # If train becomes empty (small n), keep at least one in train
    if len(train) == 0 and len(val) > 1:
        train.append(val.pop())
    train_rows.extend(train)
    val_rows.extend(val)

# final shuffle
random.shuffle(train_rows)
random.shuffle(val_rows)

# write out
with open(OUT_TRAIN, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    for r in train_rows:
        w.writerow([r['text'], r['label'], r['notes'], r['source_community']])

with open(OUT_VAL, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    for r in val_rows:
        w.writerow([r['text'], r['label'], r['notes'], r['source_community']])

# print summary
print(f"Input rows: {orig_count}")
print(f"After dedup: {after_dedup}")
print(f"After clean: {after_clean}")
print("Label distribution (total/ train / val):")
for label in sorted(groups.keys()):
    total = len(groups[label])
    t = sum(1 for r in train_rows if r['label']==label)
    v = sum(1 for r in val_rows if r['label']==label)
    print(f"  '{label or '<EMPTY>'}': {total} / {t} / {v}")

print(f"Wrote train: {len(train_rows)} rows -> {OUT_TRAIN}")
print(f"Wrote val:   {len(val_rows)} rows -> {OUT_VAL}")
