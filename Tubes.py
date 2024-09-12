
class Tubes(list):

    def __init__(self, tubes):
        super().__init__(tubes)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if len(self[i]) != len(other[i]):
                return False
            for j in range(len(self[i])):
                if self[i][j] != other[i][j]:
                    return False
        return True

    def __hash__(self):
        string = ""
        for tube in self:
            string += "_" + '.'.join(str(item) for item in tube)
        return hash(string)

