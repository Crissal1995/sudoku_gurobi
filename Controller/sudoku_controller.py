import Controller.gurobi_controller as gurobi
import Controller.solver_error as error 
import Model.sudoku_grid as model
import random
import time

class Controller:
    time_after_generate = 1
    time_after_delete = 0.5
    should_sleep_after_gen = True

    def __init__(self):
        # instanziamo il singleton del model
        self.sudoku_grid = model.SudokuGrid()
        # dobbiamo importare dentro l'init per evitare un import circolare
        import View.sudoku_view_manager as view
        # creiamo la gui del programma
        self.view_manager = view.ViewManager(self)
        # creazione controller Gurobi e relativo modello
        self.solver = gurobi.GurobiController()
        # settiamo una griglia di partenza
        self.load_current_grid()

    def start_app(self):
        self.view_manager.start_app()

    def load_current_grid(self, first_load=True):
        self.view_manager.sudoku_frame.load_grid(self.sudoku_grid.grid, first_load)

    # Funzioni callback associate ai bottoni nella GUI
    def generate_sudoku(self):
        # ottiene il valore dello slider
        nnz = self.view_manager.get_choice()
        assert(17 <= nnz <= 81)
        # ottiene uno schema completo
        complete_grid = self.generate_full_grid()
        # se abbiamo impostato lo sleep per visualizzare l'eliminazione
        if self.should_sleep_after_gen:
            # imposta lo schema completo
            self.sudoku_grid.set_grid(complete_grid)
            self.load_current_grid()
            self.view_manager.update_graphics()
            # e fai la sleep per un tempo fissato
            time.sleep(self.time_after_generate)
        # riduce il numero di elem fino ad avere nnz elementi
        # partendo dallo schema completo
        half_grid = self.generate_half_grid(complete_grid, nnz)
        # setta la griglia nel model
        self.sudoku_grid.set_grid(half_grid)
        # carica a schermo la nuova griglia
        self.load_current_grid()

    def risolve_sudoku(self):
        # controlla se il sudoku non è stato già risolto
        if self.sudoku_grid.full_cells_count_current_grid == 81:
            return self.view_manager.display_warning('Il sudoku è stato già risolto!')
        # prova a risolvere il sudoku corrente
        try: grid_sol = self.solver.resolve_grid(self.sudoku_grid.grid)
        # se non è possibile c'è un errore
        except error.SolverError:
            return self.view_manager.display_error('Il sudoku non ha soluzione!')
        # altrimenti prendi la soluzione del solver
        # settala come griglia del model
        self.sudoku_grid.set_grid(grid_sol)
        # e ricarica la griglia
        self.load_current_grid(first_load=False)

    def generate_full_grid(self):
        # creiamo una lista di 9 numeri
        digits_list = list(range(1,10))
        # randomizziamo ogni volta il seme
        random.seed()
        # ordiniamo in un ordine sempre differente
        random.shuffle(digits_list)
        seed = '0' * 81
        # fissiamo i quattro angoli della matrice
        for row in [0, 8]:
            for col in [0, 8]:
                pos = row*9 + col
                element = random.choice(digits_list)
                digits_list.remove(element)
                seed = seed[:pos] + str(element) + seed[pos+1:]
        # fissiamo i rimanenti numeri della lista nel resto della matrice
        for element in digits_list:
            row = random.randint(1,7)
            col = random.randint(1,7)
            pos = row*9 + col
            seed = seed[:pos] + str(element) + seed[pos+1:]
        # ritorniamo la stringa soluzione di gurobi
        # della griglia ottenuta con questi 9 numeri
        # disposti in maniera casuale
        return self.solver.resolve_grid(seed)

    def generate_half_grid(self, complete_grid, nnz):
        # copia la griglia e lavora su di essa
        half_grid = complete_grid
        # ottieni gli indici delle celle piene
        idxs_full_cells = self.sudoku_grid.full_cells_list(half_grid)
        # mischia questi indici
        random.shuffle(idxs_full_cells)
        # totale delle celle da cancellare
        cells_to_delete = 81 - nnz
        # mostra la progressbar inizialmente vuota
        self.view_manager.display_progressbar(max_value=cells_to_delete)
        # itera fin quando non raggiungi il nnz desiderato
        while cells_to_delete > 0:
            pos = random.choice(idxs_full_cells)
            # rimuovo la posizione sia se metto '0' (vuota)
            # sia se non posso rimuoverla a causa di GurobiError
            idxs_full_cells.remove(pos)
            # salvo l'elem corrente in caso di eccezione
            old_elem = half_grid[pos]
            # rimuovo l'elem dalla griglia
            half_grid = half_grid[:pos] + '0' + half_grid[pos+1:]
            # controllo se è possibile risolvere la griglia
            try:
                self.solver.resolve_grid(half_grid)
                # se sono qui, posso aggiornare contatore e progressbar
                cells_to_delete -= 1
                self.view_manager.increment_progressbar()
                # se vogliamo fare la sleep
                if self.should_sleep_after_gen:
                    # facciamo update della grid per ogni elem cancellato
                    self.sudoku_grid.set_grid(half_grid)
                    self.load_current_grid()
                    self.view_manager.update_graphics()
                    # e una sleep per farlo visualizzare
                    time.sleep(self.time_after_delete)
            # se non è possibile, ripristino l'elemento salvato
            except error.SolverError:
                half_grid = half_grid[:pos] + old_elem + half_grid[pos+1:]
        self.view_manager.remove_progressbar()
        return half_grid