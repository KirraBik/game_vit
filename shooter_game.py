#Создай собственный Шутер!

from pygame import *
from random import randint

lost = 0
score = 0

class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       # !каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       #!каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.centerx, self.rect.top, 15, 25,15)
        bullets.add(bullet)
        mixer.Sound('fire.ogg')
#класс-наследник для спрайта-врага (перемещается сам)
class Enemy(GameSprite):
   def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost += 1
       
 

#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Space")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
 
#Персонажи игры:
player = Player('rocket.png', 5, win_height - 80, 4)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', win_width - randint(0,501), -50, 2)
    monsters.add(monster)
game = True
finish = False
clock = time.Clock()
FPS = 60
 
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
 
while game:
   for e in event.get():
        if e.type == QUIT:
           game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
   if finish != True:
       window.blit(background,(0, 0))
       player.update()
       monsters.update()
       bullets.update()
      
       player.reset()
       monsters.draw(window)
       bullets.draw(window)
 
   display.update()
   clock.tick(FPS)