import random
from role import *
from player import Player, AIPlayer, Center
from statement import *
from assignment import Assignment
from collections import defaultdict


class Game:
    def __init__(self, players, roles, include_ai=False):
        if len(roles) != len(players) + 3 + (1 if include_ai else 0):
            raise Exception('you done fd up. %s != %s' % (players, roles))

        self.roles = [Role(r) for r in roles]
        self.players = [Player(p.name, inform=p.inform, ask=p.ask) for p in players] + [Center(i) for i in range(3)]
        self.players.append(AIPlayer('HAL', self.roles, self.players))
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
                msg = 'You look at your card.'
                statement = Original(player, self.assignment.get(player))
                player.inform(msg, statement)

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
            msg = 'Who do you want to kill?'
            choice = player.select(msg, self.active_players() + [None])
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
            msg = '%s, wake up. Select one other player\'s role to impersonate.' % r
            opponent = player.select(msg, self.active_players())
            self.dopplegang = self.current.get(opponent)

        r = WEREWOLF
        ps = self.get_players_for_role(r, solo=False)
        for player in ps:
            for opponent in ps:
                if player != opponent:
                    msg = '%s, wake up. See the other werewolves.' % r
                    player.inform(msg, Original(opponent, WEREWOLF))
            if len(ps) == 1:
                msg = 'Werewolf, wake up. You may choose a card from the center to look at.'
                opponent = player.select(msg, [p for p in self.players if not p.active])
                player.inform('You learn:', Original(opponent, self.current.get(opponent)))

        r = MINION
        werewolves = ps
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            for w in werewolves:
                msg = '%s, wake up. See the werewolves.' % r
                player.inform(msg, Original(w, WEREWOLF))

        r = MASON
        ps = self.get_players_for_role(r, solo=False)
        for player in ps:
            for opponent in ps:
                if player != opponent:
                    msg = '%s, wake up. See the other masons.' % r
                    player.inform(msg, Original(opponent, MASON))

        r = SEER
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            opponents_card = 'A single opponent\'s card.'
            center_card = 'Two cards from the center.'
            msg = 'Seer, wake up. You may choose to look at one other player\'s card or two cards from the center.'
            choice = player.select(msg, [opponents_card, center_card])
            active = choice == opponents_card
            msg = 'Seer, select a card to look at.'
            opponent = player.select(msg, [p for p in self.players if p.active == active])
            player.inform('You learn', Original(opponent, self.current.get(opponent)))
            if not active:
                opponent = player.select(msg, [p for p in self.players if p.active == active])
                player.inform('You learn:', Original(opponent, self.current.get(opponent)))

        r = ROBBER
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            msg = 'Robber, wake. You may swap cards with one other player.'
            opponent = player.select(msg, [p for p in self.players if p.active] + [None])
            if opponent:
                opponent_role = self.current.get(opponent)
                player_role = self.current.get(player)
                player.inform('You look at your new card.', Final(opponent, opponent_role))
                self.current.assign(player, opponent_role)
                self.current.assign(opponent, player_role)

        r = TROUBLEMAKER
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            msg = '%s, wake up. You may swap the cards of two other players.'
            opp1 = player.select(msg, self.active_players() + [None])
            if opp1:
                msg = '...and the other player.'
                opp2 = player.select(msg, [p for p in self.players if p.active and p != opp1])
                opp1_role = self.current.get(opp1)
                self.current.assign(opp1, self.current.get(opp2))
                self.current.assign(opp2, opp1_role)

        r = DRUNK
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            msg = '%s, wake up. Select a card from the center to swap with your own.' % r
            center = player.select(msg, [p for p in self.players if not p.active])
            center_role = self.current.get(center)
            self.current.assign(center, self.current.get(player))
            self.current.assign(player, center_role)

        r = INSOMNIAC
        ps = self.get_players_for_role(r)
        if ps:
            player = ps[0]
            msg = '%s, wake up. Look at your card.' % r
            player.inform(msg, Final(player, self.current.get(player)))

        print
        print self.current
        return str(self.current)


if __name__ == '__main__':
    g = Game(['amelia', 'dan', 'kavan', 'mike', 'connor', 'howard'],
             [WEREWOLF, WEREWOLF, VILLAGER, INSOMNIAC, ROBBER, TROUBLEMAKER, SEER, MINION, DRUNK])
    g.play_night()
