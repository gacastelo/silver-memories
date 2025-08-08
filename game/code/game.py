from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame 
from groups import AllSprites

from random import randint

class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Silver Memories")
        self.clock = pygame.time.Clock()
        self.running = True

        #grupos
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        #sprites
        self.player = Player((400,300), self.all_sprites, self.collision_sprites)

        for i in range(5):
            x,y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
            w,h = randint(50, 100), randint(50, 100)
            size = (w, h)
            ColisionSprite((x,y), size , (self.all_sprites, self.collision_sprites))

    def setup(self):
        map = load_pygame(join('game', 'assets', 'maps', 'map.tmx'))

        for x, y, image in map.get_layer_by_name('ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            ColisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collision'):
            ColisionSprite((obj.x, obj.y), pygame.surface((obj.width, obj.height)), self.collision_sprites)

    def run(self):
        while self.running:
            # Delta time for frame rate control
            dt = self.clock.tick(60) / 1000.0
            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update game state 
            self.all_sprites.update(dt)

            #draw 
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    # Initialize the game
    jogo = Game()
    jogo.run()