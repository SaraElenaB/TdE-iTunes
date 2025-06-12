import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._albumSelected = None

    def _fillDD(self, listaNodi):

        listaNodi.sort( key= lambda x: x.Title)
        for n in listaNodi:
            self._view._ddAlbum.options.append( ft.dropdown.Option( key=n.Title,
                                                                    data=n,
                                                                    on_click= self._readAlbum ))

    def _readAlbum(self, e):

        if e.control.data is None:
            print("error in reading dd")
            self._albumSelected = None

        self._albumSelected = e.control.data

    def handleCreaGrafo(self, e):

        dMin = self._view._txtInDurata.value
        if dMin == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, valore minimo di  durata non inserito", color="red"))
            self._view.update_page()
            return

        try:
            dMinInt = int(dMin)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, inserire un valore di durata intero", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(dMinInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        numNodi, numEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Num nodi: {numNodi}, num edges: {numEdges}"))

        self._fillDD(self._model.getAllNodes())

        self._view.update_page()


    def handleAnalisiComp(self, e):

        if self._albumSelected is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, album non selezionato", color="red"))
            self._view.update_page()
            return

        size, dTotCC = self._model.getInfoConnessa(self._albumSelected)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append( ft.Text(f"La componente connessa che contiene {self._albumSelected} ha dimensione {size} e una durata totale di {dTotCC} minuti"))
        self._view.update_page()


    def handleGetSetAlbum(self, e):

        sogliaTxt = self._view._txtInSoglia.value
        if sogliaTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, soglia massima di  durata non inserita", color="red"))
            self._view.update_page()
            return

        try:
            sogliaInt = int(sogliaTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, soglia massima non è un intero", color="red"))
            self._view.update_page()
            return

        if self._albumSelected is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Attenzione, album non selezionato", color="red"))
            self._view.update_page()
            return

        setOfNodes, sumDurate = self._model.getSetOfNodes( self._albumSelected, sogliaInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un set di album che soddisfa le specifiche: dimensione {len(setOfNodes)}, durata totale: {sumDurate}"))
        self._view.txt_result.controls.append(ft.Text(f"Di seguito gli album che fanno parte della soluzione trovata"))
        for n in setOfNodes:
            self._view.txt_result.controls.append(
                ft.Text(n))

        self._view.update_page()
