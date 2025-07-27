import random
from datetime import datetime

# Simulated in-memory user database
USERS = {
    'alice': {
        'accounts': [
            {'type': 'savings', 'balance': 2350, 'transactions': [
                {'amount': -100, 'desc': 'Grocery', 'date': '2025-07-20'},
                {'amount': 500, 'desc': 'Salary', 'date': '2025-07-18'},
                {'amount': -50, 'desc': 'Coffee', 'date': '2025-07-17'},
                {'amount': -200, 'desc': 'Rent', 'date': '2025-07-15'},
                {'amount': 100, 'desc': 'Refund', 'date': '2025-07-14'},
            ]},
        ],
        'cards': {
            'credit': {'blocked': False, 'number': '1234-5678-9012-3456'},
            'debit': {'blocked': False, 'number': '9876-5432-1098-7654'}
        },
        'loans': []
    }
}

# Helper to get user (simulate auth)
def get_user(username):
    return USERS.get(username)

def submit_loan_application(username, loan_type, amount, tenure=None):
    user = get_user(username)
    if not user:
        return {'success': False, 'msg': 'User not found.'}
    # Simulate eligibility check
    if int(amount) > 1000000:
        return {'success': False, 'msg': 'Amount exceeds eligibility.'}
    loan_id = f"LN{random.randint(1000,9999)}"
    loan = {
        'id': loan_id,
        'type': loan_type,
        'amount': amount,
        'tenure': tenure or '5 years',
        'status': 'submitted',
        'applied_on': datetime.now().strftime('%Y-%m-%d')
    }
    user['loans'].append(loan)
    return {'success': True, 'loan': loan}

def block_card(username, card_type):
    user = get_user(username)
    if not user:
        return {'success': False, 'msg': 'User not found.'}
    card = user['cards'].get(card_type)
    if not card:
        return {'success': False, 'msg': f'{card_type.title()} card not found.'}
    if card['blocked']:
        return {'success': False, 'msg': f'{card_type.title()} card already blocked.'}
    card['blocked'] = True
    return {'success': True, 'msg': f'{card_type.title()} card blocked successfully.', 'card_number': card['number']}

def get_account_summary(username, account_type='savings'):
    user = get_user(username)
    if not user:
        return {'success': False, 'msg': 'User not found.'}
    for acc in user['accounts']:
        if acc['type'] == account_type:
            txns = acc['transactions'][-5:][::-1]
            txns_fmt = [f"{t['date']}: {'+' if t['amount']>0 else ''}{t['amount']} {t['desc']}" for t in txns]
            return {
                'success': True,
                'transactions': txns_fmt,
                'balance': f"${acc['balance']}"
            }
    return {'success': False, 'msg': f'{account_type.title()} account not found.'}

def get_loan_status(username):
    user = get_user(username)
    if not user:
        return {'success': False, 'msg': 'User not found.'}
    return {'success': True, 'loans': user['loans']}

def unblock_card(username, card_type):
    user = get_user(username)
    if not user:
        return {'success': False, 'msg': 'User not found.'}
    card = user['cards'].get(card_type)
    if not card:
        return {'success': False, 'msg': f'{card_type.title()} card not found.'}
    if not card['blocked']:
        return {'success': False, 'msg': f'{card_type.title()} card is not blocked.'}
    card['blocked'] = False
    return {'success': True, 'msg': f'{card_type.title()} card unblocked successfully.', 'card_number': card['number']}
