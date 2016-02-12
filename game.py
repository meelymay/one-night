import random
from role import *
from player import Player, Center
from assignment import Assignment
from collections import defaultdict


class Game:
    def __init__(self, players, roles):
        if len(roles) != len(players) + 3:
            raise Exception('you done fd up. %s +3 != %s' % (players, roles))

        self.roles = [Role(r) for r in roles]
        self.players = [Player(p.name, inform=p.inform, ask=p.ask) for p in players] + [Center(i) for i in range(3)]
        self.assignment = Assignment({}, roles)
        self.assign()
        self.inform_players()
        print self.assignment

    def assign(self):
        self.originals = {}
        roles = self.roles[:]
        for player in self.players:
            ri = random.randint(0, len(roles) - 1)
            self.assignment.assign(player, roles[ri])
            self.originals[player] = roles[ri]
            del roles[ri]

    def inform_players(self):
        for player in self.players:
            if player.active:
                player.inform(player, self.assignment.get(player))

    def active_players(self):
        return [p for p in self.players if p.active]

    def get_players_for_role(self, role, solo=True):
        ps = filter(lambda x: self.assignment.get(x) == role and x.active, self.players)
        print 'Players for', role, [p.name for p in ps]
        if solo and len(ps) > 1:
            raise Exception('There should only be one %s.' % role)
        return ps

    def vote(self):
        votes = {}
        for player in self.active_players():
            choice = player.select(self.active_players() + [None])
            if not choice:
                return None
            else:
                votes[player.name] = choice.name
        return votes

    def play_night(self):
        self.current = self.assignment.copy()
        r = DOPPLEGANGER
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            opponent = player.select(self.active_players())
            self.dopplegang = self.current.get(opponent)

        r = WEREWOLF
        ps = self.get_players_for_role(r, solo=False)
        for player in ps:
            for opponent in ps:
                if player != opponent:
                    player.inform(opponent, WEREWOLF)
            if len(ps) == 1:
                opponent = player.select([p for p in self.players if not p.active])
                player.inform(opponent, self.current.get(opponent))

        r = MINION
        werewolves = ps
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            for w in werewolves:
                player.inform(w, WEREWOLF)

        r = MASON
        ps = self.get_players_for_role(r, solo=False)
        for player in ps:
            for opponent in ps:
                if player != opponent:
                    player.inform(opponent, MASON)

        r = SEER
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            opponents_card = "A single opponent's card."
            center_card = "Two cards from the center."
            choice = player.select([opponents_card, center_card])
            active = choice == opponents_card
            opponent = player.select([p for p in self.players if p.active == active])
            player.inform(opponent, self.current.get(opponent))
            if not active:
                opponent = player.select([p for p in self.players if p.active == active])
                player.inform(opponent, self.current.get(opponent))

        r = ROBBER
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            opponent = player.select([p for p in self.players if p.active])
            opponent_role = self.current.get(opponent)
            player_role = self.current.get(player)
            player.inform(opponent, opponent_role)
            self.current.assign(player, opponent_role)
            self.current.assign(opponent, player_role)

        r = TROUBLEMAKER
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            opp1 = player.select(self.active_players())
            opp2 = player.select([p for p in self.players if p.active and p != opp1])
            opp1_role = self.current.get(opp1)
            self.current.assign(opp1, self.current.get(opp2))
            self.current.assign(opp2, opp1_role)

        r = DRUNK
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            center = player.select([p for p in self.players if not p.active])
            center_role = self.current.get(center)
            self.current.assign(center, self.current.get(player))
            self.current.assign(player, center_role)

        r = INSOMNIAC
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            player.inform(player, self.current.get(player))

        print
        print self.current
        return str(self.current)


if __name__ == '__main__':
    g = Game(['amelia', 'dan', 'kavan', 'mike', 'connor', 'howard'],
             [WEREWOLF, WEREWOLF, VILLAGER, INSOMNIAC, ROBBER, TROUBLEMAKER, SEER, MINION, DRUNK])
    g.play_night()
