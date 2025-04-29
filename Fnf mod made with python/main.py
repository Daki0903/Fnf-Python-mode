import pygame
from game import run_game

# Inicijalizacija Pygame i muzike
pygame.init()
pygame.mixer.init()  # Inicijalizacija mixer-a za zvuk

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FNF Python - Main Menu")
font = pygame.font.SysFont("monospace", 64)
clock = pygame.time.Clock()
WHITE = (255, 255, 255)

# Učitavanje muzike i pozadinske slike
pygame.mixer.music.load("MainMenuMusic.mp3")
pygame.mixer.music.play(-1, 0.0)  # Ponavljanje muzike u glavnom meniju

bg_image = pygame.image.load("Bgimg.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

def draw_main_menu(selected):
    screen.fill((0, 0, 0))  # Započinjemo sa crnom pozadinom
    screen.blit(bg_image, (0, 0))  # Prikazivanje pozadinske slike
    title = font.render("Friday Night Funkin' Python", True, WHITE)
    play = font.render("▶ Play", True, (0, 255, 0) if selected == 0 else WHITE)
    quit_game = font.render("✖ Quit", True, (255, 0, 0) if selected == 1 else WHITE)

    screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
    screen.blit(play, (WIDTH//2 - play.get_width()//2, 300))
    screen.blit(quit_game, (WIDTH//2 - quit_game.get_width()//2, 400))
    pygame.display.flip()

def main():
    selected = 0
    running = True
    while running:
        draw_main_menu(selected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_DOWN, pygame.K_UP]:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        pygame.mixer.music.stop()  # Zaustavljanje muzike pre nego što počne igra
                        run_game(screen)
                    elif selected == 1:
                        running = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
