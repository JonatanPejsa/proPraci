import pygame
import random

pygame.init()
screen = pygame.display.set_mode((900, 500))
clock = pygame.time.Clock()
running = True
#-----------------------------------------------------------------------------
pygame.mixer.music.load("music/music.mp3")
bg = pygame.image.load("obrazky/bg.png").convert_alpha()
pygame.display.set_caption('Lidl Bird')
image = pygame.image.load("obrazky/bird4.png").convert_alpha()
pygame.display.set_icon(image)
class Pipe(pygame.sprite.Sprite):

    def __init__(self):
        y =random.randint(-200,0)
        self.up_position = [900, y]
        self.down_position = [900, y+450]
        self.image = pygame.image.load("obrazky/pipe2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, [300, 250])
        self.image = pygame.transform.rotate(self.image, 180)
        self.image2 = pygame.image.load("obrazky/pipe2.png").convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, [300, 250])

    def draw(self, surface):
        surface.blit(self.image, self.up_position)
        surface.blit(self.image2, self.down_position)

    def update_position(self, speed):

        self.up_position[0] -= speed
        self.down_position[0] -= speed
    def detect_colision(self,bird_cord):
        if bird_cord<=self.up_position[1]+230 or bird_cord>=self.down_position[1]-20:
            return True
        return False
    def update(self, surface, bird_cord, speed):
        self.draw(surface)
        self.update_position(speed)
        if self.up_position[0] <= 0 and self.up_position[0] >= -250+112:
            return self.detect_colision(bird_cord)

        return False
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        self.score = 0
        self.alive = True
        self.position = [50, 200]
        self.velocity = 0
        self.image = pygame.image.load("obrazky/bird4.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, [75, 75])
    def update_velocity(self):
        self.velocity += 0.2
    def update_position(self):
        self.position[1] += self.velocity
    def jump(self):
        self.velocity = -6

    def draw(self, surface):
        surface.blit(self.image, self.position)
    def update(self, surface):
        if self.alive:
            self.update_velocity()
            self.update_position()
            self.draw(screen)

        else:
            self.score = 0
            self.position = [50, 200]
            self.velocity = 0
            self.alive = True



sound = pygame.mixer.Sound("music/jump.mp3")
#sound.set_volume(0.1)
bird = Bird()
pipe = Pipe()
pipes = []
cyklus = 120
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 90)
speed = 2
delka_cyklu = 150
best_score = 0
f = open("bestscore.txt", "r", encoding="utf8")
for x in f:
    best_score = int(x)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()
def pause():
    x=1
    while(x==1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return True

        screen.blit(bg, [0, 0])
        score_text = font2.render(f'PAUSE', True, (255, 40, 40))
        screen.blit(score_text, (350, 180))
        
        pygame.display.flip()

while running:

    cyklus +=1
    if cyklus >delka_cyklu:
        pipes.append(Pipe())
        cyklus = 0
        if delka_cyklu<145:
            bird.score+=1
        speed+=0.05
        delka_cyklu -= 2
    # poll for events
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = pause()
            if event.key == pygame.K_SPACE:
                bird.jump()
                sound.play()

    
    screen.blit(bg, [0, 0])

   
    bird.update(screen)
    if bird.position[1] < -50 or bird.position[1] > 490:
        bird.alive = False
        pipes.clear()
        speed = 2
        delka_cyklu = 150
        pygame.mixer.music.play()
    for pipe in pipes:
        if pipe.update(screen, bird.position[1], speed):
            bird.alive = False
            pipes.clear()
            speed = 2
            delka_cyklu = 150
            pygame.mixer.music.play()
    if bird.score > best_score:
        best_score = bird.score
        f = open("bestscore.txt", "w", encoding="utf8")
        f.write(str(best_score))
    score_text = font.render(f'Score: {bird.score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    score_text = font.render(f'Best Score: {best_score}', True, (255, 150, 0))
    screen.blit(score_text, (730, 10))
    # flip() 
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()