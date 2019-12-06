# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 11:56:24 2019

@author: albii
"""

import pyxel
#import random
class Sprite:
    def __init__(self, x, y):
        if isinstance(x, int):
            self.posx = x
        if isinstance(y, int):
            self.posy = y
       
class Barril (Sprite) :
    def __init__(self, vidas=1):
        self.vidas = vidas
       
class Mario(Sprite):
    def __init__(self, x, y, v, vidas = 3):
        Sprite.__init__(self, x, y)
        self.vidas = vidas
        self.v = v
    def DibujarMario(self):
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            pyxel.blt(self.posx-8, self.posy-16, 0, 240, 19, 16, 17, 3)
        elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            pyxel.blt(self.posx-8, self.posy-16, 0, 0, 0, 16, 17, 3)
        elif (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W)) or (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S)):
            pyxel.blt(self.posx-8, self.posy-16, 0, 96, 20, 16, 17, 3)
        else:
            pyxel.blt(self.posx-8, self.posy-16, 0, 240, 19, 16, 17, 3)
           
       
class DonkeyKong(Sprite):
    def __init__ (self, x, y):
        Sprite.__init__(self, x,y)
    def PintarDonkeykong(self):
        pyxel.blt(self.posx, self.posy, 1, 0, 0, 45, 39, 3)
        
        
class Rampa(Sprite):
    def __init__(self, x, y, Vary, recto, pendiente):
       Sprite.__init__(self, x, y)
       self.Vary = Vary
       self.lista = []
       self.recto = recto
       self.pendiente = pendiente
    def CrearRampa(self):
       for i in range(self.recto):
            self.posx += 16
            self.lista.append((self.posx,self.posy))
       for i in range(self.pendiente):
            self.posx += 16
            self.posy += self.Vary
            self.lista.append((self.posx, self.posy)) 
    def DibujarRampa(self):
        for i in self.lista :
            self.posx = i[0]
            self.posy = i[1]
            pyxel.blt(self.posx, self.posy, 0, 235, 102, 17, 9, 3)

        
class Escalera(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self, x, y)
    def PintarEscalera(self):
        pyxel.blt(self.posx, self.posy-17, 0, 120,236,11,17,3)          

    
    
class Pauline(Sprite):
    pass
class Mapa():
    def __init__(self):
        self.M = Mario(8, 247, 0.02)
        self.RamAbajo = Rampa(-16, 247, -1, 7, 7)
        self.Ram2 = Rampa(-16, 205, 1, 0, 13)
        self.Ram3 = Rampa(0, 185, -1, 0, 13)
        self.Ram4 = Rampa(-16, 138, 1, 0, 13)
        self.Ram5 = Rampa(-0, 117, -1, 0, 13)
        self.RamArriba = Rampa(-16, 78, 1, 9, 4)
        self.RamRecta = Rampa(70, 50, 0, 3, 0)
        self.Rampas = [self.RamAbajo, self.RamArriba, self.Ram2, self.Ram3, self.Ram4, self.Ram5, self.RamRecta]
        self.Escaleras =[Escalera(80, 255),
                         Escalera(80, 228),
                         
                         Escalera(180,244),
                         Escalera(180, 236),
                         
                         Escalera(100, 213),
                         Escalera(100, 201),
                         
                         Escalera(32,211),
                         Escalera(32, 207),
                         
                         Escalera(64, 190),
                         Escalera(64, 160),
                         
                         Escalera(115, 180),
                         Escalera(115, 168),
                         
                         Escalera(180,176),
                         Escalera(180, 172),
                         
                         Escalera(160, 125),
                         Escalera(160, 155),
                         
                         Escalera(72, 147),
                         Escalera(72, 135),
                         
                         Escalera(32,142),
                         Escalera(32,138),
                         
                         Escalera(87, 120),
                         Escalera(87, 95),
                         
                         Escalera(180, 108),
                         Escalera(180, 104),
                         
                         Escalera(124, 80),
                         Escalera(124, 72),
                         
                         Escalera(76,80),
                         Escalera(76,68),
                         Escalera(76,56),
                         
                         Escalera(60,80), 
                         Escalera(60,68),
                         Escalera(60,56)]
    def Desplazarse(self):
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            for k in self.Rampas:
                for j in k.lista:
                    # self.posx-8, self.posy-16
                    if (self.M.posx - j[0] <= 15) and (self.M.posx - j[0] >= 0):   
                        self.M.posy -= k.Vary
                    self.M.posx += self.M.v
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            for k in self.Rampas:
               for j in k.lista:
                   if (j[1]) == self.M.posy: 
                       for i in self.Rampas:  
                           self.M.posx -= self.M.v
                           self.M.posy += i.Vary 
    def Subir(self):
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            for i in self.Escaleras:
                if (i.posx) == self.M.posx:
                    self.M.posy -= 4 
        
        
        
        
             
            
class App:
    def __init__(self):
        self.mapa = Mapa()
        self.Don = DonkeyKong(17, 40)
        for i in self.mapa.Rampas:
            i.CrearRampa()
        pyxel.init(224, 256, caption = "Donkey Kong", fps = 60)
        pyxel.load("assets/my_resource.pyxres")
        pyxel.run(self.update, self.draw)
      
    def update(self):
        self.mapa.Desplazarse()
        self.mapa.Subir()
    def draw(self):
        pyxel.cls(0)
        pyxel.text(0, 0, ( "vidas: " + str(self.mapa.M.vidas) ), 8)
        for i in self.mapa.Escaleras:
            i.PintarEscalera()
        self.mapa.M.DibujarMario()
        for k in self.mapa.Rampas:
            k.DibujarRampa()
        self.Don.PintarDonkeykong()
        
        
      
App()