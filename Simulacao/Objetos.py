#from typing import Any
import pygame
import random

from Utilidades import *
from Constantes import *

from NeuralNetwork import NN



# Inicialização do Pygame
pygame.init()

SEEKERS = pygame.sprite.Group()
HUNTERS = pygame.sprite.Group()
COMIDA = pygame.sprite.Group()

class Seeker(pygame.sprite.Sprite):
    largura, altura = 30,60
    seekercount = 0
    live = []

    def __init__(self, x, y, cor, scale = 5, tipo = 2, cerebro = None, *groups) -> None:
        super().__init__(groups)
        #Variaveis principais
        self.scale = scale
        self.largura, self.altura = 6*scale ,12*scale 
        self.x = x - self.largura / 2 #Offset
        self.y = y - self.altura / 2 #Offset
        self.centro = (self.largura/2, self.altura/2)
        
        self.cerebro = cerebro
        self.visao = []
        self.raio_visao = RAIO_VISAO
        self.estomago = 0
        self.consumido = 0 # Variavel para analise
        self.energia = ENERGIA_MAXIMA
        self.tipo = tipo
        
        self.cor1 = cor # Cor base
        self.cor2 = cor # Cor do núcleo
        
        #Variaveis Movimento autonomo
        self.autonomia = True
        self.current_move = 0 #Apenas um counter para continuar se movendo aleatoriamente em testes (Remover)
        self.turn = 0
        self.resposta = [0,0,0,0]

        self.vel = 3
        self.vel_giro = 2
        self.angle = random.randint(-179,179)

        self.image = pygame.Surface((self.largura, self.altura),pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = (self.x,self.y))
        pygame.draw.polygon(self.image, self.cor1,[[0,self.altura/4],[self.largura/2,0],[self.largura,self.altura/4],[self.largura/2,self.altura]])
        
        
        Seeker.seekercount += 1
        self.seekercount = Seeker.seekercount

        Seeker.live.append(self)

    def desenhar(self,tela, cor2):
        img_girada = pygame.transform.rotate(self.image,self.angle) #Gira a imagem

        
        #Nucleo desenhado separado para sua cor ser dinamica
        pygame.draw.circle(self.image, self.cor2,[self.largura/2,self.altura/2],5*self.scale/4)

        #Gera um novo rect baseado na nova imagem rotacionada
        self.rect = img_girada.get_rect(center=(self.x, self.y))

        #Coloca a imagem no rect na tela
        tela.blit(img_girada, self.rect)

        self.cor2 = cor2

    def andar(self, movimento = 1):
        self.energia -= movimento
        self.x += math.sin(math.radians(self.angle)) * self.vel * movimento
        self.y += math.cos(math.radians(self.angle)) * self.vel * movimento
              
    def girar(self,angulo):
        self.angle += angulo * self.vel_giro
        self.energia -= angulo/5 # Consome 1/4 da energia aplicada

    def ouvir_comandos(self,keys):
        if keys[pygame.K_UP]:
            self.autonomia = False
            self.andar()
        if keys[pygame.K_LEFT]:
            self.autonomia = False
            self.girar(5)
        if keys[pygame.K_RIGHT]:
            self.autonomia = False
            self.girar(-5)
        if keys[pygame.K_DOWN]:
            self.autonomia = False
            self.andar(-0.5)

    def procurar(self):
        self.visao = []
        

        for pellet in COMIDA:
            distx = self.rect.centerx - pellet.rect.centerx
            disty = self.rect.centery - pellet.rect.centery
            distancia = hipotenusa(distx, disty)
            angle = angulo(distx, disty)

            if distancia <= self.raio_visao:
                self.visao.append(1)
                self.visao.append(distancia)
                self.visao.append(angle)
        
        for seeker in SEEKERS:
            distx = self.rect.centerx - seeker.rect.centerx
            disty = self.rect.centery - seeker.rect.centery
            distancia = hipotenusa(distx, disty)
            angle = angulo(distx, disty)

            if distancia <= self.raio_visao:
                self.visao.append(2)
                self.visao.append(distancia)
                self.visao.append(angle)
        
        for hunter in HUNTERS:
            distx = self.rect.centerx - hunter.rect.centerx
            disty = self.rect.centery - hunter.rect.centery
            distancia = hipotenusa(distx, disty)
            angle = angulo(distx, disty)
            
            if distancia <= self.raio_visao:
                self.visao.append(3)
                self.visao.append(distancia)
                self.visao.append(angle)
        
    def update(self,tela, cor = MAGENTA):
        
        colisao = pygame.sprite.spritecollide(self, COMIDA, False)
        #---- Tratar colisao ----
        for i in colisao:
            COMIDA.remove(i)
            self.estomago += 1

        # Desenha e ativa a visão
        self.desenhar(tela, cor)

        #Limites da Tela
        if self.x < 0 - self.largura:
            self.x  = WN_WIDTH + self.largura

        elif self.x > WN_WIDTH + self.largura:
            self.x = 0 - self.largura 

        if self.y < 0 - self.altura:
            self.y = WN_HEIGHT + self.altura 
        elif self.y > WN_HEIGHT + self.altura:
            self.y = 0 - self.altura 
        
        

        self.auto_pilot()

    def organizar_dados(self, inputs):
        resultado = [math.radians(self.angle % 360), self.energia]
        counter = 0
        sensores = len(self.cerebro.layers["sensores"])
        
        while sensores > len(resultado)  and len(inputs) > 0:
            resultado.append(inputs[counter])

        return resultado

    def auto_pilot(self):
        if self.autonomia:
            self.procurar()
            self.cerebro(self.organizar_dados(self.visao))
            self.resposta = self.cerebro.output(softmax=True) #self.cerebro.output(softmax=True)
            if self.consumido < self.estomago:
                self.consumido += 1
                self.energia += 20


            if self.energia > 0:
                self.andar(self.resposta[0]) # Frente
                self.girar(-self.resposta[1]) #Direita
                self.girar(self.resposta[2]) #Esquerda
                self.andar(-self.resposta[3]) #Ré
            else:
                self.cor1 = BRANCO
                self.cor2 = PRETO

        else:
            self.cor2 = VERDE

        self.autonomia = True #Recuperar controle
    
    def gerar_rede_neural(self, sensores=10, prim_geracao = False, max_conexoes_extra = 0):
        # ---- Rede Neural ----
        self.cerebro = NN(sensores,4)
        if prim_geracao:
            self.cerebro.gerar_conexoes(max_conexoes_extra)
        
    def __call__(self, inputs):
        pass

    def __repr__(self) -> str:
        return f"Seeker: {self.seekercount} | Pos: {(self.x,self.y)} | Estomago: {self.estomago}"

class Pellet(pygame.sprite.Sprite):
    pellets = []
    def __init__(self, x, y, cor, scale=5, *groups: SEEKERS) -> None:
        super().__init__(*groups)
        self.raio = 1 * scale
        self.x = x
        self.y = y
        self.cor = cor

        self.image = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)

        # Desenha dois circulos na superfície (self.image)
        pygame.draw.circle(self.image, self.cor, (self.raio, self.raio), self.raio)
        pygame.draw.circle(self.image, PRETO, (self.raio, self.raio), self.raio,1)

        # Inicia o self.rect depois para envolver o círculo corretamente
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Adiciona também um retângulo colorido para visualização
        #pygame.draw.rect(self.image, VERMELHO, self.image.get_rect(),2)  # Cor vermelha

        self.energia = 10  # Placeholder
        Pellet.pellets.append(self)

    def desenhar(self,tela):
        self.rect = self.image.get_rect(center=(self.x, self.y))

        tela.blit(self.image,self.rect)
    
    def update(self):
        #self.x+=random.random() * 2 - 1
        #self.y+=random.random() * 2 - 1
        pass


"""
if __name__ == "__main__":


    # Tela
    WN_WIDTH, WN_HEIGHT = 1200, 700
    WN_WIDTH, WN_HEIGHT = 600, 300 # resolucao de teste
    screen = pygame.display.set_mode((WN_WIDTH, WN_HEIGHT))
    pygame.display.set_caption("Moving the Block")
    ESCALA = 3





    for i in range(1):
        individuo = Seeker(WN_WIDTH // 2, WN_HEIGHT // 2, CIANO, ESCALA, SEEKERS) 
        individuo.gerar_rede_neural(sensores = 10, prim_geracao = True, max_conexoes_extra = 10)
    player = Seeker.live[0]


    for _ in range(20):
        Pellet(random.randrange(WN_WIDTH), random.randrange(WN_HEIGHT),BRANCO,ESCALA,COMIDA) 


    #clock = pygame.time.Clock()
    frameseg = 30

    # Main game loop
    while True:

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Comandos
        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        for i,k in enumerate(keys):
            if k:
                print(f"keyboard : {i} - {k}")
        for i,k in enumerate(mouse):
            if k:
                print(f"mouse : {i} - {k}")


        #if keys[pygame.K_UP]:
        #    player.andar()
        #if keys[pygame.K_LEFT]:
        #    player.girar(5)
        #if keys[pygame.K_RIGHT]:
        #    player.girar(-5)
        #if keys[pygame.K_DOWN]:
        #    pass


        #Receber comandos
        player.ouvir_comandos(keys)


        # Limpar a tela antes de desenhar
        screen.fill((0, 0, 0))


        # Desenhar tudo ---------------------------
        
        pygame.draw.line(screen,BRANCO,(WN_WIDTH//2, WN_HEIGHT//2),(player.x,player.y),1)

        for i in Pellet.pellets:
            i.desenhar(screen)
            i.update()
        for i in Seeker.live:
            #i.desenhar(screen, VERMELHO)
            i.update(screen, VERMELHO)


        #Outros Updates ----------------------------
        #SEEKERS.update(screen)
        #COMIDA.update(screen)
        #Atualizar o display
        pygame.display.flip()  #Atualiza o display inteiro
        
        #pygame.display.update(player.rect)   #Atualiza apenas os itens

        # Frame rate
        #clock.tick(frameseg)
"""

