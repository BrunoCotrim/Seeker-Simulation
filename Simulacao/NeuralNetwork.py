import random
import numpy as np
from Utilidades import *


# ------------- Rede Neural --------------------
class NN:
    individuo = 0
    layer = 0
    def __init__(self, entrada=4, saida=4, hidden=[]): #hidden deve receber IDS de neuronios
        NN.individuo += 1
        self.individuo = NN.individuo
        self.layers = {"sensores" : self.camada(entrada), "saida" : self.camada(saida), "ocultas" : self.camada(escondidos = hidden)}
        self.hidden_id_min = entrada+saida+1
        self.neuronios = self.layers["sensores"] + self.layers["ocultas"] + self.layers["saida"]
        
        NN.layer = 0 #Reseta o numero das layers
        Neuronio.ID = 0 #Reseta o id dos neuronios

        self.conexoes = []
    

    def __call__(self, inputs):
        self.forward(inputs)
        
    #-------- Feedfoward de dados ----------
    def forward (self, inputs):
        for i in range(len(inputs)):
            self.layers["sensores"][i].output = inputs[i]

        
        for neuronio in self.layers["ocultas"] + self.layers["saida"]:
            neuronio.inputs = achar_inputs(neuronio,self.conexoes,self.layers)
            digest = np.sum(neuronio.inputs) #np.sum() trabalha mais rapido que o sum()nativo
            if digest:
                neuronio.activate(digest)
        
    #----------- Retorno da Rede Neural ----------
    def output(self,softmax=False):
        self.out = [i.output for i in self.layers["saida"]]
        if softmax:
            
            exp_out = np.exp(self.out)
            self.softmax_out = exp_out / np.sum(exp_out)
            self.softmax_out = self.softmax_out.tolist()
            return self.softmax_out

        return self.out
    
    def one_hot(self):
        self.output(softmax=True)
        #maior = self.softmax_out.index(max(self.softmax_out))
        return [1 if i  == max(self.softmax_out) else 0 for i in self.softmax_out]
    #--------- Gera sinapses aleatorias com pesos aleatorios ------
    def gerar_conexoes (self, conexoes=5): 
        sinapses = []

        #---- Gera sinapses para todos os sensores ----
        for i in self.layers["sensores"]:
            entrada = i.ID
            saida = random.choice(self.layers["ocultas"] + self.layers["saida"]).ID
            conect = Conexao(entrada,saida)

            if conect.inov_id not in sinapses:
                sinapses.append(conect.inov_id)
                self.conexoes.append(conect)

        #---- Gera sinapses para todas as saidas ----
        for i in self.layers["saida"]:
            entrada = random.choice(self.layers["sensores"] + self.layers["ocultas"]).ID
            saida = i.ID
            conect = Conexao(entrada,saida)

            if conect.inov_id not in sinapses:
                conect.peso = random.uniform(-3,3)
                sinapses.append(conect.inov_id)
                self.conexoes.append(conect)
        
        #---- Gera sinapses extras aleatorias ----
        for _ in range(conexoes):
            entrada = random.choice(self.layers["sensores"] + self.layers["ocultas"]).ID
            saida = random.choice(self.layers["ocultas"] + self.layers["saida"]).ID
            conect = Conexao(entrada,saida)

            if conect.inov_id not in sinapses:
                conect.peso = random.uniform(-3,3)
                sinapses.append(conect.inov_id)
                self.conexoes.append(conect)
    
    #--------- Cria camadas de neuronios ------------
    def camada(self, neuronios=0, escondidos = None): #Gera camadas de neuronios
        NN.layer += 1
        self.layer = NN.layer
        camada = [Neuronio(camada = self.layer) for i in range(neuronios)]

        if escondidos is not None: #Se a variavel estiver definida criar os neuronios com os valores na lista
            camada = [Neuronio(ID = i,camada = self.layer) for i in escondidos]
        
        return camada

    def analisar(self):
        print("----------------")
        print(f"Individuo {self.individuo}")
        print(f"Sinapses: {self.conexoes}")
        for i in self.conexoes:
            print(f"Sinapse: {i} - {i.peso} - {i.ativa}")
        print(f"Camadas de Neuronios: {self.neuronios}")
        print(f"Camada Oculta: {self.layers["ocultas"]}")
        for i in self.layers["ocultas"]:
            print(f"Neuronio: {i.ID} - {i.vies}")

    def __repr__(self):
        return f"{self.individuo}"

# ------------- Neuronio --------------------
class Neuronio:
    ID = 0
    def __init__(self, ID=None, camada=2, vies=None, ativ=0):
        if ID is None: #Gera um Id novo se o neuronio nao existir
            Neuronio.ID += 1
            self.ID = Neuronio.ID
        else:
            self.ID = ID
        
        self.camada = camada
        self.vies = random.uniform(-1,1) if vies is None else vies
        
        self.inputs = []
        self.output = 0

        self.ativ = int(ativ) #Index de ativacao
        self.ativacoes = ["Tahn","Sigmoid","ReLu"]
        self.func = self.ativacoes[self.ativ]

    # ------- Funcoes de ativacao -------
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def relu(self, x):
        return max(0, x)

    def tahn(self,x):
        return np.tanh(x)

    # ----------- Ativação ---------
    def activate(self, x):
        if self.func == "Tahn":
            self.output = self.tahn(x + self.vies)
        elif self.func == "Sigmoid":
            self.output =  self.sigmoid(x + self.vies)
        elif self.func == "ReLu":
            self.output = self.relu(x + self.vies)
        
    def __repr__(self):
        return f"{self.ID} - in:{self.inputs} » out:{self.output}"

# ------------- Sinapses --------------------
class Conexao:
    tabela = {}
    def __init__(self, entrada=0, saida=0, peso=None, ativa = True, inov_id = None):
        
        if inov_id is None:
            self.inov_id = entrada*1000 + saida
            self.entrada = entrada
            self.saida = saida
        else:
            self.inov_id = inov_id
            self.entrada = Conexao.tabela[self.inov_id][0]
            self.saida = Conexao.tabela[self.inov_id][1]

        self.peso = random.uniform(-3,3) if peso is None else peso
        self.ativa = ativa #Permite que uma sinapse seja desativada mas permaneça no codigo genetico

        Conexao.tabela[self.inov_id] = [self.entrada,self.saida]
    def __repr__(self):
        return f"{self.inov_id}"


print("Neural Network <OK>")





    