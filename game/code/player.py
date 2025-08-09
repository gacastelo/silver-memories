from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.image = self.frames[self.state][0]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        # movement 
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

        # ataque
        self.attacking = False
        self.attack_cooldown = 400  # ms para duração do ataque
        self.attack_time = None
        self.attack_hitbox = None  # retângulo para o ataque

        # escudo
        self.shield_active = False
        self.shield_duration = 500 # Duração que o escudo fica ativo
        self.shield_time = None
        self.shield_hitbox = None

        # carregar sprites da espada
        self.sword_frames = {'up': [], 'down': [], 'left': [], 'right': []}
        self.load_sword_images()
        self.sword_frame_index = 0

    def load_sword_images(self):
        # Helper para carregar imagens da espada
        for direction in self.sword_frames.keys():
            sword_path = join('images', 'sword', direction)
            # Checa se o diretório existe para evitar erros
            try:
                for _, _, files in walk(sword_path):
                    if files:
                        for file_name in sorted(files, key=lambda n: int(n.split('.')[0])):
                            full_path = join(sword_path, file_name)
                            img = pygame.image.load(full_path).convert_alpha()
                            self.sword_frames[direction].append(img)
            except FileNotFoundError:
                print(f"Aviso: Diretório de espada não encontrado em '{sword_path}'. A espada não terá sprites para esta direção.")


    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': [], 'left_idle': [], 'right_idle': [], 'up_idle': [], 'down_idle': []}
        # Adicione também os estados de defesa se tiver sprites para eles
        # 'left_shield': [], 'right_shield': [], 'up_shield': [], 'down_shield': []
        
        for state in self.frames.keys():
            path = join('images', 'player', state)
            # Apenas tenta carregar se o diretório existir
            try:
                self.frames[state] = [pygame.image.load(join(path, file_name)).convert_alpha() 
                                    for _, _, file_names in walk(path) for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0]))]
            except FileNotFoundError:
                 # Se não houver sprites de idle, usa o primeiro frame do movimento
                if '_idle' in state:
                    base_state = state.replace('_idle', '')
                    if self.frames[base_state]:
                        self.frames[state] = [self.frames[base_state][0]]
                    else:
                        print(f"Aviso: Sprites para '{state}' e '{base_state}' não encontrados.")


    def input(self):
        # Se o jogador estiver em uma ação (atacando ou defendendo), não processa novos inputs de movimento/ação
        if self.attacking or self.shield_active:
            return

        keys = pygame.key.get_pressed()
        
        # Movimento
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction.length() > 0 else pygame.Vector2()

        # Ações com o mouse
        mouse_buttons = pygame.mouse.get_pressed()
        
        # Ataque com botão esquerdo
        if mouse_buttons[0]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.direction = pygame.Vector2()  # Para o movimento durante o ataque
            self.create_attack_hitbox()
            self.sword_frame_index = 0
        
        # Ativar escudo com botão direito
        elif mouse_buttons[2]:
            self.shield_active = True
            self.shield_time = pygame.time.get_ticks()
            self.direction = pygame.Vector2()  # Para o movimento durante a defesa
            self.create_shield_hitbox()

    def create_shield_hitbox(self):
        offset = 10 # Distância do escudo em relação ao jogador
        
        # Para esquerda e direita, o escudo é VERTICAL
        if 'left' in self.state or 'right' in self.state:
            shield_w, shield_h = 20, 90 # Largura e altura para um escudo vertical
            
            if 'right' in self.state:
                # Posição X: na direita do jogador + offset
                # Posição Y: centralizado verticalmente
                self.shield_hitbox = pygame.Rect(
                    self.hitbox_rect.right + offset, 
                    self.hitbox_rect.centery - shield_h / 2, 
                    shield_w, shield_h)
            else: # left
                # Posição X: na esquerda do jogador - largura do escudo - offset
                # Posição Y: centralizado verticalmente
                self.shield_hitbox = pygame.Rect(
                    self.hitbox_rect.left - shield_w - offset, 
                    self.hitbox_rect.centery - shield_h / 2, 
                    shield_w, shield_h)
    
        # Para cima e para baixo, o escudo é HORIZONTAL
        else:
            shield_w, shield_h = 90, 20 # Largura e altura para um escudo horizontal
    
            if 'down' in self.state:
                # Posição X: centralizado horizontalmente
                # Posição Y: abaixo do jogador + offset
                self.shield_hitbox = pygame.Rect(
                    self.hitbox_rect.centerx - shield_w / 2, 
                    self.hitbox_rect.bottom + offset, 
                    shield_w, shield_h)
            else: # up
                # Posição X: centralizado horizontalmente
                # Posição Y: acima do jogador - altura do escudo - offset
                self.shield_hitbox = pygame.Rect(
                    self.hitbox_rect.centerx - shield_w / 2, 
                    self.hitbox_rect.top - shield_h - offset, 
                    shield_w, shield_h)

    def create_attack_hitbox(self):
        offset = 5
        if 'up' in self.state:
            self.attack_hitbox = pygame.Rect(self.hitbox_rect.centerx - 40, self.hitbox_rect.top - 80 - offset, 80, 80)
        elif 'down' in self.state:
            self.attack_hitbox = pygame.Rect(self.hitbox_rect.centerx - 40, self.hitbox_rect.bottom + offset, 80, 80)
        elif 'left' in self.state:
            self.attack_hitbox = pygame.Rect(self.hitbox_rect.left - 80 - offset, self.hitbox_rect.centery - 40, 80, 80)
        elif 'right' in self.state:
            self.attack_hitbox = pygame.Rect(self.hitbox_rect.right + offset, self.hitbox_rect.centery - 40, 80, 80)

    def move(self, dt):
        if self.direction.length() > 0:
            self.hitbox_rect.x += self.direction.x * self.speed * dt
            self.collision('horizontal')
            self.hitbox_rect.y += self.direction.y * self.speed * dt
            self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else: # vertical
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def get_state(self):
        # Define o estado atual (direção) para animação
        # Prioriza o movimento horizontal para a escolha do sprite (left/right)
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        elif self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        # Se não houver movimento, o estado não muda, mantendo a última direção olhada

    def animate(self, dt):
        self.get_state() # Atualiza a direção do personagem
        
        # Animação de ataque
        if self.attacking:
            # Mantém o personagem no primeiro frame da animação de andar da direção atual
            self.image = self.frames[self.state.replace('_idle', '')][0]
            
            # Anima a espada
            frames = self.sword_frames[self.state.replace('_idle', '')]
            self.sword_frame_index += 15 * dt
            if self.sword_frame_index >= len(frames):
                self.sword_frame_index = len(frames) - 1

        # Animação de defesa
        elif self.shield_active:
            # Idealmente, você teria sprites 'up_shield', 'down_shield', etc.
            # Por enquanto, vamos usar a imagem de idle (parado)
            idle_state = self.state.split('_')[0] + '_idle'
            if self.frames[idle_state]:
                self.image = self.frames[idle_state][0]
            else: # Fallback para o primeiro frame de movimento
                self.image = self.frames[self.state.replace('_idle', '')][0]

        # Animação de movimento ou parado
        else:
            if self.direction.length() > 0: # Movendo
                self.frame_index += 5 * dt
                current_frames = self.frames[self.state]
                self.image = current_frames[int(self.frame_index) % len(current_frames)]
            else: # Parado
                self.frame_index = 0
                idle_state = self.state.split('_')[0] + '_idle'
                if self.frames[idle_state]:
                    self.image = self.frames[idle_state][0]
                else: # Fallback
                    self.image = self.frames[self.state.replace('_idle', '')][0]


    def draw(self, surface, offset):
        pos = self.rect.topleft + offset
        surface.blit(self.image, pos)

        # Desenha a espada e sua hitbox (para debug)
        if self.attacking and self.attack_hitbox:
            # Desenha a hitbox do ataque
            pygame.draw.rect(surface, 'red', self.attack_hitbox.move(offset), 2)
            
            # Desenha a imagem da espada
            sword_frames = self.sword_frames[self.state.replace('_idle', '')]
            if sword_frames:
                sword_img = sword_frames[int(self.sword_frame_index)]
                # Centraliza a imagem da espada na hitbox de ataque
                sword_rect = sword_img.get_rect(center=self.attack_hitbox.center)
                surface.blit(sword_img, sword_rect.topleft + offset)

        # Desenha a hitbox do escudo (para debug)
        if self.shield_active and self.shield_hitbox:
            pygame.draw.rect(surface, 'blue', self.shield_hitbox.move(offset), 2)


    def cooldowns(self):
        now = pygame.time.get_ticks()
        
        # Cooldown do ataque
        if self.attacking:
            if now - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.attack_hitbox = None

        # Cooldown do escudo (agora separado e independente)
        if self.shield_active:
            if now - self.shield_time >= self.shield_duration:
                self.shield_active = False
                self.shield_hitbox = None

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.cooldowns() # Chama o método que lida com todos os cooldowns
