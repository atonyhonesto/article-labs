"""Conversational ML for an SMS concierge bot: intent + slots + a confidence gate.

* Intent: TF-IDF (word and character n-grams, robust to texting typos) into a
  logistic regression.
* Slots: small, explicit extractors (party size, time) rather than another model.
* Confidence gate: below the threshold, the bot hands the guest to a human
  instead of guessing. Most chatbot failures are confident wrong answers.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

TRAIN = {
    "book_table": ["table for 2 at 8", "can i book dinner for four tonight", "reservation for 6 people at 7pm",
                   "need a table tmrw 730", "book us in for brunch sunday", "do you have space for 3 at 9",
                   "res for two please", "get me a dinner reservation"],
    "spa": ["book a massage", "is the spa open", "facial appointment tomorrow", "can i get a spa slot at 4",
            "couples massage for 2", "spa hours?"],
    "late_checkout": ["can i check out late", "late checkout please", "checkout at 2pm ok?", "extend my checkout",
                      "can we stay till 1", "late check out tmrw"],
    "recommendation": ["where should we go for drinks", "best bar nearby", "something fun to do tonight",
                       "recommend a show", "where's good for cocktails", "any tips for tonight"],
}


@dataclass
class Parsed:
    intent: str
    confidence: float
    slots: dict
    handoff: bool


def build() -> Pipeline:
    feats = FeatureUnion([("word", TfidfVectorizer(ngram_range=(1, 2))),
                          ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)))])
    model = Pipeline([("feats", feats), ("clf", LogisticRegression(C=5, max_iter=1000))])
    X = [t for ts in TRAIN.values() for t in ts]
    y = [k for k, ts in TRAIN.items() for _ in ts]
    return model.fit(X, y)


WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8}


def slots(text: str) -> dict:
    t = text.lower()
    out = {}
    m = re.search(r"(?:for|party of)\s+(\d+|" + "|".join(WORDNUM) + r")\b(?!\s*(?:pm|am))", t)
    if m:
        out["party_size"] = int(m.group(1)) if m.group(1).isdigit() else WORDNUM[m.group(1)]
    m = (re.search(r"\bat\s+(\d{1,2})(?::?(\d{2}))?\s*(am|pm)?", t)
         or re.search(r"\b(\d{1,2}):(\d{2})\s*(am|pm)?\b", t)
         or re.search(r"\b(\d{1,2})()\s*(am|pm)\b", t))
    if m:
        h, mm, ap = m.group(1), m.group(2), m.group(3)
        hour = int(h) % 12 + (12 if (ap == "pm" or (ap is None and int(h) < 11)) else 0)
        out["time"] = f"{hour:02d}:{int(mm or 0):02d}"
    return out


def parse(model: Pipeline, text: str, threshold: float = 0.45) -> Parsed:
    proba = model.predict_proba([text])[0]
    i = proba.argmax()
    conf = float(proba[i])
    return Parsed(model.classes_[i], conf, slots(text), handoff=conf < threshold)
