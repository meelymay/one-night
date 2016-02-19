SWAP = 0
ORIGINAL = 1
AFTER_DOPPLE = 2
AFTER_ROBBER = 3
AFTER_TROUBLEMAKER = 4
FINAL = 5

ASSIGNMENT_STATES = [
    ORIGINAL,
    AFTER_DOPPLE,
    AFTER_ROBBER,
    AFTER_TROUBLEMAKER,
    FINAL
]

ADVERB = {
    ORIGINAL: 'originally',
    AFTER_DOPPLE: 'after the Doppleganger',
    AFTER_ROBBER: 'after the Robber',
    AFTER_TROUBLEMAKER: 'after the Troublemaker',
    FINAL: 'finally'
}

class Statement:
    def __init__(self, speaker):
        self.speaker = speaker

    def __eq__(self, o):
        return False not in [self.type == o.type,
                             self.player == o.player,
                             self.role == o.role]

    def __hash__(self):
        return hash(self.type) + 123*hash(self.player) + 1117*hash(self.role)


class Swap(Statement):
    def __init__(self, swapper, p1, p2):
        self.swapper = swapper
        self.p1 = p1
        self.p2 = p2
        self.type = SWAP

    def __eq__(self, o):
        return False not in [self.type == o.type,
                             self.swapper == o.swapper,
                             self.p1 == o.p1,
                             self.p2 == o.p2]

    def __hash__(self):
        return hash(self.swapper) + hash(self.p1)*123 + hash(self.p2)*1117

    def __str__(self):
        return '%s swaps %s for %s' % (self.swapper, self.p1, self.p2)


class RoleClaim(Statement):
    def __init__(self, player, role, state):
        self.player = player
        self.role = role
        self.type = state

    def __str__(self):
        return '%s was the %s (%s)' % (self.player, self.role, ADVERB[self.type])
