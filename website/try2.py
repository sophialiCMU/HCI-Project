# import sys module
import pygame
import sys
import os
from typing import Tuple

# pygame.init() will initialize all
# imported module
pygame.init()

clock = pygame.time.Clock()

# it will display on screen
screen = pygame.display.set_mode([960, 540])

bgMain = pygame.image.load("bgMain.jpg")
bgRegister = pygame.image.load("bgRegister.jpg")
bgAvatar = pygame.image.load("bgAvatar.jpg")
bgWhatWeDo = pygame.image.load("bgWhatWeDo.jpg")
bgVirtual1 = pygame.image.load("bgVirtual1.jpg")
bgVirtual2 = pygame.image.load("bgVirtual2.jpg")
bgVirtual3 = pygame.image.load("bgVirtual3.jpg")
girlSpriteImg = pygame.image.load("girl.PNG")

active = False

## For sprites
worldx = 960
worldy = 540
fps = 40
ani = 4
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

# Stuff
# basic font for user typed
base_font = pygame.font.Font(None, 32)

# color_active stores color(lightskyblue3) which
# gets active when input box is clicked by user
color_active = pygame.Color('lightskyblue3')

# color_passive store color(chartreuse4) which is
# color of input box.
color_passive = pygame.Color('chartreuse4')

# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)
# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

class Input(object):
	def __init__(self, name, x, y, h, w):
		self.name = name
		self.x = x
		self.y = y
		self.height = h
		self.width = w
		self.user_text = ''
		self.active = False
		# init drawing
		

		# create rectangle
		self.input_rect = pygame.Rect(self.x, self.y, self.height, self.width)
		
		self.color = color_passive

	def update(self):
		if self.active:
			self.color = color_active
		else:
			self.color = color_passive

class Button(object):
	def __init__(self,  name, x, y, h, w, next, color = color_passive, view = False):
		self.next = next
		self.name = name
		self.x = x
		self.y = y
		self.height = h
		self.width = w
		self.color = color
		self.view = view

		# create rectangle
		if self.view:
			self.input_rect1 = pygame.Rect(self.x, self.y, self.height, self.width) # FOR SIZING
		self.input_rect = pygame.Surface((self.height,self.width))  # the size of your rect
		self.input_rect.set_alpha(128)                # alpha level
		self.input_rect.fill((255,255,255))           # this fills the entire surface
		# windowSurface.blit(s, (0,0))    # (0,0) are the top-left coordinates
	
	def collision(self, mouseX, mouseY):
		if (self.x < mouseX and mouseX < self.x + self.height and
        self.y < mouseY and mouseY < self.y + self.width):
			return True
		return False

class TextBoxMine(object):
	# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
	def __init__(self, name, textLoc, x, y, txtSize = 32):
		self.name = name
		self.textLocation = textLoc
		self.text = self.textLocation.user_text
		self.x = x
		self.y = y
		self.font= pygame.font.Font('freesansbold.ttf', txtSize)
		self.textRender = self.font.render(self.name, True, green, white)
		# self.textRender = self.font.render(self.text, True, green, blue)
		# create a rectangular object for the
		# text surface object
		self.textRect = self.textRender.get_rect()
 
		# set the center of the rectangular object.
		self.textRect.center = (x // 2, y // 2)
	
	def textUpdate(self):
		if (self.textLocation.user_text == ""):
			self.textRender = self.font.render(self.name, True, green, white)
			self.textRect = self.textRender.get_rect()
			self.textRect.center = (self.x // 2, self.y // 2)
			return
		self.textRender = self.font.render(f"{self.textLocation.user_text}", True, green, white)
		self.textRect = self.textRender.get_rect()
		self.textRect.center = (self.x // 2, self.y // 2)
		
class Page(object):
	def __init__(self, background, buttonList, inputList, textList = [], sprite = None):
		self.buttonList = buttonList
		self.inputList = inputList
		self.textList = textList
		self.sprite = sprite
		self.bg = background

class Player(pygame.sprite.Sprite):
	# https://opensource.com/article/17/12/game-python-moving-player
	def __init__(self, name, image, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.name = name
		self.movex = 0 # move along X
		self.movey = 0 # move along Y
		self.frame = 0 # count frames
		self.images = [image]

		for i in range(1, 5):
			img = image
			img.convert_alpha()  # optimise alpha
			img.set_colorkey(ALPHA)  # set alpha
			self.images.append(img)
			self.image = self.images[0]
			self.rect = self.image.get_rect()
	
	def control(self,x,y):
		"""
		control player movement
		"""
		self.movex += x
		self.movey += y

	def reset(self):
		self.movex = 0
		self.movey = 0

	def update(self):
		"""
		Update sprite position
		"""
		self.rect.x = self.rect.x + self.movex
		self.rect.y = self.rect.y + self.movey
		# moving left
		if self.movex < 0:
				self.frame += 1
				if self.frame > 3*ani:
						self.frame = 0
				self.image = self.images[self.frame//ani]

		# moving right
		if self.movex > 0:
				self.frame += 1
				if self.frame > 3*ani:
						self.frame = 0
				self.image = self.images[self.frame//ani]

player = Player("girl sprite", girlSpriteImg, 20, 50)
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10

# All the inputs
input1 = Input("name", 140,175,140,32)
input2 = Input("email", 140,275,140,32)
input3 = Input("password", 140,375,140,32)
input4 = Input("native language", 575,175,140,32)
input5 = Input("acquiring language", 575,275,140,32)
input6 = Input("short bio", 575,375,140,32)

# All the texts
# def __init__(self, name, textLoc, x, y, txtSize = 32):
text1 = TextBoxMine("Avatar Name", input1, 1100, 300)
text2 = TextBoxMine("English", input4, 1300, 440, 20)
text3 = TextBoxMine("Mandarin", input5, 1300, 515, 20)
text4 = TextBoxMine("Bio", input6, 900, 630, 15)

# All the pages
pgMain = Page(bgMain, [], [], [])
pgWhatWeDo = Page(bgWhatWeDo, [], [], [])
pgRegister = Page(bgRegister, [], [input1, input2, input3, input4, input5, input6])
pgAvatar = Page(bgAvatar, [], [], [text1, text2, text3, text4])
pgVirtual1 = Page(bgVirtual1, [], [], [], sprite = player_list)
pgVirtual2 = Page(bgVirtual2, [], [], [], sprite = player_list)
pgVirtual3 = Page(bgVirtual3, [], [], [], sprite = player_list)

# Button = (self,  name, x, y, h, w, next, color = color_passive)
# The buttons change pages
backToMainBtn = Button("backToMain", 10,10,140,30, pgMain, view = True)
whatWeDoBtn = Button("whatWeDo", 960/2-75,355,170,35, pgWhatWeDo)
registerBtn = Button("aboutUs", 815,487,120,35, pgRegister)
avatarBtn = Button("pgAvatar", 960/2-130,475,170,35, pgAvatar)
virtual1Btn = Button("pgVirtual1", 860,475,72,35, pgVirtual1)
virtual2Btn = Button("pgVirtual2", 595,85,40,90, pgVirtual2)
virtual3Btn = Button("pgVirtual3", 650,187,78,40, pgVirtual3)

pgMain.buttonList = [whatWeDoBtn, backToMainBtn]
pgWhatWeDo.buttonList = [registerBtn, backToMainBtn]
pgRegister.buttonList = [avatarBtn, backToMainBtn]
pgAvatar.buttonList = [virtual1Btn, backToMainBtn]
pgVirtual1.buttonList = [avatarBtn, virtual2Btn, backToMainBtn]
pgVirtual2.buttonList = [avatarBtn, virtual3Btn, backToMainBtn]
pgVirtual3.buttonList = [avatarBtn, backToMainBtn]

curPg = pgMain

while True:
	for event in pygame.event.get():

	# if user types QUIT then the screen will close
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			for btn in curPg.buttonList:
				mouseX, mouseY = pygame.mouse.get_pos()
				if btn.collision(mouseX, mouseY):
					curPg = btn.next
					break
			for box in curPg.inputList:
				if box.input_rect.collidepoint(event.pos):
					box.active = True
				else:
					box.active = False

		if event.type == pygame.KEYDOWN:
			if curPg.sprite != None:
				pass
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					player.control(-steps,0)
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					player.control(steps,0)
				if event.key == pygame.K_UP or event.key == ord('w'):
					player.control(0, -steps)
				if event.key == pygame.K_DOWN or event.key == ord('s'):
					player.control(0,steps)

			# change text in any active boxes
			for box in curPg.inputList:
				if (box.active == True): # make sure the box is active
					# Check for backspace
					if event.key == pygame.K_BACKSPACE:
						# get text input from 0 to -1 i.e. end.
						box.user_text = box.user_text[:-1]

					# Unicode standard is used for string
					# formation
					else:
						box.user_text += event.unicode

		elif event.type == pygame.KEYUP:
			if curPg.sprite != None:
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					player.control(steps,0)
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					player.control(-steps,0)
				if event.key == pygame.K_UP or event.key == ord('w'):
					player.control(0,steps)
				if event.key == pygame.K_DOWN or event.key == ord('s'):
					player.control(0,-steps)
		else:
			player.reset()
		
	# it will set background color of screen
	screen.fill((255, 255, 255))


	for box in curPg.inputList:
		box.update()

	# gameDisplay.blit(bg, (0, 0))
	screen.blit(curPg.bg, (0,0))

	#### PUT ALL DRAW STUFF AFTER THIS

	# draw rectangle and argument passed which should
	# be on screen
	for box in curPg.inputList:
		pygame.draw.rect(screen, box.color, box.input_rect)
		text_surface = base_font.render(box.user_text, True, (255, 255, 255))
	
		# render at position stated in arguments
		screen.blit(text_surface, (box.input_rect.x+5, box.input_rect.y+5))
	
		# set width of textfield so that text cannot get
		# outside of user's text input
		box.input_rect.w = max(100, text_surface.get_width()+10)
	
	# draw rectangle and argument passed which should
	# be on screen
	for btn in curPg.buttonList:
		# ====
		# FOR SIZING
		if btn.view:
			pygame.draw.rect(screen, btn.color, btn.input_rect1)
			text_surface = base_font.render(btn.name, True, (255, 255, 255))
		
			# render at position stated in arguments
			screen.blit(text_surface, (btn.input_rect1.x+5, btn.input_rect1.y+5))
		
			# set width of textfield so that text cannot get
			# outside of user's text input
			btn.input_rect1.w = max(100, text_surface.get_width()+10)
			# ===== end of FOR SIZING
		screen.blit(btn.input_rect, (btn.x, btn.y))    # (0,0) are the top-left coordinates

	for txt in curPg.textList:
		txt.textUpdate()
		screen.blit(txt.textRender, txt.textRect)

	if curPg.sprite != None:
		pass
		player.update()  # update player position
		player_list.draw(screen)
		pygame.display.flip()
		clock.tick(fps)
	
	#### PUT ALL DRAW STUFF BEFORE THIS
	# display.flip() will update only a portion of the
	# screen to updated, not full area
	pygame.display.flip()
	
	# clock.tick(60) means that for every second at most
	# 60 frames should be passed.
	clock.tick(60)
