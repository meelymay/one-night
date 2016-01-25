SWAP = 0
ORIGINAL = 1
FINAL = 2

ADVERB = {
    ORIGINAL: 'originally',
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


class Original(Statement):
    def __init__(self, player, role):
        self.player = player
        self.role = role
        self.type = ORIGINAL

    def __str__(self):
        return '%s started as the %s' % (self.player, self.role)


class Final(Statement):
    def __init__(self, player, role):
        self.player = player
        self.role = role
        self.type = FINAL

    def __str__(self):
        return '%s is now the %s' % (self.player, self.role)
