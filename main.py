import pygame
import random
import sys
import math
import numpy as np
from snake import Snake

# Inicializa o pygame
pygame.init()

# Configurações da tela
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake - Direções N, S, L, O")

# Cores
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# Fonte
fonte = pygame.font.SysFont("Arial", 24)

# Configurações da cobra
tamanho_celula = 20

def desenhar_cobra(cobra):
    for segmento in cobra.positions:
        pygame.draw.rect(tela, VERDE, (segmento[0], segmento[1], tamanho_celula, tamanho_celula))

def desenhar_comida(comida):
    pygame.draw.rect(tela, VERMELHO, (comida[0], comida[1], tamanho_celula, tamanho_celula))

def mover_cobra(cobra, direcao):
    x, y = cobra.positions[0]
    if direcao == "N":
        nova_cabeca = (x, y - tamanho_celula)
    elif direcao == "S":
        nova_cabeca = (x, y + tamanho_celula)
    elif direcao == "L":
        nova_cabeca = (x + tamanho_celula, y)
    elif direcao == "O":
        nova_cabeca = (x - tamanho_celula, y)

    return nova_cabeca

def verificar_colisao(cobra):
    copia = cobra.positions.copy()
    cabeca = copia.popleft()

    x, y = cobra.positions[0]
    if x < 0 or x >= largura or y < 0 or y >= altura:
        return True
    if cabeca in copia:
        return True
    return False

def coletar_recompensas(cobra, fruta, direcao_atual, tamanho_celula):
    analizar_cobra = cobra.positions.copy()
    cabeca = analizar_cobra[0]
    analizar_cobra.popleft()
    
    print(fruta, cabeca)
    dist = math.dist(fruta, cabeca)
    existem_obstaculos = 0
    n_obstaculos = 0
    colisao_iminente = 0

    for posicao in analizar_cobra:
        if (direcao_atual == 'N' or direcao_atual == 'S') and posicao[0] == cabeca[0]:
            existem_obstaculos = 1
            n_obstaculos += 1

            if posicao[1] - tamanho_celula == cabeca[1]:
                colisao_iminente = 1

        elif (direcao_atual == 'L' or direcao_atual == 'O') and posicao[1] == cabeca[1]: 
            existem_obstaculos = 1
            n_obstaculos += 1

            if posicao[0] - tamanho_celula == cabeca[0]:
                colisao_iminente = 1

    return dist, existem_obstaculos, n_obstaculos, colisao_iminente

def direcao_reversa(direcao):
    if direcao == 'L':
        return ['S', 'N', 'L']

    if direcao == 'O':
        return ['N', 'S', 'O']

    if direcao == 'S':
        return ['S', 'O', 'L']

    if direcao == 'N':
        return ['N', 'L', 'O']      
    

def mostrar_pontuacao(pontos):
    texto = fonte.render(f"Pontuação: {pontos}", True, BRANCO)
    tela.blit(texto, (10, 10))

def jogo():
    cobra = Snake((100, 100), (80, 100), (60, 100))
    direcao = "L"
    cobra.brain.direcoes.remove("O")
    comida = (random.randrange(0, largura, tamanho_celula),
              random.randrange(0, altura, tamanho_celula))
    
    anterior = np.ones((4,))
    pontos = 0
    clock = pygame.time.Clock()
    ai_mode = True

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_TAB:
                    ai_mode = not ai_mode
                
                if not ai_mode:
                    direcao = atualizar_direcao(evento.key, direcao)

        if ai_mode:   
            cobra.brain.direcoes = direcao_reversa(direcao)
            recompensas = coletar_recompensas(cobra=cobra, fruta=comida, direcao_atual=direcao, tamanho_celula=tamanho_celula)
            direcao_nova, anterior = cobra.proxima_direcao(recompensas, np.array(anterior))
            anterior = (recompensas[0], *anterior[0])
            direcao = direcao_nova
            

        if list(cobra.positions)[0] == comida:
            pontos += 1
            comida = (random.randrange(0, largura, tamanho_celula),
                      random.randrange(0, altura, tamanho_celula))
            
            cobra.forward(mover_cobra(cobra, direcao), True)

        else:
            cobra.forward(mover_cobra(cobra, direcao))

        if verificar_colisao(cobra):
            return pontos  # retorna pontuação final para reinício

        tela.fill(PRETO)
        desenhar_cobra(cobra)
        desenhar_comida(comida)
        mostrar_pontuacao(pontos)
        pygame.display.update()
        clock.tick(10)

def main():
    while True:
        pontos = jogo()
        tela.fill(PRETO)
        texto_gameover = fonte.render(f"Game Over! Pontuação: {pontos}", True, BRANCO)
        texto_restart = fonte.render("Pressione ESPAÇO para reiniciar ou ESC para sair", True, BRANCO)
        tela.blit(texto_gameover, (largura//2 - 150, altura//2 - 30))
        tela.blit(texto_restart, (largura//2 - 200, altura//2 + 10))
        pygame.display.update()

        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        esperando = False  # reinicia
                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

main()
