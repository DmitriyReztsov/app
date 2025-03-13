from cell import Cell
from window import Window


class MockedWindow(Window):
    def run(self):
        pass


def test_score():
    a1 = Cell()
    a1.set_value("A")
    a2 = Cell()
    a2.set_value("B")
    a3 = Cell()
    a3.set_value("C")
    b1 = Cell()
    b1.set_value("B")
    b2 = Cell()
    b2.set_value("B")
    b3 = Cell()
    b3.set_value("B")
    c1 = Cell()
    c1.set_value("C")
    c2 = Cell()
    c2.set_value("B")
    c3 = Cell()
    c3.set_value("A")

    a1.right = b1
    a1.up = a2

    a2.down = a1
    a2.right = b2
    a2.up = a3

    a3.right = b3
    a3.down = a2

    b1.left = a1
    b1.up = b2
    b1.right = c1

    b2.down = b1
    b2.left = a2
    b2.up = b3
    b2.right = c2

    b3.down = b2
    b3.left = a3
    b3.right = c3

    c1.left = b1
    c1.up = c2

    c2.down = c1
    c2.left = b2
    c2.up = c3

    c3.down = c2
    c3.left = b3

    window = MockedWindow("gamer")
    window._playground.a1 = a1
    window._playground.dimension = window._playground.Dimension(3, 3)

    window._playground.analyze_playground(window._combinations_list)

    assert window._playground.is_combinations_found() is True

    # horizontal + vertical + cross
    assert window._gamer_score.get_score() == 3 + 3 + 5
