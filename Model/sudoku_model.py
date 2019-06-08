# applichiamo il pattern Singleton alla classe
# per gestire un'unica griglia sudoku

class SudokuGrid:
    default_grid = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'
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
    def full_cells_count(self):
        return len([c for c in self.grid if c in SudokuGrid.digits])

    def set_grid(self, grid: str):
        self.grid = grid

    def is_valid_grid(self):
        return len([char for char in self.grid if char in SudokuGrid.valid_chars]) == 81

