"""collect_reddit_noauth.py
Fetch subreddit posts and top-level comments using Reddit's public JSON endpoints (no auth required).

Usage:
  python3 scripts/collect_reddit_noauth.py --subreddit Homeplate --limit 500 --out data/takemeter_raw.csv

Notes:
- This uses the public Reddit JSON endpoints and respects a simple rate limit.
"""
import argparse
import csv
import time
import requests

HEADERS = {"User-Agent": "takemeter-collector/0.1 (by /u/yourusername)"}

def fetch_posts(subreddit, limit):
    posts = []
    after = None
    fetched = 0
    per_page = 100
    while fetched < limit:
        to_fetch = min(per_page, limit - fetched)
        params = {"limit": to_fetch}
        if after:
            params['after'] = after
        url = f"https://www.reddit.com/r/{subreddit}/top/.json"
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if r.status_code != 200:
            raise RuntimeError(f"Failed to fetch posts: {r.status_code} {r.text}")
        data = r.json()
        children = data.get('data', {}).get('children', [])
        if not children:
            break
        for c in children:
            p = c.get('data', {})
            posts.append(p)
            fetched += 1
            if fetched >= limit:
                break
        after = data.get('data', {}).get('after')
        if not after:
            break
        time.sleep(1)
    return posts

def fetch_comments_for_post(post_id):
    # post_id should be fullname without t3_ prefix or with
    url = f"https://www.reddit.com/comments/{post_id}.json?limit=500"
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        return []
    j = r.json()
    if len(j) < 2:
        return []
    comments = []
    def walk(comments_list):
        for c in comments_list:
            kind = c.get('kind')
            data = c.get('data', {})
            if kind == 't1':
                body = data.get('body')
                if body and body not in ['[deleted]', '[removed]']:
                    comments.append(body)
                # fetch replies
                replies = data.get('replies')
                if replies and isinstance(replies, dict):
                    walk(replies.get('data', {}).get('children', []))
    walk(j[1].get('data', {}).get('children', []))
    return comments

def collect(subreddit, limit, out_path):
    posts = fetch_posts(subreddit, limit)
    rows = []
    for p in posts:
        title = p.get('title','')
        selftext = p.get('selftext') or ''
        text = (title + '\n\n' + selftext).strip()
        if text:
            rows.append((text.replace('\n',' '), '', '', f"r/{subreddit}"))
        post_id = p.get('id')
        # fetch top-level comments for the post
        try:
            comments = fetch_comments_for_post(post_id)
        except Exception:
            comments = []
        for c in comments:
            rows.append((c.replace('\n',' '), '', '', f"r/{subreddit}"))
        time.sleep(1)
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['text','label','notes','source_community'])
        for r in rows:
            writer.writerow(r)
    print(f"Wrote {len(rows)} rows to {out_path}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--subreddit', default='Homeplate')
    p.add_argument('--limit', type=int, default=200)
    p.add_argument('--out', dest='out_path', default='data/takemeter_raw.csv')
    args = p.parse_args()
    collect(args.subreddit, args.limit, args.out_path)
