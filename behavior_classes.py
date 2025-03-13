import random
from collections import namedtuple
from typing import Any, Optional


class IWindow:
    def __init__(self, gamer: "IGamer") -> None:
        self._gamer = gamer
        self._combinations_list: list[ICombination]
        self._gamer_score: IScore
        self._playground: IPlayGround
        self._current_step: IStep

        self._create_score()
        self._create_combinations_list()
        self._create_step_stack()
        self._create_playground()
        self.run()

    def _create_combinations_list(self) -> None:
        ...

    def _create_score(self) -> None:
        self._gamer_score = IScore(self._gamer)

    def _create_step_stack(self) -> None:
        self._step_stack = IStepStack()

    def _create_playground(self) -> None:
        """предусловия: нет
        постусловия: создано игровое поле
        """
        ...

    def run(self) -> None:
        """команда. Создает сущности игрового поля. Запускает цикл ввод -
        обработка - вывод результата.
        предусловия: нет
        постусловия: нет
        """
        ...

    def _input_step(self):
        """предусловия: введены корректные координаты ячейки
        посусловия: создан объект Step"""
        ...

    def _start_process(self):
        """предусловия: сделан шаг
        постусловия: проведена замена значений в ячейках, проведен цикл
        анализа поля, нахождения комбинации,
        начисления бонуса, изменения счета, генерация новых ячеек, анализ
        нового поля. Новых сложившихся
        комбинаций не найдено, возвращаем управление игроку.
        """
        ...

    def _print_result(self):
        """предусловия: поле изменилось
        послусловия: выведено новое состояние игрового поля
        """
        ...


class IScore:
    START_POINT = 0

    def __init__(self, gamer: "IGamer"):
        self._score = self.START_POINT
        self._gamer = gamer

    def add_points(self, points: int) -> None:
        self._score += points

    def get_score(self) -> int:
        return self._score


class IBonus:
    INIT_POINTS: int = 0
    STANDARD_POINTS: int = 0

    def __init__(self):
        self._score: "IScore"
        self._points = self.INIT_POINTS

    def _calculate_points(self, cell_num: int) -> int:
        ...

    def bonus_behavior(self, cells_num: int) -> None:
        """предусловия: сработала комбинация, которая привязана к данному
        бонусу
        постусловия: бонус поменял поле в соответствии со своим поведением"""
        points = self._calculate_points(cells_num)
        self.update_points(points)

    def get_points(self) -> int:
        return self._points

    def update_points(self, value: int) -> None:
        self._points = value
        self._score.add_points(self._points)


class ICombination:
    DEFAULT_BONUS: Optional["IBonus"] = None
    CHECK_STATUS_NULL = 0
    CHECK_STATUS_OK = 1
    CHECK_STATUS_ERR = 2

    def __init__(self):
        self._bonus = self.DEFAULT_BONUS
        self._combi_template = self._default_template
        self._check_status = self.CHECK_STATUS_NULL
        self._combi_cells = []

    def _default_template(self):
        """функция, описывающая порядок проверки смежных ячеек
        должна быть определена в наследниках
        """
        ...

    def check_combination(self, start_cell: "ICell") -> None:
        """предусловие: передана правильная стартовая ячейка
        постусловие: статус 1 если от стартовой ячейки можно построить
        комбинацию, иначе - 2
        """
        ...

    def is_combination(self) -> bool:
        return self._check_status == self.CHECK_STATUS_OK

    def get_combi_cells(self) -> list["ICell"]:
        return self._combi_cells

    def get_combi_bonus(self) -> "IBonus":
        return self._bonus

    def reset_combination(self) -> None:
        self._check_status = self.CHECK_STATUS_NULL
        self._combi_cells.clear()


class HorizontalLineCombination(ICombination): ...  # noqa


class VerticalLineCombination(ICombination): ...  # noqa


class CrossCombination(ICombination): ...  # noqa 


class IPlayGround:
    Dimension = namedtuple("Dimension", ["x", "y"])

    GET_CELL_NULL = 0
    GET_CELL_OK = 1
    GET_CELL_ERR = 2

    def __init__(self, dimension: tuple[int, int]) -> None:
        self.dimension = self.Dimension(*dimension)
        self.a1: ICell = None
        self._get_cell_status = self.GET_CELL_NULL
        self._combi_cells_to_remove: set[ICell] = set()

    # command
    def analyze_playground(self) -> None:
        """предусловия: заполненное поле
        постусловия: поле проанализировано и заполнен список найденных
        ячеек в комбинациях
        """
        ...

    def generate_playground(self) -> None:
        """предусловия: нет
        постусловия: должен сформироваться список клеток с заполненными
        значениями и соседями
        """
        ...

    def clean_playground(self) -> None:
        """предусловия: нет
        постусловия: поле очищено от ячеек в комбинациях"""

    def regenerate_playground(self) -> None:
        """предусловия: нет
        постусловия: сгенерировано новое поле"""
        ...

    # request
    def get_cell_by_text_coord(self, text_coord: str) -> "ICell":
        """предусловие: координаты находятся в диапазоне допустимых значений
        в виде а1 (текст + цифра)
        постусловие: возращена ячейка по заданным координатам
        """

        ...

    def get_cell_by_int_coord(self, x: int, y: int) -> "ICell":
        """предусловия: координаты находятся в диапазоне допустимых значений
        заданных параметром dimension и переданы в виде индекса по горизонтали
        и по вертикали, начиная от 0
        постусловиеЖ возвращена ячейка по заданным координатам
        """

        ...

    def get_plauground_state(self) -> list[Any]:
        """предусловия: поле сгенерировано
        постусловия: сформирован список с копиями значений ячеек по состоянию
        на момент запроса
        """
        ...

    def is_get_cell_status_ok(self) -> bool:
        return self._get_cell_status == self.GET_CELL_OK

    def is_combinations_found(self) -> bool:
        return bool(self._combi_cells_to_remove)


class ICell:
    VALUE_CHOICES = []  # defined in subclasses

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

    def set_value(self, value: str | None = None) -> None:
        if value is None:
            value = random.choice(self.VALUE_CHOICES)
        self.value = value

    def clean_value(self) -> None:
        self.value = None


class IGamer:
    DEFAULT_NAME = ""

    def __init__(self, name: str | None = None) -> None:
        self.name = name or self.DEFAULT_NAME
        self.score = 0


class IStep:
    def __init__(self, cell_a: "ICell", cell_b: "ICell") -> None:
        self.cell_a = cell_a
        self.cell_b = cell_b

    def perform_step(self) -> None:
        """предусловия: введены разные соседние ячейки
        постусловия: значения в ячейках поменяны местами, запущен процесс
        анализа поля"""
        ...


class IStepStack:
    def __init__(self):
        self._stack = []

    def add_step(self, playground_state: list[Any], step: "IStep") -> None:
        self._stack.append((playground_state, step))

    def pop_step(self) -> "IStep":
        return self._stack.pop()
