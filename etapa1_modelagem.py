"""
Etapa 1: Modelagem Formal e Matriz de Pesos 8x8
RA: A2025.1A.0278
Dígitos extraídos: D1=5, D2=1, D3=0, D4=2, D5=7, D6=8
Destino: S7 (D6 é par)
"""

# Dígitos do RA
D1, D2, D3, D4, D5, D6 = 5, 1, 0, 2, 7, 8

# Cálculo dos Pesos dos 13 Ramais (em km)
PESOS = {
    "e1":  ("S0", "S1", 10 + (D6 % 5)),                # 10 + 3 = 13
    "e2":  ("S0", "S2", 15 + (D5 % 7)),                # 15 + 0 = 15
    "e3":  ("S1", "S2", 8 + (D4 % 4)),                 # 8 + 2 = 10
    "e4":  ("S1", "S3", 12 + (D3 % 6)),                # 12 + 0 = 12
    "e5":  ("S2", "S4", 14 + (D2 % 5)),                # 14 + 1 = 15
    "e6":  ("S2", "S5", 9 + (D1 % 6)),                 # 9 + 5 = 14
    "e7":  ("S3", "S4", 7 + ((D5 + D6) % 5)),          # 7 + 0 = 7
    "e8":  ("S3", "S6", 11 + ((D4 + D5) % 6)),         # 11 + 3 = 14
    "e9":  ("S4", "S5", 6 + ((D3 + D4) % 4)),          # 6 + 2 = 8
    "e10": ("S4", "S7", 16 + ((D2 + D3) % 7)),         # 16 + 1 = 17
    "e11": ("S5", "S7", 18 + ((D1 + D2) % 8)),         # 18 + 6 = 24
    "e12": ("S6", "S7", 9 + ((D5 + D1) % 5)),          # 9 + 2 = 11
    "e13": ("S1", "S4", 20 + (D6 % 4))                 # 20 + 0 = 20
}

# Construção da Matriz de Adjacência 8x8
VERTICES = [f"S{i}" for i in range(8)]
MATRIZ_8X8 = [[None for _ in range(8)] for _ in range(8)]

for i in range(8):
    MATRIZ_8X8[i][i] = 0

for cod, (u, v, w) in PESOS.items():
    i_u, i_v = int(u[1]), int(v[1])
    MATRIZ_8X8[i_u][i_v] = w
    MATRIZ_8X8[i_v][i_u] = w

def exibir_etapa1():
    print("=== ETAPA 1: TABELA DE PESOS DO RA A2025.1A.0278 ===")
    for cod, (u, v, w) in PESOS.items():
        print(f"{cod:>3} | ({u}, {v}) : {w:>2} km")
    
    print("\n=== MATRIZ DE ADJACÊNCIA 8x8 (SIMÉTRICA COM NULO) ===")
    header = "      " + " ".join([f"{v:>6}" for v in VERTICES])
    print(header)
    print("    " + "-" * (len(header) - 4))
    for i in range(8):
        linha = f"{VERTICES[i]:>4} |"
        for j in range(8):
            val = MATRIZ_8X8[i][j]
            linha += "  NULO" if val is None else f"{val:>6}"
        print(linha)

if __name__ == "__main__":
    exibir_etapa1()