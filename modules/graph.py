import json
from geopy.distance import geodesic
import igraph as ig

def calcular_distancia(source: str, target: str):
    with open('bairros.json', 'r') as json_bairros:
        locacoes = json.load(json_bairros)
    
    with open('adjacencias.json', 'r') as json_adjacencias:
        adjacencias = json.load(json_adjacencias)

    # Criando o grafo igraph
    grafo = ig.Graph(directed=True)

    # Adicionando vértices com atributos de localização
    for nome, localizacao in locacoes.items():
        grafo.add_vertex(name=nome, location=localizacao)

    # Adicionando arestas com pesos calculados usando geodesic distance (em km)
    for origem, destinos in adjacencias.items():
        origem_loc = locacoes[origem]
        for destino in destinos:
            destino_loc = locacoes[destino]
            distancia = geodesic(origem_loc, destino_loc).kilometers
            grafo.add_edge(origem, destino, weight=distancia)

    # Encontrando o caminho mais curto com Dijkstra
    caminho = grafo.get_shortest_paths(v=source, to=target, weights='weight', mode='out', output='vpath', algorithm='dijkstra')[0]
    distancia_total = sum(grafo.es[grafo.get_eid(caminho[i], caminho[i+1])]['weight'] for i in range(len(caminho) - 1))
    
    # Obtendo os nomes dos bairros no caminho
    bairros_no_caminho = [grafo.vs[vertice]['name'] for vertice in caminho]

    return distancia_total, bairros_no_caminho