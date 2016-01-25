class Player:
    def __init__(self, name):
        self.name = name
        self.active = True

    def __str__(self):
        return self.name


class Center(Player):
    def __init__(self, id):
        self.name = 'center%s' % id
        self.active = False
