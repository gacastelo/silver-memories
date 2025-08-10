from settings import *
from sprites import *

class BossBase(pygame.sprite.Sprite):


    def __init__(self, pos, groups, player, spawn_points, name="Boss", health=1000, speed=50):
        super().__init__(groups)
        # atributos do boss
        self.name = name
        self.health = health
        self.max_health = health
        self.speed = speed
        self.player = player
        self.file_name = remove_accents(self.name.lower()).replace(" ", "_") 

        self.load_images()  # Carrega as imagens do boss depois de tudo carregado
        self.state = 'down_idle'
        self.frame_index = 0
        self.previous_state = self.state
        self.animation_speed = 6  # frames por segundo

        # carrega imagem original
        original_image = pygame.image.load(join('images', 'bosses', f'{self.file_name}', 'state_null.png')).convert_alpha()

        # redimensiona para 128x128
        self.image = pygame.transform.smoothscale(original_image, (128, 128))

        # define posição
        self.rect = self.image.get_rect(center=pos)

        # colisão
        self.collision_rect = self.rect.inflate(-20, -20)
        self.collision_sprite = BossCollisionSprite(self)
        self.true_state = 'down'
        self.weakspot = Weakspot(self, groups, self.true_state)


        #Boss Fight features
        self.phase = 1  # Começa na fase 1
        self.spawn_points = spawn_points  # lista de posições possíveis para teleporte

        # Controle de teleporte
        self.teleport_cooldown = 5000  # ms
        self.last_teleport = pygame.time.get_ticks()

        # Efeito de desaparecimento
        self.visible = True
        self.fade_time = 20  # tempo invisível antes de reaparecer

    #Combate methods
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, amount, is_weak=False):
        if is_weak:
            amount *= 2  # dano dobrado no ponto fraco
        self.health -= amount
        print(f"Boss HP: {self.health}")

    def is_player_behind(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        if self.true_state == "right":
            return dx < 0  # player está à esquerda
        elif self.true_state == "left":
            return dx > 0  # player está à direita
        elif self.true_state == "up":
            return dy > 0  # player está abaixo
        elif self.true_state == "down":
            return dy < 0  # player está acima


    def choose_state(self):
        estados_movendo = ['left', 'right', 'up', 'down']
        estados_idle = [f"{estado}_idle" for estado in estados_movendo]
        if not self.visible:
            return random.choice(estados_idle)
        else:
            return random.choice(estados_movendo)

    def get_state(self):
        self.state = self.choose_state()
        self.true_state = self.state.replace('_idle', '')  # remove idle para lógica de movimento
        print(f"[DEBUG] Novo estado escolhido: {self.state}")

    def animate(self, dt):
        frames = self.frames[self.state]
        if frames:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(frames):
                self.frame_index = 0
            self.image = frames[int(self.frame_index)]

    def collide_with_player(self):
        """Verifica colisão com o jogador"""
        print(f"[DEBUG] Verificando colisão com o jogador: {self.collision_rect.colliderect(self.player.hitbox_rect)}")

    def teleport(self):
        """Teleporta para um ponto aleatório do mapa"""
        self.visible = False  # fica invisível por um instante
        self.get_state()
        pygame.time.set_timer(pygame.USEREVENT + 1, self.fade_time, loops=1)  # evento para reaparecer
        print(f"[DEBUG] Teleportando... posição antiga: {self.rect.center}")
        new_pos = random.choice(self.spawn_points)
        self.rect.center = new_pos
        self.collision_rect.center = new_pos  # atualiza a colisão
        print(f"[DEBUG] Nova posição: {self.rect.center}")

    def load_images(self):
        # Adiciona os estados com idle igual ao player
        self.frames = {
            'left': [], 'right': [], 'up': [], 'down': [],
            'left_idle': [], 'right_idle': [], 'up_idle': [], 'down_idle': []
        }

        for state in self.frames.keys():
            path = join('images', 'bosses', self.file_name, state)
            try:
                self.frames[state] = [
                    pygame.image.load(join(path, file_name)).convert_alpha()
                    for _, _, file_names in walk(path)
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0]))
                ]
            except FileNotFoundError:
                # fallback: usa o primeiro frame da versão sem idle
                if '_idle' in state:
                    base_state = state.replace('_idle', '')
                    if self.frames[base_state]:
                        self.frames[state] = [self.frames[base_state][0]]



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
        #print(f"{self.name} atacou!")
        pass

    def special_attack(self):
        """Ataque especial (deve ser sobrescrito pelo boss específico)"""
        pass
    
    def draw(self, surface, offset=(0, 0)):
        dt = pygame.time.get_ticks() / 1000  # tempo em segundos
        moving = self.state not in ['left_idle', 'right_idle', 'up_idle', 'down_idle']
        if self.visible:
            pos = (self.rect.left + offset[0], self.rect.top + offset[1])
            surface.blit(self.image, pos)
            if moving:
                    self.frame_index += (self.speed/50) * dt
                    current_frames = self.frames[self.state]
                    if current_frames:
                        self.image = current_frames[int(self.frame_index) % len(current_frames)]
            else:
                self.frame_index = 0
                idle_state = self.state.split('_')[0] + '_idle'
                if idle_state in self.frames and self.frames[idle_state]:
                    self.image = self.frames[idle_state][0]
                else:
                    self.image = self.frames[self.state.replace('_idle', '')][0]


        self.debug_draw(surface, offset)

    def debug_draw(self, surface, offset):
        pygame.draw.rect(surface, (255, 255, 0), self.rect.move(offset), 2)


    def handle_event(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.visible = True

    def update(self, dt):
        #print(f"[DEBUG] Boss update called, dt={dt}, pos={self.rect.center}, health={self.health}")
        now = pygame.time.get_ticks()
        self.animate(dt)
        self.weakspot.update_position(self.true_state)
        
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
        bar_y = 50

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
