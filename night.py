import assignment
from role import *
from statement import *


class Night:
    def __init__(self, roles, players):
        empty_ass = {}
        for p in players:
            empty_ass[p] = None
        self.assignments = {}
        for state in ASSIGNMENT_STATES:
            self.assignments[state] = assignment.Assignment(empty_ass, roles)
        self.roles = roles
        self.swaps = {}
        self.statements = {}

    def __str__(self):
        s = ''
        s += 'Originals:\n' + str(self.assignments[ORIGINAL])
        s += 'Swaps:\n'
        for swap in self.swaps.values():
            s += '\t%s\n' % swap
        s += 'Finals:\n' + str(self.assignments[FINAL])
        return s

    def deep_copy(self):
        n = Night(self.roles, self.players)
        n.assignments = {}
        for state in ASSIGNMENT_STATES:
            n.assignments = self.assignments[state].copy()
        n.swaps = dict(self.swaps)
        n.statements = dict(self.statements)
        return n

    def incorporate(self, statement, credibility=100, overwrite=False):
        if not self.is_consistent(statement) and not overwrite:
            return False

        if statement.type == SWAP:
            self.swaps[statement.swapper] = statement
        elif statement.type in ASSIGNMENT_STATES:
            a = self.assignments[statement.type]
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
        originals = originals if originals else self.assignments[ORIGINAL].copy()

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
                if not self.assignments[ORIGINAL].has_role(swap.swapper):
                    print 'There is no %s in the game yet.' % swap.swapper
                    return False
                if swap.swapper == ROBBER and not self.assignments[ORIGINAL].player_is_role(swap.p1, ROBBER):
                    print 'Robber must swap himself.'
                    return False
            if self.has_all_swaps(swaps=swaps):
                if not self.assignments[ORIGINAL].play_swaps(swaps).matches(self.assignments[FINAL]):
                    return False
            return True

        p = statement.player
        r = statement.role

        if statement.type in ASSIGNMENT_STATES:
            assignments = self.assignments[statement.type].copy()
            if not assignments.player_is_role(p, r, flex=True):
                print '%s is the %s, not the %s (%s).' % (p, assignments.get(p), r, ADVERB[statement.type])
                return False
            assignments.assign(p, r)
            if not assignments.consistent_role(r):
                print 'There are too many %ss.' % r
                return False
            if (statement.type == ORIGINAL and self.has_all_swaps(originals=assignments) and
               not assignments.play_swaps(self.swaps).matches(self.assignments[FINAL])):
                print 'Swaps after changing originals are inconsistent.'
                return False
            elif (statement.type == FINAL and
                  self.has_all_swaps() and
                  not self.assignments[ORIGINAL].play_swaps(self.swaps).matches(assignments)):
                print 'Swaps are inconsistent with new finals.'
                return False
            return True

        raise Exception('Unknown statement type %s' % statement)
