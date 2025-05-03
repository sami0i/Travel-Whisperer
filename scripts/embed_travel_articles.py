import pandas as pd
import json
import time
from agent.topic_rag_agent import get_embedding

# Load mock travel articles
with open("data/travel_fallback_articles.json", "r", encoding="utf-8") as f:
    travel_data = json.load(f)

df = pd.json_normalize(travel_data)
df["text"] = "bunq help: " + df["source_text"].fillna("")

# Embed
embeddings = []
for i, row in df.iterrows():
    print(f"Embedding {i+1}/{len(df)}")
    try:
        embedding = get_embedding(row["text"])
    except Exception as e:
        print(f"⚠️ Skipped row {i}: {e}")
        embedding = None
    embeddings.append(embedding)
    time.sleep(0.5)

df["embedding"] = embeddings
df = df[df["embedding"].notnull()].reset_index(drop=True)
df.rename(columns={"source_link": "link"}, inplace=True)

# Save
df.to_pickle("data/travel_articles_embedded.pkl")
print("✅ Embedded travel articles saved.")
