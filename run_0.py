from operator import truediv
import pygame as pg  
from entities.entities import *

BLACK = (255,255,255,0)
FPS = 60


class Game():
    def __init__(self, W = 640 , H = 480 , titulo='ejemplo'):
        self.pantalla =  pg.display.set_mode((W,H))
        pg.display.set_caption(titulo)
        #self.nave = ejemplo(self.pantalla , 'static\graphic\planeta_ejemplo.png' , 200 , 200, 50 )
        self.nave = ejemplo(self.pantalla , 'static\graphic\_nave_ejemplo.png')
        self.reloj = pg.time.Clock()
        
    def bbp(self):
        while True:
            dt = self.reloj.tick(FPS)
            self.pantalla.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                #if event.type == pg.KEYDOWN:
                #    if event.key == pg.K_f:
                #        self.nave.giro180()
                '''
                key = pg.key.get_pressed()
                if key[pg.K_RIGHT]:
                    self.nave.dir.x += 1 
                elif key[pg.K_LEFT]:
                    self.nave.dir.x -= 1 
                else:
                    self.nave.dir.x = 0 

                if key[pg.K_UP]:
                    self.nave.dir.y -= 1
                elif key[pg.K_DOWN]:
                    self.nave.dir.y += 1 
                else:
                    self.nave.dir.y = 0

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_d:
                        self.nave.dir.x = 1
                    if event.key == pg.K_a:
                        self.nave.dir.x = -1

                if event.type == pg.KEYUP:
                    if event.key == pg.K_d:
                        self.nave.dir.x = 0
                    if event.key == pg.K_a:
                        self.nave.dir.x = 0
                '''
            self.nave.update( dt )
            pg.display.update()

if __name__ == '__main__':
    pg.init()
    game = Game()
    game.bbp()
    pg.quit()
