from typing import Any

from behavior_classes import ICell, ICombination, IPlayGround
from cell import Cell


class PlayGround(IPlayGround):
    # commands
    def generate_playground(self):
        """предусловия: нет
        постусловия: должен сформироваться список клеток с заполненными
        значениями и соседями
        """
        self.a1 = Cell()
        self.a1.set_value()

        for x in range(self.dimension.x):
            for y in range(self.dimension.y):
                if x == 0 and y == 0:
                    continue
                cell = Cell()
                if x > 0:
                    cell.left = self._get_cell(x - 1, y)
                    cell.left.right = cell
                if y > 0:
                    cell.down = self._get_cell(x, y - 1)
                    cell.down.up = cell
                cell.set_value()

    def _analyze_cell(
        self, cell: "ICell", combinations_list: list[ICombination]
    ) -> None:
        """предусловия: передана ячейка и список комбинаций
        постусловия: найдены комбинации, построенные от ячейки
        """

        for combination in combinations_list:
            combination.check_combination(cell)
            if combination.is_combination():
                self._combi_cells_to_remove.update(
                    combination.get_combi_cells()
                )
            combination.reset_combination()

    def analyze_playground(
        self, combinations_list: list[ICombination]
    ) -> None:
        """предусловия: заполненное поле
        постусловия: поле проанализировано и заполнен список найденных
        комбинаций
        """

        for x in range(self.dimension.x):
            for y in range(self.dimension.y):
                cell = self._get_cell(x, y)
                self._analyze_cell(cell, combinations_list)

    def clean_playground(self) -> None:
        """предусловия: набор ячеек _combi_cells_to_remove заполнен
        постусловия: поле очищено от ячеек в комбинациях"""

        for cell in self._combi_cells_to_remove:
            cell.clean_value()
        self._combi_cells_to_remove.clear()

    def regenerate_playground(self) -> None:
        """предусловия: нет
        постусловия: сгенерировано новое поле"""

        for x in range(self.dimension.x):
            for y in range(self.dimension.y - 1, -1, -1):
                cell = self._get_cell(x, y)
                if cell.value is None:
                    cell.set_value()
                elif cell.down and cell.down.value is None:
                    cell.down.set_value(cell.value)
                    cell.clean_value()
                    cell.set_value()

    # request
    def _get_cell(self, x: str, y: int) -> "ICell":
        """предусловия: координаты находятся в диапазоне допустимых значений
        постусловия: возвращена ячейка по координатам
        """

        if x < 0 or x >= self.dimension.x or y < 0 or y >= self.dimension.y:
            self._get_cell_status = self.GET_CELL_ERR
            return None
        self._get_cell_status = self.GET_CELL_OK
        cell = self.a1
        for _ in range(x):
            cell = cell.get_right()
        for _ in range(y):
            cell = cell.get_up()
        return cell

    def get_cell_by_text_coord(self, text_coord: str) -> "ICell":
        x = ord(text_coord[0].lower()) - ord("a")
        y = int(text_coord[1]) - 1
        return self._get_cell(x, y)

    def get_cell_by_int_coord(self, x: int, y: int) -> "ICell":
        return self._get_cell(x, y)

    def get_plauground_state(self) -> list[Any]:
        """предусловия: поле сгенерировано
        постусловия: сформирован список с копиями значений ячеек по состоянию
        на момент запроса
        """

        values_list = []
        for y in self.dimension.y:
            row_values = []
            for x in self.dimension.x:
                cell = self._get_cell(x, y)
                row_values.append(cell.value)
            values_list.append(row_values)
        return values_list
