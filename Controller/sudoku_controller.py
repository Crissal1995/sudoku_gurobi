import Controller.gurobi_controller as gurobi
import Model.sudoku_grid as model
import random

class Controller:
    def __init__(self):
        # instanziamo il singleton del model
        self.sudoku_grid = model.SudokuGrid()
        # dobbiamo importare dentro l'init per evitare un import circolare
        import View.sudoku_view_manager as view
        # creiamo la gui del programma
        self.view_manager = view.ViewManager(self)
        # creazione controller Gurobi e relativo modello
        self.gurobi_control = gurobi.GurobiController()
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
            return self.view_manager.display_error('Il sudoku è stato già risolto!')
        # prova a risolvere il sudoku corrente
        try: grid_sol = self.gurobi_control.resolve_grid(self.sudoku_grid.grid)
        # se non è possibile c'è un errore
        except gurobi.GurobiError:
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
                seed = seed[:pos] + str(element) + seed[pos+1:]
                digits_list.remove(element)
        # fissiamo i rimanenti numeri della lista
        # nel resto della matrice
        for element in digits_list:
            row = random.randint(1,7)
            col = random.randint(1,7)
            pos = row*9 + col
            seed = seed[:pos] + str(element) + seed[pos+1:]
        # ritorniamo la stringa soluzione di gurobi
        # della griglia ottenuta con questi 9 numeri
        # disposti in maniera casuale
        return self.gurobi_control.resolve_grid(seed)

    def generate_half_grid(self, complete_grid, nnz):
        # copia la griglia e lavora su di essa
        half_grid = complete_grid
        # ottieni gli indici delle celle piene
        idxs_full_cells = self.sudoku_grid.full_cells_list(half_grid)
        # mischia questi indici
        random.shuffle(idxs_full_cells)
        # itera fin quando non raggiungi il nnz desiderato
        while self.sudoku_grid.full_cells_count(half_grid) > nnz:
            pos = random.choice(idxs_full_cells)
            # rimuovo la posizione sia se metto '0' (vuota)
            # sia se non posso rimuoverla a causa di GurobiError
            idxs_full_cells.remove(pos)
            # salvo l'elem corrente in caso di eccezione
            old_elem = half_grid[pos]
            # rimuovo l'elem dalla griglia
            half_grid = half_grid[:pos] + '0' + half_grid[pos+1:]
            # controllo se è possibile risolvere la griglia
            try: self.gurobi_control.resolve_grid(half_grid)
            # se non è possibile, ripristino l'elemento salvato
            except gurobi.GurobiError:
                half_grid = half_grid[:pos] + old_elem + half_grid[pos+1:]
        return half_grid