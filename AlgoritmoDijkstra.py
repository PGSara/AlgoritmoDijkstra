import networkx as nx
import matplotlib.pyplot as plt

def dijkstra(grafo, inicio):
    distancias = {no: float('inf') for no in grafo.nodes}
    distancias[inicio] = 0
    visitados = set()

    while len(visitados) < len(grafo.nodes):
        # Seleciona o nó não visitado com a menor distância
        no_atual = min((n for n in grafo.nodes if n not in visitados), key=lambda n: distancias[n])

        for vizinho in grafo.neighbors(no_atual):
            peso = grafo[no_atual][vizinho]['weight']
            nova_distancia = distancias[no_atual] + peso
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia

        visitados.add(no_atual)

    return distancias

# Criando o grafo
G = nx.Graph()

# Adicionando arestas com pesos
G.add_edge('A', 'B', weight=1)
G.add_edge('A', 'C', weight=4)
G.add_edge('B', 'C', weight=2)
G.add_edge('B', 'D', weight=5)
G.add_edge('C', 'D', weight=1)

# Rodando o algoritmo de Dijkstra
inicio = 'A'
distancias = dijkstra(G, inicio)

# Visualizando o grafo
pos = nx.spring_layout(G)  # Posição dos nós

# Desenhar o grafo
nx.draw(G, pos, with_labels=True, node_color='#6d098c', font_weight='bold', node_size=1000, font_color='white')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Mostrando as distâncias calculadas
for no, distancia in distancias.items():
    x, y = pos[no]
    plt.text(x, y - 0.1, f'Dist: {distancia}', fontsize=9, color='black', ha='center')

plt.title(f'Dijkstra a partir do nó {inicio}')
plt.show()
