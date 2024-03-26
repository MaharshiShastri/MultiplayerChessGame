
class Move:

    def __init__(self, initial, final):
        # initial and final are squares
        self.initial = initial
        self.final = final
        
    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final

    def has_moved(self):
        if self.initial == self.final:
            return 0
        return 1
    
