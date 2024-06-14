import matplotlib.pyplot as plt
import pandas as pd

from graph import graph


def plot_histogram(data, title, ylabel):
    _, centralities = zip(*data)

    plt.figure(figsize=(10, 5))
    plt.title(title)
    plt.hist(centralities)
    plt.xlabel("Vértices")
    plt.ylabel(ylabel)
    plt.xticks(rotation=30)
    plt.show()


def plot_top_k(top_k, title, ylabel):
    vertices, centralities = zip(*top_k)

    plt.figure(figsize=(10, 5))
    plt.title(title)
    plt.bar(vertices, centralities, color="blue")
    plt.xlabel("Vértices")
    plt.ylabel(ylabel)
    plt.xticks(rotation=30)
    plt.show()


if __name__ == "__main__":
    file_path = "./netflix_amazon_disney_titles.csv"
    data = pd.read_csv(file_path)
    filtered_data = data[data["type"] == "Movie"]

    print("Populando grafo para analise exploratória de colaborações entre diretores e atores")
    director_actor_collaboration_graph = graph(undirected=False)
    director_actor_collaboration_graph.populate_with_director_and_actor(data=filtered_data)

    print("Populando grafo para analise exploratória de colaborações entre atores")
    actors_collaboration_graph = graph(undirected=True)
    actors_collaboration_graph.populate_with_partner_actors(data=filtered_data)

    # Exercício 1
    print("Grafo entre diretores e atores:")
    print(f"Quantidade de vertices: {director_actor_collaboration_graph.vertices_count}")
    print(f"Quantidade de arestas: {director_actor_collaboration_graph.edges_count}")

    print("Grafo entre atores:")
    print(f"Quantidade de vertices: {actors_collaboration_graph.vertices_count}")
    print(f"Quantidade de arestas: {actors_collaboration_graph.edges_count}")

    # Exercício 2
    print("Quantidade de componentes:")
    print(f"Grafo entre diretores e atores: {director_actor_collaboration_graph.get_components_count()}")
    print(f"Grafo entre atores: {actors_collaboration_graph.get_components_count()}")

    # Exercício 3
    print("Árvore geradora mínima (Grafo entre diretores e atores):")
    spanning_tree, total_cost = director_actor_collaboration_graph.get_spanning_tree('jorge michel grau')
    print(f"Vértices: {spanning_tree}")
    print(f"Custo total: {total_cost}")

    print("Árvore geradora mínima (Grafo entre atores):")
    spanning_tree, total_cost = actors_collaboration_graph.get_spanning_tree('jorge michel grau')
    print(f"Vértices: {spanning_tree}")
    print(f"Custo total: {total_cost}")

    # Exercício 4
    print("Distribuição da centralidade dos vértices:")
    plot_histogram(
        data=director_actor_collaboration_graph.get_all_degree_centrality(),
        title="Grafo não direcionado",
        ylabel="Centralidade de grau",
    )
    plot_histogram(
        data=actors_collaboration_graph.get_all_degree_centrality(),
        title="Grafo não direcionado",
        ylabel="Centralidade de grau",
    )

    # Exercício 5
    print("Buscando os 10 vértices com maiores graus de centralidade: ")
    top_10_directed = director_actor_collaboration_graph.get_all_degree_centrality()[:10]
    top_10_undirected = actors_collaboration_graph.get_all_degree_centrality()[:10]
    plot_top_k(
        top_k=top_10_directed, title="Grafo direcionado", ylabel="Centralidade de grau"
    )
    plot_top_k(
        top_k=top_10_undirected,
        title="Grafo não direcionado",
        ylabel="Centralidade de grau",
    )

    # Exercício 6
    print("Buscando os 10 vértices com maiores graus de betweeness")
    top_10_directed = director_actor_collaboration_graph.top_k_betweenness_centrality(k=10)
    top_10_undirected = actors_collaboration_graph.top_k_betweenness_centrality(k=10)
    plot_top_k(
        top_k=top_10_directed,
        title="Grafo direcionado",
        ylabel="Centralidade de intermediação",
    )
    plot_top_k(
        top_k=top_10_undirected,
        title="Grafo não direcionado",
        ylabel="Centralidade de intermediação",
    )

    # Exercício 7
    print("Buscando os 10 vértices com maiores graus de closeness")
    top_10_directed = director_actor_collaboration_graph.top_k_closeness_centrality(k=10)
    top_10_undirected = actors_collaboration_graph.top_k_closeness_centrality(k=10)

    plot_top_k(
        top_k=top_10_directed,
        title="Grafo direcionado",
        ylabel="Centralidade de proximidade",
    )
    plot_top_k(
        top_k=top_10_undirected,
        title="Grafo não direcionado",
        ylabel="Centralidade de proximidade",
    )
