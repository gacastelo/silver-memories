import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --------------------
# Classes
# --------------------
class VinhaShadow(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos, groups, delay=400):
        super().__init__(groups)
        self.start_pos = pygame.Vector2(start_pos)
        self.end_pos = pygame.Vector2(end_pos)
        self.groups_ = groups
        self.delay = delay

        # Linha amarela de aviso
        self.image = pygame.Surface((1, 4))
        self.image.fill((255, 255, 0))
        self.image = pygame.transform.scale(self.image, (int(self.start_pos.distance_to(self.end_pos)), 4))

        angle = math.degrees(math.atan2(-(self.end_pos.y - self.start_pos.y), self.end_pos.x - self.start_pos.x))
        self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect(center=(self.start_pos + self.end_pos) / 2)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt):
        now = pygame.time.get_ticks()
        if now - self.spawn_time >= self.delay:
            Vinha(self.start_pos, self.end_pos, self.groups_)
            self.kill()


class Vinha(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos, groups, growth_speed=300, damage=40):
        super().__init__(groups)
        self.start_pos = pygame.Vector2(start_pos)
        self.end_pos = pygame.Vector2(end_pos)
        self.current_length = 0
        self.full_length = self.start_pos.distance_to(self.end_pos)
        self.growth_speed = growth_speed
        self.damage = damage

        # Ângulo
        dx = self.end_pos.x - self.start_pos.x
        dy = self.end_pos.y - self.start_pos.y
        self.angle = math.degrees(math.atan2(-dy, dx))

        # Base verde
        self.base_image = pygame.Surface((1, 12))
        self.base_image.fill((0, 150, 0))

        self.image = self.base_image
        self.rect = self.image.get_rect(center=self.start_pos)

    def update(self, dt):
        self.current_length += self.growth_speed * dt
        if self.current_length > self.full_length:
            self.current_length = self.full_length

        # Estica e rotaciona
        self.image = pygame.transform.scale(self.base_image, (int(self.current_length), 12))
        self.image = pygame.transform.rotate(self.image, self.angle)

        # Centraliza
        direction = (self.end_pos - self.start_pos).normalize()
        center_pos = self.start_pos + direction * (self.current_length / 2)
        self.rect = self.image.get_rect(center=center_pos)


# --------------------
# Setup
# --------------------
all_sprites = pygame.sprite.Group()

def spawn_vinha():
    start_pos = (random.randint(100, 700), random.randint(100, 500))
    end_pos = (random.randint(100, 700), random.randint(100, 500))
    VinhaShadow(start_pos, end_pos, all_sprites)

# --------------------
# Loop principal
# --------------------
running = True
spawn_timer = 0
while running:
    dt = clock.tick(60) / 1000  # delta time em segundos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn a cada 1 segundo
    spawn_timer += dt
    if spawn_timer >= 1:
        spawn_timer = 0
        spawn_vinha()

    all_sprites.update(dt)

    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
