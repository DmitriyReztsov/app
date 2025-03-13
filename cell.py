from behavior_classes import ICell


class Cell(ICell):
    VALUE_CHOICES = ["A", "B", "C", "D", "E"]

    def __init__(self):
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.value = None

    # requests
    def get_up(self) -> "ICell":
        return self.up

    def get_down(self) -> "ICell":
        return self.down

    def get_right(self) -> "ICell":
        return self.right

    def get_left(self) -> "ICell":
        return self.left

    def __eq__(self, other: "ICell") -> bool:
        return self.value == other.value

    def __hash__(self):
        return id(self)
