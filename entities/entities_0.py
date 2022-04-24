import pygame as pg  
import os 

FPS = 60

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((20,20))        #'.convert_alpha() no se puede hacer un convert o un convert_alpha sin iniciar un pygame.display 
        self.image.fill((255,0,0,255))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.velocity = pg.math.Vector2((0,0))
        self.dir = pg.math.Vector2((0,0))
        self.pos = pg.math.Vector2(self.rect.center)
    def move(self): 
        self.pos += self.dir * self.velocity
        self.rect.center = round(self.pos.x), round(self.pos.y)


class Bullet(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((5,2))
        self.image.fill((255,255,255,255))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

class Obtacle(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50,50))
        self.image.fill((0,0,255,255))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.status = 5

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((20,20))
        self.image.fill((0,255,0,255))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

'''
class limitsDisplay(pg.sprite.Sprite):
    def __init__(self ,screen ):
        super().__init__()
        self.screen = screen
        self.rect = self.screen.get_rect(center=(self.screen.get_width()//2,self.screen.get_height()//2))
        self.pintaLinites()
        self.mask = pg.mask.from_surface(self.image)

    def pintaLinites(self):
        pg.draw.rect(self.image , (255,0,0,255) , ( 5 , 5 , self.screen.get_width() - 5 , self.screen.get_height() - 5 ) , 5 )
'''

class ejemplo(pg.sprite.Sprite):
    def __init__(self , screen , sprite , spriteCutWidth = 0 , spriteCutHeight = 0 ,  numColSpriteAnimation = 0 , numRowSpriteAnimation = 0 ):
        super().__init__()
        self.screen = screen
        self.frameIndex = 0
        self.currentTime = 0
        self.animation = False
        self.image = pg.image.load(sprite).convert_alpha()
        if spriteCutHeight != 0 and spriteCutWidth != 0 and numColSpriteAnimation != 0 and numRowSpriteAnimation != 0:
            self.loadSpriteMatrix( spriteCutHeight , spriteCutWidth , numColSpriteAnimation , numRowSpriteAnimation )
            self.animation = True
        elif spriteCutHeight != 0 and spriteCutWidth != 0 and numColSpriteAnimation != 0:
            self.loadSpriteArray( spriteCutHeight , spriteCutWidth , numColSpriteAnimation )
            self.animation = True
        self.rect = self.image.get_rect(center=(self.screen.get_width()//2,self.screen.get_height()//2))
        # mitad de la pantalla = (self.screen.get_width()//2,self.screen.get_height()//2)
        self.vel = 1
        self.dir = pg.math.Vector2()
        self.pos = pg.math.Vector2((self.rect.x,self.rect.y))
        self.mask = pg.mask.from_surface(self.image)
        

    def loadSpriteMatrix(self , spriteCutHeight , spriteCutWidth , numColSpriteAnimation , numRowSpriteAnimation):
        self.listAnimation = []
        for row in range(0,numRowSpriteAnimation):
            y = row * spriteCutWidth
            for col in range(0,numColSpriteAnimation):
                x = col * spriteCutHeight
                image = pg.Surface( (spriteCutWidth,spriteCutHeight) , pg.SRCALPHA ).convert_alpha()
                image.blit(self.image,(0,0),(x,y,spriteCutWidth,spriteCutHeight))
                imgRect = image.get_rect()
                imgMask = pg.mask.from_surface(image)
                frame = { 'image' : image , 'rect' : imgRect , 'mask' : imgMask }
                self.listAnimation.append(frame)
        self.image = self.listAnimation[self.frameIndex]['image']

    def loadSpriteArray(self , spriteCutWidth , spriteCutHeight , numColSpriteAnimation ):
        self.listAnimation = []
        y = 0
        for col in range(0,numColSpriteAnimation):
            x = col * spriteCutHeight
            image = pg.Surface( (spriteCutWidth,spriteCutHeight) , pg.SRCALPHA ).convert_alpha()
            image.blit(self.image,(0,0),(x,y,spriteCutWidth,spriteCutHeight))
            imgRect = image.get_rect()
            imgMask = pg.mask.from_surface(image)
            frame = { 'image' : image , 'rect' : imgRect , 'mask' : imgMask }
            self.listAnimation.append(frame)
        self.image = self.listAnimation[0]['image']

    def imput(self):
        key = pg.key.get_pressed()
        #detection of keys and aplicate sum to vector dir for move 
        if key[pg.K_RIGHT]:
            self.dir.x = 1 
        elif key[pg.K_LEFT]:
            self.dir.x = -1 
        else:
            self.dir.x = 0 

        if key[pg.K_UP]:
            self.dir.y = -1
        elif key[pg.K_DOWN]:
            self.dir.y = 1 
        else:
            self.dir.y = 0

    def move(self):
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()

        #self.rect.move_ip((self.dir.x * self.vel * self.limite , self.dir.y * self.vel * self.limite))
        #self.pos = (self.rect.x,self.rect.y)
        self.pos.x += self.dir.x * self.vel  
        self.pos.y += self.dir.y * self.vel 
        self.rect.x , self.rect.y = self.pos.x , self.pos.y

    def limitDisplay(self):
        mask_rect = self.mask.get_bounding_rects()
        #se coje la pantalla por el momento pero luego esto debe cojer el tamaño del mapa del juego e informarlo por parametro para el objeto o el metodo 
        map_widht , map_height = self.screen.get_size()
        #print(mask_rect)
        #print(mask_rect[0].top , mask_rect[0].bottom ,mask_rect[0].left ,mask_rect[0].right) 
        print('#----------------------------------------------#')
        print('el rect es : ' , self.rect)
        for rect in mask_rect:
            scroll_right = rect.x
            scroll_top = rect.y
            scroll_left = self.rect.width - (rect.x + rect.width)
            scroll_bottom = self.rect.height - (rect.y + rect.height)
            print('##' , rect)
            print(rect.top , rect.bottom , rect.right , rect.left)
            if self.rect.top + scroll_top <= 0 or self.rect.bottom - scroll_bottom >= map_height: 
                print('toca')

    def pinta(self):
        self.screen.blit(self.image , (self.pos))

    def generaListImgRotate(self , angulo , step):
        centerPrevius = self.rect.center
        listaImagenesRotadas = []
        for grado in range(0,angulo, step):
            image = pg.transform.rotate(self.image , grado)
            imgRect = image.get_rect(center = centerPrevius)
            imgMask = pg.mask.from_surface(image)
            frame = { 'image' : image , 'rect' : imgRect , 'mask' : imgMask }
            listaImagenesRotadas.append(frame)
        return listaImagenesRotadas

    def rotar(self):
        pass

    def Animation(self , dt):
        centerPrevius = self.rect.center
        self.currentTime += dt   
        self.animationTime = FPS * 2
        if self.currentTime > self.animationTime:
            self.currentTime = 0
            self.frameIndex +=1
            if self.frameIndex == len(self.listAnimation):
                self.frameIndex = 0
            self.image = self.listAnimation[self.frameIndex]['image']
            self.rect = self.listAnimation[self.frameIndex]['rect']
            self.rect.center = centerPrevius
            self.mask = self.listAnimation[self.frameIndex]['mask']

    def update(self , dt):
        if self.animation:
            self.Animation(dt)
        self.limitDisplay()
        self.imput()
        self.move()
        self.pinta()



