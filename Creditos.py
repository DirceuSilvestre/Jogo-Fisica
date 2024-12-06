import pygame
import random

def creditos():
    pygame.init()

    # Configurações da tela
    LARGURA, ALTURA = 800, 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Fase das Bolas")

    # Carregar imagens de fundo
    fundo = pygame.image.load("fundoTelaInicial.jpg")  # Troque pelo nome da primeira imagem

        
    mensagem = "Programadores:\n\nWalter Monteiro & Dirceu Silvestre\n\nObrigado por jogar, espero que se divirta e aprenda!"
    linhas_mensagem = mensagem.split("\n")

    fonte_texto = pygame.font.Font(None, 40)

    # Loop principal
    rodando = True

    while rodando:

        # Atualizar a tela
        tela.blit(fundo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Desenhar mensagem centralizada
        y_texto = ALTURA // 3
        for linha in linhas_mensagem:
            texto = fonte_texto.render(linha, True, (0, 0, 0))
            x_texto = (LARGURA - texto.get_width()) // 2
            tela.blit(texto, (x_texto, y_texto))
            y_texto += texto.get_height() + 10

        pygame.display.flip()

    pygame.quit()
