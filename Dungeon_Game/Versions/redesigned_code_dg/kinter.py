from tkinter import *

class GameWindow:

	def __init__(self, keySet, resolution):

		#config vars
		self.keySet = keySet
		self.resolution = resolution

		#main window
		self.window = Tk()
		self.window.configure(bg='dim gray')
		self.window.title('Dungeon Game')
		windowPush = '1280x720+'+str(int(resolution[0])//2-640)+'+'+str(int(resolution[1])//2-360)
		self.window.geometry(windowPush)
		self.window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
		
		# menu bar
		self.menu = Menu(self.window)
		self.helpMenu = Menu(self.menu, tearoff=0)
		self.helpMenu.add_command(label="Map Legend", command=self.mapLegend)
		self.menu.add_cascade(label="Help", menu=self.helpMenu)
		self.saveMenu = Menu(self.menu, tearoff=0)
		self.saveMenu.add_command(label="Save", command=self.doNothing)
		self.menu.add_cascade(label="Save", menu=self.saveMenu)
		self.loadMenu = Menu(self.menu, tearoff=0)
		self.loadMenu.add_command(label="Load", command=self.doNothing)
		self.menu.add_cascade(label="Load", menu=self.loadMenu)
		self.window.config(menu=self.menu)
		
		#map screen
		self.mapScreen = Text(self.window, state='disabled', bg='gray9',fg='red4')
		self.mapScreen.place(x = 20, y = 20,width=330, height=490)
		
		#event screen
		self.eventScreen = Text(self.window, state='normal', bg='gray9',fg='red4', wrap=WORD)
		self.eventScreen.place(x = 380, y = 20,width = 870, height=490) #255 is y centered / 140 start end at 1250
		self.eventScreen.insert('end', "You wake up alone in a cave system wearing only a shredded up cheap tunic. Looking around, you see a narrow passageway in front and behind you. From behind you theres a constant low ringing sound but you can only make out a caved in wall of rocks, in front of you is a silent and empty, dark passgeway.\n\n")
		self.eventScreen.config(state='disabled')
		
		#status screen
		self.statusScreen = Text(self.window, state='normal', bg='gray9',fg='red4', wrap=WORD)
		self.statusScreen.place(x = 84, y = 530, width = 260, height=170) #split width by 3; 426 remainder 2; put 1 on each side then 3 sections; 166 extra for status / inv width; 83
		
		#button inputs
		self.buttonPushed = StringVar()

		self.button8Text = StringVar()
		self.b8 = Button(self.window, textvariable=self.button8Text, bg='gray9',fg='red4', command=lambda: self.buttonPushed.set('8'))
		self.b8.place(x = 615, y = 530, width = 50, height = 50)
		if keySet == "W, A, S, D, R":
			self.button8Text.set("╔═╗\n║W║\n╚═╝")
			self.window.bind('<KeyRelease-W>', lambda e: self.buttonPushed.set('8'))
			self.window.bind('<KeyRelease-w>', lambda e: self.buttonPushed.set('8'))
		else:
			self.button8Text.set("╔═╗\n║ 8 ║\n╚═╝")
			self.window.bind('<KeyRelease-8>', lambda e: self.buttonPushed.set('8'))

		self.button6Text = StringVar()
		self.b6 = Button(self.window, textvariable=self.button6Text, bg='gray9',fg='red4', command=lambda: self.buttonPushed.set('6'))
		self.b6.place(x = 675, y = 590, width = 50, height = 50)
		if keySet == "W, A, S, D, R":
			self.button6Text.set("╔═╗\n║ D ║\n╚═╝")
			self.window.bind('<KeyRelease-D>', lambda e: self.buttonPushed.set('6'))
			self.window.bind('<KeyRelease-d>', lambda e: self.buttonPushed.set('6'))
		else:
			self.button6Text.set("╔═╗\n║ 6 ║\n╚═╝")
			self.window.bind('<KeyRelease-6>', lambda e: self.buttonPushed.set('6'))


		self.button4Text = StringVar()
		self.b4 = Button(self.window, textvariable=self.button4Text, bg='gray9',fg='red4', command=lambda: self.buttonPushed.set('4'))
		self.b4.place(x = 555,y = 590,width = 50,height = 50) #427 + ; 170 in 426; 256 excess; 128 push; total 555
		if keySet == "W, A, S, D, R":
			self.button4Text.set("╔═╗\n║ A ║\n╚═╝")
			self.window.bind('<KeyRelease-A>', lambda e: self.buttonPushed.set('4'))
			self.window.bind('<KeyRelease-a>', lambda e: self.buttonPushed.set('4'))
		else:
			self.button4Text.set("╔═╗\n║ 4 ║\n╚═╝")
			self.window.bind('<KeyRelease-4>', lambda e: self.buttonPushed.set('4'))

		self.button2Text = StringVar()
		self.b2 = Button(self.window, textvariable=self.button2Text, bg='gray9',fg='red4', command=lambda: self.buttonPushed.set('2'))
		self.b2.place(x = 615, y = 650, width = 50, height = 50)
		if keySet == "W, A, S, D, R":
			self.button2Text.set("╔═╗\n║ S ║\n╚═╝")
			self.window.bind('<KeyRelease-S>', lambda e: self.buttonPushed.set('2'))
			self.window.bind('<KeyRelease-s>', lambda e: self.buttonPushed.set('2'))
		else:
			self.button2Text.set("╔═╗\n║ 2 ║\n╚═╝")
			self.window.bind('<KeyRelease-2>', lambda e: self.buttonPushed.set('2'))
		
		self.button5Text = StringVar()
		self.b5 = Button(self.window, textvariable=self.button5Text, bg='gray9',fg='red4', command=lambda: self.buttonPushed.set('5'))
		self.b5.place(x = 615, y = 590, width = 50, height = 50)
		if keySet == "W, A, S, D, R":
			self.button5Text.set("╔═╗\n║ R ║\n╚═╝")
			self.window.bind('<KeyRelease-R>', lambda e: self.buttonPushed.set('5'))
			self.window.bind('<KeyRelease-r>', lambda e: self.buttonPushed.set('5'))
		else:
			self.button5Text.set("╔═╗\n║ 5 ║\n╚═╝")
			self.window.bind('<KeyRelease-5>', lambda e: self.buttonPushed.set('5'))
		self.b5.config(state='disabled')

		#inventory screen
		self.inventoryScreen = Text(self.window, state='normal', bg='gray9',fg='red4', wrap=WORD)
		self.inventoryScreen.place(x = 936, y = 530,width = 260, height=170) #427+426; 853; push 83; total 936
		self.inventoryScreen.insert('end', "Usable inventory:\n\n")
		self.inventoryScreen.insert('end', "\nHeld inventory:\n\n")
		self.inventoryScreen.config(state='disabled')

	def doNothing(self):
		pass

	def mapLegend(self):

		self.helpMenu.entryconfigure(0, command=self.doNothing)

		def closed():
			self.helpMenu.entryconfigure(0, command=self.mapLegend)
			helpGuide.destroy()

		helpGuide = Toplevel()
		helpGuide.config(bg="dim gray")
		helpGuide.title('Map Legend')
		helpGuidePush = '840x420+'+str(int(self.resolution[0])//2-420)+'+'+str(int(self.resolution[1])//2-50)
		helpGuide.geometry(helpGuidePush)

		tutText = Text(helpGuide, wrap=WORD, state='normal', bg='gray9', font='Garmon 12', relief=FLAT, spacing1=5, spacing2=5)
		tutText.place(x = 20,y = 20, height = 380, width = 800)

		tutText.tag_configure('tagSelf', foreground='yellow')
		tutText.insert('end', "\nX is your current tile\n\n", 'tagSelf')

		tutText.tag_configure('tagWall', foreground='red4')
		tutText.insert('end', "█ is a wall\n\n", 'tagWall')

		tutText.tag_configure('tagWalk', foreground='peachpuff3')
		tutText.insert('end', "░ is a free walking tile\n\n", 'tagWalk')

		tutText.tag_configure('tagExcOne', foreground='yellow')
		tutText.insert('end', "a yellow ! is an item to pick up, ", 'tagExcOne')

		tutText.tag_configure('tagExcTwo', foreground='Orange')
		tutText.insert('end', " an orange one is a transition to the next stage, ", 'tagExcTwo')

		tutText.tag_configure('tagExcThree', foreground='white')
		tutText.insert('end', "other ! are a progression flag tile\n\n", 'tagExcThree')

		tutText.tag_configure('tagChance', foreground='indianRed1')
		tutText.insert('end', "▒ is a chance encounter tile\n\n", 'tagChance')

		tutText.tag_configure('tagPoison', foreground='dark green')
		tutText.insert('end', "⌂ is a poisonous fumes tile\n\n", 'tagPoison')

		tutText.tag_configure('tagExtreme', foreground='red')
		tutText.insert('end', "Ω is an extreme difficulty encounter tile\n\n", 'tagExtreme')

		tutText.tag_configure('tagHunter', foreground='indianRed1')
		tutText.insert('end', "Ö is an enemy that chases you\n\n", 'tagHunter')

		helpGuide.protocol("WM_DELETE_WINDOW", closed)

	def Update_Map(self, Map):
		self.mapScreen.config(state = 'normal')
		self.mapScreen.delete('1.0', 'end')
		for _ in range(0, (29-Map.lastRow)//2):
			self.mapScreen.insert('end', '\n')
		for y in range(0, Map.lastRow+1):
			for _ in range(0, (39-Map.lastCol)//2):
				self.mapScreen.insert('end', ' ')
			for x in range(0, Map.lastCol+1):
				if Map.mapData[y][x] in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='red4')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif y == Map.curY and x == Map.curX:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='yellow')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif Map.mapData[y][x] in [1, 51, 52, 53, 54, 55, 56, 57, 58, 59]:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='peachpuff3')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif Map.mapData[y][x] in [2, 20, 22, 23, 24, 25]:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='white')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif Map.mapData[y][x] == 21:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='dark orange')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif Map.mapData[y][x] in [3, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='yellow')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif Map.mapData[y][x] == 2000:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='paleTurqoise3')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif Map.mapData[y][x] in [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='red')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif Map.mapData[y][x] in [4, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 410, 420, 430, 440, 450, 460, 470, 480, 490, 411, 421, 431, 441, 451, 461, 471, 481, 491]:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='indianRed1')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif Map.mapData[y][x] == 5:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='dark green')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif Map.mapData[y][x] == 6:
					self.mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='black')
					self.mapScreen.insert('end', Map.shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == Map.lastCol:
						self.mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					self.mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

		self.mapScreen.config(state = 'disabled')

	def takeInput(self, sentence):
		self.eventScreen.config(state = 'normal')
		self.eventScreen.insert('end', sentence)
		self.eventScreen.see('end')
		self.eventScreen.config(state = 'disabled')
		self.buttonPushed.set('hi')
		self.window.wait_variable(self.buttonPushed)
		return self.buttonPushed.get()

	def eventMessage(self, sentence):
		self.eventScreen.config(state = 'normal')
		self.eventScreen.insert('end', sentence)
		self.eventScreen.see('end')
		self.eventScreen.config(state = 'disabled')

	def updateStatus(self, hero):
		self.statusScreen.config(state = 'normal')
		self.statusScreen.delete('1.0', 'end')
		self.statusScreen.insert('end', "Status:\n\nLevel:              "+str(hero.Stats['Lvl'])+"\nHealth:          "+str(hero.curHealth)+"/"+str(hero.Stats["Health"])+"\nStamina:         "+str(hero.curStam)+"/"+str(hero.Stats["Stam"]*10)+"\nSkill points:       "+str(hero.curTokens)+"\nExperience:         "+str(hero.Stats['Exp'])+"\nTo Level:           "+str(hero.Stats['ExpPoint']-hero.Stats['Exp']))
		self.statusScreen.config(state='disabled')

	def updateInventory(self, hero):
		self.inventoryScreen.config(state = 'normal')
		self.inventoryScreen.delete('1.0', 'end')
		self.inventoryScreen.insert('end', 'Inventory:\n\n')
		i = 0
		j = 0
		for item in hero.inventory:
			i+=1
			self.inventoryScreen.insert('end', str(i)+'.) '+item+'\n\n')
		self.inventoryScreen.insert('end', 'Held Inventory:\n\n')
		for item in hero.heldInventory:
			j+=1
			self.inventoryScreen.insert('end', str(j)+'.) '+item+'\n\n')