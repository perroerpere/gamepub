import pygame
import sys
import random
import math

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
fuchsia = (255, 0, 255)
silver = (192, 192, 192)
gray = (128, 128, 128)
maroon = (128, 0, 0)
olive = (128, 128, 0)
purple = (128, 0, 128)
teal = (0, 128, 128)
navy = (0, 0, 128)
brown = (150, 75, 0)

background = pygame.image.load("GameBackground.jpg")

width = 1500
height = 1000

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("WohoGaming")
pygame.key.set_repeat(True)

times_hit = 0
health_points = 150
attack_speed = 100
enemy_size = 50
bullet_size = 25
player_damage = 1

score_start = 0
score_behind = 0
score_power = 0
skudd_mengde = 1
enemy_mengde = 5
power_up_scaling = 50
orbital_distance = 200

"powerups"
amount_of_powerups = 5

lifesteal_power_up = 0

trippleshot_power_up = 0

piercing_power_up = 0

total_nuke_power_up = 0

attack_speed_power_up = 0
    #TODO
bombs_power_up = 0
    #TODO
movement_speed_power_up = 0
    #TODO
shield_power_up = 0

higher_range_power_up = 0
    #TODO
"powerups"
"scaling"
smaller_enemy_scaling = 0
    #TODO
bigger_bullet_scaling = 0
    #TODO
player_damage_scaling = 0
    #TODO
"scaling"

def scoreboard():
    font = pygame.font.SysFont("Arial", 26)
    score = font.render("score: " + str(score_start), True, black)
    screen.blit(score, ((width / 2), 50))


def score_check():
    with open("high_score.txt", "r") as file:
        old_score = file.read()
        file.close()
        old_score = int(old_score)
    new_score = score_start
    if new_score >= old_score:
        high_score = new_score
        print(f"You got the new high score with the score of {new_score}, the old high score was {old_score}")
    else:
        high_score = old_score
        print(f"high_score: {old_score}")
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))
        file.close()


def score_check_menu():
    with open("high_score.txt", "r") as file:
        old_score = file.read()
        file.close()
        old_score = int(old_score)
    return old_score


def health_number_text(hp):
    font = pygame.font.SysFont("Arial", 26)
    health_number = font.render("health:" + " " + str(hp), True, black)
    screen.blit(health_number, (10, 70))


def deletesprite(survivor, deleted):
    pygame.sprite.spritecollide(survivor, deleted, True)


def blocksprite(moving, blocking):
    pygame.sprite.spritecollide(moving, blocking, False)


def skyting(retning, right, left):
    global skudd_mengde
    x, y = player.get_pos()
    if skudd_mengde % attack_speed == 0:
        skudd_sprite.add(Skudd(retning, x, y))
        if trippleshot_power_up:
            skudd_sprite.add(Skudd(right, x, y))
            skudd_sprite.add(Skudd(left, x, y))
        skudd_mengde = 1
    skudd_mengde += 1


def addscore(amount):
    global score_behind
    global score_start
    global score_power
    score_start += amount
    score_power += amount
    score_behind += amount


def reset_score():
    global score_behind
    global score_start
    global score_power
    score_start = 0
    score_behind = 0
    score_power = 0


def reload():
    global skudd_mengde
    if skudd_mengde != attack_speed:
        skudd_mengde += 1


def update_sycle(player_x, player_y):
    sprite_nuke.update()
    player_sprite.update()
    sprite_powerups.update()
    sprite_enemy.update(player_x, player_y)
    player.update()
    skudd_sprite.update()
    orbital_sprite.update(player_x, player_y)


def losegame():
    global times_hit
    global enemy_mengde
    print(f"you got a score of {score_start}")
    score_check()
    times_hit = 0
    reset_score()
    for i in sprite_enemy:
        sprite_enemy.remove(i)
    enemy_mengde = 5
    main_menu()


def main_menu():
    menu = True
    high_score = score_check_menu()

    while menu:
        screen.blit(background, (0, 0))
        font = pygame.font.SysFont("Arial", 50)
        small_font = pygame.font.SysFont("Arial", 30)

        title_text = font.render("WohoGaming - Main Menu", True, black)
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 100))

        high_score_text = small_font.render(f"High Score: {high_score}", True, black)
        screen.blit(high_score_text, (width // 2 - high_score_text.get_width() // 2, 200))

        start_button = pygame.Rect(width // 2 - 100, 300, 200, 50)
        pygame.draw.rect(screen, green, start_button)
        start_text = small_font.render("Start Game", True, black)
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, 310))

        quit_button = pygame.Rect(width // 2 - 100, 400, 200, 50)
        pygame.draw.rect(screen, red, quit_button)
        quit_text = small_font.render("Quit", True, black)
        screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, 410))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    menu = False
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mesteren.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.speed = 1

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right:
            self.rect.x += self.speed
        if self.moving_left:
            self.rect.x -= self.speed
        if self.moving_up:
            self.rect.y -= self.speed
        if self.moving_down:
            self.rect.y += self.speed

    def get_pos(self):
        return player.rect.x,player.rect.y

    def update_image_shield(self):
        self.image = pygame.image.load("mesteren_shield.png")

    def update_image_origin(self):
        self.image = pygame.image.load("mesteren.png")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.speed = 1
        self.spawn = random.randrange(1,5)
        self.hitpoints = 2
        #TODO
        self.max_hitpoints = 2
        #TODO

        if self.spawn == 1:
            self.rect.x = (0 - self.rect.width)
            self.rect.y = random.randrange(0, height - self.image.get_size()[1])

        if self.spawn == 2:
            self.rect.x = random.randrange(0, width - self.image.get_size()[1])
            self.rect.y = (0 - self.rect.height)

        if self.spawn == 3:
            self.rect.x = (width + self.rect.width)
            self.rect.y = random.randrange(0,height - self.image.get_size()[1])

        if self.spawn == 4:
            self.rect.x = random.randrange(0, width - self.image.get_size()[1])
            self.rect.y = (height + self.rect.height)

    def update(self, player_x, player_y):

        if self.rect.x > player_x+45:
            self.rect.x -= self.speed
        else: self.rect.x += self.speed

        if self.rect.y > player_y+45:
            self.rect.y -= self.speed
        else: self.rect.y += self.speed

        if self.hitpoints <= 0:
            self.kill()
            addscore(1)


    def draw_health_bar(self):
        bar_width = self.rect.width
        bar_height = 50
        fill = (self.hitpoints/self.max_hitpoints) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + 2, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + 2, fill, bar_height)

        pygame.draw.rect(screen, (red), fill_rect)
        pygame.draw.rect(screen, (white), outline_rect, 1)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = screen_height
        self.rect.y = screen_width

    def update(self):
        pass


class Boarders(pygame.sprite.Sprite):
    def __init__(self, brd_width, brd_height, brd_x, brd_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((brd_width, brd_height))
        self.image.fill(brown)
        self.rect = self.image.get_rect()
        self.rect.x = brd_x
        self.rect.y = brd_y


class Nuke(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        amount = len(sprite_enemy)
        kill_all_enemy = pygame.sprite.spritecollide(self, sprite_enemy, True)
        if kill_all_enemy:
            addscore(amount)

        kill_self = pygame.sprite.spritecollide(self, player_sprite, False)
        if kill_self:
            self.kill()


class Hitpoints(pygame.sprite.Sprite):
    def __init__(self, hits):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((health_points-hits, 20))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 100


class Skudd(pygame.sprite.Sprite):
    def __init__(self, retning, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((bullet_size,bullet_size))
        self.speed = 4
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x + 40
        self.rect.y = y + 40
        self.retning = retning

        #TODO legge til skuddlengde for range

    def update(self):
        if self.retning == 1:
            self.rect.x -= self.speed

        if self.retning == 5:
            self.rect.x -= self.speed
            self.rect.y -= self.speed/3

        if self.retning == 6:
            self.rect.x -= self.speed
            self.rect.y += self.speed/3

        if self.retning == 2:
            self.rect.x += self.speed

        if self.retning == 7:
            self.rect.x += self.speed
            self.rect.y += self.speed/3

        if self.retning == 8:
            self.rect.x += self.speed
            self.rect.y -= self.speed/3

        if self.retning == 3:
            self.rect.y += self.speed

        if self.retning == 9:
            self.rect.x += self.speed/3
            self.rect.y -= self.speed

        if self.retning == 10:
            self.rect.x -= self.speed/3
            self.rect.y -= self.speed

        if self.retning == 4:
            self.rect.y -= self.speed

        if self.retning == 11:
            self.rect.x -= self.speed/3
            self.rect.y += self.speed

        if self.retning == 12:
            self.rect.x += self.speed/3
            self.rect.y += self.speed

        kill_enemy = pygame.sprite.spritecollide(self, sprite_enemy, True)
        if kill_enemy:
            addscore(1)
            global times_hit
            global piercing_power_up
            if piercing_power_up == 0:
                self.kill()
            if lifesteal_power_up == 1 and times_hit > 0:
                times_hit -= 1


class Orbital(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((bullet_size,bullet_size))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.angle = 0
        self.radius = 0
        self.speed = 0

    def update(self, player_x, player_y):
        self.radius = orbital_distance
        self.speed = 5 / orbital_distance
        self.angle += self.speed
        self.rect.x = (player_x + 50) + self.radius * math.cos(self.angle) - self.rect.width / 2
        self.rect.y = (player_y + 50) + self.radius * math.sin(self.angle) - self.rect.height / 2

        kill_enemy = pygame.sprite.spritecollide(self, sprite_enemy, True)
        if kill_enemy:
            addscore(1)




class Powerups(pygame.sprite.Sprite):
    def __init__(self, power):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.power = power
        if self.power == 1:
            self.image.fill(green)
        if self.power == 2:
            self.image.fill(navy)
        if self.power == 3:
            self.image.fill(fuchsia)
        if self.power == 4:
            self.image.fill(yellow)
        if self.power == 5:
            self.image.fill(teal)

        self.rect = self.image.get_rect()
        self.speed = 2
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = 0

    def update(self):
        self.rect.y += self.speed

        get_power_up = pygame.sprite.spritecollide(self, player_sprite, False)

        if get_power_up:
            self.kill()
            global trippleshot_power_up
            if self.power == 1:
                trippleshot_power_up += 2000

            if self.power == 2:
                global piercing_power_up
                piercing_power_up = 1

            if self.power == 3:
                global lifesteal_power_up
                if lifesteal_power_up > 0:
                    global times_hit
                    times_hit = 0
                lifesteal_power_up = 1

            if self.power == 4:
                global total_nuke_power_up
                total_nuke_power_up = 1

            if self.power == 5:
                global shield_power_up
                shield_power_up += 1500
                player.update_image_shield()


boarder_sprite1 = pygame.sprite.Group()

boarder_sprite2 = pygame.sprite.Group()

boarder_sprite3 = pygame.sprite.Group()

boarder_sprite4 = pygame.sprite.Group()

player_sprite = pygame.sprite.Group()

skudd_sprite = pygame.sprite.Group()

orbital_sprite = pygame.sprite.Group()

sprite_enemy = pygame.sprite.Group()

sprite_powerups = pygame.sprite.Group()

sprite_nuke = pygame.sprite.Group()

player = Player()
player_sprite.add(player)

'#boarders'
boarder1 = Boarders(width, 200, 0, height - 25)
boarder_sprite1.add(boarder1)

boarder2 = Boarders(width, 25, 0, 0)
boarder_sprite2.add(boarder2)

boarder3 = Boarders(25, height, 0, 0)
boarder_sprite3.add(boarder3)

boarder4 = Boarders(25, height, width-25, 0)
boarder_sprite4.add(boarder4)
'#boarders'

orbital_sprite.add(Orbital())

main_menu()

'#game loop'
game_loop = True

while game_loop:
    if total_nuke_power_up == 1:
        sprite_nuke.add(Nuke())
        total_nuke_power_up = 0

    '#health'
    health_sprite = pygame.sprite.Group()
    health = Hitpoints(times_hit)
    health_sprite.add(health)
    '#health'

    if len(sprite_enemy) < enemy_mengde:
        sprite_enemy.add(Enemy())

    if score_behind >= 33:
        enemy_mengde += 1
        score_behind -= 33

    if score_power >= power_up_scaling:
        sprite_powerups.add(Powerups(random.randrange(1,amount_of_powerups+1)))
        score_power -= power_up_scaling

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        player.moving_right = True
    else:
        player.moving_right = False

    if keys[pygame.K_a]:
        player.moving_left = True
    else:
        player.moving_left = False

    if keys[pygame.K_w]:
        player.moving_up = True
    else:
        player.moving_up = False

    if keys[pygame.K_s]:
        player.moving_down = True
    else:
        player.moving_down = False

    if keys[pygame.K_LEFT]:
        skyting(1,5,6)
    else:
        reload()

    if keys[pygame.K_RIGHT]:
        skyting(2,7,8)
    else:
        reload()

    if keys[pygame.K_DOWN]:
        skyting(3,11,12)
    else:
        reload()

    if keys[pygame.K_UP]:
        skyting(4,9,10)
    else:
        reload()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    get_hit = pygame.sprite.spritecollide(player, sprite_enemy, False)
    if get_hit and shield_power_up <= 0:
        pass
        #times_hit += 1

    if times_hit == (health_points+1):
        losegame()


    if trippleshot_power_up > 0 and score_start < 1000:
        trippleshot_power_up -= 1

    if shield_power_up > 0:
        shield_power_up -= 1
        if shield_power_up == 0:
            player.update_image_origin()

    deletesprite(boarder1, skudd_sprite)
    deletesprite(boarder2, skudd_sprite)
    deletesprite(boarder3, skudd_sprite)
    deletesprite(boarder4, skudd_sprite)

    if pygame.sprite.spritecollide(player, boarder_sprite1, False):
        player.moving_down = False

    if pygame.sprite.spritecollide(player, boarder_sprite2, False):
        player.moving_up = False

    if pygame.sprite.spritecollide(player, boarder_sprite3, False):
        player.moving_left = False

    if pygame.sprite.spritecollide(player, boarder_sprite4, False):
        player.moving_right = False

    '#updates'
    player_x, player_y = player.get_pos()

    update_sycle(player_x, player_y)
    '#updates'

    '#draw'
    sprite_nuke.draw(screen)
    screen.blit(background, (0, 0))
    sprite_powerups.draw(screen)
    boarder_sprite1.draw(screen)
    boarder_sprite2.draw(screen)
    boarder_sprite3.draw(screen)
    boarder_sprite4.draw(screen)
    player_sprite.draw(screen)
    skudd_sprite.draw(screen)
    sprite_enemy.draw(screen)
    health_sprite.draw(screen)
    orbital_sprite.draw(screen)
    scoreboard()
    health_number_text(health_points-times_hit)
    '#draw'

    pygame.display.flip()
    '#game loop'