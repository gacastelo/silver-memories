from settings import *
from game import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Silver Memories - Menu")
    clock = pygame.time.Clock()

    # Criar botões
    start_button = Button("Iniciar Jogo", (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50))
    quit_button = Button("Sair", (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 30))

    running = True

    background = pygame.transform.scale(pygame.image.load(join('images', 'background.jpg')).convert_alpha(), (WINDOW_WIDTH, WINDOW_HEIGHT))

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # Botões
        if start_button.draw(screen):
            game = Game()
            game.run()

        if quit_button.draw(screen):
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
