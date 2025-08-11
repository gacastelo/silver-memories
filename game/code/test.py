import pygame

# Inicializa o pygame
pygame.init()

# Cria a tela
screen = pygame.display.set_mode((400, 400))

# Define as cores
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define o retângulo vermelho
red_rect = pygame.Rect(100, 100, 100, 150)

# Margens ao redor do vermelho
left_margin = 20
top_margin = 10
right_margin = 10
bottom_margin = 10

# Calcula o retângulo verde com base no vermelho + margens
green_rect = pygame.Rect(
    red_rect.left + left_margin,
    red_rect.top - top_margin,
    red_rect.width + left_margin + right_margin,
    red_rect.height + top_margin + bottom_margin
)

# Loop principal
running = True
while running:
    screen.fill((255, 255, 255))  # fundo branco

    # Desenha os retângulos
    pygame.draw.rect(screen, RED, red_rect, 1)
    pygame.draw.rect(screen, GREEN, green_rect, 1)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
