#Character: https://zerie.itch.io/tiny-rpg-character-asset-pack

import pygame 

#constant variables
SCREEN_SIZE = (800,600)
SCREEN_COLOR = (200,200,200)
PLATFORM_COLOR = (100,200,100)

#init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Kriegmesser')
clock = pygame.time.Clock()

#player
player_image = pygame.image.load('CHARACTER/Soldier-Walk/knightwalk_0.png')
player_x = 300
player_y = 0
player_width = 45 #pixel width
player_height = 60 #pixel height
player_speed = 0
player_acceleration = 0.1 #gravity

#platforms
platforms = [

    # (x, y, width, height)
    #middle
    pygame.Rect(100,300,400,50),
    #left
    pygame.Rect(100,250,50,50),
    #right
    pygame.Rect(450,250,50,50)
]

#collectible
collectible_image = pygame.image.load('collectible/sprite_0.png')
collectible = [
    pygame.Rect(100, 200, 32, 32), #(collectiible x, collectible y, pixel width, pixel height)
]

running = True
while running:
#game loop

    #-----
    #INPUT
    #-----

    #check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    new_player_x = player_x
    new_player_y = player_y

    #player_input
    keys = pygame.key.get_pressed()
    #a left
    if keys[pygame.K_a]:
        new_player_x -= 2 #speed
    #d right
    if keys[pygame.K_d]:
        new_player_x += 2 #speed
    #w jump (if on the ground)
    if keys[pygame.K_w] and player_on_ground:
        player_speed = -4 #jump height
    
    #-----
    #update
    #-----

    #horizontal movement

    new_player_rect = pygame.Rect(new_player_x, player_y, player_width, player_height) # (player x, player y, pixel width, pixel height)
    x_collision = False

    #...check against every platform
    for p in platforms:
        if p.colliderect(new_player_rect):
            x_collision = True
            break

    if x_collision == False:
        player_x = new_player_x

    #vertical movement

    player_speed += player_acceleration
    new_player_y += player_speed

    new_player_rect = pygame.Rect(player_x,new_player_y, player_width, player_height) # (player x, player y, pixel width, pixel height)
    y_collision = False
    player_on_ground = False

    #...check against every platform
    for p in platforms:
        if p.colliderect(new_player_rect):
            y_collision = True
            player_speed = 0
            #if the platform is below the player
            if p[1] > new_player_y:
                #stick the player to the platform
                player_y = p[1] - player_height
                player_on_ground = True
            break

    if y_collision == False:
        player_y = new_player_y

    #collecting collectible
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for c in collectible:
        if c.colliderect(player_rect):
            collectible.remove(c)
            # Increase multiple stats
            stats_to_increase = {
                "health": 5,  # Increment health
                "magic armor": 10,  # Increment score
                "magic damage": 10,  # Increment score
                "phsycal armor": 10,  # Increment score
                "phsycal damage": 10,  # Increment score
            }

    #-----
    #draw
    #-----

    #background
    screen.fill(SCREEN_COLOR)
    #platforms
    for p in platforms:
         pygame.draw.rect(screen, PLATFORM_COLOR, p)

    #collectible
    for c in collectible:
        screen.blit(collectible_image, (c[0], c[1])) #x, y, first and second value from collectible

    #player
    screen.blit(player_image, (player_x, player_y)) 
    #present screen
    pygame.display.flip()
    #clock
    clock.tick(120)

#quit
pygame.quit()
