from settings import *
class BossAttackHitbox(pygame.sprite.Sprite):
    def __init__(self, boss):
        super().__init__()
        self.boss = boss
    
    def create_attack_hitbox(self):
        if self.boss.true_state == "right":
            self.boss.attack_zone = pygame.Rect(
                self.boss.rect.right,                 # começa ao lado direito do boss
                self.boss.rect.top,
                self.boss.attack_range,
                self.boss.rect.height
            )
        elif self.boss.true_state == "left":
            self.boss.attack_zone = pygame.Rect(
                self.boss.rect.left - self.attack_range,
                self.boss.rect.top,
                self.boss.attack_range,
                self.boss.rect.height
            )
        elif self.boss.true_state == "up":
            self.boss.attack_zone = pygame.Rect(
                self.boss.rect.left,
                self.boss.rect.top - self.attack_range,
                self.boss.rect.width,
                self.boss.attack_range
            )
        elif self.boss.true_state == "down":
            self.boss.attack_zone = pygame.Rect(
                self.boss.rect.left,
                self.boss.rect.bottom,
                self.boss.rect.width,
                self.boss.attack_range
            )

        return self.boss.attack_zone