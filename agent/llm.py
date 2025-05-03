# agent/llm.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def build_prompt(user_summary_df, account_balance, savings_goal, travel_goal=None):
    summary_lines = []
    for _, row in user_summary_df.iterrows():
        summary_lines.append(
            f"- {row['country']}: €{int(row['total_spent'])} across {int(row['total_transactions'])} transactions"
        )
    summary_text = "\n".join(summary_lines)

    goal_text = f"\nThe user is considering a trip to **{travel_goal}** and may want to start saving for it." if travel_goal else ""

    return f"""
You are a smart, friendly AI travel agent and financial assistant.

Your job is to:
1. Analyze the user's spending by country and identify travel interests.
2. Encourage the user to plan their next trip.
3. Recommend a realistic monthly savings plan to reach their travel goal.
4. Highlight how bunq can help (e.g., savings accounts, travel insurance, travel cards).
5. Provide motivating and actionable advice.

User info:
- Account balance: €{account_balance:.2f}
- Savings goal: €{savings_goal:.2f}{goal_text}

Travel spending summary:
{summary_text}

Provide a short, inspiring recommendation (3–5 sentences) in plain language.
"""

def generate_recommendation_from_llm(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant specializing in travel and banking."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content
