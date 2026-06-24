#!/usr/bin/env python3
import csv
import random

OUT = "data/takemeter_synthetic_200.csv"
HEADER = ["text","label","notes","source_community"]

help_templates = [
    "Does anyone have drills for improving bat speed?",
    "How do I stop choking with runners on base?",
    "What are good drills for infield footwork?",
    "Any advice for recovering from a hamstring tweak?",
    "How should I approach bullpen sessions to build endurance?",
    "What gear do youth players really need for winter training?",
    "How can I get my timing back after a long layoff?",
    "Which drills improve tracking breaking balls?",
    "Does anyone recommend programs for weightlifting for hitters?",
    "Tips for hitting off-speed better?",
    "How to read a pitcher's release point?",
    "Best way to practice situational hitting alone?",
    "Looking for recommendations on protective gear for catchers",
    "How to mentally prepare for a big at-bat?",
    "What drills help with soft hands on ground balls?",
]

reflective_templates = [
    "I realized I was pressing at the plate — slowed my swing and it helped.",
    "Been practicing shorter strides; my contact improved.",
    "After talking with my coach, I try to focus on finish not power.",
    "I used to chase pitches out of the zone; now I wait for my pitch.",
    "Stepping back, my approach to practice was unfocused; small changes helped.",
    "Sitting on fastballs didn't work for me; adjusting approach improved AVG.",
    "I learned to trust my mechanics during slump — results followed.",
    "Realized conditioning was the issue; extra sprints improved later innings.",
    "Reflecting on last season, better pitch recognition was the key.",
    "I slowed my load and timing became more consistent.",
    "Switched glove backhand technique and my throws are more accurate.",
    "Taking BP with situational reps changed how I approach games.",
    "Small mechanical tweak fixed my fielding range issues.",
]

vent_templates = [
    "That ump cost us the game with a phantom strike call!",
    "Can't believe the manager left our starter in for 120 pitches.",
    "Another blown save — bullpen is trash this year.",
    "Why do people warm up five minutes before game time? It's disrespectful.",
    "My team always chokes in the ninth; it's infuriating.",
    "So tired of players who don't hustle getting roster spots.",
    "Lost another close one because someone couldn't catch a popup.",
    "The coaching staff doesn't adjust — it's maddening.",
    "He swung at a hanger with two outs. Unbelievable.",
    "Fans acting like they know everything from the cheap seats.",
    "Sick of the constant replay reviews slowing the game down.",
]

counts = {"help_seeking":67, "reflective":67, "blame_or_venting":66}

rows = []
random.seed(42)

for label, n in counts.items():
    if label == "help_seeking":
        pool = help_templates
    elif label == "reflective":
        pool = reflective_templates
    else:
        pool = vent_templates
    for i in range(n):
        text = random.choice(pool)
        # small random variation
        if random.random() < 0.35:
            text = text + " " + random.choice(["Anyone else?","Thoughts?","Experienced players?","Please help."])
        if random.random() < 0.15:
            notes = "synthetic"
        else:
            notes = ""
        rows.append((text.replace('\n',' '), label, notes, "Homeplate"))

# shuffle to mix labels
random.shuffle(rows)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
    for r in rows:
        w.writerow(r)

print(f"Wrote {len(rows)} rows to {OUT}")
