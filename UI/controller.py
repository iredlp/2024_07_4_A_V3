import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDAnno(self):
        try:
            anno = self._model.getAllYears()
            for y in anno:
                self._view.ddyear.options.append(ft.dropdown.Option(y))
            # self._view._ddYear2.options.append(ft.dropdown.Option(y))
            # key=y.id,
            # text=y.name))
            self._view.update_page()

        except Exception as ex:
            self._view.txt_result1.controls.append(ft.Text(f"Errore nel recupero delle shape: {ex}", color="red"))
            self._view.update_page()

    def fillDDShape(self, e):
        anno = self._view.ddyear.value

        self._view.ddshape.options.clear()
        self._view.ddshape.value = None

        if not anno:
            self._view.create_alert("Selezionare l'anno prima di creare il grafo.")
            return

        try:
            shape = self._model.getAllShapes(anno)
            for y in shape:
                self._view.ddshape.options.append(ft.dropdown.Option(y))
            # key=y.id,
            # text=y.name))
            self._view.update_page()
        except Exception as ex:
            self._view.txt_result1.controls.append(ft.Text(f"Errore nel recupero delle shape: {ex}", color="red"))
            self._view.update_page()

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        shape = self._view.ddshape.value

        if not anno:
            self._view.create_alert("Selezionare Il valore MINIMO rima di creare il grafo.")
            return

        if not shape:
            self._view.create_alert("Selezionare la SHAPE prima di creare il grafo.")
            return
        # if Cmin > Cmax:
        # self._view.create_alert("Hai inserito un valore MINIMO più grande del MASSIMO! CORREGGI.", color="red")
        # return

        try:
            self._model.creaGrafo(anno, shape)
            # self._view._txt_result.controls.append(ft.Text(f"Data selezionata: {anno1}", color="green"))
            # self._view._txt_result.controls.append(ft.Text(f"Data selezionata: {anno2}\n", color="green"))
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()
            # Stampa immediata numero di vertici e archi (Punto 1.c)
            self._view.txt_result1.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
            # RIEMPIO IL DROPDOWN DEI FILM DEL GRAFO
            # self.fillDDNodoStart(categoria)
            # self.fillDDNodoEnd(categoria)

        except Exception as ex:
            self._view.txt_result1.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            # return

        components, numero, largest = self._model.getConnessaInfo()

        self._view.txt_result1.controls.append(
            ft.Text(f"Numero componenti debolmente connesse: {numero}") )

        self._view.txt_result1.controls.append(
            ft.Text(f"Dimensione componente maggiore: {len(largest)}"))

        self._view.txt_result1.controls.append(
            ft.Text("Nodi della componente maggiore:")  )

        for nodo in largest:
            self._view.txt_result1.controls.append(
                ft.Text( f"ID: {nodo.id} - Città: {nodo.city} - Data: {nodo.datetime}")
            )

       # self._view.update_page()
        self._view.update_page()

    def handle_path(self, e):
        n_nodes, _ = self._model.getGraphDetails()
        if n_nodes == 0:
            self._view.txt_result2.controls.append(
                ft.Text("Prima di cercare il percorso, devi creare il grafo!", color="red"))
            self._view.update_page()
            return
        try:
            punteggio, cammino = self._model.getCamminoMassimo()

            self._view.txt_result2.controls.clear()

            self._view.txt_result2.controls.append(
                ft.Text(f"Punteggio massimo: {punteggio}") )

            self._view.txt_result2.controls.append(
                ft.Text("Cammino:") )

            for a in cammino:
                self._view.txt_result2.controls.append(
                    ft.Text( f"ID: {a.id}, Durata: {a.duration}, "
                        f"Mese: {a.datetime.month}" )  )
            self._view.update_page()

        except Exception as ex:
            self._view.txt_result2.controls.append(
                ft.Text(f"Errore: {ex}", color="red")
            )
            self._view.update_page()
