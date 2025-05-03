def build_mcp_context(user_id, user_summary_df, account_balance, savings_goal, agent_output, travel_goal=None):
    """
    Formats a full AI agent session into a Model Context Protocol (MCP)-style dictionary.
    """
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
            "recommendation": agent_output.get("recommendation"),
            "together_topic": agent_output.get("together_topic"),
            "together_link": agent_output.get("together_link"),
            "deeplink_action": agent_output.get("deeplink_action"),
            "deeplink_url": agent_output.get("deeplink_url")
        }
    }
