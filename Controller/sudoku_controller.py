import View.sudoku_view as view
import Controller.gurobi_controller as gurobi
import Model.sudoku_model as model
from tkinter import messagebox

class Controller:
    def __init__(self):
        # instanziamo il singleton del model
        self.sudoku_grid = model.SudokuGrid()

        # creiamo la gui del programma
        self.view_manager = view.ViewManager(self)

        # creazione controller Gurobi e relativo modello
        self.gurobi_control = gurobi.GurobiController(self.sudoku_grid)

        # settiamo una griglia di partenza
        self.load_current_grid()

        # lanciamo l'applicazione
        self.view_manager.start_app()

    @property
    def grid(self):
        return self.sudoku_grid.grid

    def load_current_grid(self):
        self.view_manager.sudoku_frame.load_grid(self.grid)

    ######## FUNZIONI CALLBACK (associate ai bottoni nella GUI)
    def generate_sudoku(self):
        self.gurobi_control.reset_vars()
        nnz = self.view_manager.get_choice()
        assert(17 <= nnz <= 81)
        ### TODO GENERAZIONE
        self.sudoku_grid.set_grid(self.grid[-7:] + self.grid[:-7])
        ### END GENERAZIONE
        self.load_current_grid()

    def risolve_sudoku(self):
        if self.gurobi_control.objective == 81:
            return messagebox.showwarning('Errore','Il sudoku è già stato risolto!')
        self.gurobi_control.set_vars(self.grid)
        grid_sol = self.gurobi_control.resolve_grid()
        self.sudoku_grid.set_grid(grid_sol)
        self.load_current_grid()

    def reset_sudoku(self):
        if messagebox.askokcancel('Reset', 'Vuoi resettare il puzzle?'):
            for c in self.sudoku_grid.cells:
                if not c.is_static: c.clear_value()

if __name__ == '__main__':
    controller = Controller()