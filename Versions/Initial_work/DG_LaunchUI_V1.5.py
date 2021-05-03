from tkinter import *
import ctypes
import copy
import random
import pickle

#for save file -
#
#add menu bar with save/load
#when save is triggered populate a dictionary item that creates a file e.g. JSON or XML with all relevant data [current map, global and local conditionals, character stats, character inventory, map position]
#Game will always boot to intro level fresh, and load save will then parse that and read what map to go to; then update all conditional values, stats, inventories, and position on the map.
#or
#when save game is called run function, create disctionary of all relevant data; pickle_out = open("dict.pickle", "wb"); pickle.dump(example_dict, pickle_out), pickle_out.close()
#when load game is called run function, pickle_in = open("dict.pickle", "rb"); example_dict = pickle.load(pickle_in); then evaluate game state from example_dict
#or
#with open('file_name.pkl', 'wb') as pickled_file: -wb means write and then binary; file_name.pkl will result in a file_name.pkl file being placed in the same folder as the python code / application; a file path can be used instead.
#	pickle.dump(the_object, pickled_file)
#
#with open('file_name.pkl', 'rb') as pickled_file: -rb is read and then binary
#	imported_object = pickle.load(pickled_file)
#
# ----------------------------------------------------------------example save dictionary----------------------------------------------------------------
# dict_storing = {
# 	'currentMap': 'secondMap',
#	'shownMap': shownMap,
# 	'globalConditionals': globalConditionals,
# 	'localConditionals': localConditionals,
# 	'currentStats': Stats,
# 	'currentHealth': curHealth,
# 	'currentStamina': curStam,
# 	'inventory': inventory,
# 	'heldInventory': heldInventory,
# 	'currentPosition': [curY, curX],
# }
# so call save function passing these criteria, and then pickle into a file.
#---------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------goes into loading--------------------------------------------------------------------
#call load function, unpickle file
#parse 'currentMap' key and call that function to go to that map; !!!find a way to dictate pulling other information after the map data initializes normally!!!
#reassign shownmap to the stored shownMap
#parse global and local conditionals and assign the appropriate values
#parse stats and assign the current values
#parse current health, stamina, inventories, and map position and assign those values
#if loaded file has the charm of awareness place the 5 button
#---------------------------------------------------------------------------------------------------------------------------------------------------------
#
#possibility; create empty dict as global variable 'importedData', when load is ran alter global dict to loaded dict minus currentMap key. On each map after initialization do a try: method to reassign values from the global dict


def gamePlay(keySet, resolution):
	
	summOpen = [0]

	def mapLegend():

		def closed():
			summOpen[0] = 0
			helpGuide.destroy()

		if not summOpen[0]:
			summOpen[0] = 1

			helpGuide = Toplevel()
			helpGuide.config(bg="dim gray")
			helpGuide.title('Map Legend')
			helpGuidePush = '840x420+'+str(int(resolution[0])//2-420)+'+'+str(int(resolution[1])//2-50)
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

			tutText.tag_configure('tagSelf', foreground='dark green')
			tutText.insert('end', "⌂ is a poisonous fumes tile\n\n", 'tagSelf')

			tutText.tag_configure('tagExtreme', foreground='red')
			tutText.insert('end', "Ω is an extreme difficulty encounter tile\n\n", 'tagExtreme')

			tutText.tag_configure('tagHunter', foreground='indianRed1')
			tutText.insert('end', "Ö is an enemy that chases you\n\n", 'tagHunter')

			helpGuide.protocol("WM_DELETE_WINDOW", closed)


	#Hero's status
	Stats = {
		"Lvl": 1,
		"Exp": 0,
		"Atk": 4,
		"Def": 3,
		"Stam": 3,
		"Health": 25,
		"ExpPoint": 50,
		"Skills": [],
	}
	inventory = []
	heldInventory = []

	#Regularly called text
	combatTutorial="\nYou can press, '8' to attack the Opponent, '6' to reduce your damage received, '4' to get double stamina returned, '2' to view your skills menu, or '5' to view your item menu.\n"

	#Ending conditionals
	globalConditionals = {
		"acceptedMaiden": False,
		"firstMaidenDead": False,
		"AdomaDead": False,
		"hasCharm": False,
	}

	StamBar = Stats["Stam"]*10
	curStam = StamBar
	curHealth = Stats["Health"]
	curTokens = len(Stats["Skills"])

	importedData = {}

	gameWindow = Tk()
	gameWindow.configure(bg='dim gray')
	gameWindow.title('Dungeon Game')
	gameWindowPush = '1280x720+'+str(int(resolution[0])//2-640)+'+'+str(int(resolution[1])//2-360)
	gameWindow.geometry(gameWindowPush)

	gameWindow.protocol("WM_DELETE_WINDOW", lambda: gameWindow.destroy())

	menuBar = Menu(gameWindow)
	helpMenu = Menu(menuBar, tearoff=0)
	helpMenu.add_command(label="Map Legend", command=mapLegend)
	menuBar.add_cascade(label="Help", menu=helpMenu)
	gameWindow.config(menu=menuBar)

	mapScreen = Text(gameWindow, state='normal', bg='gray9',fg='red4')
	mapScreen.place(x = 20, y = 160,width=90, height=190)
	mapScreen.insert('end', "╔═════════╗\n")
	mapScreen.insert('end', "║         ║\n")
	mapScreen.insert('end', "║         ║\n")
	mapScreen.insert('end', "║         ║\n")
	mapScreen.insert('end', "║         ║\n")
	mapScreen.insert('end', "║         ║\n")
	mapScreen.insert('end', "║         ║\n")
	mapScreen.insert('end', "║         ║\n")
	mapScreen.insert('end', "║         ║\n")
	mapScreen.insert('end', "║         ║\n")
	mapScreen.insert('end', "╚═════════╝")
	mapScreen.config(state='disabled')

	eventScreen = Text(gameWindow, state='normal', bg='gray9',fg='red4', wrap=WORD)
	eventScreen.place(x = 140, y = 20,width = 1110, height=490) #255 is y centered / 140 start end at 1250
	eventScreen.insert('end', "You wake up alone in a cave system wearing only a shredded up cheap tunic. Looking around, you see a narrow passageway in front and behind you. From behind you theres a constant low ringing sound but you can only make out a caved in wall of rocks, in front of you is a silent and empty, dark passgeway.\n\n")
	eventScreen.config(state='disabled')

	statusScreen = Text(gameWindow, state='normal', bg='gray9',fg='red4', wrap=WORD)
	statusScreen.place(x = 84, y = 530, width = 260, height=170) #split width by 3; 426 remainder 2; put 1 on each side then 3 sections; 166 extra for status / inv width; 83
	statusScreen.insert('end', "Status:\n\nLevel:              "+str(Stats['Lvl'])+"\nHealth:          "+str(curHealth)+"/"+str(Stats["Health"])+"\nStamina:         "+str(curStam)+"/"+str(Stats["Stam"]*10)+"\nSkill points:       "+str(curTokens)+"\nExperience:         "+str(Stats['Exp'])+"\nTo Level:           "+str(Stats['ExpPoint']-Stats['Exp']))
	statusScreen.config(state='disabled')

	buttonPushed = StringVar()

	button8Text = StringVar()
	b8 = Button(gameWindow, textvariable=button8Text, bg='gray9',fg='red4', command=lambda: buttonPushed.set('8'))
	b8.place(x = 615, y = 530, width = 50, height = 50)
	if keySet[0] == "W, A, S, D, R":
		button8Text.set("╔═╗\n║W║\n╚═╝")
		gameWindow.bind('<KeyRelease-W>', lambda e: buttonPushed.set('8'))
		gameWindow.bind('<KeyRelease-w>', lambda e: buttonPushed.set('8'))
	else:
		button8Text.set("╔═╗\n║ 8 ║\n╚═╝")
		gameWindow.bind('<KeyRelease-8>', lambda e: buttonPushed.set('8'))

	button6Text = StringVar()
	b6 = Button(gameWindow, textvariable=button6Text, bg='gray9',fg='red4', command=lambda: buttonPushed.set('6'))
	b6.place(x = 675, y = 590, width = 50, height = 50)
	if keySet[0] == "W, A, S, D, R":
		button6Text.set("╔═╗\n║ D ║\n╚═╝")
		gameWindow.bind('<KeyRelease-D>', lambda e: buttonPushed.set('6'))
		gameWindow.bind('<KeyRelease-d>', lambda e: buttonPushed.set('6'))
	else:
		button6Text.set("╔═╗\n║ 6 ║\n╚═╝")
		gameWindow.bind('<KeyRelease-6>', lambda e: buttonPushed.set('6'))
	

	button4Text = StringVar()
	b4 = Button(gameWindow, textvariable=button4Text, bg='gray9',fg='red4', command=lambda: buttonPushed.set('4'))
	b4.place(x = 555,y = 590,width = 50,height = 50) #427 + ; 170 in 426; 256 excess; 128 push; total 555
	if keySet[0] == "W, A, S, D, R":
		button4Text.set("╔═╗\n║ A ║\n╚═╝")
		gameWindow.bind('<KeyRelease-A>', lambda e: buttonPushed.set('4'))
		gameWindow.bind('<KeyRelease-a>', lambda e: buttonPushed.set('4'))
	else:
		button4Text.set("╔═╗\n║ 4 ║\n╚═╝")
		gameWindow.bind('<KeyRelease-4>', lambda e: buttonPushed.set('4'))

	button2Text = StringVar()
	if keySet[0] == "W, A, S, D, R":
		button2Text.set("╔═╗\n║ S ║\n╚═╝")
		gameWindow.bind('<KeyRelease-S>', lambda e: buttonPushed.set('2'))
		gameWindow.bind('<KeyRelease-s>', lambda e: buttonPushed.set('2'))
	else:
		button2Text.set("╔═╗\n║ 2 ║\n╚═╝")
		gameWindow.bind('<KeyRelease-2>', lambda e: buttonPushed.set('2'))
	b2 = Button(gameWindow, textvariable=button2Text, bg='gray9',fg='red4', command=lambda: buttonPushed.set('2'))
	b2.place(x = 615, y = 650, width = 50, height = 50)

	button5Text = StringVar()
	if keySet[0] == "W, A, S, D, R":
		button5Text.set("╔═╗\n║ R ║\n╚═╝")
		gameWindow.bind('<KeyRelease-R>', lambda e: buttonPushed.set('5'))
		gameWindow.bind('<KeyRelease-r>', lambda e: buttonPushed.set('5'))
	else:
		button5Text.set("╔═╗\n║ 5 ║\n╚═╝")
		gameWindow.bind('<KeyRelease-5>', lambda e: buttonPushed.set('5'))
	b5 = Button(gameWindow, textvariable=button5Text, bg='gray9',fg='red4', command=lambda: buttonPushed.set('5'))
	b5.config(state = 'disabled')

	inventoryScreen = Text(gameWindow, state='normal', bg='gray9',fg='red4', wrap=WORD)
	inventoryScreen.place(x = 936, y = 530,width = 260, height=170) #427+426; 853; push 83; total 936
	inventoryScreen.insert('end', "Usable inventory:\n\n")
	for i in range(0, len(inventory)):
		inventoryScreen.insert('end', str(i+1)+'.) '+inventory[i]+'\n')
	inventoryScreen.insert('end', "\nHeld inventory:\n\n")
	for i in range(0, len(heldInventory)):
		inventoryScreen.insert('end', str(i+1)+'.) '+heldInventory[i]+'\n')
	inventoryScreen.config(state='disabled')

	#Map discovery
	def printEnvironment(Map, shownMap, curY, curX, lastRow, lastCol):
		
		def show(ValY, ValX, Map, shownMap, curY, curX):
			if Map[curY+ValY][curX+ValX] in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
				shownMap[str(curY+ValY)+"-"+str(curX+ValX)] = "█"
			elif Map[curY+ValY][curX+ValX] in [1, 51, 52, 53, 54, 55, 56, 57, 58, 59]:
				shownMap[str(curY+ValY)+"-"+str(curX+ValX)] = "░"
			elif Map[curY+ValY][curX+ValX] in [4, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]:
				shownMap[str(curY+ValY)+"-"+str(curX+ValX)] = "▒"
			elif Map[curY+ValY][curX+ValX] == 5:
				shownMap[str(curY+ValY)+"-"+str(curX+ValX)] = "⌂"
			elif Map[curY+ValY][curX+ValX] in [410, 420, 430, 440, 450, 460, 470, 480, 490, 411, 421, 431, 441, 451, 461, 471, 481, 491]:
				shownMap[str(curY+ValY)+"-"+str(curX+ValX)] = "Ö"
			elif Map[curY+ValY][curX+ValX] in [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]:
				shownMap[str(curY+ValY)+"-"+str(curX+ValX)] = "Ω"
			else:
				shownMap[str(curY+ValY)+"-"+str(curX+ValX)] = "!"
			return(shownMap)

		shownMap[str(curY)+"-"+str(curX)] = "X"
		
		#_________
		#_________
		#_________
		#_________
		#____X____
		#_________
		#_________
		#_________
		#_________

		if curX != 1:
			shownMap = show(0, -1, Map, shownMap, curY, curX)
			#_________
			#_________
			#_________
			#_________
			#___OX____
			#_________
			#_________
			#_________
			#_________
			if Map[curY][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
				if curY != lastRow-1:
					shownMap = show(1, -1, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#_________
					#___OX____
					#___O_____
					#_________
					#_________
					#_________
					if Map[curY+1][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curY != lastRow-2:
							shownMap = show(2, -1, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#___OX____
							#___O_____
							#___O_____
							#_________
							#_________
							if Map[curY+2][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curX != 2:
									shownMap = show(2, -2, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#___OX____
									#___O_____
									#__OO_____
									#_________
									#_________
								if curY != lastRow-3:
									shownMap = show(3, -1, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#___OX____
									#___O_____
									#___O_____
									#___O_____
									#_________
						if curX != 2:
							shownMap = show(1, -2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#___OX____
							#__OO_____
							#_________
							#_________
							#_________
							if Map[curY+1][curX-2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curX != 3:
									shownMap = show(1, -3, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#___OX____
									#_OOO_____
									#_________
									#_________
									#_________
								if curY != lastRow-2:
									shownMap = show(2, -2, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#___OX____
									#__OO_____
									#__O_____
									#_________
									#_________
				if curY != 1:	
					shownMap = show(-1, -1, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#___O_____
					#___OX____
					#_________
					#_________
					#_________
					#_________
					if Map[curY-1][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curY != 2:
							shownMap = show(-2, -1, Map, shownMap, curY, curX)
							#_________
							#_________
							#___O_____
							#___O_____
							#___OX____
							#_________
							#_________
							#_________
							#_________
							if Map[curY-2][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curX != 2:
								if curX != 2:
									shownMap = show(-2, -2, Map, shownMap, curY, curX)
									#_________
									#_________
									#__OO_____
									#___O_____
									#___OX____
									#_________
									#_________
									#_________
									#_________
								if curY != 3:
									shownMap = show(-3, -1, Map, shownMap, curY, curX)
									#_________
									#___O_____
									#___O_____
									#___O_____
									#___OX____
									#_________
									#_________
									#_________
									#_________
						if curX != 2:
							shownMap = show(-1, -2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#__OO_____
							#___OX____
							#_________
							#_________
							#_________
							#_________
							if Map[curY-1][curX-2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curY != 2:
									shownMap = show(-2, -2, Map, shownMap, curY, curX)
									#_________
									#_________
									#__O______
									#__OO_____
									#___OX____
									#_________
									#_________
									#_________
									#_________
								if curX != 3:
									shownMap = show(-1, -3, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_OOO_____
									#___OX____
									#_________
									#_________
									#_________
									#_________
				if curX != 2:
					shownMap = show(0, -2, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#_________
					#__OOX____
					#_________
					#_________
					#_________
					#_________
					if Map[curY][curX-2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curY != lastRow-1:
							shownMap = show(1, -2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#__OOX____
							#__O______
							#_________
							#_________
							#_________
							if Map[curY+1][curX-2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curX != 3:
								shownMap = show(1, -3, Map, shownMap, curY, curX)
								#_________
								#_________
								#_________
								#_________
								#__OOX____
								#_OO______
								#_________
								#_________
								#_________
						if curY != 1:	
							shownMap = show(-1, -2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#__O______
							#__OOX____
							#_________
							#_________
							#_________
							#_________
							if Map[curY-1][curX-2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curX != 3:
								shownMap = show(-1, -3, Map, shownMap, curY, curX)
								#_________
								#_________
								#_________
								#_OO______
								#__OOX____
								#_________
								#_________
								#_________
								#_________
						if curX != 3:
							shownMap = show(0, -3, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#_OOOX____
							#_________
							#_________
							#_________
							#_________
							if Map[curY][curX-3] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curY != lastRow-1:
									shownMap = show(1, -3, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#_OOOX____
									#_O_______
									#_________
									#_________
									#_________
								if curY != 1:	
									shownMap = show(-1, -3, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_O_______
									#_OOOX____
									#_________
									#_________
									#_________
									#_________
								if curX != 4:
									shownMap = show(0, -4, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#OOOOX____
									#_________
									#_________
									#_________
									#_________



		if curX != lastCol-1:
			shownMap = show(0, 1, Map, shownMap, curY, curX)
			#_________
			#_________
			#_________
			#_________
			#____XO___
			#_________
			#_________
			#_________
			#_________
			if Map[curY][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
				if curY != lastRow-1:
					shownMap = show(1, 1, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#_________
					#____XO___
					#_____O___
					#_________
					#_________
					#_________
					if Map[curY+1][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curY != lastRow-2:
							shownMap = show(2, 1, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____XO___
							#_____O___
							#_____O___
							#_________
							#_________
							if Map[curY+2][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curX != lastCol-2:
									shownMap = show(2, 2, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____XO___
									#_____O___
									#_____OO__
									#_________
									#_________
								if curY != lastRow-3:
									shownMap = show(3, 1, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____XO___
									#_____O___
									#_____O___
									#_____O___
									#_________
						if curX != lastCol-2:
							shownMap = show(1, 2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____XO___
							#_____OO__
							#_________
							#_________
							#_________
							if Map[curY+1][curX+2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curX != lastCol-3:
									shownMap = show(1, 3, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____XO___
									#_____OOO_
									#_________
									#_________
									#_________
								if curY != lastRow-2:
									shownMap = show(2, 2, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____XO___
									#_____OO__
									#______O_
									#_________
									#_________
				if curY != 1:	
					shownMap = show(-1, 1, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#_____O___
					#____XO___
					#_________
					#_________
					#_________
					#_________
					if Map[curY-1][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curY != 2:
							shownMap = show(-2, 1, Map, shownMap, curY, curX)
							#_________
							#_________
							#_____O___
							#_____O___
							#____XO___
							#_________
							#_________
							#_________
							#_________
							if Map[curY-2][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curX != lastCol-2:
									shownMap = show(-2, 2, Map, shownMap, curY, curX)
									#_________
									#_________
									#_____OO__
									#_____O___
									#____XO___
									#_________
									#_________
									#_________
									#_________
								if curY != 3:
									shownMap = show(-3, 1, Map, shownMap, curY, curX)
									#_________
									#_____O___
									#_____O___
									#_____O___
									#____XO___
									#_________
									#_________
									#_________
									#_________
						if curX != lastCol-2:
							shownMap = show(-1, 2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_____OO__
							#____XO___
							#_________
							#_________
							#_________
							#_________
							if Map[curY-1][curX+2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curY != 2:
								shownMap = show(-2, 2, Map, shownMap, curY, curX)
								#_________
								#_________
								#______O__
								#_____OO__
								#____XO___
								#_________
								#_________
								#_________
								#_________
				if curX != lastCol-2:
					shownMap = show(0, 2, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#_________
					#____XOO__
					#_________
					#_________
					#_________
					#_________
					if Map[curY][curX+2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curY != lastRow-1:
							shownMap = show(1, 2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____XOO__
							#______O__
							#_________
							#_________
							#_________
							if Map[curY+1][curX+2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curX != lastCol-3:
								shownMap = show(1, 3, Map, shownMap, curY, curX)
								#_________
								#_________
								#_________
								#_________
								#____XOO__
								#______OO_
								#_________
								#_________
								#_________
						if curY != 1:	
							shownMap = show(-1, 2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#______O__
							#____XOO__
							#_________
							#_________
							#_________
							#_________
							if Map[curY-1][curX+2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curX != lastCol-3:
								shownMap = show(-1, 3, Map, shownMap, curY, curX)
								#_________
								#_________
								#_________
								#______OO_
								#____XOO__
								#_________
								#_________
								#_________
								#_________
						if curX != lastCol-3:
							shownMap = show(0, 3, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____XOOO_
							#_________
							#_________
							#_________
							#_________
							if Map[curY][curX+3] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curY != lastRow-1:
									shownMap = show(1, 3, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____XOOO_
									#_______O_
									#_________
									#_________
									#_________
								if curY != 1:	
									shownMap = show(-1, 3, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_______O_
									#____XOOO_
									#_________
									#_________
									#_________
									#_________
								if curX != lastCol-4:
									shownMap = show(0, 4, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____XOOOO
									#_________
									#_________
									#_________
									#_________


		if curY != 1:
			shownMap = show(-1, 0, Map, shownMap, curY, curX)
			#_________
			#_________
			#_________
			#____O____
			#____X____
			#_________
			#_________
			#_________
			#_________
			if Map[curY-1][curX] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
				if curX != lastCol-1:
					shownMap = show(-1, 1, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#____OO___
					#____X____
					#_________
					#_________
					#_________
					#_________
					if Map[curY-1][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curX != lastCol-2:
							shownMap = show(-1, 2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#____OOO__
							#____X____
							#_________
							#_________
							#_________
							#_________
							if Map[curY-1][curX+2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curY != 2:
									shownMap = show(-2, 2, Map, shownMap, curY, curX)
									#_________
									#_________
									#______O_
									#____OOO__
									#____X____
									#_________
									#_________
									#_________
									#_________
								if curX != lastCol-3:
									shownMap = show(-1, 3, Map, shownMap, curY, curX)
									#_________
									#_________
									#________
									#____OOOO_
									#____X____
									#_________
									#_________
									#_________
									#_________
						if curY != 2:
							shownMap = show(-2, 1, Map, shownMap, curY, curX)
							#_________
							#_________
							#_____O___
							#____OO___
							#____X____
							#_________
							#_________
							#_________
							#_________
							if Map[curY-2][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curX != lastCol-2:
								shownMap = show(-2, 2, Map, shownMap, curY, curX)
								#_________
								#_________
								#_____OO__
								#____OO___
								#____X____
								#_________
								#_________
								#_________
								#_________
				if curX != 1:	
					shownMap = show(-1, -1, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#___OO____
					#____X____
					#_________
					#_________
					#_________
					#_________
					if Map[curY-1][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curY != 2:
							shownMap = show(-2, -1, Map, shownMap, curY, curX)
							#_________
							#_________
							#___O_____
							#___OO____
							#____X____
							#_________
							#_________
							#_________
							#_________
							if Map[curY-2][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curX != 2:
								shownMap = show(-2, -2, Map, shownMap, curY, curX)
								#_________
								#_________
								#__OO_____
								#___OO____
								#____X____
								#_________
								#_________
								#_________
								#_________
						if curX != 2:
							shownMap = show(-1, -2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#__OOO____
							#____X____
							#_________
							#_________
							#_________
							#_________
							if Map[curY-1][curX-2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curY != 2:
									shownMap = show(-2, -2, Map, shownMap, curY, curX)
									#_________
									#_________
									#__O______
									#__OOO____
									#____X____
									#_________
									#_________
									#_________
									#_________
								if curX != 3:
									shownMap = show(-1, -3, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_OOOO____
									#____X____
									#_________
									#_________
									#_________
									#_________
						
				if curY != 2:
					shownMap = show(-2, 0, Map, shownMap, curY, curX)
					#_________
					#_________
					#____O____
					#____O____
					#____X____
					#_________
					#_________
					#_________
					#_________
					if Map[curY-2][curX] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curX != lastCol-1:
							shownMap = show(-2, 1, Map, shownMap, curY, curX)
							#_________
							#_________
							#____OO___
							#____O____
							#____X____
							#_________
							#_________
							#_________
							#_________
							if Map[curY-2][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curY != 3:
								shownMap = show(-3, 1, Map, shownMap, curY, curX)
								#_________
								#_____O___
								#____OO___
								#____O____
								#____X____
								#_________
								#_________
								#_________
								#_________
						if curX != 1:	
							shownMap = show(-2, -1, Map, shownMap, curY, curX)
							#_________
							#_________
							#___OO____
							#____O____
							#____X____
							#_________
							#_________
							#_________
							#_________
							if Map[curY-2][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curY != 3:
								shownMap = show(-3, -1, Map, shownMap, curY, curX)
								#_________
								#___O_____
								#___OO____
								#____O____
								#____X____
								#_________
								#_________
								#_________
								#_________
						if curY != 3:
							shownMap = show(-3, 0, Map, shownMap, curY, curX)
							#_________
							#____O____
							#____O____
							#____O____
							#____X____
							#_________
							#_________
							#_________
							#_________
							if Map[curY-3][curX] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curX != lastCol-1:
									shownMap = show(-3, 1, Map, shownMap, curY, curX)
									#_________
									#____OO___
									#____O____
									#____O____
									#____X____
									#_________
									#_________
									#_________
									#_________
								if curX != 1:	
									shownMap = show(-3, -1, Map, shownMap, curY, curX)
									#_________
									#___OO____
									#____O____
									#____O____
									#____X____
									#_________
									#_________
									#_________
									#_________
								if curY != 4:
									shownMap = show(-4, 0, Map, shownMap, curY, curX)
									#____O____
									#____O____
									#____O____
									#____O____
									#____X____
									#_________
									#_________
									#_________
									#_________
								
		if curY != lastRow-1:
			shownMap = show(1, 0, Map, shownMap, curY, curX)
			#_________
			#_________
			#_________
			#_________
			#____X____
			#____O____
			#_________
			#_________
			#_________
			if Map[curY+1][curX] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
				if curX != lastCol-1:
					shownMap = show(1, 1, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#_________
					#____X____
					#____OO___
					#_________
					#_________
					#_________
					if Map[curY+1][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curX != lastCol-2:
							shownMap = show(1, 2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____X____
							#____OOO__
							#_________
							#_________
							#_________
							if Map[curY+1][curX+2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curY != lastRow-2:
									shownMap = show(2, 2, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____X____
									#____OOO__
									#______O__
									#_________
									#_________
								if curX != lastCol-3:
									shownMap = show(1, 3, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____X____
									#____OOOO_
									#_________
									#_________
									#_________
						if curY != lastRow-2:
							shownMap = show(2, 1, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____X____
							#____OO___
							#_____O___
							#_________
							#_________
							if Map[curY+2][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curX != lastCol-2:
								shownMap = show(2, 2, Map, shownMap, curY, curX)
								#_________
								#_________
								#_________
								#_________
								#____X____
								#____OO___
								#_____OO__
								#_________
								#_________
				if curX != 1:	
					shownMap = show(1, -1, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#_________
					#____X____
					#___OO____
					#_________
					#_________
					#_________
					if Map[curY+1][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curY != lastRow-2:
							shownMap = show(2, -1, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____X____
							#___OO____
							#___O_____
							#_________
							#_________
							if Map[curY+2][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curX != 2:
								shownMap = show(2, -2, Map, shownMap, curY, curX)
								#_________
								#_________
								#_________
								#_________
								#____X____
								#___OO____
								#__OO_____
								#_________
								#_________
						if curX != 2:
							shownMap = show(1, -2, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____X____
							#__OOO____
							#_________
							#_________
							#_________
							if Map[curY+1][curX-2] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curY != lastRow-2:
								if curY != lastRow-2:
									shownMap = show(2, -2, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____X____
									#__OOO____
									#__O______
									#_________
									#_________
								if curX != 3:
									shownMap = show(1, -3, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____X____
									#_OOOO____
									#_________
									#_________
									#_________
						
				if curY != lastRow-2:
					shownMap = show(2, 0, Map, shownMap, curY, curX)
					#_________
					#_________
					#_________
					#_________
					#____X____
					#____O____
					#____O____
					#_________
					#_________
					if Map[curY+2][curX] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
						if curX != lastCol-1:
							shownMap = show(2, 1, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____X____
							#____O____
							#____OO___
							#_________
							#_________
							if Map[curY+2][curX+1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curY != lastRow-3:
								shownMap = show(3, 1, Map, shownMap, curY, curX)
								#_________
								#_________
								#_________
								#_________
								#____X____
								#____O____
								#____OO___
								#_____O___
								#_________
						if curX != 1:	
							shownMap = show(2, -1, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____X____
							#____O____
							#___OO____
							#_________
							#_________
							if Map[curY+2][curX-1] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89] and curY != lastRow-3:
								shownMap = show(3, -1, Map, shownMap, curY, curX)
								#_________
								#_________
								#_________
								#_________
								#____X____
								#____O____
								#___OO____
								#___O_____
								#_________
						if curY != lastRow-3:
							shownMap = show(3, 0, Map, shownMap, curY, curX)
							#_________
							#_________
							#_________
							#_________
							#____X____
							#____O____
							#____O____
							#____O____
							#_________
							if Map[curY+3][curX] not in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
								if curX != lastCol-1:
									shownMap = show(3, 1, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____X____
									#____O____
									#____O____
									#____OO___
									#_________
								if curX != 1:	
									shownMap = show(3, -1, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____X____
									#____O____
									#____O____
									#___OO____
									#_________
								if curY != lastRow-4:
									shownMap = show(4, 0, Map, shownMap, curY, curX)
									#_________
									#_________
									#_________
									#_________
									#____X____
									#____O____
									#____O____
									#____O____
									#____O____
		return(shownMap)


	def updateStatus(curHealth, curStam, curTokens):
		statusScreen.config(state = 'normal')
		statusScreen.delete('1.0', 'end')
		statusScreen.insert('end', "Status:\n\nLevel:              "+str(Stats['Lvl'])+"\nHealth:          "+str(curHealth)+"/"+str(Stats["Health"])+"\nStamina:         "+str(curStam)+"/"+str(Stats["Stam"]*10)+"\nSkill points:       "+str(curTokens)+"\nExperience:         "+str(Stats['Exp'])+"\nTo Level:           "+str(Stats['ExpPoint']-Stats['Exp']))
		statusScreen.config(state='disabled')

	def eventMessage(sentence):
		eventScreen.config(state = 'normal')
		eventScreen.insert('end', sentence)
		eventScreen.see('end')
		eventScreen.config(state = 'disabled')

	def takeInput(sentence):
		eventScreen.config(state = 'normal')
		eventScreen.insert('end', sentence)
		eventScreen.see('end')
		eventScreen.config(state = 'disabled')
		buttonPushed.set('hi')
		gameWindow.wait_variable(buttonPushed)

	def maidenEncounter(curHealth, curStam, curTokens):
		globalConditionals["acceptedMaiden"] = True
		curTokens = len(Stats["Skills"])
		curHealth = min(max(curHealth + (Stats["Health"]), 0), Stats["Health"])
		curStam = min(max(curStam + StamBar, 0), StamBar)
		updateStatus(curHealth, curStam, curTokens)
		return(curHealth, curStam, curTokens)

	def restRecovery(curHealth, curStam, curTokens):
		curTokens = len(Stats["Skills"])
		curHealth = min(max(curHealth + (Stats["Health"]/2), 0), Stats["Health"])
		curStam = min(max(curStam + (StamBar/2), 0), StamBar)
		updateStatus(curHealth, curStam, curTokens)
		return(curHealth, curStam, curTokens)

	def useItem(curHealth, curStam, item, inCombat, OppName, OppStats, OppCurHealth, OppCurStam, OppStamBar):

		if item == "Stale bread":
			curStam = min(curStam + (Stats["Stam"]*10/4), Stats["Stam"]*10)
			eventMessage("\nYou start eating through a rather unpleasant loaf, you regain some stamina"+str(Stats["Stam"]*10/4)+" and your stamina is now "+str(curStam)+"\n")
			return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
		if item == "Bandages":
			curHealth = min(curHealth + (Stats["Health"]/4), Stats["Health"])
			eventMessage("\nYou wrap up some open wounds. You heal "+str(Stats["Health"]/4)+" and your health is now "+str(curHealth)+"\n")
			return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
		elif item == "Adrenaline":
			curStam = min(curStam + (Stats["Stam"]*5), Stats["Stam"]*10)
			eventMessage("\nYou consume some adrenaline, you regain some stamina"+str(Stats["Stam"]*5)+" and your stamina is now "+str(curStam)+"\n")
			return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
		elif item == "Oily water":
			#If Opponent is axe demon, Devora, Adoma, Imp, Shadow... deal % health damage and reduce their def by 2; if Opponent fire demon deal 2x the %health damage
			#If used out of combat eventMessage something like splash and do nothing; if used in combat on target not above eventMessage something like you throw a spritz of water... it doesn't seem to do much
			#will need to pass if in combat and string for Opponents name
			if not inCombat:
				eventMessage("\nsplash!\n")
				return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
			elif inCombat and OppName in ["axeDemon", "Devora", "Adoma", "imp", "Shadow"]:
				(OppCurHealth) = takeDamage((OppStats["Health"]/8), OppStats, OppCurHealth)
				OppStats["Def"]-=2
				return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
			elif inCombat and OppName == ("Fire Shadow"):
				(OppCurHealth) = takeDamage((OppStats["Health"]/4), OppStats, OppCurHealth)
				OppStats["Def"]-=2
				return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
			else:
				eventMessage("\nYou splash out the vials contents... nothing happened\n")
				return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)

	def fullInventoryPrompt(inventory, heldInventory):
		Inventory = ",".join(inventory[0:len(inventory-1)])
		HeldInventory = ",".join(heldInventory[0:len(heldInventory-1)])

		if len(inventory) == 4:
			return("\nYou have "+Inventory+" currently in your inventory. You found '"+inventory[3]+"'\n\nYou can:\n8.) Use an item to make room\n6.) Throw away an item\n")
			
		elif len(heldInventory) == 4:
			return("\nYou are holding "+HeldInventory+". You found a '"+heldInventory[3]+"'\n\nWhich item will you throw away?\n8.) "+heldInventory[0]+"\n6.) "+heldInventory[1]+"\n4.) "+heldInventory[2]+"\n2.) "+heldInventory[3]+"\n")
			
		else:
			inventoryString = ''
			n=8
			while i < len(inventory):
				inventoryString+=str(n)+".) "+inventory[i]+"\n"
				n-=2
				i+=1
			return("\nYou have "+Inventory+" currently in your inventory.\n\nWhich item will you use?\n"+inventoryString)
			

	def fullInventoryChoiceOne(curHealth, curStam, inventory, heldInventory, OppName, OppStats, OppCurHealth, OppCurStam, OppStamBar, buttonPushed):
		Inventory = ",".join(inventory[0:len(inventory)])
		HeldInventory = ",".join(heldInventory[0:len(heldInventory)])
		l = 0
		n = 8
		i = 0
		takeInput()
		choice = buttonPushed

		if len(inventory) == 4:
			while l == 0:
				if choice == 8:
					l+=1
					while l == 1:
						return("\nWhich item will you use?\n8.) "+inventory[0]+"\n6.) "+inventory[1]+"\n4.) "+inventory[2]+"\n2.) "+inventory[3]+"\n")

				elif choice == 6:
					l+=1
					return("\nWhich item will you throw away?\n8.) "+inventory[0]+"\n6.) "+inventory[1]+"\n4.) "+inventory[2]+"\n2.) "+inventory[3]+"\n")

		elif len(heldInventory) == 4:
			while l == 0:
				if choice == 8:
					choice = 0
				elif choice == 6:
					choice = 1
				elif choice == 4:
					choice = 2
				elif choice == 2:
					choice = 3
			inventory.remove(heldInventory[choice])
			return(curHealth, curStam, inventory, heldInventory, OppStats, OppCurHealth, OppCurStam)

		else:
			while l == 0:
				if len(inventory) == 1:
					if choice == 8:
						choice = 0
						l+=1
				elif len(inventory) == 2:
					if choice == 8:
						choice = 0
						l+=1
					elif choice == 6:
						choice = 1
						l+=1
				elif len(inventory) == 3:
					if choice == 8:
						choice = 0
						l+=1
					elif choice == 6:
						choice = 1
						l+=1
					elif choice == 4:
						choice = 2
						l+=1
			(curHealth, curStam, OppStats, OppCurHealth, OppCurStam) = useItem(curHealth, curStam, inventory[use], 1, OppName, OppStats, OppCurHealth, OppCurStam, OppStamBar)
			inventory.remove(inventory[use])
			return(curHealth, curStam, inventory, heldInventory, OppStats, OppCurHealth, OppCurStam)


	def fullInventoryChoiceTwo(curHealth, curStam, inventory, heldInventory, route):

		if route == 0:
			if use == 8:
				use = 0
			elif use == 6:
				use = 1
			elif use == 4:
				use = 2
			elif use == 2:
				use = 3
			(curHealth, curStam) = useItem(curHealth, curStam, StamBar, inventory[use], 0, "", [], 0, 0, 0)[0:2]
			inventory.remove(inventory[use])
			return(curHealth, curStam, inventory, heldInventory)

		if route == 1:
			if throw == 8:
				throw = 0
			elif throw == 6:
				throw = 1
			elif throw == 4:
				throw = 2
			elif throw == 2:
				throw = 3
			del inventory[throw]
			return(curHealth, curStam, inventory, heldInventory)

	def useSkill(curStam, OppCurStam, OppStamToAtk, curTokens):
		skillList = ", ".join(Stats["Skills"])
		promptString = ''
		promptString+="\nYour skills are "+skillList+".\n"
		promptString+="\nYou have "+curTokens+" skill points left, What skill do you want to use?\n"
		amountSkills = len(Stats["Skills"])
		numSkills = []
		k = 0
		while k < amountSkills+1:
			numSkills.append(str(k))
			k+=1
		i = 0
		while i < amountSkills:
			promptString+=(i, ".)", Stats["Skills"][i], "\n")
			i+=1
		promptString+=(i, ".) Don't use a skill\n")

		numSkills = []
		k = 0
		while k < len(Stats["Skills"])+1:
			numSkills.append(str(k))
			k+=1
		l = 0
		choice = ''
		while l == 0:
			takeInput(promptString)
			use = buttonPushed.get()
			if use == str(len(Stats["Skills"])):
				choice = "Back"
				l+=1
			elif Stats["Skills"][int(use)] == "Heavy_Blow" and curStam < 10:
				choice="\nYou do not have enough stamina to do that.\n"
			elif Stats["Skills"][int(use)] == "Counter" and curStam < 8:
				choice="\nYou do not have enough stamina to do that.\n"
			elif Stats["Skills"][int(use)] == "Shatter" and curStam < 8:
				choice="\nYou do not have enough stamina to do that.\n"
			elif Stats["Skills"][int(use)] == "Grapple" and curStam < 10:
				choice="\nYou do not have enough stamina to do that.\n"
			elif Stats["Skills"][int(use)] == "Flurry" and curStam < 30:
				choice="\nYou do not have enough stamina to do that.\n"
			elif Stats["Skills"][int(use)] == "Atemi" and (curStam < 8 or OppCurStam < OppStamToAtk):
				if curStam < 8:
					choice="\nYou do not have enough stamina to do that.\n"
				elif OppCurStam < OppStamToAtk:
					choice="\nYour Opponent does not have enough stamina to do that.\n"
			elif Stats["Skills"][int(use)] == "Datotsu" and curStam < 14:
				choice="\nYou do not have enough stamina to do that.\n"
			elif Stats["Skills"][int(use)] == "Haya_Suburi" and curStam < 12:
				choice="\nYou do not have enough stamina to do that.\n"
			elif Stats["Skills"][int(use)] == "Pierce" and curStam < 12:
				choice="\nYou do not have enough stamina to do that.\n"
			elif Stats["Skills"][int(use)] == "Kachinuki" and curStam < 8:
				choice="\nYou do not have enough stamina to do that.\n"
			else:
				l+=1
				choice = Stats["Skills"][int(use)]

		return(choice)

	def Heavy_Blow(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		OppCurHealth = takeDamage((Stats["Atk"]*1.5)-OppStats["Def"], OppStats, OppCurHealth)
		curStam = fatigueStatus((10-Stats["Stam"]), Stats, curStam)
		curTokens-=1
		fatiguedSentence = 0
		if OppCurStam >= OppStamToAtk:
			curHealth = takeDamage((OppStats["Atk"] - Stats["Def"]), Stats, curHealth)
			OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
		else:
			fatiguedSentence = 1
			OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam, fatiguedSentence)

	def Counter(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		curTokens-=1
		OppCurHealth = takeDamage(Stats["Atk"]-OppStats["Def"], OppStats, OppCurHealth)
		curStam = fatigueStatus(8-Stats["Stam"], Stats, curStam)
		fatiguedSentence = 0
		if OppCurStam >= OppStamToAtk:
			curHealth = takeDamage(((OppStats["Atk"] - Stats["Def"])//2), Stats, curHealth)
			OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
		else:
			fatiguedSentence = 1
			OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)

	def Meditate(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		curTokens-=1
		curStam = fatigueStatus(-3*Stats["Stam"], Stats, curStam)
		fatiguedSentence = 0
		if OppCurStam >= OppStamToAtk:
			curHealth = takeDamage(((OppStats["Atk"] - Stats["Def"])), Stats, curHealth)
			OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
		else:
			fatiguedSentence = 1
			OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)

	def Shatter(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		#Find a way to limit stacking
		curTokens-=1
		OppStats["Def"]-=2
		OppCurHealth = takeDamage(Stats["Atk"]-OppStats["Def"], OppStats, OppCurHealth)
		curStam = fatigueStatus(8-Stats["Stam"], Stats, curStam)
		fatiguedSentence = 0
		if OppCurStam >= OppStamToAtk:
			curHealth = takeDamage((OppStats["Atk"] - Stats["Def"]), Stats, curHealth)
			OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
		else:
			fatiguedSentence = 1
			OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)

	def Grapple(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		curTokens-=1
		OppCurStam = fatigueStatus((1.5*Stats["Atk"])-OppStats["Def"], OppStats, OppCurHealth)
		curStam = fatigueStatus(10-Stats["Stam"], Stats, curStam)
		OppCurStam = fatigueStatus(-OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)

	def Flurry(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		attacks = random.randint(1, 101)
		if attack >= 80:
			numAtk = 5
		elif attack >= 40:
			numAtk = 4
		else:
			numAtk = 3
		OppCurHealth = takeDamage((Stats["Atk"]*numAtk)-OppStats["Def"*numAtk], OppStats, OppCurHealth)
		curStam = fatigueStatus((6*numAtk)-(numAtk*Stats["Stam"]), Stats, curStam)
		curTokens-=1
		i = 0
		while i < numAtk:
			if OppCurStam >= OppStamToAtk:
				curHealth = takeDamage((OppStats["Atk"] - Stats["Def"]), Stats, curHealth)
				OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
			else:
				OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)

	def Atemi(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		#Come back to this when you build out enemy skills to check how it returns and functions.
		#Enemy skillsets slot 0 should always be the strongest swing excluding one time use triggered event skills
		#(OppStats, OppCurHealth, OppCurStam, OppStamBar) = eval(OppStats["Skills"][0]+'(OppStats, OppCurHealth, OppCurStam, OppStamBar, OppStats, OppCurHealth, OppCurStam, OppStamBar)')
		OppCurHealth = takeDamage((OppStats["Atk"]*1.5)-OppStats["Def"], OppStats, OppCurHealth)
		curStam = fatigueStatus((8-Stats["Stam"]), Stats, curStam)
		curTokens-=1
		OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)

	def Datotsu(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		OppCurHealth = takeDamage((Stats["Atk"]*1.5)-OppStats["Def"], OppStats, OppCurHealth)
		curStam = fatigueStatus((14-Stats["Stam"]), Stats, curStam)
		curTokens-=1
		fatiguedSentence = 0
		if OppCurStam >= OppStamToAtk:
			curHealth = takeDamage((OppStats["Atk"] - Stats["Def"]), Stats, curHealth)
			OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
		else:
			fatiguedSentence = 1
			OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)

	def Haya_Suburi(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		OppCurHealth = takeDamage((Stats["Atk"])-OppStats["Def"], OppStats, OppCurHealth)
		curStam = fatigueStatus((12-Stats["Stam"]), Stats, curStam)
		curTokens-=1
		fatiguedSentence = 0
		if OppCurStam >= OppStamToAtk:
			OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
		else:
			fatiguedSentence = 1
			OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)

	def Mokuso(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		curTokens-=1
		curStam = fatigueStatus(-4*Stats["Stam"], Stats, curStam)
		fatiguedSentence = 0
		if OppCurStam >= OppStamToAtk:
			curHealth = takeDamage(((OppStats["Atk"] - Stats["Def"])), Stats, curHealth)
			OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
		else:
			fatiguedSentence = 1
			OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)

	def Pierce(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		OppCurHealth = takeDamage(Stats["Atk"], OppStats, OppCurHealth)
		curStam = fatigueStatus((12-Stats["Stam"]), Stats, curStam)
		curTokens-=1
		fatiguedSentence = 0
		if OppCurStam >= OppStamToAtk:
			curHealth = takeDamage((OppStats["Atk"] - Stats["Def"]), Stats, curHealth)
			OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
		else:
			fatiguedSentence = 1
			OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)


	def Drain(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		curTokens-=1
		OppCurStam = fatigueStatus((Stats["Atk"]*1.5)-OppStats["Def"], OppStats, OppCurStam)
		curStam = fatigueStatus(-(1.5*Stats["Atk"]-OppStats["Def"]), Stats, curStam)
		OppCurStam = fatigueStatus(-OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)

	def Regenerate(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		curHealth = takeDamage(-(Stats["Health"]/6), Stats, curHealth)
		curStam = fatigueStatus((-Stats["Stam"]), Stats, curStam)
		curTokens-=1
		fatiguedSentence = 0
		if OppCurStam >= OppStamToAtk:
			curHealth = takeDamage((OppStats["Atk"] - Stats["Def"]), Stats, curHealth)
			OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
		else:
			fatiguedSentence = 1
			OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
		eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)


	def Kachinuki(curHealth, curStam, curTokens, Stats, OppStats, OppCurHealth, OppCurStam, OppStamToAtk):
		#Yeah I have no idea. Need to make a while loop to continuosly pick attack if stamina > 8 and min for curHealth = 1
		while curStam > 8:
			OppCurHealth = takeDamage(Stats["Atk"]-OppStats["Def"], OppStats, OppCurHealth)
			curStam = fatigueStatus((8-Stats["Stam"]), Stats, curStam)
			curTokens-=1
			if OppCurStam >= OppStamToAtk:
				curHealth = max(takeDamage((OppStats["Atk"] - Stats["Def"]), Stats, curHealth), 1)
				OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
			else:
				OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
			eventMessage("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n")
		return(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam)


	def CheckLvl(curHealth, curStam, curTokens):
		
		def upStats(curHealth, curStam, curTokens):
		
			def NewStats():
		
				skillsToLearn = ["Heavy_Blow", "Counter", "Meditate", "Shatter", "Grapple", "Flurry", "Atemi"]
				skillsString = ''

				if Stats["Lvl"] == 2:
					Stats["Atk"] = 6
					Stats["Def"] = 4
					Stats["Stam"] = 3
					Stats["Health"] = 30
					#Heavy Blow deals 1.5* attack stat

				elif Stats["Lvl"] == 3:
					Stats["Atk"] = 9
					Stats["Def"] = 6
					Stats["Stam"] = 3
					Stats["Health"] = 35
					#Counter skill blends pros of attack and defend

				elif Stats["Lvl"] == 4:
					Stats["Atk"] = 14
					Stats["Def"] = 8
					Stats["Stam"] = 3
					Stats["Health"] = 45
					#Meditate skill restores 1.5* rest actions stam

				elif Stats["Lvl"] == 5:
					Stats["Atk"] = 20
					Stats["Def"] = 11
					Stats["Stam"] = 4
					Stats["Health"] = 60
					#Shatter skill deals normal attack after reducing Opponents def, stacks 3 times max

				elif Stats["Lvl"] == 6:
					Stats["Atk"] = 28
					Stats["Def"] = 14
					Stats["Stam"] = 5
					Stats["Health"] = 80
					#Grapple does an attack selection ignoring the Opponents input and dealing stamina damage instead of health
				elif Stats["Lvl"] == 7:
					Stats["Atk"] = 36
					Stats["Def"] = 18
					Stats["Stam"] = 6
					Stats["Health"] = 100
					#Flurry uses 3-5 attacks in one turn, consequently 3-5 stamina lots however.

				elif Stats["Lvl"] == 8:
					Stats["Atk"] = 50
					Stats["Def"] = 22
					Stats["Stam"] = 8
					Stats["Health"] = 135
					#Atemi forces the Opponent into its largest attack, and redirects it onto its self.

				i = Stats['Lvl']
				if Stats['Lvl'] - LvlPre > 2:
					skillsString+="\nYou learned new skills, "
					while i > LvlPre:
						Stats["Skills"].append(skillsToLearn[i-2].strip())
						i-=1
					i = Stats['Lvl']
					while i > LvlPre+1:
						skillsString+=Stats["Skills"][i-2].replace("_", " ")+", "
						i-=1
					skillsString+=" and "+Stats["Skills"][i-2].replace("_", " ")+".\n"
				elif Stats['Lvl'] - LvlPre > 1:
					skillsString+="\nYou learned new skills, "
					while i > LvlPre:
						Stats["Skills"].append(skillsToLearn[i-2].strip())
						i-=1
					i = Stats['Lvl']
					while i > LvlPre+1:
						skillsString+=Stats["Skills"][i-2].replace("_", " ")
						i-=1
					skillsString+=" and "+Stats["Skills"][i-2].replace("_", " ")+".\n"
				else:
					Stats["Skills"].append(skillsToLearn[i-2].strip())
					skillsString+="You learned a new skill, "+Stats["Skills"][i-2].replace("_", " ")+".\n"

				eventMessage(skillsString)
				return

			if Stats["Lvl"]==2:
				Stats["ExpPoint"]=100
			elif Stats["Lvl"]==3:
				Stats["ExpPoint"]=150
			elif Stats["Lvl"]==4:
				Stats["ExpPoint"]=250
			elif Stats["Lvl"]==5:
				Stats["ExpPoint"]=400
			elif Stats["Lvl"]==6:
				Stats["ExpPoint"]=600
			else:
				Stats["Lvl"]=7
				Stats["ExpPoint"]=1000
			NewStats()
			curTokens = len(Stats["Skills"])
			curHealth = Stats["Health"]
			curStam = Stats["Stam"]*10
			return(curHealth, curStam, curTokens)

		LvlPre = Stats["Lvl"]
		if Stats["Exp"] < 50:
			Stats["Lvl"] = 1
		elif Stats["Exp"] < 100:
			Stats["Lvl"] = 2
		elif Stats["Exp"] < 150:
			Stats["Lvl"] = 3
		elif Stats["Exp"] < 250:
			Stats["Lvl"] = 4
		elif Stats["Exp"] < 400:
			Stats["Lvl"] = 5
		elif Stats["Exp"] < 600:
			Stats["Lvl"] = 6
		elif Stats["Exp"] < 1000:
			Stats["Lvl"] = 7
		else:
			Stats["Lvl"] = 8
		expToLevel = Stats["ExpPoint"] - Stats["Exp"]
		if LvlPre != Stats['Lvl']:
			eventMessage("\nCongratulations! Leveled up\n")
			(curHealth, curStam, curTokens) = upStats(curHealth, curStam, curTokens)
			updateStatus(curHealth, curStam, curTokens)
			return(curHealth, curStam, curTokens)
		else:
			eventMessage("\nExp to next level: " + str(expToLevel) + "\n")
			updateStatus(curHealth, curStam, curTokens)
			return(curHealth, curStam, curTokens)


	def swordCheckLvl(curHealth, curStam, curTokens):
		
		def upStats(curHealth, curStam, curTokens):
		
			def NewStats():
		
				skillsToLearn = ["Datotsu", "Haya_Suburi", "Mokuso", "Pierce", "Drain", "Regenerate", "Kachinuki"]
				skillsString = ''

				if Stats["Lvl"] == 2:
					Stats["Atk"] = 18
					Stats["Def"] = 12
					Stats["Stam"] = 4
					Stats["Health"] = 50
					#Datotsu skill is a 2 handed overhead strike that deals 1.5* normal attack damage
				elif Stats["Lvl"] == 3:
					Stats["Atk"] = 27
					Stats["Def"] = 16
					Stats["Stam"] = 4
					Stats["Health"] = 60
					#Haya_Suburi skill evades the Opponents attack and deals out one attack damage
				elif Stats["Lvl"] == 4:
					Stats["Atk"] = 36
					Stats["Def"] = 20
					Stats["Stam"] = 4
					Stats["Health"] = 80
					#Mokuso restores 3* stam return
				elif Stats["Lvl"] == 5:
					Stats["Atk"] = 45
					Stats["Def"] = 25
					Stats["Stam"] = 5
					Stats["Health"] = 100
					#pierce skill is normal attack ignoring Opponent defense
				elif Stats["Lvl"] == 6:
					Stats["Atk"] = 54
					Stats["Def"] = 32
					Stats["Stam"] = 7
					Stats["Health"] = 130
					#Drain skill uses blades magic to sap the Opponents stamina
				elif Stats["Lvl"] == 7:
					Stats["Atk"] = 66
					Stats["Def"] = 42
					Stats["Stam"] = 9
					Stats["Health"] = 160
					#Regenerate uses sword magic to heal self
				elif Stats["Lvl"] == 8:
					Stats["Atk"] = 84
					Stats["Def"] = 54
					Stats["Stam"] = 11
					Stats["Health"] = 200
					#Kachinuki is a multi-round choice that locks in attacks until stamina is too low to attack, 
					#and prevents health going below 1 until resolved 

				i = Stats['Lvl']
				if Stats['Lvl'] - LvlPre > 2:
					skillsString+="\nYou learned new skills, "
					while i > LvlPre:
						Stats["Skills"].append(skillsToLearn[i-2].strip())
						i-=1
					i = Stats['Lvl']
					while i > LvlPre+1:
						skillsString+=Stats["Skills"][i-2].replace("_", " ")+", "
						i-=1
					skillsString+=" and "+Stats["Skills"][i-2].replace("_", " ")+".\n"
				elif Stats['Lvl'] - LvlPre > 1:
					skillsString+="\nYou learned new skills, "
					while i > LvlPre:
						Stats["Skills"].append(skillsToLearn[i-2].strip())
						i-=1
					i = Stats['Lvl']
					while i > LvlPre+1:
						skillsString+=Stats["Skills"][i-2].replace("_", " ")
						i-=1
					skillsString+=" and "+Stats["Skills"][i-2].replace("_", " ")+".\n"
				else:
					Stats["Skills"].append(skillsToLearn[i-2].strip())
					skillsString+="You learned a new skill, "+Stats["Skills"][i-2].replace("_", " ")+".\n"

				eventMessage(skillsString)
				return

			if Stats["Lvl"]==2:
				Stats["ExpPoint"]=100
			elif Stats["Lvl"]==3:
				Stats["ExpPoint"]=150
			elif Stats["Lvl"]==4:
				Stats["ExpPoint"]=250
			elif Stats["Lvl"]==5:
				Stats["ExpPoint"]=400
			elif Stats["Lvl"]==6:
				Stats["ExpPoint"]=600
			else:
				Stats["Lvl"]=7
				Stats["ExpPoint"]=1000
			NewStats()
			curTokens = len(Stats["Skills"])
			curHealth = Stats["Health"]
			curStam = Stats["Stam"]*10
			return(curHealth, curStam, curTokens)

		LvlPre = Stats["Lvl"]
		if Stats["Exp"] < 50:
			Stats["Lvl"] = 1
		elif Stats["Exp"] < 100:
			Stats["Lvl"] = 2
		elif Stats["Exp"] < 150:
			Stats["Lvl"] = 3
		elif Stats["Exp"] < 250:
			Stats["Lvl"] = 4
		elif Stats["Exp"] < 400:
			Stats["Lvl"] = 5
		elif Stats["Exp"] < 600:
			Stats["Lvl"] = 6
		elif Stats["Exp"] < 1000:
			Stats["Lvl"] = 7
		else:
			Stats["Lvl"] = 8
		expToLevel = Stats["ExpPoint"] - Stats["Exp"]
		if LvlPre != Stats['Lvl']:
			eventMessage("\nCongratulations! Leveled up\n")
			(curHealth, curStam, curTokens) = upStats(curHealth, curStam, curTokens)
			updateStatus(curHealth, curStam, curTokens)
			return(curHealth, curStam, curTokens)
		else:
			eventMessage("\nExp to next level: " + str(expToLevel) + "\n")
			updateStatus(curHealth, curStam, curTokens)
			return(curHealth, curStam, curTokens)

	def updateMap(curMap, shownMap, curY, curX, lastRow, lastCol):
		shownMap = printEnvironment(curMap, shownMap, curY, curX, lastRow, lastCol)
		mapScreen.config(state = 'normal')
		mapScreen.delete('1.0', 'end')
		for y in range (0, lastRow+1):
			for x in range (0, lastCol+1):
				if curMap[y][x] in [0, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='red4')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif y == curY and x == curX:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='yellow')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif curMap[y][x] in [1, 51, 52, 53, 54, 55, 56, 57, 58, 59]:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='peachpuff3')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif curMap[y][x] in [2, 20, 22, 23, 24, 25]:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='white')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif curMap[y][x] == 21:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='dark orange')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif curMap[y][x] in [3, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='yellow')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif curMap[y][x] == 2000:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='paleTurqoise3')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif curMap[y][x] in [90, 91, 92, 93, 94, 95, 96, 97, 98, 99]:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='red')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif curMap[y][x] in [4, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 410, 420, 430, 440, 450, 460, 470, 480, 490, 411, 421, 431, 441, 451, 461, 471, 481, 491]:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='indianRed1')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif curMap[y][x] == 5:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='dark green')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')

				elif curMap[y][x] == 6:
					mapScreen.tag_configure('tag'+str(y)+'-'+str(x), foreground='black')
					mapScreen.insert('end', shownMap[str(y)+'-'+str(x)], 'tag'+str(y)+'-'+str(x))
					if x == lastCol:
						mapScreen.insert('end', '\n', 'tag'+str(y)+'-'+str(x))
					mapScreen.tag_add('tag'+str(y)+'-'+str(x), 'end')



		mapScreen.config(state = 'disabled')

	def takeDamage(damage, Stats, curHealth):
		curHealth = min(max(curHealth - damage, 0), Stats["Health"])
		return(curHealth)


	def fatigueStatus(fatigue, Stats, curStam):
		curStam = min(max(curStam - fatigue, 0), Stats["Stam"]*10)
		return(curStam)

	def basicCombat(curHealth, curStam, curTokens, inventory, heldInventory, stamToAtk, OppStats, OppStamToAtk, topCombatSentence, fatiguedSentence, endHealth, OppEndHealth):
		#skill storage
		skill = ""
		#turn counter
		turn = 0

		OppStamBar = OppStats["Stam"]*10
		OppCurStam = OppStamBar
		OppCurHealth = OppStats["Health"]

		eventMessage(combatTutorial)
		while OppCurHealth > OppEndHealth and curHealth > endHealth:
			updateStatus(curHealth, curStam, curTokens)
			takeInput("\nOpponent HP:      " + str(OppCurHealth) + "\nOpponent Stamina: " + str(OppCurStam) + "\n\n"+ topCombatSentence)

			if turn != 0 and turn%3 == 0 and curTokens <= len(Stats["Skills"]):
				curTokens+=1
			if buttonPushed.get() == '6':
				turn+=1
				if OppCurStam >= OppStamToAtk:
					curHealth = takeDamage(((OppStats["Atk"] - Stats["Def"])//2), Stats, curHealth)
					OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
					curStam = fatigueStatus(-Stats["Stam"], Stats, curStam)
				else:
					eventMessage(fatiguedSentence)
					OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
					curStam = fatigueStatus(-Stats["Stam"], Stats, curStam)
			elif buttonPushed.get() == '8':
				if curStam >= stamToAtk:
					turn+=1
					OppCurHealth = takeDamage((Stats["Atk"] - OppStats["Def"]), OppStats, OppCurHealth)
					curStam = fatigueStatus((6-Stats["Stam"]), Stats, curStam)
					if OppCurStam >= OppStamToAtk:
						curHealth = takeDamage(OppStats["Atk"] - Stats["Def"], Stats, curHealth)
						OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
					else:
						eventMessage(fatiguedSentence)
						OppCurStam = fatigueStatus(-OppStats["Stam"]*2, OppStats, OppCurStam)
				else:
					eventMessage("\nYou are too fatigued to attack\n")
			elif buttonPushed.get() == '4':
				if curStam >= (StamBar-3):
					eventMessage("\nYou've no need to rest now.\n")
				else:
					turn+=1
					curStam = fatigueStatus(-2*Stats["Stam"], StamBar, curStam)
					if OppCurStam >= OppStamToAtk:
						curHealth = takeDamage((OppStats["Atk"] - Stats["Def"]), Stats, curHealth)
						OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
					else:
						eventMessage("\nYou both sink down meekly, eyeing each other in anticipation\n")
						OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
					
			elif buttonPushed.get() == '2':
				if curTokens == 0:
					eventMessage("\nYou do not have any skill points to use.\n")
				else:					
					skill = useSkill(curStam, OppCurStam, OppStamToAtk, curTokens)
					if skill != "Back":
						turn+=1
						(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam) = eval(skill+"(curHealth, curStam, curTokens, OppStats, OppCurHealth, OppCurStam, stamToAtk, fatiguedSentence)")
			elif buttonPushed.get() == '5':
				if len(inventory) != 0:
					(curHealth, curStam, inventory, heldInventory, OppStats, OppCurHealth, OppCurStam) = fullInventory(curHealth, curStam, inventory, heldInventory, "Opp", OppStats, OppCurHealth, OppCurStam, OppStamBar)
					turn+=1
					curStam = fatigueStatus(-Stats["Stam"], Stats, curStam)
					if OppCurStam >= OppStamToAtk:
						curHealth = takeDamage((OppStats["Atk"] - Stats["Def"]), Stats, curHealth)
						OppCurStam = fatigueStatus((OppStamToAtk-OppStats["Stam"]), OppStats, OppCurStam)
					else:
						eventMessage(fatiguedSentence)
						OppCurStam = fatigueStatus(-2*OppStats["Stam"], OppStats, OppCurStam)
				else:
					eventMessage("\nYou don't have an item to use.\n")

		return(curHealth, curStam, curTokens, inventory)

	def secondMap(curHealth, curStam, curTokens, inventory, heldInventory, hasSword, disillusioned):

		mapScreen.place(x = 20,y = 20,width=330, height=490) #increase width 240
		eventScreen.place(x = 380,y = 20, width = 870, height = 490) #shrink width to compensate map size

		def skeletonCrazedManFight(curHealth, curStam, curTokens, inventory, heldInventory, hasSword, disillusioned):

			#skeleton stats
			OppStats = {
			"Atk": 9,
			"Def": 3,
			"Stam": 3,
			"Health": 40,
			}
			ExpGain = 50

			if hasSword:
				stamToAtk = 8
			else:
				stamToAtk = 6

			if hasSword or disillusioned:
				eventMessage("\nA wild looking man charges at you!\n")
				topCombatSentence = "The man is clearly aggressive and is coming into reach, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
				fatiguedSentence = "\nThe man squares up and lets out a low growl.\n"
				endCombatSentence = "\nYou defended yourself from the crazed mans attack\n"

			else:
				eventMessage("\nYou see a skeleton clumsily rushing towards you!\n")
				topCombatSentence = "The skeletons bones rattle as it jostles closer to you, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
				fatiguedSentence = "\nThe skeleton sways around and doesn't attack\n"
				endCombatSentence = "\nYou slew the skeleton!\n"

			(curHealth, curStam, curTokens, inventory) = basicCombat(curHealth, curStam, curTokens, inventory, heldInventory, stamToAtk, OppStats, 6, topCombatSentence, fatiguedSentence, 0, 0)		
			if curHealth == 0:
				eventMessage("\nBeaten and bloodied you collpase and fade out of consciousness for one last eternal slumber.")
				gameOver()
			Stats["Exp"] += ExpGain
			eventMessage("\n"+endCombatSentence+"\n\nYou gained 50 exp!")
			if hasSword:
				(Stats, StamBar, curTokens) = swordCheckLvl(Stats, curHealth, curStam, StamBar, curTokens)					
			else:
				(Stats, StamBar, curTokens) = CheckLvl(Stats, curHealth, curStam, StamBar, curTokens)			
			
			return(curHealth, curStam, curTokens, inventory)
		
		def giantSlugImpFight(curHealth, curStam, curTokens, inventory, heldInventory, hasSword, disillusioned):

			if hasSword:
				stamToAtk = 8
			else:
				stamToAtk = 6

			if hasSword or disillusioned:
				eventMessage("\nYou notice a small cackling imp creature sneakily walking around the area. When his eyes meet yours it whelps and he readies to fight you.\n")
				topCombatSentence = "The imp is growling in a high pitch voice while he squares up to you, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
				fatiguedSentence = "\nThe imp pants briskly and cowers away from you.\n"
				endCombatSentence = "\nYou defended yourself from the Imps attack\n"
				OppStats = {			
				"Atk": 12,
				"Def": 2,
				"Stam": 4,
				"Health": 25,
				}

			else:
				eventMessage("\nYou see a Giant Slug creeping towards you and furling its strange mouth around, it's most certainly looking to make a meal of you.\n")
				topCombatSentence = "The Giant Slug creeps towards you and lifts its body near the head slightly off the ground to be over your waist level, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
				fatiguedSentence = "\nThe Giant Slug sinks down dejectedly and it's eyes spin around dazed.\n"
				endCombatSentence = "\nYou slew the Giant Slug!\n"
				OppStats = {
				"Atk": 8,
				"Def": 3,
				"Stam": 3,
				"Health": 60,
				}

			(curHealth, curStam, curTokens, inventory) = basicCombat(curHealth, curStam, curTokens, inventory, heldInventory, stamToAtk, OppStats, 6, topCombatSentence, fatiguedSentence, 0, 0)		

			if curHealth == 0:
				eventMessage("\nBeaten and bloodied you collpase and fade out of consciousness for one last eternal slumber.")
				gameOver()		
			ExpGain = 50
			Stats["Exp"] += ExpGain
			eventMessage("\n", endCombatSentence, "\n\nYou gained", ExpGain, "exp!")
			if hasSword:
				(Stats, StamBar, curTokens) = swordCheckLvl(Stats, curHealth, curStam, StamBar, curTokens)					
			else:
				(Stats, StamBar, curTokens) = CheckLvl(Stats, curHealth, curStam, StamBar, curTokens)

			return(curHealth, curStam, curTokens, inventory)		
		
		def axeDemonSavageFight(curHealth, curStam, curTokens, inventory, heldInventory, hasSword, disillusioned):

			if hasSword:
				stamToAtk = 8
			else:
				stamToAtk = 6


			if hasSword or disillusioned:
				eventMessage("\nAn immense reptilian like humanoid being, with 2 gnarled and curved horns coming from its head, wielding a large two sided axe notices you and snarls angrily before marching towards you at an increasing pace.\n")
				topCombatSentence = "The creature slithers forward swiftly, one hand on the ground and the other hoisting the axe overhead, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
				fatiguedSentence = "\nThe creature slams the head of the axe down and uses it to hold itself up while it rests.\n"
				endCombatSentence = "\nYou defeated the giant creature!\n"

			else:
				eventMessage("\nThere's an immensely muscular man running his fingers along the edge of a double sided axe infront of you. For a moment you're excited to see another human in this cave and think perhaps you could work togetherm but only that breif moment. The man also sees you and lets out a low groaning noise before whipping the axe over his shoulder with ease and charging towards you.\n")
				topCombatSentence = "The man dashes forward quickly and drops one hand down to the ground while hoisting the axe overhead with the other, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
				fatiguedSentence = "\nThe man drops the axe head down under himself to help hold himself up as he rests.\n"
				endCombatSentence = "\nYou defended yourself from the mans attack\n"

			OppStats = {
			"Atk": 30,
			"Def": 8,
			"Stam": 4,
			"Health": 65,
			}

			(curHealth, curStam, curTokens, inventory) = basicCombat(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned, OppStats, 14, topCombatSentence, fatiguedSentence, endCombatSentence, 0, 0)

			if curHealth == 0:
				eventMessage("\nThe giant sliced you apart with their axe. You can no longer carry on.")
				gameOver()
			ExpGain = 150
			Stats["Exp"] += ExpGain
			eventMessage("\n", endCombatSentence, "\n\nYou gained", ExpGain, "exp!")
			if hasSword:
				(Stats, StamBar, curTokens) = swordCheckLvl(Stats, curHealth, curStam, StamBar, curTokens)					
			else:
				(Stats, StamBar, curTokens) = CheckLvl(Stats, curHealth, curStam, StamBar, curTokens)

			return(curHealth, curStam, curTokens, inventory)	
		
		def viciousBatFight(curHealth, curStam, curTokens, inventory, heldInventory, hasSword, disillusioned):

			if hasSword:
				stamToAtk = 8
			else:
				stamToAtk = 6

			eventMessage("\nA swarm of bats surround you scratching and biting at you.\n")
			topCombatSentence = "The bat whirls around you wildly, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
			fatiguedSentence = "\nThe bat lands down on a perch and tries to hide.\n"
			endCombatSentence = "\nYou took care of one of many bats.\n"
			OppStats = {
			"Atk": 4,
			"Def": 2,
			"Stam": 2,
			"Health": 15,
			}

			(curHealth, curStam, curTokens, inventory) = basicCombat(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned, OppStats, 4, topCombatSentence, fatiguedSentence, endCombatSentence, 0, 0)		

			if curHealth == 0:
				eventMessage("\nAmidst the swarm of bats one must have cut into a main artery. You bleed to death in the cavern.\n")
				gameOver()
			ExpGain = 10
			Stats["Exp"] += ExpGain
			eventMessage("\n", endCombatSentence, "\n\nYou gained", ExpGain, "exp!")
			if hasSword:
				(Stats, StamBar, curTokens) = swordCheckLvl(Stats, curHealth, curStam, StamBar, curTokens)					
			else:
				(Stats, StamBar, curTokens) = CheckLvl(Stats, curHealth, curStam, StamBar, curTokens)

			return(curHealth, curStam, curTokens, inventory)
		
		
		def starvedMenZombieFight(curHealth, curStam, curTokens, inventory, heldInventory, hasSword, disillusioned):

			if hasSword:
				stamToAtk = 8
			else:
				stamToAtk = 6

			if hasSword or disillusioned:
				eventMessage("\nA frail malnourished man spots you and clambers towards you. You cautiosly try to greet them but meet no response, only hungry eyes leering into your own.\n")
				topCombatSentence = "The man pulls out a small knife and clumsily stumbles towards you, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
				fatiguedSentence = "\nThe man fumbles in place struggling to do so much as stand.\n"
				endCombatSentence = "\nYou defended yourself succesfully, but somehow don't feel all too successful.\n"

			else:
				eventMessage("\nA husk of rotting flush that may have once been human slowly wobbles towards you.\n")
				topCombatSentence = "As the creature draws near it brandishes sharp looking claws, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
				fatiguedSentence = "\nThe creature stands dazed wobbling in place.\n"
				endCombatSentence = "\nYou defeated the creature!\n"
				
			OppStats = {
			"Atk": 12,
			"Def": 2,
			"Stam": 1.5,
			"Health": 45,
			}

			(curHealth, curStam, curTokens, inventory) = basicCombat(curHealth, curStam, curTokens, inventory, heldInventory, stamToAtk, OppStats, 6, topCombatSentence, fatiguedSentence, 0, 0)		

			if curHealth == 0:
				eventMessage("\nYou've been sliced apart and can no longer fight as you fall over and bleed out you simply hope your life will fade out before youre devoured.")
				gameOver()
			ExpGain = 50
			Stats["Exp"] += ExpGain
			eventMessage("\n", endCombatSentence, "\n\nYou gained", ExpGain, "exp!")
			if hasSword:
				(Stats, StamBar, curTokens) = swordCheckLvl(Stats, curHealth, curStam, StamBar, curTokens)					
			else:
				(Stats, StamBar, curTokens) = CheckLvl(Stats, curHealth, curStam, StamBar, curTokens)

			return(curHealth, curStam, curTokens, inventory)	
		
		
		def smallGolemBruteFight(curHealth, curStam, curTokens, inventory, heldInventory, hasSword, disillusioned):

			if hasSword:
				stamToAtk = 8
			else:
				stamToAtk = 6

			if hasSword or disillusioned:
				eventMessage("\nAs you walk along you're caught off guard when a pile of what you had thought to have been rocks stands and shuffles into a large humanoid form.\n")
				topCombatSentence = "The golem stamps towards you, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
				fatiguedSentence = "\nThe light flaring in the golems eyes dims and it stops in place for a moment.\n"
				endCombatSentence = "\nYou managed to beat the golem!\n"


			else:
				eventMessage("\nAs you walk through the opening you suddnely hear a loud stomping sound from behind you. When you turn what you see is a herculean looking man standing a head or two taller than the average man.\n")
				topCombatSentence = "The man is slowly and menacingly approaching, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
				fatiguedSentence = "\nThe man stops and stands still for a moment.\n"
				endCombatSentence = "\nThe amount of attacks the man was able to take was incredible but you finally bested him.\n"

			OppStats = {
			"Atk": 20,
			"Def": 16,
			"Stam": 2,
			"Health": 100,
			}

			(curHealth, curStam, curTokens, inventory) = basicCombat(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned, OppStats, 16, topCombatSentence, fatiguedSentence, endCombatSentence, 0, 0)		

			if curHealth == 0:
				eventMessage("\nBeaten and bloodied you collpase and fade out of consciousness for one last eternal slumber.")
				gameOver()
			ExpGain = 150
			Stats["Exp"] += ExpGain
			eventMessage("\n", endCombatSentence, "\n\nYou gained", ExpGain, "exp!")
			if hasSword:
				(Stats, StamBar, curTokens) = swordCheckLvl(Stats, curHealth, curStam, StamBar, curTokens)					
			else:
				(Stats, StamBar, curTokens) = CheckLvl(Stats, curHealth, curStam, StamBar, curTokens)

			return(curHealth, curStam, curTokens, inventory)	
		
		def crazedScientistFight(curHealth, curStam, curTokens, inventory, heldInventory, hasSword, disillusioned):

			if hasSword:
				stamToAtk = 8
			else:
				stamToAtk = 6

			eventMessage("\nA small man with a wild look about him and eyes glazed over white whirls around to face you as you approach and lets out a strange murmuring.\n")
			topCombatSentence = "The man starts to throw strange vials of liquids at you swipe with a very small blade, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
			fatiguedSentence = "\nThe man stumbles back and holds himself up on a bench behind him.\n"
			OppStats = {
			"Atk": 12,
			"Def": 5,
			"Stam": 4,
			"Health": 60,
			}

			(curHealth, curStam, curTokens, inventory) = basicCombat(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned, OppStats, 8, topCombatSentence, fatiguedSentence, endCombatSentence, 30, 0)
			if curHealth == 0:
				eventMessage("\nThe man seems to have severed some vital regions with his tiny blade. You can no longer move, and the scientist starts to force some strange substance down your throat. You'll likely become a test subject until you die.")
				gameOver()

			#Phase 2
			eventMessage("\nThe man lets out some angered groans and quickly drinks down a series of strange liquids before dropping the blade, expanding in size and approaching you.\n")
			topCombatSentence = "The enlargened man is swinging at you, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
			fatiguedSentence = "\nThe man starts to drink a strange vial.\n"
			endCombatSentence = "\nYou slayed the mad scientist.\n"
			OppStats = {
			"Atk": 15,
			"Def": 6,
			"Stam": 3,
			"Health": 30,
			}

			(curHealth, curStam, curTokens, inventory) = basicCombat(curHealth, curStam, curTokens, inventory, heldInventory, stamToAtk, OppStats, 6, topCombatSentence, fatiguedSentence, 0, 0)

			if curHealth == 0:
				eventMessage("\nBeaten and bloodied you collpase and fade out of consciousness for one last eternal slumber.")
				gameOver()
			ExpGain = 150
			Stats["Exp"] += ExpGain
			eventMessage("\n", endCombatSentence, "\n\nYou gained", ExpGain, "exp!")			
			(Stats, StamBar, curTokens) = CheckLvl(Stats, curHealth, curStam, StamBar, curTokens)

			return(curHealth, curStam, curTokens, inventory)

		def AdomaMap2Fight(curHealth, curStam, curTokens, inventory, heldInventory, hasSword, disillusioned):
		
			#Adoma stats
			AdomaStats = {
			"Atk": 50,
			"Def": 22,
			"Stam": 8,
			"Health": 135,
			}
			AdomaStamBar = AdomaStats["Stam"]*10
			AdomaCurStam = AdomaStamBar
			AdomaCurHealth = AdomaStats["Health"]

			eventMessage("\nYou approach a man in black robes garnished with sliver linings, but his hood down. He has a blend of white, silver, and black hair with burning red eyes.")

			if hasSword:
				eventMessage("As he in turn spots you he says \"hmm? it's far too soon for you my friend\" and suddenly the blade warps from your hand in to his own and in a blur he rushes forth and stabs it into your sternum.")
				gameOver()
			#build
			#build
			#build
			#build
			#build
			eventMessage("fight things")
			
			#build
			#build
			#build
			#build
			#build
			if AdomaCurHealth == 0:
				globalConditionals["AdomaDead"] = True
			else:
				eventMessage("\nYour eyes lock one final time with those burning red embers looking down on you before everything fades to black.")
			return(curHealth, curStam, curTokens, inventory)
		
		map2 = [[0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0],
		 		[0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0],
		 		[0,  0,  1,  0,  0,  0,  0, 41, 41, 41, 41, 41,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0, 0],
		 		[0,  0,  3,  1,  0,  0,  0, 41, 41, 41, 41, 41, 41,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0,  1,  1,  1,  0, 0],
		 		[0,  0,  1,  2,  1,  1,  1, 41, 41, 41, 41, 41, 41,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0,  0,  1,  6,  1,  1,  0,  0,  0,  0, 32,  0, 0],
		 		[0,  0,  0,  1,  1,  1,  1, 41, 41, 41, 41, 41, 41,  1,  1,  0,  0,  0,  1,  1,  1,  1,  1,  0,  1,  1,  1,  1, 20,  6,  6,  6,  1,  1,  0,  0,  0,  0,  0, 0],
		 		[0,  0,  0,  0,  1,  0,  0, 41, 41, 41, 41, 41, 41,  0,  1,  1,  0,  0,  0,  1,  1,  1,  0,  1,  1,  1,  1,  0,  0,  6,  6,  6,  6,  0,  0,  0,  0,  0,  0, 0],
		 		[0,  0,  0,  0,  0,  0,  0,  0, 41, 41, 41, 41, 41,  0,  1,  1,  0,  0,  0,  1,  1,  0,  1,  1,  1,  1,  0,  1,  0,  6,  6,  6,  0,  0,  0,  0,  0,  0,  0, 0],
	 			[0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  0,  1, 34,  1,  0,  0,  0,  1,  1,  0,  1,  0,  0,  0,  1,  1,  1,  0, 20,  0,  0,  0,  0,  0,  0,  1,  0, 0],
	 			[0, 35,  1,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  1,  0,  0,  0,  1,  1,  1,  0,  1,  1,  1,  1,  1,  1,  1,  0,  1,  0,  0,  0,  0,  0,  0,  1,  0, 0],
	 			[0,  1,  1,  1,  1,  1,  1,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  1,  1,  1,  0,  1,  1,  1,  1,  1,  0,  1,  1,  0,  1,  1,  1,  1,  1,  1,  0,  1,  0, 0],
	 			[0,  1,  0,  0,  1,  1,  0,  0,  0,  1,  1,  0,  0,  0,  0,  0,  0,  1,  1,  0,  1,  0,  0,  0,  0,  0, 42, 21, 21,  1,  0,  0,  0,  0,  0,  1,  1,  1,  0, 0],
	 			[0,  0,  0,  0,  0,  1,  0,  0,  0,  1,  1,  0,  0,  0,  0,  0,  1,  1,  1,  0, 42, 42, 42, 42, 42, 42, 42, 42, 42,  0,  1,  1,  1,  1,  0,  0,  0,  1,  0, 0],
	 			[0,  0,  0,  0,  0,  1,  0,  0,  0,  1,  1,  1,  0,  0,  0,  1,  1,  1,  0,  1, 42, 42, 42, 42, 42, 42, 42, 42, 42,  0,  1,  0,  0,  1,  1,  1,  0,  1,  0, 0],
	 			[0,  0,  0,  0,  0,  1,  0,  0,  0,  1,  0,  1,  1,  1,  1,  1,  1,  1,  0,  1, 42, 42, 42, 42, 42, 42, 42, 42,  0,  1,  1,  1,  1,  0,  1,  1,  0,  1,  0, 0],
	 			[0,  0,  0,  0,  0,  1,  1,  0,  1,  1,  0,  1,  1,  1,  1,  1,  1,  1,  0,  1, 42, 42, 42, 42, 42, 42, 42,  0, 43, 43, 43, 43,  1,  1,  0,  1,  0,  1,  0, 0],
	 			[0,  0,  0,  0,  1,  1,  1,  1,  1,  0, 44, 44, 44, 44,  0,  1,  1,  1,  0,  1, 42, 42, 42, 42, 42, 42, 42,  0, 43, 43, 43, 43,  1,  1,  0,  1,  0,  1,  0, 0],
	 			[0,  0,  0, 45, 45, 45, 45,  0,  1,  1,  0, 44, 44, 44, 44,  0,  1,  1,  1,  0,  1, 42, 42, 42, 42, 42,  0,  1, 43, 43, 43, 43,  1,  1,  0, 31,  0,  1,  0, 0],
	 			[0,  0,  0, 45, 45, 45, 45, 45,  0,  1,  0, 44, 44, 44, 44,  0,  1,  1,  1,  1,  0,  0,  0,  1, 42, 42,  0,  1, 43, 43, 43, 43,  0,  0,  0,  0,  0,  1,  0, 0],
	 			[0,  0,  0, 45, 45, 45, 45, 45,  0,  1,  1,  0, 44, 44, 44, 44,  0,  1,  1,  1,  1,  1,  1,  0,  1,  1,  0,  1, 43, 43, 43,  1,  1,  1,  1,  1,  1,  1,  0, 0],
	 			[0,  0, 45, 45, 45, 45, 45, 45, 45,  0, 99,  0, 44, 44, 44, 44, 44,  0,  1,  1,  1,  1,  1, 98,  1,  0,  1,  1,  1,  1,  1,  1,  0,  0,  0,  1,  0,  0,  0, 0],
	 			[0,  0,  0, 45, 45, 45, 45, 45, 45,  0,  1,  0,  0, 44, 44, 44,  1,  0,  1,  1,  0,  0,  0,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0,  1,  1,  1,  0,  0,  0, 0],
	 			[0,  0,  0,  0,  0, 45, 45, 45,  0, 46, 46, 46, 46,  0,  0,  1, 38,  0,  1,  1,  5,  5,  5,  5,  5,  5,  5,  0,  0,  0, 47, 47, 80, 80,  0,  1,  1,  0,  0, 0],
	 			[0,  0,  0,  0,  0, 45, 45, 45,  0, 46, 46, 46, 46, 46, 46,  0,  0,  0,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 47, 47,  0,  0,  0,  0,  1,  0,  0, 0],
	 			[0,  0,  0,  0,  0, 45, 45,  0, 46, 46, 46, 46, 46, 46, 46,  0,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  5, 47,  0,  0,  0,  0,  1,  0,  0, 0],
	 			[0,  0,  0,  0,  1, 45, 45,  0, 33, 46, 46, 46, 46, 46, 46,  0,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  5,  5,  5,  5,  0,  0,  0,  0,  0,  1,  0,  0, 0],
	 			[0,  0,  0, 36,  1,  1,  0,  0, 46, 46, 46, 46, 46, 46, 46,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  5,  5,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  0, 0],
	 			[0,  0,  0, 37,  1,  0,  0,  0,  0, 46, 46, 46, 46, 46,  0,  0,  0,  0,  1,  0,  0,  0,  0,  1,  5,  5,  5,  0,  0,  0,  0,  0,  1,  1,  0,  0,  1,  1,  0, 0],
	 			[0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0, 30, 90,  0,  0,  0,  0,  0,  0,  0,  1, 38,  0,  0,  1, 39,  0,  0, 0],
	 			[0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0]]

		shownMap = {
			"0-0": "╔", "0-1": "═", "0-2": "═", "0-3": "═", "0-4": "═", "0-5": "═", "0-6": "═", "0-7": "═", "0-8": "═", "0-9": "═", "0-10": "═", "0-11": "═", "0-12": "═", "0-13": "═", "0-14": "═", "0-15": "═", "0-16": "═", "0-17": "═", "0-18": "═", "0-19": "═", "0-20": "═", "0-21": "═", "0-22": "═", "0-23": "═", "0-24": "═", "0-25": "═", "0-26": "═", "0-27": "═", "0-28": "═", "0-29": "═", "0-30": "═", "0-31": "═", "0-32": "═", "0-33": "═", "0-34": "═", "0-35": "═", "0-36": "═", "0-37": "═", "0-38": "═", "0-39": "╗",
			"1-0": "║", "1-1": " ", "1-2": " ", "1-3": " ", "1-4": " ", "1-5": " ", "1-6": " ", "1-7": " ", "1-8": " ", "1-9": " ", "1-10": " ", "1-11": " ", "1-12": " ", "1-13": " ", "1-14": " ", "1-15": " ", "1-16": " ", "1-17": " ", "1-18": " ", "1-19": " ", "1-20": " ", "1-21": " ", "1-22": " ", "1-23": " ", "1-24": " ", "1-25": " ", "1-26": " ", "1-27": " ", "1-28": " ", "1-29": " ", "1-30": " ", "1-31": " ", "1-32": " ", "1-33": " ", "1-34": " ", "1-35": " ", "1-36": " ", "1-37": " ", "1-38": " ", "1-39": "║",
			"2-0": "║", "2-1": " ", "2-2": " ", "2-3": " ", "2-4": " ", "2-5": " ", "2-6": " ", "2-7": " ", "2-8": " ", "2-9": " ", "2-10": " ", "2-11": " ", "2-12": " ", "2-13": " ", "2-14": " ", "2-15": " ", "2-16": " ", "2-17": " ", "2-18": " ", "2-19": " ", "2-20": " ", "2-21": " ", "2-22": " ", "2-23": " ", "2-24": " ", "2-25": " ", "2-26": " ", "2-27": " ", "2-28": " ", "2-29": " ", "2-30": " ", "2-31": " ", "2-32": " ", "2-33": " ", "2-34": " ", "2-35": " ", "2-36": " ", "2-37": " ", "2-38": " ", "2-39": "║",
			"3-0": "║", "3-1": " ", "3-2": " ", "3-3": " ", "3-4": " ", "3-5": " ", "3-6": " ", "3-7": " ", "3-8": " ", "3-9": " ", "3-10": " ", "3-11": " ", "3-12": " ", "3-13": " ", "3-14": " ", "3-15": " ", "3-16": " ", "3-17": " ", "3-18": " ", "3-19": " ", "3-20": " ", "3-21": " ", "3-22": " ", "3-23": " ", "3-24": " ", "3-25": " ", "3-26": " ", "3-27": " ", "3-28": " ", "3-29": " ", "3-30": " ", "3-31": " ", "3-32": " ", "3-33": " ", "3-34": " ", "3-35": " ", "3-36": " ", "3-37": " ", "3-38": " ", "3-39": "║",
			"4-0": "║", "4-1": " ", "4-2": " ", "4-3": " ", "4-4": " ", "4-5": " ", "4-6": " ", "4-7": " ", "4-8": " ", "4-9": " ", "4-10": " ", "4-11": " ", "4-12": " ", "4-13": " ", "4-14": " ", "4-15": " ", "4-16": " ", "4-17": " ", "4-18": " ", "4-19": " ", "4-20": " ", "4-21": " ", "4-22": " ", "4-23": " ", "4-24": " ", "4-25": " ", "4-26": " ", "4-27": " ", "4-28": " ", "4-29": " ", "4-30": " ", "4-31": " ", "4-32": " ", "4-33": " ", "4-34": " ", "4-35": " ", "4-36": " ", "4-37": " ", "4-38": " ", "4-39": "║",
			"5-0": "║", "5-1": " ", "5-2": " ", "5-3": " ", "5-4": " ", "5-5": " ", "5-6": " ", "5-7": " ", "5-8": " ", "5-9": " ", "5-10": " ", "5-11": " ", "5-12": " ", "5-13": " ", "5-14": " ", "5-15": " ", "5-16": " ", "5-17": " ", "5-18": " ", "5-19": " ", "5-20": " ", "5-21": " ", "5-22": " ", "5-23": " ", "5-24": " ", "5-25": " ", "5-26": " ", "5-27": " ", "5-28": " ", "5-29": " ", "5-30": " ", "5-31": " ", "5-32": " ", "5-33": " ", "5-34": " ", "5-35": " ", "5-36": " ", "5-37": " ", "5-38": " ", "5-39": "║",
			"6-0": "║", "6-1": " ", "6-2": " ", "6-3": " ", "6-4": " ", "6-5": " ", "6-6": " ", "6-7": " ", "6-8": " ", "6-9": " ", "6-10": " ", "6-11": " ", "6-12": " ", "6-13": " ", "6-14": " ", "6-15": " ", "6-16": " ", "6-17": " ", "6-18": " ", "6-19": " ", "6-20": " ", "6-21": " ", "6-22": " ", "6-23": " ", "6-24": " ", "6-25": " ", "6-26": " ", "6-27": " ", "6-28": " ", "6-29": " ", "6-30": " ", "6-31": " ", "6-32": " ", "6-33": " ", "6-34": " ", "6-35": " ", "6-36": " ", "6-37": " ", "6-38": " ", "6-39": "║",
			"7-0": "║", "7-1": " ", "7-2": " ", "7-3": " ", "7-4": " ", "7-5": " ", "7-6": " ", "7-7": " ", "7-8": " ", "7-9": " ", "7-10": " ", "7-11": " ", "7-12": " ", "7-13": " ", "7-14": " ", "7-15": " ", "7-16": " ", "7-17": " ", "7-18": " ", "7-19": " ", "7-20": " ", "7-21": " ", "7-22": " ", "7-23": " ", "7-24": " ", "7-25": " ", "7-26": " ", "7-27": " ", "7-28": " ", "7-29": " ", "7-30": " ", "7-31": " ", "7-32": " ", "7-33": " ", "7-34": " ", "7-35": " ", "7-36": " ", "7-37": " ", "7-38": " ", "7-39": "║",
			"8-0": "║", "8-1": " ", "8-2": " ", "8-3": " ", "8-4": " ", "8-5": " ", "8-6": " ", "8-7": " ", "8-8": " ", "8-9": " ", "8-10": " ", "8-11": " ", "8-12": " ", "8-13": " ", "8-14": " ", "8-15": " ", "8-16": " ", "8-17": " ", "8-18": " ", "8-19": " ", "8-20": " ", "8-21": " ", "8-22": " ", "8-23": " ", "8-24": " ", "8-25": " ", "8-26": " ", "8-27": " ", "8-28": " ", "8-29": " ", "8-30": " ", "8-31": " ", "8-32": " ", "8-33": " ", "8-34": " ", "8-35": " ", "8-36": " ", "8-37": " ", "8-38": " ", "8-39": "║",
			"9-0": "║", "9-1": " ", "9-2": " ", "9-3": " ", "9-4": " ", "9-5": " ", "9-6": " ", "9-7": " ", "9-8": " ", "9-9": " ", "9-10": " ", "9-11": " ", "9-12": " ", "9-13": " ", "9-14": " ", "9-15": " ", "9-16": " ", "9-17": " ", "9-18": " ", "9-19": " ", "9-20": " ", "9-21": " ", "9-22": " ", "9-23": " ", "9-24": " ", "9-25": " ", "9-26": " ", "9-27": " ", "9-28": " ", "9-29": " ", "9-30": " ", "9-31": " ", "9-32": " ", "9-33": " ", "9-34": " ", "9-35": " ", "9-36": " ", "9-37": " ", "9-38": " ", "9-39": "║",
			"10-0": "║", "10-1": " ", "10-2": " ", "10-3": " ", "10-4": " ", "10-5": " ", "10-6": " ", "10-7": " ", "10-8": " ", "10-9": " ", "10-10": " ", "10-11": " ", "10-12": " ", "10-13": " ", "10-14": " ", "10-15": " ", "10-16": " ", "10-17": " ", "10-18": " ", "10-19": " ", "10-20": " ", "10-21": " ", "10-22": " ", "10-23": " ", "10-24": " ", "10-25": " ", "10-26": " ", "10-27": " ", "10-28": " ", "10-29": " ", "10-30": " ", "10-31": " ", "10-32": " ", "10-33": " ", "10-34": " ", "10-35": " ", "10-36": " ", "10-37": " ", "10-38": " ", "10-39": "║",
			"11-0": "║", "11-1": " ", "11-2": " ", "11-3": " ", "11-4": " ", "11-5": " ", "11-6": " ", "11-7": " ", "11-8": " ", "11-9": " ", "11-10": " ", "11-11": " ", "11-12": " ", "11-13": " ", "11-14": " ", "11-15": " ", "11-16": " ", "11-17": " ", "11-18": " ", "11-19": " ", "11-20": " ", "11-21": " ", "11-22": " ", "11-23": " ", "11-24": " ", "11-25": " ", "11-26": " ", "11-27": " ", "11-28": " ", "11-29": " ", "11-30": " ", "11-31": " ", "11-32": " ", "11-33": " ", "11-34": " ", "11-35": " ", "11-36": " ", "11-37": " ", "11-38": " ", "11-39": "║",
			"12-0": "║", "12-1": " ", "12-2": " ", "12-3": " ", "12-4": " ", "12-5": " ", "12-6": " ", "12-7": " ", "12-8": " ", "12-9": " ", "12-10": " ", "12-11": " ", "12-12": " ", "12-13": " ", "12-14": " ", "12-15": " ", "12-16": " ", "12-17": " ", "12-18": " ", "12-19": " ", "12-20": " ", "12-21": " ", "12-22": " ", "12-23": " ", "12-24": " ", "12-25": " ", "12-26": " ", "12-27": " ", "12-28": " ", "12-29": " ", "12-30": " ", "12-31": " ", "12-32": " ", "12-33": " ", "12-34": " ", "12-35": " ", "12-36": " ", "12-37": " ", "12-38": " ", "12-39": "║",
			"13-0": "║", "13-1": " ", "13-2": " ", "13-3": " ", "13-4": " ", "13-5": " ", "13-6": " ", "13-7": " ", "13-8": " ", "13-9": " ", "13-10": " ", "13-11": " ", "13-12": " ", "13-13": " ", "13-14": " ", "13-15": " ", "13-16": " ", "13-17": " ", "13-18": " ", "13-19": " ", "13-20": " ", "13-21": " ", "13-22": " ", "13-23": " ", "13-24": " ", "13-25": " ", "13-26": " ", "13-27": " ", "13-28": " ", "13-29": " ", "13-30": " ", "13-31": " ", "13-32": " ", "13-33": " ", "13-34": " ", "13-35": " ", "13-36": " ", "13-37": " ", "13-38": " ", "13-39": "║",
			"14-0": "║", "14-1": " ", "14-2": " ", "14-3": " ", "14-4": " ", "14-5": " ", "14-6": " ", "14-7": " ", "14-8": " ", "14-9": " ", "14-10": " ", "14-11": " ", "14-12": " ", "14-13": " ", "14-14": " ", "14-15": " ", "14-16": " ", "14-17": " ", "14-18": " ", "14-19": " ", "14-20": " ", "14-21": " ", "14-22": " ", "14-23": " ", "14-24": " ", "14-25": " ", "14-26": " ", "14-27": " ", "14-28": " ", "14-29": " ", "14-30": " ", "14-31": " ", "14-32": " ", "14-33": " ", "14-34": " ", "14-35": " ", "14-36": " ", "14-37": " ", "14-38": " ", "14-39": "║",
			"15-0": "║", "15-1": " ", "15-2": " ", "15-3": " ", "15-4": " ", "15-5": " ", "15-6": " ", "15-7": " ", "15-8": " ", "15-9": " ", "15-10": " ", "15-11": " ", "15-12": " ", "15-13": " ", "15-14": " ", "15-15": " ", "15-16": " ", "15-17": " ", "15-18": " ", "15-19": " ", "15-20": " ", "15-21": " ", "15-22": " ", "15-23": " ", "15-24": " ", "15-25": " ", "15-26": " ", "15-27": " ", "15-28": " ", "15-29": " ", "15-30": " ", "15-31": " ", "15-32": " ", "15-33": " ", "15-34": " ", "15-35": " ", "15-36": " ", "15-37": " ", "15-38": " ", "15-39": "║",
			"16-0": "║", "16-1": " ", "16-2": " ", "16-3": " ", "16-4": " ", "16-5": " ", "16-6": " ", "16-7": " ", "16-8": " ", "16-9": " ", "16-10": " ", "16-11": " ", "16-12": " ", "16-13": " ", "16-14": " ", "16-15": " ", "16-16": " ", "16-17": " ", "16-18": " ", "16-19": " ", "16-20": " ", "16-21": " ", "16-22": " ", "16-23": " ", "16-24": " ", "16-25": " ", "16-26": " ", "16-27": " ", "16-28": " ", "16-29": " ", "16-30": " ", "16-31": " ", "16-32": " ", "16-33": " ", "16-34": " ", "16-35": " ", "16-36": " ", "16-37": " ", "16-38": " ", "16-39": "║",
			"17-0": "║", "17-1": " ", "17-2": " ", "17-3": " ", "17-4": " ", "17-5": " ", "17-6": " ", "17-7": " ", "17-8": " ", "17-9": " ", "17-10": " ", "17-11": " ", "17-12": " ", "17-13": " ", "17-14": " ", "17-15": " ", "17-16": " ", "17-17": " ", "17-18": " ", "17-19": " ", "17-20": " ", "17-21": " ", "17-22": " ", "17-23": " ", "17-24": " ", "17-25": " ", "17-26": " ", "17-27": " ", "17-28": " ", "17-29": " ", "17-30": " ", "17-31": " ", "17-32": " ", "17-33": " ", "17-34": " ", "17-35": " ", "17-36": " ", "17-37": " ", "17-38": " ", "17-39": "║",
			"18-0": "║", "18-1": " ", "18-2": " ", "18-3": " ", "18-4": " ", "18-5": " ", "18-6": " ", "18-7": " ", "18-8": " ", "18-9": " ", "18-10": " ", "18-11": " ", "18-12": " ", "18-13": " ", "18-14": " ", "18-15": " ", "18-16": " ", "18-17": " ", "18-18": " ", "18-19": " ", "18-20": " ", "18-21": " ", "18-22": " ", "18-23": " ", "18-24": " ", "18-25": " ", "18-26": " ", "18-27": " ", "18-28": " ", "18-29": " ", "18-30": " ", "18-31": " ", "18-32": " ", "18-33": " ", "18-34": " ", "18-35": " ", "18-36": " ", "18-37": " ", "18-38": " ", "18-39": "║",
			"19-0": "║", "19-1": " ", "19-2": " ", "19-3": " ", "19-4": " ", "19-5": " ", "19-6": " ", "19-7": " ", "19-8": " ", "19-9": " ", "19-10": " ", "19-11": " ", "19-12": " ", "19-13": " ", "19-14": " ", "19-15": " ", "19-16": " ", "19-17": " ", "19-18": " ", "19-19": " ", "19-20": " ", "19-21": " ", "19-22": " ", "19-23": " ", "19-24": " ", "19-25": " ", "19-26": " ", "19-27": " ", "19-28": " ", "19-29": " ", "19-30": " ", "19-31": " ", "19-32": " ", "19-33": " ", "19-34": " ", "19-35": " ", "19-36": " ", "19-37": " ", "19-38": " ", "19-39": "║",
			"20-0": "║", "20-1": " ", "20-2": " ", "20-3": " ", "20-4": " ", "20-5": " ", "20-6": " ", "20-7": " ", "20-8": " ", "20-9": " ", "20-10": " ", "20-11": " ", "20-12": " ", "20-13": " ", "20-14": " ", "20-15": " ", "20-16": " ", "20-17": " ", "20-18": " ", "20-19": " ", "20-20": " ", "20-21": " ", "20-22": " ", "20-23": " ", "20-24": " ", "20-25": " ", "20-26": " ", "20-27": " ", "20-28": " ", "20-29": " ", "20-30": " ", "20-31": " ", "20-32": " ", "20-33": " ", "20-34": " ", "20-35": " ", "20-36": " ", "20-37": " ", "20-38": " ", "20-39": "║",
			"21-0": "║", "21-1": " ", "21-2": " ", "21-3": " ", "21-4": " ", "21-5": " ", "21-6": " ", "21-7": " ", "21-8": " ", "21-9": " ", "21-10": " ", "21-11": " ", "21-12": " ", "21-13": " ", "21-14": " ", "21-15": " ", "21-16": " ", "21-17": " ", "21-18": " ", "21-19": " ", "21-20": " ", "21-21": " ", "21-22": " ", "21-23": " ", "21-24": " ", "21-25": " ", "21-26": " ", "21-27": " ", "21-28": " ", "21-29": " ", "21-30": " ", "21-31": " ", "21-32": " ", "21-33": " ", "21-34": " ", "21-35": " ", "21-36": " ", "21-37": " ", "21-38": " ", "21-39": "║",
			"22-0": "║", "22-1": " ", "22-2": " ", "22-3": " ", "22-4": " ", "22-5": " ", "22-6": " ", "22-7": " ", "22-8": " ", "22-9": " ", "22-10": " ", "22-11": " ", "22-12": " ", "22-13": " ", "22-14": " ", "22-15": " ", "22-16": " ", "22-17": " ", "22-18": " ", "22-19": " ", "22-20": " ", "22-21": " ", "22-22": " ", "22-23": " ", "22-24": " ", "22-25": " ", "22-26": " ", "22-27": " ", "22-28": " ", "22-29": " ", "22-30": " ", "22-31": " ", "22-32": " ", "22-33": " ", "22-34": " ", "22-35": " ", "22-36": " ", "22-37": " ", "22-38": " ", "22-39": "║",
			"23-0": "║", "23-1": " ", "23-2": " ", "23-3": " ", "23-4": " ", "23-5": " ", "23-6": " ", "23-7": " ", "23-8": " ", "23-9": " ", "23-10": " ", "23-11": " ", "23-12": " ", "23-13": " ", "23-14": " ", "23-15": " ", "23-16": " ", "23-17": " ", "23-18": " ", "23-19": " ", "23-20": " ", "23-21": " ", "23-22": " ", "23-23": " ", "23-24": " ", "23-25": " ", "23-26": " ", "23-27": " ", "23-28": " ", "23-29": " ", "23-30": " ", "23-31": " ", "23-32": " ", "23-33": " ", "23-34": " ", "23-35": " ", "23-36": " ", "23-37": " ", "23-38": " ", "23-39": "║",
			"24-0": "║", "24-1": " ", "24-2": " ", "24-3": " ", "24-4": " ", "24-5": " ", "24-6": " ", "24-7": " ", "24-8": " ", "24-9": " ", "24-10": " ", "24-11": " ", "24-12": " ", "24-13": " ", "24-14": " ", "24-15": " ", "24-16": " ", "24-17": " ", "24-18": " ", "24-19": " ", "24-20": " ", "24-21": " ", "24-22": " ", "24-23": " ", "24-24": " ", "24-25": " ", "24-26": " ", "24-27": " ", "24-28": " ", "24-29": " ", "24-30": " ", "24-31": " ", "24-32": " ", "24-33": " ", "24-34": " ", "24-35": " ", "24-36": " ", "24-37": " ", "24-38": " ", "24-39": "║",
			"25-0": "║", "25-1": " ", "25-2": " ", "25-3": " ", "25-4": " ", "25-5": " ", "25-6": " ", "25-7": " ", "25-8": " ", "25-9": " ", "25-10": " ", "25-11": " ", "25-12": " ", "25-13": " ", "25-14": " ", "25-15": " ", "25-16": " ", "25-17": " ", "25-18": " ", "25-19": " ", "25-20": " ", "25-21": " ", "25-22": " ", "25-23": " ", "25-24": " ", "25-25": " ", "25-26": " ", "25-27": " ", "25-28": " ", "25-29": " ", "25-30": " ", "25-31": " ", "25-32": " ", "25-33": " ", "25-34": " ", "25-35": " ", "25-36": " ", "25-37": " ", "25-38": " ", "25-39": "║",
			"26-0": "║", "26-1": " ", "26-2": " ", "26-3": " ", "26-4": " ", "26-5": " ", "26-6": " ", "26-7": " ", "26-8": " ", "26-9": " ", "26-10": " ", "26-11": " ", "26-12": " ", "26-13": " ", "26-14": " ", "26-15": " ", "26-16": " ", "26-17": " ", "26-18": " ", "26-19": " ", "26-20": " ", "26-21": " ", "26-22": " ", "26-23": " ", "26-24": " ", "26-25": " ", "26-26": " ", "26-27": " ", "26-28": " ", "26-29": " ", "26-30": " ", "26-31": " ", "26-32": " ", "26-33": " ", "26-34": " ", "26-35": " ", "26-36": " ", "26-37": " ", "26-38": " ", "26-39": "║",
			"27-0": "║", "27-1": " ", "27-2": " ", "27-3": " ", "27-4": " ", "27-5": " ", "27-6": " ", "27-7": " ", "27-8": " ", "27-9": " ", "27-10": " ", "27-11": " ", "27-12": " ", "27-13": " ", "27-14": " ", "27-15": " ", "27-16": " ", "27-17": " ", "27-18": " ", "27-19": " ", "27-20": " ", "27-21": " ", "27-22": " ", "27-23": " ", "27-24": " ", "27-25": " ", "27-26": " ", "27-27": " ", "27-28": " ", "27-29": " ", "27-30": " ", "27-31": " ", "27-32": " ", "27-33": " ", "27-34": " ", "27-35": " ", "27-36": " ", "27-37": " ", "27-38": " ", "27-39": "║",
			"28-0": "║", "28-1": " ", "28-2": " ", "28-3": " ", "28-4": " ", "28-5": " ", "28-6": " ", "28-7": " ", "28-8": " ", "28-9": " ", "28-10": " ", "28-11": " ", "28-12": " ", "28-13": " ", "28-14": " ", "28-15": " ", "28-16": " ", "28-17": " ", "28-18": " ", "28-19": " ", "28-20": " ", "28-21": " ", "28-22": " ", "28-23": " ", "28-24": " ", "28-25": " ", "28-26": " ", "28-27": " ", "28-28": " ", "28-29": " ", "28-30": " ", "28-31": " ", "28-32": " ", "28-33": " ", "28-34": " ", "28-35": " ", "28-36": " ", "28-37": " ", "28-38": " ", "28-39": "║",
			"29-0": "╚", "29-1": "═", "29-2": "═", "29-3": "═", "29-4": "═", "29-5": "═", "29-6": "═", "29-7": "═", "29-8": "═", "29-9": "═", "29-10": "═", "29-11": "═", "29-12": "═", "29-13": "═", "29-14": "═", "29-15": "═", "29-16": "═", "29-17": "═", "29-18": "═", "29-19": "═", "29-20": "═", "29-21": "═", "29-22": "═", "29-23": "═", "29-24": "═", "29-25": "═", "29-26": "═", "29-27": "═", "29-28": "═", "29-29": "═", "29-30": "═", "29-31": "═", "29-32": "═", "29-33": "═", "29-34": "═", "29-35": "═", "29-36": "═", "29-37": "═", "29-38": "═", "29-39": "╝",
		}

		curY = 28
		curX = 18
		lastRow = 29
		lastCol = 39

		foes1 = 15
		foes2 = 15
		foes3 = 40
		foes4 = 15
		foes5 = 15
		foes6 = 15

		if hasSword or disillusioned:
			for y, outer in enumerate(map2):
				for x, inner in enumerate(outer):
					if map2[y][x] == 80:
						map2[y][x] = 1
			for y, outer in enumerate(map2):
				for x, inner in enumerate(outer):
					if map2[y][x] == 43:
						map2[y][x] = 1

		charmUsed = 0

		while curHealth > 0:

			if foes2 == 14:
				for y, outer in enumerate(map2):
					for x, inner in enumerate(outer):
						if map2[y][x] == 21:
							map2[y][x] = 42

			if foes1 == 0:
				for y, outer in enumerate(map2):
					for x, inner in enumerate(outer):
						if map2[y][x] == 41:
							map2[y][x] = 1

			if foes2 == 0:
				for y, outer in enumerate(map2):
					for x, inner in enumerate(outer):
						if map2[y][x] == 42:
							map2[y][x] = 1

			if foes3 == 0:
				for y, outer in enumerate(map2):
					for x, inner in enumerate(outer):
						if map2[y][x] == 43:
							map2[y][x] = 1

			if foes4 == 0:
				for y, outer in enumerate(map2):
					for x, inner in enumerate(outer):
						if map2[y][x] == 44:
							map2[y][x] = 1

			if foes5 == 0:
				for y, outer in enumerate(map2):
					for x, inner in enumerate(outer):
						if map2[y][x] == 45:
							map2[y][x] = 1

			if foes6 == 0:
				for y, outer in enumerate(map2):
					for x, inner in enumerate(outer):
						if map2[y][x] == 46:
							map2[y][x] = 1

			updateMap(map2, shownMap, curY, curX, lastRow, lastCol)

			if globalConditionals['hasCharm']:
				takeInput("\nmove up, down, right, or left?\n\n8.) Up\n6.) Right\n4.) Left\n2.) Down\n5.) Rest\n\n")
			else:
				takeInput("\nmove up, down, right, or left?\n\n8.) Up\n6.) Right\n4.) Left\n2.) Down\n\n")

			#Moving Down
			if buttonPushed.get() == "2":
				if curY == lastRow-1 or map2[curY+1][curX] in [0, 80]:
					eventMessage("\nCannot move down\n")

				elif map2[curY+1][curX] == 1:
					curY+=1

				#Items
				elif map2[curY+1][curX] == 31:
					curY+=1
					eventMessage("\nYou found some bandages!\n")
					if len(inventory) <= 3:
						inventory.append("Bandages")
					else:
						inventory.append("Bandages")
						(curHealth, curStam, inventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[0:3]
					map2[curY][curX] = 1
			
				elif map2[curY+1][curX] == 32:
					curY+=1
					eventMessage("\nYou found a Charm of Awareness. Now you can press 5 to rest and gain half of your health and stamina back anywhere on the map, but you may be attacked and have to fight.\n")
					globalConditionals['hasCharm'] = True
					b5.place(x = 615, y = 590, width = 50, height = 50)
					b5.config(state = 'normal')
					map2[curY][curX] = 1

				elif map2[curY+1][curX] == 33:
					curY+=1
					eventMessage("\nYou found some Oily water!\n")
					if len(inventory) <= 3:
						inventory.append("Oily water")
					else:
						inventory.append("Oily water")
						(curHealth, curStam, inventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[0:3]
					map2[curY][curX] = 1

				elif map2[curY+1][curX] == 34:
					curY+=1
					eventMessage("\nYou found a salt rock!\n")
					if len(heldInventory) <= 3:
						heldInventory.append("Salt rock")
					else:
						heldInventory.append("Salt rock")
						(heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[3:4]
					map2[curY][curX] = 1

				elif map2[curY+1][curX] == 37:
					curY+=1
					eventMessage("\nYou found a scalpel!\n")
					if len(heldInventory) <= 3:
						heldInventory.append("Scalpel")
					else:
						heldInventory.append("Scalpel")
						(heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[3:4]
					map2[curY][curX] = 1

				elif map2[curY+1][curX] == 38:
					curY+=1
					eventMessage("\nYou found some adrenaline!\n")
					if len(inventory) <= 3:
						inventory.append("Adrenaline")
					else:
						inventory.append("Adrenaline")
						(curHealth, curStam, inventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[0:3]
					map2[curY][curX] = 1

				elif map2[curY+1][curX] == 39:
					if "Canteen" in heldInventory:
						curY+=1
						eventMessage("You found a puddle of clean looking water and filled your canteen.")
						heldInventory.remove("Canteen")
						heldInventory.append("Full Canteen")
						map2[curY][curX] = 1
					else:
						eventMessage("\nTheres a puddle infront of you, you'd rather not get feet wet for no reason.\n")


				#chance encounters
				elif map2[curY+1][curX] == 41:
					curY+=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = giantSlugImpFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes1-=1

				elif map2[curY+1][curX] == 42:
					curY+=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = axeDemonSavageFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes2-=1


				elif map2[curY+1][curX] == 43:
					curY+=1
					encounter = random.randint(1,101)
					if encounter <= 60:
						(curHealth, curStam, curTokens, inventory) = viciousBatFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes3-=1

				elif map2[curY+1][curX] == 44:
					curY+=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						if foes4 == 15 and ("Stale bread") in inventory and ("Full Canteen" and "Salt rock") in heldInventory and (hasSword or disillusioned):
							eventMessage("lore")
							inventory.remove("Stale bread" and "Full Canteen" and "Salt rock")
							foes4 = 0
						else:
							(curHealth, curStam, curTokens, inventory) = starvedMenZombieFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
							foes4-=1

				elif map2[curY+1][curX] == 45:
					curY+=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = skeletonCrazedManFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes5-=1

				elif map2[curY+1][curX] == 46:
					curY+=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = smallGolemBruteFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes6-=1

				elif map2[curY+1][curX] == 47:
					curY+=1
					encounter = random.randint(1,101)
					if encounter <= 90:
						(curHealth, curStam, curTokens, inventory) = smallGolemBruteFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)

				#Poison
				elif map2[curY+1][curX] == 5:
					curY+=1
					if "Ventilator" not in heldInventory:
						curHealth = takeDamage((Stats["Health"]/8), Stats, curHealth)
						updateStatus(curHealth, curStam, curTokens)
						eventMessage("\nThe poison eats away at you. You took " + str(Stats["Health"]/8) + " damage.\nYour health is now " + str(curHealth) + ".\n")

				#Extreme encounter
				elif map2[curY+1][curX] == 90:
					curY+=1
					(curHealth, curStam, curTokens, inventory) = AdomaMap2Fight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
					map2[curY][curX] = 1

				#Warning
				elif  map2[curY+1][curX] == 100:
					curY+=1
					eventMessage("\nYou get a strong sense of danger ahead")

			
			#Moving Up

			elif buttonPushed.get() == "8":
				
				if curY == 1 or map2[curY-1][curX] == 0:
					eventMessage("\nCannot move up\n")
				
				elif map2[curY-1][curX] == 1:
					curY-=1

				#Main Encounter
				elif map2[curY-1][curX] == 2:
					if not disillusioned and not hasSword:
						curY-=1
						(curHealth, curStam, curTokens, inventory) = crazedScientistFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
					elif hasSword:
						eventMessage("\nYou approach an intelligent looking man working feverishly. As you get close he shouts 'Go away, I'm busy!'.\n")
					else:
						if "Scalpel" in heldInventory:
							eventMessage("\nYou approach a feverishly working man, 'Ooooo! That would be perfect!!, come give me that scalpel at once.' he blurts out as he reaches over and snatches the scalpel from your pouch before scurrying over closer to his shoddily crafted work desk\n")
							curY-=1
							map2[curY][curX] = 1
							map2[curY][curX-1] = 22
							inventory.remove("Scalpel")
						else:
							eventMessage("\nYou approach a feverishly working man, 'Wha- who the heck are you. I'm busy, if you aren't going to help go away!' he shouts\n")

				elif map2[curY-1][curX] == 21:
					curY-=1
					choice = input("\nYou see a pitfall in front of you, it looks like you could carefully let yourself down some ledges. \n\n8.) Drop yourself carefully down the opening\n2.) Come back later\n")
					if choice == "8":
						eventMessage("\nYou carefully let yourself down the first few ledges, suddenly a ledge snaps along the way and you drop down. You feel fine, however you won't be able to climb back up.\n")
						map3(Stats, curHealth, curStam, StamBar, curTokens, inventory, heldInventory, hasSword, disillusioned)
					elif choice == "2":
						curY+=1
						eventMessage("\nYou turn back from the pitfall.\n")
					else:
						choice = input("\nPlease input '8' or '2' only.\n")

				elif map2[curY-1][curX] == 20:
					curY-=1
					(curHealth, curStam, curTokens, inventory) = axeDemonSavageFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
					foes2-=1

				#Items
				
				elif map2[curY-1][curX] == 3:
					eventMessage("\nYou see what seems to be a grotesque mask made of the giant slugs face lying on the table. You could take it if you wanted to?\n 8.) take it\n 6.) Leave it behind\n")
					mask = input()
					if len(heldInventory) <= 3 and mask == "8":
						heldInventory.append("Ventilator")
						map2[curY][curX-1] = 0
					elif mask == "8":
						heldInventory.append("Ventilator")
						(heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[3:4]
						map2[curY][curX-1] = 0
				
				elif  map2[curY-1][curX] == 33:
					curY-=1
					eventMessage("\nYou found some oily water!\n")
					if len(inventory) <= 3:
						inventory.append("Oily water")
					else:
						inventory.append("Oily water")
						(curHealth, curStam, inventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[0:3]
					map2[curY][curX] = 1

				elif  map2[curY-1][curX] == 35:
					curY-=1
					eventMessage("\nYou found an empty canteen!\n")
					if len(heldInventory) <= 3:
						heldInventory.append("Canteen")
					else:
						heldInventory.append("Canteen")
						(heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[3:4]
					map2[curY][curX] = 1

				elif  map2[curY-1][curX] == 36:
					curY-=1
					eventMessage("\nYou found some stale bread!\n")
					if len(inventory) <= 3:
						inventory.append("Stale bread")
					else:
						inventory.append("Stale bread")
						(curHealth, curStam, inventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[0:3]
					map2[curY][curX] = 1

				#chance encounters
				elif map2[curY-1][curX] == 41:
					curY-=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = giantSlugImpFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes1-=1

				elif map2[curY-1][curX] == 42:
					curY-=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = axeDemonSavageFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes2-=1

				elif map2[curY-1][curX] == 43:
					curY-=1
					encounter = random.randint(1,101)
					if encounter <= 60:
						(curHealth, curStam, curTokens, inventory) = viciousBatFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes3-=1

				elif map2[curY-1][curX] == 44:
					curY-=1
					encounter = random.randint(1,101)
					if encounter <= 20:	
						(curHealth, curStam, curTokens, inventory) = starvedMenZombieFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes4-=1


				elif map2[curY-1][curX] == 45:
					curY-=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = skeletonCrazedManFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes5-=1

				elif map2[curY-1][curX] == 46:
					curY-=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = smallGolemBruteFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes6-=1

				elif map2[curY-1][curX] == 47:
					curY-=1
					encounter = random.randint(1,101)
					if encounter <= 90:
						(curHealth, curStam, curTokens, inventory) = smallGolemBruteFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)

				#Poison
				elif map2[curY-1][curX] == 5:
					curY-=1
					if "Ventilator" not in heldInventory:
						curHealth = takeDamage((Stats["Health"]/8), Stats, curHealth)
						updateStatus(curHealth, curStam, curTokens)
						eventMessage("\nThe poison eats away at you. You took " + str(Stats["Health"]/8) + " damage.\nYour health is now " + str(curHealth) + ".\n")

				#Warning
				elif  map2[curY-1][curX] == 100:
					curY-=1
					eventMessage("\nYou get a strong sense of danger ahead")


			#Moving Right
			elif buttonPushed.get() == "6":
				
				if curX == lastCol-1 or map2[curY][curX+1] == 0:
					eventMessage("\nCannot move right.")
				
				elif map2[curY][curX+1] == 1:
					curX+=1

				#Main Encounter
				elif map2[curY][curX+1] == 21:
					curX+=1
					choice = input("\nYou see a pitfall in front of you, it looks like you could carefully let yourself down some ledges. \n\n6.) Drop yourself carefully down the opening\n4.) Come back later\n")
					if choice == "6":
						eventMessage("\nYou carefully let yourself down the first few ledges, suddenly a ledge snaps along the way and you drop down. You feel fine, however you won't be able to climb back up.\n")
						map3(Stats, curHealth, curStam, StamBar, curTokens, inventory, heldInventory, hasSword, disillusioned)
					elif choice == "4":
						curY+=1
						eventMessage("\nYou turn back from the pitfall.\n")
					else:
						choice = input("\nPlease input '6' or '4' only.\n")

				elif map2[curY][curX+1] == 20:
					curX+=1
					(curHealth, curStam, curTokens, inventory) = axeDemonSavageFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
					foes2-=1

				#Items
				elif map2[curY][curX+1] == 38:
					curX+=1
					eventMessage("\nYou found some adrenaline!\n")
					if len(inventory) <= 3:
						inventory.append("Adrenaline")
					else:
						inventory.append("Adrenaline")
						(curHealth, curStam, inventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[0:3]
					map2[curY][curX] = 1

				#chance encounters
				elif map2[curY][curX+1] == 41:
					curX+=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = giantSlugImpFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes1-=1

				elif map2[curY][curX+1] == 42:
					curX+=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = axeDemonSavageFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes2-=1


				elif map2[curY][curX+1] == 43:
					curX+=1
					encounter = random.randint(1,101)
					if encounter <= 60:
						(curHealth, curStam, curTokens, inventory) = viciousBatFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes3-=1

				elif map2[curY][curX+1] == 44:
					curX+=1
					encounter = random.randint(1,101)
					if encounter <= 20:	
						(curHealth, curStam, curTokens, inventory) = starvedMenZombieFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes4-=1

				elif map2[curY][curX+1] == 45:
					curX+=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = skeletonCrazedManFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes5-=1

				elif map2[curY][curX+1] == 46:
					curX+=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = smallGolemBruteFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes6-=1

				elif map2[curY][curX+1] == 47:
					curX+=1
					encounter = random.randint(1,101)
					if encounter <= 90:
						(curHealth, curStam, curTokens, inventory) = smallGolemBruteFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)

				#Poison
				elif map2[curY][curX+1] == 5:
					curX+=1
					if "Ventilator" not in heldInventory:
						curHealth = takeDamage((Stats["Health"]/8), Stats, curHealth)
						updateStatus(curHealth, curStam, curTokens)
						eventMessage("\nThe poison eats away at you. You took " + str(Stats["Health"]/8) + " damage.\nYour health is now " + str(curHealth) + ".\n")

				#Warning
				elif  map2[curY][curX+1] == 100:
					curX+=1
					eventMessage("\nYou get a strong sense of danger ahead")		

			#Moving Left
			elif buttonPushed.get() == "4":

				if curX == 1 or map2[curY][curX-1] == 0:
					eventMessage("\nCannot move left")

				elif map2[curY][curX-1] == 1:
					curX-=1

				#Main Encounter
				elif map2[curY][curX-1] == 2:
					if not disillusioned and not hasSword:
						curX-=1
						(curHealth, curStam, curTokens, inventory) = crazedScientistFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						map2[curY][curX] = 1
					elif hasSword:
						eventMessage("\nYou approach an intelligent looking man working feverishly. As you get close he shouts 'Go away, I'm busy!'.\n")
					else:
						if "Scalpel" in heldInventory:
							eventMessage("\nYou approach a feverishly working man, 'Ooooo! That would be perfect!!, come give me that scalpel at once.' he blurts out as he reaches over and snatches the scalpel from your pouch before scurrying over closer to his shoddily crafted work desk\n")
							curX-=1
							map2[curY][curX] = 1
							map2[curY][curX-1] = 22
							inventory.remove("Scalpel")
						else:
							eventMessage("\nYou approach a feverishly working man, 'Wha- who the heck are you. I'm busy, if you aren't going to help go away!' he shouts\n")


				elif map2[curY][curX-1] == 22:
					eventMessage("\n'Don't bother me!' the scientist shouts\n")
					

				#Items
				elif map2[curY][curX-1] == 3:
					if disillusioned:
						eventMessage("\n'I noticed these giant bugs don't seem to mind the poison clouds around here and I've disected them and made these nice little masks out of the part of their body that filters out the posion. You shouuuld be able to put it over your mouth and breath fine in the posion!\n")
						if len(heldInventory) <= 3:
							heldInventory.append("Ventilator")
							map2[curY][curX-1] = 9
						else:
							heldInventory.append("Ventilator")
							(heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[3:4]
							map2[curY][curX-1] = 9
					else:
						eventMessage("\nYou see what seems to be a grotesque mask made of the giant slugs face lying on the table. You could take it if you wanted to?\n8.) to take it\n6.) to leave it\n")
						mask = input()
						if len(heldInventory) <= 3 and mask == "8":
							heldInventory.append("Ventilator")
							map2[curY][curX-1] = 0
						elif mask == "8":
							heldInventory.append("Ventilator")
							(heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[3:4]
							map2[curY][curX-1] = 0

				elif map2[curY][curX-1] == 9:
					eventMessage("\n'well I hardly think you'll need more than one.' the scientist says\n")

				elif map2[curY][curX-1] == 30:
					curX-=1
					eventMessage("\nYou found a silver idol!\n")
					if len(heldInventory) <= 3:
						heldInventory.append("Silver Idol")
					else:
						heldInventory.append("Silver Idol")
						(heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[3:4]
					map2[curY][curX] = 1

				elif map2[curY][curX-1] == 33:
					curX-=1
					eventMessage("\nYou found some oily water!\n")
					if len(inventory) <= 3:
						inventory.append("Oily water")
					else:
						inventory.append("Oily water")
						(curHealth, curStam, inventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[0:3]
					map2[curY][curX] = 1

				elif map2[curY][curX-1] == 34:
					curX-=1
					eventMessage("\nYou found a salt rock!\n")
					if len(heldInventory) <= 3:
						heldInventory.append("Salt rock")
					else:
						heldInventory.append("Salt rock")
						(heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[3:4]
					map2[curY][curX] = 1

				elif map2[curY][curX-1] == 35:
					curX-=1
					eventMessage("\nYou found a canteen!\n")
					if len(heldInventory) <= 3:
						heldInventory.append("Canteen")
					else:
						heldInventory.append("Canteen")
						(heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[3:4]
					map2[curY][curX] = 1

				elif map2[curY][curX-1] == 36:
					curX-=1
					eventMessage("\nYou found some stale bread!\n")
					if len(inventory) <= 3:
						inventory.append("Stale bread")
					else:
						inventory.append("Stale bread")
						(curHealth, curStam, inventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[0:3]
					map2[curY][curX] = 1

				elif map2[curY][curX-1] == 37:
					curX-=1
					eventMessage("\nYou found a scalpel!\n")
					if len(heldInventory) <= 3:
						heldInventory.append("Scalpel")
					else:
						heldInventory.append("Scalpel")
						(heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory, "", [], 0, 0, 0)[3:4]
					map2[curY][curX] = 1

				#chance encounters
				elif map2[curY][curX-1] == 41:
					curX-=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = giantSlugImpFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes1-=1

				elif map2[curY][curX-1] == 42:
					curX-=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = axeDemonSavageFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes2-=1

				elif map2[curY][curX-1] == 43:
					curX-=1
					encounter = random.randint(1,101)
					if encounter <= 60:
						(curHealth, curStam, curTokens, inventory) = viciousBatFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes3-=1

				elif map2[curY][curX-1] == 44:
					curX-=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = starvedMenZombieFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes4-=1

				elif map2[curY][curX-1] == 45:
					curX-=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = skeletonCrazedManFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes5-=1

				elif map2[curY][curX-1] == 46:
					curX-=1
					encounter = random.randint(1,101)
					if encounter <= 20:
						(curHealth, curStam, curTokens, inventory) = smallGolemBruteFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						foes6-=1

				elif map2[curY][curX-1] == 47:
					curX-=1
					encounter = random.randint(1,101)
					if encounter <= 90:
						(curHealth, curStam, curTokens, inventory) = smallGolemBruteFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)

				#Poison
				elif map2[curY][curX-1] == 5:
					curX-=1
					if "Ventilator" not in heldInventory:
						curHealth = takeDamage((Stats["Health"]/8), Stats, curHealth)
						updateStatus(curHealth, curStam, curTokens)
						eventMessage("\nThe poison eats away at you. You took " + str(Stats["Health"]/8) + " damage.\nYour health is now " + str(curHealth) + ".\n")
			
				#Warning
				elif  map2[curY][curX-1] == 100:
					curX-=1
					eventMessage("\nYou get a strong sense of danger ahead")

			#Resting
			elif buttonPushed.get() == "5":
				if globalConditionals['hasCharm'] and map2[curY][curX] == 1:
					if charmUsed == 0:
						(curHealth, curStam, curTokens) = restRecovery(curHealth, curStam, curTokens)
						charmUsed+=1
					else:
						encounter = random.randint(0,101)
						if encounter <= 20:
							(curHealth, curStam, curTokens, inventory) = skeletonCrazedManFight(Stats, curHealth, curStam, StamBar, curTokens, inventory, hasSword, disillusioned)
						else:
							(curHealth, curStam, curTokens) = restRecovery(curHealth, curStam, StamBar)
				elif globalConditionals['hasCharm']:
					eventMessage("\nYou can't rest here.\n")
				else:
					eventMessage("\nPlease input '8' '6' '4' or '2'\n")

		eventMessage("\nYou cough and weeze in the posion clouds. Everything goes hazy.\n")
		gameOver()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------First Map------------------------------------------------------------------------------------------------------------------------------
#
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	
	def firstMap():

		def clearingIllusions(curHealth, curStam, curTokens, inventory, heldInventory):
		
			disillusioned = False
			loop = 0

			eventMessage("\n\nYou quickly shuffle forward to get distance from the burrow fearful there may be more creatures yet inside. Your body rings out in agonizing pain, missing chunks of flesh and losing blood fast. Even still you progress, ahead you see a blinding light amidst the darkness. When you cross into the light and your vision adjusts you a see a spacious circular room with the narrow pathway you came from behind you and another similar continuation on the other side of the room. The right side of the floor seems to be all water and lining the wall rather than cavern walls of rock is a glistening polished white marble with an occasional lit torch along it. In front of the center of the wall amidst the bath stands a life sized marble statue of young maiden shedding a single tear. As you lock eyes with the statue you feel a strong urge to get into the water and the intensity of the pain you feel from each of your wounds increases immensely more and more each second.")
			while loop == 0:
				takeInput("\nPeel away from the statues gaze and move on in the caverns or accept its call and join it in the waters?\n\n8.) Peel away\n6.) Accept\n\n")
				if buttonPushed.get() == "6":
					loop+=1
					eventMessage("\nAs you step into the water you can see the single tear on the maiden change form from stone to liquid and drip into the water. The water begins to feel warmer and you notice a slight shimmer along the surface. Suddenly the water bursts into a glaring golden color and rises up around you, encapsualting you in it. At first you struggle against the water in fear of drowning but as you flail around you see that your wounds are closing up and as though you've never endured a hardship in your life. You give in to the comforting aura and let out a gasp to find you can still breathe.\n")
					(curHealth, curStam, curTokens) = maidenEncounter(curHealth, curStam, curTokens)
					globalConditionals["acceptedMaiden"] = True
					eventMessage("\nThe shimmering gold color settles and slowly fades in the water around you and soon it all falls to the pool again beneath you. Suddenly two torches flare up on either side of the entrance to the narrow passageway across from where you entered this opening. You glance back to the statue of the maiden and see that it has changed and she is smiling sweetly now instead of crying, and holds an arm up pointing to the passageway. You take hold of the meaning and venture forth into the cavern again.\n")
					return(curHealth, curStam, curTokens, disillusioned)
				elif buttonPushed.get() == "8":
					loop+=1
					eventMessage("\nYou peel your eyes away from the maidens and step back, suddenly you feel a horrendous stinging pain all across your body and you're certain it isn't from your existing wounds. You fumble in agony and lose your footing until you collapse against the wall Opposite the pool of water, when you open your eyes and glance back at the pool the maiden statue appears different. She now has an arm raised pointing at you, and the other into the waters with a stern frown and sharp eyes.\n")
					curHealth = takeDamage(2, Stats, curHealth)
					updateStatus(curHealth, curStam, curTokens)
					eventMessage("\nThe stinging pain running along your skin takes its toll, your health drops to "+str(curHealth)+"\n")
					if curHealth < 1:
						eventMessage("\nYour body goes limp and your vision fades away. The lashing pain you suddenly felt untop added to your existing wounds proved fatal.\n")
						gameOver()
					
					while loop == 1:
						takeInput("Do you accept the demand or ignore it?\n\n8.) Ignore\n6.) Accept\n\n")
						if buttonPushed.get() == "6":
							eventMessage("\nFearfully you crawl to the waters, roll yourself in, and sink down. You feel your wounds and pain fading from your body, the holes of flesh bitten off of you sealing up. Lifelessly you lay at the bottom of the pool, but as the last of your wounds seals itself and you still lie there the water itself surges and throws you beside the pools edge. After a fit of coughing for a moment you look up and see that again the statue has changed and now stands hands down and cupped together, face directed at the passage way youve yet ventured in with a beaming smile. Torches on either side of the entrance flare up and you collect yourself and venture into it hesitantly taking glances at the statue behind you.\n")
							loop+=1
							(curHealth, curStam, curTokens) = maidenEncounter(curHealth, curStam, curTokens)
							globalConditionals["acceptedMaiden"] = True
							return(curHealth, curStam, curTokens, disillusioned)
						elif buttonPushed.get() == "8":
							loop+=1
							eventMessage("\nThe stinging pain you felt before intensifies to what can only be described as the most horrendously agonizing sensation you've ever felt in your life. Were you to lacerate your own body along every inch of it, douse yourself with a batch of a citrusy liquid, and then light yourself ablaze, even still it could not compare the pain ringing out across your entire body. You freeze in place, the pain so great your brain entirely shut down to protect you from going insane. While your mind is blacked out from reality your consciousness drifts into a vision like a sort of dream. You see a family around a table, amongst them is an individual that resembles yourself, perhaps more groomed in appearance with a little more fat on your build and slightly less aged but it's certainly the same face you saw looking back in the pond before. The whole family seems to be enjoying themself bantering and sharing a moment together yet everytime theres a lull you can read an expression of teror across their faces. You hear a knocking at the door a few meters from the table and see everyones face freeze up besides your own look alike. They push their seat away from the table, stand, and walk to another room within the small home before returning with a sword tucked into a scabbard and held down into it with chains. Before they open the door they pull on the handle as if to draw the blade and although the chains prevent that it does partially click out of the scabbard and reveal a shimmering silver blade that resonates out a calming ringing sound. They stare for a moment then click it back in and opens the front door, through which you view a gathering of men with black cloaks, silver garnished, with a bright silver mask. The apparent leader of the group stands ahead of the others, adorned with even more silver decorations along their cloak and mask, and gestures your double to join them. After they do, the leader extends his arms out infront of himself and peers at the blade they hold. They clench their fist and grimace, but still lay the blade across the leaders arms, after which the others form a circle around them and start walking away and the leader peers in on the family for a while before shutting the door. The family all hurriedly clusters together and seem to be grieving in eachothers arms... As you wonder why?, what happened to your lookalike?, who were those cloaked people? and so many more questions you start to come back into reality and scream out at the pain across your body. It's died down and is no longer even a fraction of what it had been but still the pain is agonizing and your snaps out of the dreamlike sight you had viewed before and the memory of it becomes fuzzy. You recollect yourself mentally and stand shakily, before lies the pond full of black waters with the statue showing an incredibly angered face directed at you. To your right is the passage you came from, and as you peer into its darkness you hear the same faint ringing you heard before. To your left the passageway you've yet to venture into, silent and dark as the abyss.\n")
							curHealth = takeDamage(4, Stats, curHealth)
							updateStatus(curHealth, curStam, curTokens)
							eventMessage("\nThe agonizing pain ringing across your body finally comes to a stop but it's certainly left its mark, your health falls to "+str(curHealth)+"\n")
							if curHealth < 1:
								eventMessage("\nYour vision starts to go fuzzy and fade out and your body goes limp. For a moment you think you are going to see more of this dreamscape you peered into before, however you quickly come to terms with the fact that this is not the case but rather your life itself is coming to an end.\n")
								gameOver()
							disillusioned = True
							
							while loop == 2:
								takeInput("Do you finally embrace the waters, or leave it?\n\n8.) Embrace\n6.) leave\n\n")
								if buttonPushed.get() == "8":
									loop+=1
									eventMessage("\nYou wade into the black waters and watch as a shadowy mist wraps around the statue and change its appearance to a beaming smile and holding it's hands up and together like in prayer. The water wraps around your body and all of your wounds and your fatigue are cured, you can see where your wounds had been is a flowing black fluid joining and mixing into the lighter black water. When you're fully recovered the water falls back into the pool splashing around you and again you see a shadowy mist wrap around the statue and change it to be looking fondly at the passageway you haven't traversed through and pointing an arm to it.\n")
									(curHealth, curStam, curTokens) = maidenEncounter(curHealth, curStam, StamBar)
									globalConditionals["acceptedMaiden"] = True
									return(curHealth, curStam, curTokens, disillusioned)
								elif buttonPushed.get() == "6":
									loop+=1
									eventMessage("\nCurious about the ringing noise you've been hearing you consider heading back to where you came from and following the noise.\n\n")
									return(curHealth, curStam, curTokens, disillusioned)



		def clearingNoIllusions(curHealth, curStam, curTokens, inventory, heldInventory):

			eventMessage("\nYou venture into the passage the other direction. Along the way you see a burrow in the cavern wall and a family of immense rats with smooth sleek coats of fur. As intimidating as these large creatures may be they seem friendly enough and they let you pass freely. Further beyond you come into a spacious clearing between the passage you came from and another ahead of you. On the right half of the cave wall is a pool lined with marble, filled with black eerie waters, and at the far end of it is a shadowy figure shaped sort of like a woman with horns. As you notice this creature you close your grip around your sword tighter and stare, and the shadow breaks the stand still in the room with an angry shriek and the water around her stirs up.\n")

			topCombatSentence = "\nThe waters whirl in unnatural patterns and the shadow cackles maniacally, what will you do?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
			fatiguedSentence = "\nThe shadowy figure envelopes its lower half in the murky waters and hisses.\n"
			endCombatSentence = "\nYou defended yourself from the Imps attack\n"
			#status for Shadow
			OppStats = {
			"Atk": 12,
			"Def": 7,
			"Stam": 4.5,
			"Health": 60,
			}

			(curHealth, curStam, curTokens, inventory) = basicCombat(curHealth, curStam, curTokens, inventory, heldInventory, 8, OppStats, 8, topCombatSentence, fatiguedSentence, 35, 0)		

			if curHealth == 0:
				eventMessage("\nThe shadow cackles mockingly while dark bubbles rise from the pool and pop around her. Your vision gets hazy and you collapse.\n")
				gameOver()
			else:
				curStam = fatigueStatus(12, Stats, curStam)
				eventMessage("\nThe Shadow grabs it's horns firmly and pulls on them while screeching. All of the water rises from the floor, a large amount forming a base around the shadows legs, and the rest hovering in the air formed into something like 10 seperate giant tails. The shadow silences its screech and releases its hands down by its side and stares blankly at you for a moment.... \n\nSuddenly it raises its arms up extended towards you and its fingers start to snap out of their human like shape and extend, and you notice the tails of water move corresponding to the way it moves it's fingers. You brace yourself unsure what to do and then 4 of the tails slam into you far too fast for you to react. The tails hit you in an x pattern and form a ball around you suffocating you, in a mad flail to free yourself you slash at the waters and the sword glows bright, the water around you loses its rigid form and splashes down onto the floor dropping you onto your back.\n\n")
				eventMessage("Your struggle wore you out, your stamina is now "+str(curStam))
				updateStatus(curHealth, curStam, curTokens)

				while curHealth > 0:
					takeInput("\n\nThe tails that struck you are very slowly being pulled back into the water around the shadows legs, do you want to make a dash to try and slice away some or try to prepare to intercept an attack?\n\n8.) Dash forward\n6.) Prepare to intercept\n\n")

					if buttonPushed.get() == "6":
						eventMessage("\nyou stand firm and when a single tail is propelled towards you, you run the glowing blade through it and again watch it lose form and splash down around you.\n")
						loop = 0
						while loop == 0:
							takeInput("\nYour plan seems to be working, continue to intercept incoming tails or go on the offensive?\n\n8.) Continue intercepting\n6.) Go on the offense\n")
							if buttonPushed.get() == "8":
								loop+=1
								curHealth = takeDamage(7, Stats, curHealth)
								eventMessage("\nYou prepare to repeat your same action and wait for a tail to launch after you. After a short moment the next tail comes flying towards you and you time your motion and start to swing. When the tail and sword are about to collide the tail suddenly buckles up to avoid the blade and two more tails slam into your sides. You cut your way out again but the force the tails slammed into you with was much higher this time and severely injured you.\n\nyou took 6 damage, your health dropped to "+str(curHealth)+"\n")
								updateStatus(curHealth, curStam, curTokens)
								if curHealth == 0:
									eventMessage("\nThe blast from the tails likely broke some ribs and caused internal bleeding. You struggle to hold yourself up but inevitably collapse. The shadow cackles softly and the tails wrap around your legs and drag you into the murky waters around its legs. Everything goes black.\n")
									gameOver()
								else:
									while loop == 1:
										takeInput("\nThe shadows face distorts rapidly while making a constant spastic clicking noise. With only 4 tails left it seems to be getting antsy, do you want to prepare to intercept again or charge?\n\n8.) Prepare to intercept\n6.) Charge\n\n")
										if buttonPushed.get() == "8":
											loop+=1
											curHealth = takeDamage(8, Stats, curHealth)
											eventMessage("\nThe shadow whips its head forward and screeches, slamming the remaining 4 tails directly into you. You slash you're blade through the oncoming torrent, and find you're unable to nullify all four tails momentum at once and take a heavy blow. however, as you tumble along the ground you see the tails all collapse down.\n\nYou took another 8 damage, your health drOpped to "+str(curHealth)+"\n")										
											if curHealth == 0:
												eventMessage("\nYou see that you were able to knock out the last 4 tails, and the shadow is breaking down, however you can no longer move your body and a raging pain stings along your chest. You taste your own blood filling your mouth, and resign yourself to your fate.\n")
												gameOver()
											else:
												eventMessage("\nThe shadow makes a sad chirping noise, then loses form and becomes nothing more than a dark mist. It slowly spreads wide infront of you, and then in an instant picks all of the waters drOpped from the tails off the ground and back into itself, and bolts away like a massive arrow of water, down into the passageway you've yet to venture into. Holding your blade forth anticipating its return, you stand stoicly, yet after a long pause you decide it's likely not coming back and decide to rest and give your body a chance to recover. You slouch down against the cave wall in the clearing and take a breath. Suddenly, your blade glistens white again and cloaks you in it's aura.\n\nYou gained 100 Exp!")
												Stats["Exp"] += 100
												(curHealth, curStam, curTokens) = swordCheckLvl(curHealth, curStam, curTokens)
												(curHealth, curStam, curTokens) = restRecovery(curHealth, curStam, curTokens)
												eventMessage("\nYou pick yourself up and head into the caverns ahead of you, blade at the ready.\n")
												return(curHealth, curStam, curTokens, inventory)
										elif buttonPushed.get() == "6":
											if curStam >= 20:
												loop+=1
												curStam = fatigueStatus(20, Stats, curStam)
												eventMessage("\nYou charge at a dead seventMessage and land the blow into the chest of the shadow itself, it screams and implodes like an over filled ballon.\n You hold firm and run the blade through the shadow to the hilt. To your surprise the white aura the sword let off earlier surrounds the shadow and then chages sensation from its calm serene feeling to one of a divine, awe inspiring, being casting judgement down on a child that lost its's way. The aura burned angrily and the shadow bellowed in screams, not like the screeches before but truly screams of horror and fear. The shadow slowly ceased to be and as it burned away and shriveled the aura shrank around it until it only wrapped around the blade again and the shadow was entirely gone. The waters collapsed into the pool once more and a black mist rose from it and into the blade, transforming to the white glow of the blade itself, and the pool beneath turned in color to be normal everyday waters.\n\nYou've gained 250 Exp!!")
												globalConditionals["firstMaidenDead"] = True
												Stats["Exp"] += 250
												(curHealth, curStam, curTokens) = swordCheckLvl(curHealth, curStam, curTokens)
												eventMessage( "\nYour heart pounding, body shaking from both exhaustion and internal damage, you collapse face first into the pool of now cleansed waters. You think to yourself for a moment, 'am I going to die here like this? after everything!?' face under water unable to move your body. As you run out of breath, you nearly let the blade slip from your hand and drift away, but before it does the same white aura envelopes you and you feel it mending your body.\n")
												(curHealth, curStam, curTokens) = restRecovery(curHealth, curStam, curTokens)
												eventMessage("\nAble to move your limbs once more you lift yourself out from the pool of water and gasp for air. after a moment to catch your breath you glance at the passage you've yet to travel down and the blade at your side intensifies its ringing sound. You feel strangely indebted to this sword and accept its desire. You pick yourself up and start to venture down the passageway.\n")
												return(curHealth, curStam, curTokens, inventory)
											elif curStam >= 12:
												loop+=1
												eventMessage("\nYou pause for just a moment and as a tail slams forth with great speed, you run under it and charge at the shadow. Before you can reach all the way to it the other tails curl in front of the shadow to protect it. You slash through all 3 successfully, but immediately get slammed in the back by the last tail. Having the wind knocked out of you, you struggle to get back to your feet and the shadow cackles and twirls its last tail over your head.\n")
												curStam = fatigueStatus(12, Stats, curStam)
												curHealth = takeDamage(6, Stats, curHealth)
												eventMessage("\nYou took 6 damage, and lost 12 stamina. Your health is now: "+str(curHealth)+" and your stamina is now: "+str(curStam)+"\n")
												if curHealth == 0:
													eventMessage("\nYour consciousness fades out as you're continuosly wailed on by the last tail, the force rippling waves in the shallow pool of water around you.\n")
													gameOver()
												else:
													takeInput("You know you need to move before that tail hanging over head strikes again, and you know you're in a vulnerable position, but you struggle to move at all let alone quickly. You quickly run some ideas through your mind and realize you have limited options. You could try rolling over and swinging your blade along the way in a wide arc to try and take out the last tail, you could try and get a footing and quickly spring forward to stab into the shadow, or you could try to quickly spring backwards and prepare to defend yourself, what will you do?\n\n8.) Roll\n6.) Stab\n4.) Spring backwards\n\n")
													while loop == 2:
														if buttonPushed.get() == "8":
															loop+=1
															eventMessage("\nYou tuck the blade in against your side, and slowly get your arm into a stiff straight position. Then, swiftly and simultaneously you push your arm out perpendicular to your body and roll letting your body weight drag your arm across with you in an arc. You successfully take out the last tail, but now lay flat on your back, sword at a full arms distance from your abdomen, with the shadow looming over you a mere foot or so away. You should be in mortal danger, yet the shadow has lost it's own composure and is stumbling back whilst screeching. Suddenly it reaccumulates all the waters fallen from the tails into itself, losing its humanoid form, and then bolts away as a mass of black liquid. You take the Opportunity to stand and brace for it's return, but several moments pass with no further action. You cautiously decide to lower your guard and take a chance to rest.\n")
															eventMessage("\n\nYou gained 100 exp!")
															Stats["Exp"]+=100
															(curHealth, curStam, curTokens) = swordCheckLvl(curHealth, curStam, curTokens)
															(curHealth, curStam, curTokens) = restRecovery(curHealth, curStam, curTokens)
															return(curHealth, curStam, curTokens, inventory)
														elif buttonPushed.get() == "6":
															loop+=1
															eventMessage("\nYou take your time to position your footing and joints to make one swift push forward and stab into the shadow without alerting the shadow itself. Your attack is a success... sort of. You were able to get up and lunge forward without being struck in return, however the watery base at the shadows legs stOpped your blades momentum only a few inches into it. The blade starts to shimmer like in the tails before, and the remaining tails collapse around you, but you're blade is still stuck in the waters around the shadow and those waters aren't collapsin like the tails. You lock eyes with the shadow for a brief moment, before it screeches in your face and slams you across the room.\n")
															curHealth = takeDamage(8, Stats, curHealth)
															if curHealth < 1:
																eventMessage("\nThe last forceful shove from the shadow was the straw that broke the camels back for you. Your body is too broken down to will forward anymore. Your life fades away...\n")
																gameOver()
															else:
																eventMessage("Disoriented and nearing death you scramble to get to your feet and collect up your sword, but you see that the shadow bolting dwon the chamber you've yet to traverse. You take a moment to collect your things and slouch against the wall for awhile. After a long enough stretch of time to feel sustainable you get up move towards the next passageway\n")
																eventMessage("\n\nYou gained 100 exp!")
																Stats["Exp"]+=100
																(curHealth, curStam, curTokens) = swordCheckLvl(curHealth, curStam, curTokens)
																(curHealth, curStam, curTokens) = restRecovery(curHealth, curStam, curTokens)
																return(curHealth, curStam, curTokens, inventory)
														elif buttonPushed.get() == "4":
															loop+=1
															eventMessage("\nYou try to place your footing down, and push with your arms to spring up swiftly to a stand and then backpedal away, and succeed. However, just as you get up and move to get away the tails looming over you start to pummel down on you with no ability to defend yourself. They slam into you relentlessly until suddenly the shadows face is over your own and its claws rips into your face.\n")
															curHealth = 0
															gameOver()
							elif buttonPushed.get() == "6":
								loop+=1
								#go on the offense, 5 tails
								eventMessage("\nYou recognize that the shadow is adapting to your strategy and think that perhaps you need to change it up yourself. You feign a full on charge and then stop in place swiftly pivoting on your right foot to slash around you with your sword, catching 2 tails intended to strike you from behind. The tails splash down and the Shadow screeches, and flails the last 3 tails around.wildly around itself.\n")
								takeInput("\nDo you want to push the momentum or change it up and try something new again?\n8.) Push the momentum\n6.) Try something new again\n\n")
								while loop < 2:
									if buttonPushed.get() == "8":
										loop+=1
										eventMessage("\nYou continue your offensive push, and the shadow launches 2 tails at you. Before they get in range to slash at they slow significantly, swell up at the tips, and then slam together to capture you in their water. You're able to use the sword to instantly nullify the waters like before, but as you're freed from the waters grip the last tail slams into your skull with great force.\n")
										curHealth = takeDamage(10, Stats, curHealth)
										if curHealth < 1:
											gameOver()
										else:
											eventMessage("\nYou took 10 damage, your health is now "+str(curHealth)+"\n")
											eventMessage("\n\nimmediately as you hit the ground the tail flails around wildly and slams into your sprawled out body again.\n")
											curHealth = takeDamage(6, Stats, curHealth)
											if curHealth < 1:
												eventMessage("The follow up attack from the last tail proved to be too much for you, and you slowly lose consciousness...")
												gameOver()
											else:
												eventMessage("\nYou lost 6 more health, and your health is now "+str(curHealth)+"\n")
												eventMessage("\nAs the tail goes to strike at you again you barely manage to lift up your sword and burst the tail before it crushes you. The shadow having lost all of its tails shreeks horrifically before transforming into a dark mist and bolting down the passageway you haven't yet traversed.\n")
												Stats["Exp"]+=100
												(curHealth, curStam, curTokens) = swordCheckLvl(curHealth, curStam, curTokens)
												(curHealth, curStam, curTokens) = restRecovery(curHealth, curStam, curTokens)
												return(curHealth, curStam, curTokens, inventory)
									elif buttonPushed.get() == "6":
										loop+=1
										eventMessage("\nTrying to think quick what you haven't done yet, you come up with an idea to bait the tails away from the shadow and then javelin tossing the sword into the shadow. You charge forward like before, stop and turn away like before, and as you hear the watery tails surging towards you, you grip the hilt with a c-grip and lock in your elbow. You turn and instantly hurl the blade with an upward arc towards the shadow. The shadow cackles and surges the tails at you knowing you've just tossed away your only means of defending yourself. You recognize that perhaps that wasn't the best idea you've ever had and close your eyes bracing for impact......\n\n but instead you open your ears to the sound of the shadow angrily screeching. the blade landed into the murky waters wrapped around the shadows legs, and all the remaining tails seem to have fallen down. The shadow screeches and jumps out of the water, near instantly gets infront of you and slams you across the room before vanishing through the passageway you've yet to traverse\n")
										Stats["Exp"]+=100
										(curHealth, curStam, curTokens) = swordCheckLvl(curHealth, curStam, curTokens)
										(curHealth, curStam, curTokens) = restRecovery(curHealth, curStam, curTokens)
										return(curHealth, curStam, curTokens, inventory)
					elif buttonPushed.get() == "8":
						#dash forward, 6 tails
						eventMessage("\nYou dash forward at the shadow and it slams all 6 remaining tails into you one at a time in quick succession. You were able to swipe your blade through the first two and the waters drOpped to the floor, but the reamining four slammed you down.\n")
						#4 tails left
						curHealth = takeDamage(6, Stats, curHealth)
						if curHealth == 0:
							eventMessage("\ntails whirling around overhead, you lie on your back and slowly fade out of consciousness.\n")
							gameOver()
						else:
							eventMessage("\nYou took 6 damage, you have "+str(curHealth)+" health left.\n")
							loop = 0
							eventMessage("\nYou get up off the ground, and square up again. Do you want to try dashing in again or play it safer?\n8.) Dash again\n6.) Play it safe\n\n")
							while loop == 0:
								if buttonPushed.get() == "8":
									loop+=1
									eventMessage("\nYou start to charge forth again and the scene starts to play out the same as before, however you're prepared this time and there are fewer tails to fight through. You succeed, barely, in knocking away all 4 tails, but while you're stumbling and off balance the shadow changes chape into a dark mist and bolts down the passageway you've yet to travel down with a fading shreek\n\n")
									eventMessage("\n\nYou gained 100 exp!")
									Stats["Exp"]+=100
									(curHealth, curStam, curTokens) = swordCheckLvl(curHealth, curStam, curTokens)
									(curHealth, curStam, curTokens) = restRecovery(curHealth, curStam, curTokens)
									return(curHealth, curStam, curTokens, inventory)
								elif buttonPushed.get() == "6":
									loop+=1
									eventMessage("\nYou set yourself in a firm stance and wait for the shadow to make the next move. In time the shadow grows impatient and starts creeping the tails along the floor like snakes around you. The tip of the tails rise up from the ground and feign launching at you, over time starting to unnerve you and get you off your footing. Eventually one of the tails commits to the attack while your watching another tail and knocks you down. While your down all 4 tails simultaneously start to slam into you repeatedly\n")
									curHealth = takeDamage(10, Stats, curHealth)
									if curHealth == 0:
										eventMessage("\nThe tails pound at you until you're body is unrecognizable as a human corpse.\n")
										gameOver()
									else:
										eventMessage("\nYour brain starts to shut out the repetitive pain and you collect yourself enough to tighten your grip on the hilt of your blade and suddenly turn and slash down all 4 tails at once. The shadow screeches and turns into a dark mist before vanishing down the passageway you haven't traveled through yet.\n")
										eventMessage("\n\nYou gained 100 exp!")
										Stats["Exp"]+=100
										(curHealth, curStam, curTokens) = swordCheckLvl(curHealth, curStam, curTokens)
										(curHealth, curStam, curTokens) = restRecovery(curHealth, curStam, curTokens)
										return(curHealth, curStam, curTokens, inventory)
		
			return(curHealth, curStam, curTokens, inventory)	

		def ratFight(curHealth, curStam, curTokens, inventory, heldInventory):
			
			eventMessage("\n\nAs you walk along the passageway you notice a large hole near the ground ahead on your right side. You cautiously approach and peer in but can't see anything but darkness. You begin to walk along your path again, but short after feel a sudden chill. Nervously you peer slowly over your shoulder and spot a shadow a couple feet long, and it begins to snarl back at you. As it approaches to strike you get a more clear picture, it is an immense rat with tufts of fur missing and jagged teeth. In this cavern you don't think you'll be able to outrun it and fearfully prepare to fight for your life.")

			topCombatSentence = "The rat is gnarling viciously, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
			fatiguedSentence = "\nThe rat is busy panting and doesn't attack\n"
			OppStats = {
			"Atk": 6,
			"Def": 2,
			"Stam": 1.5,
			"Health": 20,
			}

			(curHealth, curStam, curTokens, inventory) = basicCombat(curHealth, curStam, curTokens, inventory, heldInventory, 6, OppStats, 6, topCombatSentence, fatiguedSentence, 0, 0)		

			if curHealth == 0:
				eventMessage("\n\nYou feel the warmth of your own blood leaving your insides and running across your flesh. You come to terms with the fact that you died not knowing who you are or how you got to this cave, food for a feral rat creature.\n\nGAME OVER")
				gameOver()
			Stats["Exp"] += 50
			eventMessage("\nYou're shaking from a mix of blood loss and adrenaline as you stand over the now dead rat.\n\nYou gained 50 exp!")	
			(curHealth, curStam, curTokens) = CheckLvl(curHealth, curStam, curTokens)

			return(curHealth, curStam, curTokens, inventory)	
		
		
		def digDisillusioned(curHealth, curStam, curTokens, hasSword):
			loop = 0
			while loop == 0:
				takeInput('\n\nMaking it back to where the cave seems to have given in you look at the pile of boulders and rocks, and hear that low ringing thunderously rolling out from the cracks. Do you begin digging out rocks or turn away?\n\n8.) Dig\n6.) Turn away')
			
				if buttonPushed.get() == "8":
					eventMessage("\nYou struggle to pull out rock after rock from the pile honing in on the origin of the sound. Your hands start to bleed and ache as you work through the rocks but it's nothing compared to the pain from the clearing earlier and you keep digging through. The ringing becomes higher and higher pitched as you remove more rocks around it and eventually you see a couple broken chain links scattered aroud and pick up your pace. Finally you unveil a shimmering silver blade and pick it out of the rubble. The ring intensifies and resonates inside of your body and mind, meanwhile the silver blade glows white brighter and brighter by the second until you can no longer see anything but white around you, and then suddenly the light fades out and the ringing stops. You look at the blade and a white sheen dances along the surface with a gentle sound resonating quietly for only a brief moment and then its nothing more than a beautifully smithed sword. Gripping the sword tightly you feel a new energy flowing through you!\n")

					hasSword = True

					Stats["Lvl"] = 1
					Stats["Exp"] = 0
					Stats["Atk"] = 12
					Stats["Def"] = 9
					Stats["Stam"] = 4
					Stats["Health"] = 40
					Stats["ExpPoint"] = 50
					Stats["Skills"] = []

					StamBar = Stats["Stam"]*10
					curStam = StamBar
					curHealth = Stats["Health"]

					updateStatus(curHealth, curStam, curTokens)

					eventMessage('\nFeeling invigorated you confidently hold the glowing blade over head and move your previously sore and frail joints.\n\nYou have new stats!\n\n')

					return(curHealth, curStam, hasSword)

				elif buttonPushed.get() == "6":
					
					eventMessage('\n\nListening to the resonating sound calling out for you from under the rubble you stop and decide maybe you would be better off leaving it in its place.')
					return(curHealth, curStam, hasSword)
	
		
		def digStart(curHealth, curStam, curTokens, hasSword):
			eventMessage("\nYou eye up the mound of rocks and boulders and designate a few that you feel you can pull out from the weight of the others. As you start to work them out all you seem to be achieving is having more rocks come down in their place from the collapsed ceiling.")
			loop = 0
			while loop == 0:
				takeInput("\nDo you want to continue digging into the rocks or give up?\n\n8.) Continue digging\n6.) Give up\n\n")

				if buttonPushed.get() == '8':
					loop+=1
					curHealth = takeDamage(4, Stats, curHealth)
					updateStatus(curHealth, curStam, curTokens)
					eventMessage('\nAs you peel out rocks a large rock falls down on top of you and strikes the back of your head.\nYour health drops 4 points, it is now '+str(curHealth))
					
					while loop == 1:
						takeInput('\nDo you still continue or give up?\n\n8.) Continue\n6.) Give up\n\n')

						if buttonPushed.get() == '8':
							loop+=1
							curHealth = takeDamage(2, Stats, curHealth)
							updateStatus(curHealth, curStam, curTokens)
							eventMessage('\nYou dig feverishly thorugh the pile and the ringing you\'ve been hearing resonates in a higher and higher tone as you do so, several stones into the process you notice the skin wearing off of your hands rubbing them raw.\nYour health drops another 2 points, it is now '+str(curHealth))
							
							while loop == 2:
								takeInput('\nDo you still continue or give up?\n\n8.) Continue\n6.) Give up\n\n')

								if buttonPushed.get() == '8':

									hasSword = True

									Stats["Lvl"] = 1
									Stats["Exp"] = 0
									Stats["Atk"] = 12
									Stats["Def"] = 9
									Stats["Stam"] = 4
									Stats["Health"] = 40
									Stats["ExpPoint"] = 50
									Stats["Skills"] = []

									StamBar = Stats["Stam"]*10
									curStam = StamBar
									curHealth = Stats["Health"]

									updateStatus(curHealth, curStam, curTokens)
									eventMessage('\nYou finally uncover what appears to be a brilliantly crafted shimmering blade. Hoisting it out of the heap you feel a warmth shoot out of the blade and into your hand and rippling through your body.\nYou have new stats!\n\n')

									return(curHealth, curStam, hasSword)

								elif buttonPushed.get() == '6':
									eventMessage('\nYou give up on trying to work through all this rubble and turn back to go through the passage way behind you.\n\n')
									return(curHealth, curStam, hasSword)

						elif buttonPushed.get() == '6':
							eventMessage('\nYou give up on trying to work through all this rubble and turn back to go through the passage way behind you.\n\n')
							return(curHealth, curStam, hasSword)

				elif buttonPushed.get() == '6':
					eventMessage("\nYou give up on trying to work through all this rubble and turn back to go through the passage way behind you.\n\n")
					return(curHealth, curStam, hasSword)

		#Map information
		map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
			    [0, 0, 0, 0, 21, 0, 0, 0, 0],
			    [0, 0, 0, 1, 1, 1, 0, 0, 0],
			    [0, 0, 1, 1, 1, 1, 1, 0, 0],
		   		[0, 0, 0, 1, 23, 1, 0, 0, 0],
			    [0, 0, 0, 0, 1, 0, 0, 0, 0],
			    [0, 0, 0, 0, 24, 0, 0, 0, 0],
			    [0, 0, 0, 0, 1, 0, 0, 0, 0],
			    [0, 0, 0, 0, 1, 0, 0, 0, 0],
			    [0, 0, 0, 0, 20, 0, 0, 0, 0],
			    [0, 0, 0, 0, 0, 0, 0, 0, 0]]

		shownMap = {
		"0-0": "╔", "0-1": "═", "0-2": "═", "0-3": "═", "0-4": "═", "0-5": "═", "0-6": "═", "0-7": "═", "0-8": "╗",
		"1-0": "║", "1-1": " ", "1-2": " ", "1-3": " ", "1-4": " ", "1-5": " ", "1-6": " ", "1-7": " ", "1-8": "║",
		"2-0": "║", "2-1": " ", "2-2": " ", "2-3": " ", "2-4": " ", "2-5": " ", "2-6": " ", "2-7": " ", "2-8": "║",
		"3-0": "║", "3-1": " ", "3-2": " ", "3-3": " ", "3-4": " ", "3-5": " ", "3-6": " ", "3-7": " ", "3-8": "║",
		"4-0": "║", "4-1": " ", "4-2": " ", "4-3": " ", "4-4": " ", "4-5": " ", "4-6": " ", "4-7": " ", "4-8": "║",
		"5-0": "║", "5-1": " ", "5-2": " ", "5-3": " ", "5-4": " ", "5-5": " ", "5-6": " ", "5-7": " ", "5-8": "║",
		"6-0": "║", "6-1": " ", "6-2": " ", "6-3": " ", "6-4": " ", "6-5": " ", "6-6": " ", "6-7": " ", "6-8": "║",
		"7-0": "║", "7-1": " ", "7-2": " ", "7-3": " ", "7-4": " ", "7-5": " ", "7-6": " ", "7-7": " ", "7-8": "║",
		"8-0": "║", "8-1": " ", "8-2": " ", "8-3": " ", "8-4": " ", "8-5": " ", "8-6": " ", "8-7": " ", "8-8": "║",
		"9-0": "║", "9-1": " ", "9-2": " ", "9-3": " ", "9-4": " ", "9-5": " ", "9-6": " ", "9-7": " ", "9-8": "║",
		"10-0": "╚", "10-1": "═", "10-2": "═", "10-3": "═", "10-4": "═", "10-5": "═", "10-6": "═", "10-7": "═", "10-8": "╝",
		}


		curX = 4
		curY = 7

		lastRow = 10
		lastCol = 8


		#Hero's status
		StamBar = Stats["Stam"]*10
		curStam = StamBar
		curHealth = Stats["Health"]
		curTokens = len(Stats["Skills"])

		#Conditionals
		enteredClearing = False
		ratKilled = False
		metNoIllusionRats = False
		disillusioned = False
		hasSword = False
		hasDug = False
		hasDug2 = False
		seenMaidenLeave = False

		while curHealth > 0:
			updateMap(map1, shownMap, curY, curX, lastRow, lastCol)
			takeInput("\nmove up, down, right, or left?\n\n8.) Up\n6.) Right\n4.) Left\n2.) Down\n\n")

			#Moving Down
			if buttonPushed.get() == "2":
				
				if curY == lastRow-1 or map1[curY+1][curX] == 0:
					eventMessage("\nCannot move down")

				elif map1[curY+1][curX] == 1:
					curY+=1

				elif map1[curY+1][curX] == 2:
					curY+=1

				elif map1[curY+1][curX] == 20:
					curY+=1
					if ratKilled == False and hasDug == False:
						updateMap(map1, shownMap, curY, curX, lastRow, lastCol)
						(curHealth, curStam, hasSword) = digStart(curHealth, curStam, curTokens, hasSword)
						hasDug = True
						map1[9][4] = 1
					elif enteredClearing == True and hasSword == False and globalConditionals["acceptedMaiden"] == False:
						updateMap(map1, shownMap, curY, curX, lastRow, lastCol)
						(curHealth, curStam, hasSword) = digDisillusioned(curHealth, curStam, curTokens, hasSword)
						hasDug2 = True
						map1[9][4] = 1

				elif map1[curY+1][curX] == 23:
					curY+=1
			
				elif map1[curY+1][curX] == 24:
					curY+=1
					if ratKilled == True and disillusioned == True and seenDisillusionedRat == False:
						eventMessage("\nCautiously sneaking past the burrow the rat emerged from earlier you notice the corpse of the rat looks much less feral than before, almost friendly and well groomed....")
						seenDisillusionedRat = True
			
			#Moving Up
			elif buttonPushed.get() == "8":
				
				if curY == 1 or map1[curY-1][curX] == 0:
					eventMessage("\nCannot move up")
				
				elif map1[curY-1][curX] == 1:
					curY-=1

				elif map1[curY-1][curX] == 2:
					curY-=1
					map1[curY][curX] = 1
					map1[4][4] = 23

				elif map1[curY-1][curX] == 21:
					secondMap(curHealth, curStam, curTokens, inventory, heldInventory, hasSword, disillusioned)
				
				elif map1[curY-1][curX] == 23:
					curY-=1
					if hasSword == False and enteredClearing == False:
						updateMap(map1, shownMap, curY, curX, lastRow, lastCol)
						(curHealth, curStam, curTokens, disillusioned) = clearingIllusions(curHealth, curStam, curTokens, inventory, heldInventory)
						enteredClearing = True
						map1[4][4] = 1
						if disillusioned:
							map1[9][4] == 20
							map1[6][4] == 24
							map1[curY+2][curX] == 2
						else:
							map1[9][4] = 1
						updateMap(map1, shownMap, curY, curX, lastRow, lastCol)
						eventMessage(str(map1[4][4]))
					elif hasSword == True and enteredClearing == False:
						updateMap(map1, shownMap, curY, curX, lastRow, lastCol)
						(curHealth, curStam, curTokens, inventory) = clearingNoIllusions(curHealth, curStam, curTokens, inventory, heldInventory)
						enteredClearing = True
						map1[curY][curX] = 1
						if globalConditionals["firstMaidenDead"] == True:
							map1[3][6] == 2000

					elif enteredClearing == True and disillusioned == True and seenMaidenLeave == False:
						seenMaidenLeave == True
						eventMessage("\nYou note that the statue and the waters from before are missing now.\n")
				
				elif map1[curY-1][curX] == 24:
					curY-=1
					if ratKilled == False and hasSword == False:
						updateMap(map1, shownMap, curY, curX, lastRow, lastCol)
						(curHealth, curStam, curTokens, inventory) = ratFight(curHealth, curStam, curTokens, inventory, heldInventory)
						ratKilled = True
						map1[curY][curX] = 1
					elif ratKilled == False and hasSword == True:
						eventMessage("\nAlong the way you see a burrow in the cavern wall and a family of immense rats with smooth sleek coats of fur. As intimidating as these large creatures may be they seem friendly enough and they let you pass freely.\n")                             
						map1[curY][curX] = 1         
			
			#Moving Right
			elif buttonPushed.get() == "6":
				
				if curX == lastCol-1 or map1[curY][curX+1] == 0:
					eventMessage("\nCannot move right")
				
				elif map1[curY][curX+1] == 1:
					curX+=1
				
				elif map1[curY][curX+1] == 2000:
					curX+=1
					if hasSword == True and globalConditionals["firstMaidenDead"] == True:
						eventMessage('\n"This waters gross.."')
						map1[curY][curX] = 1
			
			#Moving Left
			elif buttonPushed.get() == "4":
				
				if curX == 1 or map1[curY][curX-1] == 0:
					eventMessage("\nCannot move left")
				
				else:
					curX-=1		

		updateMap(map1, shownMap, curY, curX, lastRow, lastCol)

	firstMap()

	gameWindow.mainloop()


def launchApp():
	keySet = ["8, 6, 4, 2, 5"]
	resolution = []
	user32 = ctypes.windll.user32
	resolution.append(user32.GetSystemMetrics(0))
	resolution.append(user32.GetSystemMetrics(1))

	def doNothing():
		return

	def keyChoice():

		def closed():
			b6.config(command=keyChoice)
			keys.destroy()

		def nums():
			wasd.deselect()
			var.set(True)
			var2.set(False)
			
		def wasd():
			nums.deselect()
			var.set(False)
			var2.set(True)

		def store():
			if var.get():
				keySet[0]="8, 6, 4, 2, 5"
			elif var2.get():
				keySet[0]="W, A, S, D, R"
			b6.config(command=keyChoice)
			keys.destroy()
			
		var = BooleanVar()
		var2 = BooleanVar()
		
		keys = Toplevel()
		keys.configure(bg='dim gray')
		keys.title('Key sets')
		keysPush = '160x110+'+str(int(resolution[0])//2-80)+'+'+str(int(resolution[1])//2-5)
		keys.geometry(keysPush)

		b6.config(command=doNothing)

		checkButtonsFrame = Frame(keys, bg='dim gray')
		checkButtonsFrame.grid()

		nums = Checkbutton(checkButtonsFrame, text="8, 6, 4, 2, 5", bg='dim gray', fg='black', variable=var, command=nums)
		nums.grid(columnspan=13, pady=3, padx=3, sticky="w")

		wasd = Checkbutton(checkButtonsFrame, text="W, A, S, D, R", bg='dim gray', fg='black', variable=var2, command=wasd)
		wasd.grid(columnspan=13, pady=3, padx=3, sticky="w")

		if keySet[0] == '8, 6, 4, 2, 5':
			nums.select()
		elif keySet[0] == 'W, A, S, D, R':
			wasd.select()

		Apply = Button(checkButtonsFrame, text="Apply", bg='gray9', fg='red4', command=store)
		Apply.grid(column=5, columnspan=5, pady=6)

		keys.protocol("WM_DELETE_WINDOW", closed)

		keys.mainloop()

	def goToMap1():
		launch.destroy()
		gamePlay(keySet, resolution)
		
	launch = Tk()
	launch.configure(bg='dim gray')
	launch.title('Dungeon Game')
	launchPush = '400x430+'+str(int(resolution[0])//2-200)+'+'+str(int(resolution[1])//2-215)
	launch.geometry(launchPush)

	launch.protocol("WM_DELETE_WINDOW", lambda: launch.destroy())

	launchFrame = Frame(launch, bg='dim gray')
	launchFrame.grid()

	textFrame = Frame(launchFrame, width=400, height=360, bg='dim gray')
	textFrame.grid(columnspan=50)
   
	textFrame.columnconfigure(0, weight=10)  

	textFrame.grid_propagate(False)

	introImage = Text(textFrame, state='normal', bg='gray9',fg='red4')
	introImage.grid(pady=3, padx=6, sticky="we")
	introImage.insert('end', "╔══════════════════════════════════════════════╗\n")
	introImage.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░▓▓░░░░▓░░░▓░▓░░░▓░▓▓▓▓▓░▓▓▓▓▓░▓▓▓▓▓░▓░░░▓░░░║\n")
	introImage.insert('end', "║░░▓░▓░░░▓░░░▓░▓▓░░▓░▓░░░▓░▓░░░░░▓░░░▓░▓▓░░▓░░░║\n")
	introImage.insert('end', "║░░▓░░▓░░▓░░░▓░▓▓░░▓░▓░░░▓░▓░░░░░▓░░░▓░▓▓░░▓░░░║\n")
	introImage.insert('end', "║░░▓░░░▓░▓░░░▓░▓░▓░▓░▓░░░░░▓▓▓▓▓░▓░░░▓░▓░▓░▓░░░║\n")
	introImage.insert('end', "║░░▓░░▓░░▓░░░▓░▓░▓░▓░▓░▓▓▓░▓░░░░░▓░░░▓░▓░▓░▓░░░║\n")
	introImage.insert('end', "║░░▓░▓░░░▓░░░▓░▓░░▓▓░▓░░░▓░▓░░░░░▓░░░▓░▓░░▓▓░░░║\n")
	introImage.insert('end', "║░░▓▓░░░░▓▓▓▓▓░▓░░░▓░▓▓▓▓▓░▓▓▓▓▓░▓▓▓▓▓░▓░░░▓░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░▓▓▓▓▓░░░▓░░░▓░░░▓░▓▓▓▓▓░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░▓░░░▓░░░▓░░░▓▓░▓▓░▓░░░░░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░▓░░░▓░░▓░▓░░▓▓░▓▓░▓░░░░░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░▓░░░░░░▓░▓░░▓░▓░▓░▓▓▓▓▓░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░▓░▓▓▓░▓▓▓▓▓░▓░▓░▓░▓░░░░░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░▓░░░▓░▓░░░▓░▓░░░▓░▓░░░░░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░▓▓▓▓▓░▓░░░▓░▓░░░▓░▓▓▓▓▓░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	introImage.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	introImage.insert('end', "╚══════════════════════════════════════════════╝")
	introImage.config(state='disabled')

	b6 = Button(launchFrame, text="Set keys", bg='gray9',fg='red4', command=keyChoice)
	b6.grid(row=3, column=18, columnspan=14, pady=3, sticky="we")

	b4 = Button(launchFrame, text="Launch game", bg='gray9',fg='red4', command=goToMap1)
	b4.grid(row=4, column=18, columnspan=14, pady=3, sticky="we")

	launch.mainloop()

launchApp()