# Otimização de Redes Elétricas Inteligentes (Smart Grid)

**Projeto:** Otimização de Rede Elétrica Smart Grid (Recomposição de Alta Tensão)  
**Módulo:** Teoria dos Grafos, Parametrização por RA, Algoritmos de Dijkstra e Prim   
---

##  Visão Geral do Projeto

Este DevLog documenta a modelagem matemática, o teste de mesa passo a passo, a implementação algorítmica e a análise de contingência de um sistema de roteamento de emergência para uma malha elétrica de alta tensão com 8 subestações ($S_0$ a $S_7$).

---

##  Registro de Desenvolvimento 1: Parametrização e Topologia (Etapa 1)

### 1.1 Extração dos Parâmetros do RA

* **RA:** `A2025.1A.0278`
* **Dígitos Extraídos:** $D_1=5, D_2=1, D_3=0, D_4=2, D_5=7, D_6=8$
* **Regra de Definição do Destino:** $D_6 = 8$ (par) $\rightarrow$ **Subestação de Destino =** $S_7$
* **Subestação de Origem:** $S_0$ (fixo)

### 1.2 Cálculo dos Pesos dos Ramais ($w(e)$ em km)

Cálculo de cada aresta utilizando operações de módulo com os dígitos do RA:

| Código da Aresta | Ramal | Fórmula do Peso | Cálculo Executado | Peso Final (km) |
| :---: | :---: | :---: | :---: | :---: |
| `e1` | $(S_0, S_1)$ | $10 + (D_6 \bmod 5)$ | $10 + (8 \bmod 5)$ | **13** |
| `e2` | $(S_0, S_2)$ | $15 + (D_5 \bmod 7)$ | $15 + (7 \bmod 7)$ | **15** |
| `e3` | $(S_1, S_2)$ | $8 + (D_4 \bmod 4)$ | $8 + (2 \bmod 4)$ | **10** |
| `e4` | $(S_1, S_3)$ | $12 + (D_3 \bmod 6)$ | $12 + (0 \bmod 6)$ | **12** |
| `e5` | $(S_2, S_4)$ | $14 + (D_2 \bmod 5)$ | $14 + (1 \bmod 5)$ | **15** |
| `e6` | $(S_2, S_5)$ | $9 + (D_1 \bmod 6)$ | $9 + (5 \bmod 6)$ | **14** |
| `e7` | $(S_3, S_4)$ | $7 + ((D_5 + D_6) \bmod 5)$ | $7 + (15 \bmod 5)$ | **7** |
| `e8` | $(S_3, S_6)$ | $11 + ((D_4 + D_5) \bmod 6)$ | $11 + (9 \bmod 6)$ | **14** |
| `e9` | $(S_4, S_5)$ | $6 + ((D_3 + D_4) \bmod 4)$ | $6 + (2 \bmod 4)$ | **8** |
| `e10` | $(S_4, S_7)$ | $16 + ((D_2 + D_3) \bmod 7)$ | $16 + (1 \bmod 7)$ | **17** |
| `e11` | $(S_5, S_7)$ | $18 + ((D_1 + D_2) \bmod 8)$ | $18 + (6 \bmod 8)$ | **24** |
| `e12` | $(S_6, S_7)$ | $9 + ((D_5 + D_1) \bmod 5)$ | $9 + (12 \bmod 5)$ | **11** |
| `e13` | $(S_1, S_4)$ | $20 + (D_6 \bmod 4)$ | $20 + (8 \bmod 4)$ | **20** |

### 1.3 Topologia do Grafo e Matriz de Adjacência $8 \times 8$

Representação da rede como um grafo não orientado, ponderado e simétrico. As ausências de conexões diretas são indicadas pela sentinela **NULO**.

```text
       (13)          (12)          (14)
  S0 -------- S1 ----------- S3 ----------- S6
   |        / |             |               |
   |      /   |             |               |
   |   (10)   | (20)        | (7)           | (11)
(15)|   /      |             |               |
   | /        v             v               v
  S2 -------- S4 ----------- S5 ----------- S7
       (15)        (8)   (17: S4-S7, 24: S5-S7)
```

$$M = \begin{bmatrix} 
 & S_0 & S_1 & S_2 & S_3 & S_4 & S_5 & S_6 & S_7 \\ 
S_0 & 0 & 13 & 15 & \text{NULO} & \text{NULO} & \text{NULO} & \text{NULO} & \text{NULO} \\ 
S_1 & 13 & 0 & 10 & 12 & 20 & \text{NULO} & \text{NULO} & \text{NULO} \\ 
S_2 & 15 & 10 & 0 & \text{NULO} & 15 & 14 & \text{NULO} & \text{NULO} \\ 
S_3 & \text{NULO} & 12 & \text{NULO} & 0 & 7 & \text{NULO} & 14 & \text{NULO} \\ 
S_4 & \text{NULO} & 20 & 15 & 7 & 0 & 8 & \text{NULO} & 17 \\ 
S_5 & \text{NULO} & \text{NULO} & 14 & \text{NULO} & 8 & 0 & \text{NULO} & 24 \\ 
S_6 & \text{NULO} & \text{NULO} & \text{NULO} & 14 & \text{NULO} & \text{NULO} & 0 & 11 \\ 
S_7 & \text{NULO} & \text{NULO} & \text{NULO} & \text{NULO} & 17 & 24 & 11 & 0 
\end{bmatrix}$$

---

## Registro de Desenvolvimento 2: Teste de Mesa Tabular (Etapa 2)

### 2.1 Regras de Execução

* **Origem:** $S_0$ | **Destino:** $S_7$
* **Desempate:** Vértice de menor índice numérico quando houver igualdade no valor de $L[v]$.

### 2.2 Tabela de Rastreamento Manual

| Iter. | Vértice Fechado $u$ | $L[u]$ | $L[S_0]$ | $L[S_1]$ | $L[S_2]$ | $L[S_3]$ | $L[S_4]$ | $L[S_5]$ | $L[S_6]$ | $L[S_7]$ | Antecessores Atualizados |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Inic.** | - | - | 0 | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | Inicialização na origem $S_0 = 0$ |
| **1** | $S_0$ | 0 | **[0]** | 13 | 15 | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $Ant[S_1]=S_0$, $Ant[S_2]=S_0$ |
| **2** | $S_1$ | 13 | **[0]** | **[13]** | 15 | 25 | 33 | $\infty$ | $\infty$ | $\infty$ | $Ant[S_3]=S_1$, $Ant[S_4]=S_1$ |
| **3** | $S_2$ | 15 | **[0]** | **[13]** | **[15]** | 25 | 30 | 29 | $\infty$ | $\infty$ | $Ant[S_4]=S_2$ *(30<33)*, $Ant[S_5]=S_2$ |
| **4** | $S_3$ | 25 | **[0]** | **[13]** | **[15]** | **[25]** | 30 | 29 | 39 | $\infty$ | $Ant[S_6]=S_3$ |
| **5** | $S_5$ | 29 | **[0]** | **[13]** | **[15]** | **[25]** | 30 | **[29]** | 39 | 53 | $Ant[S_7]=S_5$ |
| **6** | $S_4$ | 30 | **[0]** | **[13]** | **[15]** | **[25]** | **[30]** | **[29]** | 39 | 47 | $Ant[S_7]=S_4$ *(47 < 53)* |
| **7** | $S_6$ | 39 | **[0]** | **[13]** | **[15]** | **[25]** | **[30]** | **[29]** | **[39]** | 47 | Nenhum relaxamento |
| **8** | $S_7$ | 47 | **[0]** | **[13]** | **[15]** | **[25]** | **[30]** | **[29]** | **[39]** | **[47]** | **Destino Alcançado e Fechado** |

---

##  Registro de Desenvolvimento 3: Implementação e Validação (Etapa 3)

### 3.1 Estrutura do Repositório

```text
smart-grid-otimizacao/
├── etapa1_modelagem.py              # Inicialização de dados e exibição da matriz
├── etapa2_teste_de_mesa.py          # Verificação do teste de mesa tabular
├── etapa3_codigo_tad.py             # TAD Grafo + Algoritmos de Dijkstra e Prim
├── etapa4_questionario_engenharia.py# Simulação de contingência e análise de trade-off
└── README.md                        # DevLog completo do projeto 
```

### 3.2 Validação: Código vs Teste de Mesa Manual

* **Saída da Execução:** `Custo Mínimo: 47 km` | `Rota Ótima: S0 -> S2 -> S4 -> S7`
* **Sequência de Fechamento:** `S0 -> S1 -> S2 -> S3 -> S5 -> S4 -> S6 -> S7`
* **Conclusão:** Coincidência exata de 100% entre os cálculos do rastreamento manual e a execução do programa em Python.

---
##  Registro de Desenvolvimento 4: Análise de Engenharia e Contingência (Etapa 4)

### 4.1 Questão 1: Rota e Custo Ótimo (Operação Normal)

* **Distância Mínima Acumulada:** **47 km**
* **Sequência Exata da Rota Ótima:** $S_0 \rightarrow S_2 \rightarrow S_4 \rightarrow S_7$
* **Ordem Cronológica de Fechamento dos Vértices pelo Dijkstra:**
  $$S_0 \rightarrow S_1 \rightarrow S_2 \rightarrow S_3 \rightarrow S_5 \rightarrow S_4 \rightarrow S_6 \rightarrow S_7$$

### 4.2 Questão 2: Simulação de Contingência — Falha no Ramal $e_5 = (S_2, S_4)$

Simulação da queda de uma torre desativando o ramal $e_5$ ($w_5 = \infty$).

* **Nova Rota Ótima de Emergência:** $S_0 \rightarrow S_1 \rightarrow S_3 \rightarrow S_4 \rightarrow S_7$
* **Novo Custo Total Acumulado:** $13 + 12 + 7 + 17 =$ **49 km**
* **Acréscimo Absoluto:** $+2\text{ km}$
* **Impacto Percentual:**
  $$\Delta\% = \left(\frac{49 - 47}{47}\right) \times 100\% \approx 4,26\%$$

### 4.3 Questão 3: Árvore Geradora Mínima (Prim) vs Dijkstra

* **Custo Total da Infraestrutura Global (Prim MST):** **75 km**
  * **Arestas Selecionadas pela MST:**  
    $(S_0, S_1) = 13$, $(S_1, S_2) = 10$, $(S_1, S_3) = 12$, $(S_3, S_4) = 7$, $(S_4, S_5) = 8$, $(S_3, S_6) = 14$, $(S_6, S_7) = 11$.