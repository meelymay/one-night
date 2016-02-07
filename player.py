class Player:
    def __init__(self, name):
        self.name = name
        self.active = True

    def inform(self, player, role):
    	print '%s discovers: Player %s is %s.' % (self, player, role)

    def select(self, options):
    	return options[0]

    def __str__(self):
        return self.name


class Center(Player):
    def __init__(self, id):
        self.name = 'center%s' % id
        self.active = False
