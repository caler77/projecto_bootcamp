from math import fabs
import numpy as np 
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

class Base(pg.sprite.Sprite):
    def __init__(self , screen , sprite , howManyRotationsIn360Grades = 16 , spriteCutWidth = 0 , spriteCutHeight = 0 ,  numColSpriteAnimation = 0 , numRowSpriteAnimation = 1 , cordinates = None ):
        super().__init__()
        self.screen = screen
        self.animationTime = FPS * 2
        self.listFramesIndex = 0
        self.frameIndex = 0
        self.imputTime = 0
        self.currentAnimationLoopTime = 0
        self.currentAnimationSequenceTime = 0
        self.animation = False
        self.animationSequence = False
        self.animationSequenceEnd = False
        self.fristFrameIndexChangeSequence = False
        self.fristFrameIndexChangeLoop = False
        self.Animations = []
        self.angle = 360 / howManyRotationsIn360Grades
        self.image = pg.image.load(sprite).convert_alpha()
        self.imgAngle = self.listFramesIndex * self.angle
        if spriteCutHeight != 0 and spriteCutWidth != 0 and spriteCutHeight != 0 and  numColSpriteAnimation != 0:
            self.animation = True
            self.Animations.append( self.loadSpriteMatrix( spriteCutHeight , spriteCutWidth , numColSpriteAnimation , numRowSpriteAnimation ) )
            self.image = self.Animations[self.listFramesIndex][self.frameIndex]['image']
        self.rect = self.image.get_rect(center=(self.screen.get_width()//2,self.screen.get_height()//2))
        # mitad de la pantalla = (self.screen.get_width()//2,self.screen.get_height()//2)
        self.mask = pg.mask.from_surface(self.image)
        self.dir_hit_display = []
        if cordinates:
            self.vel = pg.math.Vector2(cordinates['vel']) 
            self.dir = pg.math.Vector2(cordinates['dir'])
            self.pos = pg.math.Vector2(cordinates['pos'])
        else:
            self.vel = pg.math.Vector2((0,0)) 
            self.dir = pg.math.Vector2((0,0))
            self.pos = pg.math.Vector2((self.rect.x,self.rect.y))
        if not self.animation:
            self.Animations.append([{ 'image' : self.image , 'rect' : self.rect , 'mask' : self.mask }])
        for angle in np.arange(0,360,self.angle):
            if angle != 0:
                self.Animations.append(self.generaListImgRotate(angle))
        self.valueStart = {
            'vel':(self.vel.x,self.vel.y),
            'dir':(self.dir.x,self.dir.y),
            'pos':(self.pos.x,self.pos.y)
        }
        c = 1

    def reset(self):
        self.animationTime = FPS * 2
        self.listFramesIndex = 0
        self.frameIndex = 0
        self.imputTime = 0
        self.currentAnimationLoopTime = 0
        self.currentAnimationSequenceTime = 0
        self.animation = False
        self.animationSequence = False
        self.animationSequenceEnd = False
        self.fristFrameIndexChangeSequence = False
        self.fristFrameIndexChangeLoop = False
        self.dir_hit_display = []
        self.vel = pg.math.Vector2(self.valueStart['vel']) 
        self.dir = pg.math.Vector2(self.valueStart['dir'])
        self.pos = pg.math.Vector2(self.valueStart['pos'])
        self.image = self.Animations[self.listFramesIndex][self.frameIndex]['image']
        self.rect = self.Animations[self.listFramesIndex][self.frameIndex]['rect']
        self.mask = self.Animations[self.listFramesIndex][self.frameIndex]['mask']
        pass

    def loadSpriteMatrix(self , spriteCutHeight , spriteCutWidth , numColSpriteAnimation , numRowSpriteAnimation = 1):
        listAnimation = []
        for row in range(0,numRowSpriteAnimation):
            y = row * spriteCutWidth
            for col in range(0,numColSpriteAnimation):
                x = col * spriteCutHeight
                image = pg.Surface( (spriteCutWidth,spriteCutHeight) , pg.SRCALPHA ).convert_alpha()
                image.blit(self.image,(0,0),(x,y,spriteCutWidth,spriteCutHeight))
                imgRect = image.get_rect()
                imgMask = pg.mask.from_surface(image)
                frame = { 'image' : image , 'rect' : imgRect , 'mask' : imgMask }
                listAnimation.append(frame)
        return listAnimation

    '''
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
    '''

    def imput(self , dt ):
        self.imputTime += dt
        key = pg.key.get_pressed()
        #detection of keys and aplicate sum to vector dir for move 
        if key[pg.K_d]:
            self.dir.x = 1 
            if 'right' in self.dir_hit_display:
                self.vel.x = 0
            else:
                self.vel.x = 1
        elif key[pg.K_a]:
            self.dir.x = -1 
            if 'left' in self.dir_hit_display:
                self.vel.x = 0
            else:
                self.vel.x = 1
        else:
            self.dir.x = 0 

        if key[pg.K_w]:
            self.dir.y = -1
            if 'top' in self.dir_hit_display:
                self.vel.y = 0
            else:
                self.vel.y = 1
        elif key[pg.K_s]:
            self.dir.y = 1 
            if 'bottom' in self.dir_hit_display:
                self.vel.y = 0
            else:
                self.vel.y = 1
        else:
            self.dir.y = 0

        if key[pg.K_q] and self.imputTime >= 100:
            self.imputTime = 0
            self.rotar(1)

        if key[pg.K_e] and self.imputTime >= 100:
            self.imputTime = 0
            self.rotar(-1)

        if key[pg.K_r]:
            self.animation = False

        if key[pg.K_t] and not self.animationSequence:
            self.animation = True 
            self.fristFrameIndexChangeLoop = False

        if key[pg.K_y] and not self.animation and self.imputTime >= 1000 and not self.animationSequence:
            self.imputTime = 0
            self.animationSequence = True
            self.fristFrameIndexChangeSequence = False

    def move(self):
        #if self.dir.magnitude() != 0:
        #    self.dir = self.dir.normalize()

        #self.rect.move_ip((self.dir.x * self.vel * self.limite , self.dir.y * self.vel * self.limite))
        #self.pos = (self.rect.x,self.rect.y)
        self.pos.x += self.dir.x * self.vel.x 
        self.pos.y += self.dir.y * self.vel.y
        self.rect.x , self.rect.y = self.pos.x , self.pos.y

    def limitDisplay(self):
        mask_rect = self.mask.get_bounding_rects()
        #se coje la pantalla por el momento pero luego esto debe cojer el tamaño del mapa del juego e informarlo por parametro para el objeto o el metodo 
        map_widht , map_height = self.screen.get_size()
        #print(mask_rect)
        #print(mask_rect[0].top , mask_rect[0].bottom ,mask_rect[0].left ,mask_rect[0].right) 
        #print('#----------------------------------------------#')
        #print('el rect es : ' , self.rect)
        self.dir_hit_display = []
        for rect in mask_rect:
            scroll_right = rect.x
            scroll_top = rect.y
            scroll_left = self.rect.width - (rect.x + rect.width)
            scroll_bottom = self.rect.height - (rect.y + rect.height)
            #print('##' , rect)
            #print(rect.top , rect.bottom , rect.right , rect.left)

            if self.rect.top + scroll_top <= 0: 
                #print('toca arriba')
                self.dir_hit_display.append('top')

            if self.rect.bottom - scroll_bottom >= map_height:
                #print('toca abajo')
                self.dir_hit_display.append('bottom')

            if self.rect.left + scroll_left <= 0: 
                #print('toca izquierda')
                self.dir_hit_display.append('left')

            if self.rect.right - scroll_right >= map_widht:
                #print('toca derecha')
                self.dir_hit_display.append('right')

    def pinta(self):
        self.screen.blit(self.image , (self.pos))

    '''
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

    '''

    def generaListImgRotate(self , angulo): 
        listaImagenesRotadas = []
        for i in range(len(self.Animations[self.listFramesIndex])):
            image = self.Animations[self.listFramesIndex][i]['image']
            image_rotate = pg.transform.rotate( image , angulo )
            imgRect_rotate = image_rotate.get_rect()
            imgMask_rotate = pg.mask.from_surface(image_rotate)
            frame = { 'image' : image_rotate , 'rect' : imgRect_rotate , 'mask' : imgMask_rotate }
            listaImagenesRotadas.append(frame)
        return listaImagenesRotadas

    def rotar(self , PosOrNeg ):
        centerPrevius = self.rect.center
        if PosOrNeg == 1:
            if self.listFramesIndex +1 == len(self.Animations):
                self.listFramesIndex = 0
            else:
                self.listFramesIndex += 1

        if PosOrNeg == -1:
            if self.listFramesIndex - 1 == -1:
                self.listFramesIndex = len(self.Animations) - 1
            else:
                self.listFramesIndex += -1

        self.imgAngle = self.listFramesIndex * self.angle
        self.image = self.Animations[self.listFramesIndex][self.frameIndex]['image']
        self.rect = self.Animations[self.listFramesIndex][self.frameIndex]['rect']
        self.rect.center = centerPrevius
        self.pos.x , self.pos.y = self.rect.x , self.rect.y
        self.mask = self.Animations[self.listFramesIndex][self.frameIndex]['mask']

    def AnimationLoop(self , dt , frameEnd = 0 , frameStart = 0 ):
        if frameStart < 0:
            frameStart = 0
        if frameEnd == 0:
            frameEnd = len(self.Animations[self.listFramesIndex])
        else:
            if frameEnd > len(self.Animations[self.listFramesIndex]):
                frameEnd = len(self.Animations[self.listFramesIndex])
            else:
                frameEnd = frameEnd
        if self.frameIndex != frameStart and not self.fristFrameIndexChangeLoop:
            self.fristFrameIndexChangeLoop = True
            self.frameIndex = frameStart
        centerPrevius = self.rect.center
        self.currentAnimationLoopTime += dt   
        if self.currentAnimationLoopTime > self.animationTime:
            self.currentAnimationLoopTime = 0
            self.frameIndex +=1
            if self.frameIndex == frameEnd :
                self.frameIndex = frameStart
                self.fristFrameIndexChangeLoop = False
            else :
                self.image = self.Animations[self.listFramesIndex][self.frameIndex]['image']
                self.rect = self.Animations[self.listFramesIndex][self.frameIndex]['rect']
                self.rect.center = centerPrevius
                self.mask = self.Animations[self.listFramesIndex][self.frameIndex]['mask']

    def AnimationSequence(self , dt , frameEnd , frameStart ):
        if frameStart < 0:
            frameStart = 0
        if frameEnd > len(self.Animations[self.listFramesIndex]):
            frameEnd = len(self.Animations[self.listFramesIndex]) - 1
        self.animationSequenceEnd = False
        if self.frameIndex != frameStart and not self.fristFrameIndexChangeSequence:
            self.fristFrameIndexChangeSequence = True
            self.frameIndex = frameStart
        centerPrevius = self.rect.center
        self.currentAnimationSequenceTime += dt   
        if self.currentAnimationSequenceTime > self.animationTime:
            self.currentAnimationSequenceTime = 0
            self.frameIndex +=1
            if self.frameIndex == frameEnd :
                self.frameIndex = frameEnd 
                self.image = self.Animations[self.listFramesIndex][self.frameIndex]['image']
                self.rect = self.Animations[self.listFramesIndex][self.frameIndex]['rect']
                self.rect.center = centerPrevius
                self.mask = self.Animations[self.listFramesIndex][self.frameIndex]['mask']
                self.animationSequenceEnd = True
                self.fristFrameIndexChangeSequence = False
            else:
                self.image = self.Animations[self.listFramesIndex][self.frameIndex]['image']
                self.rect = self.Animations[self.listFramesIndex][self.frameIndex]['rect']
                self.rect.center = centerPrevius
                self.mask = self.Animations[self.listFramesIndex][self.frameIndex]['mask']

    def update(self , dt):
        if self.animationSequenceEnd:
            self.animationSequence = False
            self.animationSequenceEnd = False
        #self.pos.x , self.pos.y = self.rect.x , self.rect.y
        if self.animation:
            self.AnimationLoop(dt,9,0)
        if self.animationSequence:
            self.AnimationSequence(dt,15,10)
        self.limitDisplay()
        self.imput(dt)
        self.move()
        self.pinta()



