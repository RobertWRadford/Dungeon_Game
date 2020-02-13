#Written by Robert W. Radford
#V1.0
#21Jan2020
#V1.1 - Split main() code into more functions to clear up clutter
#26Jan2020
#V2.0 - Stats changed to dictionary, and skills/items lists are added (not implemented)
#03Feb2020
#V2.5 - Resolved all global variables calls to local scope, started skills implementation
#04Feb2020 
#V2.6 - Changed all input to take integer answers 8 -> 6 -> 4 -> 2 -> 5
#05Feb2020
#V3.0 - Took game off rails, add blind map discovery system to display
#06Feb2020


#Hero's status
TeroStats = {
	"Lvl": 1,
	"Exp": 0,
	"Atk": 4,
	"Def": 2,
	"Stam": 3,
	"Health": 25,
	"ExpPoint": 50,
	"Skills": [],
}
TeroStamBar = TeroStats["Stam"]*10
TeroCurrentStam = TeroStamBar
TeroCurrentHealth = TeroStats["Health"]
TeroSkillTokens = len(TeroStats["Skills"])
TeroCurrentTokens = TeroSkillTokens

#Hero's sword status
swordStats = {
	"Lvl": 1,
	"Exp": 0,
	"Atk": 12,
	"Def": 7,
	"Stam": 4,
	"Health": 40,
	"ExpPoint": 50,
	"Skills": [],
}
swordStamBar = swordStats["Stam"]*10
swordCurrentStam = swordStamBar
swordCurrentHealth = swordStats["Health"]
swordToLevel = swordStats["ExpPoint"] - swordStats["Exp"]
swordSkillTokens = len(swordStats["Skills"])
swordCurrentTokens = swordSkillTokens

inventory = []

#Regularly called text
combatInvalidChoice = "\nPlease choose from the available actions 'attack' 'defend' 'rest' 'skills'\n"
combatTutorial="\nYou can type, 'attack' to attack the opponent, 'defend' to reduce your damage received, 'rest' to get double stamina returned, or 'skills' to view your skills menu.\n"


#Ending conditionals
usedMaiden = False
firstMaidenDead = False



def printStatus(Stats, curHealth, curStam, StamBar):
	print("\n\nLevel: " + str(Stats["Lvl"]) + "\nAttack: " + str(Stats["Atk"]) + "\nDefense: " + str(Stats["Def"]) + "\nHealth: " + str(curHealth) + "/" + str(Stats["Health"]) + "\nStamina: " + str(curStam) + "/" + str(StamBar) + "\n\n")





def statProgress(OppCurHealth, OppCurStam, curHealth, curStam):
	print("\nOpponent HP:      " + str(OppCurHealth) + "                     " + "Your HP:      " + str(curHealth))
	print("Opponent Stamina: " + str(OppCurStam) + "                   " + "Your Stamina: " + str(curStam) + "\n")





def TeroSkillMenu(Stats):
	tokens = TeroCurrentTokens
	if tokens == 0:
		return("none")
	else:
		n = TeroSkillTokens
		i = 0
		while i < n:
			print(i+1, "). ", Stats["Skills"][i]+"\n")
		choice = input("You have ", tokens, " skill points left. What do you want to do?\n\n")
		return(choice)





def swordSkillMenu(Stats):
	tokens = swordCurrentTokens
	if tokens == 0:
		return("none")
	else:
		n = swordSkillTokens
		i = 0
		while i < n:
			print(i+1, "). ", Stats["Skills"][i]+"\n")
		choice = input("You have ", tokens, " skill points left. What do you want to do?\n\n")
		return(choice)






#StatusAdjustmentFunctions
def CheckLvl(Stats, curHealth, curStam, StamBar):
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
		print("\nCongratulations! Leveled up\n")
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
		print("\nExp to next level: " + str(expToLevel) + "\n")
		NewStats(Stats)
		printStatus(Stats, curHealth, curStam, StamBar)
	else:
		print("\nExp to next level: " + str(expToLevel) + "\n")
	return(Stats)





def NewStats(Stats):
	if Stats["Lvl"] == 2:
		Stats["Atk"] = 6
		Stats["Def"] = 3
		Stats["Stam"] = 3
		Stats["Health"] = 30
		#Heavy Blow deals 1.5* attack stat
		Stats["Skills"].append("Heavy Blow")
		print("\nYou learned a new skill, Heavy Blow\n")

	elif Stats["Lvl"] == 3:
		Stats["Atk"] = 9
		Stats["Def"] = 4
		Stats["Stam"] = 3
		Stats["Health"] = 35
		#Counter skill blends pros of attack and defend
		Stats["Skills"].append("Counter")
		print("\nYou learned a new skill, Counter\n")

	elif Stats["Lvl"] == 4:
		Stats["Atk"] = 12
		Stats["Def"] = 6
		Stats["Stam"] = 3
		Stats["Health"] = 45
		#Meditate skill restores 1.5* rest actions stam
		Stats["Skills"].append("Meditate")
		print("\nYou learned a new skill, Meditate\n")

	elif Stats["Lvl"] == 5:
		Stats["Atk"] = 15
		Stats["Def"] = 8
		Stats["Stam"] = 4
		Stats["Health"] = 60
		#Shatter skill deals normal attack after reducing opponents def, stacks 3 times max
		Stats["Skills"].append("Shatter")
		print("\nYou learned a new skill, Shatter\n")

	elif Stats["Lvl"] == 6:
		Stats["Atk"] = 18
		Stats["Def"] = 11
		Stats["Stam"] = 5
		Stats["Health"] = 80
		#Grapple does an attack selection ignoring the opponents input and dealing stamina damage instead of health
		Stats["Skills"].append("Grapple")
		print("\nYou learned a new skill, Grapple\n")

	elif Stats["Lvl"] == 7:
		Stats["Atk"] = 22
		Stats["Def"] = 14
		Stats["Stam"] = 6
		Stats["Health"] = 100
		#Flurry uses 3-5 attacks in one turn, consequently 3-5 stamina lots however.
		Stats["Skills"].append("Flurry")
		print("\nYou learned a new skill, Flurry\n")

	elif Stats["Lvl"] == 8:
		Stats["Atk"] = 28
		Stats["Def"] = 18       
		Stats["Stam"] = 8
		Stats["Health"] = 135
		#Atemi forces the opponent into its largest attack, and redirects it onto its self.
		Stats["Skills"].append("Atemi")
		print("\nYou learned a new skill, Atemi\n")
	return(Stats)





def swordCheckLvl(Stats, curHealth, curStam, StamBar):
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
	sToLevel = Stats["Point"] - Stats["Exp"]                
	LvlNow = Stats["Lvl"]
	if LvlPre != LvlNow:
		print("\nCongratulations! Leveled up\n")
		if Stats["Lvl"]==2:
			Stats["Point"]=100
		elif Stats["Lvl"]==3:
			Stats["Point"]=150
		elif Stats["Lvl"]==4:
			Stats["Point"]=250
		elif Stats["Lvl"]==5:
			Stats["Point"]=400
		elif Stats["Lvl"]==6:
			Stats["Point"]=600
		else:
			Stats["Lvl"]=7
			Stats["Point"]=1000
		sToLevel = Stats["ExpPoint"] - Stats["Exp"]
		print("\nExp to next level: " + str(sToLevel) + "\n")
		swordNewStats(Stats)
		printStatus(Stats, curHealth, curStam, StamBar)
	else:
		print("\nExp to next level: " + str(sToLevel) + "\n")
	return(Stats)





def swordNewStats(Stats):
	if Stats["Lvl"] == 2:
		Stats["Atk"] = 18
		Stats["Def"] = 10
		Stats["Stam"] = 4
		Stats["Health"] = 50
		#Datotsu skill is a 2 handed overhead strike that deals 1.5* normal attack damage
		Stats["Skills"].append("Datotsu")
		print("\nYou learned a new skill, Datotsu\n")
	elif Stats["Lvl"] == 3:
		Stats["Atk"] = 27
		Stats["Def"] = 14
		Stats["Stam"] = 4
		Stats["Health"] = 60
		#Haya-suburi skill evades the opponents attack and deals out one attack damage
		Stats["Skills"].append("Haya-suburi")
		print("\nYou learned a new skill, Haya-Suburi\n")
	elif Stats["Lvl"] == 4:
		Stats["Atk"] = 36
		Stats["Def"] = 19
		Stats["Stam"] = 4
		Stats["Health"] = 80
		#Mokuso restores 3* stam return
		Stats["Skills"].append("Mokuso")
		print("\nYou learned a new skill, Mokuso\n")
	elif Stats["Lvl"] == 5:
		Stats["Atk"] = 45
		Stats["Def"] = 24
		Stats["Stam"] = 5
		Stats["Health"] = 100
		#pierce skill is normal attack ignoring opponent defense
		Stats["Skills"].append("Pierce")
		print("\nYou learned a new skill, Pierce\n")
	elif Stats["Lvl"] == 6:
		Stats["Atk"] = 54
		Stats["Def"] = 32
		Stats["Stam"] = 7
		Stats["Health"] = 130
		#Drain skill uses blades magic to sap the opponents stamina
		Stats["Skills"].append("Drain")
		print("\nYou learned a new skill, Drain\n")
	elif Stats["Lvl"] == 7:
		Stats["Atk"] = 66
		Stats["Def"] = 42
		Stats["Stam"] = 9
		Stats["Health"] = 160
		#Regenerate uses sword magic to heal self
		Stats["Skills"].append("Regenerate")
		print("\nYou learned a new skill, Regenerate\n")
	elif Stats["Lvl"] == 8:
		Stats["Atk"] = 84
		Stats["Def"] = 54
		Stats["Stam"] = 11
		Stats["Health"] = 200
		#Kachinuki is a multi-round choice that locks in attacks until stamina is too low to attack, 
		#and prevents health going below 1 until resolved
		Stats["Skills"].append("Kachinuki")
		print("\nYou learned a new skill, Kachinuki\n") 
	return(Stats)






def takeDamage(damage, Stats, curHealth):
	curHealth = min(max(curHealth - damage, 0), Stats["Health"])
	return(curHealth)






def fatigueStatus(fatigue, curStam, StamBar):
	curStam = min(max(curStam - fatigue, 0), StamBar)
	return(curStam)





def maidenEncounter(Stats, curHealth, curStam, StamBar):
	global usedMaiden
	usedMaiden = True
	curHealth = min(max(curHealth + (Stats["Health"]), 0), Stats["Health"])
	curStam = min(max(curStam + StamBar, 0), StamBar)
	printStatus(Stats, curHealth, curStam, StamBar)
	return(curHealth, curStam)





def restRecovery(Stats, curHealth, curStam, StamBar):
	curHealth = min(max(curHealth + (Stats["Health"]/2), 0), Stats["Health"])
	curStam = min(max(curStam + (StamBar/2), 0), StamBar)
	printStatus(Stats, curHealth, curStam, StamBar)
	return(curHealth, curStam)





#Map discovery
def printEnvironment(Map, showMap, curY, curX, lastRow, lastCol):
	showMap[str(curY)+"-"+str(curX)] = "X"
	if curX != 1:
		if curX != 2:
			if Map[curY][curX-1] == 0:
				showMap[str(curY)+"-"+str(curX-1)] = "█"
			else:
				showMap[str(curY)+"-"+str(curX-1)] = "░"
			if Map[curY][curX-1] != 0 and Map[curY][curX-2] == 0:
				showMap[str(curY)+"-"+str(curX-2)] = "█"
			elif Map[curY][curX-1] != 0 and Map[curY][curX-2] != 0:
				showMap[str(curY)+"-"+str(curX-2)] = "░"
		else:
			if Map[curY][curX-1] == 0:
				showMap[str(curY)+"-"+str(curX-1)] = "█"
			else:
				showMap[str(curY-1)+"-"+str(curX)] = "░"
	if curX != lastCol-1:
		if curX != lastCol-2:
				if Map[curY][curX+1] == 0:
					showMap[str(curY)+"-"+str(curX+1)] = "█"
				else:
					showMap[str(curY)+"-"+str(curX+1)] = "░"
				if Map[curY][curX+1] != 0 and Map[curY][curX+2] == 0:
					showMap[str(curY)+"-"+str(curX+2)] = "█"
				elif Map[curY][curX+1] != 0 and Map[curY][curX+2] != 0:
					showMap[str(curY)+"-"+str(curX+2)] = "░"
		else:
			if Map[curY][curX+1] == 0:
				showMap[str(curY)+"-"+str(curX+1)] = "█"
			else:
				showMap[str(curY-1)+"-"+str(curX)] = "░"
	if curY != 1:
		if curY != 2:
			if Map[curY-1][curX] == 0:
				showMap[str(curY-1)+"-"+str(curX)] = "█"
			else:
				showMap[str(curY-1)+"-"+str(curX)] = "░"
			if Map[curY-1][curX] != 0 and Map[curY-2][curX] == 0:
				showMap[str(curY-2)+"-"+str(curX)] = "█"
			elif Map[curY-1][curX] != 0 and Map[curY-2][curX] != 0:
				showMap[str(curY-2)+"-"+str(curX)] = "░"
		else:
			if Map[curY-1][curX] == 0:
				showMap[str(curY-1)+"-"+str(curX)] = "█"
			else:
				showMap[str(curY-1)+"-"+str(curX)] = "░"
	if curY != lastRow-1:
		if curY != lastRow-2:
			if Map[curY+1][curX] == 0:
				showMap[str(curY+1)+"-"+str(curX)] = "█"
			else:
				showMap[str(curY+1)+"-"+str(curX)] = "░"
			if Map[curY+1][curX] != 0 and Map[curY+2][curX] == 0:
				showMap[str(curY+2)+"-"+str(curX)] = "█"
			elif Map[curY+1][curX] != 0 and Map[curY+2][curX] != 0:
				showMap[str(curY+2)+"-"+str(curX)] = "░"
		else:
			if Map[curY+1][curX] == 0:
				showMap[str(curY+1)+"-"+str(curX)] = "█"
			else:
				showMap[str(curY+1)+"-"+str(curX)] = "░"
	if curX != 1 and curY != 1:
		if Map[curY-1][curX] != 0 or Map[curY][curX-1] != 0:
			if Map[curY-1][curX-1] == 0:
				showMap[str(curY-1)+"-"+str(curX-1)] = "█"
			else:
				showMap[str(curY-1)+"-"+str(curX-1)] = "░"
	if curX != lastCol-1 and curY != 1:
		if Map[curY-1][curX] != 0 or Map[curY][curX+1] != 0:
			if Map[curY-1][curX+1] == 0:
				showMap[str(curY-1)+"-"+str(curX+1)] = "█"
			else:
				showMap[str(curY-1)+"-"+str(curX+1)] = "░"
	if curX != lastCol-1 and curY != lastRow-1:
		if Map[curY+1][curX] != 0 or Map[curY][curX+1] != 0:
			if Map[curY+1][curX+1] == 0:
				showMap[str(curY+1)+"-"+str(curX+1)] = "█"
			else:
				showMap[str(curY+1)+"-"+str(curX+1)] = "░"
	if curX != 1 and curY != lastRow-1:
		if Map[curY+1][curX] != 0 or Map[curY][curX-1] != 0:
			if Map[curY+1][curX-1] == 0:
				showMap[str(curY+1)+"-"+str(curX-1)] = "█"
			else:
				showMap[str(curY+1)+"-"+str(curX-1)] = "░"
	return(showMap)







#Encounter functions
def map2(Stats, curHealth, curStam, StamBar, hasSword, disillusioned):
	#Map information
	map2 = [[1, 1, 0, 1, 0, 1, 1, 1, 1],
		[0, 0, 1, 0, 1, 0, 1, 0, 0],
		[0, 1, 0, 1, 1, 1, 0, 1, 0],
		[1, 0, 1, 1, 1, 1, 5, 0, 1],
		[0, 1, 0, 1, 3, 1, 0, 1, 0],
		[0, 0, 1, 0, 1, 0, 1, 0, 0],
		[0, 0, 1, 0, 4, 0, 1, 0, 0],
		[0, 0, 1, 0, 1, 0, 1, 0, 0],
		[0, 0, 1, 0, 1, 0, 1, 0, 0],
		[0, 0, 1, 0, 2, 0, 1, 0, 0],
		[0, 0, 0, 1, 0, 1, 0, 0, 0]]

	shownMap = {
	"0-0": "╔",
	"0-1": "═",
	"0-2": "═",
	"0-3": "═",
	"0-4": "═",
	"0-5": "═",
	"0-6": "═",
	"0-7": "═",
	"0-8": "╗",
	"1-0": "║",
	"1-1": " ",
	"1-2": " ",
	"1-3": " ",
	"1-4": " ",
	"1-5": " ",
	"1-6": " ",
	"1-7": " ",
	"1-8": "║",
	"2-0": "║",
	"2-1": " ",
	"2-2": " ",
	"2-3": " ",
	"2-4": " ",
	"2-5": " ",
	"2-6": " ",
	"2-7": " ",
	"2-8": "║",
	"3-0": "║",
	"3-1": " ",
	"3-2": " ",
	"3-3": " ",
	"3-4": " ",
	"3-5": " ",
	"3-6": " ",
	"3-7": " ",
	"3-8": "║",
	"4-0": "║",
	"4-1": " ",
	"4-2": " ",
	"4-3": " ",
	"4-4": " ",
	"4-5": " ",
	"4-6": " ",
	"4-7": " ",
	"4-8": "║",
	"5-0": "║",
	"5-1": " ",
	"5-2": " ",
	"5-3": " ",
	"5-4": " ",
	"5-5": " ",
	"5-6": " ",
	"5-7": " ",
	"5-8": "║",
	"6-0": "║",
	"6-1": " ",
	"6-2": " ",
	"6-3": " ",
	"6-4": " ",
	"6-5": " ",
	"6-6": " ",
	"6-7": " ",
	"6-8": "║",
	"7-0": "║",
	"7-1": " ",
	"7-2": " ",
	"7-3": " ",
	"7-4": " ",
	"7-5": " ",
	"7-6": " ",
	"7-7": " ",
	"7-8": "║",
	"8-0": "║",
	"8-1": " ",
	"8-2": " ",
	"8-3": " ",
	"8-4": " ",
	"8-5": " ",
	"8-6": " ",
	"8-7": " ",
	"8-8": "║",
	"9-0": "║",
	"9-1": " ",
	"9-2": " ",
	"9-3": " ",
	"9-4": " ",
	"9-5": " ",
	"9-6": " ",
	"9-7": " ",
	"9-8": "║",
	"10-0": "╚",
	"10-1": "═",
	"10-2": "═",
	"10-3": "═",
	"10-4": "═",
	"10-5": "═",
	"10-6": "═",
	"10-7": "═",
	"10-8": "╝",
	}

	curY = 7
	curX = 4
	curPos = map2[curY][curX]
	lastRow = 10
	lastCol = 8

	if disillusioned == True:
		stuff
	elif hasSword == True:
		stuff
	else:
		stuff

	print("You wake up alone in a cave system wearing only a shredded up cheap tunic. Looking around, you see a narrow passageway in front and behind you. From behind you theres a constant low ringing sound but you can only make out a caved in wall of rocks, in front of you is a silent and empty, dark passgeway.\n\n")
	while curY != 1 or curX != 4:
		shownMap = printEnvironment(map2, shownMap, curY, curX, lastRow, lastCol)
		print("\n\n"+shownMap["0-0"]+shownMap["0-1"]+shownMap["0-2"]+shownMap["0-3"]+shownMap["0-4"]+shownMap["0-5"]+shownMap["0-6"]+shownMap["0-7"]+shownMap["0-8"]+"\n"+shownMap["1-0"]+shownMap["1-1"]+shownMap["1-2"]+shownMap["1-3"]+shownMap["1-4"]+shownMap["1-5"]+shownMap["1-6"]+shownMap["1-7"]+shownMap["1-8"]+"\n"+shownMap["2-0"]+shownMap["2-1"]+shownMap["2-2"]+shownMap["2-3"]+shownMap["2-4"]+shownMap["2-5"]+shownMap["2-6"]+shownMap["2-7"]+shownMap["2-8"]+"\n"+shownMap["3-0"]+shownMap["3-1"]+shownMap["3-2"]+shownMap["3-3"]+shownMap["3-4"]+shownMap["3-5"]+shownMap["3-6"]+shownMap["3-7"]+shownMap["3-8"]+"\n"+shownMap["4-0"]+shownMap["4-1"]+shownMap["4-2"]+shownMap["4-3"]+shownMap["4-4"]+shownMap["4-5"]+shownMap["4-6"]+shownMap["4-7"]+shownMap["4-8"]+"\n"+shownMap["5-0"]+shownMap["5-1"]+shownMap["5-2"]+shownMap["5-3"]+shownMap["5-4"]+shownMap["5-5"]+shownMap["5-6"]+shownMap["5-7"]+shownMap["5-8"]+"\n"+shownMap["6-0"]+shownMap["6-1"]+shownMap["6-2"]+shownMap["6-3"]+shownMap["6-4"]+shownMap["6-5"]+shownMap["6-6"]+shownMap["6-7"]+shownMap["6-8"]+"\n"+shownMap["7-0"]+shownMap["7-1"]+shownMap["7-2"]+shownMap["7-3"]+shownMap["7-4"]+shownMap["7-5"]+shownMap["7-6"]+shownMap["7-7"]+shownMap["7-8"]+"\n"+shownMap["8-0"]+shownMap["8-1"]+shownMap["8-2"]+shownMap["8-3"]+shownMap["8-4"]+shownMap["8-5"]+shownMap["8-6"]+shownMap["8-7"]+shownMap["8-8"]+"\n"+shownMap["9-0"]+shownMap["9-1"]+shownMap["9-2"]+shownMap["9-3"]+shownMap["9-4"]+shownMap["9-5"]+shownMap["9-6"]+shownMap["9-7"]+shownMap["9-8"]+"\n"+shownMap["10-0"]+shownMap["10-1"]+shownMap["10-2"]+shownMap["10-3"]+shownMap["10-4"]+shownMap["10-5"]+shownMap["10-6"]+shownMap["10-7"]+shownMap["10-8"]+"\n\n")
		move = input("move up, down, right, or left?\n\n8.) Up\n6.) Right\n4.) Left\n2.) Down\n\n")
		if move == "2":
			if curY == lastRow-1 or map2[curY+1][curX] == 0:
				print("\nCannot move down")
			elif map2[curY+1][curX] == 1:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY+=1
			elif map2[curY+1][curX] == 2:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY+=1
				(Stats, curHealth, curStam, StamBar, hasSword) = digStart(Stats, curHealth, curStam, StamBar, hasSword)
			elif map2[curY+1][curX] == 3:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY+=1
			elif map2[curY+1][curX] == 4:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY+=1
				if ratKilled == True and disillusioned == True:
					print("Cautiously sneaking past the burrow the rat emerged from earlier you notice the corpse of the rat looks much less feral than before, almost friendly and well groomed.... ")
					seenDisillusionedRat = True
		elif move == "8":
			if curY == 1 or map2[curY-1][curX] == 0:
				print("\nCannot move up")
			elif map2[curY-1][curX] == 1:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY-=1 
			elif map2[curY-1][curX] == 3:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY-=1
				if hasSword == False:
					(Stats, curHealth, curStam, StamBar) = clearingIllusions(Stats, curHealth, curStam, StamBar)
					enteredClearing = True
				else:
					(Stats, curHealth, curStam, StamBar) = clearingNoIllusions(Stats, curHealth, curStam, StamBar)
					enteredClearing = True
			elif map2[curY-1][curX] == 4:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY-=1
				if ratKilled == False and hasSword == False:
					(Stats, curHealth, curStam, StamBar) = ratFight(Stats, curHealth, curStam, StamBar)
					ratKilled = True
				elif ratKilled == False and hasSword == True and metNoIllusionRats == False:
					print("Along the way you see a burrow in the cavern wall and a family of immense rats with smooth sleek coats of fur. As intimidating as these large creatures may be they seem friendly enough and they let you pass freely.")                                 
					metNoIllusionRats = True                
		elif move == "6":
			if curX == lastCol-1 or map2[curY][curX+1] == 0:
				print("\nCannot move right.")
			elif map2[curY][curX+1] == 1:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curX+=1
			elif map2[curY][curX+1] == 5:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curX+=1
				if hasSword == True:
					print("This waters gross..")
				if acceptedMaiden == False and hasSword == False:
					(curHealth, curStam) = maidenEncounter(Stats, curHealth, curStam, StamBar)
		elif move == "4":
			if curX == 1 or map2[curY][curX-1] == 0:
				print("\nCannot move left")
			else:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curX-=1
		else:
			print("Please input '8' '6' '4' or '2'")
	shownMap = printEnvironment(map2, shownMap, curY, curX, lastRow, lastCol)
	print("\n\n"+shownMap["0-0"]+shownMap["0-1"]+shownMap["0-2"]+shownMap["0-3"]+shownMap["0-4"]+shownMap["0-5"]+shownMap["0-6"]+shownMap["0-7"]+shownMap["0-8"]+"\n"+shownMap["1-0"]+shownMap["1-1"]+shownMap["1-2"]+shownMap["1-3"]+shownMap["1-4"]+shownMap["1-5"]+shownMap["1-6"]+shownMap["1-7"]+shownMap["1-8"]+"\n"+shownMap["2-0"]+shownMap["2-1"]+shownMap["2-2"]+shownMap["2-3"]+shownMap["2-4"]+shownMap["2-5"]+shownMap["2-6"]+shownMap["2-7"]+shownMap["2-8"]+"\n"+shownMap["3-0"]+shownMap["3-1"]+shownMap["3-2"]+shownMap["3-3"]+shownMap["3-4"]+shownMap["3-5"]+shownMap["3-6"]+shownMap["3-7"]+shownMap["3-8"]+"\n"+shownMap["4-0"]+shownMap["4-1"]+shownMap["4-2"]+shownMap["4-3"]+shownMap["4-4"]+shownMap["4-5"]+shownMap["4-6"]+shownMap["4-7"]+shownMap["4-8"]+"\n"+shownMap["5-0"]+shownMap["5-1"]+shownMap["5-2"]+shownMap["5-3"]+shownMap["5-4"]+shownMap["5-5"]+shownMap["5-6"]+shownMap["5-7"]+shownMap["5-8"]+"\n"+shownMap["6-0"]+shownMap["6-1"]+shownMap["6-2"]+shownMap["6-3"]+shownMap["6-4"]+shownMap["6-5"]+shownMap["6-6"]+shownMap["6-7"]+shownMap["6-8"]+"\n"+shownMap["7-0"]+shownMap["7-1"]+shownMap["7-2"]+shownMap["7-3"]+shownMap["7-4"]+shownMap["7-5"]+shownMap["7-6"]+shownMap["7-7"]+shownMap["7-8"]+"\n"+shownMap["8-0"]+shownMap["8-1"]+shownMap["8-2"]+shownMap["8-3"]+shownMap["8-4"]+shownMap["8-5"]+shownMap["8-6"]+shownMap["8-7"]+shownMap["8-8"]+"\n"+shownMap["9-0"]+shownMap["9-1"]+shownMap["9-2"]+shownMap["9-3"]+shownMap["9-4"]+shownMap["9-5"]+shownMap["9-6"]+shownMap["9-7"]+shownMap["9-8"]+"\n"+shownMap["10-0"]+shownMap["10-1"]+shownMap["10-2"]+shownMap["10-3"]+shownMap["10-4"]+shownMap["10-5"]+shownMap["10-6"]+shownMap["10-7"]+shownMap["10-8"]+"\n\n")
	map3(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)





def clearingIllusions(Stats, curHealth, curStam, StamBar, hasSword, disillusioned):
	
	loop = 0
	move=input("\n\nYou quickly shuffle forward to get distance from the burrow fearful there may be more creatures yet inside. Your body rings out in agonizing pain missing chunks of flesh and losing blood fast but still you progress. Ahead you see a blinding light amidst the darkness. When you cross into the light and your vision adjusts you a see a spacious circular room with the narrow pathway you came from behind you and another similar continuation on the other side of the room. The right side of the floor seems to be all water and lining the of the wall rather than cavern walls of rock is a glistening polished white marble with an occasional lit torch along it. In front of the center of the wall amidst the bath stands a life sized marble statue of young maiden shedding a single tear. As you lock eyes with the statue you feel a strong urge to get into the water and the intensity of the pain you feel from each of your wounds increases immensely more and more each second. Peel away from the statues gaze and move on in the caverns or accept its call and join it in the waters?\n\n8.) Peel away\n6.) Accept\n\n")  
	while loop == 0:
			if move == "6":
				loop+=1
				print("\nAs you step into the water you can see the single tear on the maiden change form from stone to liquid and drip into the water. The water begins to feel warmer and you notice a slight shimmer along the surface. Suddenly the water bursts into a glaring golden color and rises up around you, encapsualting you in it. At first you struggle against the water in fear of drowning but as you flail around you see that your wounds are closing up and as though you've never endured a hardship in your life. You give in to the comforting aura and let out a gasp to find you can still breathe.\n")
				(curHealth, curStam) = maidenEncounter(Stats, curHealth, curStam, StamBar) 
				print("\nThe shimmering gold color settles and slowly fades in the water around you and soon it all falls to the pool again beneath you. Suddenly two torches flare up on either side of the entrance to the narrow passageway across from where you entered this opening. You glance back to the statue of the maiden and see that it has changed and she is smiling sweetly now instead of crying, and holds an arm up pointing to the passageway. You take hold of the meaning and venture forth into the cavern again.\n")
				map2(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)
			elif move == "8":
				loop+=1
				print("\nYou peel your eyes away from the maidens and step back, suddenly you feel a horrendous stinging pain all across your body and you're certain it isn't from your existing wounds. You fumble in agony and lose your footing until you collapse against the wall opposite the pool of water, when you open your eyes and glance back at the pool the maiden statue appears different. She now has an arm raised pointing at you, and the other into the waters with a stern frown and sharp eyes.\n")
				curHealth = takeDamage(2, Stats, curHealth)
				print("\nThe stinging pain running along your skin takes its toll, your health drops to ",curHealth,"\n")
				if TeroCurrentHealth < 1:
					print("\nYour body goes limp and your vision fades away. The lashing pain you suddenly felt untop added to your existing wounds proved fatal.\n")
					SystemExit()
				move = input("Do you accept the demand or ignore it?\n\n8.) Ignore\n6.) Accept\n\n")
				while loop == 1:
					if move == "6":
						print("\nFearfully you crawl to the waters, roll yourself in, and sink down. You feel your wounds and pain fading from your body, the holes of flesh bitten off of you sealing up. Lifelessly you lay at the bottom of the pool, but as the last of your wounds seals itself and you still lie there the water itself surges and throws you beside the pools edge. After a fit of coughing for a moment you look up and see that again the statue has changed and now stands hands down and cupped together, face directed at the passage way youve yet ventured in with a beaming smile. Torches on either side of the entrance flare up and you collect yourself and venture into it hesitantly taking glances at the statue behind you.\n")
						loop+=1
						(Stats, curHealth, curStam, StamBar) = maidenEncounter(Stats, curHealth, curStam, StamBar)
						map2(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)
					elif move == "8":
						loop+=1
						print("\nThe stinging pain you felt before intensifies to what can only be described as the most horrendously agonizing sensation you've ever felt in your life. Were you to lacerate your own body along every inch of it, douse yourself with a batch of a citrusy liquid, and then light yourself ablaze, even still it could not compare the pain ringing out across your entire body. You freeze in place, the pain so great your brain entirely shut down to protect you from going insane. While your mind is blacked out from reality your consciousness drifts into a vision like a sort of dream. You see a family around a table, amongst them is an individual that resembles yourself, perhaps more groomed in appearance with a little more fat on your build and slightly less aged but it's certainly the same face you saw looking back in the pond before. The whole family seems to be enjoying themself bantering and sharing a moment together yet everytime theres a lull you can read an expression of terror across their faces. You hear a knocking at the door a few meters from the table and see everyones face freeze up besides your own look alike. They push their seat away from the table, stand, and walk to another room within the small home before returning with a sword tucked into a scabbard and held down into it with chains. Before they open the door they pull on the handle as if to draw the blade and although the chains prevent that it does partially click out of the scabbard and reveal a shimmering silver blade that resonates out a calming ringing sound. They stare for a moment then click it back in and opens the front door, through which you view a gathering of men with black cloaks, silver garnished, with a bright silver mask. The apparent leader of the group stands ahead of the others, adorned with even more silver decorations along their cloak and mask, and gestures your double to join them. After they do, the leader extends his arms out infront of himself and peers at the blade they hold. They clench their fist and grimace, but still lay the blade across the leaders arms, after which the others form a circle around them and start walking away and the leader peers in on the family for a while before shutting the door. The family all hurriedly clusters together and seem to be grieving in eachothers arms... As you wonder why?, what happened to your lookalike?, who were those cloaked people? and so many more questions you start to come back into reality and scream out at the pain across your body. It's died down and is no longer even a fraction of what it had been but still the pain is agonizing and your snaps out of the dreamlike sight you had viewed before and the memory of it becomes fuzzy. You recollect yourself mentally and stand shakily, before lies the pond full of black waters with the statue showing an incredibly angered face directed at you. To your right is the passage you came from, and as you peer into its darkness you hear the same faint ringing you heard before. To your left the passageway you've yet to venture into, silent and dark as the abyss.\n")
						curHealth = takeDamage(4, Stats, curHealth)
						print("\nThe agonizing pain ringing across your body finally comes to a stop but it's certainly left its mark, your health falls to ",curHealth,"\n")
						if TeroCurrentHealth < 1:
							print("\nYour vision starts to go fuzzy and fade out and your body goes limp. For a moment you think you are going to see more of this dreamscape you peered into before, however you quickly come to terms with the fact that this is not the case but rather your life itself is coming to an end.\n")
							SystemExit()
						disillusioned = True
						move = input("Do you finally embrace the waters, or leave it?\n\n8.) Embrace\n6.) leave\n\n")
						while loop == 2:
							if move == "8":
								loop+=1
								print("\nYou wade into the black waters and watch as a shadowy mist wraps around the statue and change its appearance to a beaming smile and holding it's hands up and together like in prayer. The water wraps around your body and all of your wounds and your fatigue are cured, you can see where your wounds had been is a flowing black fluid joining and mixing into the lighter black water. When you're fully recovered the water falls back into the pool splashing around you and again you see a shadowy mist wrap around the statue and change it to be looking fondly at the passageway you haven't traversed through and pointing an arm to it.\n")
								(Stats, curHealth, curStam, StamBar) = maidenEncounter(Stats, curHealth, curStam, StamBar)
								map2(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)
							elif move == "6":
								loop+=1
								print("\nCurious about the ringing noise you've been hearing you consider heading back to where you came from and following the noise.\n\n")
								return(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)
							else:
								move = input("please answer '8' or '6'\n\n") 
					else:
						move = input("Please answer '8' or '6'\n\n")
			else:
				move = input("Please answer '8' or '6'\n\n")





def clearingNoIllusions(Stats, curHealth, curStam, StamBar, hasSword, disillusioned):
	#status for Shadow
	ShadowStats = {
	"Atk": 12,
	"Def": 4,
	"Stam": 4.5,
	"Health": 60,
	}

	ShadowStamBar = ShadowStats["Stam"]*10
	ShadowCurrentStam = ShadowStamBar
	ShadowCurrentHealth = ShadowStats["Health"]

	global firstMaidenDead
	firstMaidenFought = False

	print("\nYou venture into the passage the other direction. Along the way you see a burrow in the cavern wall and a family of immense rats with smooth sleek coats of fur. As intimidating as these large creatures may be they seem friendly enough and they let you pass freely. Further beyond you come into a spacious clearing between the passage you came from and another ahead of you. On the right half of the cave wall is a pool lined with marble, filled with black eerie waters, and at the far end of it is a shadowy figure shaped sort of like a woman with horns. As you notice this creature you close your grip around your sword tighter and stare, and the shadow breaks the stand still in the room with an angry shriek and the water around her stirs up.\n")
	print(combatTutorial)
	statProgress(ShadowCurrentHealth, ShadowCurrentStam, curHealth, curStam)
	while ShadowCurrentHealth > 35 and curHealth > 0:
		choice = input("\nThe waters whirl in unnatural patterns and the shadow cackles maniacally, what will you do?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n\n")
		if choice == "6":
			if ShadowCurrentStam >= 8:
				curHealth = takeDamage(((ShadowStats["Atk"] - Stats["Def"])//2), Stats, curHealth)
				ShadowCurrentStam = fatigueStatus((8-ShadowStats["Stam"]), ShadowCurrentStam, ShadowStamBar)
				curStam = fatigueStatus(-Stats["Stam"], curStam, StamBar)
				statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
			else:
				print("\nThe shadowy figure envelopes its lower half in the murky waters and hisses.\n")
				ShadowCurrentStam = fatigueStatus(-2*ShadowStats["Stam"], ShadowCurrentStam, ShadowStamBar)
				statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
		elif choice == "8":
			if curStam >= 8:
				ShadowCurrentHealth = takeDamage(Stats["Atk"] - Stats["Def"], ShadowStats, ShadowCurrentHealth)
				curStam = fatigueStatus(8-Stats["Stam"], curStam, StamBar)
				if ShadowCurrentStam >= 8:
					curHealth = takeDamage(ShadowStats["Atk"] - Stats["Def"], Stats, curHealth)
					ShadowCurrentStam = fatigueStatus(8-ShadowStats["Stam"], ShadowCurrentStam, ShadowStamBar)
					statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
				else:
					print("\nThe shadow writhes in place trying to dodge your blade, but is held still by the waters wrapped around it.\n")
					ShadowCurrentStam = fatigueStatus(-ShadowStats["Stam"]*2, ShadowCurrentStam, ShadowStamBar)
					statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
			else:
				print("\nYou are too fatigued to attack\n")
		elif choice == "4":
			if curStam >= (StamBar-4):
				print("\nYou've no need to rest now.\n")
			else:
				curStam = fatigueStatus(-2*Stats["Stam"], curStam, StamBar)
				if ShadowCurrentStam >= 8:
					curHealth = takeDamage(ShadowStats["Atk"] - Stats["Def"], Stats, curHealth)
					ShadowCurrentStam = fatigueStatus(8-ShadowStats["Stam"], ShadowCurrentStam, ShadowStamBar)
					statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
				else:
					print("\nThe shadow rapidly twirls and lowers itself within a bubble of the murky water, leaving only its eyes over the water keeping you in sight while you catch your breath.\n")
					ShadowCurrentStam = fatigueStatus(-2*ShadowStats["Stam"], ShadowCurrentStam, ShadowStamBar)
					statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
		elif choice == "2":
			print("\nYou haven't learned any skills yet.\n")
		else:
			choice = input("\nPlease input '8' '6' '4' or '2'")
	if curHealth <= 0:
		print("\nThe shadow cackles mockingly while dark bubbles rise from the pool and pop around her. Your vision gets hazy and you collapse.\n")
		SystemExit()



	elif ShadowCurrentHealth < 35:
		print("\nThe Shadow grabs it's horns firmly and pulls on them while screeching. All of the water rises from the floor, a large amount forming a base around the shadows legs, and the rest hovering in the air formed into something like 10 seperate giant tails. The shadow silences its screech and releases its hands down by its side and stares blankly at you for a moment.... \n\nSuddenly it raises its arms up extended towards you and its fingers start to snap out of their human like shape and extend, and you notice the tails of water move corresponding to the way it moves it's fingers. You brace yourself unsure what to do and then 4 of the tails slam into you far too fast for you to react. The tails hit you in an x pattern and form a ball around you suffocating you, in a mad flail to free yourself you slash at the waters and the sword glows bright, the water around you loses its rigid form and splashes down onto the floor dropping you onto your back.\n")
		curStam = fatigueStatus(12, curStam, StamBar)
		print("\nYour struggle wore you out, your stamina is now ", curStam, "\n")
		choice = input("\nThe tails that struck you are very slowly being pulled back into the water around the shadows legs, do you want to make a dash to try and slice away some or try to prepare to intercept an attack?\n\n8.) Dash forward\n6.) Prepare to intercept\n\n")
		while curHealth > 0 or firstMaidenFought == False:
			if choice == "6":
				print("\nyou stand firm and when a single tail is propelled towards you, you run the glowing blade through it and again watch it lose form and splash down around you.\n")
				loop = 0
				choice = input("Your plan seems to be working, continue to intercept incoming tails or go on the offensive?\n\n8.) Continue intercepting\n6.) Go on the offense\n\n")
				while loop == 0:
					if choice == "8":
						loop+=1
						print("\nYou prepare to repeat your same action and wait for a tail to launch after you. After a short moment the next tail comes flying towards you and you time your motion and start to swing. When the tail and sword are about to collide the tail suddenly buckles up to avoid the blade and two more tails slam into your sides. You cut your way out again but the force the tails slammed into you with was much higher this time and severely injured you.\n")
						curHealth = takeDamage(6, Stats, curHealth)
						print("\nyou took 6 damage, your health dropped to ", curHealth, "\n")
						if curHealth == 0:
							print("\nThe blast from the tails likely broke some ribs and caused internal bleeding. You struggle to hold yourself up but inevitably collapse. The shadow cackles softly and the tails wrap around your legs and drag you into the murky waters around its legs. Everything goes black.\n")
							SystemExit()
						else:
							while loop == 1:
								choice = input("The shadows face distorts rapidly while making a constant spastic clicking noise. With only 4 tails left it seems to be getting antsy, do you want to prepare to intercept again or charge?\n\n8.) Prepare to intercept\n6.) Charge\n\n")
								if choice == "8":
									loop+=1
									print("\nThe shadow whips its head forward and screeches, slamming the remaining 4 tails directly into you. You slash you're blade through the oncoming torrent, and find you're unable to nullify all four tails momentum at once and take a heavy blow. however, as you tumble along the ground you see the tails all collapse down.\n")
									curHealth = takeDamage(8, Stats, curHealth)
									print("\nYou took another 8 damage, your health dropped to ", curHealth, "\n")
									if curHealth == 0:
										print("\nYou see that you were able to knock out the last 4 tails, and the shadow is breaking down, however you can no longer move your body and a raging pain stings along your chest. You taste your own blood filling your mouth, and resign yourself to your fate.\n")
										SystemExit()
									else:
										print("\nThe shadow makes a sad chirping noise, then loses form and becomes nothing more than a dark mist. It slowly spreads wide infront of you, and then in an instant picks all of the waters dropped from the tails off the ground and back into itself, and bolts away like a massive arrow of water, down into the passageway you've yet to venture into. Holding your blade forth anticipating its return, you stand stoicly, yet after a long pause you decide it's likely not coming back and decide to rest and give your body a chance to recover. You slouch down against the cave wall in the clearing and take a breath. Suddenly, your blade glistens white again and cloaks you in it's aura.\n")
										firstMaidenFought == True
										Stats["Exp"] += 100
										print("\n\nYou gained 100 Exp!")
										Stats = swordCheckLvl(Stats, curHealth, curStam, StamBar)
										(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
										print("\nYou pick yourself up and head into the caverns ahead of you, blade at the ready.\n")
										map2(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)
								elif choice == "6":
									if curStam >= 20:
										loop+=1
										print("\nYou charge at a dead sprint and land the blow into the chest of the shadow itself, as you do so it reacts by slamming its tails into your back with huge force one at a time\n")
										curStam = fatigueStatus(20, curStam, StamBar)
										curHealth = takeDamage(8, Stats, curHealth)
										if curHealth == 0:
											print("\nyo\n")
											SystemExit()
										else:
											firstMaidenDead = True
											firstMaidenFought = True
											print(", but you hold firm and run the blade through the shadow to the hilt. To your surprise the white aura the sowrd let off earlier surrounds the shadow and then chages sensation from its calm serene feeling to one of a divine, awe inspiring, being casting judgement down on a child that lost its's way. The aura burned angrily and the shadow bellowed in screams, not like the screeches before but truly screams of horror and fear. The shadow slowly ceased to be and as it burned away and shriveled the aura shrank around it until it only wrapped around the blade again and the shadow was entirely gone. The waters collapsed into the pool once more and a black mist rose from it and into the blade, transforming to the white glow of the blade itself, and the pool beneath turned in color to be normal everyday waters.\n")
											Stats["Exp"] += 250
											print("\n\nYou've gained 250 Exp!!")
											Stats = swordCheckLvl(Stats, curHealth, curStam, StamBar)
											print("\nYour heart pounding, body shaking from both exhaustion and internal damage, you collapse face first into the pool of now cleansed waters. You think to yourself for a moment, 'am I going to die here like this? after everything!?' face under water unable to move your body. As you run out of breath, you nearly let the blade slip from your hand and drift away, but before it does the same white aura envelopes you and you feel it mending your body.\n")
											(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
											print("\nAble to move your limbs once more you lift yourself out from the pool of water and gasp for air. after a moment to catch your breath you glance at the passage you've yet to travel down and the blade at your side intensifies its ringing sound. You feel strangely indebted to this sword and accept its desire. You pick yourself up and start to venture down the passageway.\n")
											map2(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)
									elif curStam >= 12:
										loop+=1
										print("\nYou pause for just a moment and as a tail slams forth with great speed, you run under it and charge at the shadow. Before you can reach all the way to it the other tails curl in front of the shadow to protect it. You slash through all 3 successfully, but immediately get slammed in the back by the last tail. Having the wind knocked out of you, you struggle to get back to your feet and the shadow cackles and twirls its last tail over your head.\n")
										curStam = fatigueStatus(12, curStam, StamBar)
										curHealth = takeDamage(6, Stats, curHealth)
										print("\nYou took 6 damage, and lost 12 stamina. Your health is now: ", curHealth, " and your stamina is now: ", curStam, "\n")
										if curHealth == 0:
											print("\nYour consciousness fades out as you're continuosly wailed on by the last tail, the force rippling waves in the shallow pool of water around you.\n")
											SystemExit()
										else:
											choice = input("You know you need to move before that tail hanging over head strikes again, and you know you're in a vulnerable position, but you struggle to move at all let alone quickly. You quickly run some ideas through your mind and realize you have limited options. You could try rolling over and swinging your blade along the way in a wide arc to try and take out the last tail, you could try and get a footing and quickly spring forward to stab into the shadow, or you could try to quickly spring backwards and prepare to defend yourself, what will you do?\n\n8.) Roll\n6.) Stab\n4.) Spring backwards\n\n")
											while loop == 2:
												if choice == "8":
													loop+=1
													print("\nYou tuck the blade in against your side, and slowly get your arm into a stiff straight position. Then, swiftly and simultaneously you push your arm out perpendicular to your body and roll letting your body weight drag your arm across with you in an arc. You successfully take out the last tail, but now lay flat on your back, sword at a full arms distance from your abdomen, with the shadow looming over you a mere foot or so away. You should be in mortal danger, yet the shadow has lost it's own composure and is stumbling back whilst screeching. Suddenly it reaccumulates all the waters fallen from the tails into itself, losing its humanoid form, and then bolts away as a mass of black liquid. You take the opportunity to stand and brace for it's return, but several moments pass with no further action. You cautiously decide to lower your guard and take a chance to rest.\n")
													print("\n\nYou gained 100 exp!")
													Stats["Exp"]+=100
													Stats = swordCheckLvl(Stats, curHealth, curStam, StamBar)
													(curHealth, curStam) = swordRestRecovery(Stats, curHealth, curStam, StamBar)
												elif choice == "6":
													loop+=1
													print("\nYou take your time to position your footing and joints to make one swift push forward and stab into the shadow without alerting the shadow itself. \nYO\n \n")
												elif choice == "4":
													loop+=1
													print("\nyo\n")
												else:
													choice = input("Please input '8', '6', or '4'\n\n")
									else:
										choice = input("It seems you're too fatigued to make the attack, you'll only be able to intercept, please try again.\n\n")
								else:
									choice = input("Please input '8' or '6'\n\n")
					elif choice == "6":
						loop+=1
						print("\nyo\n")

					else:
						choice = input("Please input '8' or '6'\n\n")
			elif choice == "8":
				loop+=1
				print("\nyo\n")

			else:
				choice = input("Please input '8' or '6'\n\n")





def ratFight(Stats, curHealth, curStam, StamBar):
	#Rat Stats
	RatStats = {
	"Atk": 6,
	"Def": 2,
	"Stam": 1.5,
	"Health": 20,
	}
	RatStamBar = RatStats["Stam"]*10
	RatCurrentStam = RatStamBar
	RatCurrentHealth = RatStats["Health"]

	print("\nAs you walk along the passageway you notice a large hole near the ground ahead on your right side. You cautiously approach and peer in but can't see anything but darkness. You begin to walk along your path again, but short after feel a sudden chill. Nervously you peer slowly over your shoulder and spot a shadow a couple feet long, and it begins to snarl back at you. As it approaches to strike you get a more clear picture, it is an immense rat with tufts of fur missing and jagged teeth. In this cavern you don't think you'll be able to outrun it and fearfully prepare to fight for your life.\n\n")
	print(combatTutorial)
	statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
	while RatCurrentHealth > 0 and curHealth > 0:
		choice = input("The rat is gnarling viciously, what action will you take?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n\n")
		if choice == "6":
			if RatCurrentStam >= 6:
				curHealth = takeDamage(((RatStats["Atk"] - Stats["Def"])//2), Stats, curHealth)
				RatCurrentStam = fatigueStatus((6-RatStats["Stam"]), RatCurrentStam, RatStamBar)
				curStam = fatigueStatus(-Stats["Stam"], curStam, StamBar)
				statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
			else:
				print("\nThe rat is busy panting and doesn't attack\n")
				RatCurrentStam = fatigueStatus(-2*RatStats["Stam"], RatCurrentStam, RatStamBar)
				curStam = fatigueStatus(-Stats["Stam"], curStam, StamBar)
				statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
		elif choice == "8":
			if curStam >= 6:
				RatCurrentHealth = takeDamage((Stats["Atk"] - RatStats["Def"]), RatStats, RatCurrentHealth)
				curStam = fatigueStatus((6-Stats["Stam"]), curStam, StamBar)
				if RatCurrentStam >= 6:
					curHealth = takeDamage(RatStats["Atk"] - Stats["Def"], Stats, curHealth)
					RatCurrentStam = fatigueStatus((6-RatStats["Stam"]), RatCurrentStam, RatStamBar)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
				else:
					print("\nThe rat sluggishly takes the blow\n")
					RatCurrentStam = fatigueStatus(-RatStats["Stam"]*2, RatCurrentStam, RatStamBar)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
			else:
				print("\nYou are too fatigued to attack\n")
		elif choice == "4":
			if curStam >= (StamBar-3):
				print("\nYou've no need to rest now.\n")
			else:
				curStam = fatigueStatus(-2*Stats["Stam"], curStam, Stambar)
				if RatCurrentStam >= 6:
					curHealth = takeDamage((RatStats["Atk"] - Stats["Def"]), Stats, curHealth)
					RatCurrentStam = fatigueStatus((6-RatStats["Stam"]), RatCurrentStam, RatStamBar)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
				else:
					print("\nYou both sink down and breathe heavily eyeing each other in anticipation\n")
					RatCurrentStam = fatigueStatus(-2*RatStats["Stam"], RatCurrentStam, RatStamBar)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
		elif choice == "2":
			print("\nYou haven't learned a skill yet\n")
		else:
			choice = input("\nPlease input '8' '6' '4' or '2'")
	if curHealth <= 0:
		print("\nYou feel the warmth of your own blood leaving your insides and running across your flesh. You come to terms with the fact that you died not knowing who you are or how you got to this cave, food for a feral rat creature.")
		SystemExit()
	else:
		print("\nYou're shaking from a mix of blood loss and adrenaline as you stand over the now dead rat.\n")
		Stats["Exp"] += 50
		print("\nGained 50 exp!")
		Stats = CheckLvl(Stats, curHealth, curStam, StamBar)
		return(Stats, curHealth, curStam, StamBar)


def digDisillusioned(Stats, curHealth, curStam, StamBar, hasSword):
	move = input("Making it back to where the cave seems to have given in you look at the pile of boulders and rocks, and hear that low ringing thunderously rolling out from the cracks. Do you begin digging out rocks or turn away?\n\n8.) Dig\n6.) Turn away\n\n")
	while loop == 0:
		if move == "8":
			loop+=1
			print("\nYou struggle to pull out rock after rock from the pile honing in on the origin of the sound. Your hands start to bleed and ache as you work through the rocks but it's nothing compared to the pain from the clearing earlier and you keep digging through. The ringing becomes higher and higher pitched as you remove more rocks around it and eventually you see a couple broken chain links scattered aroud and pick up your pace. Finally you unveil a shimmering silver blade and pick it out of the rubble. The ring intensifies and resonates inside of your body and mind, meanwhile the silver blade glows white brighter and brighter by the second until you can no longer see anything but white around you, and then suddenly the light fades out and the ringing stops. You look at the blade and a white sheen dances along the surface with a gentle sound resonating quietly for only a brief moment and then its nothing more than a beautifully smithed sword. Gripping the sword tightly you feel a new energy flowing through you!\n")
			Stats = swordStats
			curHealth = swordCurrentHealth
			curStam = swordCurrentStam
			StamBar = swordStamBar
			(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
			print("\nFeeling invigorated you confidently hold the glowing blade over head and move your previously sore and frail joints\n")
			hasSword = True
			return(Stats, curHealth, curStam, StamBar, hasSword)
		elif move == "6":
			print("\nListening to the resonating sound calling out for you from under the rubble you stop and decide maybe you would be better off leaving it in its place.\n")
			loop+=1
			return(Stats, curHealth, curStam, StamBar, hasSword)
		else:
			move = input("please input '8' or '6'\n\n")


def digStart(Stats, curHealth, curStam, StamBar, hasSword):
	loop = 0
	move = input("You eye up the mound of rocks and boulders and designate a few that you feel you can pull out from the weight of the others. As you start to work them out all you seem to be achieving is having more rocks come down in their place from the collapsed ceiling. Do you want to continue digging into the rocks or give up?\n\n8.) Continue digging\n6.) Give up\n\n")
	while loop == 0:
		if move == "8":
			loop+=1
			print("\nAs you peel out rocks a large rock falls down on top of you and strikes the back of your head.\n")
			curHealth = takeDamage(4, Stats, curHealth)
			print("\nYour health drops 4 points, it is now ",curHealth)
			move = input("Do you still continue or give up?\n\n8.) Continue\n6.) Give up\n\n")
			while loop == 1:
				if move == "8":
					loop+=1
					print("\nYou dig feverishly thorugh the pile and the ringing you've been hearing resonates in a higher and higher tone as you do so, several stones into the process you notice the skin wearing off of your hands rubbing them raw.\n\n")
					curHealth = takeDamage(2, Stats, curHealth)
					print("Your health drops another 2 points, it is now ",curHealth)
					move = input("Do you still continue or give up?\n\n8.) Continue\n6.) Give up\n\n")
					while loop == 2:
						if move == "8":
							loop+=1
							print("\nYou finally uncover what appears to be a brilliantly crafted shimmering blade. Hoisting it out of the heap you feel a warmth shoot out of the blade and into your hand and rippling through your body.\n")
							curHealth = swordCurrentHealth
							curStam = swordCurrentStam
							StamBar = swordStamBar
							Stats = swordStats
							hasSword = True
							(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
							return(Stats, curHealth, curStam, StamBar, hasSword)
						elif move == "6":
							loop+=1
							print("\nYou give up on trying to work through all this rubble and turn back to go through the passage way behind you.\n\n")
							return(Stats, curHealth, curStam, StamBar, hasSword)
						else:
							move = input("\nPlease input '8' or '6'.\n\n")
				elif move == "6":
					loop+=1
					print("\nYou give up on trying to work through all this rubble and turn back to go through the passage way behind you.\n\n")
					return(Stats, curHealth, curStam, StamBar, hasSword)
				else:
					move = input("Please input 'continue' or 'give up'\n\n")
		elif move == "6":
			loop+=1
			print("\nYou give up on trying to work through all this rubble and turn back to go through the passage way behind you\n\n")
			return(Stats, curHealth, curStam, StamBar, hasSword)
		else:
			move = input("Please input '8' or '6'\n\n")






def main():

	#Map information
	map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
		    [0, 0, 0, 0, 1, 0, 0, 0, 0],
		    [0, 0, 0, 1, 1, 1, 0, 0, 0],
		    [0, 0, 1, 1, 1, 1, 5, 0, 0],
		    [0, 0, 0, 1, 3, 1, 0, 0, 0],
		    [0, 0, 0, 0, 1, 0, 0, 0, 0],
		    [0, 0, 0, 0, 4, 0, 0, 0, 0],
		    [0, 0, 0, 0, 1, 0, 0, 0, 0],
		    [0, 0, 0, 0, 1, 0, 0, 0, 0],
		    [0, 0, 0, 0, 2, 0, 0, 0, 0],
		    [0, 0, 0, 0, 0, 0, 0, 0, 0]]

	shownMap = {
	"0-0": "╔",
	"0-1": "═",
	"0-2": "═",
	"0-3": "═",
	"0-4": "═",
	"0-5": "═",
	"0-6": "═",
	"0-7": "═",
	"0-8": "╗",
	"1-0": "║",
	"1-1": " ",
	"1-2": " ",
	"1-3": " ",
	"1-4": " ",
	"1-5": " ",
	"1-6": " ",
	"1-7": " ",
	"1-8": "║",
	"2-0": "║",
	"2-1": " ",
	"2-2": " ",
	"2-3": " ",
	"2-4": " ",
	"2-5": " ",
	"2-6": " ",
	"2-7": " ",
	"2-8": "║",
	"3-0": "║",
	"3-1": " ",
	"3-2": " ",
	"3-3": " ",
	"3-4": " ",
	"3-5": " ",
	"3-6": " ",
	"3-7": " ",
	"3-8": "║",
	"4-0": "║",
	"4-1": " ",
	"4-2": " ",
	"4-3": " ",
	"4-4": " ",
	"4-5": " ",
	"4-6": " ",
	"4-7": " ",
	"4-8": "║",
	"5-0": "║",
	"5-1": " ",
	"5-2": " ",
	"5-3": " ",
	"5-4": " ",
	"5-5": " ",
	"5-6": " ",
	"5-7": " ",
	"5-8": "║",
	"6-0": "║",
	"6-1": " ",
	"6-2": " ",
	"6-3": " ",
	"6-4": " ",
	"6-5": " ",
	"6-6": " ",
	"6-7": " ",
	"6-8": "║",
	"7-0": "║",
	"7-1": " ",
	"7-2": " ",
	"7-3": " ",
	"7-4": " ",
	"7-5": " ",
	"7-6": " ",
	"7-7": " ",
	"7-8": "║",
	"8-0": "║",
	"8-1": " ",
	"8-2": " ",
	"8-3": " ",
	"8-4": " ",
	"8-5": " ",
	"8-6": " ",
	"8-7": " ",
	"8-8": "║",
	"9-0": "║",
	"9-1": " ",
	"9-2": " ",
	"9-3": " ",
	"9-4": " ",
	"9-5": " ",
	"9-6": " ",
	"9-7": " ",
	"9-8": "║",
	"10-0": "╚",
	"10-1": "═",
	"10-2": "═",
	"10-3": "═",
	"10-4": "═",
	"10-5": "═",
	"10-6": "═",
	"10-7": "═",
	"10-8": "╝",
	}

	curY = 7
	curX = 4
	curPos = map1[curY][curX]
	lastRow = 10
	lastCol = 8



	#Character stats
	Stats = TeroStats
	curHealth = TeroCurrentHealth
	curStam = TeroCurrentStam
	StamBar = TeroStamBar



	#Conditionals
	global firstMaidenDead
	enteredClearing = False
	ratKilled = False
	metNoIllusionRats = False
	disillusioned = False
	seenDisillusionedRat = False
	acceptedMaiden = False
	hasSword = False
	hasDug = False
	hasDug2 = False
	seenMaidenLeave = False

	print("You wake up alone in a cave system wearing only a shredded up cheap tunic. Looking around, you see a narrow passageway in front and behind you. From behind you theres a constant low ringing sound but you can only make out a caved in wall of rocks, in front of you is a silent and empty, dark passgeway.\n\n")
	while curY != 1 or curX != 4:
		shownMap = printEnvironment(map1, shownMap, curY, curX, lastRow, lastCol)
		print("\n\n"+shownMap["0-0"]+shownMap["0-1"]+shownMap["0-2"]+shownMap["0-3"]+shownMap["0-4"]+shownMap["0-5"]+shownMap["0-6"]+shownMap["0-7"]+shownMap["0-8"]+"\n"+shownMap["1-0"]+shownMap["1-1"]+shownMap["1-2"]+shownMap["1-3"]+shownMap["1-4"]+shownMap["1-5"]+shownMap["1-6"]+shownMap["1-7"]+shownMap["1-8"]+"\n"+shownMap["2-0"]+shownMap["2-1"]+shownMap["2-2"]+shownMap["2-3"]+shownMap["2-4"]+shownMap["2-5"]+shownMap["2-6"]+shownMap["2-7"]+shownMap["2-8"]+"\n"+shownMap["3-0"]+shownMap["3-1"]+shownMap["3-2"]+shownMap["3-3"]+shownMap["3-4"]+shownMap["3-5"]+shownMap["3-6"]+shownMap["3-7"]+shownMap["3-8"]+"\n"+shownMap["4-0"]+shownMap["4-1"]+shownMap["4-2"]+shownMap["4-3"]+shownMap["4-4"]+shownMap["4-5"]+shownMap["4-6"]+shownMap["4-7"]+shownMap["4-8"]+"\n"+shownMap["5-0"]+shownMap["5-1"]+shownMap["5-2"]+shownMap["5-3"]+shownMap["5-4"]+shownMap["5-5"]+shownMap["5-6"]+shownMap["5-7"]+shownMap["5-8"]+"\n"+shownMap["6-0"]+shownMap["6-1"]+shownMap["6-2"]+shownMap["6-3"]+shownMap["6-4"]+shownMap["6-5"]+shownMap["6-6"]+shownMap["6-7"]+shownMap["6-8"]+"\n"+shownMap["7-0"]+shownMap["7-1"]+shownMap["7-2"]+shownMap["7-3"]+shownMap["7-4"]+shownMap["7-5"]+shownMap["7-6"]+shownMap["7-7"]+shownMap["7-8"]+"\n"+shownMap["8-0"]+shownMap["8-1"]+shownMap["8-2"]+shownMap["8-3"]+shownMap["8-4"]+shownMap["8-5"]+shownMap["8-6"]+shownMap["8-7"]+shownMap["8-8"]+"\n"+shownMap["9-0"]+shownMap["9-1"]+shownMap["9-2"]+shownMap["9-3"]+shownMap["9-4"]+shownMap["9-5"]+shownMap["9-6"]+shownMap["9-7"]+shownMap["9-8"]+"\n"+shownMap["10-0"]+shownMap["10-1"]+shownMap["10-2"]+shownMap["10-3"]+shownMap["10-4"]+shownMap["10-5"]+shownMap["10-6"]+shownMap["10-7"]+shownMap["10-8"]+"\n\n")
		move = input("move up, down, right, or left?\n\n8.) Up\n6.) Right\n4.) Left\n2.) Down\n\n")
	
		#Moving Down
		
		if move == "2":
			if curY == lastRow-1 or map1[curY+1][curX] == 0:
				print("\nCannot move down")

			elif map1[curY+1][curX] == 1:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY+=1

			elif map1[curY+1][curX] == 2:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY+=1
				if enteredClearing == False and hasDug == False:
					(Stats, curHealth, curStam, StamBar, hasSword) = digStart(Stats, curHealth, curStam, StamBar, hasSword)
					hasDug = True
				elif enteredClearing == True and hasSword == False and hasDug2 == False:
					(Stats, curHealth, curStam, StamBar, hasSword) = digDisillusioned(Stats, curHealth, curStam, StamBar, hasSword)
					hasDug2 = True

			elif map1[curY+1][curX] == 3:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY+=1
		
			elif map1[curY+1][curX] == 4:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY+=1
				if ratKilled == True and disillusioned == True and seenDisillusionedRat == False:
					print("Cautiously sneaking past the burrow the rat emerged from earlier you notice the corpse of the rat looks much less feral than before, almost friendly and well groomed.... ")
					seenDisillusionedRat = True
		
		#Moving Up

		elif move == "8":
			
			if curY == 1 or map1[curY-1][curX] == 0:
				print("\nCannot move up")
			
			elif map1[curY-1][curX] == 1:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY-=1 
			
			elif map1[curY-1][curX] == 3:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY-=1
				if hasSword == False and enteredClearing == False:
					(Stats, curHealth, curStam, StamBar, hasSword, disillusioned) = clearingIllusions(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)
					enteredClearing = True
				elif hasSword == True and enteredClearing == False:
					(Stats, curHealth, curStam, StamBar, hasSword, disillusioned) = clearingNoIllusions(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)
					enteredClearing = True
				elif enteredClearing == True and disillusioned == True and seenMaidenLeave == False:
					seenMaidenLeave == True
					print("\nYou note that the statue and the waters from before are missing now.\n")
			
			elif map1[curY-1][curX] == 4:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curY-=1
				if ratKilled == False and hasSword == False:
					(Stats, curHealth, curStam, StamBar) = ratFight(Stats, curHealth, curStam, StamBar)
					ratKilled = True
				elif ratKilled == False and hasSword == True and metNoIllusionRats == False:
					print("\nAlong the way you see a burrow in the cavern wall and a family of immense rats with smooth sleek coats of fur. As intimidating as these large creatures may be they seem friendly enough and they let you pass freely.\n")                                     
					metNoIllusionRats = True                
		

		#Moving Right

		elif move == "6":
			
			if curX == lastCol-1 or map1[curY][curX+1] == 0:
				print("\nCannot move right.")
			
			elif map1[curY][curX+1] == 1:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curX+=1
			
			elif map1[curY][curX+1] == 5:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curX+=1
				if hasSword == True and firstMaidenDead == True:
					print("This waters gross..")
		

		#Moving Left

		elif move == "4":
			
			if curX == 1 or map1[curY][curX-1] == 0:
				print("\nCannot move left")
			
			else:
				shownMap[str(curY)+"-"+str(curX)] = "░"
				curX-=1
		

		#Correcting

		else:
			print("Please input '8' '6' '4' or '2'")
	


	shownMap = printEnvironment(map1, shownMap, curY, curX, lastRow, lastCol)
	print("\n\n"+shownMap["0-0"]+shownMap["0-1"]+shownMap["0-2"]+shownMap["0-3"]+shownMap["0-4"]+shownMap["0-5"]+shownMap["0-6"]+shownMap["0-7"]+shownMap["0-8"]+"\n"+shownMap["1-0"]+shownMap["1-1"]+shownMap["1-2"]+shownMap["1-3"]+shownMap["1-4"]+shownMap["1-5"]+shownMap["1-6"]+shownMap["1-7"]+shownMap["1-8"]+"\n"+shownMap["2-0"]+shownMap["2-1"]+shownMap["2-2"]+shownMap["2-3"]+shownMap["2-4"]+shownMap["2-5"]+shownMap["2-6"]+shownMap["2-7"]+shownMap["2-8"]+"\n"+shownMap["3-0"]+shownMap["3-1"]+shownMap["3-2"]+shownMap["3-3"]+shownMap["3-4"]+shownMap["3-5"]+shownMap["3-6"]+shownMap["3-7"]+shownMap["3-8"]+"\n"+shownMap["4-0"]+shownMap["4-1"]+shownMap["4-2"]+shownMap["4-3"]+shownMap["4-4"]+shownMap["4-5"]+shownMap["4-6"]+shownMap["4-7"]+shownMap["4-8"]+"\n"+shownMap["5-0"]+shownMap["5-1"]+shownMap["5-2"]+shownMap["5-3"]+shownMap["5-4"]+shownMap["5-5"]+shownMap["5-6"]+shownMap["5-7"]+shownMap["5-8"]+"\n"+shownMap["6-0"]+shownMap["6-1"]+shownMap["6-2"]+shownMap["6-3"]+shownMap["6-4"]+shownMap["6-5"]+shownMap["6-6"]+shownMap["6-7"]+shownMap["6-8"]+"\n"+shownMap["7-0"]+shownMap["7-1"]+shownMap["7-2"]+shownMap["7-3"]+shownMap["7-4"]+shownMap["7-5"]+shownMap["7-6"]+shownMap["7-7"]+shownMap["7-8"]+"\n"+shownMap["8-0"]+shownMap["8-1"]+shownMap["8-2"]+shownMap["8-3"]+shownMap["8-4"]+shownMap["8-5"]+shownMap["8-6"]+shownMap["8-7"]+shownMap["8-8"]+"\n"+shownMap["9-0"]+shownMap["9-1"]+shownMap["9-2"]+shownMap["9-3"]+shownMap["9-4"]+shownMap["9-5"]+shownMap["9-6"]+shownMap["9-7"]+shownMap["9-8"]+"\n"+shownMap["10-0"]+shownMap["10-1"]+shownMap["10-2"]+shownMap["10-3"]+shownMap["10-4"]+shownMap["10-5"]+shownMap["10-6"]+shownMap["10-7"]+shownMap["10-8"]+"\n\n")
	map2(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)


main()
