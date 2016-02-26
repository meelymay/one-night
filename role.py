from statement import *

VILLAGER = 'villager'
WEREWOLF = 'werewolf'
ROBBER = 'robber'
TROUBLEMAKER = 'troublemaker'
SEER = 'seer'
INSOMNIAC = 'insomniac'
MASON = 'mason'
HUNTER = 'hunter'
DRUNK = 'drunk'
MINION = 'minion'
TANNER = 'tanner'
DOPPLEGANGER = 'doppleganger'

ORDER = [DOPPLEGANGER,
         WEREWOLF,
         MINION,
         MASON,
         SEER,
         ROBBER,
         TROUBLEMAKER,
         DRUNK,
         INSOMNIAC]

SWAPPERS = {
    None: ORIGINAL,
    DOPPLEGANGER: AFTER_DOPPLE,
    ROBBER: AFTER_ROBBER,
    TROUBLEMAKER: AFTER_TROUBLEMAKER,
    DRUNK: FINAL
}


class Role:
    def __init__(self, name):
        self.name = name
        self.is_swapper = name in SWAPPERS

    def __eq__(self, o):
        return str(self) == str(o)

    def __hash__(self):
        return self.name.__hash__()

    def __str__(self):
        return self.name
