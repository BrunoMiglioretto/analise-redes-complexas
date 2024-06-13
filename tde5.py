import matplotlib.pyplot as plt
import pandas as pd

from graph import graph


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

    print(len(director_actor_collaboration_graph.adjacency_list))
    print(len(actors_collaboration_graph.adjacency_list))

    print("Buscando os 10 vértices com maiores graus de centralidade ")
    top_10_directed = director_actor_collaboration_graph.top_k_degree_centrality(k=10)
    top_10_undirected = actors_collaboration_graph.top_k_degree_centrality(k=10)

    plot_top_k(
        top_k=top_10_directed, title="Grafo direcionado", ylabel="Centralidade de grau"
    )
    plot_top_k(
        top_k=top_10_undirected,
        title="Grafo não direcionado",
        ylabel="Centralidade de grau",
    )

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
