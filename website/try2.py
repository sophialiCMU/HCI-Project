# import sys module
import pygame
import sys


# pygame.init() will initialize all
# imported module
pygame.init()

clock = pygame.time.Clock()

# it will display on screen
screen = pygame.display.set_mode([960, 540])

bgMain = pygame.image.load("pgMain.jpg")
bgRegister = pygame.image.load("pgRegister.jpg")
bgAvatar = pygame.image.load("pgAvatar.jpg")
bgWhatWeDo = pygame.image.load("pgWhatWeDo.jpg")

active = False

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
	def __init__(self, background, buttonList, inputList, textList = []):
		self.buttonList = buttonList
		self.inputList = inputList
		self.textList = textList
		self.bg = background

# All the inputs
input1 = Input("name", 140,175,140,32)
input2 = Input("email", 140,275,140,32)
input3 = Input("password", 140,375,140,32)
input4 = Input("native language", 600,175,140,32)
input5 = Input("acquiring language", 600,275,140,32)
input6 = Input("short bio", 600,375,140,32)

# All the texts
# def __init__(self, name, textLoc, x, y, txtSize = 32):
text1 = TextBoxMine("Avatar Name", input1, 1100, 300)
text2 = TextBoxMine("English", input4, 1300, 440, 32)
text3 = TextBoxMine("Mandarin", input5, 1300, 515, 15)
text4 = TextBoxMine("Bio", input6, 900, 630, 15)

# All the pages
pgMain = Page(bgMain, [], [], [])
pgWhatWeDo = Page(bgWhatWeDo, [], [], [])
pgRegister = Page(bgRegister, [], [input1, input2, input3, input4, input5, input6])
pgAvatar = Page(bgAvatar, [], [], [text1, text2, text3, text4])

# Button = (self,  name, x, y, h, w, next, color = color_passive)
# The buttons change pages
registerBtn = Button("aboutUs", 960/2-75,355,170,35, pgRegister)
whatWeDoBtn = Button("whatWeDo", 960/2-75,355,170,35, pgWhatWeDo)
avatarBtn = Button("pgAvatar", 300,300,140,32, pgAvatar)
backToMainBtn = Button("backToMain", 10,10,140,32, pgMain, view = True)

pgMain.buttonList = [whatWeDoBtn, backToMainBtn]
pgWhatWeDo.buttonList = [registerBtn, backToMainBtn]
pgRegister.buttonList = [avatarBtn, backToMainBtn]
pgAvatar.buttonList = [backToMainBtn, backToMainBtn]


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
	
	# it will set background color of screen
	screen.fill((255, 255, 255))


	for box in curPg.inputList:
		box.update()

	# gameDisplay.blit(bg, (0, 0))
	screen.blit(curPg.bg, (0,0))

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
	
	# display.flip() will update only a portion of the
	# screen to updated, not full area
	pygame.display.flip()
	
	# clock.tick(60) means that for every second at most
	# 60 frames should be passed.
	clock.tick(60)
