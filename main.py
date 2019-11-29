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
		self.vel_x = 0
		self.vel_y = 0
		self.gravity = gravity
		self.init_sprites() 
		self.state = None
	
	def setVelx(self, val):
		self.vel_x = val
	
	def giveVely(self, val):
		self.vel_y += val

	def setSprite(self, sprite):
		self.sprite = self.sprites[sprite]
		self.state = sprite
		
	def update(self):
		'''
		Actualiza la posición de la entidad un frame con respecto a sus propiedades
		físicas
		'''

		if self.y + self.vel_y >= HEIGHT-1: # Si cae por debajo de la pantalla
			self.y = HEIGHT-1 # Se queda justo al fondo
			
			# Se para
			self.vel_y = 0 
		else:
			self.y += self.vel_y # Si no, se mueve normalmente.

		self.vel_y += self.gravity/FPS # Se acelera gravity por segundo, luego gravity/fps por cada frame.
		self.x += self.vel_x # Se mueve en el eje x
		

class Mario(Entity):
	'''
	Mario, el personaje principal
	'''
	def init_sprites(self):
		self.sprites = {
			'left':Sprite( (2, 1), (13, 16), 0, 3 ), 
			'right':Sprite( (242, 20), (253, 35), 0, 3 ),
			'jump_left':Sprite( (25, 1), (39, 16), 0, 3 ), 
			'jump_right':Sprite( (216, 20), (231, 35), 0, 3 )
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
		pass

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
		self.mario = Mario( WIDTH/2, HEIGHT/2)
		self.mario.setSprite('right')

		#TODO:
		# self.donkey
		# self.pauline
		# ... etc

class Game:
	'''
	El juego (pyxel)
	'''
	
	def __init__(self):
		self.map = Map()
		pyxel.init(WIDTH, HEIGHT, caption='Donkey Kong', fps=FPS) # Inicializa pyxel
		pyxel.load('assets/my_resource.pyxres') # Banco de imagenes
		pyxel.run(self.update, self.draw) # Ejecuta pyxel con las funciones update y draw definidas en esta misma clase
		
	def update(self):
		floor = self.map.mario.y == HEIGHT-1 # para evitar tener que hacer dos veces la misma comprobación

		if floor:
			self.map.mario.setVelx(0) # Si toca el suelo, se para (en el eje x)

		if (pyxel.btn(pyxel.KEY_UP)): # si se pulsa la flecha de arriba
			if floor: # y esta en el suelo 
				self.map.mario.giveVely(-4) # Se le da a Mario velocidad positiva pa que salte
						
		if (pyxel.btn(pyxel.KEY_RIGHT)): # si se pulsa la flecha derecha
			self.map.mario.setVelx(2) # se le da a mario velocidad en x para la derecha
			self.map.mario.setSprite('right') # Se actualiza el sprite

		elif (pyxel.btn(pyxel.KEY_LEFT)): # si en cambio se pulsa la izquierda
			self.map.mario.setVelx(-2) # se le da velocidad para la izquierda
			self.map.mario.setSprite('left') # Se actualiza el sprite
		
		if not floor and not 'jump_' in self.map.mario.state: # si está en el aire y no se ha actualizado ya el sprite
			self.map.mario.setSprite('jump_' + self.map.mario.state) # Se actualiza el sprite
		
		if floor and 'jump_' in self.map.mario.state: # justo al contrario, si llega al suelo y no se ha actualizado
			self.map.mario.setSprite(self.map.mario.state[5::]) # Se actualiza el sprite

		self.map.mario.update() # Se actualizan las coordenadas
		
	
	def draw(self):
		pyxel.cls(0) # Limpia la pantalla, todo a negro

		pyxel.blt(
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
