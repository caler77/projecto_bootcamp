import sqlite3 as sql

def createDB():
    con = sql.connect('data/juegosDB.db')
    cur = con.cursor()
    con.commit()
    cur.execute(
        '''CREATE TABLE records(
            name text,
            level interger,
            puntuacion interger
        )
        '''
    )
    con.commit()
    for i in range(5):
        cur.execute(
            '''INSERT INTO records VALUES('___',0,0)
            '''
        )
        con.commit()
    con.commit()
    con.close()

def insertDB(nombre,level,puntuacion):
    con = sql.connect('data/juegosDB.db')
    cur = con.cursor()
    cur.execute(
        f'''INSERT INTO records VALUES('{nombre}',{level},{puntuacion})
        '''
    )
    con.commit()
    con.close()

def readDB():
    con = sql.connect('data/juegosDB.db')
    cur = con.cursor()
    cur.execute(
        '''SELECT name ,level, puntuacion  FROM records ORDER BY puntuacion DESC LIMIT 5
        '''
    )
    datos = cur.fetchall()
    con.close()
    return datos