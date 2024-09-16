import pygame
import random
import sys
from moviepy.editor import VideoFileClip

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ocean Protector")

# Colors
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)  # Changed from white to black

# Load images
player_image = pygame.image.load('player.png') 
player_image = pygame.transform.scale(player_image, (140, 140))
trash_image = pygame.image.load('trash.png')
trash_image = pygame.transform.scale(trash_image, (80, 80))
powerup_image = pygame.image.load('powerup.png') 
powerup_image = pygame.transform.scale(powerup_image, (100, 100))

# Load and set up the video as background
background_video = VideoFileClip('background_video.mp4')

# Game variables
player_width = 50
player_height = 50
player_x = screen_width // 2
player_y = screen_height - player_height - 10
player_speed = 20
score = 0
level = 1
timer = 60
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Classes
class Trash:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 30, 30)
    
    def draw(self):
        screen.blit(trash_image, (self.x, self.y))

    def move(self):
        self.y += 5
        if self.y > screen_height:
            self.y = -30
            self.x = random.randint(0, screen_width - 30)
        self.rect = pygame.Rect(self.x, self.y, 30, 30)

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 30, 30)
    
    def draw(self):
        screen.blit(powerup_image, (self.x, self.y))

    def is_collected(self, player_rect):
        return self.rect.colliderect(player_rect)

# Initialize game elements
trash_list = [Trash(random.randint(0, screen_width - 30), random.randint(-100, screen_height - 30)) for _ in range(5)]
powerups = [PowerUp(random.randint(0, screen_width - 30), random.randint(-100, screen_height - 30))]

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        # Get current frame of the video
        frame = background_video.get_frame(pygame.time.get_ticks() / 1000)  # Time in seconds
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # Convert to Pygame surface
        screen.blit(pygame.transform.scale(frame_surface, (screen_width, screen_height)), (0, 0))
        
        draw_text('Ocean Protector', font, black, screen, screen_width // 2, screen_height // 2 - 100)
        draw_text('Press Enter to Start', font, black, screen, screen_width // 2, screen_height // 2)
        draw_text('Press Q to Quit', font, black, screen, screen_width // 2, screen_height // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def game_over_screen():
    global score
    while True:
        # Get current frame of the video
        frame = background_video.get_frame(pygame.time.get_ticks() / 1000)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(pygame.transform.scale(frame_surface, (screen_width, screen_height)), (0, 0))

        draw_text('Game Over', font, black, screen, screen_width // 2, screen_height // 2 - 100)
        draw_text(f'Score: {score}', font, black, screen, screen_width // 2, screen_height // 2)
        draw_text('Press R to Retry', font, black, screen, screen_width // 2, screen_height // 2 + 50)
        draw_text('Press Q to Quit', font, black, screen, screen_width // 2, screen_height // 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Main game loop
def game_loop():
    global player_x, player_y, score, timer

    while True:
        # Get current frame of the video
        frame = background_video.get_frame(pygame.time.get_ticks() / 1000)
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(pygame.transform.scale(frame_surface, (screen_width, screen_height)), (0, 0))

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
            player_y += player_speed

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        for trash in trash_list:
            trash.move()
            if trash.rect.colliderect(player_rect):
                score += 10
                trash.y = -30
                trash.x = random.randint(0, screen_width - 30)

        for powerup in powerups:
            if powerup.is_collected(player_rect):
                score += 50
                powerups.remove(powerup)
                powerups.append(PowerUp(random.randint(0, screen_width - 30), random.randint(-100, screen_height - 30)))
        
        if timer <= 0:
            game_over_screen()

        for trash in trash_list:
            trash.draw()
        for powerup in powerups:
            powerup.draw()

        screen.blit(player_image, (player_x, player_y))
        draw_text(f'Score: {score}', font, black, screen, 100, 30)
        draw_text(f'Time: {int(timer)}', font, black, screen, screen_width - 100, 30)
        
        pygame.display.flip()

        timer -= 1 / 30

# Start the game
main_menu()
while True:
    if not game_loop():
        break
