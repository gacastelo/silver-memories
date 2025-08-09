from settings import *

class BossBase(pygame.sprite.Sprite):


    def __init__(self, pos, groups, player, spawn_points, name="Boss", health=1000, speed=50):
        super().__init__(groups)
        # carrega imagem original
        original_image = pygame.image.load(join('images', 'bosses', 'guardiao.png')).convert_alpha()
    
        # redimensiona para 150x150
        self.image = pygame.transform.smoothscale(original_image, (150, 150))

        # define posição
        self.rect = self.image.get_rect(center=pos)

        self.name = name
        self.health = health
        self.max_health = health
        self.speed = speed
        self.player = player

        self.phase = 1  # Começa na fase 1

        #Boss Fight features

        self.spawn_points = spawn_points  # lista de posições possíveis para teleporte

        # Controle de teleporte
        self.teleport_cooldown = 1000  # ms
        self.last_teleport = pygame.time.get_ticks()

        # Efeito de desaparecimento
        self.visible = True
        self.fade_time = 20  # tempo invisível antes de reaparecer

    def teleport(self):
        """Teleporta para um ponto aleatório do mapa"""
        self.visible = False  # fica invisível por um instante
        pygame.time.set_timer(pygame.USEREVENT + 1, self.fade_time, loops=1)  # evento para reaparecer
        print(f"[DEBUG] Teleportando... posição antiga: {self.rect.center}")
        new_pos = random.choice(self.spawn_points)
        self.rect.center = new_pos
        print(f"[DEBUG] Nova posição: {self.rect.center}")

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

        # Controle de fases
        self.update_phase()

    def update_phase(self):
        """Altera comportamento conforme a vida restante"""
        health_percent = self.health / self.max_health
        if health_percent <= 0.3:
            self.phase = 3
        elif health_percent <= 0.6:
            self.phase = 2
        else:
            self.phase = 1

    def die(self):
        print(f"{self.name} foi derrotado!")
        self.kill()

    def attack(self):
        """Ataque padrão (pode ser sobrescrito)"""
        print(f"{self.name} atacou!")

    def special_attack(self):
        """Ataque especial (deve ser sobrescrito pelo boss específico)"""
        pass
    
    def draw(self, surface, offset=(0, 0)):
        if self.visible:
            pos = (self.rect.left + offset[0], self.rect.top + offset[1])
            surface.blit(self.image, pos)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.visible = True

    def update(self, dt):
        #print(f"[DEBUG] Boss update called, dt={dt}, pos={self.rect.center}, health={self.health}")
        now = pygame.time.get_ticks()

        # Teste: ataque sempre que estiver perto
        if self.rect.colliderect(self.player.rect):
            self.attack()

        # Verifica se é hora de teleportar
        if now - self.last_teleport >= self.teleport_cooldown:
            self.teleport()
            self.last_teleport = now

    def draw_health_bar(self, surface):
        """Desenha barra de vida do boss no topo da tela"""
        bar_width = 400
        bar_height = 20
        bar_x = (surface.get_width() - bar_width) // 2
        bar_y = 20

        # Fundo da barra
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        # Vida
        fill_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(surface, (200, 0, 0), (bar_x, bar_y, fill_width, bar_height))

        # Nome do boss
        font = pygame.font.Font(None, 30)
        text = font.render(self.name, True, (255, 255, 255))
        surface.blit(text, (bar_x, bar_y - 25))

class GuardiaoAstra(BossBase):
    def __init__(self, pos, groups, player, spawn_points):
        super().__init__(pos, groups, player, spawn_points, name="Guardião de Astra", health=1200, speed=40)

    def special_attack(self):
        if self.phase == 2:
            print("Guardião invoca vinhas para prender o jogador!")
        elif self.phase == 3:
            print("Guardião libera lodo tóxico que reduz velocidade!")
