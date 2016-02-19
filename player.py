import random
from night import Night


class CardSlot:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Player(CardSlot):
    def __init__(self, name, inform=lambda msg, statement: None, ask=lambda msg, options: 0):
        self.name = name
        self.active = True
        self.inform_me = inform
        self.ask_me = ask

    def inform(self, msg, statement):
        self.inform_me(msg, statement)

    def select(self, msg, options):
        option = self.ask_me(msg, options)
        return option


class Center(CardSlot):
    def __init__(self, id):
        self.name = 'center%s' % id
        self.active = False


class AIPlayer(CardSlot):
    def __init__(self, name, roles, players):
        self.name = name
        self.active = True
        self.night = Night(roles, players+[self])

    def inform(self, msg, statement):
        self.night.incorporate(statement)
        print self.night

    def select(self, msg, options):
        return random.choice(options)
