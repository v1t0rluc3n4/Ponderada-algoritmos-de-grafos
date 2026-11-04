"""
Etapa 3: Implementação em Código do TAD Grafo, Dijkstra e Prim
"""

class GrafoSmartGrid:
    def __init__(self, num_vertices=8):
        self.num_vertices = num_vertices
        self.nos = [f"S{i}" for i in range(num_vertices)]
        self.nos_map = {f"S{i}": i for i in range(num_vertices)}
        self.matriz = [[None for _ in range(num_vertices)] for _ in range(num_vertices)]
        for i in range(num_vertices):
            self.matriz[i][i] = 0

    def adicionar_ramal(self, u_nome, v_nome, peso):
        if peso < 0:
            raise ValueError("O algoritmo de Dijkstra exige pesos não negativos.")
        u = self.nos_map[u_nome]
        v = self.nos_map[v_nome]
        self.matriz[u][v] = peso
        self.matriz[v][u] = peso

    def remover_ramal(self, u_nome, v_nome):
        u = self.nos_map[u_nome]
        v = self.nos_map[v_nome]
        self.matriz[u][v] = None
        self.matriz[v][u] = None

    def exibir_matriz(self):
        header = "      " + " ".join([f"{n:>6}" for n in self.nos])
        print(header)
        print("    " + "-" * (len(header) - 4))
        for i in range(self.num_vertices):
            linha = f"{self.nos[i]:>4} |"
            for j in range(self.num_vertices):
                val = self.matriz[i][j]
                val_str = "  NULO" if val is None else f"{val:>6}"
                linha += val_str
            print(linha)

    def dijkstra(self, origem_nome, destino_nome):
        s = self.nos_map[origem_nome]
        t = self.nos_map[destino_nome]
        
        dist = [float('inf')] * self.num_vertices
        ant = [None] * self.num_vertices
        fechado = [False] * self.num_vertices
        
        dist[s] = 0
        ordem_fechamento = []

        for _ in range(self.num_vertices):
            u = -1
            min_dist = float('inf')
            for i in range(self.num_vertices):
                if not fechado[i] and dist[i] < min_dist:
                    min_dist = dist[i]
                    u = i

            if u == -1:
                break

            fechado[u] = True
            ordem_fechamento.append(self.nos[u])

            for v in range(self.num_vertices):
                peso = self.matriz[u][v]
                if not fechado[v] and peso is not None and peso > 0:
                    if dist[u] + peso < dist[v]:
                        dist[v] = dist[u] + peso
                        ant[v] = u

            if u == t:
                break

        caminho = []
        curr = t
        while curr is not None:
            caminho.append(self.nos[curr])
            curr = ant[curr]
        caminho.reverse()

        return dist[t], caminho, ordem_fechamento

    def prim_mst(self):
        chave = [float('inf')] * self.num_vertices
        parent = [None] * self.num_vertices
        in_mst = [False] * self.num_vertices
        
        chave[0] = 0
        arestas_mst = []
        custo_total = 0

        for _ in range(self.num_vertices):
            u = -1
            min_key = float('inf')
            for i in range(self.num_vertices):
                if not in_mst[i] and chave[i] < min_key:
                    min_key = chave[i]
                    u = i

            in_mst[u] = True
            if parent[u] is not None:
                peso = self.matriz[u][parent[u]]
                arestas_mst.append((self.nos[parent[u]], self.nos[u], peso))
                custo_total += peso

            for v in range(self.num_vertices):
                peso = self.matriz[u][v]
                if peso is not None and peso > 0 and not in_mst[v]:
                    if peso < chave[v]:
                        chave[v] = peso
                        parent[v] = u

        return custo_total, arestas_mst

if __name__ == "__main__":
    grafo = GrafoSmartGrid()
    ramais = [
        ("S0", "S1", 13), ("S0", "S2", 15), ("S1", "S2", 10), ("S1", "S3", 12),
        ("S2", "S4", 15), ("S2", "S5", 14), ("S3", "S4", 7),  ("S3", "S6", 14),
        ("S4", "S5", 8),  ("S4", "S7", 17), ("S5", "S7", 24), ("S6", "S7", 11),
        ("S1", "S4", 20)
    ]
    for u, v, w in ramais:
        grafo.adicionar_ramal(u, v, w)

    print("=== EVIDENCIA DE TERMINAL: MATRIZ DE ADJACENCIA 8x8 ===")
    grafo.exibir_matriz()

    custo_opt, rota_opt, fechamento = grafo.dijkstra("S0", "S7")
    print(f"\nCusto Minimo Acumulado: {custo_opt} km")
    print(f"Rota Otima: {' -> '.join(rota_opt)}")
    print(f"Ordem de Fechamento: {' -> '.join(fechamento)}")