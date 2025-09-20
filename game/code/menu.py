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

    title_font = pygame.font.Font(None, 80)
    running = True

    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Título
        title_surface = title_font.render("Silver Memories", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 - 50))
        screen.blit(title_surface, title_rect)

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
