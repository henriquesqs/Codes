# -*- coding: utf-8 -*-
"""Buscas-IA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dEaT02Rk_melMfW9RAT3VtOKKLK2ZaUI

### Trabalho de IA: Buscas
#### Prof.º Alneu de Andrade Lopes
##### Por:
- Caio A. D. Basso, NUSP 10801173
- Gabriel G. Lorencetti, NUSP 10691891
- Henrique de S. Q. dos Santos, NUSP 10819029
- Witor M. A. de Oliveira, NUSP 10692190
"""

# Importando bibliotecas
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import queue as Q
from heapq import *
import math
import time

node_id = 0 # variável global para controlar o ID dos nós no grafo

class Aux:
    def __init__(self, id, weight):
        self.weight = weight
        self.id = id

    def __gt__(self, other):
        if self.weight > other.weight:
            return True
        else:
            return False

# Estrutura que representa um nó de um vértice
class Node:
        
    def __init__(self, x, y, boolFinal): # construtor do nó
        
        global node_id

        self.id = node_id # ID do nó
        node_id += 1

        self.posX = x # posição X do vértice no labirinto
        self.posY = y # posição y do vértice no labirinto

        self.boolFinal = boolFinal # variável que controla se o nó é o final

        self.adjacentNodes = [] # lista de adjacência dos nós

    def isNodeOnList(self, adj): # verifica se o nó 'adj' é adjacente ao nó que chama o método
      if (len(self.adjacentNodes) != 0):
        for node in self.adjacentNodes:
          if node.posX == adj.posX and node.posY == adj.posY:
            return True
      return False

    def addAdjNode(self, adj):  # adiciona um nó na lista de adjacentes ao nó que chama o método
      if not self.isNodeOnList(adj): self.adjacentNodes.append(adj)

# Estrutura que representa um grafo
class Graph:

    def __init__(self, n): # construtor do grafo
        self.nodeList = []

    def addNodeToGraph(self, node): # adds node to graph's list of nodes
      self.nodeList.append(node)

    def printGraph(self): # imprime na tela uma representação do grafo
      for u in self.nodeList:
        print("(", u.posX, ",", u.posY, ")", " F " if u.boolFinal else "", end=" ->", sep="")

        for v in u.adjacentNodes:
          print(" (", v.posX, ",", v.posY, ")", end="," if v != u.adjacentNodes[-1] else "", sep="")

        print("\n\n")

    def returnNode(self, x, y): # procura por um nó dado a sua posição (x,y)

      if (len(self.nodeList) != 0):
        for node in self.nodeList:
          if node.posX == x and node.posY == y:
            return node
      return None

    def findFinalNode(self): # procura e retorna o nó final. se não existir, retorna None
      for u in self.nodeList:
        if u.boolFinal == True:
          return u
      return None

"""#### Algoritmos
Nessa seção, é possível visualizar o código-fonte de todos os algoritmos de busca implementados. São eles:

- Depth-First Search (DFS);
- Breadth-First Search (BFS);
- Hill Climbing;
- Best-First Search;
- A* (A Star).
"""

def depth_first_search(g, initial, final):
    
    visited = []
    dfs_extensoes = 0 # variável para controlar as extensões no DFS

    stack = Q.deque()
    stack.append(initial)

    while stack:

        dfs_extensoes += 1
        current = stack.pop()

        if current.id == final.id:
          return visited, dfs_extensoes

        elif current not in visited:
          visited.append(current)
          for i in current.adjacentNodes:
              stack.append(i)

    return visited, dfs_extensoes

# Método responsável pelo BFS. Aplicação iterativa do algoritmo.
def BFS(g, initial, final):

    extensoes = 0 # número de extensões do algoritmo
    queue = [] # fila de prioridades
    path = []
    visited = [False] * len(g.nodeList) # vetor de visitados

    queue.append(initial) # adiciona o nó atual na fila
    visited[initial.id] = True # marca o nó atual como visitado
                
    # Enquanto a fila não estiver vazia
    while len(queue) != 0: 
        
        extensoes += 1
        initial = queue.pop(0) 
        visited[initial.id] = True 

        # Descomente a linha abaixo se desejar printar o caminho
        # print(initial.posX, initial.posY)
        path.append(initial)

        # Verifica se o nó atual é o nó destino
        if initial.id == final.id: 
            # print("BFS encontrou!")
            return extensoes, path

        # Adicionando vizinhos do nó atual na fila
        for v in initial.adjacentNodes:
            extensoes += 1
            if visited[v.id] == False: 
                queue.append(v) 
                visited[v.id] = True

# Hill Climbing
## Calcula a distância entre dois nós
def Eval(node, goal):
    distance = abs(node.posX - goal.posX) + abs(node.posY - goal.posY)
    return distance

## Retorna uma lista contendo todos os vizinhos de um nó
def Neighbors(node):
    L = []
    for neighbors in node.adjacentNodes:
      L.append(neighbors)
    return L

## Printa um caminho
def printPath(path):
    for node in path:
      print(node.posX, node.posY)

## Algoritmo simples do Hill Climbing
## NÃO garante uma resposta
def HillClimb(startNode, goalNode, graph):

    extensoes = 0
    currentNode = startNode
    path = []
    
    while True:

        extensoes += 1
        path.append(currentNode) # Adiciona o nó atual no vetor 'path'
        if Eval(currentNode, goalNode) == 0: # Se chegou no destino, retorna
            
            # print("HillClimb encontrou!")
            return path, extensoes

        L = Neighbors(currentNode)
        nextEval = 10000
        nextNode = None
        
        # Para todos os vizinhos, verifica qual é o mais próximo ao destino
        for i in L:
            extensoes += 1

            # Se existir um nó mais próximo ao destino, define ele como o
            # próximo nó a ser visitado
            if Eval(i, goalNode) < nextEval:
                nextNode = i
                nextEval = Eval(i, goalNode)
        
        # Se existir um nó melhor, retorna o 'path' incompleto
        if nextEval >= Eval(currentNode, goalNode):
          return path, extensoes

        currentNode = nextNode

# Método responsável pelo cálculo da distância de Manhattan
# Ele é aplicado como heurística no algoritmo Best-First Search
def manhattanDistance(x1,y1,x2,y2):
    return (abs(x1-x2) + abs(y1-y2))

# Algoritmo de busca Best-First Search
def bestFirstSearch(g, start, final):

    extensoes = 0
    path = []

    queue = []
    heapify(queue) # Criando uma fila de prioridades (min-heap) vazia 

    cost = [Aux] * len(g.nodeList) # Criando um vetor de custos
    cost[start.id] = Aux(start.id,0)

    visited = [False] * len(g.nodeList) # Criando vetor de visitados

    # Inserindo o vetor inicial na fila de prioridades
    heappush(queue,cost[start.id])

    # Enquanto a fila não estiver vazia
    while len(queue) != 0:

        extensoes += 1

        # Pega o nó de menor prioridade na fila
        current = g.nodeList[heappop(queue).id]

        # Para ver o caminho, descomente a linha abaixo
        # print(current.posX, current.posY)
        path.append(current)
        
        # Verifica se o nó atual é o nó destino
        if current.id == final.id:
            # print("Best-First-Search encontrou!")
            return extensoes, path
        
        else:            
            for neighbour in current.adjacentNodes:
                if visited[neighbour.id] == False:

                    visited[neighbour.id] = True
                    cost[neighbour.id] = Aux(neighbour.id, 
                                             cost[current.id].weight + 1 
                                             + manhattanDistance(neighbour.posX,neighbour.posY,final.posX,final.posY))

                    heappush(queue, cost[neighbour.id])
            
            visited[current.id] = True

    return extensoes, path

# Método responsável pelo cálculo da distância euclideana
# def euclideanDistance(a, b):
#     return math.sqrt(math.pow(b.posX - a.posX,2) + math.pow(b.posY - a.posY,2))

# Algoritmo de busca A* (A star)
def a_Star(g, start, end):

    extensoes = 0
    path = []
    frontier = Q.PriorityQueue()
    frontier.put(start.id, 0)

    cost = [0.0] * len(g.nodeList) # inserimos em cost, já que é o menor custo

    cost[start.id] = -1

    # Enquanto a fila não estiver vazia
    while not frontier.empty():

        extensoes += 1
        current = g.nodeList[frontier.get()]

        # Descomente abaixo se precisar imprimir o caminho
        # print(current.posX, current.posY)
        # path.append(current)

        # Verificando se chegou no final
        if current.id == end.id:
            # print("aStar encontrou!")
            return extensoes, path
        
        # Percorrendo vizinhos do atual
        for next in current.adjacentNodes:
            
            extensoes += 1
            # 1 eh o custo do atual até chegar em qualquer um adjacente à ele
            new_cost = cost[current.id] + 1

            # se o custo até o próximo nó não foi calculado e guardado no vetor de custos 
            # ou se o que estiver no vetor de custo for maior do que o que foi calculado na iteração atual
            
            if cost[next.id] == 0.0 or new_cost < cost[next.id]:
                cost[next.id] = new_cost
                priority = new_cost + manhattanDistance(next.posX, next.posY, end.posX, end.posY)
                
                frontier.put(next.id, priority)
                path.append(current)
                
    return extensoes, path

"""#### Programa

##### Funções utilizadas na main
Abaixo, encontram-se as funções utilizadas na main. O programa cliente as utiliza para a montagem do grafo.
"""

# Método responsável pela impressão colorida do labirinto mostrando o caminho
# (cor rosa) percorrido pelo algoritmo 'nomeAlgoritmo' a partir de um ponto 
# inicial (cor verde) até o destino (cor vermelha)
def imprimeLabirintoColorido(path, labirinto, linhas, colunas, nomeAlgoritmo):

    # Essas duas listas serão responsáveis pelo armazenamento dos valores
    # numéricos do eixo-x e eixo-y
    x, y = [],[]

    # Inicializando o mapa onde serão impressas as cores
    mapa = np.zeros((linhas,colunas), dtype=int)

    # Convertendo nosso labirinto para uma matriz
    lab = np.asarray(labirinto)

    temHifen = False
    charCount = 0
    
    # Atribuindo um valor inteiro para cada posição na matriz, de forma que
    # cada caracter tenha uma cor específica
    for i in range(linhas):
        for j in range(colunas):
            if (lab[i][j] == "-"):
                mapa[i][j] = 0
                temHifen = True
            elif (lab[i][j] == "*"):
                mapa[i][j] = 1
            elif (lab[i][j] == "#"):
                mapa[i][j] = 2
            elif (lab[i][j] == "$"):
                mapa[i][j] = 3

    # Percorrendo o mapa e colorindo de rosa o caminho feito pelo algoritmo
    # até o encontro (ou não) do destino
    for i in range(len(path)):
        if mapa[path[i].posX][path[i].posY] == 2 or mapa[path[i].posX][path[i].posY] == 3:            
            continue
        else:
            if mapa[path[i].posX][path[i].posY] == 1:
                charCount += 1
            mapa[path[i].posX][path[i].posY] = 4

    # Imprimindo o mapa colorido
    if temHifen:
        if len(path) > 1:
            cores = 'black gray green red pink'.split() # define color
        else:
            cores = 'black gray green red'.split() # define color
    else:
        if charCount == (linhas*colunas) - 2:
            cores = 'green red pink'.split() # define color
        else:
            cores = 'gray green red pink'.split() # define color

    cmap = matplotlib.colors.ListedColormap(cores, name='colors', N=None)
    figure(num=None, figsize=(8, 8), dpi=80)
    
    plt.title("Caminho feito pelo algoritmo "+nomeAlgoritmo, fontsize=15)
    plt.imshow(mapa, cmap=cmap)
    
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # plt.grid(False)
    plt.show()

# Método responsável pela leitura do arquivo contendo o labirinto,
# bem como o armazenamento do número de linhas, colunas e do próprio labirinto
def lerLabirinto(arquivo):

	arqLabirinto = open(arquivo, 'r')

	conteudo = arqLabirinto.read().split()

	linhas = int(conteudo[0])
	colunas = int(conteudo[1])
	labirinto = conteudo[2:]
	
	arqLabirinto.close()
 
	return linhas, colunas, labirinto

# Função responsável pela criação do grafo a partir do labirinto lido
def createGraph(linhas, colunas, labirinto):
	
	global node_id
	node_id = 0
	
	g = Graph(linhas*colunas)

	for i in range(linhas):
		for j in range(colunas):
			# Se a posição for um caminho possível, cria um nó no grafo
			if labirinto[i][j] == '#':
				 createNode(g, labirinto, linhas, colunas, i, j)

	return g

# Função responsávelpela criação dos nós, bem como a atribuição dos 
# nós adjacentes, do grafo.
def createNode(grafo, matriz, NLMat, NCMat, posX, posY):

	# Se o nó da posição atual já foi criado, retorna
	no = grafo.returnNode(posX, posY)
	
	if no == None:
		no = Node(posX, posY, True if matriz[posX][posY] == '$' else False)
		# Criando a adiciona o nó atual no grafo
		grafo.addNodeToGraph(no) 
	else:
		return no

	# Chamadas recursivas da função createNode() para todos os nós.
	# No retorno, cria as arestas entre os nós
	if posX + 1 < NLMat and (matriz[posX + 1][posY] == '*' or matriz[posX + 1][posY] == '$'):
		back = createNode(grafo, matriz, NLMat, NCMat, posX+1, posY)
		if (back != None):
			no.addAdjNode(back)
			back.addAdjNode(no)

	if posX - 1 >= 0 and (matriz[posX - 1][posY] == '*' or matriz[posX - 1][posY] == '$'):
		back = createNode(grafo, matriz, NLMat, NCMat, posX-1, posY)
		if (back != None):
			no.addAdjNode(back)
			back.addAdjNode(no)

	if posY + 1 < NCMat and (matriz[posX][posY + 1] == '*' or matriz[posX][posY + 1] == '$'):
		back = createNode(grafo, matriz, NLMat, NCMat, posX, posY+1)
		if (back != None):
			no.addAdjNode(back)
			back.addAdjNode(no)

	if posY - 1 >= 0 and (matriz[posX][posY - 1] == '*' or matriz[posX][posY - 1] == '$'):
		back = createNode(grafo, matriz, NLMat, NCMat, posX, posY-1)
		if (back != None):
			no.addAdjNode(back)
			back.addAdjNode(no)

	return no # retorna o nó na chamada da recursão para criar a aresta

"""##### Main
O programa inteiro é executado a partir daqui
"""

numExecucoes = 1 # quantidade de execuções para fazer a média
numLabirintos = 10 # número de labirintos de teste

for i in range(numLabirintos):

    # O nome do arquivo deve ser LabirintoNUM.txt, onde NUM corresponde
    # à um número até 'numLabirintos' definido anteriormente
    nomeArq = 'Labirinto'+str(i+1)+'.txt'

    # Inicializando variáveis
    linhas = 0
    colunas = 0
    labirinto = 0

    # Recebendo o número de linhas e colunas e o labirinto
    linhas, colunas, labirinto = lerLabirinto(nomeArq)

    # Criando o grafo
    g = createGraph(linhas, colunas, labirinto)

    # Salvando o nó inicial do labirinto (aquele cuja posição 
    # corresponde) ao caracter '#'
    noInicial = g.nodeList[0]

    # Salvando o nó final do labirinto (aquele cuja posição 
    # corresponde) ao caracter '$' e o atributo "boolFinal" é verdadeiro
    noFinal = g.findFinalNode()

    # Verifica se foi possível encontrar o nó destino. Se não, pula para
    # a execução do próximo labirinto
    if noFinal == None:
        print("Labirinto impossível")
        continue

    # Inicializando variáveis de média e extensões de cada algoritmo
    # Na posição 0: DFS | Na posição 1: BFS | Na posição 2: Hill Climbing
    # Na posição 3: Best-First Search | Na posição 4: A*

    time_values = [0 for i in range(5)]
    extension_values = [0 for i in range(5)]

    for j in range(numExecucoes):
        
        dfs_start_time = time.time() # Contabilizando tempo de início
        
        dfs_path, dfs_extensoes = depth_first_search(g, noInicial, noFinal)

        dfs_end_time = time.time() # Contabilizando tempo de término

        # Contabilização do tempo de execução e quantidade de extensões
        time_values[0] += (dfs_end_time - dfs_start_time)
        extension_values[0] += dfs_extensoes

        imprimeLabirintoColorido(dfs_path, labirinto, linhas, colunas, "DFS")

        bfs_start_time = time.time()
        bfs_extensoes, bfs_path = BFS(g, noInicial, noFinal)
        bfs_end_time = time.time()

        # Contabilização do tempo de execução e quantidade de extensões
        time_values[1] += (bfs_end_time - bfs_start_time)
        extension_values[1] += bfs_extensoes

        imprimeLabirintoColorido(bfs_path, labirinto, linhas, colunas, "BFS")

        bestFirst_start_time = time.time()
        bestFirst_extensoes, bestfirst_path = bestFirstSearch(g, noInicial, noFinal)
        bestFirst_end_time = time.time()
        
        # Contabilização do tempo de execução e quantidade de extensões
        time_values[3] += (bestFirst_end_time - bestFirst_start_time)
        extension_values[3] += bestFirst_extensoes

        imprimeLabirintoColorido(bestfirst_path, labirinto, linhas, colunas, "Best First Search")

        aStar_start_time = time.time()
        aStar_extensoes, aStar_path = a_Star(g, noInicial,noFinal)
        aStar_end_time = time.time()

        imprimeLabirintoColorido(aStar_path, labirinto, linhas, colunas, "A Star")
        
        # Contabilização do tempo de execução e quantidade de extensões
        time_values[4] += (aStar_end_time - aStar_start_time)
        extension_values[4] += aStar_extensoes

        hillClimbing_start_time = time.time()
        hillClimbing_path, hillClimbing_extensoes = HillClimb(noInicial, noFinal, g)
        hillClimbing_end_time = time.time()

        # Contabilização do tempo de execução e quantidade de extensões
        time_values[2] += (hillClimbing_end_time - hillClimbing_start_time)
        extension_values[2] += hillClimbing_extensoes

        imprimeLabirintoColorido(hillClimbing_path, labirinto, linhas, colunas, "Hill Climbing")

    print("Médias do tempo de execuções para o Labirinto ", str(i+1))

    time_values[0] = time_values[0] / numExecucoes # dfs
    time_values[1] = time_values[1] / numExecucoes # bfs
    time_values[2] = time_values[2] / numExecucoes # hillClimbing
    time_values[3] = time_values[3] / numExecucoes # best-first
    time_values[4] = time_values[4] / numExecucoes # a star

    print("DFS: ", time_values[0])
    print("BFS: ", time_values[1])
    print("Best First: ", time_values[3])
    print("A Star: ", time_values[4])
    print("Hill Climbing: ", time_values[2])
    print("\n")

    print("Médias de extensões para o Labirinto ", str(i+1))

    extension_values[0] = extension_values[0] / numExecucoes # dfs
    extension_values[1] = extension_values[1] / numExecucoes # bfs
    extension_values[2] = extension_values[2] / numExecucoes # hill climbing
    extension_values[3] = extension_values[3] / numExecucoes # best-first
    extension_values[4] = extension_values[4] / numExecucoes # a star

    print("DFS: ", extension_values[0])
    print("BFS: ", extension_values[1])
    print("Best First: ", extension_values[3])
    print("A Star: ", extension_values[4])
    print("Hill Climbing: ", extension_values[2])
    print("---------------------------------------------", "\n")