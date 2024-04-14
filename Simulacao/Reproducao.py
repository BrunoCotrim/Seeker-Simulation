import random
import copy
import numpy as np
from Utilidades import *
from NeuralNetwork import *


def sortear_sinapses(sinapses_alfa, sinapses_beta, dominancia):
    alfas = {i.inov_id : i.peso for i in sinapses_alfa}
    betas = {i.inov_id : i.peso for i in sinapses_beta}
    exclusivo_alfa = [copy.copy(i) for i in sinapses_alfa if i.inov_id not in betas.keys()]
    exclusivo_beta = [copy.copy(i) for i in sinapses_beta if i.inov_id not in alfas.keys() and probabilidade(0.5)] #50% chance de adicionar uma conexao exclusiva de beta
    sinapses = []
    
    for i in sinapses_alfa:
        if i.inov_id not in alfas.keys() or i.inov_id not in betas.keys():
            continue #Ignora os exclusivos
        peso_sorteado = sortear(alfas[i.inov_id], betas[i.inov_id], dominancia)
        temp = Conexao(i.entrada, i.saida, peso_sorteado)
        sinapses.append(temp)
    
    prole = sinapses + exclusivo_alfa + exclusivo_beta
    return prole

def conexao_existe(sinapse, lista_sinapses):
    return sinapse.inov_id in [i.inov_id for i in lista_sinapses]

def gerar_id(individuo):
    ocultos = [i.ID for i in individuo.layers["ocultas"]]
    id_minimo = individuo.hidden_id_min
    
    while id_minimo in ocultos:
        id_minimo += 1
    return id_minimo

def sortear_vies(neuronio, vies_alfa, vies_beta, fator_dominancia):
    if neuronio.ID in vies_alfa.keys():
        if neuronio.ID in vies_beta.keys(): # Se o neuronio estiver presente nos dois cai aqui
            vies_escolhido = sortear(vies_alfa[neuronio.ID], vies_beta[neuronio.ID], fator_dominancia)
            return vies_escolhido
        
        vies_escolhido = vies_alfa[neuronio.ID] # Se estiver presente apenas em alfa passa direto para esse
    
    elif neuronio.ID in vies_beta.keys(): # Se estiver presente em beta apenas cai aqui
        vies_escolhido = vies_beta[neuronio.ID]

    else: # Se for exclusivo cai aqui
        vies_escolhido = random.uniform(-3,3)

    return vies_escolhido

def encaixar_neuronio(neuronio, individuo): #Adicionar neuronio dentro de uma sinapse
    #Inclui o neuronio na rede
    individuo.layers["ocultas"].append(neuronio)
    individuo.neuronios.append(neuronio)

    #Seleciona a sinapse e separa seus dados para manipulacao
    sinapse_original = random.choice(individuo.conexoes) 
    entrada_original =  sinapse_original.entrada
    saida_original = sinapse_original.saida
    peso_original = sinapse_original.peso

    #Gera novas sinapses, as insere na rede e, por fim, desativa a sinapse original
    nova_sinapse_entrada = Conexao(entrada_original, neuronio.ID, sortear(peso_original,random.uniform(-3,3),0.9))
    nova_sinapse_saida = Conexao(neuronio.ID, saida_original, sortear(peso_original,random.uniform(-3,3),0.9))
    individuo.conexoes.append(nova_sinapse_entrada)
    individuo.conexoes.append(nova_sinapse_saida)
    sinapse_original.ativa = False

def reproduzir(rede_neural_1, rede_neural_2, fator_dominancia = 0.8, taxa_mutação = 0.2):
    alfa = rede_neural_1
    beta = rede_neural_2
    rede_a = [i.ID for i in alfa.layers["ocultas"]]
    rede_b = [i.ID for i in beta.layers["ocultas"] if i.ID not in rede_a]
    rede_p = rede_a+rede_b


    prole = NN(len(alfa.layers["sensores"]), len(alfa.layers["saida"]), hidden=rede_p) # Criação da prole

    mutacoes = 0 #contador de mutacoes
    maximo = 8 #maximo de mutacoes
    #-------- Definindo Sinapses com Mutação -------
    sinapses_prole = sortear_sinapses(alfa.conexoes,beta.conexoes, fator_dominancia)
    
    if probabilidade(taxa_mutação): # -- Mutação no peso --
        temp = random.choice(sinapses_prole)
        temp.peso += random.uniform(-3,3)

        mutacoes+=1
 
    if probabilidade(taxa_mutação): # -- Mutação na ativação --
        temp = random.choice(sinapses_prole)
        temp.ativa = not temp.ativa
        
        mutacoes+=1
    
    if probabilidade(taxa_mutação): # -- Mutação Criar/Reativar/Desativar sinapse --
        recursive = True
        while recursive: # Testa se a conexao será recursiva
            entrada = random.choice(prole.layers["sensores"] + [i for i in prole.layers["ocultas"]]).ID
            saida = random.choice([i for i in prole.layers["ocultas"]] + prole.layers["saida"]).ID
            recursive = entrada == saida
        
        temp = Conexao(entrada,saida,peso = random.uniform(-3,3))

        
        if not conexao_existe(temp, prole.conexoes):
            sinapses_prole.append(temp)
            
        mutacoes+=1


    prole.conexoes = sinapses_prole # Coloca a nova lista de sinapses na prole

    #------------------------------------

    #-------- Mutacoes em Neuronios --------
    # ---- Remove Neuronio com Sinapse ----
    if probabilidade(taxa_mutação) and len(rede_p) > 0: 
        temp = random.choice(prole.layers["ocultas"])
        prole.layers["ocultas"].remove(temp)
        prole.neuronios.remove(temp)
        
        mutacoes+=1

    # ---- Adição de Neuronio em Sinapse ----
    if probabilidade(taxa_mutação): 
        temp = Neuronio(gerar_id(prole)) # Usa a funcao para calcular o id mais baixo disponivel para o neuronio
        encaixar_neuronio(temp, prole)

        mutacoes+=1

    # ---- Alteração de Ativação ----
    if probabilidade(taxa_mutação):
        temp = random.choice(prole.neuronios)
        nova_ativ = random.randrange(len(temp.ativacoes))

        while temp.ativ == nova_ativ: # Garante que a mutação achará um valor diferente
            nova_ativ = random.randrange(len(temp.ativacoes))

        temp.ativ = nova_ativ

        mutacoes+=1
    
    # ---- Definindo Vieses com Mutação ----

    vies_alfa = {v.ID:v.vies for v in alfa.neuronios}
    vies_beta = {v.ID:v.vies for v in beta.neuronios}

    for neuronio in prole.neuronios:
        neuronio.vies = sortear_vies(neuronio, vies_alfa, vies_beta, fator_dominancia)
        
        maximo += 1
        if probabilidade(taxa_mutação): # -- Mutação --
            neuronio.vies += random.uniform(-1,1) 
            
            mutacoes+=1


    # ---- Mutando Vieses individuais ----
    if probabilidade(taxa_mutação): # -- Mutação --
        temp = random.choice(prole.neuronios)
        temp.vies = random.uniform(-1,1)
        
        mutacoes+=1

    #------------------------------------
        
    # ---- Remoção de sinapses soltas ----
    validacao_de_neuronios = [i.ID for i in prole.neuronios]
    sinapses_inuteis = []
    for i in prole.conexoes:
        if i.entrada not in validacao_de_neuronios or i.saida not in validacao_de_neuronios:
            sinapses_inuteis.append(i)


    return prole


def reproduzir_solo(rede_neural, taxa_mutacao = 0.2):
    alfa = rede_neural
    rede_a = [i.ID for i in alfa.layers["ocultas"]]
    rede_p = rede_a


    prole = NN(len(alfa.layers["sensores"]), len(alfa.layers["saida"]), hidden=rede_p) # Criação da prole

    mutacoes = 0
    #-------- Definindo Sinapses com Mutação -------
    sinapses_prole = alfa.conexoes
    
    if probabilidade(taxa_mutacao): # -- Mutação no peso --
        temp = random.choice(sinapses_prole)
        temp.peso += random.uniform(-3,3)

        mutacoes+=1
 
    if probabilidade(taxa_mutacao): # -- Mutação na ativação --
        temp = random.choice(sinapses_prole)
        temp.ativa = not temp.ativa
        
        mutacoes+=1
    
    if probabilidade(taxa_mutacao): # -- Mutação Criar/Reativar/Desativar sinapse --
        recursive = True
        while recursive: # Testa se a conexao será recursiva
            entrada = random.choice(prole.layers["sensores"] + [i for i in prole.layers["ocultas"]]).ID
            saida = random.choice([i for i in prole.layers["ocultas"]] + prole.layers["saida"]).ID
            recursive = entrada == saida
        
        temp = Conexao(entrada,saida,peso = random.uniform(-3,3))

        
        if not conexao_existe(temp, prole.conexoes):
            sinapses_prole.append(temp)
            
        mutacoes+=1


    prole.conexoes = sinapses_prole # Coloca a nova lista de sinapses na prole

    #------------------------------------

    #-------- Mutacoes em Neuronios --------
    # ---- Remove Neuronio com Sinapse ----
    if probabilidade(taxa_mutacao) and len(prole.layers["ocultas"]) > 0: 
        temp = random.choice(prole.layers["ocultas"])
        prole.layers["ocultas"].remove(temp)
        prole.neuronios.remove(temp)
        
        mutacoes+=1

    # ---- Adição de Neuronio em Sinapse ----
    if probabilidade(taxa_mutacao): 
        temp = Neuronio(gerar_id(prole)) # Usa a funcao para calcular o id mais baixo disponivel para o neuronio
        encaixar_neuronio(temp, prole)

        mutacoes+=1

    # ---- Alteração de Ativação ----
    if probabilidade(taxa_mutacao):
        temp = random.choice(prole.neuronios)
        nova_ativ = random.randrange(len(temp.ativacoes))

        while temp.ativ == nova_ativ: # Garante que a mutação achará um valor diferente
            nova_ativ = random.randrange(len(temp.ativacoes))

        temp.ativ = nova_ativ

        mutacoes+=1
    
    # ---- Definindo Vieses com Mutação ----

    vies_alfa = {v.ID:v.vies for v in prole.neuronios}


    for neuronio in prole.neuronios:
        neuronio.vies = vies_alfa[neuronio.ID]
        
        if probabilidade(taxa_mutacao): # -- Mutação --
            neuronio.vies += random.uniform(-1,1) 
            
            mutacoes+=1


    # ---- Mutando Vieses individuais ----
    if probabilidade(taxa_mutacao): # -- Mutação --
        temp = random.choice(prole.neuronios)
        temp.vies = random.uniform(-1,1)
        
        mutacoes+=1

    #------------------------------------
        
    # ---- Remoção de sinapses soltas ----
    validacao_de_neuronios = [i.ID for i in prole.neuronios]
    sinapses_inuteis = []
    for i in prole.conexoes:
        if i.entrada not in validacao_de_neuronios or i.saida not in validacao_de_neuronios:
            sinapses_inuteis.append(i)
    for i in sinapses_inuteis:
        prole.conexoes.remove(i)

    print(mutacoes)

    return prole



