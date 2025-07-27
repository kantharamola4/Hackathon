class FallbackHandler:
    def __init__(self, context):
        self.context = context

    def handle(self, user_input):
        # Simple fallback for PoC
        return "I'm sorry, I didn't understand that. Could you please rephrase or provide more details?"
