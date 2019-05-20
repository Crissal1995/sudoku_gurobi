from gurobipy import *
from Model.sudoku_view_model import SudokuGrid

class GurobiController:
    # il costruttore crea modello e vincoli seguendo le regole del sudoku;
    # per poter differenziare lo schema, dobbiamo chiamare la funzione set_grid()
    # per poter assegnare un lowerbound di 1 alla cella (i,j) con valore k -> x_ijk
    def __init__(self, sudoku_grid: SudokuGrid):
        self.model: Model = Model('gus')
        self.vars = self.model.addVars(9,9,9, vtype=GRB.BINARY, name='x_ijk')
        ### constraints
        # Ogni elemento della matrice deve contenere un numero da 1 a 9
        self.model.addConstrs(
            (self.vars.sum(i,j,'*') == 1 for i in range(9) for j in range(9))
        )
        # In ogni colonna della tabella devono essere presenti tutti i numeri da 1 a 9
        self.model.addConstrs(
            (self.vars.sum('*',j,k) == 1 for j in range(9) for k in range(9))
        )
        # In ogni riga della tabella devono essere presenti tutti i numeri da 1 a 9
        self.model.addConstrs(
            (self.vars.sum(i,'*',k) == 1 for i in range(9) for k in range(9))
        )
        # In ogni riquadro della tabella devono essere presenti tutti i numeri da 1 a 9
        for subgrid in sudoku_grid.subgrids:
            self.model.addConstrs(
                (self.vars.sum(i,j,'*') == 1 for (i,j) in sudoku_grid.cells_in_subgrid[subgrid])
            )

    # funzione per resettare i vincoli
    def reset_grid(self):
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    self.vars[i,j,k].LB = 0

    # funzione per settare i vincoli, data una griglia (str) in ingresso
    def set_grid(self, grid: str):
        assert(len(grid) == 81)
        for i in range(9):
            for j in range(9):
                k = grid[i*9 + j]
                if k not in SudokuGrid.delimiters:
                    self.vars[i,j,int(k)-1].LB = 1

    # funzione per risolvere la griglia corrente
    def resolve_grid(self):
        self.model.optimize()
        dict_values = self.model.getAttr('X', self.vars)
        grid_sol = ''
        for x_ijk, value in dict_values.items():
            # i,j = x_ijk[:1]
            k = x_ijk[2]
            if value == 1: grid_sol += f'{k+1}'
        return grid_sol

    # funzione per generare una griglia
    def generate_grid(self, nnz: int = 17):
        count = 0
