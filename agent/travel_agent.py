# agent/travel_agent.py

from agent.llm import build_prompt, generate_recommendation_from_llm
from agent.topic_rag_agent import recommend_together_topic
from agent.mcp_format import build_mcp_context

def match_deeplink_to_recommendation(recommendation, deeplink_df):
    """
    Naive fuzzy matching of LLM output to available deeplink actions.
    Ideally replaced by embedding-based similarity search.
    """
    if deeplink_df is None or len(deeplink_df) == 0:
        return None

    for _, row in deeplink_df.iterrows():
        if row.get("label") and row["label"].lower() in recommendation.lower():
            return {
                "action": row["label"],
                "url": row["url"]
            }
    return None

def travel_ai_agent(
    user_id,
    user_summary_df,
    account_balance,
    savings_goal,
    together_df,
    deeplink_df,
    travel_goal=None  # new optional param
):
    # Build prompt for LLM
    prompt = build_prompt(
        user_summary_df=user_summary_df,
        account_balance=account_balance,
        savings_goal=savings_goal,
        travel_goal=travel_goal
    )

    # Generate main recommendation from LLM
    recommendation = generate_recommendation_from_llm(prompt)

    # Find relevant Together article (RAG-style)
    topic, link = recommend_together_topic(recommendation, together_df)

    # Find deeplink action (fuzzy or embedding match)
    deeplink_data = match_deeplink_to_recommendation(recommendation, deeplink_df)
    deeplink_action = deeplink_data["action"] if deeplink_data else None
    deeplink_url = deeplink_data["url"] if deeplink_data else None

    return {
        "identity": {
            "name": "Travel Whisperer",
            "role": "financial travel assistant",
            "version": "1.1"
        },
        "user": {
            "id": user_id,
            "balance_eur": account_balance,
            "savings_goal_eur": savings_goal
        },
        "context": {
            "travel_summary": user_summary_df.to_dict(orient="records"),
            "goal_destination": travel_goal or ""
        },
        "task": {
            "type": "recommendation",
            "description": "Generate a travel-related financial suggestion with actionable tips"
        },
        "output": {
            "recommendation": recommendation,
            "together_topic": topic,
            "together_link": link,
            "deeplink_action": deeplink_action,
            "deeplink_url": deeplink_url
        }
    }
