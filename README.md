# TakeMeter — discourse quality classifier (r/nba)

This repo contains the planning and tooling for the TakeMeter project: a fine-tuned classifier that distinguishes `analysis`, `hot_take`, and `reaction` in r/nba posts and comments.

Files
- [planning.md](planning.md) — design decisions, labels, edge cases, and AI tool plan.
- [data/takemeter_labeled.csv](data/takemeter_labeled.csv) — labeled dataset (CSV with `text,label,notes,source_community`).
- `notebook/takemeter_starter.ipynb` — Colab-ready starter notebook with train/eval pipeline (use the official starter notebook recommended in the course for Groq baseline).
- `scripts/collect_reddit.py` — helper script to download public posts/comments from Reddit into CSV.
- `requirements.txt` — python deps for local experimentation.

Quick start

1. Prepare data: fill `data/takemeter_labeled.csv` with at least 200 labeled examples (see `planning.md`).
2. Open the Colab starter notebook (recommended: copy the course's Colab starter and follow runtime instructions) or run `notebook/takemeter_starter.ipynb` in Colab.
3. Add your Groq API key in Colab secrets for the zero-shot baseline, and run Sections 1–2 before running baseline or fine-tuning.

Data collection (script)

The included `scripts/collect_reddit.py` uses `praw` to fetch posts/comments. Create a Reddit app and set `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `REDDIT_USER_AGENT` in your environment before running.

Evaluation and submission

When training is done, download `evaluation_results.json` and `confusion_matrix.png` from Colab and commit them to the repo. Put the demo video in the repo (or include an external link) and document results in this README: overall accuracy for both models, per-class metrics, confusion matrix (as markdown table), 3 analyzed failure cases, and sample classifications.
# ai201-project3-takemeter
TakeMeter: Coachability Meter for Baseball Discussions

A fine-tuned text classifier that categorizes baseball-related online discussion into:

- reflective

- help_seeking

- blame_or_venting

The project uses public Reddit baseball discussions and compares a fine-tuned DistilBERT classifier with a zero-shot Groq LLM baseline.

## Project Status

- [x] Community and label taxonomy selected

- [x] Initial planning document created

- [ ] Dataset collection and annotation

- [ ] Zero-shot baseline evaluation

- [ ] DistilBERT fine-tuning

- [ ] Final evaluation report

- [ ] Demo video
