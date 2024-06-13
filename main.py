from grafo import *
import csv


def processar_linha(linha):
    diretor = linha[3].strip().upper()
    elenco = linha[4].strip().upper()

    if diretor and elenco:
        return [diretor.replace(" ", "").split(","), elenco.replace(" ", "").split(",")]
    return None


def abri_e_processar_arquivo(nome_do_arquivo):
    with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
        leitor_csv = csv.reader(arquivo, delimiter=",")
        next(leitor_csv)
        linhas_processadas = []
        for linha in leitor_csv:
            linha_processada = processar_linha(linha)
            if linha_processada:
                linhas_processadas.append(linha_processada)
    return linhas_processadas


linhas_processadas = abri_e_processar_arquivo(
    "TDE5 dataset/netflix_amazon_disney_titles.csv"
)

# # EX 001 parte 1
# G = Grafo()
# for linha in linhas_processadas:
#     for diretor in linha[0]:
#         G.adiciona_varias_arestas(diretor, linha[1])
#
# print(f'O número de vértices é: {G.get_ordem()}.')
# print(f'O número de arestas é: {G.get_tamanho()}.')

# EX 001 parte 2
G = Grafo()
for linha in linhas_processadas:
    for i in range(len(linha[1])):
        for j in range(i + 1, len(linha[1])):
            G.adiciona_aresta(linha[1][i], linha[1][j])

print(f"O número de vértices é: {G.get_ordem()}.")
print(f"O número de arestas é: {G.get_tamanho()}.")


# G = Grafo(False)
# # Adicionando vértices
# G.adiciona_vertice('Pedro')
# G.adiciona_vertice('Maria')
# G.adiciona_vertice('Antônio')
# G.adiciona_vertice('Clara')
#
# # Adicionando arestas e pesos
# G.adiciona_aresta('Pedro', 'Maria')
# G.adiciona_aresta('Pedro', 'Antônio')
# G.adiciona_aresta('Maria', 'Clara')
# G.adiciona_aresta('Clara',  'Maria')
#
# print(G)
