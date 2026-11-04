"""
Etapa 2: Teste de Mesa Tabular do Algoritmo de Dijkstra
Origem: S0 | Destino: S7
Regra de desempate: menor índice numérico.
"""

from etapa1_modelagem import MATRIZ_8X8, VERTICES

def simular_teste_de_mesa():
    dist = [float('inf')] * 8
    ant = [None] * 8
    fechado = [False] * 8
    
    dist[0] = 0  # S0
    
    print("=== ETAPA 2: TESTE DE MESA TABULAR DE DIJKSTRA ===")
    print(f"{'Iter':<5} | {'u':<4} | {'L[u]':<5} | " + " | ".join([f"L[{v}]" for v in VERTICES]) + " | Antecessores Atualizados")
    print("-" * 110)
    
    # Inicialização
    line_init = f"{'Inic':<5} | {'-':<4} | {'-':<5} | "
    line_init += " | ".join([f"{dist[i]:>5}" if dist[i] != float('inf') else "  inf" for i in range(8)])
    line_init += " | Inicializacao na origem S0"
    print(line_init)
    
    for it in range(1, 9):
        # Selecionar u
        u = -1
        min_d = float('inf')
        for i in range(8):
            if not fechado[i] and dist[i] < min_d:
                min_d = dist[i]
                u = i
                
        if u == -1:
            break
            
        fechado[u] = True
        u_nome = VERTICES[u]
        
        updates = []
        for v in range(8):
            peso = MATRIZ_8X8[u][v]
            if not fechado[v] and peso is not None and peso > 0:
                if dist[u] + peso < dist[v]:
                    dist[v] = dist[u] + peso
                    ant[v] = VERTICES[u]
                    updates.append(f"Ant[{VERTICES[v]}]={VERTICES[u]}")
                    
        line = f"{it:<5} | {u_nome:<4} | {dist[u]:<5} | "
        vals = []
        for i in range(8):
            if fechado[i]:
                vals.append(f"[{dist[i]:>3}]")
            elif dist[i] == float('inf'):
                vals.append("  inf")
            else:
                vals.append(f"{dist[i]:>5}")
        line += " | ".join(vals)
        line += " | " + (", ".join(updates) if updates else "Nenhum")
        print(line)
        
        if u_nome == "S7":
            break

if __name__ == "__main__":
    simular_teste_de_mesa()