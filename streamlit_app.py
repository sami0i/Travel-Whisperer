# streamlit_app.py

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import pycountry

from agent.travel_agent import travel_ai_agent
from agent.travel_map_helper import (
    build_choropleth_df,
    build_choropleth_map,
    build_spending_barchart
)
from scripts.user_data_loader import load_user_context

# --------------------------
# Caching for performance
# --------------------------
@st.cache_data
def load_data():
    transactions = pd.read_csv("data/transactions_cleaned.csv")
    accounts = pd.read_csv("data/monetary_accounts.csv")
    with open("data/together_topics.json", "r", encoding="utf-8") as f:
        together = json.load(f)
    together_df = pd.json_normalize(together)
    return transactions, accounts, together_df

# --------------------------
# Add timeline of travel spending
# --------------------------
def build_travel_timeline(df):
    df["updated_timestamp"] = pd.to_datetime(df["updated_timestamp"], errors="coerce")
    df = df.dropna(subset=["updated_timestamp"])

    if df.empty:
        st.warning("No valid transaction dates found for timeline.")
        return None

    timeline = (
        df[df["country_normalized"].notna()]
        .groupby(pd.Grouper(key="updated_timestamp", freq="M"))
        .agg(monthly_spent=("amount", lambda x: pd.to_numeric(x, errors="coerce").sum()))
        .reset_index()
    )

    fig = px.line(
        timeline,
        x="updated_timestamp",
        y="monthly_spent",
        title="✈️ Travel Spending Over Time (€)"
    )
    return fig

# --------------------------
# Optional: Add flags to country names
# --------------------------
def get_flag(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        return f":flag-{country.alpha_2.lower()}:"
    except:
        return ""

# --------------------------
# Streamlit UI Setup
# --------------------------
st.set_page_config(page_title="Travel Whisperer", page_icon="🌍")
st.title("🌍 Travel Whisperer")

# Load data
# transactions_all, accounts_all, together_df_raw = load_data()
transactions_all, _, together_df_raw = load_data()

# User selection (based on raw data)
user_id = st.sidebar.selectbox("Select user ID", sorted(transactions_all["owner_user_id"].unique()))

# Load filtered user data
# user_data = load_user_context(user_id, transactions_all, accounts_all)
user_data = load_user_context(user_id)
transactions_df = user_data["transactions_df"]
user_summary = user_data["travel_summary_df"]
account_balance = user_data["account_balance"]
savings_goal = user_data["savings_goal"]

# Sidebar user info
st.sidebar.markdown(f"👤 **User ID {user_id}**")
st.sidebar.write(f"💰 Account Balance: €{account_balance:.2f}")
st.sidebar.write(f"🎯 Savings Goal: €{savings_goal:.2f}")

# Flag emoji for travel summary
user_summary["flag"] = user_summary["country"].apply(get_flag)

# Travel visualizations
choropleth_df = build_choropleth_df(user_summary)

with st.sidebar.expander("🌍 Travel Visualizations", expanded=False):
    st.plotly_chart(build_choropleth_map(choropleth_df), use_container_width=True)
    st.plotly_chart(build_spending_barchart(choropleth_df), use_container_width=True)

with st.sidebar.expander("📆 Travel Trends Over Time", expanded=False):
    timeline_fig = build_travel_timeline(transactions_df)
    if timeline_fig:
        st.plotly_chart(timeline_fig, use_container_width=True)

# Display travel summary
st.subheader("🔍 Travel Summary")
st.dataframe(user_summary)

# Travel goal input
dest = st.text_input("Where would you like to travel next?", value="Portugal")

# Travel tone messaging
total_trips = user_summary["total_transactions"].sum()
if total_trips > 50:
    st.info("✈️ Looks like you're a frequent traveler—we’ve tailored these suggestions just for your lifestyle.")
elif total_trips > 10:
    st.info("🌍 You clearly enjoy occasional travel—here's how to plan your next adventure.")
else:
    st.info("🧭 Getting started with travel? We’ve got some ideas for your first great trip.")


# Travel spending analysis
import re

@st.cache_data
def load_deeplink_json():
    import json
    with open("data/deeplinks.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.json_normalize(data)


def enrich_recommendation(text, deeplink_df=None):
    PRODUCT_KEYWORDS = {
        "travel insurance": "https://together.bunq.com/d/travel-insurance",
        "travel cards": "https://together.bunq.com/d/bunq-abroad",
        "savings accounts": "https://together.bunq.com/d/sub-accounts",
        "AutoSave": "https://together.bunq.com/d/autosave"
    }

    def find_deeplink_url(phrase):
        if deeplink_df is not None and "web_description" in deeplink_df.columns:
            match = deeplink_df[deeplink_df["web_description"].str.lower().str.contains(phrase.lower(), na=False)]
            if not match.empty:
                return match.iloc[0].get("deeplink")  # or "url" if that's what your field is called
        return PRODUCT_KEYWORDS.get(phrase)

    for phrase in PRODUCT_KEYWORDS:
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        url = find_deeplink_url(phrase)
        if url:
            text = pattern.sub(f"[**{phrase}**]({url})", text)

    return text

# Trigger agent analysis
if st.button("🔍 Analyze Travel Spending"):
    together_df = pd.read_pickle("data/together_topics_embedded.pkl")
    deeplink_df = pd.read_pickle("data/deeplinks_embedded.pkl")

    with st.spinner("Analyzing your travel history..."):
        result = travel_ai_agent(
            user_id=str(user_id),
            user_summary_df=user_summary,
            account_balance=account_balance,
            savings_goal=savings_goal,
            together_df=together_df,
            deeplink_df=deeplink_df,
            travel_goal=dest
        )

    st.subheader("🤖 Recommendation")
    # st.write(result["output"]["recommendation"])
    deeplink_df_raw = load_deeplink_json()
    enriched = enrich_recommendation(result["output"]["recommendation"], deeplink_df_raw)
    st.markdown(enriched)

    if result["output"].get("together_topic"):
        st.markdown("**🔗 Related Help**")
        st.write(result['output']['together_topic'].splitlines()[0])
        st.markdown(f"[Open article]({result['output']['together_link']})")
        with st.expander("🔎 View full article"):
            st.write(result['output']['together_topic'])
    else:
        st.info("No related Together article found.")

    if result["output"].get("deeplink_action") and result["output"].get("deeplink_url"):
        st.markdown("**🚀 Quick Action**")
        st.markdown(f"[{result['output']['deeplink_action']}]({result['output']['deeplink_url']})", unsafe_allow_html=True)
