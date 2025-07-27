# This is a placeholder for Rasa NLU or other open-source NLU integration
# For demo, use simple keyword-based intent/entity extraction

def parse(text):
    text = text.lower()
    if 'loan' in text:
        return {'intent': 'apply_loan', 'entities': {}}
    if 'block' in text and 'card' in text:
        return {'intent': 'block_card', 'entities': {}}
    if any(x in text for x in ['balance', 'statement', 'transaction']):
        return {'intent': 'account_query', 'entities': {}}
    return {'intent': 'unknown', 'entities': {}}
