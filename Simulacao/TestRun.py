import matplotlib.pyplot as plt
from NeuralNetwork import *
from Reproducao import *
import DataSet as data
from Eval import avaliar_populacao
import random


#random.seed(40)

TAMANHO_MAPA = 300
QUANT_ESTADOS = 500
CICLOS = 100
POP_MAX = 30
CONEXOES_INICIAIS = 6
TAXA_MUTACAO = 0.15 #Alcance ideal entre 0.1 e 0.2
DOMINANCIA = 0.7 #Alcance ideal entre 0.6 e 0.7


#------ Variaveis para analise ----------
maior_fitness_da_geracao = []
media_fitness_geracao = []
conjunto_fitness_geracao = []
geracoes = [i for i in range(CICLOS)]
#----------------------------------------


pop_inicial = [NN(2,4) for i in range(POP_MAX)]
pop_final = []
for i in pop_inicial:
    i.gerar_conexoes(CONEXOES_INICIAIS)

dados = data.gerar_dados(TAMANHO_MAPA,QUANT_ESTADOS)[1]


# primeira populacao
ranking_inicial = avaliar_populacao(pop_inicial, dados)


pop_atual = pop_inicial
for i in range(CICLOS):
    selecao = avaliar_populacao(pop_atual, dados) 
    next_gen = [selecao[0][0]]
    while not len(next_gen) == POP_MAX:
        next_gen.append(reproduzir(selecao[0][0],selecao[1][0],fator_dominancia=DOMINANCIA,taxa_mutação=TAXA_MUTACAO))
    pop_atual = next_gen
    if i % 5 == 0:
        print(f"Rodada: {i} - Winner: {selecao[0]} ")

    valores_de_fitness = [i[1] for i in selecao]

    maior_fitness_da_geracao.append(selecao[0][1])
    media_fitness_geracao.append(media(valores_de_fitness))
    conjunto_fitness_geracao.append(selecao)
    

ranking_final = avaliar_populacao(pop_atual, dados)

print("Diferenca: ",calcular_diff(ranking_inicial[0][0],ranking_final[0][0]))




print("------ Ranking Inicial --------- Ranking Final ------")
for i in range(len(ranking_inicial)):
    print(f"{ranking_inicial[i]}   {ranking_final[i]}")



# ---- Plotando os valores ------

# Criando a figura e os eixos para os dois gráficos
fig, axs = plt.subplots(2)

# Primeiro gráfico (superior)
#axs[0].scatter(geracoes, media_fitness_geracao, color='blue')
for ranking in conjunto_fitness_geracao:
    boids = [i[0].individuo for i in ranking]
    avaliacoes = [i[1] for i in ranking]
    axs[0].scatter(boids, avaliacoes, s=3, marker="+")




axs[0].set_title('Fitness')


# Segundo gráfico (inferior)
axs[1].plot(geracoes, maior_fitness_da_geracao, color='red')
axs[1].plot(geracoes, media_fitness_geracao, color='green')
axs[1].set_title(f'Maior Fitness{ranking_final[0][1]}')

# Ajustando o layout para evitar sobreposição
plt.tight_layout()

# Mostrando os gráficos
plt.show()

# -------------------------------






