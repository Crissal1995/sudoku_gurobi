# applichiamo il pattern Singleton alla classe
# per gestire un'unica griglia sudoku
import Controller.gurobi_controller as gurobi

class SudokuGrid:
    default_grid = '0'*81
    grid = ''
    digits = '123456789'
    delimiters = '0.'
    valid_chars = digits + delimiters

    __instance = None
    # singleton pattern
    def __new__(cls, grid: str = default_grid):
        if SudokuGrid.__instance is None:
            SudokuGrid.__instance = object.__new__(cls)
        SudokuGrid.__instance.grid = grid
        return SudokuGrid.__instance

    @property
    def full_cells_count_current_grid(self):
        return SudokuGrid.full_cells_count(self.grid)

    def set_grid(self, grid: str):
        self.grid = grid

    def is_valid_grid(self):
        return len([char for char in self.grid if char in SudokuGrid.valid_chars]) == 81 and \
               len(gurobi.GurobiController().resolve_grid(self.grid)) == 81

    @staticmethod
    def full_cells_count(grid: str):
        return len([c for c in grid if c in SudokuGrid.digits])

    @staticmethod
    def full_cells_list(grid: str):
        return [idx for idx,value in enumerate(grid) if value in SudokuGrid.digits]