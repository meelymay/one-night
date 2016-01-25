class Model:
    def __init__(self, night):
        self.nights = {night: 0}

    def incorporate(self, statement):
        for night in nights:
            if not night.incorporate(statement):
                new_night = night.deep_copy()
                new_night.incorporate(statement, overwrite=True)
                self.nights[new_night] = 0
