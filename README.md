# TakeMeter

TakeMeter is a text classification project for baseball discussion. It labels short Reddit-style posts into three categories:

- `reflective`
- `help_seeking`
- `blame_or_venting`

The repository is prepared for submission with a Colab-first training workflow, preprocessing scripts, evaluation scripts, and a synthetic 200-example smoke-test dataset for development when live collection is blocked.

## What is included

- [planning.md](planning.md) - taxonomy, annotation rules, and project plan
- [SUBMISSION.md](SUBMISSION.md) - submission checklist and run instructions
- [data/takemeter_labeled.csv](data/takemeter_labeled.csv) - labeled CSV template
- [data/takemeter_synthetic_200.csv](data/takemeter_synthetic_200.csv) - synthetic development dataset
- [data/train.csv](data/train.csv) and [data/val.csv](data/val.csv) - cleaned train/validation splits
- [notebook/takemeter_colab.ipynb](notebook/takemeter_colab.ipynb) - Colab notebook for install, upload, train, predict, and evaluate
- [notebook/takemeter_starter.ipynb](notebook/takemeter_starter.ipynb) - original starter notebook
- [scripts/collect_reddit.py](scripts/collect_reddit.py) - Reddit collector using PRAW
- [scripts/collect_reddit_noauth.py](scripts/collect_reddit_noauth.py) - Reddit collector using public JSON
- [scripts/generate_synthetic.py](scripts/generate_synthetic.py) - synthetic data generator
- [scripts/preprocess_and_split.py](scripts/preprocess_and_split.py) - cleaning and split script
- [scripts/quick_train.py](scripts/quick_train.py) - 1-epoch DistilBERT smoke test
- [scripts/predict.py](scripts/predict.py) - inference script
- [scripts/evaluate.py](scripts/evaluate.py) - metric and confusion-matrix script
- [requirements.txt](requirements.txt) and [requirements-submission.txt](requirements-submission.txt)

## Data format

The labeled CSV uses this header:

```csv
text,label,notes,source_community
```

`text` is the Reddit post/comment text, `label` is one of the three target classes, `notes` is optional annotation context, and `source_community` stores the subreddit name.

## Recommended workflow

1. Open [notebook/takemeter_colab.ipynb](notebook/takemeter_colab.ipynb) in Google Colab.
2. Switch the runtime to GPU.
3. Install dependencies in the notebook.
4. Upload `data/takemeter_labeled.csv` or use Google Drive to mount the repo.
5. Run preprocessing, training, prediction, and evaluation cells in order.
6. Download `outputs/` and `results/` after evaluation.

## Local scripts

If you are running locally in an environment with the required packages installed:

```bash
python3 scripts/preprocess_and_split.py
python3 scripts/quick_train.py
python3 scripts/predict.py
python3 scripts/evaluate.py --preds outputs/predictions.csv --gold data/val.csv --out results/metrics.json
```

## Notes

- Reddit collection can be blocked by network policy. In that case, use the synthetic dataset for smoke testing or upload a pre-collected CSV.
- The repository currently includes a Colab pipeline and supporting scripts so the submission can be reproduced end to end.

## Repository status

- Project scaffold: complete
- Colab pipeline: complete
- Synthetic smoke-test data: complete
- Final training/evaluation on real Reddit data: pending when data is available
