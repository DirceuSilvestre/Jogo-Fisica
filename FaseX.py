import pygame
import random

def fase_bolas():
    pygame.init()

    # Configurações da tela
    LARGURA, ALTURA = 800, 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Fase das Bolas")

    # Cores
    AZUL = (0, 122, 255)
    VERMELHO = (255, 0, 0)
    PRETO = (0, 0, 0)
    BRANCO = (255, 255, 255)

    # Configurações das bolas
    NUM_BOLAS = 120
    TAMANHO_INICIAL = 36
    VELOCIDADE_REPULSAO_BASE = 20

    # Carregar imagens de fundo
    fundo1 = pygame.image.load("fundoTelaInicial.jpg")  # Troque pelo nome da primeira imagem
    fundo2 = pygame.image.load("fundoTelaInicial.jpg")  # Troque pelo nome da segunda imagem

    # Inicializar bolas
    bolas = []
    for _ in range(NUM_BOLAS):
        x = random.randint(TAMANHO_INICIAL, LARGURA - TAMANHO_INICIAL)
        y = random.randint(TAMANHO_INICIAL, ALTURA - TAMANHO_INICIAL)
        cor = AZUL if random.random() < 0.5 else VERMELHO
        bolas.append({"x": x, "y": y, "cor": cor, "tamanho": TAMANHO_INICIAL, "ativo": True})

    # Função para desenhar botão
    def desenhar_botao(tela, texto, pos, cor_botao, cor_texto):
        fonte = pygame.font.Font(None, 36)
        texto_render = fonte.render(texto, True, cor_texto)
        texto_rect = texto_render.get_rect(center=pos)

        pygame.draw.rect(tela, cor_botao, texto_rect.inflate(20, 20), border_radius=10)
        tela.blit(texto_render, texto_rect)

        return texto_rect.inflate(20, 20)

    # Função para checar se todas as condições estão concluídas
    def checar_conclusao(bolas, cor_atual):
        for bola in bolas:
            if bola["ativo"]:
                if bola["cor"] != cor_atual:
                    return False
        return True

    # Loop principal
    rodando = True
    arrastando = None
    cor_atual = None
    velocidade_repulsao = VELOCIDADE_REPULSAO_BASE
    objetivo_concluido = False
    botao_proxima_fase = None

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clique esquerdo
                    for bola in bolas:
                        distancia = ((bola["x"] - evento.pos[0]) ** 2 + (bola["y"] - evento.pos[1]) ** 2) ** 0.5
                        if bola["ativo"] and distancia < bola["tamanho"]:
                            arrastando = bola
                            cor_atual = bola["cor"]
                            break

                    # Clique no botão após o objetivo concluído
                    if botao_proxima_fase and botao_proxima_fase.collidepoint(evento.pos):
                        print("Indo para a próxima fase!")
                        rodando = False

            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    arrastando = None

            if evento.type == pygame.MOUSEMOTION and arrastando:
                arrastando["x"], arrastando["y"] = evento.pos

        # Atualizar a tela
        tela.blit(fundo2 if objetivo_concluido else fundo1, (0, 0))

        # Atualizar e desenhar bolas
        for bola in bolas:
            if bola["ativo"]:
                if arrastando and bola != arrastando:
                    dx = bola["x"] - arrastando["x"]
                    dy = bola["y"] - arrastando["y"]
                    distancia = (dx ** 2 + dy ** 2) ** 0.5

                    if bola["cor"] == cor_atual and distancia < bola["tamanho"] + arrastando["tamanho"]:
                        # Aumentar tamanho da bola arrastada
                        arrastando["tamanho"] += 2
                        bola["ativo"] = False  # Desativar a bola após colidir
                        # Aumentar velocidade de repulsão
                        velocidade_repulsao += 2

                    elif bola["cor"] != cor_atual and distancia < bola["tamanho"] + arrastando["tamanho"]:
                        # Repelir bola de cor diferente
                        bola["x"] += velocidade_repulsao * dx / distancia
                        bola["y"] += velocidade_repulsao * dy / distancia

                        # Desativar se sair da tela
                        if (
                            bola["x"] < 0
                            or bola["x"] > LARGURA
                            or bola["y"] < 0
                            or bola["y"] > ALTURA
                        ):
                            bola["ativo"] = False

                # Desenhar bola
                pygame.draw.circle(tela, bola["cor"], (int(bola["x"]), int(bola["y"])), bola["tamanho"])

        # Checar conclusão
        if not objetivo_concluido and checar_conclusao(bolas, cor_atual):
            objetivo_concluido = True

        if objetivo_concluido:
            fonte = pygame.font.Font(None, 48)
            texto = fonte.render("Objetivo Concluído", True, PRETO)
            texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2))
            tela.blit(texto, texto_rect)

            botao_proxima_fase = desenhar_botao(
                tela, "Próxima Fase", (LARGURA // 2, ALTURA // 2 + 50), AZUL, PRETO
            )

        pygame.display.flip()

    pygame.quit()
