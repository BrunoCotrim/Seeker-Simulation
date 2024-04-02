#import pygame
#import neat
#import sys
#from Constantes import *
from Objetos import *
#from NeuralNetwork import NN
#from Reproducao import reproduzir

#Inicialização
#pygame.init()

JANELA = pygame.display.set_mode((WN_WIDTH,WN_HEIGHT))


#Relógio
RELOGIO = pygame.time.Clock()
frameseg = 2200
ROUND = 1
MAX_ROUND = 1000
TAM_POP = 20
Food = 50
MIN_FOOD = 15
ENERGIA_MAXIMA = 50


POPULACAO = []
for i in range(TAM_POP):
    individuo = Seeker(random.randrange(WN_WIDTH), random.randrange(WN_HEIGHT), CIANO, ESCALA, SEEKERS) 
    individuo.gerar_rede_neural(sensores = 32, prim_geracao = True, max_conexoes_extra = 30)
    POPULACAO.append(individuo)

while ROUND < MAX_ROUND:
    if ROUND % 20 == 0:
        frameseg /=2


    pygame.display.set_caption(f"Learning Seekers: {ROUND}")
    TIMER = 1200
    player = Seeker.live[0]

    for _ in range(Food):
        Pellet(random.randrange(WN_WIDTH), random.randrange(WN_HEIGHT),BRANCO,ESCALA,COMIDA) 

    #Loop
    rodando = True
    while rodando and TIMER:
        if len(COMIDA) < MIN_FOOD:
            Pellet(random.randrange(WN_WIDTH), random.randrange(WN_HEIGHT),BRANCO,ESCALA,COMIDA) 


        TIMER -= 1

        #comandos
        mouse = pygame.mouse.get_pressed()
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RIGHT]:
            pass
        if teclas[pygame.K_LEFT]:
            pass
        if teclas[pygame.K_UP]:
            pass
        if teclas[pygame.K_DOWN]:
            pass

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if event.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        # Preenche a janela com cor
        JANELA.fill(PRETO)  

        #Receber comandos
        player.ouvir_comandos(teclas)


        # Desenhar tudo ---------------------------
        
        pygame.draw.line(JANELA,BRANCO,(WN_WIDTH//2, WN_HEIGHT//2),(player.x,player.y),1)

        for i in COMIDA:
            i.desenhar(JANELA)
            i.update()
        for i in Seeker.live:
            i.update(JANELA, VERMELHO)



        pygame.display.flip()  #Atualiza o display inteiro
        
        #pygame.display.update(player.rect)   #Atualiza apenas os itens

        # Atualiza a tela
        pygame.display.update()  
        RELOGIO.tick(frameseg)  # Limita a taxa de quadros

    # --- Fim da Geração e Avaliação ---
    ROUND += 1
    avaliacao = quick_sort_key([[i, i.estomago] for i in POPULACAO], 1)
    Seeker.live = []
    POPULACAO = [Seeker(random.randrange(WN_WIDTH), random.randrange(WN_HEIGHT), CIANO, ESCALA, reproduzir(avaliacao[0][0].cerebro, avaliacao[random.randint(0,3)][0].cerebro), SEEKERS) for i in range (TAM_POP)]
    COMIDA.empty()

    

        


# Finalização do Pygame
pygame.quit()
sys.exit()




