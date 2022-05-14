#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(700,500))

clock = time.Clock()
FPS = 60







class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_speed,player_x,player_y,w,h):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed=key.get_pressed()        
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',3, self.rect.centerx,self.rect.top,10,15)
        bullets.add(bullet)

lost=0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >=500:
            lost = lost +1
            self.rect.x =randint(0,635)
            self.rect.y = 0

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.y >=500:
            
            self.rect.x =randint(0,635)
            self.rect.y = 0


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <=0:
            self.kill()           


hero =Player('rocket.png',10,300,400,65,80)
monsters = sprite.Group()
for i in range(5):
    n =randint(0,635)
    monster = Enemy('ufo.png',randint(2,4),n,0,65,45)
    monsters.add(monster)
font.init()
font1 = font.SysFont('Arial',36)
asteroids = sprite.Group()
for i in range(2):
    n =randint(0,635)
    asteroid = Asteroid('asteroid.png',randint(1,2),n,0,65,45)
    asteroids.add(asteroid)

bullets = sprite.Group()

rel_time= False
num_fire=0
finish =False
game =True
score = 0
while game:
    if finish != True:

        text_reload = font1.render('wait reload',1,(255,255,255))
        window.blit(background,(0,0))
        text_lose = font1.render('Пропущено: '+ str(lost),1,(255,255,255))
        text_win = font1.render('Счет: '+ str(score),1,(255,255,255))
        window.blit(text_win,(0,20))
        window.blit(text_lose,(0,60))
        hero.reset()
        hero.update()
        asteroids.draw(window)
        asteroids.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        win=font1.render('Победа',1,(0,255,0))
        lose=font1.render('Ну блин',1,(255,0,0))
        sprites_list = sprite.groupcollide(monsters,bullets,True,True)
        sprites_list1 = sprite.spritecollide(hero,monsters,False)
        sprites_list2 = sprite.spritecollide(hero,asteroids,False)
        if len(sprites_list1) >0:
            finish=True
            window.blit(lose,(350,250))
        
        if len(sprites_list2) >0:
            finish=True
            window.blit(lose,(350,250))

        if score >10:
            finish=True
            window.blit(win,(350,250))

        if lost >15:
            finish=True
            window.blit(lose,(350,250))

        for s in sprites_list:
            score +=1
            monster = Enemy('ufo.png',randint(2,4),randint(0,635),0,65,45)
            monsters.add(monster)
        if rel_time == True:
            new_time=timer()
            if new_time-old_time>=3:
                num_fire=0
                rel_time=False
            else:
                window.blit(text_reload,(350,250))

        
   

          
        
        
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire<5 and rel_time==False:
                    hero.fire()
                    num_fire+=1
                else:
                    rel_time = True
                    old_time = timer()
    
                
    
    
       
 
    display.update()
    clock.tick(FPS)
    