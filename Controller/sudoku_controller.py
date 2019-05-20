import Model.sudoku_view_model as vmodel
import View.sudoku_view as view
import Controller.gurobi_controller as gurobi
from tkinter import messagebox
from tkinter import Tk

class Controller:
    def __init__(self):
        # creazione finestra GUI
        self.root = Tk()
        self.root.title('GUS - Gurobi Sudoku')
        # creazione frame griglia sudoku
        self.sudoku_grid = vmodel.SudokuGrid(self.root)
        # creazione controller Gurobi e relativo modello
        self.gurobi_control = gurobi.GurobiController(self.sudoku_grid)
        # settiamo una griglia di partenza
        self.load_current_grid()
        # settiamo il modello sulla griglia caricata
        self.gurobi_control.set_grid(self.grid)
        # creiamo il resto dei frame
        self.view_manager = view.ViewManager(self, self.root)
        # lanciamo l'applicazione
        self.root.mainloop()

    def load_current_grid(self):
        self.sudoku_grid.load_grid(self.sudoku_grid.grid)

    @property
    def grid(self):
        return self.sudoku_grid.grid

    def set_grid(self, grid2):
        self.sudoku_grid.grid = grid2

    ######## FUNZIONI CALLBACK (associate ai bottoni nella GUI)
    def generate_sudoku(self):
        nnz = self.view_manager.get_choice()
        assert(17 <= nnz <= 81)
        self.set_grid(self.grid[-7:] + self.grid[:-7]) # debug
        self.load_current_grid()

    def risolve_sudoku(self):
        grid_sol = self.gurobi_control.resolve_grid()
        self.set_grid(grid_sol)
        self.load_current_grid()

    def reset_sudoku(self):
        if messagebox.askokcancel('Reset', 'Vuoi resettare il puzzle?'):
            for c in self.sudoku_grid.cells:
                if not c.is_static: c.clear_value()

if __name__ == '__main__':
    controller = Controller()