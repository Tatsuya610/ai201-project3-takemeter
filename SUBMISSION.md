TakeMeter — Submission Instructions

What to include in the zip/tar you submit
- README.md (this repo's README with final evaluation summary)
- SUBMISSION.md (this file)
- data/: takemeter_labeled.csv (final labeled CSV) OR takemeter_synthetic_200.csv (if using synthetic for testing)
- notebook/: takemeter_starter.ipynb
- scripts/: all scripts (collectors, preprocess, quick_train, evaluate)
- outputs/: trained model directory (if produced) and evaluation artifacts (predictions, metrics.json)
- results/: final evaluation plots / report

How I prepared the project
- Collected data: primary plan is to collect Reddit posts/comments from target subreddits using `scripts/collect_reddit.py` (PRAW) or `scripts/collect_reddit_noauth.py` (public JSON). Note: collection may be blocked by network policies; in that case provide an uploaded CSV to `data/`.
- Labeled data format: CSV with header `text,label,notes,source_community`. Labels: `help_seeking`, `reflective`, `blame_or_venting`.
- Synthetic dataset: `scripts/generate_synthetic.py` produces `data/takemeter_synthetic_200.csv` (used for development when live collection is blocked).
- Preprocessing & split: `scripts/preprocess_and_split.py` creates `data/train.csv` and `data/val.csv`.
- Quick training: `scripts/quick_train.py` fine-tunes `distilbert-base-uncased` for a smoke test. It requires `torch` and `transformers`.
- Evaluation: `scripts/evaluate.py` computes precision/recall/F1 and saves `results/metrics.json` and `results/confusion_matrix.png`.

How to run everything (recommended: on Colab or a machine with internet)
1. Install dependencies (see `requirements-submission.txt`), preferably in a virtualenv.
2. Put your labeled CSV in `data/takemeter_labeled.csv` (or use synthetic for testing).
3. Preprocess and split:
   ```bash
   python3 scripts/preprocess_and_split.py
   ```
4. Train (quick smoke test):
   ```bash
   python3 scripts/quick_train.py
   ```
5. Evaluate:
   ```bash
   python3 scripts/evaluate.py --preds outputs/predictions.csv --gold data/val.csv
   ```

Notes for graders
- If `outputs/quick_distilbert` is present, the trained model is saved there. If not present, run `scripts/quick_train.py` (may require installing PyTorch). 
- The notebook `notebook/takemeter_starter.ipynb` contains a Colab-oriented walkthrough for tokenization, dataset preparation, and model fine-tuning.

If you want, I can produce a single zip file ready for submission once you approve the contents.
