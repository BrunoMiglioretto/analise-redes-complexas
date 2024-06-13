class graph:
    def __init__(self, undirected):
        self.adjacency_list = {}
        self.undirected = undirected
        self.vertices_count = 0
        self.edges_count = 0

    def _check_vertex(self, vertex):
        return vertex in self.adjacency_list

    def add_vertex(self, vertex):
        if self._check_vertex(vertex):
            print(f"O vértice {vertex} já existe...")
        else:
            self.adjacency_list[vertex] = {}
            self.vertices_count += 1

    def add_edge(self, from_vertex, to_vertex, weight=1):
        if from_vertex not in self.adjacency_list:
            self.add_vertex(from_vertex)

        if to_vertex not in self.adjacency_list:
            self.add_vertex(to_vertex)

        if to_vertex in self.adjacency_list[from_vertex]:
            weight = self.adjacency_list[from_vertex][to_vertex]

        self.adjacency_list[from_vertex][to_vertex] = weight
        if self.undirected:
            self.adjacency_list[to_vertex][from_vertex] = weight

        self.edges_count += 1

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

    def populate_with_director_and_actor(self, data):
        for _, row in data.iterrows():
            director_data = str(row["director"])
            actors_data = str(row["cast"])

            director = director_data.upper().strip()
            actors = map(lambda x: str(x).upper().strip(), actors_data.split(","))

            if director and actors:
                if director not in self.adjacency_list:
                    self.add_vertex(director)

                for actor in actors:
                    if actor not in self.adjacency_list:
                        self.add_vertex(actor)

                    self.add_edge(actor, director)

    def populate_with_partner_actors(self, data):
        for _, row in data.iterrows():
            actors_data = str(row["cast"])
            actors = map(lambda x: str(x).upper(), actors_data.split(","))

            for actor in actors:
                if actor not in self.adjacency_list:
                    self.add_vertex(actor)

                for partner in actors:
                    self.add_edge(actor, partner)

    def _dfs(self, node, visited, stack=None):
        visited.add(node)
        component = [node]
        for neighbor in self.adjacency_list[node]:
            if neighbor not in visited:
                component.extend(self._dfs(neighbor, visited, stack))
        if stack is not None:
            stack.append(node)
        return component if stack is None else []

    def _strongly_connected_components(self):
        stack = []
        visited = set()
        for vertex in self.adjacency_list:
            if vertex not in visited:
                self._dfs(vertex, visited, stack)

        transpose_graph = {v: [] for v in self.adjacency_list}
        for vertex in self.adjacency_list:
            for neighbor in self.adjacency_list[vertex]:
                transpose_graph[neighbor].append(vertex)

        visited.clear()
        scc_list = []

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                scc = self._dfs(vertex, visited)
                scc_list.append(scc)

        return len(scc_list)

    def get_components_count(self):
        if self.undirected:
            visited = set()
            components_count = 0
            for vertex in self.adjacency_list:
                if vertex not in visited:
                    self._dfs(vertex, visited)
                    components_count += 1
            return components_count
        else:
            return self._strongly_connected_components()

    def get_spanning_tree(self, start_vertex):
        if not self._check_vertex(start_vertex):
            print(f"O vértice {start_vertex} não existe")
            return [], 0

        spanning_tree = []
        total_cost = 0
        visited = set()
        edges = [(0, start_vertex, None)]

        while edges:
            edges.sort()
            weight, current, from_vertex = edges.pop(0)
            if current not in visited:
                visited.add(current)
                if from_vertex is not None:
                    spanning_tree.append((from_vertex, current, weight))
                    total_cost += weight

                for neighbor in self.adjacency_list[current]:
                    if neighbor not in visited:
                        edges.append(
                            (self.adjacency_list[current][neighbor], neighbor, current)
                        )

        return spanning_tree, total_cost

    def _degree_centrality(self, vertex):
        n = len(self.adjacency_list)
        if self.undirected:
            return len(self.adjacency_list[vertex]) / (n - 1)
        else:
            return self.out_degree(vertex) / (n - 1)

    def top_k_degree_centrality(self, k):
        centrality = {
            vertex: self._degree_centrality(vertex) for vertex in self.adjacency_list
        }
        sorted_centrality = sorted(
            centrality.items(), key=lambda item: item[1], reverse=True
        )
        return sorted_centrality[:k]

    def _betweenness_centrality(self):
        betweenness = {v: 0.0 for v in self.adjacency_list}

        for s in self.adjacency_list:
            stack = []
            predecessors = {v: [] for v in self.adjacency_list}
            shortest_paths = {v: 0 for v in self.adjacency_list}
            shortest_paths[s] = 1
            distances = {v: -1 for v in self.adjacency_list}
            distances[s] = 0
            queue = [s]

            while queue:
                v = queue.pop(0)
                stack.append(v)
                for w in self.adjacency_list[v]:
                    if distances[w] < 0:
                        queue.append(w)
                        distances[w] = distances[v] + 1
                    if distances[w] == distances[v] + 1:
                        shortest_paths[w] += shortest_paths[v]
                        predecessors[w].append(v)

            dependency = {v: 0 for v in self.adjacency_list}
            while stack:
                w = stack.pop()
                for v in predecessors[w]:
                    dependency[v] += (shortest_paths[v] / shortest_paths[w]) * (
                        1 + dependency[w]
                    )
                if w != s:
                    betweenness[w] += dependency[w]

        if self.undirected:
            for v in betweenness:
                betweenness[v] /= 2.0

        return betweenness

    def top_k_betweenness_centrality(self, k):
        betweenness = self._betweenness_centrality()
        sorted_centrality = sorted(
            betweenness.items(), key=lambda item: item[1], reverse=True
        )
        return sorted_centrality[:k]

    def _closeness_centrality(self, vertex):
        distances = {}
        for v in self.adjacency_list:
            if v != vertex:
                distances[v] = float("inf")

        distances[vertex] = 0
        visited = set()
        visited.add(vertex)
        queue = [vertex]

        while queue:
            current_vertex = queue.pop(0)
            for neighbor in self.adjacency_list[current_vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    distances[neighbor] = distances[current_vertex] + 1

        total_distance = sum(distances.values())

        closeness_centrality = 0
        for dist in distances.values():
            closeness_centrality += 1 / dist if dist != 0 else 0

        if len(self.adjacency_list) > 1:
            closeness_centrality = (
                (len(distances) - 1) / total_distance * closeness_centrality
            )
        else:
            closeness_centrality = 0

        return closeness_centrality

    def top_k_closeness_centrality(self, k):
        closeness = {
            vertex: self._closeness_centrality(vertex) for vertex in self.adjacency_list
        }
        sorted_centrality = sorted(
            closeness.items(), key=lambda item: item[1], reverse=True
        )
        return sorted_centrality[:k]
