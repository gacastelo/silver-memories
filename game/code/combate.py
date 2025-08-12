from settings import *

class Combate:
    def __init__(self, player, boss):
        self.player = player
        self.boss = boss

    def start_combat(self):
        self.player.in_combat = True
    
    def end_combat(self):
        self.player.in_combat = False

    def update(self, dt):
        self.check_player_hit()


    def check_player_hit(self):
        if not self.player.attacking:
            return

        damage = self.player.dar_dano()
        print(f"[DEBUG] Player atacando! Dano base: {damage}")

        weakspot_hit = self.player.attack_hitbox.colliderect(self.boss.weakspot.rect) and self.boss.is_player_behind()
        body_hit = self.player.attack_hitbox.colliderect(self.boss.rect)

        print(f"[DEBUG] Colisão ponto fraco: {weakspot_hit}")
        print(f"[DEBUG] Colisão corpo: {body_hit}")

        # Cooldown de dano
        now = pygame.time.get_ticks()
        tempo_desde_ultimo_hit = now - self.boss.last_hit_time
        print(f"[DEBUG] Tempo desde último hit: {tempo_desde_ultimo_hit} ms")

        if tempo_desde_ultimo_hit < self.boss.hit_cooldown:
            print("[DEBUG] Boss ainda em invulnerabilidade.")
            return

        if weakspot_hit:
            print("[DEBUG] Golpe no ponto fraco e player está atrás!")
            self.boss.take_damage(damage, True)
            self.boss.last_hit_time = now
        elif body_hit:
            print("[DEBUG] Golpe no corpo do boss.")
            self.boss.take_damage(damage, False)
            self.boss.last_hit_time = now
        else:
            print("[DEBUG] Ataque não acertou o boss.")

    def check_boss_especial_hit(self):
        pass
