import pygame
import sys
from Creditos import creditos # Importa a função de outro arquivo
from faseImas import fase_imas
from faseTransistores import transistors_stage
from FasePortas import portas_logicas

# Inicializa o pygame
pygame.init()

# Configurações da janela
LARGURA = 800
ALTURA = 600
TITULO = "StaticRoom"
COR_AZUL = (0, 122, 255)
COR_PRETO = (0, 0, 0)
COR_BRANCA = (255, 255, 255)

# Criação da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

# Carregando a imagem de fundo
fundo = pygame.image.load("fundoTelaInicial.jpg")  # Imagem no mesmo diretório.

# Função para desenhar botões
def desenhar_botao(tela, texto, pos, cor_botao, cor_texto):
    fonte = pygame.font.Font(None, 36)
    texto_render = fonte.render(texto, True, cor_texto)
    texto_rect = texto_render.get_rect(center=pos)

    # Desenha o botão arredondado
    pygame.draw.rect(tela, cor_botao, texto_rect.inflate(20, 20), border_radius=30)
    tela.blit(texto_render, texto_rect)

    return texto_rect.inflate(20, 20)  # Retorna o retângulo do botão (para clique)

def desenhar_titulo(tela, texto, pos, cor_texto):
    """
    Função para desenhar um título em letras maiúsculas e negrito no Pygame.

    Args:
        tela (pygame.Surface): A superfície onde o texto será desenhado.
        texto (str): O texto a ser exibido.
        posicao (tuple): Uma tupla com as coordenadas (x, y) para posicionar o texto.
        cor (tuple): A cor do texto em formato RGB.
    """
    # Fonte com tamanho maior e em negrito
    fonte = pygame.font.Font(None, 72)  # Tamanho grande para o título
    texto_renderizado = fonte.render(texto, True, cor_texto)
    texto_rect = texto_renderizado.get_rect(center=pos)
    tela.blit(texto_renderizado, texto_rect)

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Clique esquerdo do mouse
            pos_mouse = evento.pos

            # Verifica se clicou no botão "Iniciar"
            if botao_iniciar.collidepoint(pos_mouse):
                fase_imas()  # Chama a função Fase1 do arquivo externo

            # Verifica se clicou no botão "Créditos"
            if botao_creditos.collidepoint(pos_mouse):
                creditos()  # Mensagem de exemplo

    # Desenhando o fundo
    tela.blit(fundo, (-100, -100))

    # Desenhando o título
    desenhar_titulo(tela, "STATIC ROOM", (LARGURA // 2, ALTURA - ((ALTURA // 4) * 3)), COR_AZUL)

    # Desenhando os botões
    botao_iniciar = desenhar_botao(tela, "Iniciar", (LARGURA // 2, ALTURA // 1.7 - 75), COR_AZUL, COR_PRETO)
    botao_creditos = desenhar_botao(tela, "Créditos", (LARGURA // 2, ALTURA // 1.7 + 75), COR_AZUL, COR_PRETO)
    

    # Atualizando a tela
    pygame.display.flip()

# Fecha o pygame
pygame.quit()
sys.exit()