import math
from Utilidades import quick_sort_key



def avaliar(estado, resposta): # Avalia individualmente cada estado
    start = estado
    distancia = start[0]
    angulo = start[1]

    acoes = resposta
    recompensa = 1

    speed = 2
    turn_speed = 2

    #0 frente, 1 direita, 2 esquerda, 3 desacelerar
    angulo -= resposta[1] + turn_speed # Direita
    angulo += resposta[2] + turn_speed # Esquerda
    speed -= speed * resposta[3] # Freio
    nova_distancia = distancia - (resposta[0] * speed * math.cos(angulo)) # Frente

    recompensa_total = (distancia - nova_distancia) * recompensa

    return recompensa_total


def fitness(objeto, estados): # Avalia um conjunto de estados
    total_fitness = 0
    for i in estados:
        objeto(i)
        resposta = objeto.output(softmax=True)
        total_fitness += avaliar(i, resposta)
    return total_fitness


def avaliar_populacao(populacao, estados):
    ranking = []
    for individuo in populacao:
        ranking.append([individuo ,fitness(individuo, estados)])
    
    ranking = quick_sort_key(ranking, 1)
    return ranking






print("Eval <ok>")





