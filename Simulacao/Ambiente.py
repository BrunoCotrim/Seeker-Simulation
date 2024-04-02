from Objetos import *
import sys
from Reproducao import reproduzir

JANELA = pygame.display.set_mode((WN_WIDTH,WN_HEIGHT))
RELOGIO = pygame.time.Clock()
frameseg = 1200
POPULACAO = []





# Gerando Perseguidores
for i in range(POP_INICIAL_SEEKER):
    individuo = Seeker(random.randrange(WN_WIDTH), random.randrange(WN_HEIGHT), CIANO, ESCALA,2,0,SEEKERS) 
    individuo.gerar_rede_neural(sensores = 32, prim_geracao = True, max_conexoes_extra = 30)
    POPULACAO.append(individuo)

# Gerando Caçadores
for i in range(POP_INICIAL_HUNTER):
    individuo = Seeker(random.randrange(WN_WIDTH), random.randrange(WN_HEIGHT), VERMELHO, ESCALA,3,0,HUNTERS) 
    individuo.gerar_rede_neural(sensores = 32, prim_geracao = True, max_conexoes_extra = 30)
    POPULACAO.append(individuo) 


while ROUND < MAX_ROUND:

    pygame.display.set_caption(f"Learning Seekers: {ROUND}")
    TIMER = 1200

    for _ in range(MAX_FOOD):
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

        # Desenhar tudo ---------------------------

        for i in COMIDA:
            i.desenhar(JANELA)
            i.update()
        for i in SEEKERS:#Seeker.live:
            i.update(JANELA)


        # Atualiza a tela
        pygame.display.flip()  #Atualiza o display inteiro
        RELOGIO.tick(frameseg)  # Limita a taxa de quadros

    # --- Fim da Geração e Avaliação ---
    ROUND += 1
    avaliacao = quick_sort_key([[i, i.estomago] for i in POPULACAO], 1)
    COMIDA.empty()
    SEEKERS.empty()
    HUNTERS.empty()
    POPULACAO = [Seeker(random.randrange(WN_WIDTH), random.randrange(WN_HEIGHT), CIANO, ESCALA, 2, reproduzir(avaliacao[0][0].cerebro, avaliacao[random.randint(0,3)][0].cerebro), SEEKERS) for i in range (POP_INICIAL_SEEKER)]


    

# Finalização do Pygame
pygame.quit()
sys.exit()



