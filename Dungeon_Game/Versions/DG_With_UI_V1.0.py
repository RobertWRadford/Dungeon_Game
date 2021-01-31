#Written by Robert W. Radford
#V1.0
#21Jan2020
#V1.1 - Split main() code into more functions to clear up clutter
#26Jan2020
#V2.0 - Stats changed to dictionary, and skills/items lists are added (not implemented)
#03Feb2020
#V2.5 - Resolved all global variable calls to local scope, started skills implementation
#04Feb2020 
#V2.6 - Changed all input to take integer answers 8 -> 6 -> 4 -> 2 -> 5
#05Feb2020
#V3.0 - Took game off rails, add blind map discovery system to display
#05Feb2020
#V3.1 - Changed event tiles appearance in mapping to distinguish them.
#06Feb2020
#V4.0 - Fully implemented map 2, made balance changes for map 1 combat, approaching full implementation of item and skill use.
#		Polished up some new line usage and some output. Fixed bug for gaining more than 1 level at a time not giving all skills up to new level.
#		Modified printEnvironment() to include a 4th possible symbol for chance encounter zones.
#13Feb2020
#
#V4.5 - Expanded vision to 3 tiles, restructured for organization, added a symbol for poison as well as changed items and main encounters to be more distinguished.
#		Moved global functions into local scopes
#		Implemented fights for rest triggers on map 2 and finalized item and skill implementation
#20Feb2020
#V4.6 - Expanded vision to 4 tiles, cleaned fights into "basic fight" function. Modified scaling stats for no sword route.
#		Added lore details from feeding starved men and implemented the Adoma map 2 fight 
#29Feb2020
#V5.0 - Made map 3 hunters project and implemented for game purposes. implemented maps 3, 4, and 5. Troubleshot minor errors
#
#Future plans - Make side project for UI that calls this project; implement toolbar with a help tutorials tab and a savestate option.
#				Build out story details, individual fights and units, as well as designate items on maps 3 and 4.
#				Improve combat "ai" to make more decisions than attack and rest if out of stam.
#				give opponents skills and build atemi to use opponents skill on themself if they have one, else default to current state.
#				consider a higher level cap and scaling potential.
#				consider music and art options to add.
#				package into an executable file 

import copy
import random
from tkinter import *

#Regularly called text
combatTutorial="\nYou can type, '8' to attack the Opponent, '6' to reduce your damage received, '4' to get double stamina returned, '2' to view your skills menu, or '5' to view your item menu.\n"

#Ending conditionals
usedMaiden = False
firstMaidenDead = False
AdomaDead = False

def theGame(keySet):
	
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
	StamBar = [Stats["Stam"]*10]
	curStam = [StamBar]
	curHealth = [Stats["Health"]]
	curTokens = [len(Stats["Skills"])]
	inventory = []
	heldInventory = []
	hasSword = [0]

	#StatusAdjustmentFunctions
	def CheckLvl():
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
		LvlNow = Stats["Lvl"]
		expToLevel = Stats["ExpPoint"] - Stats["Exp"]
		if LvlPre != LvlNow:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nCongratulations! Leveled up\n")
			eventScreen.config(state='disabled')
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
			expToLevel = Stats["ExpPoint"] - Stats["Exp"]
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nExp to next level: ", expToLevel, "\n")
			eventScreen.config(state='disabled')
			NewStats()
			StamBar[0] = Stats["Stam"]*10
			curTokens[0] = len(Stats["Skills"])
			printStatus(Stats, curHealth, curStam, StamBar)
		else:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "and ", "\nExp to next level: ", expToLevel, "\n")
			eventScreen.config(state='disabled')

	def NewStats():
		
		skillsToLearn = ["Heavy_Blow", "Counter", "Meditate", "Shatter", "Grapple", "Flurry", "Atemi"]

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

		i = LvlNow
		if LvlNow - LvlPre > 2:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nYou learned new skills, ", end='')
			eventScreen.config(state='disabled')
			while i > LvlPre:
				Stats["Skills"].append(skillsToLearn[i-2].strip())
				i-=1
			i = LvlNow
			while i > LvlPre+1:
				eventScreen.config(state='normal')
				eventScreen.insert('end', Stats["Skills"][i-2].replace("_", " "), ", ", end='')
				eventScreen.config(state='disabled')
				i-=1
			eventScreen.config(state='normal')
			eventScreen.insert('end', "and ", Stats["Skills"][i-2].replace("_", " "), ".\n")
			eventScreen.config(state='disabled')
		elif LvlNow - LvlPre > 1:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nYou learned new skills, ", end='')
			eventScreen.config(state='disabled')
			while i > LvlPre:
				Stats["Skills"].append(skillsToLearn[i-2].strip())
				i-=1
			i = LvlNow
			while i > LvlPre+1:
				eventScreen.config(state='normal')
				eventScreen.insert('end', Stats["Skills"][i-2].replace("_", " "), end=' ')
				eventScreen.config(state='disabled')
				i-=1
			eventScreen.config(state='normal')
			eventScreen.insert('end', "and ", Stats["Skills"][i-2].replace("_", " "), ".\n")
			eventScreen.config(state='disabled')
		else:
			Stats["Skills"].append(skillsToLearn[i-2].strip())
			eventScreen.config(state='normal')
			eventScreen.insert('end', "You learned a new skill, ", Stats["Skills"][i-2].replace("_", " "), ".\n")
			eventScreen.config(state='disabled')

	def swordCheckLvl():
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
		sToLevel = Stats["ExpPoint"] - Stats["Exp"]                
		LvlNow = Stats["Lvl"]
		if LvlPre != LvlNow:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nCongratulations! Leveled up\n")
			eventScreen.config(state='disabled')
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
			sToLevel = Stats["ExpPoint"] - Stats["Exp"]
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nExp to next level: " + str(sToLevel) + "\n")
			eventScreen.config(state='disabled')
			swordNewStats()
			StamBar[0] = Stats["Stam"]*10
			curTokens[0] = len(Stats["Skills"])
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nYour new stats are:")
			eventScreen.config(state='disabled')
			printStatus(Stats, curHealth, curStam, StamBar)
		else:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nExp to next level: ", sToLevel, "\n")
			eventScreen.config(state='disabled')

	def swordNewStats():
		skillsToLearn = ["Datotsu", "Haya_Suburi", "Mokuso", "Pierce", "Drain", "Regenerate", "Kachinuki"]

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

		i = LvlNow
		if LvlNow - LvlPre > 2:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nYou learned new skills, ", end='')
			eventScreen.config(state='disabled')
			while i > LvlPre:
				Stats["Skills"].append(skillsToLearn[i-2].strip())
				i-=1
			i = LvlNow
			while i > LvlPre+1:
				eventScreen.config(state='normal')
				eventScreen.insert('end', Stats["Skills"][i-2].replace("_", " "), ", ", end='')
				eventScreen.config(state='disabled')
				i-=1
			eventScreen.config(state='normal')
			eventScreen.insert('end', "and ", Stats["Skills"][i-2].replace("_", " "), ".\n")
			eventScreen.config(state='disabled')
		elif LvlNow - LvlPre > 1:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nYou learned new skills, ", end='')
			eventScreen.config(state='disabled')
			while i > LvlPre:
				Stats["Skills"].append(skillsToLearn[i-2].strip())
				i-=1
			i = LvlNow
			while i > LvlPre+1:
				eventScreen.config(state='normal')
				eventScreen.insert('end', Stats["Skills"][i-2].replace("_", " "), end=' ')
				eventScreen.config(state='disabled')
				i-=1
			eventScreen.config(state='normal')
			eventScreen.insert('end', "and ", Stats["Skills"][i-2].replace("_", " "), ".\n")
			eventScreen.config(state='disabled')
		else:
			Stats["Skills"].append(skillsToLearn[i-2].strip())
			eventScreen.config(state='normal')
			eventScreen.insert('end', "You learned a new skill, ", Stats["Skills"][i-2].replace("_", " "), ".\n")
			eventScreen.config(state='disabled')

	def fullInventory():
		itemCount = len(inventory)
		heldItemCount = len(heldInventory)
		Inventory = ",".join(inventory[0:itemCount])
		HeldInventory = ",".join(heldInventory[0:heldItemCount])
		l = 0
		n = 8
		i = 0

		if len(inventory) == 4:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nYou have ", Inventory, " currently in your inventory. You found '", inventory[3], "'\n")
			eventScreen.config(state='disabled')
			choice = input("\nYou can\n8.) Use an item to make room\n6.) Throw away an item\n")
			while l == 0:
				if choice == 8:
					l+=1
					while l == 1:
						use = input("\nWhich item will you use?\n8.) ", inventory[0], "\n6.) ", inventory[1], "\n4.) ", inventory[2], "\n2.) ", inventory[3], "\n")
						if use != (8 or 6 or 4 or 2):
							continue
						else:
							if use == 8:
								use = 0
							elif use == 6:
								use = 1
							elif use == 4:
								use = 2
							elif use == 2:
								use = 3
							useItem(0)
							inventory.remove(inventory[use])
				elif choice == 6:
					l+=1
					throw = input("\nWhich item will you throw away?\n8.) ", inventory[0], "\n6.) ", inventory[1], "\n4.) ", inventory[2], "\n2.) ", inventory[3], "\n")
					while l == 1:
						if throw != (8 or 6 or 4 or 2):
							throw = input("\nPlease input '8' '6' '4' or '2'\n")
						else:
							if throw == 8:
								throw = 0
							elif throw == 6:
								throw = 1
							elif throw == 4:
								throw = 2
							elif throw == 2:
								throw = 3
							inventory.remove(inventory[throw])
				else:
					choice = input("Please only input '8' or '6'")

		elif len(HeldInventory) == 4:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nYou are holding ", HeldInventory, ". You found a '", HeldInventory[3], "'\n")
			eventScreen.config(state='disabled')
			while l == 0:
				throw = input("\nWhich item will you throw away?\n8.) ", holdInventory[0], "\n6.) ", holdInventory[1], "\n4.) ", holdInventory[2], "\n2.) ", holdInventory[3], "\n")
				if throw != (8 or 6 or 4 or 2):
					continue
				else:
					if throw == 8:
						throw = 0
					elif throw == 6:
						throw = 1
					elif throw == 4:
						throw = 2
					elif throw == 2:
						throw = 3
					inventory.remove(heldInventory[throw])
					return(curHealth, curStam, inventory, heldInventory, OppStats, OppCurHealth, OppCurStam)

		else:
			eventScreen.config(state='normal')
			eventScreen.insert('end', "\nYou have ", Inventory, " currently in your inventory.\n")
			eventScreen.config(state='disabled')
			while l == 0:
				eventScreen.config(state='normal')
				eventScreen.insert('end', "\nWhich item will you use?\n")
				eventScreen.config(state='disabled')
				while i < itemCount:
					eventScreen.config(state='normal')
					eventScreen.insert('end', (n, ".) ", inventory[i], "\n"))
					eventScreen.config(state='disabled')
					n-=2
					i+=1
				use = input("\n")
				if itemCount == 1:
					if use == 8:
						use = 0
						l+=1
				elif itemCount == 2:
					if use == 8:
						use = 0
						l+=1
					elif use == 6:
						use = 1
						l+=1
				elif itemCount == 3:
					if use == 8:
						use = 0
						l+=1
					elif use == 6:
						use = 1
						l+=1
					elif use == 4:
						use = 2
						l+=1
			useItem(1)
			inventory.remove(inventory[use])

	def useItem(Stats, curHealth, curStam, StamBar, item, inCombat, OppName, OppStats, OppCurHealth, OppCurStam, OppStamBar):

		if item == "Stale bread":
			curStam = min(curStam + (StamBar/4), StamBar)
			print("\nYou start eating through a rather unpleasant loaf, you regain some stamina", StamBar/4, " and your stamina is now ", curStam, "\n")
			return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
		if item == "Bandages":
			curHealth = min(curHealth + (Stats["Health"]/4), Stats["Health"])
			print("\nYou wrap up some open wounds. You heal ", Stats["Health"]/4, " and your health is now ", curHealth, "\n")
			return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
		elif item == "Adrenaline":
			curStam = min(curStam + (StamBar/2), StamBar)
			print("\nYou consume some adrenaline, you regain some stamina", StamBar/2, " and your stamina is now ", curStam, "\n")
			return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
		elif item == "Oily water":
			#If Opponent is axe demon, Devora, Adoma, Imp, Shadow... deal % health damage and reduce their def by 2; if Opponent fire demon deal 2x the %health damage
			#If used out of combat print something like splash and do nothing; if used in combat on target not above print something like you throw a spritz of water... it doesn't seem to do much
			#will need to pass if in combat and string for Opponents name
			if not inCombat:
				print("\nsplash!\n")
				return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
			elif inCombat and OppName in ["axeDemon", "Devora", "Adoma", "imp", "Shadow"]:
				(OppCurHealth) = takeDamage((OppStats["Health"]/8), OppStats, OppCurHealth)
				OppStats["Def"]-=2
				return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
			elif inCombat and OppName == ("Fire Shadow"):
				(OppCurHealth[0]) = takeDamage((OppStats["Health"]/4), OppStats, OppCurHealth[0])
				OppStats["Def"]-=2
			else:
				eventScreen.config(state='normal')
				eventScreen.insert('end', "\nYou splash out the vials contents... nothing happened\n")
				eventScreen.config(state='disabled')

	def statProgress():
		eventScreen.config(state='normal')
		eventScreen.insert('end', "\nOpponent HP:      ", OppCurHealth[0], "                     ", "Your HP:      ", curHealth[0], "Opponent Stamina: ", OppCurStam[0], "                   ", "Your Stamina: ", curStam[0], "\n")
		eventScreen.config(state='disabled')

	def printStatus():
		eventScreen.config(state='normal')
		eventScreen.insert('end', "\nLevel: ", Stats["Lvl"], "\nAttack: ", Stats["Atk"], "\nDefense: ", Stats["Def"], "\nHealth: ", curHealth[0], "/", Stats["Health"], "\nStamina: ", curStam[0], "/", StamBar[0], "\n\n")
		eventScreen.config(state='disabled')

	def button8():
		buttonPressed = ["8"]

	def button6():
		buttonPressed = ["6"]

	def button4():
		buttonPressed = ["4"]

	def button2():
		buttonPressed = ["2"]

	def button5():
		buttonPressed = ["5"]

	def saveGame():
		mainScreen.config(state='normal')
		mainScreen.insert('end', "Saved the worl-... game\n")
		mainScreen.config(state='disabled')

	def loadGame():
		mainScreen.config(state='normal')
		mainScreen.insert('end', "hey this totally like... opened a saave file... heh\n")
		mainScreen.config(state='disabled')

	def tutorial():
		mainScreen.config(state='normal')
		mainScreen.insert('end', "press 8, 6, 4, 2, or 5\n")
		mainScreen.config(state='disabled')

	def mapLegend():
		mainScreen.config(state='normal')
		mainScreen.insert('end', "╕ is a main event\n")
		mainScreen.config(state='disabled')

	gameWindow = Tk()
	gameWindow.title('Dungeon Game')
	gameWindow.geometry("900x600")

	menuBar = Menu(gameWindow)
	fileMenu = Menu(menuBar, tearoff=0)
	fileMenu.add_command(label="Save", command=saveGame)
	fileMenu.add_command(label="Load", command=loadGame)
	fileMenu.add_separator()
	menuBar.add_cascade(label="File",menu=fileMenu)
	helpMenu = Menu(menuBar, tearoff=0)
	helpMenu.add_command(label="Combat tutorial", command=tutorial)
	helpMenu.add_command(label="Map Legend", command=mapLegend)
	menuBar.add_cascade(label="Help", menu=helpMenu)
	screen.config(menu=menuBar)

	mapFrame = Frame(gameWindow, width=110, height=180)
	mapFrame.grid(column=1, row=1, rowspan=2, columnspan=40, padx=25, pady=25)
	mapFrame.columnconfigure(0, weight=10)
	mapFrame.grid_propagate(False)

	mapScreen = Text(mapFrame, state='normal', bg='black',fg='white')
	mapScreen.grid(pady=6, padx=6, sticky="we")
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

	eventFrame = Frame(gameWindow, width = 700, height=300)
	eventFrame.grid(column=42, row=1, columnspan=80, rowspan=2, padx=25, pady=25)
	eventFrame.columnconfigure(0, weight=10)
	eventFrame.grid_propagate(False)

	eventScreen = Text(eventFrame, state='normal', bg='black',fg='white', wrap=WORD)
	eventScreen.grid(pady=6, padx=6, sticky="we")
	eventScreen.insert('end', "You wake up alone in a cave system wearing only a shredded up cheap tunic. Looking around, you see a narrow passageway in front and behind you. From behind you theres a constant low ringing sound but you can only make out a caved in wall of rocks, in front of you is a silent and empty, dark passgeway.\n\n")
	eventScreen.config(state='disabled')

	buttonsFrame = Frame(gameWindow, width=500, height=720)
	buttonsFrame.grid(column=1, row=3, columnspan=95, padx=25)
	buttonsFrame.columnconfigure(0, weight=10)
	buttonsFrame.grid_propagate(False)

	button8Text = StringVar()
	if keySet == "W, A, S, D, R":
		button8Text.set("╔═════╗\n║         W         ║\n╚═════╝")
		gameWindow.bind('<W>', lambda e: button8())
	else:
		button8Text.set("╔═════╗\n║         8         ║\n╚═════╝")
		gameWindow.bind('<8>', lambda e: button8())
	b8 = Button(buttonsFrame, textvariable=button8Text, bg='black', fg = 'white', command=button8)
	b8.grid(column=19, columnspan=8, row=1, pady=6)

	button6Text = StringVar()
	if keySet == "W, A, S, D, R":
		button6Text.set("╔═════╗\n║         D         ║\n╚═════╝")
		gameWindow.bind('<D>', lambda e: button6())
	else:
		button6Text.set("╔═════╗\n║         6         ║\n╚═════╝")
		gameWindow.bind('<6>', lambda e: button6())
	b6 = Button(buttonsFrame, textvariable=button6Text, bg='black', fg = 'white', command=button6)
	b6.grid(column=29, columnspan=8, row=2, padx=6, pady=6)

	button4Text = StringVar()
	if keySet == "W, A, S, D, R":
		button4Text.set("╔═════╗\n║         A         ║\n╚═════╝")
		gameWindow.bind('<A>', lambda e: button4())
	else:
		button4Text.set("╔═════╗\n║         4         ║\n╚═════╝")
		gameWindow.bind('<4>', lambda e: button4())
	b4 = Button(buttonsFrame, textvariable=button4Text, bg='black', fg = 'white', command=button4)
	b4.grid(column=9, columnspan=8, row=2, padx=6, pady=6)

	button2Text = StringVar()
	if keySet == "W, A, S, D, R":
		button2Text.set("╔═════╗\n║         S         ║\n╚═════╝")
		gameWindow.bind('<S>', lambda e: button2())
	else:
		button2Text.set("╔═════╗\n║         2         ║\n╚═════╝")
		gameWindow.bind('<2>', lambda e: button2())
	b2 = Button(buttonsFrame, textvariable=button2Text, bg='black', fg = 'white', command=button2)
	b2.grid(column=19, columnspan=8, row=3, pady=6)

	button5Text = StringVar()
	if keySet == "W, A, S, D, R":
		button5Text.set("╔═════╗\n║         R         ║\n╚═════╝")
		gameWindow.bind('<R>', lambda e: button5())
	else:
		button5Text.set("╔═════╗\n║         5         ║\n╚═════╝")
		gameWindow.bind('<5>', lambda e: button5())
	b5 = Button(buttonsFrame, textvariable=button5Text, bg='black', fg = 'white', command=button5)
	b5.grid(column=19, columnspan=8, row=2, padx=6, pady=6)
	b5.grid_forget()

	gameWindow.mainloop()


def launchApp():
	resolution = ["1280x720",]
	keySet = ["8, 6, 4, 2, and 5",]

	def keys():

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
			keys.destroy()
			
		var = BooleanVar()
		var2 = BooleanVar()
		
		keys = Tk()
		keys.title('Key sets')
		keys.geometry("160x110")

		checkButtonsFrame = Frame(keys)
		checkButtonsFrame.grid()

		nums = Checkbutton(checkButtonsFrame, text="8, 6, 4, 2, 5", variable=var, command=nums)
		nums.grid(columnspan=13, pady=3, padx=3, sticky="w")

		wasd = Checkbutton(checkButtonsFrame, text="W, A, S, D, R", variable=var2, command=wasd)
		wasd.grid(columnspan=13, pady=3, padx=3, sticky="w")

		Apply = Button(checkButtonsFrame, text="Apply", bg='black', fg = 'white', command=store)
		Apply.grid(column=5, columnspan=5, pady=6)

		keys.mainloop()

	def goToMap1():
		launch.destroy()
		map1(keySet[0])

	def resolutions():
		def small():
			medium.deselect()
			large.deselect()
			var2.set(False)
			var3.set(False)
			var.set(True)

		def medium():
			small.deselect()
			large.deselect()
			var2.set(True)
			var3.set(False)
			var.set(False)

		def large():
			small.deselect()
			medium.deselect()
			var2.set(False)
			var3.set(True)
			var.set(False)

		def store():
			nonlocal resolution
			if var.get():
				resolution="1280x720"
			elif var2.get():
				resolution="1920x1080"
			elif var3.get():
				resolution="2560x1440"
			res.destroy()
			
		var = BooleanVar()
		var2 = BooleanVar()
		var3 = BooleanVar()
		
		res = Tk()
		res.title('Resolutions')
		res.geometry("160x140")

		checkButtonsFrame = Frame(res)
		checkButtonsFrame.grid()

		small = Checkbutton(checkButtonsFrame, text="1280x720", variable=var, command=small)
		small.grid(columnspan=8, pady=3, padx=3, sticky="w")

		medium = Checkbutton(checkButtonsFrame, text="1920x1080", variable=var2, command=medium)
		medium.grid(columnspan=8, pady=3, padx=3, sticky="w")

		large = Checkbutton(checkButtonsFrame, text="2560x1440", variable=var3, command=large)
		large.grid(columnspan=8, pady=3, padx=3, sticky="w")

		Apply = Button(checkButtonsFrame, text="Apply", bg='black', fg = 'white', command=store)
		Apply.grid(column=5, columnspan=5, pady=6)

		res.mainloop()
		
	launch = Tk()
	launch.title('Dungeon Game')
	launch.geometry("400x460")

	launchFrame = Frame(launch)
	launchFrame.grid()

	textFrame = Frame(launchFrame, width=400, height=360)
	textFrame.grid(columnspan=50)

    # allow the column inside the entryFrame to grow    
	textFrame.columnconfigure(0, weight=10)  

    # By default the frame will shrink to whatever is inside of it and 
    # ignore width & height. We change that:
	textFrame.grid_propagate(False)
    # as far as I know you can not set this for x / y separately so you
    # have to choose a proper height for the frame or do something more sophisticated

    # input entry
	inValueText = Text(textFrame, state='normal', bg='black',fg='white')
	inValueText.grid(pady=3, padx=6, sticky="we")
	inValueText.insert('end', "╔══════════════════════════════════════════════╗\n")
	inValueText.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░▓▓░░░░▓░░░▓░▓░░░▓░▓▓▓▓▓░▓▓▓▓▓░▓▓▓▓▓░▓░░░▓░░░║\n")
	inValueText.insert('end', "║░░▓░▓░░░▓░░░▓░▓▓░░▓░▓░░░▓░▓░░░░░▓░░░▓░▓▓░░▓░░░║\n")
	inValueText.insert('end', "║░░▓░░▓░░▓░░░▓░▓▓░░▓░▓░░░▓░▓░░░░░▓░░░▓░▓▓░░▓░░░║\n")
	inValueText.insert('end', "║░░▓░░░▓░▓░░░▓░▓░▓░▓░▓░░░░░▓▓▓▓▓░▓░░░▓░▓░▓░▓░░░║\n")
	inValueText.insert('end', "║░░▓░░▓░░▓░░░▓░▓░▓░▓░▓░▓▓▓░▓░░░░░▓░░░▓░▓░▓░▓░░░║\n")
	inValueText.insert('end', "║░░▓░▓░░░▓░░░▓░▓░░▓▓░▓░░░▓░▓░░░░░▓░░░▓░▓░░▓▓░░░║\n")
	inValueText.insert('end', "║░░▓▓░░░░▓▓▓▓▓░▓░░░▓░▓▓▓▓▓░▓▓▓▓▓░▓▓▓▓▓░▓░░░▓░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░▓▓▓▓▓░░░▓░░░▓░░░▓░▓▓▓▓▓░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░▓░░░▓░░░▓░░░▓▓░▓▓░▓░░░░░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░▓░░░▓░░▓░▓░░▓▓░▓▓░▓░░░░░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░▓░░░░░░▓░▓░░▓░▓░▓░▓▓▓▓▓░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░▓░▓▓▓░▓▓▓▓▓░▓░▓░▓░▓░░░░░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░▓░░░▓░▓░░░▓░▓░░░▓░▓░░░░░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░▓▓▓▓▓░▓░░░▓░▓░░░▓░▓▓▓▓▓░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	inValueText.insert('end', "║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░║\n")
	inValueText.insert('end', "╚══════════════════════════════════════════════╝")
	inValueText.config(state='disabled')

	b8 = Button(launchFrame, text="Set Resolution", bg='black', fg = 'white', command=resolutions)
	b8.grid(row=2, column=18, columnspan=14, pady=3, sticky="we")

	b6 = Button(launchFrame, text="Set keys", bg='black', fg = 'white', command=keys)
	b6.grid(row=3, column=18, columnspan=14, pady=3, sticky="we")

	b4 = Button(launchFrame, text="Launch game", bg='black', fg = 'white', command=goToMap1)
	b4.grid(row=4, column=18, columnspan=14, pady=3, sticky="we")

	launch.mainloop()

launchApp()
