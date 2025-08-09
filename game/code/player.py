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
        self.attack_cooldown = 300  # ms para duração do ataque
        self.attack_time = None
        self.attack_hitbox = None  # retângulo para o ataque

        # carregar sprites da espada para cada direção (pode ter múltiplos frames para animação da espada)
        self.sword_frames = {'up': [], 'down': [], 'left': [], 'right': []}
        for direction in self.sword_frames.keys():
            sword_path = join('images', 'sword', direction)
            for _, _, files in walk(sword_path):
                if files:
                    for file_name in sorted(files, key=lambda n: int(n.split('.')[0])):
                        full_path = join(sword_path, file_name)
                        img = pygame.image.load(full_path).convert_alpha()
                        self.sword_frames[direction].append(img)
        self.sword_frame_index = 0

    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        for state in self.frames.keys():
            for folder_path, _, file_names in walk(join('images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.attacking:
            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
            self.direction = self.direction.normalize() if self.direction.length() > 0 else pygame.Vector2()

            # ataque com botão esquerdo do mouse
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] and not self.attacking:
                print("Attack!")
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.direction = pygame.Vector2()  # para o movimento
                self.create_attack_hitbox()
                self.sword_frame_index = 0

    def create_attack_hitbox(self):
        offset = 0
        width, height = 120, 90  # tamanho do hitbox do ataque 
        if self.state == 'up':
            print("create up")
            self.attack_hitbox = pygame.Rect(0, 0, width, height)
            self.attack_hitbox.midbottom = (self.hitbox_rect.centerx, self.hitbox_rect.top - offset)
    
        elif self.state == 'down':
            print("create down")
            self.attack_hitbox = pygame.Rect(0, 0, width, height)
            self.attack_hitbox.midtop = (self.hitbox_rect.centerx, self.hitbox_rect.bottom + offset)
    
        elif self.state == 'left':
            print("create left")
            self.attack_hitbox = pygame.Rect(0, 0, height, width)  # inverte largura e altura
            self.attack_hitbox.midright = (self.hitbox_rect.left - offset, self.hitbox_rect.centery)
    
        elif self.state == 'right':
            print("create right")
            self.attack_hitbox = pygame.Rect(0, 0, height, width)
            self.attack_hitbox.midleft = (self.hitbox_rect.right + offset, self.hitbox_rect.centery)

    def move(self, dt):
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
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def animate(self, dt):
        if self.attacking:
            frames = self.sword_frames[self.state]
            self.sword_frame_index += 15 * dt
            if self.sword_frame_index >= len(frames):
                self.sword_frame_index = len(frames) - 1  # segura no último frame da espada

            self.image = self.frames[self.state][0]
        else:
            if self.direction.x != 0:
                self.state = 'right' if self.direction.x > 0 else 'left'
            elif self.direction.y != 0:
                self.state = 'down' if self.direction.y > 0 else 'up'

            self.frame_index = self.frame_index + 5 * dt if self.direction.length() > 0 else 0
            self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def draw(self, surface, offset=pygame.Vector2(0, 0)):
        # aplica offset ao desenhar
        pos = self.rect.topleft + offset
        surface.blit(self.image, pos)

        if self.attacking:
            sword_img = self.sword_frames[self.state][int(self.sword_frame_index)]
            sword_pos = self.get_sword_position(sword_img) + offset
            surface.blit(sword_img, sword_pos)
            # Desenha a hitbox para debug
            pygame.draw.rect(surface, (255, 0, 0), self.attack_hitbox.move(offset.x, offset.y), 2)

    def get_sword_position(self, sword_img):
        x, y = self.rect.center
        offset = 30
        if self.state == 'up':
            return pygame.Vector2(x, y - offset)
        elif self.state == 'down':
            return pygame.Vector2(x, y + offset)
        elif self.state == 'left':
            return pygame.Vector2(x - offset, y)
        elif self.state == 'right':
            return pygame.Vector2(x + offset, y)

    def update(self, dt):
        if self.attacking:
            now = pygame.time.get_ticks()
            if now - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.attack_hitbox = None
        else:
            self.input()
            self.move(dt)

        self.animate(dt)