import pygame as pg  
from entities.entities import *

BLACK = (255,255,255,0)
FPS = 60


class Game():
    def __init__(self, W = 640 , H = 480 , titulo='ejemplo'):
        self.pantalla =  pg.display.set_mode((W,H))
        pg.display.set_caption(titulo)
        #self.nave = Base(self.pantalla , 'static\graphic\planeta_ejemplo.png' , 16 , 200 , 200, 50 )
        self.nave = Base(self.pantalla , 'static\graphic\Spritesheet-nave.png' , 16 , 44 , 44 , 16 )
        #self.nave = Base(self.pantalla , 'static\graphic\_nave_ejemplo.png' )
        self.reloj = pg.time.Clock()

    def bbp(self):
        while True:
            dt = self.reloj.tick(FPS)
            self.pantalla.fill((0,0,0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                #if event.type == pg.KEYDOWN:
                #    if event.key == pg.K_f:
                #        self.nave.giro180()

            self.nave.update( dt )
            pg.display.update()

if __name__ == '__main__':
    pg.init()
    game = Game()
    game.bbp()
    pg.quit()
