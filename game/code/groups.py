from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def draw(self, target_position):
        self.offset.x = -(target_position[0] + WINDOW_WIDTH // 2)
        self.offset.y = -(target_position[1] + WINDOW_HEIGHT // 2)

        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)