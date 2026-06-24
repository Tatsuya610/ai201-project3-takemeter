"""collect_reddit.py
Helper script to collect posts and top-level comments from a subreddit into a CSV.

Usage:
  export REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=... REDDIT_USER_AGENT="takemeter script"
  python scripts/collect_reddit.py --subreddit nba --limit 1000 --out data/takemeter_raw.csv

Notes:
- This script collects public data only. Inspect the CSV and label examples manually.
"""
import csv
import argparse
import os

try:
    import praw
except ImportError:
    raise RuntimeError("Install praw: pip install praw")

def collect(subreddit, limit, out_path):
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    user_agent = os.environ.get("REDDIT_USER_AGENT", "takemeter-collector")
    if not client_id or not client_secret:
        raise RuntimeError("Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET in environment")
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
    sub = reddit.subreddit(subreddit)
    rows = []
    for post in sub.top(limit=limit):
        if not post.selftext and not post.title:
            continue
        text = post.title
        if post.selftext:
            text += "\n\n" + post.selftext
        rows.append((text.replace('\n',' '), "", "", f"r/{subreddit}"))
        post.comments.replace_more(limit=0)
        for c in post.comments.list():
            if c.body and c.body not in ["[deleted]", "[removed]"]:
                rows.append((c.body.replace('\n',' '), "", "", f"r/{subreddit}"))
    with open(out_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["text","label","notes","source_community"])
        for r in rows:
            writer.writerow(r)
    print(f"Wrote {len(rows)} rows to {out_path}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--subreddit", default="nba")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--out", dest="out_path", default="data/takemeter_raw.csv")
    args = p.parse_args()
    collect(args.subreddit, args.limit, args.out_path)
