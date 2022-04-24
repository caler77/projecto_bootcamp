import random as rd
import pygame as pg  
from entities.entities import *
from data.config.config import *
from data.controller import *

def createLevel( level , sprite_size , sprite_frame , sprite , grupo , pantalla ,vel = None):
    margen = sprite_size // 10
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

class Level1():
    def __init__(self, W = 720 , H = 720 , titulo='ejemplo'):
        self.pantalla =  pg.display.set_mode((W,H))
        pg.display.set_caption(titulo)
        self.nave = Jugador( self.pantalla , 'static/graphic/space_ship/naveAzul_sheet.png' , 16 , 128 , 128 , 26 , 1 , {'pos':(0,self.pantalla.get_height()//2 - 128),'vel':(1,1),'dir':(0,0)}  )
        self.background = Background(self.pantalla)
        self.reloj = pg.time.Clock()
        self.asteroides = pg.sprite.Group()
        self.game_over = False
        createLevel(LEVEL1_200x200,200,50,'static/graphic/meteor/meteorito_rojo200x200x50f.png', self.asteroides , self.pantalla , (2.5,1))
        createLevel(LEVEL1_100x100,100,60,'static/graphic/meteor/meteoritosazules_100x100x60f.png', self.asteroides , self.pantalla , (3,1))
        createLevel(LEVEL1_50x50,50,60,'static/graphic/meteor/meteoritosverdes_50x50x60f.png', self.asteroides , self.pantalla , (4,1))

    def bbp(self , nombre):

        while True:
            dt = self.reloj.tick(FPS) 
            self.pantalla.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if self.nave.vidas <= 0:
                    return False
                if self.game_over:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            try:
                                insertDB(nombre,1,self.nave.score_player)
                            except:
                                createDB()
                                insertDB(nombre,1,self.nave.score_player)
                            return True
                        if event.key == pg.K_BACKSPACE:
                            createLevel(LEVEL1_200x200,200,50,'static/graphic/meteor/meteorito_rojo200x200x50f.png', self.asteroides , self.pantalla , (2.5,1))
                            createLevel(LEVEL1_100x100,100,60,'static/graphic/meteor/meteoritosazules_100x100x60f.png', self.asteroides , self.pantalla , (3,1))
                            createLevel(LEVEL1_50x50,50,60,'static/graphic/meteor/meteoritosverdes_50x50x60f.png', self.asteroides , self.pantalla , (4,1))
                            self.game_over = False
                        if event.key == pg.K_m:
                            try:
                                insertDB(nombre,1,self.nave.score_player)
                            except:
                                createDB()
                                insertDB(nombre,1,self.nave.score_player)
                            return True

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
                muestra_texto_center(self.pantalla, consolas, 'Pulsa "esc" para ir al menu \n Pulsa "DELETE" para repetir' , GREEN , 20 , self.pantalla.get_width()//2 , 700 )
            else:
                muestra_texto_center(self.pantalla, consolas, 'LEVEL 1' , RED , 20 , self.pantalla.get_width()//2 , 680 )
            pg.display.update()
            pg.event.clear()

class Level2():

    def __init__(self, W = 720 , H = 720 , titulo='ejemplo'):
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

    def bbp(self , nombre ):
        while True:
            dt = self.reloj.tick(FPS) 
            self.pantalla.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if self.nave.vidas <= 0:
                    return False
                if self.game_over:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            try:
                                insertDB(nombre,1,self.nave.score_player)
                            except:
                                createDB()
                                insertDB(nombre,1,self.nave.score_player)
                            return True
                        if event.key == pg.K_BACKSPACE:
                            createLevel(LEVEL2_200x200,200,50,'static/graphic/meteor/meteorito_rojo200x200x50f.png', self.asteroides , self.pantalla , (2.5,1))
                            createLevel(LEVEL2_100x100,100,60,'static/graphic/meteor/meteoritosazules_100x100x60f.png', self.asteroides , self.pantalla , (3,1))
                            createLevel(LEVEL2_50x50,50,60,'static/graphic/meteor/meteoritosverdes_50x50x60f.png', self.asteroides , self.pantalla , (4,1))
                            insertDB()
                            self.game_over = False
                        if event.key == pg.K_m:
                            try:
                                insertDB(nombre,1,self.nave.score_player)
                            except:
                                createDB()
                                insertDB(nombre,1,self.nave.score_player)
                            return True

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
            else:
                muestra_texto_center(self.pantalla, consolas, 'LEVEL 2' , RED , 20 , self.pantalla.get_width()//2 , 680 )
            pg.display.update()
            pg.event.clear()

class Level3():
    def __init__(self, W = 720 , H = 720 , titulo='ejemplo'):
        self.pantalla =  pg.display.set_mode((W,H))
        pg.display.set_caption(titulo)
        self.nave = Jugador( self.pantalla , 'static/graphic/space_ship/naveAzul_sheet.png' , 16 , 128 , 128 , 26 , 1 , {'pos':(0,self.pantalla.get_height()//2 - 128),'vel':(1,1),'dir':(0,0)}  )
        self.background = Background(self.pantalla)
        self.reloj = pg.time.Clock()
        self.asteroides = pg.sprite.Group()
        self.game_over = False
        createLevel(LEVEL3_200x200,200,50,'static/graphic/meteor/meteorito_rojo200x200x50f.png', self.asteroides , self.pantalla , (2.5,1))
        createLevel(LEVEL3_100x100,100,60,'static/graphic/meteor/meteoritosazules_100x100x60f.png', self.asteroides , self.pantalla , (3,1))
        createLevel(LEVEL3_50x50,50,60,'static/graphic/meteor/meteoritosverdes_50x50x60f.png', self.asteroides , self.pantalla , (4,1))


    def bbp(self,nombre):

        while True:
            dt = self.reloj.tick(FPS) 
            self.pantalla.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if self.nave.vidas <= 0:
                    return False
                if self.game_over:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            try:
                                insertDB(nombre,1,self.nave.score_player)
                            except:
                                createDB()
                                insertDB(nombre,1,self.nave.score_player)
                            return True
                        if event.key == pg.K_BACKSPACE:
                            createLevel(LEVEL3_200x200,200,50,'static/graphic/meteor/meteorito_rojo200x200x50f.png', self.asteroides , self.pantalla , (2.5,1))
                            createLevel(LEVEL3_100x100,100,60,'static/graphic/meteor/meteoritosazules_100x100x60f.png', self.asteroides , self.pantalla , (3,1))
                            createLevel(LEVEL3_50x50,50,60,'static/graphic/meteor/meteoritosverdes_50x50x60f.png', self.asteroides , self.pantalla , (4,1))
                            self.game_over = False
                        if event.key == pg.K_m:
                            try:
                                insertDB(nombre,1,self.nave.score_player)
                            except:
                                createDB()
                                insertDB(nombre,1,self.nave.score_player)
                            return True

            #para calcular el offset de la collision de mascaras se le resta a la posicion de la mascara del obstaculo conttra las posicion del que choca 
            #if self.nave.mask.overlap(self.planet.mask , (int( self.planet.pos.x - self.nave.pos.x ), int( self.planet.pos.y - self.nave.pos.y ))):
            #    print('toca')
            #else:
            #    print('no toca')

            #Colision 
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
            else:
                muestra_texto_center(self.pantalla, consolas, 'LEVEL 3' , RED , 20 , self.pantalla.get_width()//2 , 680 )
            pg.display.update()
            pg.event.clear()

class Game_over():
    def __init__(self, level , W = 720 , H = 640 , titulo='ejemplo'):
        self.pantalla =  pg.display.set_mode((W,H))
        pg.display.set_caption(titulo)
        self.background = Background(self.pantalla)
        self.reloj = pg.time.Clock()
        self.level = level

    def bbp(self):

        while True:
            dt = self.reloj.tick(FPS) 
            self.pantalla.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.background.reset()
                        return False
                    if event.key == pg.K_BACKSPACE:
                        self.background.reset()
                        return True 

            self.background.update(dt)
            muestra_texto_center(self.pantalla , consolas , 'GAME OVER' , RED , 50 , self.pantalla.get_width()//2 , self.pantalla.get_height()//2)
            muestra_texto_center(self.pantalla , consolas , 'Pulsa "ESC" para volver' , RED , 10 , self.pantalla.get_width()//2 , self.pantalla.get_height()//2 + 60)
            muestra_texto_center(self.pantalla , consolas , 'Pulsa "DELETE" para repetir' , RED , 10 , self.pantalla.get_width()//2 , self.pantalla.get_height()//2 + 80)
            pg.display.update()
            pg.event.clear()

class Menu():
    def __init__(self , W = 720 , H = 640 , titulo='ejemplo'):
        self.pantalla =  pg.display.set_mode((W,H))
        pg.display.set_caption(titulo)
        self.background = Background(self.pantalla)
        self.reloj = pg.time.Clock()

    def bbp(self):

        while True:
            color = rd.choice(COLORS)
            dt = self.reloj.tick(FPS) 
            self.pantalla.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pass
                    if event.key == pg.K_BACKSPACE:
                        pass
                    if event.key == pg.K_1 or event.key == pg.K_KP_1:
                        return 1
                    if event.key == pg.K_2 or event.key == pg.K_KP_2:
                        return 2
                    if event.key == pg.K_3 or event.key == pg.K_KP3:
                        return 3
                    if event.key == pg.K_d:
                        return 'datos'
                    if event.key == pg.K_c:
                        return 'nombre'

            self.background.update(dt)
            muestra_texto_center(self.pantalla, consolas, 'ESQUIVA EL ASTEROIDE' , color , 50 , self.pantalla.get_width()//2 , 100 )
            muestra_texto_center(self.pantalla,consolas,'Pulsa "1" para seleccionar el nivel 1',RED,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2)
            muestra_texto_center(self.pantalla,consolas,'Pulsa "2" para seleccionar el nivel 2',RED,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2 + 30)
            muestra_texto_center(self.pantalla,consolas,'Pulsa "3" para seleccionar el nivel 3',RED,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2 + 60)
            muestra_texto_center(self.pantalla,consolas,'Pulsa "d" para seleccionar la pantalla de datos',GREEN,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2 + 200)
            muestra_texto_center(self.pantalla,consolas,'Pulsa "c" para ir a configuracion',GREEN,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2 + 220)
            pg.display.update()
            pg.event.clear()

class Datos():
    def __init__(self , W = 720 , H = 640 , titulo='ejemplo'):
        self.pantalla =  pg.display.set_mode((W,H))
        pg.display.set_caption(titulo)
        self.background = Background(self.pantalla)
        self.reloj = pg.time.Clock()
        try:
            datos = readDB()
            self.datos = datos
        except:
            createDB()
            datos = readDB()
            self.datos = datos

    def bbp(self):

        while True:
            color = rd.choice(COLORS)
            dt = self.reloj.tick(FPS) 
            self.pantalla.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return True
                    if event.key == pg.K_BACKSPACE:
                        pass

            self.background.update(dt)
            muestra_texto_center(self.pantalla,consolas,'RECORDS',color,50,self.pantalla.get_width()//2,100)
            muestra_texto_center(self.pantalla,consolas,f'1º |nombre: {self.datos[0][0]} | level: {self.datos[0][1]} | puntuacion: {self.datos[0][2]} ',color,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2 - 10)
            muestra_texto_center(self.pantalla,consolas,f'2º |nombre: {self.datos[1][0]} | level: {self.datos[1][1]} | puntuacion: {self.datos[1][2]} ',color,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2 + 20)
            muestra_texto_center(self.pantalla,consolas,f'3º |nombre: {self.datos[2][0]} | level: {self.datos[2][1]} | puntuacion: {self.datos[2][2]} ',color,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2 + 50)
            muestra_texto_center(self.pantalla,consolas,f'4º |nombre: {self.datos[3][0]} | level: {self.datos[3][1]} | puntuacion: {self.datos[3][2]} ',color,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2 + 80)
            muestra_texto_center(self.pantalla,consolas,f'5º |nombre: {self.datos[4][0]} | level: {self.datos[4][1]} | puntuacion: {self.datos[4][2]} ',color,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2 + 110)
            muestra_texto_center(self.pantalla,consolas,'Pulsa "ESC" para seleccionar el menu',BLUE,20,self.pantalla.get_width()//2,self.pantalla.get_height()//2 + 200)
            pg.display.update()
            pg.event.clear()

class PideNombre():
    def __init__(self , W = 720 , H = 640 , titulo='ejemplo'):
        self.pantalla =  pg.display.set_mode((W,H))
        pg.display.set_caption(titulo)
        self.background = Background(self.pantalla)
        self.reloj = pg.time.Clock()
        self.nombre = []

    def bbp(self):

        while True:
            color = rd.choice(COLORS)
            dt = self.reloj.tick(FPS) 
            self.pantalla.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    return [True , self.nombre ]

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.nombre = self.nombre[:-1]
                    else:
                        self.nombre += event.unicode

                    if len(self.nombre) > 3:
                        self.nombre = self.nombre[:3]

            self.background.update(dt)
            muestra_texto_center(self.pantalla, consolas , f'Introduce tu nombre : {"".join(self.nombre)}', WHITE , 20 , self.pantalla.get_width()//2 , self.pantalla.get_height()//2)
            muestra_texto_center(self.pantalla, consolas , 'dale al "ENTER" para confirmar el nombre', color , 20 , self.pantalla.get_width()//2 , self.pantalla.get_height()//2 + 30)
            muestra_texto_center(self.pantalla, consolas , 'INSTRUCCIONES', color , 30 , self.pantalla.get_width()//2 , 50)
            muestra_texto_center(self.pantalla, consolas , '"w" "a" "s" "d" para mover la nave', GREEN , 20 , self.pantalla.get_width()//2 , 90)
            muestra_texto_center(self.pantalla, consolas , '"q" "e" para rotar la nave', GREEN , 20 , self.pantalla.get_width()//2 , 110)
            muestra_texto_center(self.pantalla, consolas , '"z" para aumentar la nave', GREEN , 20 , self.pantalla.get_width()//2 , 130)
            muestra_texto_center(self.pantalla, consolas , '"x" para disminuir nave', GREEN , 20 , self.pantalla.get_width()//2 , 150)
            muestra_texto_center(self.pantalla, consolas , 'los metodos de escalado y rotacion pueden tardar un poco disculpen molestias', WHITE , 10 , self.pantalla.get_width()//2 , 170)
            pg.display.update()
            pg.event.clear()
