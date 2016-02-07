from role import SWAPPERS


class Assignment:
    def __init__(self, players_to_roles, all_roles):
        self.all_roles = all_roles
        self.originals = dict(players_to_roles)

    def play_swaps(self, swaps):
        originals = dict(self.originals)

        for r in filter(lambda x: x in self.all_roles, SWAPPERS):
            if r not in swaps:
                continue
            swap = swaps[r]
            p1 = swap.p1
            p2 = swap.p2

            tmp = originals[p1]
            originals[p1] = originals[p2]
            originals[p2] = tmp

        return Assignment(originals, self.all_roles)

    def has_role(self, role):
        return role in self.originals.values()

    def player_is_role(self, player, role, flex=False):
        return (self.get(player) is None and flex) or self.get(player) == role

    def assign(self, player, role):
        self.originals[player] = role

    def consistent_role(self, role):
        total_r = len([x for x in self.all_roles if x == role])
        return len(filter(lambda x: self.get(x) == role, self.originals)) <= total_r

    def get(self, player):
        return self.originals[player]

    def centers(self):
        return [self.get(x) for x in self.originals if not x.active]

    def matches(self, other):
        for p in other.originals:
            if other.get(p) and self.get(p) and self.get(p) != other.get(p):
                return False
        return True

    def copy(self):
        return Assignment(dict(self.originals), self.all_roles)

    def __str__(self):
        s = ''
        for p in self.originals:
            s += '%s: %s\n' % (p, self.originals[p])
        return s
