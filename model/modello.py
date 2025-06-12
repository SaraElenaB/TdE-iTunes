import networkx as nx
from database.DAO import DAO


class Model:

    def __init__(self):

        self._grafo = nx.Graph()
        self._nodes = []
        self._idMapAlbum = {}

    def buildGraph(self, dMin):

        self._grafo.clear()
        self._nodes = DAO.getAllAlbum(dMin)
        self._grafo.add_nodes_from(self._nodes)
        for a in self._nodes:
            self._idMapAlbum[a.AlbumId]=a

        self._allEdges = DAO.getAllEdges(self._idMapAlbum)
        self._grafo.add_edges_from(self._allEdges)
        return self._grafo

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getAllNodes(self):
        return list(self._grafo.nodes()) #altrimenti nodoView

    def getInfoConnessa(self, a1):

        cc = nx.node_connected_component(self._grafo, a1)
        durataComplessiva = self._getDurataComplessiva(cc)
        return len(cc), durataComplessiva

    def _getDurataComplessiva(self, listaNodi):

        sumDurata=0
        for n in listaNodi:
            sumDurata += n.dTotMin
        return sumDurata



if __name__ == "__main__":
    m = Model()
    m.buildGraph(120)
    n,e = m.getGraphDetails()
    print( f"Num nodi: {n} \nNum edge: {e}")


