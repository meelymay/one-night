import random
import role
import player
import statement

class Game:
    def __init__(self, roles, players):
        if len(roles) != len(players) + 3:
            raise 'you done fd up'

        self.roles = [role.Role(r) for r in roles]
        self.players = [player.Player(p) for p in players]
        self.assign()

    def assign(self):
        self.originals = {}
        roles = roles[:]
        for player in self.players:
            ri = random.randint(0, len(roles) - 1)
            self.originals[player] = roles[ri]
            del roles[ri]

    def inform_players(self):
        for player in self.players:
            player.inform(self.originals[player])

    def play_night(self):
        for role in role.ORDER:
