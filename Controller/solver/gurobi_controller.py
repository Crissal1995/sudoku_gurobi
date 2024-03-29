from gurobipy import *
import Model.sudoku_exceptions as error
from Model.sudoku_chars import SudokuChars
from Controller.sudoku_solver_interface import ISudokuSolver


class GurobiController(ISudokuSolver):
    # il costruttore crea modello e vincoli seguendo le regole del sudoku;
    # per poter differenziare lo schema, dobbiamo chiamare la funzione set_grid()
    # per poter assegnare un lowerbound di 1 alla cella (i,j) con valore k -> x_ijk
    def __init__(self):
        self.model = None
        self.vars = None

    def _make_model(self):
        self.model = Model('sudoku')
        self.vars = self.model.addVars(9, 9, 9, vtype=GRB.BINARY, name='x_ijk')
        # Vincoli:
        #
        # - Ogni elemento della matrice deve contenere un numero da 1 a 9
        self.model.addConstrs(
            (self.vars.sum(i, j, '*') == 1 for i in range(9) for j in range(9))
        )
        # - In ogni colonna della tabella devono essere presenti tutti i numeri da 1 a 9
        self.model.addConstrs(
            (self.vars.sum('*', j, k) == 1 for j in range(9) for k in range(9))
        )
        # - In ogni riga della tabella devono essere presenti tutti i numeri da 1 a 9
        self.model.addConstrs(
            (self.vars.sum(i, '*', k) == 1 for i in range(9) for k in range(9))
        )
        # - In ogni riquadro della tabella devono essere presenti tutti i numeri da 1 a 9
        self.model.addConstrs(
            (quicksum(
                self.vars[i, j, k]
                for i in range(subrow * 3, (subrow + 1) * 3)
                for j in range(subcol * 3, (subcol + 1) * 3)) == 1
             for k in range(9)
             for subrow in range(3)
             for subcol in range(3)
             )
        )
        # Funzione obiettivo, massimizzo la somma delle variabili x_ijk
        # La z è il numero di celle, come UB implicito c'è 81
        self.model.setObjective(
            quicksum(self.vars.values()), sense=GRB.MAXIMIZE
        )

    # funzione per resettare i vincoli
    def _reset_vars(self):
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    self.vars[i,j,k].LB = 0

    # funzione per settare i valori delle variabili del problema, data una griglia (str) in ingresso
    def _set_vars(self, grid: str):
        assert(len(grid) == 81)
        for i in range(9):
            for j in range(9):
                k = grid[i*9 + j]
                if k not in SudokuChars.delimiters:
                    self.vars[i, j, int(k)-1].LB = 1  # salvo k come k-1

    @property
    def objective(self):
        return int(self.model.getObjective().getValue())

    # funzione per risolvere la griglia corrente
    def _resolve_grid(self):
        # Funzione che invoca gurobi per risolvere il problema
        self.model.optimize()
        # Prendo la soluzione fornita da gurobi
        vars_dict = self.model.getAttr('X', self.vars)
        # La trasformo in una griglia valida
        grid_sol = ''
        for x_ijk, value in vars_dict.items():
            # i,j = x_ijk[:1]
            k = x_ijk[2]
            if value == 1:
                grid_sol += str(k+1)  # salvo k come k+1
        return grid_sol

    # funzione per risolvere una griglia passata in input
    def resolve_grid(self, grid: str):
        self._reset_vars()
        self._set_vars(grid)
        try: 
            sol = self._resolve_grid()
        except GurobiError:
            raise error.SolverInfeasibleError()
        return sol
