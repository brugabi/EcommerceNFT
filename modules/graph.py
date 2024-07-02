import json
from geopy.distance import geodesic
import igraph as ig

def calcular_distancia(source: str, target: str):
    locacoes = {
        "Barra": [-13.0134, -38.5087],
        "Pelourinho": [-12.9714, -38.5109],
        "Rio Vermelho": [-13.0161, -38.4906],
        "Pituba": [-12.9994, -38.4602],
        "Itapuã": [-12.9519, -38.3538],
        "Ondina": [-13.0092, -38.5002],
        "Graça": [-13.0021, -38.5174],
        "Brotas": [-12.9847, -38.4850],
        "Amaralina": [-12.9981, -38.4609],
        "Stiep": [-12.9989, -38.4515],
        "Caminho das Árvores": [-12.9801, -38.4594],
        "Imbuí": [-12.9896, -38.4386],
        "Paralela": [-12.9573, -38.4373],
        "Boca do Rio": [-12.9713, -38.4400],
        "Patamares": [-12.9275, -38.3822],
        "Piatã": [-12.9351, -38.3780],
        "Stella Maris": [-12.9103, -38.3348],
        "Centro": [-12.9711, -38.5014],
        "Comércio": [-12.9664, -38.5130],
        "São Cristóvão": [-12.8997, -38.3536],
        "Alphaville": [-12.9398, -38.3736],
        "Pernambués": [-12.9843, -38.4608],
        "Iguatemi": [-12.9796, -38.4551],
        "Federação": [-13.0048, -38.5143],
        "Bonfim": [-12.9262, -38.5107]
        }

    adjacencias = {
        "Barra": ["Ondina", "Graça", "Rio Vermelho"],
        "Pelourinho": ["Centro", "Comércio", "Brotas"],
        "Rio Vermelho": ["Ondina", "Amaralina", "Barra"],
        "Pituba": ["Amaralina", "Boca do Rio", "Caminho das Árvores"],
        "Itapuã": ["São Cristóvão", "Alphaville", "Patamares"],
        "Ondina": ["Barra", "Rio Vermelho", "Amaralina"],
        "Graça": ["Barra", "Brotas", "Amaralina"],
        "Brotas": ["Centro", "Federação", "Pelourinho"],
        "Amaralina": ["Rio Vermelho", "Pituba", "Graça"],
        "Stiep": ["Pituba", "Caminho das Árvores", "Imbuí"],
        "Caminho das Árvores": ["Pituba", "Stiep", "Iguatemi"],
        "Imbuí": ["Paralela", "Stiep", "Centro"],
        "Paralela": ["Imbuí", "Boca do Rio", "Pituba"],
        "Boca do Rio": ["Pituba", "Paralela", "Itapuã"],
        "Patamares": ["Itapuã", "Piatã", "Stella Maris"],
        "Piatã": ["Patamares", "Stella Maris", "Itapuã"],
        "Stella Maris": ["Itapuã", "Patamares", "Piatã"],
        "Centro": ["Pelourinho", "Comércio", "Brotas"],
        "Comércio": ["Pelourinho", "Centro", "Bonfim"],
        "São Cristóvão": ["Itapuã", "Bonfim", "Pernambués"],
        "Alphaville": ["Itapuã", "Pernambués", "Iguatemi"],
        "Pernambués": ["Iguatemi", "Alphaville", "São Cristóvão"],
        "Iguatemi": ["Caminho das Árvores", "Pernambués", "Stiep"],
        "Federação": ["Brotas", "Graça", "Bonfim"],
        "Bonfim": ["Comércio", "São Cristóvão", "Federação"]
    }

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