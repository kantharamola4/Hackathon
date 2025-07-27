import requests
from .context_store import ContextStore
from .task_router import TaskRouter
from .fallback import FallbackHandler

API_URL = "http://127.0.0.1:5000"

class DialogueManager:
    def __init__(self, token):
        self.context = ContextStore()
        self.token = token
        self.router = TaskRouter(self.context, token)
        self.fallback = FallbackHandler(self.context)

    def handle_message(self, user_input):
        # Use backend NLU
        resp = requests.post(f"{API_URL}/nlu", json={"text": user_input})
        nlu = resp.json()
        intent = nlu.get('intent')
        entities = nlu.get('entities', {})
        # If intent is unknown, try to use last intent for slot-filling
        if not intent or intent == 'unknown':
            intent = self.context.last_intent
            entities = self.context.last_slots
        else:
            self.context.last_intent = intent
            self.context.last_slots = entities
        if not intent:
            return self.fallback.handle(user_input)
        return self.router.route(intent, entities, user_input)
