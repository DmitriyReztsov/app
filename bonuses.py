from behavior_classes import IBonus


class BonusLine(IBonus):
    STANDARD_POINTS: int = 3

    def _calculate_points(self, cells_num: int) -> None:
        return (
            cells_num
            if cells_num >= self.STANDARD_POINTS
            else self.INIT_POINTS
        )


class BonusCross(IBonus):
    STANDARD_POINTS: int = 5

    def _calculate_points(self, cells_num: int) -> None:
        return (
            cells_num
            if cells_num == self.STANDARD_POINTS
            else self.INIT_POINTS
        )
