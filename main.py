import pygame
import random
from asset_loader import load_images, load_image_icon, load_icon
from audio_loader import load_sounds
from abc import ABC, abstractmethod

pygame.init()
pygame.mixer.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (153, 255, 0)

pygame.display.set_caption('Flappy Clash')
icon = load_icon()
pygame.display.set_icon(icon)

def resize_image(image, new_width, new_height):
    return pygame.transform.smoothscale(image, (new_width, new_height))

background_image, bird_img, zeus_img, pipe_img, bullet_img, zeus_bullet_img, how_to_play_img, thor_img= load_images(screen_width, screen_height)
pause_image, paused_image, quit_image, restart_image, gameover_image, title_image, start_exit_image = load_image_icon(resize_image)

font = pygame.font.Font(None, 36)
sounds = load_sounds()

def play_sound(sounds, sound_key, loop=-1):
    if sound_key == "music":
        pygame.mixer.music.load(sounds[sound_key])
        pygame.mixer.music.play(loop)
    else:
        sounds[sound_key].play()

play_sound(sounds, "music", loop=-1)

class Bird:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.y_change = 0
        self.hp = 100
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.gravity = 0.6
        self.jump_power = -10

    def jump(self):
        self.y_change = self.jump_power

    def update(self):
        self.y_change += self.gravity
        self.y += self.y_change

    def draw(self, surface):
        rotated = pygame.transform.rotate(self.image, 30 if self.y_change < 0 else -30)
        surface.blit(rotated, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Pipe:
    def __init__(self, x, height, image, gap, screen_height):
        self.x = x
        self.height = height
        self.image = image
        self.gap = gap
        self.passed = False
        self.width = image.get_width()
        self.screen_height = screen_height

    def update(self, speed):
        self.x += speed

    def draw(self, surface):
        # Bottom pipe
        surface.blit(self.image, (self.x, self.height + self.gap))
        # Top pipe (flipped)
        pipe_top = pygame.transform.flip(self.image, False, True)
        surface.blit(pipe_top, (self.x, self.height - self.image.get_height()))

    def get_top_rect(self):
        return pygame.Rect(self.x, self.height - self.image.get_height(), self.width, self.image.get_height())

    def get_bottom_rect(self):
        return pygame.Rect(self.x, self.height + self.gap, self.width, self.image.get_height())

class Enemy(ABC):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.hp = 100
        self.lasers = []
        self.width = image.get_width()
        self.height = image.get_height()
        self.appeared = False

    def appear(self, hp):
        self.y = -self.height
        self.hp = hp
        self.appeared = True

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def shoot(self, laser_img):
        pass

    def draw(self, surface):
        if self.appeared:
            surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Zeus(Enemy):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.y_change = 3

    def update(self):
        if self.appeared:
            if self.y < screen_height // 2 - 125:
                self.y += self.y_change
            elif self.hp <= 0:
                self.y += 10

    def shoot(self, laser_img):
        self.lasers.append(ZeusLaser(self.x, self.y + 125, laser_img))

class Bullet:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()

    def update(self):
        self.x += 10

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class ZeusLaser:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()

    def update(self):
        self.x -= 15

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Thor(Zeus):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def shoot(self, laser_img):
        offsets = [-30, 0, 30]
        for offset in offsets:
            self.lasers.append(ThorLaser(self.x, self.y + 125, laser_img, offset))

class ThorLaser(ZeusLaser):
    def __init__(self, x, y, image, angle_offset):
        super().__init__(x, y, image)
        self.angle_offset = angle_offset  # sudut penyebaran

    def update(self):
        # Bergerak ke kiri dan sedikit ke atas/bawah sesuai angle
        self.x -= 15
        self.y += self.angle_offset * 0.05  # atur 0.05 agar tidak terlalu miring

def show_score(score):
    text = font.render("SCORE: " + str(score), True, white)
    screen.blit(text, [10, 10])

def draw_hp_bar(x, y, hp):
    bar_width = 100
    bar_height = 10
    fill_width = (hp / 100) * bar_width
    fill = pygame.Rect(x, y, fill_width, bar_height)
    border = pygame.Rect(x, y, bar_width, bar_height)
    pygame.draw.rect(screen, red, fill)
    pygame.draw.rect(screen, black, border, 2)

def draw_zeus_hp_bar(hp, max_hp):
    bar_width = 300
    bar_height = 20
    fill_width = (hp / max_hp) * bar_width
    fill = pygame.Rect(screen_width - 350, 20, fill_width, bar_height)
    border = pygame.Rect(screen_width - 350, 20, bar_width, bar_height)
    pygame.draw.rect(screen, yellow, fill)
    pygame.draw.rect(screen, black, border, 2)

def show_start_screen():
    screen.blit(background_image, (0, 0))
    title_x = (screen_width - title_image.get_width()) // 2
    title_y = screen_height // 18
    screen.blit(title_image, (title_x, title_y))
    start_exit_x = (screen_width - start_exit_image.get_width()) // 2
    start_exit_y = screen_height // 2.2
    screen.blit(start_exit_image, (start_exit_x, start_exit_y))
    pygame.display.update()

def show_how_to_play_screen():
    screen.blit(how_to_play_img, (0, 0))
    pygame.display.update()

def show_pause_screen():
    screen.blit(paused_image, [screen_width // 2 - paused_image.get_width() // 2, screen_height // 4.25])
    pygame.display.update()

def show_game_over_screen():
    play_sound(sounds, "gameover")
    screen.fill(black)
    go_x = (screen_width - gameover_image.get_width()) // 2
    go_y = screen_height // 10
    screen.blit(gameover_image, (go_x, go_y))
    randex_x = (screen_width - restart_image.get_width()) // 2
    randex_y = screen_height // 1.85
    screen.blit(restart_image, (randex_x, randex_y))
    pygame.display.update()
    pygame.mixer.music.stop()

def wait_for_next(main_game_func):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    pygame.mixer.music.play(-1)
                    main_game_func()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def main_game():
    bird = Bird(50, 300, bird_img)
    pipes = [Pipe(screen_width + i * 300, random.randint(150, 450), pipe_img, 300, screen_height) for i in range(3)]
    enemy_types = [Zeus, Thor]
    enemy_images = [zeus_img, thor_img]
    enemy_index = 0
    enemy = enemy_types[enemy_index](screen_width - 310, -enemy_images[enemy_index].get_height(), enemy_images[enemy_index])
    bullets = []
    score = 0
    pipe_x_change = -6
    pipes_passed = 0
    zeus_defeated_count = 0
    running = True
    paused = False
    clock = pygame.time.Clock()

    while running:
        if not paused:
            screen.blit(background_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                        play_sound(sounds, "woosh")
                    if event.key == pygame.K_v:
                        if enemy.appeared and enemy.y >= screen_height // 2 - 125:
                            bullets.append(Bullet(bird.x + 50, bird.y + 25, bullet_img))
                            play_sound(sounds, "shoot")
                    if event.key == pygame.K_p:
                        paused = True

            # Bird update
            bird.update()
            if bird.y < -50 or bird.y > screen_height:
                running = False
                show_game_over_screen()
                wait_for_next(main_game)
                break

            # Pipes update
            for pipe in pipes:
                pipe.update(pipe_x_change)
            pipes = [pipe for pipe in pipes if pipe.x > -pipe.width]
            if pipes[-1].x < screen_width - 300:
                pipes.append(Pipe(screen_width, random.randint(150, 450), pipe_img, 300, screen_height))

            # Collision bird-pipe
            for pipe in pipes:
                if bird.get_rect().colliderect(pipe.get_top_rect()) or bird.get_rect().colliderect(pipe.get_bottom_rect()):
                    bird.hp -= 20  # Atur pengurangan HP sesuai keinginan
                    if bird.hp <= 0:
                        running = False
                        show_game_over_screen()
                        wait_for_next(main_game)
                        break
                if pipe.x + pipe.width < bird.x and not pipe.passed:
                    pipe.passed = True
                    pipes_passed += 1
                    score += 1

            # Enemy muncul setiap 10 pipa dilewati, selang-seling Zeus/Thor
            if pipes_passed > 0 and pipes_passed % 10 == 0 and not enemy.appeared:
                enemy = enemy_types[enemy_index](screen_width - 310, -enemy_images[enemy_index].get_height(), enemy_images[enemy_index])
                enemy.appear(100)
                play_sound(sounds, "zeus_coming", loop=-1)
                pipes_passed = 0
                enemy_index = (enemy_index + 1) % len(enemy_types)  # <-- index naik setelah musuh dibuat

            enemy.update()
            enemy.draw(screen)

            # Zeus laser logic
            if enemy.appeared and enemy.y >= screen_height // 2 - 125 and enemy.hp > 0:
                if isinstance(enemy, Thor):
                    # Thor menembak 3 laser sekaligus
                    laser_probability = 60
                    if random.randint(1, laser_probability) == 1:
                        enemy.shoot(zeus_bullet_img)
                else:
                    # Zeus menembak 1 laser
                    laser_probability = 60
                    if random.randint(1, laser_probability) == 1:
                        enemy.lasers.append(ZeusLaser(enemy.x, enemy.y + 125, zeus_bullet_img))
                        play_sound(sounds, "thunder", loop=-1)

                for laser in enemy.lasers[:]:
                    laser.update()
                    laser.draw(screen)
                    if laser.x < 0:
                        enemy.lasers.remove(laser)
                    elif laser.get_rect().colliderect(bird.get_rect()):
                        bird.hp -= 10
                        enemy.lasers.remove(laser)
                        if bird.hp <= 0:
                            running = False
                            show_game_over_screen()
                            wait_for_next(main_game)
                            break

                draw_zeus_hp_bar(enemy.hp, 100 + 50 * zeus_defeated_count)

            if enemy.hp <= 0 and enemy.y > screen_height:
                enemy.appeared = False
                zeus_defeated_count += 1

            # Bullets logic
            for bullet in bullets[:]:
                bullet.update()
                bullet.draw(screen)
                if enemy.appeared and bullet.get_rect().colliderect(enemy.get_rect()):
                    enemy.hp -= 10
                    play_sound(sounds, "ouch")
                    bullets.remove(bullet)
                elif bullet.x > screen_width:
                    bullets.remove(bullet)

            # Draw everything
            bird.draw(screen)
            for pipe in pipes:
                pipe.draw(screen)
            show_score(score)
            draw_hp_bar(10, 40, bird.hp)
            screen.blit(pause_image, [screen_width - pause_image.get_width() - 10, 10])
            pygame.display.update()
            clock.tick(60)
        else:
            show_pause_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    if event.key == pygame.K_q:
                        running = False

# Main menu loop
show_start_screen()
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                waiting = False
                main_game()
            elif event.key == pygame.K_2:
                waiting = False
                pygame.quit()
                quit()
            elif event.key == pygame.K_3:
                waiting = False
                show_how_to_play_screen()
                how_to_play_waiting = True
                while how_to_play_waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            how_to_play_waiting = False
                            pygame.quit()
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                how_to_play_waiting = False
                                show_start_screen()
                                waiting = True
