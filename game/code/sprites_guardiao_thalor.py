from settings import *
from sprites import *
#==========================================#

           # Guardião de Thalor

#==========================================#

class ColunaAscendenteShadow(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, colision_sprite):
        super().__init__(groups)
        print("[DEBUG] colision_sprite recebido na sombra:", colision_sprite)
        self.image_prev = pygame.image.load('images/bosses/gardiao_de_thalor/coluna/shadow.png').convert_alpha()
        self.groups_ = groups
        self.image = pygame.transform.smoothscale(self.image_prev, (200, 50))
        self.rect = self.image.get_rect(topleft = pos)
        self.duracao = 800
        self.spawn_time = pygame.time.get_ticks()
        self.player = player
        self.pos = pos

        self.colision_sprite = colision_sprite

    def update(self,dt):
        now = pygame.time.get_ticks()
        if now - self.spawn_time >= self.duracao:
            ColunaAscendente(self.pos, self.groups_, self.player, self.colision_sprite)
            self.kill()
    
    def player_hit(self):
        pass

class ColunaAscendente(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, colision_sprite):
        super().__init__(groups)
        print("[DEBUG] colision_sprite recebido na coluna:", colision_sprite)
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
        self.tempo_colisao = 100
        self.colisao = False
        self.groups_ = groups
        self.colision_sprite = colision_sprite
        
    
    def update(self,dt):
        
        now = pygame.time.get_ticks()

        if now - self.spawn_time >= self.tempo_colisao:
            self.colisao = True
            print("[DEBUG] Colisão ativa!")

        if now - self.spawn_time >= self.duracao_damage:
            self.player_hit()

        if self.colisao:
            self.colision_sprite.add(self)

        if now - self.spawn_time >= self.duracao:
            self.colision_sprite.remove(self)
            self.kill()
    
    def player_hit(self):
        if self.dano_ativo and self.rect.colliderect(self.player.hitbox_rect):
            print("[DEBUG] Player atingido pela coluna!")
            self.player.take_damage()
            self.dano_ativo = False