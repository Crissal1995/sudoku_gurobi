import Controller.solver_controller as solver
import Model.sudoku_exceptions as error
from Model.sudoku_chars import SudokuChars


class SudokuGrid:
    default_grid = '0' * 81
    grid: str
    __instance = None
    __solver = None

    # singleton pattern
    def __new__(cls, grid: str = default_grid):
        if SudokuGrid.__instance is None:
            SudokuGrid.__instance = object.__new__(cls)
        SudokuGrid.__instance.grid = grid
        SudokuGrid.__solver = solver.SolverController().get_solver()
        return SudokuGrid.__instance

    @property
    def full_cells_count_current_grid(self):
        return SudokuGrid.full_cells_count(self.grid)

    def set_grid(self, grid: str):
        self.grid = grid

    @property
    def is_valid_current_grid(self):
        return self.is_valid_grid(self.grid)

    @staticmethod
    def is_valid_grid(grid: str):
        try:
            assert(len([char for char in grid if char in SudokuChars.valids]) == 81)
            SudokuGrid.__solver.resolve_grid(grid)
            return True
        except (error.SolverInfeasibleError, AssertionError):
            return False

    @staticmethod
    def full_cells_count(grid: str):
        return len([c for c in grid if c in SudokuChars.digits])

    @staticmethod
    def full_cells_indeces(grid: str):
        return [idx for idx, value in enumerate(grid) if value in SudokuChars.digits]
