import copy

import networkx as nx
from database.DAO import DAO


class Model:

    def __init__(self):

        self._grafo = nx.Graph()
        self._nodes = []
        self._idMapAlbum = {}

        self._bestSet = {}
        self._maxLen = 0

    # --------------------------------------------------------------------------------------------------------------------------------
    def buildGraph(self, dMin):

        self._grafo.clear()
        self._nodes = DAO.getAllAlbum(dMin)
        self._grafo.add_nodes_from(self._nodes)
        for a in self._nodes:
            self._idMapAlbum[a.AlbumId]=a

        self._allEdges = DAO.getAllEdges(self._idMapAlbum)
        self._grafo.add_edges_from(self._allEdges)
        return self._grafo

    # --------------------------------------------------------------------------------------------------------------------------------
    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getAllNodes(self):
        return list(self._grafo.nodes()) #altrimenti nodoView

    # --------------------------------------------------------------------------------------------------------------------------------
    def getInfoConnessa(self, a1):

        cc = nx.node_connected_component(self._grafo, a1)
        durataComplessiva = self._getDurataComplessiva(cc)
        return len(cc), durataComplessiva

    def _getDurataComplessiva(self, listaNodi):

        sumDurata=0
        for n in listaNodi:
            sumDurata += n.dTotMin
        return sumDurata

    # --------------------------------------------------------------------------------------------------------------------------------
    #PUNTO 2:
    def getSetOfNodes(self, a1, dTot):

        self._bestSet = {}
        self._maxLen = 0

        # set parziale --> sicuro non aggiungo doppioni
        # remove --> togliere gli elementi che ho già inserito, non ha senso tenerla nella cc

        parziale = {a1}
        cc = nx.node_connected_component(self._grafo, a1)
        cc.remove(a1)

        for n in set(cc): #crei una copia
            parziale.add(n)
            cc.remove(n)
            self._ricorsione( parziale, cc, dTot) #a1 --> è gia in parziale
            cc.add(n)
            parziale.remove(n)

        return self._bestSet, self._getDurataComplessiva(self._bestSet)

    # --------------------------------------------------------------------------------------------------------------------------------
    def _ricorsione(self, parziale, rimanenti, dTot):

        # terminale: #ammissibile? --> viola i vincoli?
        if self._getDurataComplessiva(parziale) > dTot:
            return

        # se non ammissibile --> è migliore?
        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet = copy.deepcopy(parziale)

        # continuo senza return, aggiungo --> e continuo con ricorsione
        for n in rimanenti:
            parziale.add(n)
            rimanenti.remove(n)
            self._ricorsione(parziale, rimanenti, dTot)
            parziale.remove(n)
            rimanenti.add(n) #backtracking opposto --> serve per andare + veloce
    #--------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    m = Model()
    m.buildGraph(120)
    n,e = m.getGraphDetails()
    print( f"Num nodi: {n} \nNum edge: {e}")


