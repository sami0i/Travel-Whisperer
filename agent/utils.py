import ast
import pandas as pd

def parse_balance_column(accounts_df):
    """
    Safely converts 'AccountBalance' column to float in a new column 'balance_eur'.
    Assumes values are already numeric or numeric strings.
    """
    try:
        accounts_df["balance_eur"] = pd.to_numeric(accounts_df["AccountBalance"], errors="coerce")
    except Exception:
        accounts_df["balance_eur"] = 0.0
    return accounts_df


def get_account_info(user_id, accounts_df):
    accounts_df = parse_balance_column(accounts_df)
    user_accounts = accounts_df[accounts_df["owner_user_id"] == int(user_id)]

    if user_accounts.empty:
        return 0.0, 0.0

    balance_total = user_accounts["balance_eur"].sum()

    # Handle optional SavingsGoal column
    if "SavingsGoal" in user_accounts.columns:
        savings_goal_series = pd.to_numeric(user_accounts["SavingsGoal"], errors="coerce")
        savings_goal = savings_goal_series.dropna().max() if not savings_goal_series.dropna().empty else 5000.0
    else:
        savings_goal = 5000.0

    return balance_total, savings_goal

