import player
from role import *
from statement import *


class Night:
    def __init__(self, roles, players):
        self.originals = {}
        self.roles = roles
        for p in players:
            self.originals[p] = None
        self.finals = dict(self.originals)
        self.swaps = {}
        self.statements = {}

    def __str__(self):
        s = ''
        s += 'Originals:\n'
        for p in self.originals:
            s += '\t%s = %s\n' % (p, self.originals[p])
        s += 'Swaps:\n'
        for swap in self.swaps.values():
            s += '\t%s\n' % swap
        s += 'Finals:\n'
        for p in self.finals:
            s += '\t%s = %s\n' % (p, self.finals[p])
        return s

    def incorporate(self, statement, credibility=100, overwrite=False):
        if not self.is_consistent(statement) and not overwrite:
            return False

        if statement.type == SWAP:
            self.swaps[statement.swapper] = statement
        if statement.type in [FINAL, ORIGINAL]:
            a = self.finals if statement.type == FINAL else self.originals
            p = statement.player
            r = statement.role
            a[p] = r

        # if self.has_all_swaps():
        #     self.finals = self.play_swaps()

        self.statements[statement] = credibility
        return True

    def has_all_swaps(self, swaps=None, originals=None):
        swaps = swaps if swaps else self.swaps
        originals = originals if originals else dict(self.originals)

        centers = [originals[x] for x in originals if not x.active]
        for r in filter(lambda x: x in self.roles, SWAPPERS):
            if r not in centers and r not in swaps:
                return False
        return True

    def play_swaps(self, swaps=None, originals=None):
        swaps = swaps if swaps else self.swaps
        originals = originals if originals else dict(self.originals)

        for r in filter(lambda x: x in self.roles, SWAPPERS):
            if r not in swaps:
                continue
            swap = swaps[r]
            p1 = swap.p1
            p2 = swap.p2

            tmp = originals[p1]
            originals[p1] = originals[p2]
            originals[p2] = tmp

        return originals

    def matches(self, after_swap, finals):
        for p in finals:
            if finals[p] and after_swap[p] and after_swap[p] != finals[p]:
                print 'Finals do not match after swapping!'
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
                if swap.swapper not in self.originals.values():
                    print 'There is no %s in the game yet.' % swap.swapper
                    return False
                if swap.swapper == ROBBER and self.originals[swap.p1] != ROBBER:
                    print 'Robber must swap himself.'
                    return False
            if self.has_all_swaps(swaps=swaps):
                if not self.matches(self.play_swaps(swaps=swaps), self.finals):
                    return False
            return True

        p = statement.player
        r = statement.role

        total_r = len([x for x in self.roles if x == r])
        if statement.type in [FINAL, ORIGINAL]:
            assignments = dict(self.originals) if statement.type == ORIGINAL else dict(self.finals)
            if assignments[p] and assignments[p] != r:
                print '%s is the %s, not the %s (%s).' % (p, assignments[p], r, ADVERB[statement.type])
                return False
            assignments[p] = r
            if len(filter(lambda x: assignments[x] == r, assignments)) > total_r:
                print 'There are already %s %ss.' % (total_r, r)
                return False
            if (statement.type == ORIGINAL and self.has_all_swaps(originals=assignments) and
               not self.matches(self.play_swaps(originals=assignments), self.finals)):
                print 'Swaps after changing originals are inconsistent.'
                return False
            elif (statement.type == FINAL and
                  self.has_all_swaps() and
                  not self.matches(self.play_swaps(), assignments)):
                print 'Swaps are inconsistent with new finals.'
                return False
            return True

        raise Exception('Unknown statement type %s' % statement)
