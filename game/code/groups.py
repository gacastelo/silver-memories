from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        # deslocamento da câmera
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        # ordena todos os sprites pela camada (z) e depois pela posição vertical (pra dar profundidade)
        for sprite in sorted(self.sprites(), key=lambda spr: (getattr(spr, 'z', 0), spr.rect.centery)):
            if hasattr(sprite, 'draw') and callable(sprite.draw):
                # UI e outros que ignoram offset
                if getattr(sprite, 'ignore_camera', False):
                    sprite.draw(self.screen, pygame.Vector2())
                else:
                    sprite.draw(self.screen, self.offset)
            else:
                pos = sprite.rect.topleft
                if not getattr(sprite, 'ignore_camera', False):
                    pos += self.offset
                self.screen.blit(sprite.image, pos)
