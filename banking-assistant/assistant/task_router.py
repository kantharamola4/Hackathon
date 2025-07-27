import requests
from .flows.loan import handle_loan
from .flows.block_card import handle_block_card
from .flows.account_query import handle_account_query

API_URL = "http://127.0.0.1:5000"

class TaskRouter:
    def __init__(self, context, token):
        self.context = context
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}

    def route(self, intent, entities, user_input):
        if intent == "apply_loan":
            return handle_loan(self.context, user_input, self.headers)
        if intent == "block_card":
            return handle_block_card(self.context, user_input, self.headers)
        if intent == "account_query":
            return handle_account_query(self.context, user_input, self.headers)
        return "Sorry, I can't handle that request. Please contact the banking assistant."
