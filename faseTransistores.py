import pygame
import sys
from FasePortas import portas_logicas

#cores
COR_AZUL = (0, 122, 255)
COR_PRETO = (0, 0, 0)
COR_BRANCA = (255, 255, 255)
COR_AZUL_CLARO = (173, 216, 230)
COR_CINZA = (200, 200, 200)
COR_AMARELO = (255, 255, 0)
COR_VERDE = (0, 255, 0)

# Função da fase 1
def transistors_stage():

    pygame.init()

    #configurações de tela
    LARGURA, ALTURA = 800, 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Fase dos Transistores")
    font_info = pygame.font.Font(None, 36)
    fundo = pygame.image.load("fundoTelaInicial.jpg")

    #variáveis da fase 1
    lamp_charge = 99  # Carga necessária para ligar a lâmpada
    player_charge = 0
    transistor_positions = [
        {"capacitance": 3, "rect": pygame.Rect(50, 500, 100, 50)},
        {"capacitance": 6, "rect": pygame.Rect(200, 500, 100, 50)},
        {"capacitance": 9, "rect": pygame.Rect(350, 500, 100, 50)}
        ]
    selected_transistors1 = []
    selected_transistors2 = []
    dragging = None

    running = True
    while running:
        tela.blit(fundo, (0, 0))
        draw_circuit(tela, font_info, player_charge, lamp_charge)
        draw_transistors(tela, font_info, transistor_positions, selected_transistors1, selected_transistors2)

        # Mostra a voltagem escolhida
        text_voltage = font_info.render(f"Carga do circuito: {player_charge}C", True, COR_PRETO)
        tela.blit(text_voltage, (300, 50))

        # Desenha o botão "Próximo" se o jogador acertou
        if check_solution(player_charge, lamp_charge, selected_transistors1, selected_transistors2):
            draw_next_button(tela, font_info)

        # Eventos
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Clique para iniciar o arraste
            if event.type == pygame.MOUSEBUTTONDOWN:
                for t in transistor_positions:
                    if t["rect"].collidepoint(event.pos):
                        dragging = t
                        break

            # Soltar para soltar o transistor
            if event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    clippedrect1 = dragging["rect"].clipline(144, 297, 606, 303) #cria um retângulo cortado pela linha de cima
                    clippedrect2 = dragging["rect"].clipline(44, 497, 606, 503) #cria um retângulo cortado pela linha de baixo
                    # Se o transistor for solto no local correto, adicione à lista
                    if clippedrect1:
                        if dragging not in selected_transistors1:
                            selected_transistors1.append(dragging)
                    elif clippedrect2:
                        if dragging not in selected_transistors2:
                            selected_transistors2.append(dragging)
                    else:
                        # Remove o transistor se for movido para fora
                        if dragging in selected_transistors1:
                            selected_transistors1.remove(dragging)
                        elif dragging in selected_transistors2:
                            selected_transistors2.remove(dragging)

                    player_charge = player_charge_function(selected_transistors1, selected_transistors2)
                    dragging = None
                    clippedrect1 = None
                    clippedrect2 = None

            # Clique no botão "Próximo"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_solution(player_charge, lamp_charge, selected_transistors1, selected_transistors2) and 650 < mouse[0] < 770 and 500 < mouse[1] < 550:
                    portas_logicas()
                    running = False

        # Arraste do transistor
        if dragging:
            dragging["rect"].center = mouse

        pygame.display.flip()

# Função para desenhar o circuito
def draw_circuit(tela,font_info,player_charge, lamp_charge):

    # Fundo azul claro
    tela.fill(COR_AZUL_CLARO)

    # Bateria
    pygame.draw.rect(tela, COR_CINZA, (50, 250, 100, 100))
    text_battery = font_info.render("Bateria: 9V", True, COR_PRETO)
    tela.blit(text_battery, (60, 220))

    # Lâmpada (dinâmica)
    lamp_color = COR_AMARELO if player_charge == lamp_charge else COR_CINZA
    pygame.draw.circle(tela, lamp_color, (700, 300), 50)
    text_lamp = font_info.render("Lâmpada: 99C", True, COR_PRETO)
    tela.blit(text_lamp, (620, 370))

    # Conexões do circuito (linhas)
    pygame.draw.line(tela, COR_PRETO, (150, 300), (600, 300), 5)  # Linha horizontal principal
    pygame.draw.line(tela, COR_PRETO, (600, 300), (600, 500), 5)  # Linha vertical para transistores
    pygame.draw.line(tela, COR_PRETO, (600, 500), (50, 500), 5)   # Linha horizontal inferior
    pygame.draw.line(tela, COR_PRETO, (50, 500), (50, 300), 5)    # Linha vertical da bateria

# Função para desenhar os transistores
def draw_transistors(tela, font_info, transistor_positions, selected_transistors1, selected_transistors2):
    for t in transistor_positions:
        color = COR_VERDE if (t in selected_transistors1) or (t in selected_transistors2) else COR_CINZA
        pygame.draw.rect(tela, color, t["rect"])
        text = font_info.render(f"{t['capacitance']}F", True, COR_PRETO)
        tela.blit(text, (t["rect"].x + 20, t["rect"].y + 10))

# Função para verificar se o jogador acertou
def check_solution(player_charge, lamp_charge, selected_transistors1, selected_transistors2):
    player_charge = player_charge_function(selected_transistors1, selected_transistors2)
    return player_charge == lamp_charge

# Função para desenhar o botão de próxima fase
def draw_next_button(tela, font_info):
    pygame.draw.rect(tela, COR_PRETO, (650, 500, 120, 50))
    text_next = font_info.render("Próximo", True, COR_BRANCA)
    tela.blit(text_next, (660, 510))

def player_charge_function(selected_transistors1, selected_transistors2):
    carga_transistor_1 = 0.00
    carga_transistor_2 = 0.00

    if len(selected_transistors1) > 0:
        for c in selected_transistors1:
            carga_transistor_1 = carga_transistor_1 + (1.00/float(c["capacitance"]))

        carga_transistor_1 = carga_transistor_1 ** (-1)
        carga_transistor_1 = carga_transistor_1 * 9.00

    if len(selected_transistors2) > 0:
        for c in selected_transistors2:
            carga_transistor_2 = carga_transistor_2 + (1.00/float(c["capacitance"]))
        carga_transistor_2 = carga_transistor_2 ** (-1)
        carga_transistor_2 = carga_transistor_2 * 9.00

    return carga_transistor_1 + carga_transistor_2
