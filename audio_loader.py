import pygame
import os

ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "audio")

def load_sounds():
    sounds = {
        "music": os.path.join(ASSET_DIR, "sound.mp3"),
        "zeus_coming": pygame.mixer.Sound(os.path.join(ASSET_DIR, "zeuscoming.mp3")),
        "woosh": pygame.mixer.Sound(os.path.join(ASSET_DIR, "woosh.mp3")),
        "gameover": pygame.mixer.Sound(os.path.join(ASSET_DIR, "gameover.mp3")),
        "shoot": pygame.mixer.Sound(os.path.join(ASSET_DIR, "shoot.mp3")),
        "thunder": pygame.mixer.Sound(os.path.join(ASSET_DIR, "thunder.mp3")),
        "ouch": pygame.mixer.Sound(os.path.join(ASSET_DIR, "ouch.mp3")),
    }
    return sounds