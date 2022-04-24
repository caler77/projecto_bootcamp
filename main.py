from pickle import TRUE
from posixpath import join
from re import M, T
from escenes.escenes import *
import pygame as pg  

pg.init()

game = PideNombre(titulo='pide nombre')
resultado = game.bbp()
if resultado[0]:
    nombre = ''.join(resultado[1])
    game = Menu(titulo='jueguito')
    selec_level = game.bbp()
while True:
    if selec_level == 1:
        level = Level1(titulo='LEVEL 1 Jueguito')
        resultado = level.bbp(nombre)
        if resultado == True:
            game = Menu(titulo='Menu')
            selec_level = game.bbp()
        if resultado == False:
            escene = Game_over(1)
            if escene.bbp():
                level = Level1(titulo='LEVEL 1 Jueguito')
                level.bbp(nombre)
            if not escene.bbp():
                game = Menu(titulo='jueguito')
                selec_level = game.bbp()

    if selec_level == 2:
        level = Level2(titulo='LEVEL 2 Jueguito')
        resultado = level.bbp(nombre)
        if resultado == True:
            game = Menu(titulo='Menu')
            selec_level = game.bbp()
        if resultado == False:
            escene = Game_over(1)
            if escene.bbp():
                level = Level2(titulo='LEVEL 2 Jueguito')
                level.bbp(nombre)
            if not escene.bbp():
                game = Menu(titulo='jueguito')
                selec_level = game.bbp()


    if selec_level == 3:
        level = Level3(titulo='LEVEL 3 Jueguito')
        resultado = level.bbp(nombre)
        if resultado == True:
            game = Menu(titulo='Menu')
            selec_level = game.bbp()
        if resultado == False:
            escene = Game_over(1)
            if escene.bbp():
                level = Level3(titulo='LEVEL 3 Jueguito')
                level.bbp(nombre)
            if not escene.bbp():
                game = Menu(titulo='jueguito')
                selec_level = game.bbp()

    if selec_level == 'datos':
        datos = Datos(titulo='Datos')
        resultado = datos.bbp()
        if resultado == True:
            game = Menu(titulo='Menu')
            selec_level = game.bbp()

    if selec_level == 'nombre':
        nombre = PideNombre(titulo='pide nombre')
        resultado = nombre.bbp()
        if resultado[0]:
            nombre = ''.join(resultado[1])
            game = Menu(titulo='jueguito')
            selec_level = game.bbp()






