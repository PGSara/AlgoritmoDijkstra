import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
import random

# 🌐 Grafo representando o município Tech
municipio = nx.Graph()

# 🛠️ Gera o mapa inteligente com pontos e conexões aleatórias
def gerar_mapa_inteligente():
    municipio.clear()
    try:
        total_pontos = int(entry_pontos.get())
        if total_pontos < 2:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "A quantidade de pontos deve ser um número inteiro maior que 1.")
        return

    locais = [f"Local {i+1}" for i in range(total_pontos)]
    for local in locais:
        municipio.add_node(local)

    # 🔄 Criar conexões aleatórias com pesos que representam tempo de trajeto
    for i in range(total_pontos):
        for j in range(i+1, total_pontos):
            if random.random() < 0.5:  # 50% de chance de conectar
                tempo = random.randint(1, 20)  # minutos estimados
                municipio.add_edge(locais[i], locais[j], weight=tempo)

    messagebox.showinfo("Mapa Gerado", f"{total_pontos} locais foram mapeados com conexões inteligentes.")

# 🤖 Algoritmo Dijkstra: núcleo do LunaPath
def dijkstra(mapa, inicio):
    distancias = {no: float('inf') for no in mapa.nodes}
    anteriores = {}
    distancias[inicio] = 0
    visitados = set()

    while len(visitados) < len(mapa.nodes):
        atual = min((n for n in mapa.nodes if n not in visitados),
                    key=lambda n: distancias[n], default=None)
        if atual is None:
            break
        for vizinho in mapa.neighbors(atual):
            peso = mapa[atual][vizinho]['weight']
            nova_distancia = distancias[atual] + peso
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anteriores[vizinho] = atual
        visitados.add(atual)

    return distancias, anteriores

# 🔍 Reconstrói o caminho encontrado
def reconstruir_rota(anteriores, inicio, destino):
    rota = []
    atual = destino
    while atual != inicio:
        anterior = anteriores.get(atual)
        if anterior is None:
            return []  # caminho não encontrado
        rota.append((anterior, atual))
        atual = anterior
    return list(reversed(rota))

# 🧠 Aciona o sistema LunaPath para calcular a melhor rota
def acionar_lunapath():
    origem = entry_origem.get().strip()
    destino = entry_destino.get().strip()

    if origem not in municipio.nodes or destino not in municipio.nodes:
        messagebox.showerror("Erro", "A origem ou destino não estão presentes no mapa.")
        return

    distancias, anteriores = dijkstra(municipio, origem)
    rota = reconstruir_rota(anteriores, origem, destino)

    pos = nx.spring_layout(municipio, seed=42)
    plt.figure(figsize=(10, 7))

    # 🛰️ Mostra todas as rotas possíveis
    nx.draw_networkx_edges(municipio, pos, edge_color='lightgray', width=2)

    # 🔵 Exibe os nós (locais)
    nx.draw_networkx_nodes(municipio, pos, node_color='#6d098c', node_size=1200)
    nx.draw_networkx_labels(municipio, pos, font_color='white', font_weight='bold')

    # ⏱️ Exibe os pesos das rotas (minutos)
    labels = nx.get_edge_attributes(municipio, 'weight')
    nx.draw_networkx_edge_labels(municipio, pos, edge_labels=labels)

    # 📍 Mostra distâncias até cada ponto
    for no, distancia in distancias.items():
        x, y = pos[no]
        plt.text(x, y - 0.1, f'{distancia} min', fontsize=9, color='black', ha='center')

    # 🔴 Destaca a melhor rota
    if rota:
        nx.draw_networkx_edges(municipio, pos, edgelist=rota, edge_color='red', width=3)
        tempo_total = distancias[destino]
        messagebox.showinfo("Rota Calculada", f"Melhor rota de {origem} até {destino} leva {tempo_total} minutos.")
    else:
        messagebox.showwarning("Sem Caminho", f"Dexter não encontrou um caminho de {origem} até {destino}.")

    plt.title(f"🚀 Rota de Entrega: {origem} → {destino}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# 🧠 Interface Gráfica - LunaPath
root = tk.Tk()
root.title("🌐 LunaPath - Sistema de Roteamento Inteligente de Dexter")

# 💡 Introdução
introducao = tk.Label(
    root,
    text="🌟 Bem-vindo ao LunaPath!\nNeste sistema, Dexter calcula a rota mais rápida entre pontos do município Tech.\n"
         "Informe a quantidade de locais no mapa, gere as conexões e defina origem e destino para a entrega.",
    wraplength=580, justify="center", fg="#444", font=("Helvetica", 10, "italic")
)
introducao.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

# 🔢 Entrada de número de pontos
tk.Label(frame, text="Quantidade de Locais no Mapa:").grid(row=0, column=0)
entry_pontos = tk.Entry(frame)
entry_pontos.grid(row=0, column=1)

btn_gerar = tk.Button(frame, text="Gerar Mapa Inteligente", command=gerar_mapa_inteligente)
btn_gerar.grid(row=0, column=2, padx=10)

# 🏠 Origem (Casa da Luna) e Destino (Lab de RV)
tk.Label(frame, text="Origem (Ex: Local 1):").grid(row=1, column=0)
entry_origem = tk.Entry(frame)
entry_origem.grid(row=1, column=1)

tk.Label(frame, text="Destino (Ex: Local 5):").grid(row=2, column=0)
entry_destino = tk.Entry(frame)
entry_destino.grid(row=2, column=1)

btn_calcular = tk.Button(frame, text="🚀 Acionar LunaPath", command=acionar_lunapath)
btn_calcular.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
