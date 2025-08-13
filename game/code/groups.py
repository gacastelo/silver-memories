from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        # Calcula o deslocamento da câmera para centralizar no alvo (player)
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        # Divide os sprites em camadas (ground e object), se quiser desenhar na ordem correta
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        # Desenha cada camada
        for layer in [ground_sprites, object_sprites]:
            # Ordena por profundidade (exemplo: pelo centro vertical do sprite)
            for sprite in sorted(layer, key=lambda spr: spr.rect.centery):
                if hasattr(sprite, 'draw') and callable(sprite.draw):
                    # Se o sprite tem método draw customizado, chama passando a surface e o offset
                    sprite.draw(self.screen, self.offset)
                else:
                    # Caso contrário, desenha o sprite usando a posição ajustada pelo offset
                    pos = sprite.rect.topleft + self.offset
                    self.screen.blit(sprite.image, pos)