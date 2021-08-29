import pygame, sys
from pygame.locals import *
pygame.init()
pygame.mixer.init() 

shark = "Shark1.png"
scuba = "diver.png"
background = pygame.image.load("ocean.png")
bottom = pygame.image.load("ground.png")
game_audio = "no_starsmixered.wav"
game_over = "total fail.wav"


background = pygame.transform.scale(background, (600,500))
x = 0


WIDTH = 600
HEIGHT = 600

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) 
WATER = (0, 102, 204)
SAND = (255, 229, 204)

oFont = pygame.font.Font("freesansbold.ttf", 30)
opening = oFont.render("Save Blahaj From The Evil Diver!", True, WHITE)
openRect = opening.get_rect()
openRect.center = ((WIDTH/2, HEIGHT/2))

insFont = pygame.font.Font("freesansbold.ttf", 20) 
instruct = insFont.render("Use the arrow keys to avoid the diver and get to the other side", True, WHITE)
instructRect = instruct.get_rect()
instructRect.center = ((WIDTH/2, (HEIGHT/2)+100))

instruct2 = insFont.render("Press any key to continue", True, WHITE)
instruct2Rect = instruct2.get_rect()
instruct2Rect = ((170, (HEIGHT/2)+ 150))

instruct3 = insFont.render("Click X to exit", True, WHITE)
instruct3Rect = instruct2.get_rect()
instruct3Rect = ((230, HEIGHT/2))

loseFont = pygame.font.Font("freesansbold.ttf", 30) 
lose = loseFont.render("YOU LOST!", True, WHITE)
loseRect = lose.get_rect()
loseRect.center = ((WIDTH/2, (HEIGHT/2)-100))

moreFont = pygame.font.Font("freesansbold.ttf", 20) 
more = moreFont.render("Better Luck Next Time", True, WHITE)
moreRect = more.get_rect()
moreRect.center = ((WIDTH/2, (HEIGHT/2)+100))

winFont = pygame.font.Font("freesansbold.ttf", 90) 
winner = loseFont.render("YOU WON!", True, WHITE)
winnerRect = lose.get_rect()
winnerRect.center = ((WIDTH/2, (HEIGHT/2)-100))


display_window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shark")

fps_clock = pygame.time.Clock() 

class Diver(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(scuba)
        self.image = pygame.transform.scale(self.image, (120, 50))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        

class Ground(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, HEIGHT - 50))
        self.image.fill(SAND)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Shark(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(shark)
        self.image = pygame.transform.scale(self.image,(110, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shark_x = 10
        self.shark_y = 10

    def update(self):

        self.speed_x = 0 
        self.speed_y = 0
        
        key_state = pygame.key.get_pressed() 

        
        if key_state[pygame.K_UP]:
            self.speed_y = -7
            self.speed_x = 5            

        elif key_state[pygame.K_DOWN]:
            self.speed_y = 7
            self.speed_x = 5
        
        if key_state[pygame.K_RIGHT]:
            self.speed_x = 7
            
        if key_state[pygame.K_LEFT]:
            self.speed_x = -7
           
        
        self.rect.x += self.speed_x 
        self.rect.y += self.speed_y
        
        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
        elif self.rect.top <= 280:
            self.rect.top = 280
            
pygame.mixer.music.load(game_audio)
pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(0.80)
runs = True
while runs:
    display_window.fill(WATER)
    display_window.blit(opening, openRect)
    display_window.blit(instruct, instructRect)
    display_window.blit(instruct2, instruct2Rect)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            runs = False
    

all_sprites = pygame.sprite.Group() 
all_obstacles = pygame.sprite.Group()

shark_sprite = Shark(10, 410)                
ground_sprite = Ground(0, HEIGHT - 50)
diver_sprite = Diver(250, 400)

all_sprites.add(shark_sprite)
all_sprites.add(ground_sprite) 
all_obstacles.add(diver_sprite)

diver_sprite.speed_x = 0
diver_sprite.speed_y = 0
diver_sprite.speed_y = 5

run = True
while run:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            

    diver_sprite.rect.y += diver_sprite.speed_y

    if diver_sprite.rect.top <= 280:
        diver_sprite.speed_y = diver_sprite.speed_y * -1
        diver_sprite.rect.y += diver_sprite.speed_y

    if diver_sprite.rect.bottom >= 550:
        diver_sprite.speed_y = diver_sprite.speed_y * -1
        diver_sprite.rect.y += diver_sprite.speed_y

    hits = pygame.sprite.spritecollide(shark_sprite, all_obstacles, False)

    if hits:

        for hit in hits:
            all_obstacles.remove(hit)
            shark_sprite.kill()
            state = 0
            run = False
    if shark_sprite.rect.left > diver_sprite.rect.right + 50:
        state = 1
        run = False
    
    #Update
    all_sprites.update() 

    #Draw
    display_window.fill(WATER)
    display_window.blit(background,(x, 0))
    display_window.blit(bottom, (x, 490)) 
    all_sprites.draw(display_window)
    all_obstacles.draw(display_window)
    
    
    pygame.display.flip()
    pygame.display.update()

    fps_clock.tick(FPS)



if state == 0:
    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_over)
    pygame.mixer.music.play(loops = -1)
    pygame.mixer.music.set_volume(0.80)
    runs = True

    while runs:
        display_window.fill(BLACK)
        display_window.blit(lose, loseRect)
        display_window.blit(more, moreRect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

elif state == 1:
    
    runs = True

    while runs:
        display_window.fill(WATER)
        display_window.blit(ground_sprite.image, (0, HEIGHT-50))
        display_window.blit(background,(x, 0))
        display_window.blit(bottom, (x, 490))
        display_window.blit(winner, winnerRect)
        display_window.blit(instruct3, instruct3Rect)
        pygame.display.update()



        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        

pygame.quit() 














    
