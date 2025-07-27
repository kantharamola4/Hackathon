class ContextStore:
    def __init__(self):
        self.state = {}
        self.current_task = None
        self.slots = {}
        self.last_intent = None
        self.last_slots = {}

    def update(self, key, value):
        self.state[key] = value

    def get(self, key, default=None):
        return self.state.get(key, default)

    def reset(self):
        self.state = {}
        self.current_task = None
        self.slots = {}
        self.last_intent = None
        self.last_slots = {}
