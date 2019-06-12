from tkinter import *
from tkinter.ttk import *
import View.sudoku_frame as model
from tkinter import messagebox


class ViewManager:
    nnz_text_whenScale = 'Numero di celle piene desiderate: '
    nnz_text_whenProgress = 'Numero di celle piene: '
    nnz_cells_count = 81

    def __init__(self, controller):
        # ref a controller
        self.controller = controller

        # inizializzazione gui
        self.root = Tk()
        self.root.title('GUS - Gurobi Sudoku')
        # creiamo la griglia del sudoku
        self.sudoku_frame = model.SudokuFrame(self.root)

        # frame per contenere label e slider delle celle piene
        self.nnz_frame = Frame(self.root, padding='5 5 5 5')
        self.nnz_frame.pack()

        # label per indicare il num di caselle piene scelto
        self.nnz_label = Label(self.nnz_frame, text=self.nnz_text_whenScale + '17', justify=CENTER)
        self.nnz_label.grid(row=0, column=0)

        # variabile contenente il valore dello slider
        self.nnz_intvar = IntVar()
        self.nnz_intvar.set(17)
        # slider per decidere un numero in un range fissato
        self.nnz_scale = Scale(self.nnz_frame, from_=17, to=60, orient=HORIZONTAL,
                               variable=self.nnz_intvar, command=self.edit_label)
        self.nnz_scale.grid(row=1, column=0, sticky=EW)

        # frame per contenere i bottoni
        self.buttons_frame = Frame(self.root, padding='5 5 5 5')
        self.buttons_frame.pack()

        # bottone per generare un puzzle random
        self.gen_button = Button(self.buttons_frame, text='Genera puzzle',
                                 command=self.gen_button_click)
        self.gen_button.grid(row=0, column=0, sticky=EW)

        # bottone per risolvere il puzzle corrente
        self.risolve_button = Button(self.buttons_frame, text='Risolvi puzzle',
                                     command=self.risolve_button_click)
        self.risolve_button.grid(row=0, column=1, sticky=EW)

        # progressbar per il caricamento in fase di generazione
        self.progress_bar = Progressbar(self.nnz_frame, mode='determinate',
                                        orient=HORIZONTAL, length=200)

        # frame per contenere labels e entry per i time di attesa
        self.time_frame = Frame(self.root, padding='5 5 5 5')
        self.time_frame.pack(side=LEFT)

        # label per la sleep dopo la generazione della griglia completa
        self.time_after_generate_label = Label(self.time_frame,
                                               text="Sleep dopo la generazione della griglia [ms]")
        self.time_after_generate_label.grid(row=0, column=0, sticky=NW)

        # entry per la sleep
        self.time_after_generate_stringvar = StringVar()
        self.time_after_generate_entry = Entry(self.time_frame,
                                               textvariable=self.time_after_generate_stringvar)
        # campo di default per l'entry
        self.time_after_generate_entry.insert(END, "1000")
        self.time_after_generate_entry.grid(row=0, column=1, padx=10)

        # label per la sleep dopo ogni cancellazione di cella
        self.time_after_delete_label = Label(self.time_frame,
                                             text="Sleep per ogni cancellazione di cella [ms]")
        self.time_after_delete_label.grid(row=1, column=0, sticky=NW)
        # stringvar per mantenere il valore
        self.time_after_delete_stringvar = StringVar()
        # entry per modificare il time to sleep
        self.time_after_delete_entry = Entry(self.time_frame,
                                             textvariable=self.time_after_delete_stringvar)
        # valore di default
        self.time_after_delete_entry.insert(END, "500")
        self.time_after_delete_entry.grid(row=1, column=1, padx=10)

    def get_choice(self):
        return self.nnz_intvar.get()

    def start_app(self):
        self.root.mainloop()

    def load_grid(self, grid: str):
        self.sudoku_frame.load_grid(grid)

    # funzione chiamata ogni volta che lo scale si ferma
    def edit_label(self, _):
        self.nnz_label.configure(text=self.nnz_text_whenScale + f'{self.get_choice()}')

    @staticmethod
    def display_warning(message: str):
        return messagebox.showwarning('Attenzione', message)

    @staticmethod
    def display_error(message: str):
        return messagebox.showerror('Errore', message)

    def gen_button_click(self):
        # blocca gli input
        self.disable_inputs()
        # genera il sudoku
        self.controller.generate_sudoku()
        # sblocca gli input
        self.enable_inputs()
    
    def risolve_button_click(self):
        self.disable_inputs()
        self.controller.risolve_sudoku()
        self.enable_inputs()

    def disable_inputs(self):
        self.gen_button['state'] = DISABLED
        self.risolve_button['state'] = DISABLED
        self.time_after_delete_entry['state'] = DISABLED
        self.time_after_generate_entry['state'] = DISABLED
    
    def enable_inputs(self):
        self.gen_button['state'] = NORMAL
        self.risolve_button['state'] = NORMAL
        self.time_after_delete_entry['state'] = NORMAL
        self.time_after_generate_entry['state'] = NORMAL

    def display_progressbar(self, max_value: int):
        # rendi visibile la progress bar
        self.progress_bar.grid(row=1, column=0)
        # rimuovi dalla griglia lo scale nnz
        self.nnz_scale.grid_remove()
        # setta il max della progressbar
        self.progress_bar['maximum'] = max_value
        # setta il text della nnz label
        self.nnz_cells_count = 81
        self.nnz_label['text'] = self.nnz_text_whenProgress + str(self.nnz_cells_count)
        # update grafico
        self.update_graphics()

    def increment_progressbar(self):
        # incrementa il valore della progress bar
        self.progress_bar.step()
        # diminuisci il valore di quanti elem ho
        self.nnz_cells_count -= 1
        # riaggiorna la label
        self.nnz_label['text'] = self.nnz_text_whenProgress + str(self.nnz_cells_count)
        # aggiorna gli elementi grafici
        self.update_graphics()

    def remove_progressbar(self):
        # rimuovi dal frame la progress bar
        self.progress_bar.grid_remove()
        # rendi di nuovo visibile lo scale nnz
        self.nnz_scale.grid(row=1, column=0)
        # ripristina la nnz label originale
        self.nnz_label['text'] = self.nnz_text_whenScale + str(self.get_choice())
        # update grafico
        self.update_graphics()

    def update_graphics(self):
        self.root.update()

    def get_time_after_generate(self):
        default_value = 1000
        try:
            value = float(self.time_after_generate_stringvar.get())
            value = value if value >= 0 else default_value
        except ValueError:
            value = default_value
        return value / 1000  # ms -> s

    def get_time_after_delete(self):
        default_value = 500
        try:
            value = float(self.time_after_delete_stringvar.get())
            value = value if value >= 0 else default_value
        except ValueError:
            value = default_value
        return value / 1000  # ms -> s
