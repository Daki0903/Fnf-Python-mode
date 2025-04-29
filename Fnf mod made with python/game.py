import pygame
import os
import random

# Initialize Pygame and the music system
pygame.mixer.init()

# Game settings
WIDTH, HEIGHT = 1280, 720
arrow_size = 80
arrow_speed = 7
hit_zone_y = 600
keys = ["left", "down", "up", "right"]
key_map = {
    "left": pygame.K_LEFT,
    "down": pygame.K_DOWN,
    "up": pygame.K_UP,
    "right": pygame.K_RIGHT
}

# Arrow class to handle arrow objects
class Arrow:
    arrow_images = {
        "left": pygame.image.load(os.path.join("assets", "leftArrow.png")),
        "down": pygame.image.load(os.path.join("assets", "downArrow.png")),
        "up": pygame.image.load(os.path.join("assets", "upArrow.png")),
        "right": pygame.image.load(os.path.join("assets", "rightArrow.png")),
    }

    def __init__(self, direction):
        self.direction = direction
        self.image = pygame.transform.scale(Arrow.arrow_images[direction], (arrow_size, arrow_size))
        self.x = keys.index(direction) * 120 + 400
        self.y = -arrow_size

    def move(self):
        self.y += arrow_speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_in_hit_zone(self):
        return hit_zone_y - 40 < self.y < hit_zone_y + 40

# Main game function
def run_game(screen):
    font = pygame.font.SysFont("monospace", 36)
    clock = pygame.time.Clock()

    # Load background music
    pygame.mixer.music.load("InGameMusic.mp3")
    pygame.mixer.music.play(-1, 0.0)  # Loop the music

    # Initialize game variables
    arrows = []
    spawn_timer = 0
    score = 0
    misses = 0
    combo = 0
    max_misses = 10
    running = True

    while running:
        screen.fill((20, 20, 20))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Stop music on quit
                return
            elif event.type == pygame.KEYDOWN:
                for arrow in arrows:
                    if arrow.is_in_hit_zone() and event.key == key_map[arrow.direction]:
                        arrows.remove(arrow)
                        score += 1
                        combo += 1  # Increase combo
                        play_sound("hit_sound.wav")  # Play hit sound
                        break
                else:
                    misses += 1
                    combo = 0  # Reset combo on miss
                    play_sound("miss_sound.wav")  # Play miss sound

        # Spawn arrows at intervals
        spawn_timer += 1
        if spawn_timer > max(30 - score // 10, 10):  # Increase frequency with score
            arrows.append(Arrow(random.choice(keys)))
            spawn_timer = 0

        # Move and draw arrows
        for arrow in arrows[:]:
            arrow.move()
            arrow.draw(screen)
            if arrow.y > HEIGHT:
                arrows.remove(arrow)
                misses += 1
                combo = 0  # Reset combo when arrow goes off-screen

        # Draw the hit zone
        pygame.draw.line(screen, (255, 255, 255), (0, hit_zone_y + arrow_size // 2), (WIDTH, hit_zone_y + arrow_size // 2), 2)

        # Display score and misses
        score_text = font.render(f"Score: {score}  Misses: {misses}/{max_misses}  Combo: {combo}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

        # Check game over condition
        if misses >= max_misses:
            pygame.mixer.music.stop()  # Stop music after game over
            game_over(screen, score)

# Play sound effect
def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()

# Game over screen
def game_over(screen, score):
    font = pygame.font.SysFont("monospace", 60)
    small_font = pygame.font.SysFont("monospace", 36)
    clock = pygame.time.Clock()

    while True:
        screen.fill((10, 0, 20))
        over_text = font.render("Game Over!", True, (255, 50, 50))
        score_text = small_font.render(f"Your Score: {score}", True, (255, 255, 255))
        info_text = small_font.render("Press ENTER to restart or ESC to exit", True, (180, 180, 180))

        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, 200))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 300))
        screen.blit(info_text, (WIDTH//2 - info_text.get_width()//2, 400))

        pygame.display.flip()

        # Event handling for restart or quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Restart the game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()  # Quit the game

        clock.tick(60)

# Start the game
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Arrow Catcher Game")
    run_game(screen)

if __name__ == "__main__":
    main()
