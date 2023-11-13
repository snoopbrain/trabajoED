from collections import deque

class Node():
    def __init__(self):
        self.visited = False
        self.color = None

def is_bipartite(n, edge_list):
    # Inicializar nodos y aristas
    nodes = [Node() for _ in range(n + 1)]
    edges = [[] for _ in range(n + 1)]

    # Construir el grafo a partir de la lista de aristas
    for edge in edge_list:
        u, v = map(int, edge.split(','))
        edges[u].append(v)
        edges[v].append(u)

    def BFS(start):
        nodes[start].visited = True
        nodes[start].color = 0
        q = deque()
        q.append(start)

        while q:
            a = q.popleft()
            for b in edges[a]:
                if not nodes[b].visited:
                    nodes[b].visited = True
                    nodes[b].color = 1 - nodes[a].color
                    q.append(b)
                elif nodes[b].color == nodes[a].color:
                    return False

        return True

    # Verificar si el grafo es bipartito
    for i in range(1, n + 1):
        if not nodes[i].visited:
            if not BFS(i):
                return False

    return True

def main():
    C = int(input())

    for _ in range(C):
        N, M = map(int, input().split())

        edge_list = [input().strip() for _ in range(M)]

        # Determinar si el grafo es bipartito
        result = "bipartito" if is_bipartite(N, edge_list) else "no bipartito"
        print(result)

if __name__ == "__main__":
    main()
