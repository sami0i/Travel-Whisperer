# scripts/embed_together_articles.py

import pandas as pd
import json
import time
from agent.topic_rag_agent import get_embedding

# Load together topics
with open("data/together_topics.json", "r", encoding="utf-8") as f:
    together_data = json.load(f)

df = pd.json_normalize(together_data)

# Use source_text as the only embedding input
df["text"] = "bunq help: " + df["source_text"].fillna("")

# Generate embeddings
embeddings = []
for i, row in df.iterrows():
    print(f"Embedding {i+1}/{len(df)}")
    try:
        embedding = get_embedding(row["text"])
    except Exception as e:
        print(f"⚠️ Error embedding row {i}: {e}")
        embedding = None
    embeddings.append(embedding)
    time.sleep(0.5)

df["embedding"] = embeddings
df = df[df["embedding"].notnull()].reset_index(drop=True)

# Optional: Rename link field for consistency with app
if "source_link" in df.columns:
    df.rename(columns={"source_link": "link"}, inplace=True)

# Save to disk
df.to_pickle("data/together_topics_embedded.pkl")
print("✅ Saved embedded Together articles.")
