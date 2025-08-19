from settings import *
#==========================================#

           # Guardião de Thalor

#==========================================#

class ColunaAscendenteShadow(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.image_prev = pygame.image.load('images/bosses/gardiao_de_thalor/coluna/shadow.png').convert_alpha()
        self.groups_ = groups
        self.image = pygame.transform.smoothscale(self.image_prev, (200, 50))
        self.rect = self.image.get_rect(topleft = pos)
        self.duracao = 800
        self.spawn_time = pygame.time.get_ticks()
        self.player = player
        self.pos = pos

    def update(self,dt):
        now = pygame.time.get_ticks()
        if now - self.spawn_time >= self.duracao:
            ColunaAscendente(self.pos, self.groups_, self.player)
            self.kill()
    
    def player_hit(self):
        pass

class ColunaAscendente(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        margemy = 50
        self.pos = (pos[0], pos[1]-margemy)
        self.image_prev = pygame.image.load('images/bosses/gardiao_de_thalor/coluna/preda.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image_prev, (200, 350))
        self.rect = self.image.get_rect(bottomleft = pos)
        self.duracao = 800
        self.spawn_time = pygame.time.get_ticks()
        self.player = player
        self.dano_ativo = True
        self.duracao_damage = 50
    
    def update(self,dt):
        
        now = pygame.time.get_ticks()

        if now - self.spawn_time >= self.duracao_damage:
            self.player_hit()

        if now - self.spawn_time >= self.duracao:
            self.kill()
    
    def player_hit(self):
        if self.dano_ativo and self.rect.colliderect(self.player.hitbox_rect):
            print("[DEBUG] Player atingido pela coluna!")
            self.player.take_damage()
            self.dano_ativo = False