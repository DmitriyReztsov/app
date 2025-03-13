from behavior_classes import IWindow
from combinations import CombinationTypes, combination_factory
from score import Score
from step import Step, StepStack
from playground import PlayGround


class Window(IWindow):
    # def __init__(self, gamer: IGamer) -> None:
    #     self._gamer = gamer
    #     self._combinations_list: list[ICombination]
    #     self._gamer_score: IScore
    #     self._playground: IPlayGround
    #     self._current_step: IStep

    #     self._create_combinations_list()
    #     self._create_score()
    #     self._create_step_stack()
    #     self._create_playground()
    #     self.run()

    def _create_score(self) -> None:
        self._gamer_score = Score(self._gamer)

    def _create_combinations_list(self) -> None:
        self._combinations_list = [
            combination_factory(combination_type)
            for combination_type in CombinationTypes.COMBINATIONS_TYPES
        ]
        self._link_score_to_conbination_bonus()

    def _link_score_to_conbination_bonus(self):
        for combi in self._combinations_list:
            combi_bonus = combi._bonus
            combi_bonus._score = self._gamer_score

    def _create_step_stack(self) -> None:
        self._step_stack = StepStack()

    def _create_playground(self) -> None:
        """предусловия: нет
        постусловия: создано игровое поле
        """
        self._playground = PlayGround((8, 8))
        self._playground.generate_playground()

    def run(self) -> None:
        """команда. Создает сущности игрового поля. Запускает цикл ввод -
        обработка - вывод результата.
        предусловия: нет
        постусловия: нет
        """

        while True:
            self._print_result()
            self._input_step()
            self._start_process()

    def _input_step(self):
        """предусловия: введены корректные координаты ячейки
        посусловия: создан объект Step"""
        input_string = input(
            ">>> Ход игрока. Для завершения игры введите 'Q'.\n"
            "Введите координаты ячеек в формате 'a1 b2': "
        )
        if input_string == "Q":
            exit()

        coord_a, coord_b = input_string.split(" ")
        cell_a = self._playground.get_cell_by_text_coord(coord_a)
        if not self._playground.is_get_cell_status_ok():
            print(">>> Ошибка ввода. Повторите попытку.")
            self._input_step()

        cell_b = self._playground.get_cell_by_text_coord(coord_b)
        if not self._playground.is_get_cell_status_ok():
            print(">>> Ошибка ввода. Повторите попытку.")
            self._input_step()

        self._current_step = Step(cell_a, cell_b)
        self._step_stack.add_step(
            self._playground.get_plauground_state(), self._current_step
        )

    def _start_process(self) -> None:
        """предусловия: сделан шаг
        постусловия: проведена замена значений в ячейках, проведен цикл
        анализа поля, нахождения комбинации, начисления бонуса, изменения
        счета, генерация новых ячеек, анализ нового поля. Новых сложившихся
        комбинаций не найдено, возвращаем управление игроку.
        """

        self._current_step.perform_step()
        self._playground.analyze_playground(self._combinations_list)
        while self._playground.is_combinations_found():
            self._playground.clean_playground()
            self._playground.regenerate_playground()
            self._playground.analyze_playground(self._combinations_list)

    def _print_result(self):
        """предусловия: поле изменилось
        послусловия: выведено новое состояние игрового поля
        """

        print(">>> -----------------")
        print(">>> Score: ", self._gamer_score.get_score())

        print(">>>- -----------------")
        for y in range(self._playground.dimension.y, 0, -1):
            print(f">>> {y} |", end="")
            line_text = ""
            for x in range(self._playground.dimension.x):
                line_text += (
                    f"{self._playground.get_cell_by_int_coord(x, y - 1).value}"
                    "|"
                )
            print(line_text)
            print(">>> - -----------------")
        print(">>>   -a-b-c-d-e-f-g-h-")
