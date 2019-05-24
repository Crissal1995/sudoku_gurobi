# applichiamo il pattern Singleton alla classe
# per gestire un'unica griglia sudoku
class SudokuGrid:
    default_grid = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
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

    # TODO INSERIRE VALIDAZIONE CON GUROBI
    def is_valid_grid(self):
        return len([char for char in self.grid if char in SudokuGrid.valid_chars]) == 81

    # TODO CREARE SEEDS SIA SEMIVUOTIVUOTI CHE PIENI
    # TODO QUELLI PIENI SERVONO PER GENERARE IL SUDOKU (PIENA -> SEMIVUOTA)
    # TODO QUELLI SEMIVUOTI SERVONO PER CARICARE RANDOMICAMENTE IL SUDOKU INIZIALE