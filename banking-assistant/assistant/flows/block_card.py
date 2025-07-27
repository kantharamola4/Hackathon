import requests

API_URL = "http://127.0.0.1:5000"

def handle_block_card(context, user_input, headers):
    # Try to fill card_type from user_input or previous slot
    if not context.slots.get('card_type'):
        if "credit" in user_input:
            context.slots['card_type'] = "credit"
        elif "debit" in user_input:
            context.slots['card_type'] = "debit"
        elif user_input.strip() in ["credit", "debit"]:
            context.slots['card_type'] = user_input.strip()
        else:
            return "Is it your credit or debit card you want to block?"
    data = {"card_type": context.slots['card_type']}
    resp = requests.post(f"{API_URL}/block_card", json=data, headers=headers)
    if resp.status_code == 200:
        context.reset()
        return "Your card has been blocked. If this was a mistake, please contact support immediately."
    return f"Error: {resp.json().get('msg', 'Failed to block card.')}"
