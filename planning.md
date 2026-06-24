Project: TakeMeter — Evaluating discourse quality on r/nba

Community
- Chosen community: r/nba (public Reddit sports community). I chose r/nba because discourse is text-heavy, frequent, and contains a mix of short reactions, bold claims, and data-driven analysis — a good fit for labels that separate `analysis`, `hot_take`, and `reaction`.

Labels (3)
- `analysis`: A post that gives a structured argument or explanation. Signals include references to specific stats, historical comparisons, tactical observations, or multi-step reasoning. Example: "His playoff PER drops 5 points when defended by switchable lineups; teams adjust and he struggles in iso possessions." / "Coach X's rotations expose the bench; look at minutes 24–36 — that's where the defensive rating spikes."
- `hot_take`: A bold or provocative opinion stated confidently without supporting evidence or argument. It may use charged language or definitive claims but lacks verifiable backing. Example: "LeBron is overrated — he won't win another title." / "This rookie is the next KD, end of story." 
- `reaction`: An immediate emotional response to an event (praise, anger, hype) without an attempt at argument or evidence. Examples: "WHAT A BANGER!!!" / "This refs crew are trash."

Hard edge cases
- Short, stat-bearing posts (e.g., "He averages 5.6 assists in playoffs") — decide: if the post's sole content is a raw stat with no reasoning or comparison, label `hot_take` if used to assert a claim, otherwise `analysis` if presented as evidence within an argument. Rule: if removing the statistic leaves the claim unsupported, treat as `hot_take`.
- Sarcastic posts: when sarcasm clearly negates literal content, prefer `reaction` unless sarcasm includes structured comparison or explicit evidence.

Data collection plan
- Source: public posts and top-level comments from r/nba (Reddit). Use manual copy or PRAW script to fetch public posts and comments. Exclude deleted or removed content.
- Target: at least 200 labeled examples, balanced (aim ≥20% per label). Desired distribution: ~80–90 examples `analysis`, 60–70 `hot_take`, 50–60 `reaction` (adjust after sampling). If a label is underrepresented, sample threads known for that style (e.g., game-thread reactions for `reaction`, longform threads for `analysis`).

Annotation process
- Create a single CSV `data/takemeter_labeled.csv` with columns: `text,label,notes,source_community`.
- Read each example fully, assign exactly one label according to definitions, and record brief notes for ambiguous cases.

Evaluation metrics
- Overall accuracy (for comparability).
- Per-class F1 score (preferred) to capture precision/recall tradeoffs for each label.
- Confusion matrix (directional errors are informative — e.g., `analysis`→`hot_take`).
- Report: accuracy for both fine-tuned model and Groq zero-shot baseline; per-class precision/recall/F1 for both models; at least 3 analyzed failure cases.

Definition of success
- Minimum: fine-tuned model improves overall accuracy by at least 10 percentage points vs zero-shot baseline, and no class has F1 < 0.40.
- Preferred: per-class F1 ≥ 0.70 for at least two labels and overall accuracy ≥ 0.75.

AI Tool Plan
- Label stress-testing: use an LLM to generate 5–10 synthetic boundary posts for each ambiguous pair (e.g., analysis vs hot_take). If synthetic posts are ambiguous, refine label definitions.
- Annotation assistance: optionally pre-label unlabeled examples using an LLM, but every pre-label must be reviewed manually. Document which examples were pre-labeled in `notes` column.
- Failure analysis: after evaluation, paste misclassified examples into an LLM and ask for patterns; verify patterns by re-reading examples and reporting results in the README.

Notes
- Start with `planning.md` before collecting or labeling. Update this file when definitions change or stretch features are attempted.
