import glob, os, math
import random

def main():
    pasta = 'entradas/'
    quantidade_de_resultados = int(input('Quantos resultados por arquivo precisa? '))
    print("As soluções estarão na pasta HillClimbing_Solucoes. Estará separado por arquivos.\n")

    for nome_arquivo in glob.glob(os.path.join(pasta, '*.txt')):
        with open(nome_arquivo, 'r') as arquivo:
            print("Arquivo de entrada: " + nome_arquivo[9:])

            inputs = [linha.rstrip() for linha in arquivo] #lê as linhas do arquivo e retira os \n
            matriz_pesos = gerar_pesos(inputs)
            for i in range(quantidade_de_resultados):
                print("Gerando solução nº:", i+1, end='', flush=True)

                solucao, valor = hill_climbing(matriz_pesos)
                escrever_em_arquivo(nome_arquivo, solucao, valor)
                print(" - Executado.")
            print()
            



#cria uma matriz, onde cada linha representa a distncia para todos os vértices existentes incluindo ele mesmo
def gerar_pesos(inputs):
    matriz_pesos = []
    for input_ in inputs:
        distancias = []
        valores = input_.split() #cria uma lista de valores separados por espaços ['1', '6734', '1453'] ['2', '2233', '10']
        
        if len(valores) == 0: # verifica se a linha lida está em branco
            continue          # se tiver, loop é interrompido e continua na proxima iteração

        vertice = {'vertice': valores[0], 'x': valores[1], 'y': valores[2]}
        
        for input_2 in inputs:
            valores2 = input_2.split() #cria uma lista de valores separados por espaços ['1', '6734', '1453'] ['2', '2233', '10']
            
            if len(valores2) == 0:
                continue
            
            vertice2 = {'vertice': valores2[0], 'x': valores2[1], 'y': valores2[2]}
            distancias.append(calcular_distancia(vertice, vertice2))
        
        matriz_pesos.append(distancias)

    return matriz_pesos


# calcula a distancia entre dois vertices
def calcular_distancia(vertice, vertice2):
    distancia_x = pow(float(vertice['x']) - float(vertice2['x']), 2)
    distancia_y = pow(float(vertice['y']) - float(vertice2['y']), 2)

    distancia_vertice = math.sqrt(distancia_x + distancia_y)
    return round(distancia_vertice, 2) # retorna valor arredondado para duas casas decimais


def gerar_solucao_aleatoria(matriz_pesos):
    cidades = list(range(len(matriz_pesos)))
    solucao = []

    for i in range(len(matriz_pesos)):
        cidade_aleatoria = cidades[random.randint(0, len(cidades) - 1)]
        solucao.append(cidade_aleatoria)
        cidades.remove(cidade_aleatoria)

    return solucao


def tamanho_rota(matriz_pesos, solucao):
    valor_solucao = 0
    for i in range(len(solucao)):
        valor_solucao += matriz_pesos[solucao[i - 1]][solucao[i]] # soma a distancia da cidade anterior com a atual
    
    return valor_solucao


# gera uma solução um pouco diferente da solução atual baseado nas cidades vizinhas
def get_vizinhos(solucao):
    vizinhos = []
    for i in range(len(solucao)):
        for j in range(i + 1, len(solucao)):
            vizinho = solucao.copy() # função copy para gerar uma cópia da lista q não faz referência a lista original
            vizinho[i] = solucao[j]
            vizinho[j] = solucao[i]
            vizinhos.append(vizinho)
    return vizinhos


# calcula o melhor vizinho baseado na distancia entre a cidade atual
def get_melhor_vizinho(matriz_pesos, vizinhos):
    melhor_valor_rota = tamanho_rota(matriz_pesos, vizinhos[0])
    melhor_vizinho = vizinhos[0]

    for vizinho in vizinhos:
        valor_rota_atual = tamanho_rota(matriz_pesos, vizinho)

        if valor_rota_atual < melhor_valor_rota:
            melhor_valor_rota = valor_rota_atual
            melhor_vizinho = vizinho

    return melhor_vizinho, melhor_valor_rota


def hill_climbing(matriz_pesos):
    solucao_atual = gerar_solucao_aleatoria(matriz_pesos)
    valor_da_solucao = tamanho_rota(matriz_pesos, solucao_atual)
    vizinhos = get_vizinhos(solucao_atual)
    melhor_vizinho, melhor_valor_rota_vizinho = get_melhor_vizinho(matriz_pesos, vizinhos)

    while melhor_valor_rota_vizinho < valor_da_solucao:
        solucao_atual = melhor_vizinho
        valor_da_solucao = melhor_valor_rota_vizinho
        vizinhos = get_vizinhos(solucao_atual)
        melhor_vizinho, melhor_valor_rota_vizinho = get_melhor_vizinho(matriz_pesos, vizinhos)

    return solucao_atual, valor_da_solucao
        

def escrever_em_arquivo(nome_arquivo, solucao, valor): 

    if not os.path.exists('HillClimbing_Solucoes/'):
        os.mkdir('HillClimbing_Solucoes/')


    gravar = str(solucao) + " => " + str(round(valor, 2)) + "\n"
    arquivo_solucao = nome_arquivo[9:len(nome_arquivo)-4] + "_solucao.txt"

    try:
        f2 = open('HillClimbing_Solucoes/'+arquivo_solucao, 'a')
    except:
        f2 = open('HillClimbing_Solucoes/'+arquivo_solucao, 'w')
    finally:
        f2.write(gravar)
        f2.close()



if __name__ == '__main__':
    main()