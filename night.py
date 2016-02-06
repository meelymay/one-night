import assignment
from role import *
from statement import *


class Night:
    def __init__(self, roles, players):
        empty_ass = {}
        for p in players:
            empty_ass[p] = None
        self.originals = assignment.Assignment(empty_ass, roles)
        self.finals = assignment.Assignment(empty_ass, roles)
        self.roles = roles
        self.swaps = {}
        self.statements = {}

    def __str__(self):
        s = ''
        s += 'Originals:\n' + str(self.originals)
        s += 'Swaps:\n'
        for swap in self.swaps.values():
            s += '\t%s\n' % swap
        s += 'Finals:\n' + str(self.finals)
        return s

    def deep_copy(self):
        n = Night(self.roles, self.players)
        n.originals = self.originals.copy()
        n.finals = self.finals.copy()
        n.swaps = dict(self.swaps)
        n.statements = dict(self.statements)
        return n

    def incorporate(self, statement, credibility=100, overwrite=False):
        if not self.is_consistent(statement) and not overwrite:
            return False

        if statement.type == SWAP:
            self.swaps[statement.swapper] = statement
        elif statement.type in [ORIGINAL, FINAL]:
            a = self.finals if statement.type == FINAL else self.originals
            p = statement.player
            r = statement.role
            a.assign(p, r)
        else:
            print 'Statement type %s does not exist.' % statement
            return False

        # if self.has_all_swaps():
        #     self.finals = self.play_swaps()

        self.statements[statement] = credibility
        return True

    # TODO pretty sure has all swaps doesn't work
    def has_all_swaps(self, swaps=None, originals=None):
        swaps = swaps if swaps else self.swaps
        originals = originals if originals else self.originals.copy()

        centers = originals.centers()
        for r in filter(lambda x: x in self.roles, SWAPPERS):
            if r not in centers and r not in swaps:
                return False
        return True

    def is_consistent(self, statement):
        if statement.type == SWAP:
            if statement.swapper in self.swaps and self.swaps[statement.swapper] != statement:
                print 'The %s has already swapped.' % statement.swapper
                return False
            swaps = dict(self.swaps)
            swaps[statement.swapper] = statement
            for swap in swaps.values():
                if not self.originals.has_role(swap.swapper):
                    print 'There is no %s in the game yet.' % swap.swapper
                    return False
                if swap.swapper == ROBBER and not self.originals.player_is_role(swap.p1, ROBBER):
                    print 'Robber must swap himself.'
                    return False
            if self.has_all_swaps(swaps=swaps):
                if not self.originals.play_swaps(swaps).matches(self.finals):
                    return False
            return True

        p = statement.player
        r = statement.role

        if statement.type in [FINAL, ORIGINAL]:
            assignments = self.originals.copy() if statement.type == ORIGINAL else self.finals.copy()
            if not assignments.player_is_role(p, r, flex=True):
                print '%s is the %s, not the %s (%s).' % (p, assignments.get(p), r, ADVERB[statement.type])
                return False
            assignments.assign(p, r)
            if not assignments.consistent_role(r):
                print 'There are too many %ss.' % r
                return False
            if (statement.type == ORIGINAL and self.has_all_swaps(originals=assignments) and
               not assignments.play_swaps(self.swaps).matches(self.finals)):
                print 'Swaps after changing originals are inconsistent.'
                return False
            elif (statement.type == FINAL and
                  self.has_all_swaps() and
                  not self.originals.play_swaps(self.swaps).matches(assignments)):
                print 'Swaps are inconsistent with new finals.'
                return False
            return True

        raise Exception('Unknown statement type %s' % statement)
