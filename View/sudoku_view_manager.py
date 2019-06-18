from tkinter import *
from tkinter.ttk import *
import View.sudoku_frame as model
from tkinter import messagebox


# Gestisce e crea tutta la GUI
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
        self.sleep_frame = Frame(self.root, padding='5 5 5 5')
        self.sleep_frame.pack(side=LEFT)

        # label per richiedere se abilitare la sleep
        self.should_sleep_label = Label(self.sleep_frame,
                                        text='Abilita la sleep dopo generazione e cancellazione')
        self.should_sleep_label.grid(row=0, column=0, sticky=NW)

        # checkbutton per abilitare o no la sleep
        self.should_sleep_boolvar = BooleanVar()
        self.should_sleep_boolvar.set(True)
        self.should_sleep_checkbutton = Checkbutton(self.sleep_frame,
                                                    variable=self.should_sleep_boolvar,
                                                    command=self.checkbutton_clicked)
        self.should_sleep_checkbutton.grid(row=0, column=1, sticky=N)

        # label per la sleep dopo la generazione della griglia completa
        self.timetosleep_after_generate_label = Label(self.sleep_frame,
                                                      text="Sleep dopo la generazione della griglia [ms]")
        self.timetosleep_after_generate_label.grid(row=1, column=0, sticky=NW)

        # entry per la sleep
        self.timetosleep_after_generate_stringvar = StringVar()
        self.timetosleep_after_generate_entry = Entry(self.sleep_frame,
                                                      textvariable=self.timetosleep_after_generate_stringvar)
        # campo di default per l'entry
        self.timetosleep_after_generate_entry.insert(END, "1000")
        self.timetosleep_after_generate_entry.grid(row=1, column=1, padx=10)

        # label per la sleep dopo ogni cancellazione di cella
        self.timetosleep_after_delete_label = Label(self.sleep_frame,
                                                    text="Sleep per ogni cancellazione di cella [ms]")
        self.timetosleep_after_delete_label.grid(row=2, column=0, sticky=NW)
        # stringvar per mantenere il valore
        self.timetosleep_after_delete_stringvar = StringVar()
        # entry per modificare il time to sleep
        self.timetosleep_after_delete_entry = Entry(self.sleep_frame,
                                                    textvariable=self.timetosleep_after_delete_stringvar)
        # valore di default
        self.timetosleep_after_delete_entry.insert(END, "500")
        self.timetosleep_after_delete_entry.grid(row=2, column=1, padx=10)

    def get_choice(self):
        return self.nnz_intvar.get()

    def start_app(self):
        self.root.mainloop()

    def load_grid(self, grid: str):
        self.sudoku_frame.load_grid(grid)

    # funzione chiamata ogni volta che lo scale si ferma
    def edit_label(self, _):
        self.nnz_label.configure(text=self.nnz_text_whenScale + f'{self.get_choice()}')

    # funzione chiamata ad ogni cambio di checkbutton
    def checkbutton_clicked(self):
        if self.is_sleep_enabled():
            self.enable_timetosleep_entries()
        else:
            self.disable_timetosleep_entries()

    # funzione per mascherare come ottenere lo stato
    def is_sleep_enabled(self):
        return self.should_sleep_boolvar.get()

    @staticmethod
    def display_warning(message: str):
        return messagebox.showwarning('Attenzione', message)

    @staticmethod
    def display_error(message: str):
        return messagebox.showerror('Errore', message)
    
    @staticmethod
    def display_choice(message: str):
        return messagebox.askokcancel('Scelta', message)

    def gen_button_click(self):
        self.disable_buttons()
        self.controller.generate_sudoku()
        self.enable_buttons()
    
    def risolve_button_click(self):
        self.disable_buttons()
        self.controller.risolve_sudoku()
        self.enable_buttons()

    def disable_buttons(self):
        self.gen_button['state'] = DISABLED
        self.risolve_button['state'] = DISABLED
    
    def enable_buttons(self):
        self.gen_button['state'] = NORMAL
        self.risolve_button['state'] = NORMAL

    def disable_timetosleep_entries(self):
        self.timetosleep_after_delete_entry['state'] = DISABLED
        self.timetosleep_after_generate_entry['state'] = DISABLED

    def enable_timetosleep_entries(self):
        self.timetosleep_after_delete_entry['state'] = NORMAL
        self.timetosleep_after_generate_entry['state'] = NORMAL

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

    def set_progressbar_value(self, value):
        self.progress_bar['value'] = value
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

    def get_timetosleep_after_generate(self):
        default_value = 1000
        try:
            value = float(self.timetosleep_after_generate_stringvar.get())
            value = value if value >= 0 else default_value
        except ValueError:
            value = default_value
        return value / 1000  # ms -> s

    def get_timetosleep_after_delete(self):
        default_value = 500
        try:
            value = float(self.timetosleep_after_delete_stringvar.get())
            value = value if value >= 0 else default_value
        except ValueError:
            value = default_value
        return value / 1000  # ms -> s
