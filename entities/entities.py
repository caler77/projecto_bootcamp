import numpy as np 
import pygame as pg  
from data.config.config import FPS


class Base(pg.sprite.Sprite):
    def __init__(self , screen , sprite , howManyRotationsIn360Grades = 16 , spriteCutWidth = 0 , spriteCutHeight = 0 ,  numColSpriteAnimation = 0 , numRowSpriteAnimation = 1 , cordinates : dict = None , scale = 1 ):
        super().__init__()
        self.screen = screen
        self.imgSprite = sprite
        self.animationTime = FPS * 2
        self.listFramesIndex = 0
        self.frameIndex = 0
        self.imputVelTime = 0
        self.imputRotateTime = 0
        self.imputSequenceTime = 0
        self.imputModTime = 0
        self.currentAnimationLoopTime = 0
        self.currentAnimationSequenceTime = 0
        self.animation = False
        self.animationSequence = False
        self.animationSequenceEnd = False
        self.fristFrameIndexChangeSequence = False
        self.fristFrameIndexChangeLoop = False
        self.transform = scale
        self.Animations = []
        self.angle = 360 / howManyRotationsIn360Grades
        self.imgAngle = self.listFramesIndex * self.angle
        self.image = pg.image.load(sprite).convert_alpha()
        if spriteCutHeight != 0 and spriteCutWidth != 0 and spriteCutHeight != 0 and  numColSpriteAnimation != 0:
            self.animation = True
            self.Animations.append( self.loadSpriteMatrix( spriteCutHeight , spriteCutWidth , numColSpriteAnimation , numRowSpriteAnimation ) )
            self.image = self.Animations[self.listFramesIndex][self.frameIndex]['image']
        if not self.animation:
            if isinstance(self.transform , int): 
                if self.transform == 2:
                    self.image = pg.transform.scale2x(self.image)
                elif self.transform < 0:
                    self.image = pg.transform.scale(self.image,(self.image.get_width() // abs(self.transform) , self.image.get_height() // abs(self.transform)))
                elif self.transform != 0 :
                    self.image = pg.transform.scale(self.image,(self.image.get_width() * self.transform , self.image.get_height() * self.transform))
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
        self.sizeTransform = [ self.rect.width , self.rect.height]
        self.valueStart = {
            'vel':(self.vel.x,self.vel.y),
            'dir':(self.dir.x,self.dir.y),
            'pos':(self.pos.x,self.pos.y),
            'spriteCutHeight': spriteCutHeight , 
            'spriteCutWidth': spriteCutWidth , 
            'numColSpriteAnimation': numColSpriteAnimation ,
            'numRowSpriteAnimation': numRowSpriteAnimation
        }    

    def reset(self):
        self.animationTime = FPS * 2
        self.listFramesIndex = 0
        self.frameIndex = 0
        self.imputVelTime = 0
        self.imputRotateTime = 0
        self.imputSequenceTime = 0
        self.imputModTime = 0
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
        self.Animations = []
        #self.Animations = self.firtsAnimations[:]  no funciona por eso:
        self.image = pg.image.load(self.imgSprite).convert_alpha()
        if self.valueStart['spriteCutHeight'] != 0 and self.valueStart['spriteCutWidth'] != 0 and self.valueStart['spriteCutHeight'] != 0 and  self.valueStart['numColSpriteAnimation'] != 0:
            self.animation = True
            self.Animations.append( self.loadSpriteMatrix( self.valueStart['spriteCutHeight'] , self.valueStart['spriteCutWidth'] , self.valueStart['numColSpriteAnimation'] , self.valueStart['numRowSpriteAnimation'] ) )
            self.image = self.Animations[self.listFramesIndex][self.frameIndex]['image']
        if not self.animation:
            if self.transform == 2:
                self.image = pg.transform.scale2x(self.image)
            elif self.transform < 0 and isinstance(self.transform , int):
                self.image = pg.transform.scale(self.image,(self.image.get_width() // abs(self.transform) , self.image.get_height() // abs(self.transform)))
            elif self.transform != 0 and isinstance(self.transform , int):
                self.image = pg.transform.scale(self.image,(self.image.get_width() * self.transform , self.image.get_height() * self.transform))
        self.rect = self.image.get_rect(center=(self.screen.get_width()//2,self.screen.get_height()//2))
        # mitad de la pantalla = (self.screen.get_width()//2,self.screen.get_height()//2)
        self.mask = pg.mask.from_surface(self.image)
        if not self.animation:
            self.Animations.append([{ 'image' : self.image , 'rect' : self.rect , 'mask' : self.mask }])
        for angle in np.arange(0,360,self.angle):
            if angle != 0:
                self.Animations.append(self.generaListImgRotate(angle))
        self.image = self.Animations[self.listFramesIndex][self.frameIndex]['image']
        self.rect = self.Animations[self.listFramesIndex][self.frameIndex]['rect']
        self.mask = self.Animations[self.listFramesIndex][self.frameIndex]['mask']
        self.sizeTransform = [ self.rect.width , self.rect.height]

    def loadSpriteMatrix(self , spriteCutHeight , spriteCutWidth , numColSpriteAnimation , numRowSpriteAnimation = 1):
        listAnimation = []
        for row in range(0,numRowSpriteAnimation):
            y = row * spriteCutWidth
            for col in range(0,numColSpriteAnimation):
                x = col * spriteCutHeight
                image = pg.Surface( (spriteCutWidth,spriteCutHeight) , pg.SRCALPHA ).convert_alpha()
                image.blit(self.image,(0,0),(x,y,spriteCutWidth,spriteCutHeight))
                if isinstance(self.transform , int):
                    if self.transform == 2:
                        image = pg.transform.scale2x(image)
                    elif self.transform < 0:
                        image = pg.transform.scale(image,(image.get_width() // abs(self.transform) , image.get_height() // abs(self.transform)))
                    elif  self.transform != 0:
                        image = pg.transform.scale(image,(image.get_width() * self.transform , image.get_height() * self.transform ))
                imgRect = image.get_rect()
                imgMask = pg.mask.from_surface(image)
                frame = { 'image' : image , 'rect' : imgRect , 'mask' : imgMask }
                listAnimation.append(frame)
        return listAnimation

    def scale(self , transform):
        centerPrevius = self.rect.center

        if self.sizeTransform[0] <= 10:
            self.sizeTransform[0] = 10
        if self.sizeTransform[1] <= 10:
            self.sizeTransform[1] = 10

        self.AnimationsTemp = []
        #self.Animations = self.firtsAnimations[:]  no funciona por eso:
        self.image = pg.image.load(self.imgSprite).convert_alpha()
        if self.valueStart['spriteCutHeight'] != 0 and self.valueStart['spriteCutWidth'] != 0 and self.valueStart['spriteCutHeight'] != 0 and  self.valueStart['numColSpriteAnimation'] != 0:
            animation = True
            self.AnimationsTemp.append( self.loadSpriteMatrix( self.valueStart['spriteCutHeight'] , self.valueStart['spriteCutWidth'] , self.valueStart['numColSpriteAnimation'] , self.valueStart['numRowSpriteAnimation'] ) )
            image = self.AnimationsTemp[0][self.frameIndex]['image']
        if not animation:
            if self.transform == 2:
                image = pg.transform.scale2x(image)
            elif self.transform < 0 and isinstance(self.transform , int):
                image = pg.transform.scale(image,(image.get_width() // abs(self.transform) , image.get_height() // abs(self.transform)))
            elif self.transform != 0 and isinstance(self.transform , int):
                image = pg.transform.scale(image,(image.get_width() * self.transform , image.get_height() * self.transform))

        rect = image.get_rect()
        # mitad de la pantalla = (self.screen.get_width()//2,self.screen.get_height()//2)
        mask = pg.mask.from_surface(image)

        if not animation:
            self.AnimationsTemp.append([{ 'image' : image , 'rect' : rect , 'mask' : mask }])

        '''
        for frame in range(len(self.AnimationsTemp[0])):
            image = self.AnimationsTemp[0][frame]['image']
            if transform == 2:
                imageTranform = pg.transform.scale2x(image)
            elif transform < 0 :
                imageTranform = pg.transform.scale(image,(self.sizeTransform[0] // abs(transform) , self.sizeTransform[1] // abs(transform)))
            elif transform != 0 :
                imageTranform = pg.transform.scale(image,(self.sizeTransform[0] * transform , self.sizeTransform[1] * transform ))
            self.AnimationsTemp[0][frame]['image'] = imageTranform
        '''

        for angle in np.arange(0,360,self.angle):
            if angle != 0:
                self.AnimationsTemp.append(self.generaListImgRotate(angle))

        for list in range(len(self.AnimationsTemp)):
            for frame in range(len(self.AnimationsTemp[list])):
                rect = self.Animations[list][frame]['rect']
                image = self.AnimationsTemp[list][frame]['image']

                
                if transform == 2:
                    imageTransform = pg.transform.scale2x(image)
                elif transform < 0 and isinstance(self.transform , int):
                    imageTransform = pg.transform.scale(image,(rect.w // abs(transform) , rect.h // abs(transform)))
                elif transform != 0 and isinstance(self.transform , int):
                    imageTransform = pg.transform.scale(image,(rect.w * transform , rect.h * transform ))
                

                self.Animations[list][frame]['image'] = imageTransform
                self.Animations[list][frame]['rect'] = imageTransform.get_rect()
                self.Animations[list][frame]['mask'] = pg.mask.from_surface(imageTransform)

        self.image = self.Animations[self.listFramesIndex][self.frameIndex]['image']
        self.rect = self.Animations[self.listFramesIndex][self.frameIndex]['rect']
        self.mask = self.Animations[self.listFramesIndex][self.frameIndex]['mask']
        self.rect.center = centerPrevius
        self.sizeTransform = [ self.rect.width , self.rect.height]
        self.pos.x ,self.pos.y = self.rect.x , self.rect.y
        c = 0

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

        if key[pg.K_y] and not self.animation and self.imputTime >= 1000 and not self.animationSequence:
            self.imputTime = 0
            self.animationSequence = True

        if key[pg.K_f]:
            self.reset()
    '''

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
        for i in range(len(self.Animations[0])):
            image = self.Animations[0][i]['image']
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

    '''
    def update(self , dt):
        if self.animationSequenceEnd:
            self.animationSequence = False
            self.animationSequenceEnd = False
        #self.pos.x , self.pos.y = self.rect.x , self.rect.y
        if self.animation:
            self.AnimationLoop(dt)
        if self.animationSequence:
            self.AnimationSequence(dt,25,0)
        self.limitDisplay()
        self.imput(dt)
        self.move()
        self.pinta()
    '''

class Jugador(Base):
    def __init__(self, screen, sprite, howManyRotationsIn360Grades=16, spriteCutWidth=0, spriteCutHeight=0, numColSpriteAnimation=0, numRowSpriteAnimation=1, cordinates=None , scale = 1 ):
        super().__init__( screen , sprite, howManyRotationsIn360Grades, spriteCutWidth, spriteCutHeight, numColSpriteAnimation, numRowSpriteAnimation, cordinates , scale )
        self.score_player = 0  
        self.dir_hit_momentum = []
        self.vidas = 3

    def limitMomvement(self , top , bottom , right , left):
        mask_rect = self.mask.get_bounding_rects()
        #se coje la pantalla por el momento pero luego esto debe cojer el tamaño del mapa del juego e informarlo por parametro para el objeto o el metodo 
        #print(mask_rect)
        #print(mask_rect[0].top , mask_rect[0].bottom ,mask_rect[0].left ,mask_rect[0].right) 
        #print('#----------------------------------------------#')
        #print('el rect es : ' , self.rect)
        self.dir_hit_momentum = []
        for rect in mask_rect:
            scroll_right = rect.x
            scroll_top = rect.y
            scroll_left = self.rect.width - (rect.x + rect.width)
            scroll_bottom = self.rect.height - (rect.y + rect.height)
            #print('##' , rect)
            #print(rect.top , rect.bottom , rect.right , rect.left)

            if self.rect.top + scroll_top <= top: 
                #print('toca arriba')
                self.dir_hit_momentum.append('top')

            if self.rect.bottom - scroll_bottom >= bottom:
                #print('toca abajo')
                self.dir_hit_momentum.append('bottom')

            if self.rect.left + scroll_left <= left: 
                #print('toca izquierda')
                self.dir_hit_momentum.append('left')

            if self.rect.right - scroll_right >= right:
                #print('toca derecha')
                self.dir_hit_momentum.append('right')

    def imput(self , dt ):
        self.imputRotateTime += dt
        self.imputSequenceTime += dt
        self.imputModTime += dt
        key = pg.key.get_pressed()
        #detection of keys and aplicate sum to vector dir for move 
        if key[pg.K_d]:
            self.dir.x = 1 
            if 'right' in self.dir_hit_display or 'right' in self.dir_hit_momentum:
                self.vel.x = 0
            else:
                if pg.key.get_mods() & pg.KMOD_SHIFT and self.imputModTime >= 1000:
                    self.vel.x = 5
                    self.imputVelTime += dt
                    if self.imputVelTime >= 200:
                        self.imputModTime = 0
                        self.imputVelTime = 0
                else:
                    self.vel.x = 1
        elif key[pg.K_a]:
            self.dir.x = -1 
            if 'left' in self.dir_hit_display or 'left' in self.dir_hit_momentum:
                self.vel.x = 0
            else:
                if pg.key.get_mods() & pg.KMOD_SHIFT and self.imputModTime >= 1000:
                    self.vel.x = 5
                    self.imputVelTime += dt
                    if self.imputVelTime >= 200:
                        self.imputModTime = 0
                        self.imputVelTime = 0
                else:
                    self.vel.x = 1
        else:
            self.dir.x = 0 

        if key[pg.K_w]:
            self.dir.y = -1
            if 'top' in self.dir_hit_display or 'top' in self.dir_hit_momentum:
                self.vel.y = 0
            else:
                if pg.key.get_mods() & pg.KMOD_SHIFT and self.imputModTime >= 1000:
                    self.vel.y = 5
                    self.imputVelTime += dt
                    if self.imputVelTime >= 200:
                        self.imputModTime = 0
                        self.imputVelTime = 0
                else:
                    self.vel.y = 1
        elif key[pg.K_s]:
            self.dir.y = 1 
            if 'bottom' in self.dir_hit_display or 'bottom' in self.dir_hit_momentum:
                self.vel.y = 0
            else:
                if pg.key.get_mods() & pg.KMOD_SHIFT and self.imputModTime >= 1000:
                    self.vel.y = 5
                    self.imputVelTime += dt
                    if self.imputVelTime >= 200:
                        self.imputModTime = 0
                        self.imputVelTime = 0
                else:
                    self.vel.y = 1
        else:
            self.dir.y = 0

        if key[pg.K_q] and self.imputRotateTime >= 100:
            self.imputRotateTime = 0
            self.rotar(1)

        if key[pg.K_e] and self.imputRotateTime >= 100:
            self.imputRotateTime = 0
            self.rotar(-1)

        if key[pg.K_r]:
            self.animation = False

        if key[pg.K_t] and not self.animationSequence:
            self.animation = True 

        if key[pg.K_y] and not self.animation and self.imputSequenceTime >= 1000 and not self.animationSequence:
            self.imputSequenceTime = 0
            self.animationSequence = True

        if key[pg.K_z]:
            self.scale(1.2)

        if key[pg.K_x]:
            self.scale(-1.2)

    def update(self , dt):
        if self.animationSequenceEnd:
            self.animationSequence = False
            self.animationSequenceEnd = False
        #self.pos.x , self.pos.y = self.rect.x , self.rect.y
        if self.animation:
            self.AnimationLoop(dt)
        if self.animationSequence:
            self.AnimationSequence(dt,25,0)
        self.limitDisplay()
        #self.limitMomvement(0 , 640 , 150 , 10 )
        self.imput(dt)
        self.move()
        self.pinta()

class Meteor(Base):
    def __init__(self, screen, sprite, howManyRotationsIn360Grades=16, spriteCutWidth=0, spriteCutHeight=0, numColSpriteAnimation=0, numRowSpriteAnimation=1, cordinates=None , scale = 1 ):
        super().__init__(  screen , sprite, howManyRotationsIn360Grades, spriteCutWidth, spriteCutHeight, numColSpriteAnimation, numRowSpriteAnimation, cordinates , scale )


    def update(self , dt ):

        if self.animation:
            self.AnimationLoop(dt)
        self.limitDisplay()
        self.move()
        self.pinta()

class Planet(Base):
    def __init__(self, screen, sprite, howManyRotationsIn360Grades=16, spriteCutWidth=0, spriteCutHeight=0, numColSpriteAnimation=0, numRowSpriteAnimation=1, cordinates=None , scale = 1):
        super().__init__( screen,  sprite, howManyRotationsIn360Grades, spriteCutWidth, spriteCutHeight, numColSpriteAnimation, numRowSpriteAnimation, cordinates , scale )

    def update ( self , dt ):
        #self.pos.x , self.pos.y = self.rect.x , self.rect.y
        if self.animation:
            self.AnimationLoop(dt)
        self.limitDisplay()
        self.move()
        self.pinta()

class Background():
    def __init__ ( self , screen ):
        self.screen = screen
        self.planet = Planet( self.screen , 'static/graphic/planets/estrella_amarilla400x400x25f.png' , 16 , 400 , 400, 25 , 1 , {'pos':(self.screen.get_width()//2 , 50),'vel':(4,0),'dir':(0,0)} , -5 )
        self.imgBackground1 = pg.image.load('static/graphic/background/nevulosa_fria_con_fondo720x640.png' ).convert()
        self.imgBackground1Rect = self.imgBackground1.get_rect()
        self.imgBackground1Pos = pg.math.Vector2((self.imgBackground1Rect.x , self.imgBackground1Rect.y))
        self.imgBackground2 = pg.image.load('static/graphic/background/nevulosa_fria_con_fondo720x640.png' ).convert()
        self.imgBackground2Rect = self.imgBackground2.get_rect()
        self.imgBackground2Pos = pg.math.Vector2((self.imgBackground2Rect.width , self.imgBackground2Rect.y))
        self.estrellas1 = pg.image.load('static/graphic/background/estrellas_polares720x640.png').convert_alpha()
        self.estrellas1Rect = self.estrellas1.get_rect()
        self.estrellas1pos = pg.math.Vector2(self.estrellas1Rect.x , self.estrellas1Rect.y )
        self.estrellas2 = pg.image.load('static/graphic/background/estrellas_polares720x640.png').convert_alpha()
        self.estrellas2Rect = self.estrellas2.get_rect()
        self.estrellas2pos = pg.math.Vector2(self.estrellas2Rect.width , self.estrellas2Rect.y )
        self.vivo = True

    def reset(self):
        self.planet = Planet( self.screen , 'static/graphic/planets/estrella_amarilla400x400x25f.png' , 16 , 400 , 400, 25 , 1 , {'pos':(self.screen.get_width()//2 , 50),'vel':(4,0),'dir':(0,0)} , -5 )
        self.imgBackground1 = pg.image.load('static/graphic/background/nevulosa_fria_con_fondo720x640.png' ).convert()
        self.imgBackground1Rect = self.imgBackground1.get_rect()
        self.imgBackground1Pos = pg.math.Vector2((self.imgBackground1Rect.x , self.imgBackground1Rect.y))
        self.imgBackground2 = pg.image.load('static/graphic/background/nevulosa_fria_con_fondo720x640.png' ).convert()
        self.imgBackground2Rect = self.imgBackground2.get_rect()
        self.imgBackground2Pos = pg.math.Vector2((self.imgBackground2Rect.width , self.imgBackground2Rect.y))
        self.estrellas1 = pg.image.load('static/graphic/background/estrellas_polares720x640.png').convert_alpha()
        self.estrellas1Rect = self.estrellas1.get_rect()
        self.estrellas1pos = pg.math.Vector2(self.estrellas1Rect.x , self.estrellas1Rect.y )
        self.estrellas2 = pg.image.load('static/graphic/background/estrellas_polares720x640.png').convert_alpha()
        self.estrellas2Rect = self.estrellas2.get_rect()
        self.estrellas2pos = pg.math.Vector2(self.estrellas2Rect.width , self.estrellas2Rect.y )
        self.vivo = True

    def update(self , dt ):
        #donde estan
        if self.planet.pos.x + self.planet.rect.width <= 0:
            self.planet.pos.x = self.screen.get_width() + 2000  

        if self.imgBackground1Pos.x + self.imgBackground1Rect.width <= 0:
            self.imgBackground1Pos.x = self.screen.get_width()
        if self.imgBackground2Pos.x + self.imgBackground2Rect.width <= 0:
            self.imgBackground2Pos.x = self.screen.get_width()
        if self.estrellas1pos.x + self.estrellas1Rect.width <= 0:
            self.estrellas1pos.x = self.screen.get_width()
        if self.estrellas2pos.x + self.estrellas2Rect.width <= 0:
            self.estrellas2pos.x = self.screen.get_width()

        #las muevo
        self.planet.dir.x = -1
        self.planet.vel.x = 3
        self.imgBackground1Pos.x += self.imgBackground1Rect.x -0.5
        self.imgBackground2Pos.x += self.imgBackground2Rect.x -0.5
        self.estrellas1pos.x += self.estrellas1Rect.x -1.5
        self.estrellas2pos.x += self.estrellas2Rect.x -1.5

        #las pinto
        self.planet.AnimationLoop(dt)
        self.planet.move()
        self.screen.blit(self.imgBackground1 , self.imgBackground1Pos)
        self.screen.blit(self.imgBackground2 , self.imgBackground2Pos)
        self.screen.blit(self.estrellas1 , self.estrellas1pos)
        self.screen.blit(self.estrellas2 , self.estrellas2pos)
        self.planet.pinta()

