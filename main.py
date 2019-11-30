import pyxel

# CONFIG
HEIGHT = 100
WIDTH = 120
FPS = 60
#

class Sprite:
	'''
	Especifica como se va a recortar un sprite del banco de imagenes principal
	'''
	def __init__(self, region_from, region_to, bank, transparent=None):
		self.region_from = region_from # (x, y)
		self.region_to = region_to # (x, y)
		self.size = (region_to[0]-region_from[0], region_to[1]-region_from[1])
		self.bank = bank # Banco de imagenes
		self.transparent = transparent # Color de transparencia, si se especifica

class Entity:
	'''
	Define una Entidad que tiene una posición en x, una posición en y,
	una imagen y a la que le afecta una aceleración en el eje y que hace que caiga: La gravedad.
	'''
	def __init__(self, x, y, gravity=9.8):
		self.x = x
		self.y = y
		self.vel_y = 0
		self.gravity = gravity
		self.init_sprites()
	
	def changeX(self, val):
		self.x += val

	def changeY(self, val):
		self.y += val
	
	def setY(self, val):
		self.y = val
	
	def getGravity(self):
		return self.gravity
	
	def getY(self):
		return self.y
	
	def setVelY(self, val):
		self.vel_y = val
	
	def getVelY(self):
		return self.vel_y
	
	def changeVelY(self, val):
		self.vel_y += val

	def setSprite(self, sprite):
		self.sprite_name = sprite
		self.sprite = self.sprites[sprite]
	
	def getSprite(self):
		return self.sprite_name

class Mario(Entity):
	'''
	Mario, el personaje principal
	'''
	def init_sprites(self):
		self.sprites = {
			'right1':Sprite((242, 20), (254, 35), 0, 3),
			'right2':Sprite((216, 20), (230, 35), 0, 3),
			'right3':Sprite((192, 21), (207, 35), 0, 3),
			'left1':Sprite((2, 1), (13, 16), 0, 3),
			'left2':Sprite((25, 1), (39, 16), 0, 3),
			'left3':Sprite((49, 2), (63, 16), 0, 3)
		}

class DonkeyKong(Entity):
	'''
	Donkey Kong, el enemigo principal del juego
	'''
	def init_sprites(self):
		pass

class Barril(Entity):
	'''
	Los barriles son los proyectiles que Mario tiene que esquivar 
	'''
	def init_sprites(self):
		pass

class Pauline(Entity):
	'''
	Pauline, la princesa que Mario tiene que rescatar
	'''
	def init_sprites(self):
		pass

class Escalera(Entity):
	'''
	Las escaleras del mapa
	'''
	def init_sprites(self):
		self.sprites = {
			'escalera':None
		}

class Platarforma(Entity):
	'''
	Las plataformas del mapa
	'''
	def init_sprites(self):
		pass

class Map():
	def __init__(self):
		self.escaleras = [] # DE TIPO Escalera
		self.plataformas = [] # DE TIPO Plataforma
		self.mario = Mario( WIDTH/2, HEIGHT-1, 9.8)
		self.mario.setSprite('right1') # sprite inicial

		#TODO:
		# self.donkey
		# self.pauline
		# ... etc

class Game:
	'''
	El juego (pyxel)
	'''
	
	def __init__(self):
		self.jumping = False
		self.map = Map()
		pyxel.init(WIDTH, HEIGHT, caption='Donkey Kong', fps=FPS) # Inicializa pyxel
		pyxel.load('assets/my_resource.pyxres') # Banco de imagenes
		pyxel.run(self.update, self.draw) # Ejecuta pyxel con las funciones update y draw definidas en esta misma clase
		
	def update(self):
		# La variable turn es el turno, lo que establece cual de los
		# 3 sprites usar en mario cuando esta corriendo.
		turn = int(pyxel.frame_count%30 / 10) + 1

		# ----------------MOVIMIENTO DE MARIO-------------------
		if (pyxel.btn(pyxel.KEY_RIGHT)): # si se pulsa la flecha derecha
			self.map.mario.changeX(1) # se le da a mario velocidad en x para la derecha
			if not self.jumping: # Si no está saltando
				self.map.mario.setSprite('right' + str(turn)) # Actualiza el sprite
			else:
				self.map.mario.setSprite('right2') # si está saltando simplemente gira

		if (pyxel.btn(pyxel.KEY_LEFT)): # si en cambio se pulsa la izquierda
			self.map.mario.changeX(-1) # se le da velocidad para la izquierda
			if not self.jumping: # Si no está saltando
				self.map.mario.setSprite('left' + str(turn)) # Actualiza el sprite
			else:
				self.map.mario.setSprite('left2') # si está saltando simplemente gira
			
		if (pyxel.btn(pyxel.KEY_SPACE)) and not self.jumping:
			self.jumping = True # comienza a saltar
			self.map.mario.setVelY(-3.5) # le da velocidad a mario pa que salte
			self.map.mario.setSprite(self.map.mario.getSprite()[:-1] + '2') # pasa al sprite de salto, el 2

		# Si no se esta moviendo, pasa al sprite 1, el de que está de pie.
		# Si no hiciese esto, se quedaria quieto en una posición de estar corriendo, lo cual queda feo.
		if not self.jumping and not(pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT)):
			self.map.mario.setSprite(self.map.mario.getSprite()[:-1] + '1')

		# CAIDA DE MARIO
		self.map.mario.changeVelY(self.map.mario.getGravity()/FPS) # la gravedad le afecta (gravedad por segundo --> gravedad/frame por frame)
		if self.map.mario.getY() + self.map.mario.getVelY() >= HEIGHT-1: # si toca el suelo
			self.map.mario.setY(HEIGHT-1) # se queda en el suelo
			self.map.mario.setVelY(0) # se para
			self.jumping = False # ya no está saltando
		else:
			self.map.mario.changeY(self.map.mario.getVelY()) # si no, sigue saltando o cayendo
		# ------------------------------------------------------------
	
	def draw(self):
		pyxel.cls(0) # Limpia la pantalla, todo a negro
		
		pyxel.blt( # Dibuja a Mario
			self.map.mario.x-5, # -5 centra la posición teórica de mario.
			self.map.mario.y-14, # -14 pone la posición en sus pies.
			self.map.mario.sprite.bank,
			self.map.mario.sprite.region_from[0], 
			self.map.mario.sprite.region_from[1],
			self.map.mario.sprite.size[0], 
			self.map.mario.sprite.size[1],
			self.map.mario.sprite.transparent
		)
		
Game() # Ejecuta el juego
