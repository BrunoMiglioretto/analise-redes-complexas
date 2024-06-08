import pandas as pd

from graph import graph

if __name__ == '__main__':
    file_path = '../netflix_amazon_disney_titles.csv'
    data = pd.read_csv(file_path).dropna()
    fields = ['director', 'cast']

    directed_graph = graph(undirected=False)
    directed_graph.populate(csv_data=data, fields=fields)

    undirected_graph = graph(undirected=True)
    undirected_graph.populate(csv_data=data, fields=fields)

    directed_graph.print()
    undirected_graph.print()
