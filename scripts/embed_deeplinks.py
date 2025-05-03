import pandas as pd
import json
import time
from agent.topic_rag_agent import get_embedding

# Load deeplinks
with open("data/deeplinks.json", "r", encoding="utf-8") as f:
    deeplink_data = json.load(f)

df = pd.json_normalize(deeplink_data)

# Combine title + description for better embedding
if "web_description" in df.columns:
    df["text"] = df["web_description"].fillna(df.get("app_description", ""))
else:
    df["text"] = df.get("app_description", "")
df["text"] = "bunq help: " + df["text"].fillna("")

# Generate embeddings safely
embeddings = []
for i, row in df.iterrows():
    print(f"Embedding {i+1}/{len(df)}")
    try:
        embedding = get_embedding(row["text"])
    except Exception as e:
        print(f"⚠️ Skipped {i} due to error: {e}")
        embedding = None
    embeddings.append(embedding)
    time.sleep(0.5)  # Be nice to the API

df["embedding"] = embeddings

# Drop rows with failed embeddings
df = df[df["embedding"].notnull()].reset_index(drop=True)

# Optional: select columns to retain
columns_to_keep = ["label", "url", "text", "embedding"]
df = df[[col for col in columns_to_keep if col in df.columns]]

# Save to disk
output_path = "data/deeplinks_embedded.pkl"
df.to_pickle(output_path)
print(f"✅ Saved embedded deeplinks to {output_path}")
