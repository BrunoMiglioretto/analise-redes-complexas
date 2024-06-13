from collections import defaultdict


class Grafo:
    def __init__(self, ehdirecionado=True):
        self.adjacency_list = defaultdict(list)
        self.direcionado = ehdirecionado

    def __str__(self):
        return self.imprime_lista_adjacencias()

    def adiciona_vertice(self, nome):
        if nome not in self.adjacency_list:
            self.adjacency_list[nome] = []
        else:
            print(f"O vértice {nome} já existe!")

    def get_ordem(self):
        return len(self.adjacency_list)

    def get_tamanho(self):
        tam = 0
        for lista in self.adjacency_list.values():
            tam += len(lista)
        return tam

    def adiciona_aresta(self, org_nome, dest_nome, peso=1):
        if dest_nome not in self.adjacency_list:
            self.adiciona_vertice(dest_nome)
        if org_nome not in self.adjacency_list:
            self.adiciona_vertice(org_nome)
        if self.direcionado:
            if not self.tem_aresta(org_nome, dest_nome):
                self.adjacency_list[org_nome].append([dest_nome, peso])
            else:
                peso = self.get_peso(org_nome, dest_nome) + 1
                indice = self.get_aresta(org_nome, dest_nome)
                self.adjacency_list[org_nome][indice][1] = peso
        else:
            if not self.tem_aresta(org_nome, dest_nome):
                self.adjacency_list[org_nome].append([dest_nome, 0])
            if not self.tem_aresta(dest_nome, org_nome):
                self.adjacency_list[dest_nome].append([org_nome, 0])
            if self.tem_aresta(org_nome, dest_nome) and self.tem_aresta(
                dest_nome, org_nome
            ):
                peso = self.get_peso(org_nome, dest_nome) + 1
                indice_org_dest = self.get_aresta(org_nome, dest_nome)
                indice_dest_org = self.get_aresta(dest_nome, org_nome)
                self.adjacency_list[org_nome][indice_org_dest][1] = peso
                self.adjacency_list[dest_nome][indice_dest_org][1] = peso

    def adiciona_varias_arestas(self, dest, lista_de_org):
        for org in lista_de_org:
            self.adiciona_aresta(org, dest)

    def remove_aresta(self, u, v):
        if self.tem_aresta(u, v):
            indice = self.get_aresta(u, v)
            del self.adjacency_list[u][indice]
        else:
            print("Aresta inexistente!")

    def get_aresta(self, org_nome, dest_nome):
        for i, valor in enumerate(self.adjacency_list[org_nome]):
            if valor[0] == dest_nome:
                return i

    def remove_vertice(self, u):
        if u in self.adjacency_list:
            del self.adjacency_list[u]
            for chave, lista in self.adjacency_list.items():
                lista[:] = [v for v in lista if v[0] != u]
        else:
            print(f"A chave '{u}' não existe no dicionário.")

    def tem_aresta(self, u, v):
        return any(valor[0] == v for valor in self.adjacency_list[u])

    def get_peso(self, u, v):
        for valor in self.adjacency_list[u]:
            if valor[0] == v:
                return valor[1]

    def grau_entrada(self, u):
        entradas = 0
        for valores in self.adjacency_list.values():
            for valor in valores:
                if valor[0] == u:
                    entradas += 1
        return entradas

    def grau_saida(self, u):
        return len(self.adjacency_list[u])

    def grau(self, u):
        return self.grau_entrada(u) + self.grau_saida(u)

    def imprime_lista_adjacencias(self):
        for chave, valor in self.adjacency_list.items():
            print(f"{chave}: ", end=" ")
            for v in valor:
                print(f"{v}", end=" -> ")
            print("\n")
        return " "
