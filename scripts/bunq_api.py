# bunq_sandbox_demo.py

import requests


API_KEY = "sandbox_8b1606af23c496bf37f0929dd0c68ad36fae88b075ecfc588495f808" 

BASE_URL = "https://sandbox.public.api.bunq.com/v1"
HEADERS = {
    "X-Bunq-Client-Authentication": API_KEY,
    "X-Bunq-Language": "en_US",
    "X-Bunq-Region": "nl_NL",
    "Content-Type": "application/json"
}

def get_user_id():
    url = f"{BASE_URL}/user"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    user_obj = response.json()["Response"][0]
    user_id = list(user_obj.values())[0]["id"]
    return user_id

def get_monetary_accounts(user_id):
    url = f"{BASE_URL}/user/{user_id}/monetary-account"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    accounts = response.json()["Response"]
    return accounts

def get_account_balance(account_obj):
    acc = list(account_obj.values())[0]
    return acc.get("balance", {}).get("value", "0.00")

def get_account_id(account_obj):
    return list(account_obj.values())[0]["id"]

if __name__ == "__main__":
    user_id = get_user_id()
    print(f"👤 User ID: {user_id}")

    accounts = get_monetary_accounts(user_id)
    for i, acc in enumerate(accounts):
        acc_id = get_account_id(acc)
        balance = get_account_balance(acc)
        print(f"💰 Account {i+1} — ID: {acc_id} — Balance: €{balance}")
