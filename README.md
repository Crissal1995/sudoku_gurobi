# sudoku_gurobi

## Prerequisiti
[Gurobi Optimizer](http://www.gurobi.com/index) e Python 3 64bit

### Guida installazione Gurobi
* Installare normalmente
* Non riavviare il PC al termine dell'installazione
* Eseguire `python setup.py install` nella folder di installazione di Gurobi (default C:\gurobi811)

## TODO
### Necessario
* Implementare correttamente la funzione generatrice delle griglie

### Facoltativo
* Aggiungere f obiettivo (somma di x_ijk a massimizzare, come upper bound implicito ha 81, num celle piene)
* Rimuovere inserimento utente? (nelle celle)
* Marcare celle generate da Gurobi (es con un font color rosso o bold) per distinguere dalle celle generate in fase di risoluzione
