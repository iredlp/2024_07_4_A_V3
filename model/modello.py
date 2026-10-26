from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMapR = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllShapes(self, year):
        return DAO.getAllShapes(year)

    def creaGrafo(self, year, shape):
        self._grafo.clear()
        self._idMapR.clear()

        avvistamenti = DAO.getAllNodes(year, shape)
        avvistamenti.sort(key=lambda a: a.datetime)
        for a in avvistamenti:
            self._idMapR[a.id] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        # Aggiungo gli archi
        for i in range(len(avvistamenti)):
            a1 = avvistamenti[i]
            for j in range(i + 1, len(avvistamenti)):
                a2 = avvistamenti[j]

                if a1.state is not None and a1.state != "" and a1.state == a2.state:
                   # if a1.state is not None and a1.state != "" and a1.state == a2.state:
                   if(a1.datetime<a2.datetime):
                        self._grafo.add_edge(a1, a2)
                      #  print("Arco:", a1.id, "->", a2.id)
                  # else:
                     #   self._grafo.add_edge(a2, a1)
                      #  print("Arco:", a2.id, "->", a1.id)
        print("4 - Archi aggiunti")


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getConnessaInfo(self):
      #  components = list(nx.connected_components(self._grafo))
      #PERCHè DEVE ESSERE DEBOLMENTE CONNESSA!!
        components = list(nx.weakly_connected_components(self._grafo))
        if len(components) == 0:
           return 0, set(), []

        # Tengo solo le componenti con più di un nodo
        #components = [c for c in components if len(c) > 1]
        largest = max(components, key=len)
      #  pesi = {}
       # for nodo in largest:
          #  minPeso = None
          #  for vicino in self._grafo.neighbors(nodo):
             #   peso = self._grafo[nodo][vicino]["weight"]
             #   if minPeso is None or peso < minPeso:
               # []    minPeso = peso

            #pesi[nodo] = minPeso
       # ordered_nodes_pesi = sorted(largest, key=lambda n: pesi[n], reverse=True)

        # Ordino per dimensione decrescente
        components = sorted(components, key=len, reverse=True)
        # details = [(n, pesi[n]) for n in ordered_nodes_pesi]

        return components , len(components), largest #, details


    def getCamminoMassimo(self):
        punteggio_massimo = 0
        cammino_massimo = []

        for nodo in self._grafo.nodes:
            mesi = {nodo.datetime.month: 1}

            punteggio, cammino = self.ricorsione( nodo, [nodo], mesi, 100  )

            if punteggio > punteggio_massimo:
                punteggio_massimo = punteggio
                cammino_massimo = cammino

        return punteggio_massimo, cammino_massimo

    def ricorsione(self, nodo, cammino, mesi, punteggio):
        punteggio_massimo = punteggio
        cammino_massimo = cammino.copy()

        for vicino in self._grafo.successors(nodo):
            # La durata deve essere strettamente crescente
            if vicino.duration <= nodo.duration:
                continue

            mese = vicino.datetime.month

            # Massimo 3 avvistamenti per mese
            if mesi.get(mese, 0) >= 3:
                continue

            # Punteggio del nuovo avvistamento
            nuovo_punteggio = punteggio + 100

            # Bonus se ha lo stesso mese del precedente
            if mese == nodo.datetime.month:
                nuovo_punteggio += 200

            # Aggiorno il conteggio dei mesi
            nuovi_mesi = mesi.copy()
            nuovi_mesi[mese] = nuovi_mesi.get(mese, 0) + 1

            nuovo_cammino = cammino + [vicino]

            # Continuo la ricorsione
            punteggio, cammino_trovato = self.ricorsione(
                vicino, nuovo_cammino, nuovi_mesi, nuovo_punteggio
            )

            if punteggio > punteggio_massimo:
                punteggio_massimo = punteggio
                cammino_massimo = cammino_trovato

        return punteggio_massimo, cammino_massimo
