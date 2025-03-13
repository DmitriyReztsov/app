from behavior_classes import IStep, IStepStack


class StepStack(IStepStack):
    pass


class Step(IStep):
    def perform_step(self) -> None:
        """предусловия: введены разные соседние ячейки
        постусловия: значения в ячейках поменяны местами, запущен процесс
        анализа поля
        """

        cell_a_value = self.cell_a.value
        cell_b_value = self.cell_b.value
        self.cell_a.set_value(cell_b_value)
        self.cell_b.set_value(cell_a_value)
