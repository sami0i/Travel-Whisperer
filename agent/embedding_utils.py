# agent/embedding_utils.py

import time
import numpy as np
from agent.topic_rag_agent import get_embedding

def embed_text_column(df, text_col, rate_limit=0.5, verbose=True):
    """
    Safely embed a text column in a DataFrame using OpenAI and return new df.
    """
    embeddings = []
    for i, text in enumerate(df[text_col].fillna("")):
        if verbose:
            print(f"Embedding {i+1}/{len(df)}")
        try:
            embedding = get_embedding(text)
        except Exception as e:
            print(f"⚠️ Error embedding row {i}: {e}")
            embedding = None
        embeddings.append(embedding)
        time.sleep(rate_limit)
    
    df["embedding"] = embeddings
    return df[df["embedding"].notnull()].reset_index(drop=True)
