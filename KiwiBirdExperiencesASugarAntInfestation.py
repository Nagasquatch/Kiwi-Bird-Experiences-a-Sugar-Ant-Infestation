#Import library
import pygame
from pygame.locals import *

import random

j = 1.5
 
class Player(pygame.sprite.Sprite):
    #def __init__(self):
        #super(Player, self).__init__()
        #self.surf = pygame.Surface((25, 25))
        #self.surf.fill((255, 255, 255))
        #self.rect = self.surf.get_rect()

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('final.png').convert_alpha()
        self.rect = self.surf.get_rect()
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-j)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,j)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-j,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(j,0)

        #Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 100:
            self.rect.top = 100
        elif self.rect.bottom >= 500:
            self.rect.bottom = 500

class Opponent(pygame.sprite.Sprite):
    def __init__(self):
        super(Opponent, self).__init__()
        self.surf = pygame.Surface((5,20))
        self.surf.fill((0,0,0))
        dog = random.randint(0,1)
        if dog == 1:
            dinosaur = -20
            direction = 1
        elif dog == 0:
            dinosaur = 620
            direction = 0
        self.rect = self.surf.get_rect(center=(random.randint(0,800),dinosaur))
        self.speed = random.randint(0,5)

    def update(self):
        direction = random.randint(0,1)
        if direction == 1:
            self.rect.move_ip(random.randint(-1,1),self.speed)
        elif direction == 0:
            self.rect.move_ip(random.randint(-1,1),-self.speed)
        if self.rect.right < 0:
                self.kill()
                
#Initialize pygame modules
pygame.init()
  
#Create your screen
screen = pygame.display.set_mode((800, 600))
 
#Instantiate our player; right now he's just a rectangle
player = Player()

#Instantiate our opponents; right now they're just rectangles
opponent = Opponent()

#Set background color
background = pygame.Surface(screen.get_size())
background.fill((255,255,255,))

#Create Groups and add game objects
players = pygame.sprite.Group()
opponents = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#Create opponent event
ADDOPPONENT = pygame.USEREVENT + 1

#Set timer for opponent ever to occur every 250ms
pygame.time.set_timer(ADDOPPONENT, 250)

#Create the surface and pass in a tuple with its length and width
#surf = pygame.Surface((75, 75))
 
#Give the surface a color to differentiate it from the background
#surf.fill((255, 255, 255))
#rect = surf.get_rect()

health = 300

running = True

#create game clock, create variable for frames per second (FPS), and get starting time
clock = pygame.time.Clock()
fps = 1000

while running:

    #set game FPS
    clock.tick(fps)
     
    #For loop through the event queue
    for event in pygame.event.get():
        #Check for KEYDOWN event
        #KEYDOWN is a constant defined in pygame.locals, imported earlier
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
            print("Escape")
        #Check for QUIT event; if QUIT, set running to false
        elif event.type == QUIT:
            running = False
            print("QUIT")
        #Check for Opponent event; if ADDOPPONENT, create and add opponent
        elif event.type == ADDOPPONENT:
            new_opponent = Opponent()
            opponents.add(new_opponent)
            all_sprites.add(new_opponent)

    #Draw background
    screen.blit(background,(0,0))

    #Get pressed keys
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    #Update opponents' postition
    opponents.update()

    #Draw surf onto screen at coordinates x:400, y:300"
    #screen.blit(surf, (400, 300))
    #screen.blit(player.surf, (400, 300))
    #screen.blit(player.surf,player.rect)

    basicfont=pygame.font.SysFont(None,20)
    text=basicfont.render("Health: " + str(health),True,(255,0,0))
    screen.blit(text,(30,30))
    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if health > 270:
        j=1.4
    elif health > 240:
        j=1.3
    elif health > 210:
        j=1.2
    elif health > 180:
        j=1.1
    elif health > 150:
        j=1
    elif health > 120:
        j=0.9
    elif health > 90:
        j=0.8
    elif health > 60:
        j=0.7
    elif health > 30:
        j=0.6
    elif health > 0:
        j=0.5

    #Kill player if player and opponent collide
    if pygame.sprite.spritecollideany(player, opponents):
        health-=1
        if health == 0:
            running = False
            player.kill()
            print("You be eated.")

    pygame.display.flip()
    
#Exit the Game
pygame.quit()
