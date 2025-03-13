from typing import Generator

from behavior_classes import ICell, ICombination
from bonuses import BonusCross, BonusLine


class CombinationTypes:
    HORIZONTAL_TYPE = "horizontal"
    VERTICAL_TYPE = "vertical"
    CROSS_TYPE = "cross"

    COMBINATIONS_TYPES = [HORIZONTAL_TYPE, VERTICAL_TYPE, CROSS_TYPE]


class HorizontalLineCombination(ICombination):
    DEFAULT_BONUS = BonusLine()

    def _default_template(self) -> Generator:
        """3 ячейки подряд, значит - минимум 2 сравнения
        """

        offset_direction = "right"
        template_completed = False
        compare_completed_counter = 0

        while True:
            if compare_completed_counter == 1:
                template_completed = True
            yield offset_direction, template_completed
            compare_completed_counter += 1

    def check_combination(self, start_cell: "ICell") -> None:
        """предусловие: передана правильная стартовая ячейка
        постусловие: статус 1 если от стартовой ячейки можно построить
        комбинацию, иначе - 2
        """

        compare_with_cell = start_cell
        self._combi_cells.append(start_cell)
        for offset_direction, template_comleted in self._default_template():
            compare_with_cell = getattr(compare_with_cell, offset_direction)
            if compare_with_cell is None or compare_with_cell != start_cell:
                break
            self._combi_cells.append(compare_with_cell)
            if template_comleted:
                self._check_status = self.CHECK_STATUS_OK
        self._bonus.bonus_behavior(len(self._combi_cells))


class VerticalLineCombination(ICombination):
    DEFAULT_BONUS = BonusLine()

    def _default_template(self) -> Generator:
        """3 ячейки подряд, значит - минимум 2 сравнения
        """

        offset_direction = "down"
        template_completed = False
        compare_completed_counter = 0

        while True:
            if compare_completed_counter == 1:
                template_completed = True
            yield offset_direction, template_completed
            compare_completed_counter += 1

    def check_combination(self, start_cell: "ICell") -> None:
        """предусловие: передана правильная стартовая ячейка
        постусловие: статус 1 если от стартовой ячейки можно построить
        комбинацию, иначе - 2
        """

        compare_with_cell = start_cell
        self._combi_cells.append(start_cell)
        for offset_direction, template_comleted in self._default_template():
            compare_with_cell = getattr(compare_with_cell, offset_direction)
            if compare_with_cell is None or compare_with_cell != start_cell:
                break
            self._combi_cells.append(compare_with_cell)
            if template_comleted:
                self._check_status = self.CHECK_STATUS_OK
        self._bonus.bonus_behavior(len(self._combi_cells))


class CrossCombination(ICombination):
    DEFAULT_BONUS = BonusCross()

    def _default_template(self) -> Generator:
        """4 ячейки по одной в каждую сторону
        """

        offset_directions = ["right", "down", "left", "up"]
        template_completed = False
        compare_completed_counter = 0

        while True:
            if compare_completed_counter == 3:
                template_completed = True
            yield (
                offset_directions[compare_completed_counter],
                template_completed,
            )
            compare_completed_counter = (
                (compare_completed_counter + 1) % len(offset_directions)
            )

    def check_combination(self, start_cell: "ICell") -> None:
        """предусловие: передана правильная стартовая ячейка
        постусловие: статус 1 если от стартовой ячейки можно построить
        комбинацию, иначе - 2
        """

        compare_with_cell = start_cell
        self._combi_cells.append(start_cell)
        for offset_direction, template_comleted in self._default_template():
            compare_with_cell = getattr(start_cell, offset_direction)
            if compare_with_cell is None or compare_with_cell != start_cell:
                break
            self._combi_cells.append(compare_with_cell)
            if template_comleted:
                self._check_status = self.CHECK_STATUS_OK
                break
        self._bonus.bonus_behavior(len(self._combi_cells))


def combination_factory(combination_type: str) -> ICombination:
    if combination_type == CombinationTypes.HORIZONTAL_TYPE:
        return HorizontalLineCombination()
    if combination_type == CombinationTypes.VERTICAL_TYPE:
        return VerticalLineCombination()
    if combination_type == CombinationTypes.CROSS_TYPE:
        return CrossCombination()
    raise ValueError("Unknown combination type")
