import requests

API_URL = "http://127.0.0.1:5000"

def handle_account_query(context, user_input, headers):
    # For demo, just return a mock summary from backend
    # You can add more advanced queries here
    resp = requests.get(f"{API_URL}/account_summary", headers=headers)
    if resp.status_code == 200:
        summary = resp.json()
        context.reset()
        return f"Your last 5 transactions: {summary['transactions']}\nCurrent balance: {summary['balance']}"
    return f"Error: {resp.json().get('msg', 'Failed to fetch account summary.')}"
