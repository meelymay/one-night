class CardSlot:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Player(CardSlot):
    def __init__(self, name, inform=lambda x, y: None, ask=lambda x, y: 0):
        self.name = name
        self.active = True
        self.inform_me = inform
        self.as_mek = ask

    def inform(self, player, role):
        print '%s discovers: Player %s is %s.' % (self, player, role)
        self.inform_me(player, role)

    def select(self, options):
        option = self.ask_me(options)
        return option


class Center(CardSlot):
    def __init__(self, id):
        self.name = 'center%s' % id
        self.active = False
