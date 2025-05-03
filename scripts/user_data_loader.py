# scripts/user_data_loader.py

import pandas as pd
from agent.utils import parse_balance_column

def load_user_context(user_id):
    # Load datasets here directly
    transactions_df = pd.read_csv("data/transactions_cleaned.csv")
    accounts_df = pd.read_csv("data/monetary_accounts.csv")

    # --- Filter user transactions ---
    user_tx = transactions_df[transactions_df["owner_user_id"] == int(user_id)]
    user_tx = user_tx[user_tx["country_normalized"].notna()]

    travel_summary = (
        user_tx.groupby("country_normalized")
        .agg(
            total_transactions=("amount", "count"),
            total_spent=("amount", lambda x: pd.to_numeric(x, errors="coerce").sum())
        )
        .reset_index()
        .rename(columns={"country_normalized": "country"})
        .sort_values(by="total_spent", ascending=False)
    )

    # --- Filter user accounts ---
    accounts_df = parse_balance_column(accounts_df)
    user_accounts = accounts_df[accounts_df["owner_user_id"] == int(user_id)]
    account_balance = user_accounts["balance_eur"].sum()

    # --- Savings goal ---
    if "SavingsGoal" in user_accounts.columns:
        savings_series = pd.to_numeric(user_accounts["SavingsGoal"], errors="coerce")
        savings_goal = savings_series.dropna().max() if not savings_series.dropna().empty else 5000.0
    else:
        savings_goal = 5000.0

    return {
        "user_id": user_id,
        "travel_summary_df": travel_summary,
        "transactions_df": user_tx,
        "account_balance": account_balance,
        "savings_goal": savings_goal
    }
