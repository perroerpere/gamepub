import pygame
import sys
import random

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lime = (0, 255, 0)
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
enemy_size = 100
bullet_size = 25
player_damage = 1

score_start = 0
score_behind = 0
score_power = 0
skudd_mengde = 1
enemy_mengde = 5

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

'#score'
def health_number_text(hp):
    font = pygame.font.SysFont("Arial", 26)
    health_number = font.render("health:" + " " + str(hp), True, black)
    screen.blit(health_number, (10, 70))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mesteren.png")
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right:
            self.rect.x += 2
        if self.moving_left:
            self.rect.x -= 2
        if self.moving_up:
            self.rect.y -= 2
        if self.moving_down:
            self.rect.y += 2

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
        self.rect = self.image.get_rect()
        self.speed = random.randrange(1, 4)
        self.spawn = random.randrange(1,5)
        self.hitpoints = 2

        #TODO gi fiender health points.
        #TODO gjøre at de ikke kan spawne halveis inni veggen
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

    def update(self):
        if self.spawn == 1:
            self.rect.x += self.speed
            if self.rect.x >= width:
                sprite_enemy.remove(self)

        if self.spawn == 2:
            self.rect.y += self.speed
            if self.rect.y >= height:
                sprite_enemy.remove(self)

        if self.spawn == 3:
            self.rect.x -= self.speed
            if self.rect.x <= 0:
                sprite_enemy.remove(self)

        if self.spawn == 4:
            self.rect.y -= self.speed
            if self.rect.y <= 0:
                sprite_enemy.remove(self)

        if self.hitpoints <= 0:
            self.kill()
            addscore(1)



class Boarders(pygame.sprite.Sprite):
    def __init__(self, brd_width, brd_height, brd_x, brd_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((brd_width, brd_height))
        self.image.fill(red)
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
        self.speed = 8
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


class Powerups(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.type = type
        if self.type == 1:
            self.image.fill(green)
        if self.type == 2:
            self.image.fill(navy)
        if self.type == 3:
            self.image.fill(fuchsia)
        if self.type == 4:
            self.image.fill(yellow)
        if self.type == 5:
            self.image.fill(teal)

        self.rect = self.image.get_rect()
        self.speed = 3
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = 0

    def update(self):
        self.rect.y += self.speed

        get_power_up = pygame.sprite.spritecollide(self, player_sprite, False)

        if get_power_up:
            self.kill()
            global trippleshot_power_up
            if self.type == 1:
                trippleshot_power_up += 2000

            if self.type == 2:
                global piercing_power_up
                piercing_power_up = 1

            if self.type == 3:
                global lifesteal_power_up
                if lifesteal_power_up > 0:
                    global times_hit
                    times_hit = 0
                lifesteal_power_up = 1

            if self.type == 4:
                global total_nuke_power_up
                total_nuke_power_up = 1

            if self.type == 5:
                global shield_power_up
                shield_power_up += 1500
                player.update_image_shield()


boarder_sprite1 = pygame.sprite.Group()

boarder_sprite2 = pygame.sprite.Group()

boarder_sprite3 = pygame.sprite.Group()

boarder_sprite4 = pygame.sprite.Group()

player_sprite = pygame.sprite.Group()

skudd_sprite = pygame.sprite.Group()

sprite_enemy = pygame.sprite.Group()

sprite_powerups = pygame.sprite.Group()

sprite_nuke = pygame.sprite.Group()

player = Player()
player_sprite.add(player)

'#boarders'
boarder1 = Boarders(width, 20, 0, 1000)
boarder_sprite1.add(boarder1)

boarder2 = Boarders(width, 20, 0, -20)
boarder_sprite2.add(boarder2)

boarder3 = Boarders(20, height, -20, 0)
boarder_sprite3.add(boarder3)

boarder4 = Boarders(20, height, 1500, 0)
boarder_sprite4.add(boarder4)
'#boarders'

for fi in range(5):
    enemy = Enemy()
    sprite_enemy.add(enemy)


def deletesprite(survivor, deleted):
    pygame.sprite.spritecollide(survivor, deleted, True)


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


def reload():
    global skudd_mengde
    if skudd_mengde != attack_speed:
        skudd_mengde += 1

'#game loop'
game_loop = True
menu = False

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

    if score_power >= 50:
        sprite_powerups.add(Powerups(random.randrange(1,amount_of_powerups+1)))
        score_power -= 50

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
        times_hit += 1

    if times_hit == (health_points+1):
        print(f"you got a score of {score_start}")
        score_check()
        sys.exit()

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

    stop_move_down = pygame.sprite.spritecollide(player, boarder_sprite1, False)
    if stop_move_down:
        player.moving_down = False
    stop_move_up = pygame.sprite.spritecollide(player, boarder_sprite2, False)
    if stop_move_up:
        player.moving_up = False

    stop_move_left = pygame.sprite.spritecollide(player, boarder_sprite3, False)
    if stop_move_left:
        player.moving_left = False

    stop_move_right = pygame.sprite.spritecollide(player, boarder_sprite4, False)
    if stop_move_right:
        player.moving_right = False

    '#updates'
    sprite_nuke.update()
    player_sprite.update()
    sprite_powerups.update()
    sprite_enemy.update()
    player.update()
    skudd_sprite.update()
    '#updates'

    '#draw'
    sprite_nuke.draw(screen)
    screen.blit(background, (0, 0))
    sprite_powerups.draw(screen)
    player_sprite.draw(screen)
    skudd_sprite.draw(screen)
    sprite_enemy.draw(screen)
    health_sprite.draw(screen)
    scoreboard()
    health_number_text(health_points-times_hit)
    '#draw'

    pygame.display.flip()
    '#game loop'