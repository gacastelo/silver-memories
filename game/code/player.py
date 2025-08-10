from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.image = self.frames[self.state][0]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-90, -75)
        self.damage_hitbox = self.rect.inflate(-40,-40)  # Retângulo para o hitbox de dano

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

        # combate atributos
        self.health = 3
        self.max_health = 3
        self.damage = 10

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
                    if base_state in self.frames and self.frames[base_state]:
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

        attack_size_horizontal = (60, 120)
        attack_size_vertical = (120, 60)

        # Cria um Rect temporário no centro do player para facilitar o cálculo
        temp_rect = pygame.Rect(self.hitbox_rect.centerx, self.hitbox_rect.centery, 0, 0)

        if 'up' in self.state:
            self.attack_hitbox = pygame.Rect(0, 0, *attack_size_vertical)
            self.attack_hitbox.midbottom = (self.hitbox_rect.centerx, self.hitbox_rect.top - offset)
        elif 'down' in self.state:
            self.attack_hitbox = pygame.Rect(0, 0, *attack_size_vertical)
            self.attack_hitbox.midtop = (self.hitbox_rect.centerx, self.hitbox_rect.bottom + offset)
        elif 'left' in self.state:
            self.attack_hitbox = pygame.Rect(0, 0, *attack_size_horizontal)
            self.attack_hitbox.midright = (self.hitbox_rect.left - offset, self.hitbox_rect.centery)
        elif 'right' in self.state:
            self.attack_hitbox = pygame.Rect(0, 0, *attack_size_horizontal)
            self.attack_hitbox.midleft = (self.hitbox_rect.right + offset, self.hitbox_rect.centery)

    # A principal alteração está nesta função para otimizar o movimento e colisão
    def move(self, dt):
        self.posicao_anterior = self.hitbox_rect.copy()
        if self.direction.length() > 0:
            # Movimento e colisão horizontal
            self.hitbox_rect.x += self.direction.x * self.speed * dt
            self.collision('horizontal')
            
            # Movimento e colisão vertical
            self.hitbox_rect.y += self.direction.y * self.speed * dt
            self.collision('vertical')
        
        # Finalmente, centraliza o retangulo visual no hitbox
        self.rect.center = self.hitbox_rect.center

        # Atualiza a posição do hitbox de dano para coincidir com o hitbox do jogador
        self.damage_hitbox.center = self.hitbox_rect.center

    #def collision(self, direction): #COLISÃO ANTIGA SAVED 
    #   for sprite in self.collision_sprites:
    #       if sprite.rect.colliderect(self.hitbox_rect):
    #           if direction == 'horizontal':
    #               if self.direction.x > 0:  # Movendo para a direita
    #                   self.hitbox_rect.right = sprite.rect.left
    #               if self.direction.x < 0:  # Movendo para a esquerda
    #                   self.hitbox_rect.left = sprite.rect.right
    #           else:  # vertical
    #               if self.direction.y < 0:  # Movendo para cima
    #                   self.hitbox_rect.top = sprite.rect.bottom
    #               if self.direction.y > 0:  # Movendo para baixo
    #                   self.hitbox_rect.bottom = sprite.rect.top

    # Lógica de colisão original e mais fudida totalmente feia 
    def collision(self, direction):
        amortecimento_horizontal = 11 # para evitar q a camera fique tremendo muito
        amortecimento_vertical = 20 # para evitar q a camera fique tremendo muito
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # Movendo para a direita
                        self.hitbox_rect.right = self.posicao_anterior.centerx + amortecimento_horizontal
                    if self.direction.x < 0:  # Movendo para a esquerda
                        self.hitbox_rect.left = self.posicao_anterior.centerx - amortecimento_horizontal
                else:  # vertical
                    if self.direction.y < 0:  # Movendo para cima
                        self.hitbox_rect.top = self.posicao_anterior.centery - amortecimento_vertical
                    if self.direction.y > 0:  # Movendo para baixo
                        self.hitbox_rect.bottom = self.posicao_anterior.centery + amortecimento_vertical


    def get_state(self):
        # Define o estado atual (direção) para animação
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        elif self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
        # Se não houver movimento, o estado não muda, mantendo a última direção olhada

    def animate(self, dt):
        previous_state = getattr(self, "previous_state", self.state)
        self.get_state()

        if self.attacking:
            self.image = self.frames[self.state.replace('_idle', '')][0]
            frames = self.sword_frames[self.state.replace('_idle', '')]
            self.sword_frame_index += 15 * dt
            if self.sword_frame_index >= len(frames):
                self.sword_frame_index = len(frames) - 1

        elif self.shield_active:
            idle_state = self.state.split('_')[0] + '_idle'
            if idle_state in self.frames and self.frames[idle_state]:
                self.image = self.frames[idle_state][0]
            else:
                self.image = self.frames[self.state.replace('_idle', '')][0]

        else:
            moving = self.direction.length() > 0
            # Se acabou de sair do idle, começar no frame 1
            if moving and "_idle" in previous_state:
                self.frame_index = 1.0

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

        self.previous_state = self.state


    def draw(self, surface, offset):
        # Desenha o sprite do jogador
        pos = self.rect.topleft + offset
        surface.blit(self.image, pos)

        # Desenha a espada e sua hitbox (para debug)
        if self.attacking and self.attack_hitbox:
            pygame.draw.rect(surface, 'red', self.attack_hitbox.move(offset), 2)
            
            sword_frames = self.sword_frames[self.state.replace('_idle', '')]
            if sword_frames:
                sword_img = sword_frames[int(self.sword_frame_index)]
                sword_rect = sword_img.get_rect(center=self.attack_hitbox.center)
                surface.blit(sword_img, sword_rect.topleft + offset)

        # Desenha a hitbox do escudo (para debug)
        if self.shield_active and self.shield_hitbox:
            pygame.draw.rect(surface, 'blue', self.shield_hitbox.move(offset), 2)
        

        # Adiciona a função de debug para desenhar o rect e hitbox do jogador e das colisões
        self.debug_draw(surface, offset)


    def debug_draw(self, surface, offset):
        """
        Função de debug para desenhar as hitboxes e rects.
        Chame esta função no loop principal do jogo para ver as caixas de colisão.
        """
        # Desenha a hitbox do jogador
        pygame.draw.rect(surface, 'yellow', self.hitbox_rect.move(offset), 2)

        # Desenha o rect visual do jogador
        pygame.draw.rect(surface, 'green', self.rect.move(offset), 2)

        # Desenha a hitbox de dano do jogador
        pygame.draw.rect(surface, 'orange', self.damage_hitbox.move(offset), 2)

        # Desenha as hitboxes de todos os sprites de colisão
        for sprite in self.collision_sprites:
            pygame.draw.rect(surface, 'purple', sprite.rect.move(offset), 2)

    def cooldowns(self):
        now = pygame.time.get_ticks()
        
        if self.attacking:
            if now - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.attack_hitbox = None

        if self.shield_active:
            if now - self.shield_time >= self.shield_duration:
                self.shield_active = False
                self.shield_hitbox = None

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.cooldowns()