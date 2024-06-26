import matplotlib.pyplot as plt
import pandas as pd

from graph import graph

def plot_top_k(top_k, title, ylabel):
    vertices, centralities = zip(*top_k)
        
    plt.figure(figsize=(10, 5))
    plt.title(title)
    plt.bar(vertices, centralities, color='blue')
    plt.xlabel('Vértices')
    plt.ylabel(ylabel)
    plt.xticks(rotation=30)
    plt.show()

if __name__ == '__main__':
    file_path = '../netflix_amazon_disney_titles.csv'
    data = pd.read_csv(file_path).dropna()
    fields = ['director', 'cast']

    directed_graph = graph(undirected=False)
    directed_graph.populate(csv_data=data, fields=fields)

    undirected_graph = graph(undirected=True)
    undirected_graph.populate(csv_data=data, fields=fields)

    top_10_directed = directed_graph.top_k_degree_centrality(k=10)
    top_10_undirected = undirected_graph.top_k_degree_centrality(k=10)

    plot_top_k(
        top_k=top_10_directed,
        title="Grafo direcionado",
        ylabel="Centralidade de grau"
    )
    plot_top_k(
        top_k=top_10_undirected,
        title="Grafo não direcionado",
        ylabel="Centralidade de grau"
    )

    top_10_directed = directed_graph.top_k_betweenness_centrality(k=10)
    top_10_undirected = undirected_graph.top_k_betweenness_centrality(k=10)
    
    plot_top_k(
        top_k=top_10_directed,
        title="Grafo direcionado",
        ylabel="Centralidade de intermediação"
    )
    plot_top_k(
        top_k=top_10_undirected,
        title="Grafo não direcionado",
        ylabel="Centralidade de intermediação"
    )

    top_10_directed = directed_graph.top_k_closeness_centrality(k=10)
    top_10_undirected = undirected_graph.top_k_closeness_centrality(k=10)
    
    plot_top_k(
        top_k=top_10_directed,
        title="Grafo direcionado",
        ylabel="Centralidade de proximidade"
    )
    plot_top_k(
        top_k=top_10_undirected,
        title="Grafo não direcionado",
        ylabel="Centralidade de proximidade"
    )
