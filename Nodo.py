
class Nodo:

    # Shared variables 
    # hijos = []
    # padre = None
    # nombre = None

    def __init__(self, nombre) -> None:
        self.nombre = nombre
        self.hijos = []
        self.padre = None
        self.board = None
        self.value = None

    def get_padre(self):
        return self.padre.nombre

    def add_hijo(self, nodo):
        if isinstance(nodo, tuple):
            for i in nodo:
                self.hijos.append(i)
                i.padre = self
        if isinstance(nodo, Nodo):
            self.hijos.append(nodo)
            nodo.padre = self
        return nodo
    
    def get_hijos(self):
        return [hijo for hijo in self.hijos]
    
    def get_hijos_nombre(self):
        return [hijo.nombre for hijo in self.hijos]
    
    
def tree_search(nodo:Nodo):
    '''BFS - Breadth First Search'''
    queue_frontier = nodo.get_hijos()
    while True:
        print([n.nombre for n in queue_frontier])
        if len(queue_frontier) == 0:
            return None
        
        # FIFO - First In First Out
        leaf_node:Nodo = queue_frontier.pop(0)

        # Goal state 
        if leaf_node.nombre == 'E':
            return leaf_node
        queue_frontier += leaf_node.get_hijos()


if __name__ == '__main__':
    A = Nodo('A')
    B = Nodo('B')
    C = Nodo('C')
    D = Nodo('D')
    E = Nodo('E')
    F = Nodo('F')

    A.add_hijo((B,C))
    B.add_hijo((D,E))
    C.add_hijo(F)
    
    # print(A.get_hijos_nombre())
    # print(D.get_padre())

    print(tree_search(A))