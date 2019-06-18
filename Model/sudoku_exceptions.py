#Eccezzioni che si verificano durante l'esecuzione
class SolverNotStandardError(Exception):
    pass


class SolverNotExistingError(Exception):
    pass

# Eccezione lanciata quando il solver non riesce a risolvere il sudoku
class SolverInfeasibleError(Exception):
    pass


class UserResettedSudokuException(Exception):
    pass
