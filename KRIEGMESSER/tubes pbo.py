import pygame


# Constants
SCREEN_SIZE = (800, 600)
SCREEN_COLOR = (200, 200, 200)
PLATFORM_COLOR = (100, 200, 100)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Kriegmesser')
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize components
        self.player = Player(300, 0)
        self.map = Map()
        self.ui = UI()

    def start(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(120)

        pygame.quit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.player.handle_input()

    def update(self):
        self.player.update(self.map.platforms, self.map.collectibles)

    def draw(self):
        # Draw background
        self.screen.fill(SCREEN_COLOR)

        # Draw platforms
        for platform in self.map.platforms:
            pygame.draw.rect(self.screen, PLATFORM_COLOR, platform)

        # Draw collectibles
        for collectible in self.map.collectibles:
            self.screen.blit(collectible.image, collectible.rect.topleft)

        # Draw player
        self.screen.blit(self.player.image, (self.player.x, self.player.y))

        # Update display
        pygame.display.flip()


class Player:
    def __init__(self, x, y):
        self.x = 300
        self.y = y
        self.speed = 0
        self.acceleration = 0.1  # Gravity
        self.image = pygame.image.load('CHARACTER/Soldier-Walk/knightwalk_0.png')
        self.rect = pygame.Rect(self.x, self.y, 60, 60)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= 2  # Move left
        if keys[pygame.K_d]:
            self.x += 2  # Move right
        if keys[pygame.K_w]:
            self.speed = -2  # Jump

    def update(self, platforms, collectibles):
        # Horizontal movement
        new_rect = self.rect.move(self.x - self.rect.x, 0)
        if not any(platform.colliderect(new_rect) for platform in platforms):
            self.rect.x = self.x

        # Vertical movement
        self.speed += self.acceleration
        new_rect = self.rect.move(0, self.speed)
        if not any(platform.colliderect(new_rect) for platform in platforms):
            self.rect.y += self.speed
        else:
            self.speed = 0

        # Update position
        self.x, self.y = self.rect.topleft

        # Collect collectibles
        for collectible in collectibles[:]:
            if self.rect.colliderect(collectible.rect):
                collectibles.remove(collectible)
                collectible.apply_effect(self)
    def stat(self):
        # Placeholder for stat display
        pass

class Enemy:
    def __init__(self, health, armor, attack):
        self.__health = health            
        self.__armor = armor
        self.__attack = attack

    def chase(self, player):
        # Chase logic
        pass

    def attack(self, player):
        # Attack logic
        pass

    def take_damage(self, damage):
        # Damage logic
        pass
    
class MagicalSwordsman(Enemy):
    def attack(self, player):
        # Magical attack logic
        pass
    

class PhysicalSwordsman(Enemy):
    def attack(self, player):
        # Physical attack logic
        pass

class Map:
    def __init__(self):
        self.platforms = [
            pygame.Rect(100, 300, 400, 50),  # Middle
            pygame.Rect(100, 250, 50, 50),  # Left
            pygame.Rect(450, 250, 50, 50),  # Right
        ]
        self.collectibles = [
            Collectible(100, 200, 'collectible/sprite_0.png', {"health": 5, "magic armor": 10}),
        ]


class Collectible:
    def __init__(self, x, y, image_path, effects):
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect(x, y, 32, 32)
        self.effects = effects

    def apply_effect(self, player):
        # Apply effects to the player
        for stat, value in self.effects.items():
            print(f"Increasing {stat} by {value}")


class UI:
    def __init__(self):
        pass

    def render_stat(self):
        pass


# Run the game
if __name__ == "__main__":
    game = Game()
    game.start()