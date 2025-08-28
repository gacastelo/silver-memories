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
        self.image = pygame.transform.smoothscale(self.image_prev, (200, 200))
        self.rect = self.image.get_rect(topleft = pos)
        self.duracao = 800
        self.spawn_time = pygame.time.get_ticks()
        self.player = player
        self.pos = pos
        self.z = ENEMY_SHADOW_ATTACK_LAYER

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
        margemy = 0
        self.pos = pos
        self.image_prev = pygame.image.load('images/bosses/gardiao_de_thalor/coluna/preda.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image_prev, (200, 200))
        self.rect = self.image.get_rect(topleft = pos)
        self.duracao = 800
        self.spawn_time = pygame.time.get_ticks()
        self.player = player
        self.dano_ativo = True
        self.duracao_damage = 50
        self.tempo_colisao = 100
        self.colisao = False
        self.groups_ = groups
        self.stop_rect = self.rect.inflate(-30,-30)
        self.colision_sprite = colision_sprite
        self.z = ENEMY_ATTACK_LAYER
        
    
    def update(self,dt):
        
        now = pygame.time.get_ticks()

        if now - self.spawn_time >= self.tempo_colisao:
            self.colisao = True

        if now - self.spawn_time >= self.duracao_damage:
            self.player_hit()

        if self.colisao:
            self.colision_sprite.add(self)

        if now - self.spawn_time >= self.duracao:
            self.colision_sprite.remove(self)
            self.player.reset_speed()
            self.kill()
    
    def player_hit(self):
        if self.dano_ativo and self.rect.colliderect(self.player.hitbox_rect):
            print("[DEBUG] Player atingido pela coluna!")
            self.player.take_damage()
            self.dano_ativo = False
        
        if self.stop_rect.colliderect(self.player.hitbox_rect):
            self.player.speed = 0

class ExplosaoMagnamica(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, cupula):
        super().__init__(groups)
        self.pos = pos
        self.image_prev = pygame.image.load('images/bosses/gardiao_de_thalor/explosao/bumm.jpg').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image_prev, (2000, 2000))
        self.rect = self.image.get_rect(center = pos)
        self.duracao = 1000
        self.spawn_time = pygame.time.get_ticks()
        self.player_atingido = False
        self.z = EFFECT_LAYER

        self.player = player
        self.cupula = cupula

    def player_hit(self):
        if self.rect.colliderect(self.player.hitbox_rect) and self.cupula.player_in_defense == False and not self.player_atingido:
            print("[DEBUG] Player atingido pela explosao!")
            self.player.take_damage()
            self.player_atingido = True

    def update(self,dt):
        self.player_hit()
        now = pygame.time.get_ticks()
        if now - self.spawn_time >= self.duracao:
            self.kill()



class CupulaDefensiva(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.pos = pos
        self.image_prev = pygame.image.load('images/bosses/gardiao_de_thalor/explosao/cupula_defensiva.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image_prev, (200, 200))
        self.rect = self.image.get_rect(center = pos)
        self.player_in_defense = False
        self.player = player
        self.spawn_time = pygame.time.get_ticks()
        self.z = EFFECT_LAYER + 1
        self.tempo_para_o_ataque = 1000
        self.groups_ = groups
        self.nao_atacou = True
    
    def player_hit(self):
        if self.rect.colliderect(self.player.hitbox_rect):
            print("[DEBUG] Player defendido pela cupula!")
            self.player_in_defense = True
            return self.player_in_defense
    

    def update(self,dt):
        self.player_hit()
        now = pygame.time.get_ticks()
        if now - self.spawn_time >= 3000:
            self.kill()
        if (now - self.spawn_time >= self.tempo_para_o_ataque) and self.nao_atacou:
            ExplosaoMagnamica(self.player.rect.center, self.groups_, self.player, self)
            self.nao_atacou = False