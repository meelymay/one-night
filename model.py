from statement import *


class Model:
    def __init__(self, night):
        self.nights = {night: 1}

    def construct_statement(self, text):
        args = text.split()
        state = args[0]
        if state == SWAP:
            swapper = args[1]
            p1 = args[2]
            p2 = args[3]
            return Swap(swapper, p1, p2)
        elif state in ASSIGNMENT_STATES:
            player = args[1]
            role = args[2]
            return RoleClaim(player, role, state)
        else:
            return None

    def incorporate(self, statement):
        for night in self.nights:
            if not night.incorporate(statement):
                new_night = night.deep_copy()
                new_night.incorporate(statement, overwrite=True)
                self.nights[new_night] = 1

    def __str__(self):
        s = ''
        for n in self.nights:
            s += '{0} ({1})'.format(n, self.nights[n])
        return s
