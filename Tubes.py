class Tubes(list):

    def __init__(self, tubes):
        """
        Initializes the Tubes object, which is a subclass of the built-in list, to store a collection of tubes.

        Parameters:
        tubes (list): A list of tubes (each tube being a list) that represents the initial state of the puzzle.
        """
        super().__init__(tubes)

    def __eq__(self, other):
        """
        Checks for equality between two Tubes objects. Two Tubes objects are equal if they contain the same tubes
        in the same order, with the same contents.

        Parameters:
        other (Tubes): Another Tubes object to compare against.

        Returns:
        bool: True if both Tubes objects are equal, False otherwise.
        """
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
        """
        Generates a unique hash value for the Tubes object based on its contents. This allows Tubes objects to be used
        in hashable collections like sets and dictionaries.

        Returns:
        int: The hash value representing the Tubes object.
        """
        string = ""
        for tube in self:
            string += "_" + '.'.join(str(item) for item in tube)
        return hash(string)
