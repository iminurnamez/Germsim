import sys
import random
import itertools
import collections
import pygame
from pygame.locals import *
from pygame import Color


pygame.init()

DISPLAYSURF = pygame.display.set_mode((1080, 740))  		# setting up the screen attributes
pygame.display.set_caption("Germ Sim")
FPS = 30
fpsClock = pygame.time.Clock()
SCREENWIDTH = 1080
HALFWIDTH = SCREENWIDTH / 2
SCREENHEIGHT = 740
HALFHEIGHT = SCREENHEIGHT / 2

text24 = pygame.font.Font("freesansbold.ttf", 24)		# font object for text
	
class Germ(object):
	# speed = pixels moved per tick, moratltiy = chance/1000 of death
	# erraticness = chance/1000 of changing direction, mutation_chance = 
	# chance/1000 of new germ being a different color(but not blue, mutants
	# only beget mutants), divide_chance = chance/1000 of creating new germ,
	# size = width and height of germ
	
	directions = ["up", "down", "left", "right"]		# class attributes
	germ_colors = [Color("red"), Color("yellow"), Color("green")]
	def __init__(self, speed = 1, mortality = 4, erraticness = 100, mutation_chance = 5, # this function defines the intial state
		divide_chance = 5, size = 5):													 # of a germ object when instantiated
		self.speed = speed												
		self.mortality = mortality
		self.erraticness = erraticness
		self.mutation_chance = mutation_chance
		self.divide_chance = divide_chance
		self.direction = random.choice(self.directions)
		self.color = random.choice(self.germ_colors)
		self.size = size
		self.x = random.randint(self.size, SCREENWIDTH - self.size)
		self.y = random.randint(self.size, SCREENHEIGHT - self.size)
		
	def check_direction(self):									# function(technically an object method)to check
		if random.randint(1, 1000) < self.erraticness:			# if germ has changed directions
			self.direction = random.choice(self.directions)
		if self.direction == "up" and self.y < self.speed:
			self.direction = "down"
		elif self.direction == "down" and self.y + self.size > SCREENHEIGHT - self.speed:
			self.direction = "up"
		elif self.direction == "left" and self.x < self.speed: 
			self.direction = "right"
		elif self.direction == "right" and self.x + self.size > SCREENWIDTH - self.speed:
			self.direction = "left"
			
	def move(self):											# method to move germ by changing x,y co-ords
		if self.direction == "up":
			self.y -= self.speed 
		elif self.direction == "down":
			self.y += self.speed 
		elif self.direction == "left":
			self.x -= self.speed 
		elif self.direction == "right":
			self.x += self.speed

	def death_check(self):								
		if random.randint(1, 1000) < self.mortality:
			return True
			
	def divide_check(self):								
		if random.randint(1, 1000) < self.divide_chance:
			return True
	
	def respond_to_mouse(self, mousex, mousey, mouse_color):				# method to make germs seek the x,y location of the mouse
		if self.color == Color("blue") and (mouse_color == "All" or mouse_color == "Blue"):
			if self.x > mousex:
				self.x -= self.speed * 2
			if self.y > mousey:
				self.y -= self.speed * 2
			if self.x < mousex:
				self.x += self.speed * 2
			if self.y < mousey:
				self.y += self.speed * 2
		elif self.color == Color("green") and (mouse_color == "All" or mouse_color == "Green"):
			if self.x > mousex:
				self.x -= self.speed * 3
			if self.y > mousey:
				self.y -= self.speed * 3
			if self.x < mousex:
				self.x += self.speed * 3
			if self.y < mousey:
				self.y += self.speed * 3
		elif self.color == Color("yellow") and (mouse_color == "All" or mouse_color == "Yellow"):
			if self.x > mousex:
				self.x -= self.speed * 4
			if self.y > mousey:
				self.y -= self.speed * 4
			if self.x < mousex:
				self.x += self.speed * 4
			if self.y < mousey:
				self.y += self.speed * 4
		elif self.color == Color("red") and (mouse_color == "All" or mouse_color == "Red"):
			if self.x > mousex:
				self.x -= self.speed * 5
			if self.y > mousey:
				self.y -= self.speed * 5
			if self.x < mousex:
				self.x += self.speed * 5
			if self.y < mousey:
				self.y += self.speed * 5

def screen_template1(surface, screen_width, top_margin, title, title_font_type, title_font_size, # handles intro screen
	title_color, title_space, lines, line_font_type, line_font_size, line_color, line_space):
	title_font = pygame.font.Font(title_font_type, title_font_size)
	title_text = title_font.render(title, True, title_color)
	title_text_Rect = title_text.get_rect()
	title_text_Rect.midtop = (screen_width/2, top_margin)
	line_font = pygame.font.Font(line_font_type, line_font_size)
	surface.blit(title_text, title_text_Rect)
	vert = top_margin + title_text_Rect.height + title_space
	for line in lines:
		line_text = line_font.render(line, True, line_color)
		line_text_Rect = line_text.get_rect()
		line_text_Rect.midtop = (screen_width/2, vert)
		surface.blit(line_text, line_text_Rect)
		vert += line_space + line_text_Rect.height				

def main():						#main program function	
	germs = []					
	germs_queue = []
	for i in range(4):			# for loop that instantiates 4 germ objects
		germ = Germ()
		germ.x = HALFWIDTH
		germ.y = HALFHEIGHT
		germ.Rect = pygame.Rect(germ.x, germ.y, germ.size, germ.size)
		germ.color = Color("blue")
		germs.append(germ)

	dividing = True				# set flags for initial state
	mouse_active = False		
	simulating = True
	mutating = True
	death = True
	mouse_colors = itertools.cycle(["All", "Blue", "Green", "Yellow", "Red"])
	mouse_color = next(mouse_colors)
	while simulating:			# game loop (not really a game but this is how games are usually set up)
		# germ logic
		for germ in germs:		
			germ.check_direction()
			germ.move()
			if dividing and germ.divide_check():	# if dividing == True AND germ.divide_check returns True:
				newgerm = Germ()		#instantiate a new germ object
				newgerm.x, newgerm.y = germ.x, germ.y - newgerm.size # puts new germ directly above the "parent" germ
				newgerm.Rect = pygame.Rect(newgerm.x, newgerm.y, newgerm.size, newgerm.size)
				newgerm.Rect.bottomleft = germ.Rect.topleft
				if mutating and random.randint(1, 100) < newgerm.mutation_chance: # check for mutation
					while newgerm.color == germ.color:			# if a mutant, pick a random color until the colors are different	
						newgerm.color = random.choice(newgerm.germ_colors)
				else:
					newgerm.color = germ.color
				germs_queue.append(newgerm)
			if death and germ.death_check():
				germs.remove(germ)
		for queued in germs_queue:
			germs.append(queued)
		germs_queue = []
		
		# event handling
		for event in pygame.event.get():	
			if event.type == QUIT:			# if you click the close button on the window the program terminates
				pygame.quit()
				sys.exit()	
			elif event.type == KEYUP:
				if event.key == K_SPACE:	# this if block calculates and prints stats to terminal when spacebar is pressed	
					print "Total: {0}".format(len(germs))
					germ_counts = collections.Counter(str(germ.color) for germ in germs)
					for name, color in [("Blue", str(Color("blue"))), ("Red", str(Color("red"))),
										("Green", str(Color("green"))), ("Yellow", str(Color("yellow")))]:
						print "{0}: {1}".format(name, germ_counts[color])
					print
				elif event.key == K_s:				# if "s" is pressed, toggle the dividing flag
					dividing = not dividing
				elif event.key == K_d:
					death = not death
				elif event.key == K_m:
					mutating = not mutating
				elif event.key == K_c:
					mouse_color = next(mouse_colors)
			elif event.type == MOUSEBUTTONDOWN:	# this elif and the next keep track of whether you're holding the mouse button down
				mouse_active = True				# and thus whether the germs should seek the mouse's (x, y)
			elif event.type == MOUSEBUTTONUP:
				mouse_active = False
		if mouse_active:					
			mousex, mousey = pygame.mouse.get_pos()
			for germ in germs:
				germ.respond_to_mouse(mousex, mousey, mouse_color)
		
		# displaying to screen
		hud = text24.render("<S>plitting: %s   <D>eath: %s   <M>utation: %s  <C>olor: %s <Space> for stats" % (dividing, death, mutating,
			mouse_color), True, Color("black"), Color("gray"))
		hudRect = hud.get_rect()
		hudRect.bottomleft = (0, SCREENHEIGHT)
		DISPLAYSURF.fill(Color("black"))
		for germ in germs:
			pygame.draw.rect(DISPLAYSURF, germ.color, (germ.x, germ.y,
						germ.size, germ.size))
		DISPLAYSURF.blit(hud, hudRect)
		pygame.display.update()		
		fpsClock.tick(FPS)			# slows the program down if its running faster than the frame rate
		
if __name__ == "__main__":			
	menuing = True
	while menuing:		
		DISPLAYSURF.fill(Color("black"))
		screen_template1(DISPLAYSURF, SCREENWIDTH, 20, "GERMSIM", "freesansbold.ttf", 24, Color("blue"),
			50, ['Germsim starts out with four blue "germs" on the screen.',
			'Each time through the game loop, germs have a chance to divide, divide and mutate or die.',
			'"Mutated" germs can only mutate into a mutant color (never blue).',
			'Division ("splitting"), mutation and death can be toggled on and off with the corresponding key.',
			"The division and death rates are very close, so sometimes the initial germs will die out without",
			"getting to divide. Turning death off at the beginning of the sim will avoid this (just make sure",
			"to turn it back on). Eventually, the germ population will reach critical mass",
			"and the program will get laggy. Disabling splitting will allow the population to reduce to",
			"a more manageable level. The space bar prints a report to the terminal. Holding down the mouse",
			"button will cause germs of the selected color to come to the mouse cursor.",
			"Click anywhere to continue."], "freesansbold.ttf", 18, Color("white"), 20)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				menuing = False
		pygame.display.update()
		fpsClock.tick(FPS)
	main()							
