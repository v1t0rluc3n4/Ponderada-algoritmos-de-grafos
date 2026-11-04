"""
Etapa 4: Questionário Analítico de Engenharia
- Questão 1: Rota e Custo Ótimo
- Questão 2: Contingência no Ramal (S2, S4)
- Questão 3: Prim (MST) vs Dijkstra
"""

from etapa3_codigo_tad import GrafoSmartGrid

def executar_questionario():
    # Instanciar Grafo
    grafo = GrafoSmartGrid()
    ramais = [
        ("S0", "S1", 13), ("S0", "S2", 15), ("S1", "S2", 10), ("S1", "S3", 12),
        ("S2", "S4", 15), ("S2", "S5", 14), ("S3", "S4", 7),  ("S3", "S6", 14),
        ("S4", "S5", 8),  ("S4", "S7", 17), ("S5", "S7", 24), ("S6", "S7", 11),
        ("S1", "S4", 20)
    ]
    for u, v, w in ramais:
        grafo.adicionar_ramal(u, v, w)

    print("==================================================")
    print("QUESTÃO 1 - ROTA E CUSTO ÓTIMO (OPERAÇÃO NORMAL)")
    print("==================================================")
    custo_norm, rota_norm, fechamento_norm = grafo.dijkstra("S0", "S7")
    print(f"• Custo mínimo total: {custo_norm} km")
    print(f"• Rota ótima: {' -> '.join(rota_norm)}")
    print(f"• Ordem cronológica de fechamento pelo Dijkstra:\n  {' -> '.join(fechamento_norm)}\n")

    print("==================================================")
    print("QUESTÃO 2 - CONTINGÊNCIA NO RAMAL e5 = (S2, S4)")
    print("==================================================")
    # Removendo o ramal (S2, S4)
    grafo.remover_ramal("S2", "S4")
    custo_cont, rota_cont, _ = grafo.dijkstra("S0", "S7")
    
    acrescimo_km = custo_cont - custo_norm
    acrescimo_pct = (acrescimo_km / custo_norm) * 100
    
    print(f"• Nova rota ótima sob contingência: {' -> '.join(rota_cont)}")
    print(f"• Novo custo mínimo total: {custo_cont} km")
    print(f"• Acréscimo absoluto de custo: {acrescimo_km} km")
    print(f"• Acréscimo percentual: {acrescimo_pct:.2f}%\n")

    print("==================================================")
    print("QUESTÃO 3 - PRIM (MST) vs DIJKSTRA")
    print("==================================================")
    # Reconstituindo o grafo original
    grafo.adicionar_ramal("S2", "S4", 15)
    custo_mst, arestas_mst = grafo.prim_mst()
    
    print(f"• Custo total da Árvore Geradora Mínima (Prim): {custo_mst} km")
    print("• Arestas selecionadas pela MST:")
    for u, v, w in arestas_mst:
        print(f"  - ({u}, {v}) = {w} km")
        
    print("\n• Fundamentação teórica de engenharia:")
    print("  1. Dijkstra busca a otimização PONTO-A-PONTO de rotas radiais a partir de uma fonte (S0),")
    print("     minimizando o tempo/perda de transmissão individual para cada destino.")
    print("  2. Prim (MST) busca a otimização GLOBAL DA INFRAESTRUTURA, conectando 100% dos nós")
    print("     com o menor custo total de cabeamento físico, sem garantia de rota mínima individual.")
    print("  3. A união dos caminhos de Dijkstra gera ciclos e duplicações de arestas, enquanto a MST")
    print("     é acíclica e minimiza o custo total de implantação do sistema elétrico.")

if __name__ == "__main__":
    executar_questionario()