import random
import math


# Acha os inputs dos Neuronios() para usar no forward pass:
def achar_inputs(neuronio, sinapses, rede):
    rede_neural_entrada = rede["sensores"] + rede["ocultas"]
    rede_neural_saida = rede["ocultas"] + rede["saida"]
    inputs = []

    for conexao in sinapses:

        if neuronio.ID == conexao.saida and conexao.ativa == True:
            for i in rede_neural_entrada:
                if i.ID == conexao.entrada:
                    inputs.append(i.output*conexao.peso)

    return inputs

# ----- Calculo de chances e sorteio ------
def probabilidade(taxa=0.5):
    return random.random() < taxa

def sortear(opcao_a, opcao_b, taxa = 0.5):
    return opcao_a if probabilidade(taxa) else opcao_b

# ----- Calcula diferenças entre 2 objetos NN() -----

def calcular_diff(sujeito, base):
    diferenca = 0

    for i in base.neuronios: # Neuronios nao presentes no sujeito
        if i.ID not in [j.ID for j in sujeito.neuronios]:
            diferenca += 1


    neur_base = {n.ID : [n.vies,n.ativ] for n in base.neuronios}
    for i in sujeito.neuronios:
        try: # Neuronio com vies diferente
            if not neur_base[i.ID][0] == i.vies and not neur_base[i.ID][1] == i.ativ:
                diferenca += 1

        except: # Neuronio nao presente na base
            diferenca += 1


    for i in base.conexoes: # Sinapses nao presentes no sujeito
        if i.inov_id not in [j.inov_id for j in sujeito.conexoes]:
            diferenca += 1
    
    sinapses_base = {n.inov_id : n.peso for n in base.conexoes}
    for i in sujeito.conexoes:
        try: # Sinapses com peso diferente
            if not sinapses_base[i.inov_id] == i.peso:
                diferenca += 1
        except: # Conexao nao presente na base
            diferenca += 1

    return diferenca

# ----- Quick Sort -----
def quick_sort(lista):
    if len(lista) <= 1:
        return lista

    pivot = lista.pop(0)
    maior = [i for i in lista if i >= pivot]
    menor = [i for i in lista if i < pivot]

    return quick_sort(menor) + [pivot] + quick_sort(maior)

# ----- Quick Sort modificado para listas -----
def quick_sort_key(lista, key=0):
    if len(lista) <= 1:
        return lista

    pivot = lista.pop(0)
    maior = [i for i in lista if i[key] >= pivot[key]]
    menor = [i for i in lista if i[key] < pivot[key]]

    return quick_sort_key(maior,key) + [pivot] + quick_sort_key(menor,key)

# ----- Media de valores em uma lista -----
def media(valores):
    return sum(valores) / len(valores)

# ----- Calculo de angulos e hipotenusa -----
def hipotenusa(c1, c2):

    return math.sqrt((c1**2) + (c2**2))
    
    
def angulo(x, y):
    return math.atan2(y,x)

print("Utilidades <OK>")

