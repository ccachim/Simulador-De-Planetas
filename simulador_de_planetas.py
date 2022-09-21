#Importar modulos necessarios
import pygame
import math
pygame.init()

#Definir janela
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Simulador de planetas")
font = pygame.font.SysFont("calibri", 16)

#Definir cores RGB
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

#Definir classe planeta
class Planet:
	unidade_astronomica = 149.6e6 * 1000
	G = 6.67428e-11 #constante de gravitacao
	escala_geometrica = 200 / unidade_astronomica 
	escala_temporal = 3600*24 

	def __init__(self, x, y, radius, color, mass):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass

		self.orbit = []
		self.sun = False
		self.distance_to_sun = 0

		self.x_vel = 0
		self.y_vel = 0

	def draw(self, win):
		x = self.x * self.escala_geometrica + 800 / 2
		y = self.y * self.escala_geometrica + 800 / 2

		pygame.draw.circle(win, self.color, (x, y), self.radius)
		
		if not self.sun:
			distance_text = font.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
			win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

	#recebe dois planetas e retorna as componentes da forca de gravitacao
	def attraction(self, other):
		other_x = other.x
		other_y = other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2) #pitagoras

		if other.sun:
			self.distance_to_sun = distance

		force = self.G * self.mass * other.mass / distance**2 #lei da gravitacao
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
		total_fx = 0
		total_fy = 0

		for planet in planets:
			if self == planet:
				continue #nao calcular forca com o proprio planeta

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		#F = ma, v = at, x = vt
		self.x_vel += total_fx / self.mass * self.escala_temporal
		self.y_vel += total_fy / self.mass * self.escala_temporal
		self.x += self.x_vel * self.escala_temporal
		self.y += self.y_vel * self.escala_temporal
		self.orbit.append((self.x, self.y))

#Game loop
def main():
	run = True
	clock = pygame.time.Clock()

	#instanciar planetas
	sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
	sun.sun = True
	earth = Planet(-1 * Planet.unidade_astronomica, 0, 16, BLUE, 5.9742 * 10**24)
	earth.y_vel = 29.783 * 1000 
	mercury = Planet(0.387 * Planet.unidade_astronomica, 0, 8, DARK_GREY, 3.30 * 10**23)
	mercury.y_vel = -47.4 * 1000
	venus = Planet(0.723 * Planet.unidade_astronomica, 0, 14, WHITE, 4.8685 * 10**24)
	venus.y_vel = -35.02 * 1000
	planets = [sun, earth, mercury, venus]

	while run == True:
		clock.tick(60)
		window.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(window)

		pygame.display.update()

	pygame.quit()


main()