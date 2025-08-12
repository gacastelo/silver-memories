from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from boss import *
from combate import Combate

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group() 

        self.setup()

        # sprites
        
    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites)
                
        self.spawn_points = [(1800, 900), (1800, 950)]
        self.boss = GuardiaoAstra((1800, 800), self.all_sprites, self.player, self.spawn_points, (196, 256))
        self.collision_sprites.add(self.boss.collision_sprite)
        
        self.combate = Combate(self.player, self.boss)
        self.combate.start_combat()

    def run(self):
        while self.running:
            # dt 
            dt = self.clock.tick(60) / 1000

            # event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.player.handle_mouse_input(event)

                #boss
                self.boss.collision_sprite.update()
                self.boss.handle_event(event)

                self.boss.update(dt)
                self.boss.draw(self.screen)

            # update 
            self.all_sprites.update(dt)
            if self.player.in_combat:
                self.combate.update(dt)

            # draw
            self.screen.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            if self.boss.alive():
                self.boss.draw_health_bar(self.screen)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()