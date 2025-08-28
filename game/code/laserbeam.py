import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Pontos dos pilares (onde o laser começa e termina), subistituir depois por pontos aleatóris, ou pré-definidos no mapa
pontoA = (250, 300)
pontoB = (600, 400)

# Cor do laser
laser_color = (255, 0, 0)

def draw_laser(surface, start, end, width=8):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)

    # cria retângulo horizontal do tamanho da distância
    laser_surf = pygame.Surface((length, width), pygame.SRCALPHA)
    pygame.draw.rect(laser_surf, laser_color, (0, 0, length, width))

    # calcula ângulo
    angle = math.degrees(math.atan2(-dy, dx))

    # rotaciona
    laser_rot = pygame.transform.rotate(laser_surf, angle)

    # agora o centro do laser fica no meio do segmento AB
    mid_point = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
    rect = laser_rot.get_rect(center=mid_point)

    surface.blit(laser_rot, rect)


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    # desenha pilares
    pygame.draw.circle(screen, (0, 200, 200), pontoA, 15)
    pygame.draw.circle(screen, (0, 200, 200), pontoB, 15)

    # desenha o laser
    draw_laser(screen, pontoA, pontoB, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
