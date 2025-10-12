from settings import *

class UI(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        self.player = player
        self.boss = None

        self.z = UI_LAYER
        self.ignore_camera = True

        # --- Player UI ---
        self.path = self._make_player_path()
        self.image = pygame.image.load(join('images', 'ui', 'health_bar', self.path)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(20, 20))

    # =============================
    # Player Health Bar
    # =============================
    def _make_player_path(self):
        """Monta o caminho da imagem da barra de vida do player"""
        return 'vida' + ('4_' if self.player.max_health == 4 else '') + str(self.player.get_health()) + '.png'

    def draw(self, screen, offset):
        """Desenha UI fixa (barra do player)"""
        screen.blit(self.image, self.rect)
        if self.boss:
            self.draw_boss_health(screen)

    def update(self, *args, **kwargs):
        """Atualiza barra de vida do player"""
        self.path = self._make_player_path()
        self.image = pygame.image.load(join('images', 'ui', 'health_bar', self.path)).convert_alpha()

    # =============================
    # Barra de Vida do Boss
    # =============================
    def set_boss(self, boss):
        """Define o boss atual (ou None se não tiver)"""
        self.boss = boss

    def draw_boss_health(self, surface):
        """Desenha barra de vida do boss no topo da tela"""
        if not self.boss:
            return

        bar_width = WINDOW_WIDTH * 0.4
        bar_height = WINDOW_HEIGHT * 0.05
        bar_x = (surface.get_width() - bar_width) // 2
        bar_y = (WINDOW_HEIGHT * 0.95) - bar_height

        # Fundo da barra
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        # Vida
        fill_width = int(bar_width * (self.boss.health / self.boss.max_health))
        pygame.draw.rect(surface, (125, 0, 0), (bar_x, bar_y, fill_width, bar_height))

        # Frame decorativo
        img = pygame.image.load(join('images', 'bosses', self.boss.file_name, 'bossbar.png')).convert_alpha()
        img = pygame.transform.smoothscale(img, (WINDOW_WIDTH * 0.45, WINDOW_HEIGHT * 0.125))
        surface.blit(img, (bar_x - WINDOW_WIDTH * 0.025, bar_y - WINDOW_HEIGHT* 0.03))

        # Nome do boss
        font_path = 'data/fonts/bossbar.ttf'
        font = pygame.font.Font(font_path, 40)
        text = font.render(self.boss.name, True, (255, 255, 255))
        surface.blit(text, (bar_x, bar_y - WINDOW_HEIGHT * 0.025))
