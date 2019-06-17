from mip.model import *
from Controller.sudoku_solver_interface import ISudokuSolver
from Model.sudoku_chars import SudokuChars
import Model.sudoku_exceptions as error


class MipController(ISudokuSolver):

    def __init__(self):
        self.model = None
        self.x = None

    def _make_model(self):
        self.model = Model('sudoku', solver_name='cbc')
        # creazione variabili binarie
        self.x = [[[self.model.add_var(name='x_{}{}{}'.format(i, j, k), var_type=BINARY)
                  for k in range(9)] for j in range(9)] for i in range(9)]
        # vincoli:
        # - ogni elem della matrice deve contenere un numero da 1 a 9
        for i in range(9):
            for j in range(9):
                self.model += xsum(self.x[i][j][k] for k in range(9)) == 1
        # - in ogni colonna devono esserci i numeri da 1 a 9
        for j in range(9):
            for k in range(9):
                self.model += xsum(self.x[i][j][k] for i in range(9)) == 1
        # - in ogni riga devono esserci i numeri da 1 a 9
        for i in range(9):
            for k in range(9):
                self.model += xsum(self.x[i][j][k] for j in range(9)) == 1
        # in ogni riquadro 3x3 devono esserci i numeri da 1 a 9
        for subrow in range(3):
            for subcol in range(3):
                for k in range(9):
                    self.model += xsum(self.x[i][j][k]
                                       for i in range(subrow*3, (subrow+1)*3)
                                       for j in range(subcol*3, (subcol+1)*3)) == 1
        # f obiettivo fittizia
        self.model.objective = maximize(xsum(self.model.vars))

    def _reset_vars(self):
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    self.x[i][j][k].lb = 0

    def _set_vars(self, grid: str):
        assert(len(grid) == 81)
        for i in range(9):
            for j in range(9):
                k = grid[i*9 + j]
                if k not in SudokuChars.delimiters:
                    self.x[i][j][int(k)-1].lb = 1

    def _resolve_grid(self):
        status = self.model.optimize()
        if status not in (OptimizationStatus.FEASIBLE, OptimizationStatus.OPTIMAL):
            raise error.SolverInfeasibleError
        grid_sol = ''
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    value = self.x[i][j][k].x
                    if value == 1:
                        grid_sol += str(k+1)
        return grid_sol

    def resolve_grid(self, grid: str):
        self._reset_vars()
        self._set_vars(grid)
        grid_sol = self._resolve_grid()
        return grid_sol
