class ContextualMemory:
    def __init__(self):
        self.chat_history = []
        self.last_context = None

    def add_turn(self, question, answer, context):
        self.chat_history.append((question, answer))
        self.last_context = context

    def get_last_context(self):
        return self.last_context

    def get_history(self):
        return self.chat_history
