"""
This file parses the reviews raw data which is fetched from the API using
another file.
"""
import pickle
import json

# Cached the data so we don't waste their API usage
submissions = []
with open("reviews.pickle", "rb") as f:
    submissions = pickle.load(f)


def parse_score(score: str) -> int:
    return int(
        score["value"][0:2].strip().replace(":", "")
    )

def parse_review(review: dict) -> dict:
    if "rating" not in review["content"].keys():
        return

    parsed_review = {}
    metrics = [
            "rating",
            "soundness",
            "presentation",
            "contribution",
            "confidence"
        ]
    for m in metrics:
        parsed_review[m] = parse_score(review["content"][m])

    return parsed_review


# Lean submission detail
subs = []

for record in submissions:
    drs = record.details["directReplies"]
    if len(drs) < 1:
        continue

    item = {
        "id": record.id,
        "number": record.number,
        "title": record.content["title"]["value"],
        "keywords": record.content["keywords"]["value"],
        # "tldr": record.content["TLDR"],
        # "abstract": record.content["abstract"],
        "primary_area": record.content["primary_area"]["value"],
        "pdf": record.content["pdf"]["value"],
        # TODO: could lump each metric into one dict item
        # rather than splitting them into individual ones
        "reviews": [parse_review(r) for r in drs if "rating" in r["content"].keys()]
    }
    subs.append(item)

print(len(subs))

with open("data.json", "w") as f:
    json.dump(subs, f)

