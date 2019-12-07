import pyxel
import random

# CONFIG
HEIGHT = 256
WIDTH = 224
FPS = 60
#

def abs(num):
	'''
	Función valor absoluto
	'''
	if num >= 0:
		return num
	else:
		return -num

def toggle(bul):
	'''
	Función 'toggle': devuelve el valor booleano contrario al recibido. 
	'''
	if bul:
		return False
	else:
		return True

class Sprite:
	'''
	Especifica como se va a recortar un sprite del banco de imagenes principal
	'''
	def __init__(self, region_from, region_to, bank, transparent=None):
		self.region_from = region_from # (x, y) punto inicial
		self.region_to = region_to # (x, y) punto final
		# A pyxel no le interesa el punto final, sino la distancia al punto inicial a la hora
		# de recortar. Para no estar todo el rato calculandolo, la función __init__ se encarga
		# de hacerlo automáticamente a continuación:
		self.size = (region_to[0]-region_from[0], region_to[1]-region_from[1])
		self.bank = bank # Banco de imagenes
		self.transparent = transparent # Color de transparencia, si se especifica

class Entity:
	'''
	Define una Entidad que tiene una posición en x, una posición en y,
	un sprite (definido explícitamente en la definición de clases hijas a esta) 
	y a la que le afecta la gravedad.
	'''
	def __init__(self, x, y, gravity=0):
		'''
		Inicia la entidad con sus propiedades:
		una posición en el mapa (x, y) junto a una velocidad en el eje y y una gravedad para
		que pueda caer
		'''
		self.x = x
		self.y = y
		self.vel_y = 0
		self.gravity = gravity
		self.init_sprites()
		# init_sprites() se define en las clases hijas de Entity, y especifica
		# los sprites que va a usar el objeto en cuestión.

	def draw(self, correction_x=0, correction_y=0):
		'''
		Dibuja el sprite actual de la entidad en la pantalla de pyxel.
		La función recibe de manera opcional unos valores de corrección en x e y. De este modo, 
		se puede ajustar el sprite respecto a la posición (teórica) de la entidad.
		'''
		pyxel.blt(
			self.x + correction_x,
			self.y + correction_y,
			self.sprite.bank,
			self.sprite.region_from[0], 
			self.sprite.region_from[1],
			self.sprite.size[0], 
			self.sprite.size[1],
			self.sprite.transparent
		)

	# GETTERS
	def getX(self):
		'''
		Devuelve la posición en x de la entidad
		'''
		return self.x

	def getY(self):
		'''
		Devuelve la posición en y de la entidad
		'''
		return self.y

	def getVelY(self):
		'''
		Devuelve la velocidad en y de la entidad
		'''
		return self.vel_y


	def getGravity(self):
		'''
		Devuelve la gravedad de la entidad
		'''
		return self.gravity

	def getSprite(self):
		'''
		Devuelve el nombre del sprite que está actualmente en uso por la entidad.
		Esta función es útil en entidades como una instancia de Mario, en la que los
		diferentes esprites están reunidos en un diccionario con diferentes 'nombres' (keys)
		para cada uno.
		'''
		return self.sprite_name

	# SETTERS
	def setX(self, val):
		'''
		Cambia la posición en x de la entidad al valor val
		'''
		self.x = val
	
	def setY(self, val):
		'''
		Cambia la posición en y de la entidad al valor val
		'''
		self.y = val
	
	def setVelY(self, val):
		'''
		Cambia la velocidad en y de la entidad al valor val
		'''
		self.vel_y = val
	
	def setSprite(self, sprite):
		'''
		Cambia el sprite de la entidad al sprite con nombre <sprite>
		(Para entidades con un diccionario de varios sprites)
		'''
		self.sprite_name = sprite # Actualiza la variable sprite_name
		self.sprite = self.sprites[sprite] # Selecciona el sprite del diccionario y lo actualiza

	# ... CHANGERS?
	# TODO: Creo que estos métodos son un poco innecesarios, pudiendo
	# hacer Entity.set(Entity.get() + variación)
	# Si no se usa demasiado yo creo que vendría bien quitarlos y cambiar sus llamadas
	# en el código. (Total, para un par de veces que se usan)
	def changeX(self, val):
		'''
		Varía la posición en x de la entidad la cantidad val
		'''
		self.x += val

	def changeY(self, val):
		'''
		Varía la posición en y de la entidad la cantidad val
		'''
		self.y += val

	def changeVelY(self, val):
		'''
		Varía la velocidad en y la cantidad val
		'''
		self.vel_y += val

class Points_text:
	'''
	Texto que se muestra en pantalla al conseguir Mario
	nuevos puntos.
	Con una posición y por supuesto un contenido que mostrar.
	Su variable count representa el número de frames restantes que
	aparecerá en pantalla antes de desaparecer. 
	'''
	def __init__(self, x, y, value, count):
		'''
		Se establece su posición en x e y junto a una string
		que será el texto que mostrará en pantalla

		También crea una variable count, usada como contador de frames
		restantes en textos temporales (como el que aparece cuando mario
		consigue puntos) 
		'''
		self.x = x
		self.y = y
		self.value = value
		self.count = count
	
	def draw(self):
		if self.count > 0:
			pyxel.text(self.x, self.y, self.value, 7)
			self.count -= 1

class Mario(Entity):
	'''
	Mario, el personaje principal.
	Posee propiedades fisicas como la gravedad que hace que caiga al saltar,
	sprites que van cambiando dependiendo de como se mueva
	y puede ser controlado por el jugador
	'''
	def init_sprites(self):
		'''
		Inicia los sprites de Mario
		'''

		# Estas variables controlan el estado de mario. Dependiendo de estas variables
		# el rango de movimientos y los sprites de Mario serán distintos.
		# En realidad la creación de estas variables no es responsabilidad de esta función,
		# pero como son únicas para Mario se ponen aquí para no complicar más la cosa.
		self.jumping = False # Salto
		self.stair = False # escalera
		self.plataforma = False # plataforma
		self.vidas = 3
		self.puntos = 0
		self.died = False

		# Sprites de Mario
		self.sprites = {
			'right1':Sprite((242, 20), (254, 35), 0, 3),
			'right2':Sprite((216, 20), (230, 35), 0, 3), # También usado para el salto
			'right3':Sprite((192, 21), (207, 35), 0, 3),
			'left1':Sprite((2, 1), (13, 16), 0, 3),
			'left2':Sprite((25, 1), (39, 16), 0, 3), # También usado para el salto
			'left3':Sprite((49, 2), (63, 16), 0, 3),
			'stairs1':Sprite((74, 1), (87, 17), 0, 3),
			'stairs2':Sprite((169, 20), (182, 36), 0, 3),
			'die1':Sprite((97, 48), (113, 62), 0, 3),
			'die2':Sprite((121, 48), (137, 64), 0, 3),
			'die3':Sprite((116, 77), (132, 93), 0, 3),
			'die4':Sprite((145, 48), (161, 64), 0, 3)
		}
		self.setSprite('right1') # Sprite inicial de Mario. De pie, mirando a la derecha.

	def update(self):

		# Si no está tocando una escalera o la está tocando pero está sobre una plataforma...
		if not self.stair or (self.stair and self.plataforma):
			# La variable turn es el turno, lo que establece cual de los
			# 3 sprites usar en mario cuando esta corriendo. El algoritmo se explica en la documentación.
			turn = int(pyxel.frame_count%30 / 10) + 1

			# DERECHA E IZQUIERDA
			if (pyxel.btn(pyxel.KEY_RIGHT)): # si se pulsa la flecha derecha
				self.changeX(1) # se mueve hacia la derecha,
				if not self.jumping: # Y si no está saltando
					self.setSprite('right' + str(turn)) # Actualiza el sprite.
				else:
					self.setSprite('right2') # si está saltando simplemente gira

			if (pyxel.btn(pyxel.KEY_LEFT)): # si en cambio se pulsa la izquierda
				self.changeX(-1) # se le da velocidad para la izquierda
				if not self.jumping: # Si no está saltando
					self.setSprite('left' + str(turn)) # Actualiza el sprite
				else:
					self.setSprite('left2') # si está saltando simplemente gira

			# QUE NO SALGA POR LOS BORDES LATERALES DE LA PANTALLA
			if self.getX() > WIDTH: # Si se sale por la derecha
				self.setX(WIDTH) # Se queda ahi, no sobrepasa el borde
			elif self.getX() < 0: # Si se sale por la izquierda
				self.setX(0) # Tampoco sale

			# SALTO
			# Si se pulsa el espacio y no está saltando...
			if (pyxel.btn(pyxel.KEY_SPACE)) and (not self.jumping):
				self.jumping = True # comienza a saltar
				self.setVelY(-2.5) # le da velocidad a mario pa que salte
				self.setSprite(self.getSprite()[:-1] + '2') # pasa al sprite de salto, el 2

			# Si no se está moviendo, pasa al sprite 1, el de que está de pie.
			# Si no hiciese esto, se quedaria quieto en una posición de estar corriendo, lo cual queda feo.
			if not self.jumping and not(pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT)):
				self.setSprite(self.getSprite()[:-1] + '1')
			
			# CAIDA
			self.changeVelY(self.getGravity()/FPS) # la gravedad le afecta (gravedad por segundo --> gravedad/frame por frame)
			if self.getY() + self.getVelY() >= HEIGHT-1: # si toca el suelo
				self.setY(HEIGHT-1) # se queda en el suelo
				self.setVelY(0) # se para
				self.jumping = False # ya no está saltando
			else:
				self.changeY(self.getVelY()) # si no, sigue saltando o cayendo
		
		# SUBIR O BAJAR ESCALERAS
		# si está en una escalera
		if self.stair:
			# El mismo algoritmo, pero cambiado para que oscile entre dos sprites en vez
			# de 3:
			turn = int(pyxel.frame_count%20/10) + 1
			
			if pyxel.btn(pyxel.KEY_UP):# Si se pulsa la flecha arriba
				self.changeY(-1) # Sube
				self.setSprite('stairs' + str(turn)) # Actualiza el sprite
			
			if pyxel.btn(pyxel.KEY_DOWN):# Si se pulsa la flecha abajo
				self.changeY(1) # baja
				self.setSprite('stairs' + str(turn)) # Actualiza el sprite
	
	def die(self):
		'''
		Mario sufre el impacto de un barril. Pierde una vida, y se inicia la secuencia de 
		muerte de mario.
		Si no tiene mas vidas, se acaba el juego. 
		'''
		self.vidas -= 1
		self.died = True

class DonkeyKong(Entity):
	'''
	Donkey Kong, el enemigo principal del juego.
	Estático, con sprite cambiante, y su posición es usada
	como punto de partida para la salida de los barriles (los lanza él)
	'''
	def init_sprites(self):

		self.sprites = {
			'static':Sprite((103, 7), (145, 38), 1, 3),
			'coge_barril1':Sprite((52, 8), (95, 39), 1, 3), 
			'coge_barril2':Sprite((33, 96), (74,127), 1, 3),
			'coge_barril3':Sprite((150, 7), (199,38), 1, 3), 
			'angry1':Sprite((2, 53), (50, 86), 1, 3),
			'angry2':Sprite((201,6), (248, 38), 1, 3)
			}
		self.setSprite('static')
		self.turn = 0
		# Si donkey ya ha lanzado un barril, no vuelve a lanzar más
		# hasta que vuelva a completar el ciclo de sprites
		self.barril_lanzado = False

	def update(self):
		if self.turn == 0:
			self.setSprite('static')
			if pyxel.frame_count%150 == 0:
				self.turn = 60
		else:
			if self.turn >= 40:
				num = '1'
			elif self.turn <= 40 and self.turn >= 20:
				num = '2'
			else:
				num = '3'

			self.setSprite('coge_barril' + num)
			del num
			self.turn -= 1

class Barril(Entity):
	'''
	Los barriles son los proyectiles que Mario tiene que esquivar.
	Con propiedades físicas y sprite cambiante, pero no pueden ser controlados por el jugador.
	'''
	def init_sprites(self):

		# Al igual que en Mario, aquí se definen inicialmante varias variables
		# que sirven para manejar el comportamiento del movimiento del barril.
		self.heading_right = True # Mira para la derecha 
		self.plataforma = False # Toca una plataforma
		self.cayendo = False # Está cayendo (POR UNA ESCALERA)
		self.jumped = False

		self.sprites = {
			'rolling1':Sprite((59, 118), (71, 128), 0, 3),
			'rolling2':Sprite((83, 118), (95, 128), 0, 3),
			'rolling3':Sprite((107, 118), (119, 128), 0, 3),
			'rolling4':Sprite((131, 118), (143, 128), 0, 3),
			'falling1':Sprite((153, 118), (169, 128), 0, 3),
			'falling2':Sprite((177, 118), (193, 128), 0, 3)
		}
		self.setSprite('rolling1') # Sprite inicial
	
	def update(self):
		# QUE NO SALGA POR LOS BORDES LATERALES DE LA PANTALLA (Menos en la zona de inicio)
		if self.getX() > WIDTH: # Si se sale por la derecha
			self.setX(WIDTH) # Se queda ahi, no sobrepasa el borde
			self.heading_right = toggle(self.heading_right)
		elif self.getX() < 0 and not self.getY() >= 247: # Si se sale por la izquierda (Y no es en la zona de inicio)
			self.setX(0) # Tampoco sale
			self.heading_right = toggle(self.heading_right)
		
		# CAIDA
		self.changeVelY(self.getGravity()/FPS) # la gravedad le afecta (gravedad por segundo --> gravedad/frame por frame)
		if self.getY() + self.getVelY() >= HEIGHT-1: # si toca el suelo
			self.setY(HEIGHT-1) # se queda en el suelo
			self.setVelY(0) # se para
		else:
			self.changeY(self.getVelY()) # si no, sigue saltando o cayendo

		if not self.cayendo:
			nums = ['1', '2', '3', '4']
			turn = int(pyxel.frame_count%40/10)
			
			if self.heading_right:
				turn = nums[turn]
				self.changeX(1)
			else:
				turn = nums[::-1][turn]
				self.changeX(-1)

			self.setSprite('rolling' + str(turn))
		else:
			turn = int(pyxel.frame_count%20/10) + 1
			self.setSprite('falling' + str(turn))

class Pauline(Entity):
	'''
	Pauline, la princesa que Mario tiene que rescatar,
	Estática, pero de vez en cuando su sprite cambia.
	'''
	def init_sprites(self):
		self.sprites = {
			'static':Sprite((3,229), (16,252), 0,3),
			'moving1':Sprite((26,229), (42,252), 0, 3),
			'moving2':Sprite((50,229), (66,252), 0, 3)
		}
		self.setSprite('static') #Sprite principal de Pauline
		self.turn = 0 # Pauline mantendrá la misma imagen cuando no pida ayuda
		# Pauline está haciendo el baile de auxilio
		self.help = 0
		self.dancing = False
		self.rescatada = False

	def update(self):
		if not self.rescatada:
			if self.turn == 0:

				if self.dancing:
					self.dancing = False
					self.help = 60

				self.setSprite('static')
				if pyxel.frame_count%300 == 299: # Cada 5 sec. Pauline baila
					self.turn = 75	
			else:
				self.dancing = True
				if (self.turn<=10) or (40<self.turn<=50):
					self.setSprite('moving1')
				elif (10<self.turn<=20) or (30<self.turn<=40) or (50<self.turn<=60) or (self.turn>=70):
					self.setSprite('moving2')
				elif (20<self.turn<=30) or (60<self.turn<70):
					self.setSprite('static')
				

				self.turn-=1


class Escalera(Entity):
	'''
	Las escaleras del mapa.
	Es estática y de sprite fijo.
	'''
	def init_sprites(self):
		'''Crea el sprite de la escalera'''
		self.sprite = Sprite((121, 237), (131, 253), 0, 3)

class Platarforma(Entity):
	'''
	Las plataformas del mapa.
	Estáticas y con sprite fijo.
	'''
	def init_sprites(self):
		'''Crea el sprite de la plataforma'''
		self.sprite = Sprite((236, 103), (251, 111), 0, 3)

class Map():
	'''
	El mapa es el objeto en el que se encuentran todas las entidades del juego.
	Esta clase no solo nos proporciona un lugar en el que buscar a las entidades,
	sino que también proporciona un entorno en el que las entidades van a interactuar entre sí.
	(en Game.update())
	'''

	def __init__(self):
		'''
		Inicialización del mapa, se crean todas las entidades que van a convivir en el juego.
		'''
		self.pauline = Pauline(105,5) # Posición de PAULINE
		self.donkey = DonkeyKong(29, 28) # Posición de DONKEY KONG
		self.mario = Mario( 7, HEIGHT-9, 9.8) # Se crea a Mario

		self.texts = [] # Lista que va a contener todos los textos de puntuación del mapa
		self.escaleras = [] # lista que va a contener a todas las escaleras del mapa
		self.escaleras_no_interactua = [] # Escaleras en las que mario NO PUEDE BAJAR (rotas)
		self.plataformas = [] # Lista que va a contener a todas las plataformas del mapa
		self.barriles = [] # Lista que va a contener a todos los barriles del mapa

		# CREACIÓN DE PLATAFORMAS y ESCALERAS
		# Todo este código va añadiendo plataformas partiendo de la posición de la inicial.
		# mientras tanto, cuando está cerca de una posición en la que hay que dibujar una escalera la
		# dibuja, ya de paso.
		# curr_plat --> posición de la última plataforma que se ha creado.
		# TODO: TIENE QUE HABER UNA FORMA DE HACER ESTO SIN TENER QUE HACER ESTA MONSTRUOSIDAD ES FEISIMO ESTO
		curr_plat = self.crea_plataforma(7, HEIGHT-8, 7)
		self.escaleras.append(Escalera(curr_plat[0]-15, curr_plat[1]+1))
		self.escaleras_no_interactua.append(Escalera(curr_plat[0]-15, curr_plat[1]-34))
		curr_plat = self.crea_plataforma(curr_plat[0], curr_plat[1], 9, var_y=-1)
		self.escaleras.append(Escalera(curr_plat[0]-30, curr_plat[1]-19))
		self.escaleras.append(Escalera(curr_plat[0]-30, curr_plat[1]-7))
		curr_plat = self.crea_plataforma(curr_plat[0]-15, curr_plat[1]-25, 14, var_x=-15, var_y=-1)
		self.escaleras.append(Escalera(curr_plat[0]+30, curr_plat[1]-19))
		self.escaleras.append(Escalera(curr_plat[0]+30, curr_plat[1]-7))
		self.escaleras.append(Escalera(curr_plat[0]+90, curr_plat[1]-23))
		self.escaleras.append(Escalera(curr_plat[0]+90, curr_plat[1]-7))
		self.escaleras.append(Escalera(curr_plat[0]+90, curr_plat[1]+5))
		curr_plat = self.crea_plataforma(curr_plat[0]+15, curr_plat[1]-25, 14, var_y=-1)
		self.escaleras.append(Escalera(curr_plat[0]-30, curr_plat[1]-19))
		self.escaleras.append(Escalera(curr_plat[0]-30, curr_plat[1]-7))
		self.escaleras_no_interactua.append(Escalera(curr_plat[0]-150, curr_plat[1]-27))
		self.escaleras.append(Escalera(curr_plat[0]-150, curr_plat[1]+5))
		self.escaleras.append(Escalera(curr_plat[0]-105, curr_plat[1]-24))
		self.escaleras.append(Escalera(curr_plat[0]-105, curr_plat[1]-8))
		self.escaleras.append(Escalera(curr_plat[0]-105, curr_plat[1]+4))
		curr_plat = self.crea_plataforma(curr_plat[0]-15, curr_plat[1]-25, 14, var_x=-15, var_y=-1)
		self.escaleras.append(Escalera(curr_plat[0]+75, curr_plat[1]-22))
		self.escaleras.append(Escalera(curr_plat[0]+75, curr_plat[1]-10))
		self.escaleras.append(Escalera(curr_plat[0]+75, curr_plat[1]+2))
		self.escaleras.append(Escalera(curr_plat[0]+30, curr_plat[1]-19))
		self.escaleras.append(Escalera(curr_plat[0]+30, curr_plat[1]-7))
		self.escaleras_no_interactua.append(Escalera(curr_plat[0]+150, curr_plat[1]-27))
		self.escaleras.append(Escalera(curr_plat[0]+150, curr_plat[1]+5))
		curr_plat = self.crea_plataforma(curr_plat[0]+15, curr_plat[1]-25, 14, var_y=-1)
		self.escaleras.append(Escalera(curr_plat[0]-30, curr_plat[1]-19))
		self.escaleras.append(Escalera(curr_plat[0]-30, curr_plat[1]-7))
		self.escaleras_no_interactua.append(Escalera(curr_plat[0]-105, curr_plat[1]-22))
		self.escaleras.append(Escalera(curr_plat[0]-105, curr_plat[1]+5))
		curr_plat = self.crea_plataforma(curr_plat[0]-15, curr_plat[1]-25, 5, var_x=-15, var_y=-1)
		self.escaleras.append(Escalera(curr_plat[0], curr_plat[1]-8))
		self.escaleras.append(Escalera(curr_plat[0], curr_plat[1]-24))
		curr_plat = self.crea_plataforma(curr_plat[0]-15, curr_plat[1], 9, var_x=-15)
		self.escaleras.append(Escalera(curr_plat[0]+90, curr_plat[1]-8))
		self.escaleras.append(Escalera(curr_plat[0]+90, curr_plat[1]-24))
		self.escaleras.append(Escalera(curr_plat[0]+90, curr_plat[1]-40))
		self.escaleras.append(Escalera(curr_plat[0]+75, curr_plat[1]-8))
		self.escaleras.append(Escalera(curr_plat[0]+75, curr_plat[1]-24))
		self.escaleras.append(Escalera(curr_plat[0]+75, curr_plat[1]-40))
		self.crea_plataforma(curr_plat[0]+102, curr_plat[1]-31, 3)

		del curr_plat # ya no se necesita más esta variable, así que se borra de la memoria. 

	def crea_plataforma(self, init_x, init_y, number, var_x=15, var_y=0):
		'''
		Crea una 'plataforma grande' (sucesión de instancias de Plataforma)
		init_x, init_y --> coordenadas de la primera plataforma
		number --> numero de plataformas a crear
		var_x --> variación en eje x entre plataformas (15 default, justo pegadas)
		var_y --> variación en y de las plataformas. (por default 0, todas rectas)
		'''
		
		for i in range(number): # tantas veces como se le haya ordenado
			self.plataformas.append(Platarforma(init_x, init_y)) # añade la plataforma a la lista
			# Se varía x e y para crear la siguiente plataforma
			init_x += var_x 
			init_y += var_y
		
		# devuelve la posición de la ultima plataforma, para
		# poder partir de ella a la hora de dibujar las siguientes
		return (init_x-var_x, init_y-var_y)

class Game:
	'''
	El juego (pyxel)
	'''
	
	def __init__(self):
		'''
		Inicio del juego: se crea el mapa, se inicia la interfaz de pyxel
		de acuerdo a las configuraciones preestablecidas y se inicia pyxel.
		'''
		self.map = Map() # Crea el mapa, de nombre map 
		self.die_temp = 0 # Controla cuanto dura la secuencia de muerte
		self.end = False # El juego ha terminado
		pyxel.init(WIDTH, HEIGHT, caption='Donkey Kong', fps=FPS) # Inicializa pyxel
		pyxel.load('assets/my_resource.pyxres') # Carga el banco de imagenes
		pyxel.run(self.update, self.draw) # Ejecuta pyxel con las funciones update y draw definidas en esta misma clase
		
	def update(self):
		'''
		Esta funcion se ejecuta cada frame, y se encarga de
		refrescar el estado del juego, actualizando cada entidad
		en base a sus propiedades y su interacción con otras entidades del 
		mapa.
		'''

		# ----------- MARIO -------------
		if not self.map.mario.died: # si mario no esta en la secuencia de muerte
			# Todo transcurre normal, todo se actualiza
			self.map.donkey.update() # Actualiza a Donkey Kong
			self.map.pauline.update() # Actualiza a Pauline
			self.map.mario.update() # Actualiza la posición de Mario
		else:# si no...
			# Desaparecen ciertas entidades como los barriles y el texto de nuevos puntos
			self.map.barriles = []
			self.map.texts = []
			if not self.die_temp == 0:
				if self.die_temp >= 250:
					self.map.mario.setSprite('die1')
				elif self.die_temp <= 160:
					self.map.mario.setSprite('die4')
				else:
					turn = int(pyxel.frame_count%30/10) + 1
					self.map.mario.setSprite('die' + str(turn))
				self.die_temp -= 1
			else:
				if self.map.mario.vidas == 0:
					self.end = True # Se acaba el juego
				self.map.mario.died = False
				self.map.mario.setX(7)
				self.map.mario.setY(HEIGHT-9)
				self.map.mario.setSprite('right1')

		# Mientras no se demuestre lo contrario, de momento
		# mario no está tocando ni escaleras ni plataformas.
		self.map.mario.stair = False
		self.map.mario.plataforma = False
		
		# Cuando está a true, los barriles saltados por mario
		# se resetean y vuelven a poder ser saltados, dandole puntos a Mario
		barril_reset = False 

		# INTERACCIÓN MARIO-PLATAFORMA
		for i in self.map.plataformas:# por cada plataforma
			if ( # SI...
				# Al continuar mario cayendo atravesaría la plataforma
				(self.map.mario.getY() + self.map.mario.getVelY() >= i.y-1) and
				# Y mario está dentro de la plataforma en el eje x 
				(abs((self.map.mario.getX()-5) - (i.x-7)) <= 9) and
				# y también lo está en el eje y
				(abs(i.y - self.map.mario.getY()) <= 3)
			): # tocará la plataforma, así que:
				self.map.mario.plataforma = True # Está tocando una plataforma
				self.map.mario.jumping = False # ya no está saltando
				barril_reset = True
				self.map.mario.setY(i.y-1) # se queda encima de la plataforma
				self.map.mario.setVelY(0) # deja de caer
		
		# INTERACCIÓN MARIO-ESCALERA
		for i in self.map.escaleras: # por cada escalera
			if (# SI...
				# Mario no está saltando
				(not self.map.mario.jumping) and
				# Y mario esta dentro de la escalera en el eje x
				(abs((self.map.mario.getX()-5) - (i.x-7)) <= 3) and
				# y tambien lo está en el eje Y
				(abs(i.y-7 - ( self.map.mario.getY() - 7) ) <= 8)
			): # está en la escalera, así que
				self.map.mario.setVelY(0) # se para
				self.map.mario.stair = True # está tocando una escalera
				if (
					( int(i.y - 7 - self.map.mario.getY() ) == 1) and 
					self.map.mario.plataforma and
					pyxel.btn(pyxel.KEY_DOWN)
					):
					self.map.mario.changeY(4) # 4 a la vez para que baje de la plataforma

		# ------------- BARRILES ---------------

		for barril in self.map.barriles: # Repite esto con cada barril
			barril.update() # Actualiza la posición del barril

			if barril_reset:
				barril.jumped = False

			barril.plataforma = False # De momento no toca ningaun plataforma

			# INTERACCIÓN BARRIL-ESCALERA
			for i in self.map.escaleras + self.map.escaleras_no_interactua: # por cada escalera
				if (# SI...
					# esta dentro de la escalera en el eje x
					(abs(barril.getX() - i.x+5) <= 3) and
					( int(i.y-7 - barril.getY()) == 0)
					): # está en la escalera, así que
					if random.randint(1, 4) == 4: # 1/4 de posibilidades de que eso pase, 25%
						barril.cayendo = True
						barril.changeY(4)

			
			# INTERACCIÓN BARRIL-PLATAFORMA
			for i in self.map.plataformas:# por cada plataforma
				if ( # SI...
					# Al continuar cayendo atravesaría la plataforma
					(barril.getY() + barril.getVelY() >= i.y-1) and
					# Y está dentro de la plataforma en el eje x 
					(abs((barril.getX()-5) - (i.x-7)) <= 9) and
					# y también lo está en el eje y
					(abs(i.y - barril.getY()) <= 3)
				): # tocará la plataforma, así que:
					barril.plataforma = True # Ahora está en una plataforma
					
					if barril.cayendo: # Si antes estaba bajando por una escalera
						barril.cayendo = False # Ya no baja
						barril.heading_right = toggle(barril.heading_right) # Cambia su dirección (dado que pasa a la plataforma de abajo)

					barril.setY(i.y-1) # se queda encima de la plataforma
					barril.setVelY(0) # deja de caer

		# INTERACCIÓN MARIO-BARRILES
		for barril in self.map.barriles:
			if (# Si está saltando
				(self.map.mario.jumping) and
				# Y se alinea con el barril en el eje x
				(abs(barril.getX() - self.map.mario.getX()) <= 3) and
				# Y está también alineado con el en el eje Y (pasando por encima)
				(barril.getY() - self.map.mario.getY() <= 20) and
				(barril.getY() - self.map.mario.getY() >= 11) and
				# Y el barril no ha sido saltado todavía durante ese salto de Mario
				not barril.jumped
				):
				self.map.mario.puntos += 100 # Añade más puntos
				self.map.texts.append( # Se añade el texto de puntuación nueva para que sea dibujado
					Points_text(self.map.mario.getX(), self.map.mario.getY(), '100', 65)
					)
				barril.jumped = True # El barril ha sido saltado, y ya no dará mas puntos hasta que Mario vuelva a saltar.
			elif (
				# Y se alinea con el barril en el eje x
				(abs(barril.getX() - self.map.mario.getX()) <= 3) and
				# Y está 'dentro' del barril en el eje Y
				(barril.getY() - self.map.mario.getY() < 11) and
				(barril.getY() - self.map.mario.getY() >= 0)
				):# Está tocando el barril, así que
				# Secuencia de muerte de Mario
				self.map.mario.die()
				self.die_temp = 300 # Añade tiempo al temporizador
		
		# INTERACCIÓN MARIO-DONKEY KONG
		if(
			# si Mario se alinea con donkey en el eje x
			(abs(self.map.donkey.getX() + 21 - self.map.mario.getX()) <= 21) and
			# Y está 'dentro' de donkey en el eje Y
			(self.map.mario.getY() - self.map.donkey.getY() < 42) and
			(self.map.mario.getY() - self.map.donkey.getY() >= 0) and
			not self.map.mario.died # Para que no le mate repetidamente
			):# Mario stá tocando a donkey, así que
			# Secuencia de muerte de Mario
			self.map.mario.die()
			self.die_temp = 300 # Añade tiempo al temporizador

		# el "Colector de basuras"
		# Si hay un barril que se ha salido del mapa (ha llegado al final y
		# se ha ido) lo desecha de la lista de barriles.
		new = []
		for i in self.map.barriles:
			if not ( (i.getX() < 0) and (i.getY() >= 247) ):
				new.append(i)
		self.map.barriles = new

		# el mismo "colector de basuras", pero
		# esta vez para eliminar los textos de puntuación
		# que ya no aparecen más en pantalla
		new = []
		for i in self.map.texts:
			if not (i.count <= 0):
				new.append(i)
		self.map.texts = new

		del new # Ya no necesitamos la variable de paso

		# DONKEY KONG LANZA BARRILES
		if (
			(self.map.donkey.getSprite() == 'coge_barril3') and
			(not self.map.donkey.barril_lanzado) and
			(len(self.map.barriles) < 10 )
			):
			self.map.barriles.append(Barril(73, 60, 4.5))
			self.map.donkey.barril_lanzado = True

		if self.map.donkey.getSprite() == 'coge_barril2':
			self.map.donkey.barril_lanzado = False

	def draw(self):
		'''
		La función draw se ejecuta cada frame justo después de la función update,
		y se encarga de dibujar todas las entidades en pantalla.
		'''

		pyxel.cls(0) # Limpia la pantalla, todo a negro
		if not self.end:
			pyxel.blt(9, 26, 0, 3, 98, 20, 33, 3) #Imagen estática de barriles donde DONKEY KONG cogerá los barriles y los lanzará
			
			for i in self.map.escaleras + self.map.escaleras_no_interactua: # Por cada escalera (incluidas las que no baja)
				i.draw(-5, -7) # Dibuja la entidad
				# DEBUG: pyxel.pix(i.x, i.y - 7, 3)

			for i in self.map.plataformas: # Por cada entidad en map.plataformas
				i.draw(correction_x=-7) # Dibuja la entidad
			
			for i in self.map.barriles:
				i.draw(-5, -9)
				# DEBUG: pyxel.pix(i.x, i.y)

			for i in self.map.texts:
				i.draw()

			self.map.pauline.draw() # Dibuja a Pauline 
			if self.map.pauline.help > 0:
				pyxel.blt(120, 5, 0, 1, 197, 23, 9, 3)
				self.map.pauline.help -= 1

			self.map.donkey.draw() # Dibuja a DONKEY KONG

			if (self.map.mario.getY() <= 27 and self.map.mario.plataforma):
				pyxel.blt(120, 10, 0, 98, 195, 16, 14, 3) # Pinta el corazon
				self.map.pauline.rescatada = True
			else:
				self.map.pauline.rescatada = False
			
			self.map.mario.draw(-5, -14) # Dibuja a Mario
			# DEBUG: pyxel.pix(self.map.mario.getX(), self.map.mario.getY(), 10)

			# Texto que muestra los puntos pon pantalla
			# Siempre tiene que ocupar 5 casillas, así que lo que falte
			# es rellenado con ceros al principio:
			pyxel.text(10, 5, '0'* (5 - len(str(self.map.mario.puntos))) + str(self.map.mario.puntos), 7)
			
			# Mini marios que representan la vida que le queda a Mario
			x = 10
			for i in range(self.map.mario.vidas):
				pyxel.blt(x, 15, 0, 241, 201, 7, 8, 3)
				x += 10
			del x # Esta variable ya no hace falta asi que se borra
		else:
			# Pinta el texto del final del juego
			pyxel.text(WIDTH/2-20, HEIGHT/2, 'GAME OVER', 7)
			pyxel.text(WIDTH/2-40, HEIGHT/2+30, 'PUNTOS CONSEGUIDOS:', 7)
			# Pinta los puntos, mas o menos centrados en la pantalla
			pyxel.text(WIDTH/2-3*len(str(self.map.mario.puntos)), HEIGHT/2+40, str(self.map.mario.puntos), 7)
Game() # Ejecuta el juego
