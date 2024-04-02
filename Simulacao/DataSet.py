import math
import random

random.seed(40)

def variavel(minimo, maximo):
    return random.randint(minimo, maximo)

def hipotenusa(c1, c2):
    catetos = c1**2 + c2**2
    return math.sqrt(catetos)
    
def angulo(x, y):
    return math.atan2(y,x)

def gerar_dados(FIELD_SIZE, DATA_SIZE):

    TRAINING_COORD = [[variavel(-FIELD_SIZE,FIELD_SIZE),variavel(-FIELD_SIZE,FIELD_SIZE)] for i in range(DATA_SIZE)]


    TRAINING_DIST = [[hipotenusa(*i), angulo(*i) ] for i in TRAINING_COORD]

    return [TRAINING_COORD,TRAINING_DIST]








print("DataSet <OK>")