class SudokuGrid:
    default_grid = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
    digits = '123456789'
    delimiters = '0.'
    valid_chars = digits + delimiters
    instance = None
    def __init__(self, grid: str = default_grid):
        if SudokuGrid.instance is None:
            SudokuGrid.instance = self
            self.grid = grid
            try: assert(self.is_valid_grid())
            except AssertionError: self.grid = SudokuGrid.default_grid

    def set_grid(self, grid: str):
        self.grid = grid

    def is_valid_grid(self):
        return len([char for char in self.grid if char in SudokuGrid.valid_chars]) == 81

    @staticmethod
    def get_instance():
        if SudokuGrid.instance is None:
            return SudokuGrid()
        return SudokuGrid.instance