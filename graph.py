class graph:
    def __init__(self, undirected):
        self.adjacency_list = {}
        self.undirected = undirected
    
    def add_vertex(self, vertex):
        if vertex in self.adjacency_list:
            print(f"O vértice {vertex} já existe...")
        else:
            print(f"Adicionando o vértice {vertex}")
            self.adjacency_list[vertex] = {}
    
    def add_edge(self, from_vertex, to_vertex, weight=1):
        if from_vertex in self.adjacency_list and to_vertex in self.adjacency_list:
            if self.has_edge(from_vertex, to_vertex):
                print(f"Já existe uma aresta entre os vértices {from_vertex} e {to_vertex}")
            else:
                print(f"Adicionando a aresta {weight} entre os vértices {from_vertex} e {to_vertex}")
                self.adjacency_list[from_vertex][to_vertex] = weight
                if self.undirected:
                    self.adjacency_list[to_vertex][from_vertex] = weight
        else:
            if from_vertex not in self.adjacency_list:
                print(f"O vértice {from_vertex} não existe, criando agora...")
                self.add_vertex(from_vertex)
            
            if to_vertex not in self.adjacency_list:
                print(f"O vértice {to_vertex} não existe, criando agora...")
                self.add_vertex(to_vertex)
            
            self.add_edge(from_vertex, to_vertex, weight)
    
    def remove_vertex(self, vertex):
        if vertex in self.adjacency_list:
            print(f"Removendo o vértice {vertex}...")

            for neighbors in self.adjacency_list:
                if vertex in self.adjacency_list[neighbors]:
                    self.adjacency_list[neighbors].pop(vertex)
            
            self.adjacency_list.pop(vertex)
        else:
            print(f"O vértice {vertex} não existe")
    
    def remove_edge(self, from_vertex, to_vertex):
        if from_vertex in self.adjacency_list and self.has_edge(from_vertex, to_vertex):
            print(f"Removendo aresta entre {from_vertex} e {to_vertex}")
            self.adjacency_list[from_vertex].pop(to_vertex)
            if self.undirected:
                self.adjacency_list[to_vertex].pop(from_vertex)
        else:
            print(f"A aresta entre {from_vertex} e {to_vertex} não existe")
    
    def has_edge(self, from_vertex, to_vertex):
        return to_vertex in self.adjacency_list[from_vertex]

    def in_degree(self, vertex):
        in_degree = 0
        for neighbor in self.adjacency_list:
            if vertex in self.adjacency_list[neighbor]:
                in_degree += 1
        return in_degree
    
    def out_degree(self, vertex):
        return len(self.adjacency_list[vertex]) if vertex in self.adjacency_list else 0
    
    def degree(self, vertex):
        if self.undirected:
            return len(self.adjacency_list[vertex])
        else:
            return self.in_degree(vertex) + self.out_degree(vertex)
    
    def get_weight(self, from_vertex, to_vertex):
        weight = None
        if from_vertex in self.adjacency_list and to_vertex in self.adjacency_list[from_vertex]:
            weight = self.adjacency_list[from_vertex][to_vertex]
        return weight
    
    def print(self):
        for vertex, neighbors in self.adjacency_list.items():
            print(f"{vertex}: {neighbors}")
    
    def populate(self, csv_data, fields):
        for index, row in csv_data.iterrows():
            source = row[fields[0]].upper().replace(" ", "")
            target = row[fields[1]].upper().replace(" ", "")
            
            if source not in self.adjacency_list:
                self.add_vertex(source)
            
            if target not in self.adjacency_list:
                self.add_vertex(target)
            
            self.add_edge(source, target)
    
    def degree_centrality(self, node):
        n = len(self.adjacency_list)
        if self.undirected:
            return len(self.adjacency_list[node]) / (n - 1)
        else:
            return self.out_degree(node) / (n - 1)