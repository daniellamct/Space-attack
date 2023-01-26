import pygame
import random
import os
FPS = 60
WIDTH = 600
HEIGHT = 1000
score = 0
health = 100
  

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("daniel's game")
clock = pygame.time.Clock()

spaceship_image = pygame.image.load(os.path.join("img", "spaceship.png")).convert()
background_image = pygame.image.load(os.path.join("img", "background.jpg")).convert()
rock_image = pygame.image.load(os.path.join("img", "poop_emoji.png")).convert() 

gun_sound = pygame.mixer.Sound(os.path.join("sound", "gun.mp3"))
gun_sound.set_volume(0.2)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255), (200, 100, 100))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.y = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()       
    all_sprites.add(r)
    rocks.add(r)


def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0

    BAR_LENGTH = 200
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spaceship_image, (200, 200))
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        self.radius = 45
        """  pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)  """
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 5
        self.health = health


    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.right += self.speedx
        if key_pressed[pygame.K_LEFT]:  
            self.rect.right -= self.speedx 

        if self.rect.centerx > WIDTH:
            self.rect.centerx = WIDTH
        if self.rect.centerx < 0:
            self.rect.centerx = 0

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange(30, 130)
        self.image_ori = pygame.transform.scale(rock_image, (self.size, self.size))
        self.image_ori.set_colorkey((255, 255, 255))
        self.image = self.image_ori.copy()

        self.rect = self.image.get_rect()
        self.radius = self.rect.width / 2
        """ pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius) """
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 6)
        self.speedx = random.randrange(-2, 2)
        self.total_degree = 0
        self.rot_degree = random.randrange(-2, 2)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        
   
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center 

        #touching boundary, -> reset every data of rock
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.size = random.randrange(30, 130)
            self.image_ori = pygame.transform.scale(rock_image, (self.size, self.size))
            self.image_ori.set_colorkey((255, 255, 255))
            self.image = self.image_ori.copy()

            self.rect = self.image.get_rect()

            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 5)
            self.speedx = random.randrange(-2,2)
            self.rot_degree = random.randrange(-2, 2)

            self.radius = self.rect.width / 2


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((8, 20))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx 
        self.rect.y = player.rect.y
        self.speedy = 10       
        

    def update(self):
        
      
            

  
        if self.rect.bottom > 0:
            self.rect.y -= self.speedy
        else:
            self.kill()




all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
 

for i in range(8):
    new_rock()



###############################################
running = True
while running: 
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s or event.key == pygame.K_d:
                
                b = Bullet()
                all_sprites.add(b)
                bullets.add(b)
                gun_sound.play()
   
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        score += round(hit.radius, 0)
        new_rock()


    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= hit.radius

        if player .health <= 0:
            running = False

    
    screen.blit(background_image, (0, 0))
    """ screen.fill((200, 60, 20)) """
    all_sprites.draw(screen)
    draw_text(screen, str(score), 28, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    pygame.display.update()

pygame.quit()