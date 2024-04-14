import matplotlib.pyplot as plt
import numpy as np
import random
import math
from NeuralNetwork import NN
from Reproducao import reproduzir_solo

"""
tamanho = 20

x = [i for i in range(tamanho)]
y = [np.array([np.random.uniform(0,15), np.random.uniform(0,15)]) for i in range(tamanho)]
z = [np.random.uniform(0,15) for i in range(tamanho)]

a = [1,2,3,4,1,2,3,4]
b = [10,25,30,7,12,10,25,50]


# Dados para os gráficos
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Criando a figura e os eixos para os dois gráficos
fig, axs = plt.subplots(2)

# Primeiro gráfico (superior)
axs[0].plot(x, y1, color='blue')
axs[0].set_title('Gráfico de Seno')

# Segundo gráfico (inferior)
axs[1].plot(x, y2, color='red')
axs[1].set_title('Gráfico de Cosseno')

# Ajustando o layout para evitar sobreposição
plt.tight_layout()

# Mostrando os gráficos
#plt.show()
"""


a = NN(9,4)
a.gerar_conexoes(5)


b = reproduzir_solo(a, 0.2)
