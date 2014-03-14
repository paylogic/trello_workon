"""Models for a Trello card."""


class Card(object):
    """Represents a Trello card."""
    card_id = None
    assigned_to = None

    def __init__(self, card_id, assigned_to):
        self.card_id = card_id
        self.assigned_to = assigned_to
