import numpy as np
import pandas as pd
import openai
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

embedding_model = "text-embedding-3-small"

def get_embedding(text):
    response = openai.Embedding.create(
        model=embedding_model,
        input=text.strip().replace("\n", " ")
    )
    return np.array(response.data[0].embedding)

def retrieve_related_topic(user_prompt, together_df, top_k=1):
    user_embed = get_embedding(user_prompt)

    valid_rows = together_df[together_df["embedding"].notnull()].copy()
    valid_rows["embedding"] = valid_rows["embedding"].apply(np.array)
    matrix = np.stack(valid_rows["embedding"].values)

    scores = cosine_similarity([user_embed], matrix)[0]
    valid_rows["score"] = scores

    best = valid_rows.sort_values("score", ascending=False).head(top_k).iloc[0]

    print(f"🔍 Top article score: {best['score']:.4f}")
    print(f"Top article text (truncated): {best.get('text')[:100]}")  # key line

    return best.get("text"), best.get("text"), best.get("link")


def recommend_together_topic(prompt, together_df):
    enhanced_prompt = (
        prompt
        + "\nFocus on travel savings, bunq travel insurance, trip budgeting, and planning tools."
    )
    try:
        title, content, link = retrieve_related_topic(enhanced_prompt, together_df)
        return content, link
    except Exception as e:
        print("❌ RAG failed:", str(e))
        return None, None

