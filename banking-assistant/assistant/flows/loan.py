import requests

API_URL = "http://127.0.0.1:5000"

def handle_loan(context, user_input, headers):
    # Slot-filling for loan_type and amount
    if not context.slots.get('loan_amount'):
        words = user_input.split()
        for w in words:
            if w.isdigit():
                context.slots['loan_amount'] = w
                break
        if not context.slots.get('loan_amount'):
            return "What loan amount do you need?"
    if not context.slots.get('loan_type'):
        if "personal" in user_input:
            context.slots['loan_type'] = "personal"
        elif "home" in user_input:
            context.slots['loan_type'] = "home"
        else:
            return "Is this a personal or home loan?"
    # Submit to backend
    data = {"loan_type": context.slots['loan_type'], "amount": context.slots['loan_amount']}
    resp = requests.post(f"{API_URL}/loan", json=data, headers=headers)
    if resp.status_code == 200:
        context.reset()
        return "Your loan application has been submitted!"
    return f"Error: {resp.json().get('msg', 'Failed to submit loan application.')}"
