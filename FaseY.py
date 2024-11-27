import pygame
from pygame.locals import *
import sys

def portas_logicas():
    pygame.init()
    
    # Configurações da janela
    largura, altura = 800, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Desafio das Portas Lógicas")
    
    # Cores
    preto = (0, 0, 0)
    azul = (0, 0, 255)
    branco = (255, 255, 255)
    
    # Fonte
    fonte = pygame.font.Font(None, 36)
    fonte_botao = pygame.font.Font(None, 28)
    
    # Imagem de fundo
    fundo = pygame.image.load("fundoTelaInicial.jpg")
    
    # Imagens dos interruptores, lâmpada e portas lógicas
    img_interruptor_off = pygame.image.load("interruptor_off.jpg")
    img_interruptor_on = pygame.image.load("interruptor_on.jpg")
    img_lampada_off = pygame.image.load("lampada_off.png")
    img_lampada_on = pygame.image.load("lampada_on.png")
    img_porta_xor = pygame.image.load("porta_xor.jpg")
    img_porta_and = pygame.image.load("porta_and.jpg")
    
    # Redimensionar imagens
    img_interruptor_off = pygame.transform.scale(img_interruptor_off, (80, 80))
    img_interruptor_on = pygame.transform.scale(img_interruptor_on, (80, 80))
    img_lampada_off = pygame.transform.scale(img_lampada_off, (90, 90))
    img_lampada_on = pygame.transform.scale(img_lampada_on, (90, 90))
    img_porta_xor = pygame.transform.scale(img_porta_xor, (200, 100))
    img_porta_and = pygame.transform.scale(img_porta_and, (200, 100))
    
    # Desafio e resposta
    desafio_texto = "Resolva o desafio lógico para acender a lâmpada!"
    solucao = [0, 1, 0, 0, 1]  # Sequência de ativação
    
    # Estados dos interruptores
    interruptores = [0, 0, 0, 0, 0]
    
    # Posições
    interruptor_posicoes = [(100, 100), (100, 200), (100, 300), (100, 400), (100, 500)]
    porta_xor_posicoes = [(300, 150), (300, 300), (300, 450)]
    porta_and_posicoes = [(500, 200), (500, 400)]
    lampada_posicao = (700, 270)
    botao_posicao = (300, 500)
    botao_tamanho = (200, 50)
    
    # Função de simulação das portas lógicas
    def calcular_saida():
        # Primeira camada (XOR)
        saidas_xor = []
        for i in range(3):
            entradas = interruptores[i:i+2]
            saidas_xor.append(1 if sum(entradas) % 2 == 1 else 0)
        
        # Segunda camada (AND)
        saidas_and = []
        for i in range(2):
            entradas = saidas_xor[i:i+2]
            saidas_and.append(1 if all(entradas) else 0)
        
        # Saída final ligada à lâmpada
        return all(saidas_and)
    
    # Função para desenhar o botão
    def desenhar_botao():
        pygame.draw.rect(tela, azul, (*botao_posicao, *botao_tamanho), border_radius=10)
        texto = fonte_botao.render("Próxima Fase", True, preto)
        texto_rect = texto.get_rect(center=(botao_posicao[0] + botao_tamanho[0] // 2, botao_posicao[1] + botao_tamanho[1] // 2))
        tela.blit(texto, texto_rect)
    
    # Loop principal
    rodando = True
    lampada_estado = False
    
    while rodando:
        tela.blit(fundo, (0, 0))
        
        # Exibir desafio
        texto = fonte.render(desafio_texto, True, preto)
        tela.blit(texto, (80, 20))
        
        # Exibir interruptores
        for i, pos in enumerate(interruptor_posicoes):
            if interruptores[i] == 1:
                tela.blit(img_interruptor_on, pos)
            else:
                tela.blit(img_interruptor_off, pos)
        
        '''# Desenhar conexões
        for i, xor_pos in enumerate(porta_xor_posicoes):
            pygame.draw.line(tela, preto, interruptor_posicoes[i], xor_pos, 2)
            if i + 1 < len(interruptor_posicoes):
                pygame.draw.line(tela, preto, interruptor_posicoes[i + 1], xor_pos, 2)
        
        for i, and_pos in enumerate(porta_and_posicoes):
            pygame.draw.line(tela, preto, porta_xor_posicoes[i], and_pos, 2)
            if i + 1 < len(porta_xor_posicoes):
                pygame.draw.line(tela, preto, porta_xor_posicoes[i + 1], and_pos, 2)
        
        pygame.draw.line(tela, preto, porta_and_posicoes[1], lampada_posicao, 2)'''
        
        # Exibir portas lógicas (primeira camada - XOR)
        for pos in porta_xor_posicoes:
            tela.blit(img_porta_xor, pos)
        
        # Exibir portas lógicas (segunda camada - AND)
        for pos in porta_and_posicoes:
            tela.blit(img_porta_and, pos)
        
        # Exibir lâmpada
        if lampada_estado:
            tela.blit(img_lampada_on, lampada_posicao)
        else:
            tela.blit(img_lampada_off, lampada_posicao)
        
        # Exibir botão se a lâmpada estiver acesa
        if lampada_estado:
            desenhar_botao()
        
        # Verificar eventos
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == MOUSEBUTTONDOWN:
                x, y = evento.pos
                # Verificar clique nos interruptores
                for i, pos in enumerate(interruptor_posicoes):
                    rect = img_interruptor_off.get_rect(topleft=pos)
                    if rect.collidepoint(x, y):
                        interruptores[i] = 1 - interruptores[i]
                # Verificar clique no botão
                if lampada_estado:
                    botao_rect = pygame.Rect(*botao_posicao, *botao_tamanho)
                    if botao_rect.collidepoint(x, y):
                        print("Próxima fase!")  # Aqui pode ser chamada a próxima fase do jogo
        
        # Atualizar estado da lâmpada
        lampada_estado = calcular_saida()
        
        pygame.display.flip()
