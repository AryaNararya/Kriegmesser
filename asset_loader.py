import pygame
import os

ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

def load_images(screen_width, screen_height):
    background_image = pygame.image.load(os.path.join(ASSET_DIR, "gambar", "background.png"))
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    bird_image = pygame.image.load(os.path.join(ASSET_DIR, "gambar", "Blitz.png"))
    bird_image = pygame.transform.scale(bird_image, (60, 50))
    zeus_image = pygame.image.load(os.path.join(ASSET_DIR, "gambar", "zeus.png"))
    thor_image = pygame.image.load(os.path.join(ASSET_DIR, "gambar", "thor.png"))
    thor_image = pygame.transform.scale(thor_image, (350, 350))
    zeus_image = pygame.transform.scale(zeus_image, (350, 350))
    pipe_image = pygame.image.load(os.path.join(ASSET_DIR, "gambar", "pipe.png"))
    pipe_image = pygame.transform.scale(pipe_image, (70, screen_height))
    bullet_image = pygame.image.load(os.path.join(ASSET_DIR, "gambar", "peluru.png"))
    bullet_image = pygame.transform.scale(bullet_image, (20, 10))
    zeus_bullet_image = pygame.image.load(os.path.join(ASSET_DIR, "gambar", "pz.png"))
    zeus_bullet_image = pygame.transform.scale(zeus_bullet_image, (30, 30))
    how_to_play_image = pygame.image.load(os.path.join(ASSET_DIR, "gambar", "how_to_play_screen.png"))
    how_to_play_image = pygame.transform.scale(how_to_play_image, (screen_width, screen_height))
    return background_image, bird_image, zeus_image, pipe_image, bullet_image, zeus_bullet_image, how_to_play_image,thor_image

def load_image_icon(resize_image):
    pause_image = pygame.image.load(os.path.join(ASSET_DIR, "caption", "pause.png"))
    paused_image = pygame.image.load(os.path.join(ASSET_DIR, "caption", "paused.png"))
    quit_image = pygame.image.load(os.path.join(ASSET_DIR, "caption", "quit.png"))
    restart_image = pygame.image.load(os.path.join(ASSET_DIR, "caption", "randex.png"))
    gameover_image = pygame.image.load(os.path.join(ASSET_DIR, "caption", "gameover.png"))
    title_image = pygame.image.load(os.path.join(ASSET_DIR, "caption", "flappy_clash.png"))
    start_exit_image = pygame.image.load(os.path.join(ASSET_DIR, "caption", "awal.png"))
    
    pause_image = resize_image(pause_image, 250, 50) 
    paused_image = resize_image(paused_image, 500, 200) 
    quit_image = resize_image(quit_image, 300, 100) 
    restart_image = resize_image(restart_image, 600, 200) 
    gameover_image = resize_image(gameover_image, 1000, 300)
    title_image = pygame.transform.scale(title_image, (1000, 300))
    start_exit_image = pygame.transform.scale(start_exit_image, (600, 300))
    
    return pause_image, paused_image, quit_image, restart_image, gameover_image, title_image, start_exit_image

def load_icon():
    return pygame.image.load(os.path.join(ASSET_DIR, "gambar", "Blitz.png"))