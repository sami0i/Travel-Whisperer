import pandas as pd

# Load existing embedded articles (real Together content)
main_df = pd.read_pickle("data/together_topics_embedded.pkl")

# Load fallback travel articles you just embedded
travel_df = pd.read_pickle("data/travel_articles_embedded.pkl")

# Combine them
combined_df = pd.concat([main_df, travel_df], ignore_index=True)

# Optional: remove duplicates (if same link was embedded twice)
combined_df = combined_df.drop_duplicates(subset=["link"]).reset_index(drop=True)

# Save over the original Together embeddings
combined_df.to_pickle("data/together_topics_embedded.pkl")

print(f"✅ Combined and saved {len(combined_df)} articles to together_topics_embedded.pkl")
