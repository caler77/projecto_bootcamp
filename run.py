import pygame as pg  
from entities.entities import *
from data.config.config import *

def createLevel( level , sprite_size , sprite_frame , sprite , grupo , pantalla ,vel = None):
    margen = sprite_size // 20
    widht , height = pg.display.get_window_size()
    if vel == None:
        vel = (1,1)
    else:
        vel = vel
    for index_row ,row in enumerate(level):
        for index_col ,col in enumerate(row):
            x = (widht + margen) + ( sprite_size * index_col ) + margen
            y = ( sprite_size * index_row ) + margen
            if col == 0:
                pass
            if col == 1 or col == 'h':
                asteroide  = Meteor(pantalla , sprite , 16 , sprite_size , sprite_size , sprite_frame , 1 , {'pos':(x,y) , 'vel': vel , 'dir' : (-1,0)} , 1) 
                grupo.add(asteroide)



class Game():
    def __init__(self, W = 720 , H = 640 , titulo='ejemplo'):
        pg.init()
        self.pantalla =  pg.display.set_mode((W,H))
        pg.display.set_caption(titulo)
        #self.planet = Planet(self.pantalla , 'static/graphic/planets/planeta_ejemplo.png' , 16 , 200 , 200, 50 , 1 , {'pos':(self.pantalla.get_width()//2 - 100, self.pantalla.get_height()//2 - 100),'vel':(4,0),'dir':(0,0)} , -2)
        self.nave = Jugador( self.pantalla , 'static/graphic/space_ship/naveAzul_sheet.png' , 16 , 128 , 128 , 26 , 1 , {'pos':(0,self.pantalla.get_height()//2 - 128),'vel':(1,1),'dir':(0,0)}  )
        #self.nave = Jugador(self.pantalla , 'static/graphic/space_ship/_nave_ejemplo.png' )
        self.background = Background(self.pantalla)
        self.reloj = pg.time.Clock()
        self.asteroides = pg.sprite.Group()
        self.game_over = False
        createLevel(LEVEL2_200x200,200,50,'static/graphic/meteor/meteorito_rojo200x200x50f.png', self.asteroides , self.pantalla , (2.5,1))
        createLevel(LEVEL2_100x100,100,60,'static/graphic/meteor/meteoritosazules_100x100x60f.png', self.asteroides , self.pantalla , (3,1))
        createLevel(LEVEL2_50x50,50,60,'static/graphic/meteor/meteoritosverdes_50x50x60f.png', self.asteroides , self.pantalla , (4,1))


    def createLevel(self , level , sprite_size , sprite_frame , sprite , grupo ,vel = None):
        margen = sprite_size // 10
        if vel == None:
            vel = (1,1)
        else:
            vel = vel
        for index_row ,row in enumerate(level):
            for index_col ,col in enumerate(row):
                x = (self.pantalla.get_width() + margen) + ( sprite_size * index_col ) + margen
                y = ( sprite_size * index_row ) + margen
                if col == 0:
                    pass
                if col == 1 or col == 'h':
                    meteor = Meteor(self.pantalla , sprite , 16 , sprite_size , sprite_size , sprite_frame , 1 , {'pos':(x,y) , 'vel': vel , 'dir' : (-1,0)} , 1) 
                    grupo.add(meteor)

    def bbp(self):

        while True:
            dt = self.reloj.tick(FPS) 
            self.pantalla.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if self.nave.vidas <= 0:
                    self.pantalla.fill(BLACK)
                    muestra_texto_center(self.pantalla,consolas,'GAME OVER',RED,50,720//2,640//2)
                    pg.display.update()
                    pg.time.delay(10000)
                    pg.quit()

                if self.game_over:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            pg.quit()
                        if event.key == pg.K_BACKSPACE:
                            createLevel(LEVEL2_200x200,200,50,'static/graphic/meteor/meteorito_rojo200x200x50f.png', self.asteroides , self.pantalla , (2.5,1))
                            createLevel(LEVEL2_100x100,100,60,'static/graphic/meteor/meteoritosazules_100x100x60f.png', self.asteroides , self.pantalla , (3,1))
                            createLevel(LEVEL2_50x50,50,60,'static/graphic/meteor/meteoritosverdes_50x50x60f.png', self.asteroides , self.pantalla , (3.5,1))
                            self.game_over = False

                #if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                #    if event.mod == pg.KMOD_NONE:
                #        print('No modifier keys were in a pressed state when this '
                #            'event occurred.')
                #    else:
                #        if event.mod & pg.KMOD_LSHIFT:
                #            print('Left shift was in a pressed state when this event '
                #                'occurred.')
                #        if event.mod & pg.KMOD_RSHIFT:
                #            print('Right shift was in a pressed state when this event '
                #                'occurred.')
                #        if event.mod & pg.KMOD_SHIFT:
                #            print('Left shift or right shift or both were in a '
                #                'pressed state when this event occurred.')

            #para calcular el offset de la collision de mascaras se le resta a la posicion de la mascara del obstaculo conttra las posicion del que choca 
            #if self.nave.mask.overlap(self.planet.mask , (int( self.planet.pos.x - self.nave.pos.x ), int( self.planet.pos.y - self.nave.pos.y ))):
            #    print('toca')
            #else:
            #    print('no toca')

            for sprite in self.asteroides:
                if self.nave.mask.overlap( sprite.mask , (int(sprite.pos.x - self.nave.pos.x),int(sprite.pos.y - self.nave.pos.y))):
                    self.nave.reset()
                    self.nave.score_player = 0
                    self.nave.vidas -= 1
                    sprite.kill()
                if 'left' in sprite.dir_hit_display and sprite.pos.x + sprite.rect.width <= 0:
                    sprite.kill()
                    self.nave.score_player += 1
                if self.asteroides.sprites() == []:
                    self.game_over = True

            self.background.update(dt)
            #self.planet.update(dt)
            self.asteroides.update(dt)
            self.nave.limitMomvement(0 , 640 , 150 , 10 )
            self.nave.update(dt)
            muestra_texto_top(self.pantalla , consolas , f'Puntuacion: {str(self.nave.score_player)}', WHITE , 20 , 5 , 640)
            muestra_texto_top(self.pantalla , consolas , f'Vidas: {str(self.nave.vidas)}', WHITE , 20 , 5 , 660)
            if self.game_over:
                muestra_texto_center(self.pantalla, consolas, 'has ganado' , RED , 20 , self.pantalla.get_width()//2 , 680 )
                muestra_texto_center(self.pantalla, consolas, 'Pulsa "esc" para salir \n Pulsa "DELETE" para repetir' , GREEN , 20 , self.pantalla.get_width()//2 , 700 )
            pg.display.update()
            pg.event.clear()
            print(self.nave.score_player)


if __name__ == '__main__':
    pg.init()
    game = Game( 720 , 720 , 'pruevita')
    game.bbp()
    pg.quit()
