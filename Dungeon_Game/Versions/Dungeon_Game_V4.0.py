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
#05Feb2020
#V3.1 - Changed event tiles appearance in mapping to distinguish them.
#06Feb2020
#V4.0 - Fully implemented map 2, made balance changes for map 1 combat, approaching full implementation of item and skill use.
#		Polished up some new line usage and some output. Fixed bug for gaining more than 1 level at a time not giving all skills up to new level.
#		Modified printEnvironment() to include a 4th possible symbol for chance encounter zones.
#13Feb2020
#Future plans - Expand vision to 3 tiles away, implement fights, fully implement item use and skill use. Make side project for hunters in map 3.

import random

#Hero's status
TeroStats = {
	"Lvl": 1,
	"Exp": 0,
	"Atk": 4,
	"Def": 3,
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
	"Def": 9,
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

Inventory = []
HeldInventory = []

#Regularly called text
combatInvalidChoice = "\nPlease choose from the available actions 'attack' 'defend' 'rest' 'skills'\n"
combatTutorial="\nYou can type, 'attack' to attack the opponent, 'defend' to reduce your damage received, 'rest' to get double stamina returned, or 'skills' to view your skills menu.\n"


#Ending conditionals
usedMaiden = False
firstMaidenDead = False



def printStatus(Stats, curHealth, curStam, StamBar):
	print("\nLevel: " + str(Stats["Lvl"]) + "\nAttack: " + str(Stats["Atk"]) + "\nDefense: " + str(Stats["Def"]) + "\nHealth: " + str(curHealth) + "/" + str(Stats["Health"]) + "\nStamina: " + str(curStam) + "/" + str(StamBar) + "\n\n")

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
		NewStats(Stats, LvlPre, LvlNow)
		printStatus(Stats, curHealth, curStam, StamBar)
	else:
		print("\nExp to next level: " + str(expToLevel) + "\n")
	return(Stats)

def NewStats(Stats, LvlPre, LvlNow):
	
	skillsToLearn = ["Heavy_Blow", "Counter", "Meditate", "Shatter", "Grapple", "Flurry", "Atemi"]

	if Stats["Lvl"] == 2:
		Stats["Atk"] = 6
		Stats["Def"] = 4
		Stats["Stam"] = 3
		Stats["Health"] = 30
		#Heavy Blow deals 1.5* attack stat

	elif Stats["Lvl"] == 3:
		Stats["Atk"] = 9
		Stats["Def"] = 5
		Stats["Stam"] = 3
		Stats["Health"] = 35
		#Counter skill blends pros of attack and defend

	elif Stats["Lvl"] == 4:
		Stats["Atk"] = 12
		Stats["Def"] = 6
		Stats["Stam"] = 3
		Stats["Health"] = 45
		#Meditate skill restores 1.5* rest actions stam

	elif Stats["Lvl"] == 5:
		Stats["Atk"] = 15
		Stats["Def"] = 8
		Stats["Stam"] = 4
		Stats["Health"] = 60
		#Shatter skill deals normal attack after reducing opponents def, stacks 3 times max

	elif Stats["Lvl"] == 6:
		Stats["Atk"] = 18
		Stats["Def"] = 11
		Stats["Stam"] = 5
		Stats["Health"] = 80
		#Grapple does an attack selection ignoring the opponents input and dealing stamina damage instead of health
	elif Stats["Lvl"] == 7:
		Stats["Atk"] = 22
		Stats["Def"] = 14
		Stats["Stam"] = 6
		Stats["Health"] = 100
		#Flurry uses 3-5 attacks in one turn, consequently 3-5 stamina lots however.

	elif Stats["Lvl"] == 8:
		Stats["Atk"] = 28
		Stats["Def"] = 18       
		Stats["Stam"] = 8
		Stats["Health"] = 135
		#Atemi forces the opponent into its largest attack, and redirects it onto its self.

	i = LvlNow
	if LvlNow - LvlPre > 2:
		print("\nYou learned new skills, ", end='')
		while i > LvlPre:
			Stats["Skills"].append(skillsToLearn[i-2].strip())
			i-=1
		i = LvlNow
		while i > LvlPre+1:
			print(Stats["Skills"][i-2].replace("_", " "), ", ", end='')
			i-=1
		print("and ", Stats["Skills"][i-2].replace("_", " "), ".\n")
	elif LvlNow - LvlPre > 1:
		print("\nYou learned new skills, ", end='')
		while i > LvlPre:
			Stats["Skills"].append(skillsToLearn[i-2].strip())
			i-=1
		i = LvlNow
		while i > LvlPre+1:
			print(Stats["Skills"][i-2].replace("_", " "), end=' ')
			i-=1
		print("and ", Stats["Skills"][i-2].replace("_", " "), ".\n")
	else:
		Stats["Skills"].append(skillsToLearn[i-2].strip())
		print("You learned a new skill, ", Stats["Skills"][i-2].replace("_", " "), ".\n")

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
	sToLevel = Stats["ExpPoint"] - Stats["Exp"]                
	LvlNow = Stats["Lvl"]
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
		sToLevel = Stats["ExpPoint"] - Stats["Exp"]
		print("\nExp to next level: " + str(sToLevel) + "\n")
		swordNewStats(Stats, LvlPre, LvlNow)
		print("\nYour new stats are:")
		printStatus(Stats, curHealth, curStam, StamBar)
	else:
		print("\nExp to next level: " + str(sToLevel) + "\n")
	return(Stats)

def swordNewStats(Stats, LvlPre, LvlNow):
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
		#Haya_Suburi skill evades the opponents attack and deals out one attack damage
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
		#pierce skill is normal attack ignoring opponent defense
	elif Stats["Lvl"] == 6:
		Stats["Atk"] = 54
		Stats["Def"] = 32
		Stats["Stam"] = 7
		Stats["Health"] = 130
		#Drain skill uses blades magic to sap the opponents stamina
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
		print("\nYou learned new skills, ", end='')
		while i > LvlPre:
			Stats["Skills"].append(skillsToLearn[i-2].strip())
			i-=1
		i = LvlNow
		while i > LvlPre+1:
			print(Stats["Skills"][i-2].replace("_", " "), ", ", end='')
			i-=1
		print("and ", Stats["Skills"][i-2].replace("_", " "), ".\n")
	elif LvlNow - LvlPre > 1:
		print("\nYou learned new skills, ", end='')
		while i > LvlPre:
			Stats["Skills"].append(skillsToLearn[i-2].strip())
			i-=1
		i = LvlNow
		while i > LvlPre+1:
			print(Stats["Skills"][i-2].replace("_", " "), end=' ')
			i-=1
		print("and ", Stats["Skills"][i-2].replace("_", " "), ".\n")
	else:
		Stats["Skills"].append(skillsToLearn[i-2].strip())
		print("You learned a new skill, ", Stats["Skills"][i-2].replace("_", " "), ".\n")


	return(Stats)


def fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory):
	Inventory = ",".join(inventory[0:2])
	HeldInventory = ",".join(heldInventory[0:2])

	if len(inventory) == 4:
		print("\nYou have ", Inventory, " currently in your inventory. You found '", inventory[3], "'\n")
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
						(curHealth, curStam) = useItem(Stats, curHealth, curStam, StamBar, inventory[use], 0, "", [], 0, 0, 0)[0:2]
						inventory.remove(inventory[use])
						return(curHealth, curStam, inventory, heldInventory)
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
						return(curHealth, curStam, inventory, heldInventory)
			else:
				choice = input("Please only input '8' or '6'")

	else:
		print("\nYou are holding ", HeldInventory, ". You found a '", HeldInventory[3], "'\n")
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
				return(urHealth, curStam, inventory, heldInventory)

def useItem(Stats, curHealth, curStam, StamBar, string, inCombat, stringName, OppStats, OppCurHealth, OppCurStam, OppStamBar):

	if string == "Stale bread":
		curStam = min(curStam + (StamBar/4), StamBar)
		print("\nYou start eating through a rather unpleasant loaf, you regain some stamina", StamBar/4, " and your stamina is now ", curStam, "\n")
		return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
	if string == "Bandages":
		curHealth = min(curHealth + (Stats["Health"]/4), Stats["Health"])
		print("\nYou wrap up some open wounds. You heal ", Stats["Health"]/4, " and your health is now ", curHealth, "\n")
		return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
	elif string == "Adrenaline":
		curStam = min(curStam + (StamBar/2), StamBar)
		print("\nYou consume some adrenaline, you regain some stamina", StamBar/2, " and your stamina is now ", curStam, "\n")
		return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
	elif string == "Oily water":
		#If opponent is axe demon, Devora, Adoma, Imp, Shadow... deal % health damage and reduce their def by 2; if opponent fire demon deal 2x the %health damage
		#If used out of combat print something like splash and do nothing; if used in combat on target not above print something like you throw a spritz of water... it doesn't seem to do much
		#will need to pass if in combat and string for opponents name
		if not inCombat:
			print("\nsplash!\n")
			return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
		elif inCombat and stringName == ("Axe Demon" or "Devora" or "Adoma" or "Imp" or "Shadow"):
			(OppCurHealth) = takeDamage((OppStats["Health"]/8), OppStats, OppCurHealth)
			OppStats["Def"]-=2
			return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
		elif inCombat and stringName == ("Fire Shadow"):
			(OppCurHealth) = takeDamage((OppStats["Health"]/4), OppStats, OppCurHealth)
			OppStats["Def"]-=2
			return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)
		else:
			print("\nYou splash out the vials contents... nothing happened\n")
			return(curHealth, curStam, OppStats, OppCurHealth, OppCurStam)

def useSkill(Stats):
	skillList = ", ".join(Stats["Skills"])
	print("\nYour skills are ", skillList, ".\n")
	print("\nWhat skill do you want to use?\n")
	amountSkills = len(Stats["Skills"])
	numSkills = []
	k = 0
	while k < amountSkills+1:
		numSkills.append(k)
		k+=1
	i = 0
	while i < amountSkills:
		print(i+1, ".) ", Stats["Skills"][i], "\n")
	print(i+1, ".) Don't use a skill\n")
	l = 0
	use = input()
	while l == 0:
		if use not in numSkills:
			use = input("\nPlease enter a valid number.\n")
		else:
			try:
				choice = Stats["Skills"][use]
			except IndexError:
				choice = "Back"
			return(choice)

def Heavy_Blow(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	OppCurHealth = takeDamage((Stats["Atk"]*1.5)-OppStats["Def"], OppStats, OppCurHealth)
	curStam = fatigueStatus(10, StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Counter(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	OppCurHealth = takeDamage(Stats["Atk"]-OppStats["Def"], OppStats, OppCurHealth)
	curStam = fatigueStatus(6, StamBar, curStam)
	Stats["Def"] = Stats["Def"]*2 #Remember to reduce by /2 after opponent attacks.
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Meditate(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	curStam = fatigueStatus(-Stats["Stam"]*3, StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Shatter(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	#Find a way to limit stacking
	OppStats["Def"] -= 2
	OppCurHealth = takeDamage((Stats["Atk"])-OppStats["Def"], OppStats, OppCurHealth)
	curStam = fatigueStatus(8, StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Grapple(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	OppCurStam = fatigueStatus((Stats["Atk"]*2)-OppStats["Def"], OppStamBar, OppCurStam)
	curStam = fatigueStatus(6, StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Flurry(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	attacks = random.randint(1, 101)
	if attack >= 80:
		OppCurHealth = takeDamage((Stats["Atk"]*5)-OppStats["Def"*5], OppStats, OppCurHealth)
		curStam = fatigueStatus(30, StamBar, curStam)
	elif attack >= 40:
		OppCurHealth = takeDamage((Stats["Atk"]*4)-OppStats["Def"*4], OppStats, OppCurHealth)
		curStam = fatigueStatus(24, StamBar, curStam)
	else:
		OppCurHealth = takeDamage((Stats["Atk"]*3)-OppStats["Def"*3], OppStats, OppCurHealth)
		curStam = fatigueStatus(18, StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Atemi(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	#Come back to this when you build out enemy skills to check how it returns and functions.
	#Enemy skillsets slot 0 should always be the strongest swing excluding one time use triggered event skills
	(OppStats, OppCurHealth, OppCurStam, OppStamBar) = eval(OppStats["Skills"][0]+'(OppStats, OppCurHealth, OppCurStam, OppStamBar, OppStats, OppCurHealth, OppCurStam, OppStamBar)')
	curStam = fatigueStatus(6, StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Datotsu(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	OppCurHealth = takeDamage((Stats["Atk"]*1.5)-OppStats["Def"], OppStats, OppCurHealth)
	curStam = fatigueStatus(14, StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Haya_Suburi(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	#Need to implement a way to make opponents attack meaningless. 
	#Maybe just make defense +999999999999 and then reduce it after the round..?
	OppCurHealth = takeDamage(Stats["Atk"]-OppStats["Def"], OppStats, OppCurHealth)
	curStam = fatigueStatus(12, StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Mokuso(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	curStam = fatigueStatus(-Stats["Stam"]*3, StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Pierce(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	OppCurHealth = takeDamage(Stats["Atk"], OppStats, OppCurHealth)
	curStam = fatigueStatus(10, StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Drain(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	OppCurStam = fatigueStatus(Stats["Atk"]-OppStats["Def"], OppStamBar, OppCurStam)
	curStam = fatigueStatus(-(Stats["Atk"]-OppStats["Def"]), StamBar, curStam)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Regenerate(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	curHealth = takeDamage(-(Stats["Health"]/6), Stats, curHealth)
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)

def Kachinuki(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar):
	#Yeah I have no idea. Need to make a while loop to continuosly pick attack if stamina > 8 and min for curHealth = 1
	print("Needs work")
	skillTokens-=1
	return(Stats, curHealth, curStam, StamBar, skillTokens, OppStats, OppCurHealth, OppCurStam, OppStamBar)



def takeDamage(damage, Stats, curHealth):
	curHealth = min(max(curHealth - damage, 0), Stats["Health"])
	return(curHealth)



def fatigueStatus(fatigue, StamBar, curStam):
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
	print("\nAfter taking a rest your stats are:")
	printStatus(Stats, curHealth, curStam, StamBar)
	return(curHealth, curStam)


#Map discovery
def printEnvironment(Map, showMap, curY, curX, lastRow, lastCol):
	
	showMap[str(curY)+"-"+str(curX)] = "X"
	
	if curX != 1:
		if curX != 2:
			if Map[curY][curX-1] == 0:
				showMap[str(curY)+"-"+str(curX-1)] = "█"
			elif Map[curY][curX-1] == (1 or 5):
				showMap[str(curY)+"-"+str(curX-1)] = "░"
			elif Map[curY][curX-1] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY)+"-"+str(curX-1)] = "▒"
			else:
				showMap[str(curY)+"-"+str(curX-1)] = "▓"

			if Map[curY][curX-1] != 0 and Map[curY][curX-2] == 0:
				showMap[str(curY)+"-"+str(curX-2)] = "█"
			elif Map[curY][curX-1] != 0 and Map[curY][curX-2] == (1 or 5):
				showMap[str(curY)+"-"+str(curX-2)] = "░"
			elif Map[curY][curX-1] != 0 and Map[curY][curX-2] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY)+"-"+str(curX-2)] = "▒"
			elif Map[curY][curX-1] != 0 and Map[curY][curX-2] != (0 or 1 or 4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49 or 5 or 8):
				showMap[str(curY)+"-"+str(curX-2)] = "▓"
		else:
			if Map[curY][curX-1] == 0:
				showMap[str(curY)+"-"+str(curX-1)] = "█"
			elif Map[curY][curX-1] == (1 or 5):
				showMap[str(curY)+"-"+str(curX-1)] = "░"
			elif Map[curY][curX-1] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY)+"-"+str(curX-1)] = "▒"
			else:
				showMap[str(curY-1)+"-"+str(curX-1)] = "▓"
	
	if curX != lastCol-1:
		if curX != lastCol-2:
			if Map[curY][curX+1] == 0:
				showMap[str(curY)+"-"+str(curX+1)] = "█"
			elif Map[curY][curX+1] == (1 or 5):
				showMap[str(curY)+"-"+str(curX+1)] = "░"
			elif Map[curY][curX+1] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY)+"-"+str(curX+1)] = "▒"
			else:
				showMap[str(curY)+"-"+str(curX+1)] = "▓"

			if Map[curY][curX+1] != 0 and Map[curY][curX+2] == 0:
				showMap[str(curY)+"-"+str(curX+2)] = "█"
			elif Map[curY][curX+1] != 0 and Map[curY][curX+2] == (1 or 5):
				showMap[str(curY)+"-"+str(curX+2)] = "░"
			elif Map[curY][curX+1] != 0 and Map[curY][curX+2] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY)+"-"+str(curX+2)] = "▒"
			elif Map[curY][curX+1] != 0 and Map[curY][curX+2] != (0 or 1 or 4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49 or 5 or 8):
				showMap[str(curY)+"-"+str(curX+2)] = "▓"
		else:
			if Map[curY][curX+1] == 0:
				showMap[str(curY)+"-"+str(curX+1)] = "█"
			elif Map[curY][curX+1] == (1 or 5):
				showMap[str(curY)+"-"+str(curX+1)] = "░"
			elif Map[curY][curX+1] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY)+"-"+str(curX+1)] = "▒"
			else:
				showMap[str(curY)+"-"+str(curX+1)] = "▓"
	
	if curY != lastRow-1:
		if curY != lastRow-2:
			if Map[curY+1][curX] == 0:
				showMap[str(curY+1)+"-"+str(curX)] = "█"
			elif Map[curY+1][curX] == (1 or 5):
				showMap[str(curY+1)+"-"+str(curX)] = "░"
			elif Map[curY+1][curX] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY+1)+"-"+str(curX)] = "▒"
			else:
				showMap[str(curY+1)+"-"+str(curX)] = "▓"

			if Map[curY+1][curX] != 0 and Map[curY+2][curX] == 0:
				showMap[str(curY+2)+"-"+str(curX)] = "█"
			elif Map[curY+1][curX] != 0 and Map[curY+2][curX] == (1 or 5):
				showMap[str(curY+2)+"-"+str(curX)] = "░"
			elif Map[curY+1][curX] != 0 and Map[curY+2][curX] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY+2)+"-"+str(curX)] = "▒"
			elif Map[curY+1][curX] != 0 and Map[curY+2][curX] != (0 or 1 or 4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49 or 5 or 8):
				showMap[str(curY+2)+"-"+str(curX)] = "▓"
		else:
			if Map[curY+1][curX] == 0:
				showMap[str(curY+1)+"-"+str(curX)] = "█"
			elif Map[curY+1][curX] == (1 or 5):
				showMap[str(curY+1)+"-"+str(curX)] = "░"
			elif Map[curY+1][curX] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY+1)+"-"+str(curX)] = "▒"
			else:
				showMap[str(curY+1)+"-"+str(curX)] = "▓"

	if curY != 1:
		if curY != 2:
			if Map[curY-1][curX] == 0:
				showMap[str(curY-1)+"-"+str(curX)] = "█"
			elif Map[curY-1][curX] == (1 or 5):
				showMap[str(curY-1)+"-"+str(curX)] = "░"
			elif Map[curY-1][curX] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY-1)+"-"+str(curX)] = "▒"
			else:
				showMap[str(curY-1)+"-"+str(curX)] = "▓"

			if Map[curY-1][curX] != 0 and Map[curY-2][curX] == 0:
				showMap[str(curY-2)+"-"+str(curX)] = "█"
			elif Map[curY-1][curX] != 0 and Map[curY-2][curX] == (1 or 5):
				showMap[str(curY-2)+"-"+str(curX)] = "░"
			elif Map[curY-1][curX] != 0 and Map[curY-2][curX] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY-2)+"-"+str(curX)] = "▒"
			elif Map[curY-1][curX] != 0 and Map[curY-2][curX] != (0 or 1 or 4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49 or 5 or 8):
				showMap[str(curY-2)+"-"+str(curX)] = "▓"
		else:
			if Map[curY-1][curX] == 0:
				showMap[str(curY-1)+"-"+str(curX)] = "█"
			elif Map[curY-1][curX] == (1 or 5):
				showMap[str(curY-1)+"-"+str(curX)] = "░"
			elif Map[curY-1][curX] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY-1)+"-"+str(curX)] = "▒"
			else:
				showMap[str(curY-1)+"-"+str(curX)] = "▓"
	
	if curX != 1 and curY != 1:
		if Map[curY-1][curX] != 0 or Map[curY][curX-1] != 0:
			if Map[curY-1][curX-1] == 0:
				showMap[str(curY-1)+"-"+str(curX-1)] = "█"
			elif Map[curY-1][curX-1] == (1 or 5):
				showMap[str(curY-1)+"-"+str(curX-1)] = "░"
			elif Map[curY-1][curX-1] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY-1)+"-"+str(curX-1)] = "▒"
			else:
				showMap[str(curY-1)+"-"+str(curX-1)] = "▓"
	
	
	if curX != lastCol-1 and curY != 1:
		if Map[curY-1][curX] != 0 or Map[curY][curX+1] != 0:
			if Map[curY-1][curX+1] == 0:
				showMap[str(curY-1)+"-"+str(curX+1)] = "█"
			elif Map[curY-1][curX+1] == (1 or 5):
				showMap[str(curY-1)+"-"+str(curX+1)] = "░"
			elif Map[curY-1][curX+1] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY-1)+"-"+str(curX+1)] = "▒"
			else:
				showMap[str(curY-1)+"-"+str(curX+1)] = "▓"
	
	
	if curX != lastCol-1 and curY != lastRow-1:
		if Map[curY+1][curX] != 0 or Map[curY][curX+1] != 0:
			if Map[curY+1][curX+1] == 0:
				showMap[str(curY+1)+"-"+str(curX+1)] = "█"
			elif Map[curY+1][curX+1] == (1 or 5):
				showMap[str(curY+1)+"-"+str(curX+1)] = "░"
			elif Map[curY+1][curX+1] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY+1)+"-"+str(curX+1)] = "▒"
			else:
				showMap[str(curY+1)+"-"+str(curX+1)] = "▓"
	

	if curX != 1 and curY != lastRow-1:
		if Map[curY+1][curX] != 0 or Map[curY][curX-1] != 0:
			if Map[curY+1][curX-1] == 0:
				showMap[str(curY+1)+"-"+str(curX-1)] = "█"
			elif Map[curY+1][curX-1] == (1 or 5):
				showMap[str(curY+1)+"-"+str(curX-1)] = "░"
			elif Map[curY+1][curX-1] == (4 or 40 or 41 or 42 or 43 or 44 or 45 or 46 or 47 or 48 or 49):
				showMap[str(curY+1)+"-"+str(curX-1)] = "▒"
			else:
				showMap[str(curY+1)+"-"+str(curX-1)] = "▓"
	return(showMap)


def map2(Stats, curHealth, curStam, StamBar, inventory, heldInventory, hasSword, disillusioned):

	map2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 			[0, 0, 1, 0, 0, 0, 0, 41, 41, 41, 41, 41, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
 			[0, 0, 3, 1, 0, 0, 0, 41, 41, 41, 41, 41, 41, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
 			[0, 0, 1, 2, 1, 1, 1, 41, 41, 41, 41, 41, 41, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 6, 1, 1, 0, 0, 0, 0, 32, 0, 0],
 			[0, 0, 0, 1, 1, 1, 1, 41, 41, 41, 41, 41, 41, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 20, 6, 6, 6, 1, 1, 0, 0, 0, 0, 0, 0],
 			[0, 0, 0, 0, 1, 0, 0, 41, 41, 41, 41, 41, 41, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0],
 			[0, 0, 0, 0, 0, 0, 0, 0, 41, 41, 41, 41, 41, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
 			[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 34, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 20, 0, 0, 0, 0, 0, 0, 1, 0, 0],
 			[0, 35, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
 			[0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0],
 			[0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 42, 21, 21, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
 			[0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 42, 42, 42, 42, 42, 42, 42, 42, 42, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
 			[0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 42, 42, 42, 42, 42, 42, 42, 42, 42, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0],
 			[0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 42, 42, 42, 42, 42, 42, 42, 42, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0],
 			[0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 42, 42, 42, 42, 42, 42, 42, 0, 43, 43, 43, 43, 1, 1, 0, 1, 0, 1, 0, 0],
 			[0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 44, 44, 44, 44, 0, 1, 1, 1, 0, 1, 42, 42, 42, 42, 42, 42, 1, 0, 43, 43, 43, 43, 1, 1, 0, 1, 0, 1, 0, 0],
 			[0, 0, 0, 45, 45, 45, 45, 0, 1, 1, 0, 44, 44, 44, 44, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 43, 43, 43, 43, 1, 1, 0, 31, 0, 1, 0, 0],
 			[0, 0, 0, 45, 45, 45, 45, 45, 0, 1, 0, 44, 44, 44, 44, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 43, 43, 43, 43, 0, 0, 0, 0, 0, 1, 0, 0],
 			[0, 0, 0, 45, 45, 45, 45, 45, 0, 1, 1, 0, 44, 44, 44, 44, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 43, 43, 43, 1, 1, 1, 1, 1, 1, 1, 0, 0],
 			[0, 0, 45, 45, 45, 45, 45, 45, 45, 0, 1, 0, 44, 44, 44, 44, 44, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
 			[0, 0, 0, 45, 45, 45, 45, 45, 45, 0, 1, 0, 0, 44, 44, 44, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
 			[0, 0, 0, 0, 0, 45, 45, 45, 0, 46, 46, 46, 46, 0, 0, 1, 38, 0, 1, 1, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0],
 			[0, 0, 0, 0, 0, 45, 45, 45, 0, 46, 46, 46, 46, 46, 46, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 80, 0, 0, 0, 0, 1, 0, 0, 0],
 			[0, 0, 0, 0, 0, 45, 45, 0, 46, 46, 46, 46, 46, 46, 46, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 1, 0, 0, 0],
 			[0, 0, 0, 0, 1, 45, 45, 0, 33, 46, 46, 46, 46, 46, 46, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 1, 0, 0, 0],
 			[0, 0, 0, 36, 1, 1, 0, 0, 46, 46, 46, 46, 46, 46, 46, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
 			[0, 0, 0, 37, 1, 0, 0, 0, 0, 46, 46, 46, 46, 46, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 5, 5, 5, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
 			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 30, 70, 0, 0, 0, 0, 0, 0, 0, 1, 38, 0, 0, 1, 39, 0, 0, 0],
 			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]

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
	foes3 = 15
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

	else:
		for y, outer in enumerate(map2):
			for x, inner in enumerate(outer):
				if map2[y][x] == 80:
					map2[y][x] = 0

	while curHealth > 0:
		if foes2 == 14:
			for y, outer in enumerate(map2):
				for x, inner in enumerate(outer):
					if map2[y][x] == 21:
						map2[y][x] = 42

		shownMap = printEnvironment(map2, shownMap, curY, curX, lastRow, lastCol)
		print("\n\n"+shownMap["0-0"]+shownMap["0-1"]+shownMap["0-2"]+shownMap["0-3"]+shownMap["0-4"]+shownMap["0-5"]+shownMap["0-6"]+shownMap["0-7"]+shownMap["0-8"]+shownMap["0-9"]+shownMap["0-10"]+shownMap["0-11"]+shownMap["0-12"]+shownMap["0-13"]+shownMap["0-14"]+shownMap["0-15"]+shownMap["0-16"]+shownMap["0-17"]+shownMap["0-18"]+shownMap["0-19"]+shownMap["0-20"]+shownMap["0-21"]+shownMap["0-22"]+shownMap["0-23"]+shownMap["0-24"]+shownMap["0-25"]+shownMap["0-26"]+shownMap["0-27"]+shownMap["0-28"]+shownMap["0-29"]+shownMap["0-30"]+shownMap["0-31"]+shownMap["0-32"]+shownMap["0-33"]+shownMap["0-34"]+shownMap["0-35"]+shownMap["0-36"]+shownMap["0-37"]+shownMap["0-38"]+shownMap["0-39"]+"\n"+shownMap["1-0"]+shownMap["1-1"]+shownMap["1-2"]+shownMap["1-3"]+shownMap["1-4"]+shownMap["1-5"]+shownMap["1-6"]+shownMap["1-7"]+shownMap["1-8"]+shownMap["1-9"]+shownMap["1-10"]+shownMap["1-11"]+shownMap["1-12"]+shownMap["1-13"]+shownMap["1-14"]+shownMap["1-15"]+shownMap["1-16"]+shownMap["1-17"]+shownMap["1-18"]+shownMap["1-19"]+shownMap["1-20"]+shownMap["1-21"]+shownMap["1-22"]+shownMap["1-23"]+shownMap["1-24"]+shownMap["1-25"]+shownMap["1-26"]+shownMap["1-27"]+shownMap["1-28"]+shownMap["1-29"]+shownMap["1-30"]+shownMap["1-31"]+shownMap["1-32"]+shownMap["1-33"]+shownMap["1-34"]+shownMap["1-35"]+shownMap["1-36"]+shownMap["1-37"]+shownMap["1-38"]+shownMap["1-39"]+"\n"+shownMap["2-0"]+shownMap["2-1"]+shownMap["2-2"]+shownMap["2-3"]+shownMap["2-4"]+shownMap["2-5"]+shownMap["2-6"]+shownMap["2-7"]+shownMap["2-8"]+shownMap["2-9"]+shownMap["2-10"]+shownMap["2-11"]+shownMap["2-12"]+shownMap["2-13"]+shownMap["2-14"]+shownMap["2-15"]+shownMap["2-16"]+shownMap["2-17"]+shownMap["2-18"]+shownMap["2-19"]+shownMap["2-20"]+shownMap["2-21"]+shownMap["2-22"]+shownMap["2-23"]+shownMap["2-24"]+shownMap["2-25"]+shownMap["2-26"]+shownMap["2-27"]+shownMap["2-28"]+shownMap["2-29"]+shownMap["2-30"]+shownMap["2-31"]+shownMap["2-32"]+shownMap["2-33"]+shownMap["2-34"]+shownMap["2-35"]+shownMap["2-36"]+shownMap["2-37"]+shownMap["2-38"]+shownMap["2-39"]+"\n"+shownMap["3-0"]+shownMap["3-1"]+shownMap["3-2"]+shownMap["3-3"]+shownMap["3-4"]+shownMap["3-5"]+shownMap["3-6"]+shownMap["3-7"]+shownMap["3-8"]+shownMap["3-9"]+shownMap["3-10"]+shownMap["3-11"]+shownMap["3-12"]+shownMap["3-13"]+shownMap["3-14"]+shownMap["3-15"]+shownMap["3-16"]+shownMap["3-17"]+shownMap["3-18"]+shownMap["3-19"]+shownMap["3-20"]+shownMap["3-21"]+shownMap["3-22"]+shownMap["3-23"]+shownMap["3-24"]+shownMap["3-25"]+shownMap["3-26"]+shownMap["3-27"]+shownMap["3-28"]+shownMap["3-29"]+shownMap["3-30"]+shownMap["3-31"]+shownMap["3-32"]+shownMap["3-33"]+shownMap["3-34"]+shownMap["3-35"]+shownMap["3-36"]+shownMap["3-37"]+shownMap["3-38"]+shownMap["3-39"]+"\n"+shownMap["4-0"]+shownMap["4-1"]+shownMap["4-2"]+shownMap["4-3"]+shownMap["4-4"]+shownMap["4-5"]+shownMap["4-6"]+shownMap["4-7"]+shownMap["4-8"]+shownMap["4-9"]+shownMap["4-10"]+shownMap["4-11"]+shownMap["4-12"]+shownMap["4-13"]+shownMap["4-14"]+shownMap["4-15"]+shownMap["4-16"]+shownMap["4-17"]+shownMap["4-18"]+shownMap["4-19"]+shownMap["4-20"]+shownMap["4-21"]+shownMap["4-22"]+shownMap["4-23"]+shownMap["4-24"]+shownMap["4-25"]+shownMap["4-26"]+shownMap["4-27"]+shownMap["4-28"]+shownMap["4-29"]+shownMap["4-30"]+shownMap["4-31"]+shownMap["4-32"]+shownMap["4-33"]+shownMap["4-34"]+shownMap["4-35"]+shownMap["4-36"]+shownMap["4-37"]+shownMap["4-38"]+shownMap["4-39"]+"\n"+shownMap["5-0"]+shownMap["5-1"]+shownMap["5-2"]+shownMap["5-3"]+shownMap["5-4"]+shownMap["5-5"]+shownMap["5-6"]+shownMap["5-7"]+shownMap["5-8"]+shownMap["5-9"]+shownMap["5-10"]+shownMap["5-11"]+shownMap["5-12"]+shownMap["5-13"]+shownMap["5-14"]+shownMap["5-15"]+shownMap["5-16"]+shownMap["5-17"]+shownMap["5-18"]+shownMap["5-19"]+shownMap["5-20"]+shownMap["5-21"]+shownMap["5-22"]+shownMap["5-23"]+shownMap["5-24"]+shownMap["5-25"]+shownMap["5-26"]+shownMap["5-27"]+shownMap["5-28"]+shownMap["5-29"]+shownMap["5-30"]+shownMap["5-31"]+shownMap["5-32"]+shownMap["5-33"]+shownMap["5-34"]+shownMap["5-35"]+shownMap["5-36"]+shownMap["5-37"]+shownMap["5-38"]+shownMap["5-39"]+"\n"+shownMap["6-0"]+shownMap["6-1"]+shownMap["6-2"]+shownMap["6-3"]+shownMap["6-4"]+shownMap["6-5"]+shownMap["6-6"]+shownMap["6-7"]+shownMap["6-8"]+shownMap["6-9"]+shownMap["6-10"]+shownMap["6-11"]+shownMap["6-12"]+shownMap["6-13"]+shownMap["6-14"]+shownMap["6-15"]+shownMap["6-16"]+shownMap["6-17"]+shownMap["6-18"]+shownMap["6-19"]+shownMap["6-20"]+shownMap["6-21"]+shownMap["6-22"]+shownMap["6-23"]+shownMap["6-24"]+shownMap["6-25"]+shownMap["6-26"]+shownMap["6-27"]+shownMap["6-28"]+shownMap["6-29"]+shownMap["6-30"]+shownMap["6-31"]+shownMap["6-32"]+shownMap["6-33"]+shownMap["6-34"]+shownMap["6-35"]+shownMap["6-36"]+shownMap["6-37"]+shownMap["6-38"]+shownMap["6-39"]+"\n"+shownMap["7-0"]+shownMap["7-1"]+shownMap["7-2"]+shownMap["7-3"]+shownMap["7-4"]+shownMap["7-5"]+shownMap["7-6"]+shownMap["7-7"]+shownMap["7-8"]+shownMap["7-9"]+shownMap["7-10"]+shownMap["7-11"]+shownMap["7-12"]+shownMap["7-13"]+shownMap["7-14"]+shownMap["7-15"]+shownMap["7-16"]+shownMap["7-17"]+shownMap["7-18"]+shownMap["7-19"]+shownMap["7-20"]+shownMap["7-21"]+shownMap["7-22"]+shownMap["7-23"]+shownMap["7-24"]+shownMap["7-25"]+shownMap["7-26"]+shownMap["7-27"]+shownMap["7-28"]+shownMap["7-29"]+shownMap["7-30"]+shownMap["7-31"]+shownMap["7-32"]+shownMap["7-33"]+shownMap["7-34"]+shownMap["7-35"]+shownMap["7-36"]+shownMap["7-37"]+shownMap["7-38"]+shownMap["7-39"]+"\n"+shownMap["8-0"]+shownMap["8-1"]+shownMap["8-2"]+shownMap["8-3"]+shownMap["8-4"]+shownMap["8-5"]+shownMap["8-6"]+shownMap["8-7"]+shownMap["8-8"]+shownMap["8-9"]+shownMap["8-10"]+shownMap["8-11"]+shownMap["8-12"]+shownMap["8-13"]+shownMap["8-14"]+shownMap["8-15"]+shownMap["8-16"]+shownMap["8-17"]+shownMap["8-18"]+shownMap["8-19"]+shownMap["8-20"]+shownMap["8-21"]+shownMap["8-22"]+shownMap["8-23"]+shownMap["8-24"]+shownMap["8-25"]+shownMap["8-26"]+shownMap["8-27"]+shownMap["8-28"]+shownMap["8-29"]+shownMap["8-30"]+shownMap["8-31"]+shownMap["8-32"]+shownMap["8-33"]+shownMap["8-34"]+shownMap["8-35"]+shownMap["8-36"]+shownMap["8-37"]+shownMap["8-38"]+shownMap["8-39"]+"\n"+shownMap["9-0"]+shownMap["9-1"]+shownMap["9-2"]+shownMap["9-3"]+shownMap["9-4"]+shownMap["9-5"]+shownMap["9-6"]+shownMap["9-7"]+shownMap["9-8"]+shownMap["9-9"]+shownMap["9-10"]+shownMap["9-11"]+shownMap["9-12"]+shownMap["9-13"]+shownMap["9-14"]+shownMap["9-15"]+shownMap["9-16"]+shownMap["9-17"]+shownMap["9-18"]+shownMap["9-19"]+shownMap["9-20"]+shownMap["9-21"]+shownMap["9-22"]+shownMap["9-23"]+shownMap["9-24"]+shownMap["9-25"]+shownMap["9-26"]+shownMap["9-27"]+shownMap["9-28"]+shownMap["9-29"]+shownMap["9-30"]+shownMap["9-31"]+shownMap["9-32"]+shownMap["9-33"]+shownMap["9-34"]+shownMap["9-35"]+shownMap["9-36"]+shownMap["9-37"]+shownMap["9-38"]+shownMap["9-39"]+"\n"+shownMap["10-0"]+shownMap["10-1"]+shownMap["10-2"]+shownMap["10-3"]+shownMap["10-4"]+shownMap["10-5"]+shownMap["10-6"]+shownMap["10-7"]+shownMap["10-8"]+shownMap["10-9"]+shownMap["10-10"]+shownMap["10-11"]+shownMap["10-12"]+shownMap["10-13"]+shownMap["10-14"]+shownMap["10-15"]+shownMap["10-16"]+shownMap["10-17"]+shownMap["10-18"]+shownMap["10-19"]+shownMap["10-20"]+shownMap["10-21"]+shownMap["10-22"]+shownMap["10-23"]+shownMap["10-24"]+shownMap["10-25"]+shownMap["10-26"]+shownMap["10-27"]+shownMap["10-28"]+shownMap["10-29"]+shownMap["10-30"]+shownMap["10-31"]+shownMap["10-32"]+shownMap["10-33"]+shownMap["10-34"]+shownMap["10-35"]+shownMap["10-36"]+shownMap["10-37"]+shownMap["10-38"]+shownMap["10-39"]+"\n"+shownMap["11-0"]+shownMap["11-1"]+shownMap["11-2"]+shownMap["11-3"]+shownMap["11-4"]+shownMap["11-5"]+shownMap["11-6"]+shownMap["11-7"]+shownMap["11-8"]+shownMap["11-9"]+shownMap["11-10"]+shownMap["11-11"]+shownMap["11-12"]+shownMap["11-13"]+shownMap["11-14"]+shownMap["11-15"]+shownMap["11-16"]+shownMap["11-17"]+shownMap["11-18"]+shownMap["11-19"]+shownMap["11-20"]+shownMap["11-21"]+shownMap["11-22"]+shownMap["11-23"]+shownMap["11-24"]+shownMap["11-25"]+shownMap["11-26"]+shownMap["11-27"]+shownMap["11-28"]+shownMap["11-29"]+shownMap["11-30"]+shownMap["11-31"]+shownMap["11-32"]+shownMap["11-33"]+shownMap["11-34"]+shownMap["11-35"]+shownMap["11-36"]+shownMap["11-37"]+shownMap["11-38"]+shownMap["11-39"]+"\n"+shownMap["12-0"]+shownMap["12-1"]+shownMap["12-2"]+shownMap["12-3"]+shownMap["12-4"]+shownMap["12-5"]+shownMap["12-6"]+shownMap["12-7"]+shownMap["12-8"]+shownMap["12-9"]+shownMap["12-10"]+shownMap["12-11"]+shownMap["12-12"]+shownMap["12-13"]+shownMap["12-14"]+shownMap["12-15"]+shownMap["12-16"]+shownMap["12-17"]+shownMap["12-18"]+shownMap["12-19"]+shownMap["12-20"]+shownMap["12-21"]+shownMap["12-22"]+shownMap["12-23"]+shownMap["12-24"]+shownMap["12-25"]+shownMap["12-26"]+shownMap["12-27"]+shownMap["12-28"]+shownMap["12-29"]+shownMap["12-30"]+shownMap["12-31"]+shownMap["12-32"]+shownMap["12-33"]+shownMap["12-34"]+shownMap["12-35"]+shownMap["12-36"]+shownMap["12-37"]+shownMap["12-38"]+shownMap["12-39"]+"\n"+shownMap["13-0"]+shownMap["13-1"]+shownMap["13-2"]+shownMap["13-3"]+shownMap["13-4"]+shownMap["13-5"]+shownMap["13-6"]+shownMap["13-7"]+shownMap["13-8"]+shownMap["13-9"]+shownMap["13-10"]+shownMap["13-11"]+shownMap["13-12"]+shownMap["13-13"]+shownMap["13-14"]+shownMap["13-15"]+shownMap["13-16"]+shownMap["13-17"]+shownMap["13-18"]+shownMap["13-19"]+shownMap["13-20"]+shownMap["13-21"]+shownMap["13-22"]+shownMap["13-23"]+shownMap["13-24"]+shownMap["13-25"]+shownMap["13-26"]+shownMap["13-27"]+shownMap["13-28"]+shownMap["13-29"]+shownMap["13-30"]+shownMap["13-31"]+shownMap["13-32"]+shownMap["13-33"]+shownMap["13-34"]+shownMap["13-35"]+shownMap["13-36"]+shownMap["13-37"]+shownMap["13-38"]+shownMap["13-39"]+"\n"+shownMap["14-0"]+shownMap["14-1"]+shownMap["14-2"]+shownMap["14-3"]+shownMap["14-4"]+shownMap["14-5"]+shownMap["14-6"]+shownMap["14-7"]+shownMap["14-8"]+shownMap["14-9"]+shownMap["14-10"]+shownMap["14-11"]+shownMap["14-12"]+shownMap["14-13"]+shownMap["14-14"]+shownMap["14-15"]+shownMap["14-16"]+shownMap["14-17"]+shownMap["14-18"]+shownMap["14-19"]+shownMap["14-20"]+shownMap["14-21"]+shownMap["14-22"]+shownMap["14-23"]+shownMap["14-24"]+shownMap["14-25"]+shownMap["14-26"]+shownMap["14-27"]+shownMap["14-28"]+shownMap["14-29"]+shownMap["14-30"]+shownMap["14-31"]+shownMap["14-32"]+shownMap["14-33"]+shownMap["14-34"]+shownMap["14-35"]+shownMap["14-36"]+shownMap["14-37"]+shownMap["14-38"]+shownMap["14-39"]+"\n"+shownMap["15-0"]+shownMap["15-1"]+shownMap["15-2"]+shownMap["15-3"]+shownMap["15-4"]+shownMap["15-5"]+shownMap["15-6"]+shownMap["15-7"]+shownMap["15-8"]+shownMap["15-9"]+shownMap["15-10"]+shownMap["15-11"]+shownMap["15-12"]+shownMap["15-13"]+shownMap["15-14"]+shownMap["15-15"]+shownMap["15-16"]+shownMap["15-17"]+shownMap["15-18"]+shownMap["15-19"]+shownMap["15-20"]+shownMap["15-21"]+shownMap["15-22"]+shownMap["15-23"]+shownMap["15-24"]+shownMap["15-25"]+shownMap["15-26"]+shownMap["15-27"]+shownMap["15-28"]+shownMap["15-29"]+shownMap["15-30"]+shownMap["15-31"]+shownMap["15-32"]+shownMap["15-33"]+shownMap["15-34"]+shownMap["15-35"]+shownMap["15-36"]+shownMap["15-37"]+shownMap["15-38"]+shownMap["15-39"]+"\n"+shownMap["16-0"]+shownMap["16-1"]+shownMap["16-2"]+shownMap["16-3"]+shownMap["16-4"]+shownMap["16-5"]+shownMap["16-6"]+shownMap["16-7"]+shownMap["16-8"]+shownMap["16-9"]+shownMap["16-10"]+shownMap["16-11"]+shownMap["16-12"]+shownMap["16-13"]+shownMap["16-14"]+shownMap["16-15"]+shownMap["16-16"]+shownMap["16-17"]+shownMap["16-18"]+shownMap["16-19"]+shownMap["16-20"]+shownMap["16-21"]+shownMap["16-22"]+shownMap["16-23"]+shownMap["16-24"]+shownMap["16-25"]+shownMap["16-26"]+shownMap["16-27"]+shownMap["16-28"]+shownMap["16-29"]+shownMap["16-30"]+shownMap["16-31"]+shownMap["16-32"]+shownMap["16-33"]+shownMap["16-34"]+shownMap["16-35"]+shownMap["16-36"]+shownMap["16-37"]+shownMap["16-38"]+shownMap["16-39"]+"\n"+shownMap["17-0"]+shownMap["17-1"]+shownMap["17-2"]+shownMap["17-3"]+shownMap["17-4"]+shownMap["17-5"]+shownMap["17-6"]+shownMap["17-7"]+shownMap["17-8"]+shownMap["17-9"]+shownMap["17-10"]+shownMap["17-11"]+shownMap["17-12"]+shownMap["17-13"]+shownMap["17-14"]+shownMap["17-15"]+shownMap["17-16"]+shownMap["17-17"]+shownMap["17-18"]+shownMap["17-19"]+shownMap["17-20"]+shownMap["17-21"]+shownMap["17-22"]+shownMap["17-23"]+shownMap["17-24"]+shownMap["17-25"]+shownMap["17-26"]+shownMap["17-27"]+shownMap["17-28"]+shownMap["17-29"]+shownMap["17-30"]+shownMap["17-31"]+shownMap["17-32"]+shownMap["17-33"]+shownMap["17-34"]+shownMap["17-35"]+shownMap["17-36"]+shownMap["17-37"]+shownMap["17-38"]+shownMap["17-39"]+"\n"+shownMap["18-0"]+shownMap["18-1"]+shownMap["18-2"]+shownMap["18-3"]+shownMap["18-4"]+shownMap["18-5"]+shownMap["18-6"]+shownMap["18-7"]+shownMap["18-8"]+shownMap["18-9"]+shownMap["18-10"]+shownMap["18-11"]+shownMap["18-12"]+shownMap["18-13"]+shownMap["18-14"]+shownMap["18-15"]+shownMap["18-16"]+shownMap["18-17"]+shownMap["18-18"]+shownMap["18-19"]+shownMap["18-20"]+shownMap["18-21"]+shownMap["18-22"]+shownMap["18-23"]+shownMap["18-24"]+shownMap["18-25"]+shownMap["18-26"]+shownMap["18-27"]+shownMap["18-28"]+shownMap["18-29"]+shownMap["18-30"]+shownMap["18-31"]+shownMap["18-32"]+shownMap["18-33"]+shownMap["18-34"]+shownMap["18-35"]+shownMap["18-36"]+shownMap["18-37"]+shownMap["18-38"]+shownMap["18-39"]+"\n"+shownMap["19-0"]+shownMap["19-1"]+shownMap["19-2"]+shownMap["19-3"]+shownMap["19-4"]+shownMap["19-5"]+shownMap["19-6"]+shownMap["19-7"]+shownMap["19-8"]+shownMap["19-9"]+shownMap["19-10"]+shownMap["19-11"]+shownMap["19-12"]+shownMap["19-13"]+shownMap["19-14"]+shownMap["19-15"]+shownMap["19-16"]+shownMap["19-17"]+shownMap["19-18"]+shownMap["19-19"]+shownMap["19-20"]+shownMap["19-21"]+shownMap["19-22"]+shownMap["19-23"]+shownMap["19-24"]+shownMap["19-25"]+shownMap["19-26"]+shownMap["19-27"]+shownMap["19-28"]+shownMap["19-29"]+shownMap["19-30"]+shownMap["19-31"]+shownMap["19-32"]+shownMap["19-33"]+shownMap["19-34"]+shownMap["19-35"]+shownMap["19-36"]+shownMap["19-37"]+shownMap["19-38"]+shownMap["19-39"]+"\n"+shownMap["20-0"]+shownMap["20-1"]+shownMap["20-2"]+shownMap["20-3"]+shownMap["20-4"]+shownMap["20-5"]+shownMap["20-6"]+shownMap["20-7"]+shownMap["20-8"]+shownMap["20-9"]+shownMap["20-10"]+shownMap["20-11"]+shownMap["20-12"]+shownMap["20-13"]+shownMap["20-14"]+shownMap["20-15"]+shownMap["20-16"]+shownMap["20-17"]+shownMap["20-18"]+shownMap["20-19"]+shownMap["20-20"]+shownMap["20-21"]+shownMap["20-22"]+shownMap["20-23"]+shownMap["20-24"]+shownMap["20-25"]+shownMap["20-26"]+shownMap["20-27"]+shownMap["20-28"]+shownMap["20-29"]+shownMap["20-30"]+shownMap["20-31"]+shownMap["20-32"]+shownMap["20-33"]+shownMap["20-34"]+shownMap["20-35"]+shownMap["20-36"]+shownMap["20-37"]+shownMap["20-38"]+shownMap["20-39"]+"\n"+shownMap["21-0"]+shownMap["21-1"]+shownMap["21-2"]+shownMap["21-3"]+shownMap["21-4"]+shownMap["21-5"]+shownMap["21-6"]+shownMap["21-7"]+shownMap["21-8"]+shownMap["21-9"]+shownMap["21-10"]+shownMap["21-11"]+shownMap["21-12"]+shownMap["21-13"]+shownMap["21-14"]+shownMap["21-15"]+shownMap["21-16"]+shownMap["21-17"]+shownMap["21-18"]+shownMap["21-19"]+shownMap["21-20"]+shownMap["21-21"]+shownMap["21-22"]+shownMap["21-23"]+shownMap["21-24"]+shownMap["21-25"]+shownMap["21-26"]+shownMap["21-27"]+shownMap["21-28"]+shownMap["21-29"]+shownMap["21-30"]+shownMap["21-31"]+shownMap["21-32"]+shownMap["21-33"]+shownMap["21-34"]+shownMap["21-35"]+shownMap["21-36"]+shownMap["21-37"]+shownMap["21-38"]+shownMap["21-39"]+"\n"+shownMap["22-0"]+shownMap["22-1"]+shownMap["22-2"]+shownMap["22-3"]+shownMap["22-4"]+shownMap["22-5"]+shownMap["22-6"]+shownMap["22-7"]+shownMap["22-8"]+shownMap["22-9"]+shownMap["22-10"]+shownMap["22-11"]+shownMap["22-12"]+shownMap["22-13"]+shownMap["22-14"]+shownMap["22-15"]+shownMap["22-16"]+shownMap["22-17"]+shownMap["22-18"]+shownMap["22-19"]+shownMap["22-20"]+shownMap["22-21"]+shownMap["22-22"]+shownMap["22-23"]+shownMap["22-24"]+shownMap["22-25"]+shownMap["22-26"]+shownMap["22-27"]+shownMap["22-28"]+shownMap["22-29"]+shownMap["22-30"]+shownMap["22-31"]+shownMap["22-32"]+shownMap["22-33"]+shownMap["22-34"]+shownMap["22-35"]+shownMap["22-36"]+shownMap["22-37"]+shownMap["22-38"]+shownMap["22-39"]+"\n"+shownMap["23-0"]+shownMap["23-1"]+shownMap["23-2"]+shownMap["23-3"]+shownMap["23-4"]+shownMap["23-5"]+shownMap["23-6"]+shownMap["23-7"]+shownMap["23-8"]+shownMap["23-9"]+shownMap["23-10"]+shownMap["23-11"]+shownMap["23-12"]+shownMap["23-13"]+shownMap["23-14"]+shownMap["23-15"]+shownMap["23-16"]+shownMap["23-17"]+shownMap["23-18"]+shownMap["23-19"]+shownMap["23-20"]+shownMap["23-21"]+shownMap["23-22"]+shownMap["23-23"]+shownMap["23-24"]+shownMap["23-25"]+shownMap["23-26"]+shownMap["23-27"]+shownMap["23-28"]+shownMap["23-29"]+shownMap["23-30"]+shownMap["23-31"]+shownMap["23-32"]+shownMap["23-33"]+shownMap["23-34"]+shownMap["23-35"]+shownMap["23-36"]+shownMap["23-37"]+shownMap["23-38"]+shownMap["23-39"]+"\n"+shownMap["24-0"]+shownMap["24-1"]+shownMap["24-2"]+shownMap["24-3"]+shownMap["24-4"]+shownMap["24-5"]+shownMap["24-6"]+shownMap["24-7"]+shownMap["24-8"]+shownMap["24-9"]+shownMap["24-10"]+shownMap["24-11"]+shownMap["24-12"]+shownMap["24-13"]+shownMap["24-14"]+shownMap["24-15"]+shownMap["24-16"]+shownMap["24-17"]+shownMap["24-18"]+shownMap["24-19"]+shownMap["24-20"]+shownMap["24-21"]+shownMap["24-22"]+shownMap["24-23"]+shownMap["24-24"]+shownMap["24-25"]+shownMap["24-26"]+shownMap["24-27"]+shownMap["24-28"]+shownMap["24-29"]+shownMap["24-30"]+shownMap["24-31"]+shownMap["24-32"]+shownMap["24-33"]+shownMap["24-34"]+shownMap["24-35"]+shownMap["24-36"]+shownMap["24-37"]+shownMap["24-38"]+shownMap["24-39"]+"\n"+shownMap["25-0"]+shownMap["25-1"]+shownMap["25-2"]+shownMap["25-3"]+shownMap["25-4"]+shownMap["25-5"]+shownMap["25-6"]+shownMap["25-7"]+shownMap["25-8"]+shownMap["25-9"]+shownMap["25-10"]+shownMap["25-11"]+shownMap["25-12"]+shownMap["25-13"]+shownMap["25-14"]+shownMap["25-15"]+shownMap["25-16"]+shownMap["25-17"]+shownMap["25-18"]+shownMap["25-19"]+shownMap["25-20"]+shownMap["25-21"]+shownMap["25-22"]+shownMap["25-23"]+shownMap["25-24"]+shownMap["25-25"]+shownMap["25-26"]+shownMap["25-27"]+shownMap["25-28"]+shownMap["25-29"]+shownMap["25-30"]+shownMap["25-31"]+shownMap["25-32"]+shownMap["25-33"]+shownMap["25-34"]+shownMap["25-35"]+shownMap["25-36"]+shownMap["25-37"]+shownMap["25-38"]+shownMap["25-39"]+"\n"+shownMap["26-0"]+shownMap["26-1"]+shownMap["26-2"]+shownMap["26-3"]+shownMap["26-4"]+shownMap["26-5"]+shownMap["26-6"]+shownMap["26-7"]+shownMap["26-8"]+shownMap["26-9"]+shownMap["26-10"]+shownMap["26-11"]+shownMap["26-12"]+shownMap["26-13"]+shownMap["26-14"]+shownMap["26-15"]+shownMap["26-16"]+shownMap["26-17"]+shownMap["26-18"]+shownMap["26-19"]+shownMap["26-20"]+shownMap["26-21"]+shownMap["26-22"]+shownMap["26-23"]+shownMap["26-24"]+shownMap["26-25"]+shownMap["26-26"]+shownMap["26-27"]+shownMap["26-28"]+shownMap["26-29"]+shownMap["26-30"]+shownMap["26-31"]+shownMap["26-32"]+shownMap["26-33"]+shownMap["26-34"]+shownMap["26-35"]+shownMap["26-36"]+shownMap["26-37"]+shownMap["26-38"]+shownMap["26-39"]+"\n"+shownMap["27-0"]+shownMap["27-1"]+shownMap["27-2"]+shownMap["27-3"]+shownMap["27-4"]+shownMap["27-5"]+shownMap["27-6"]+shownMap["27-7"]+shownMap["27-8"]+shownMap["27-9"]+shownMap["27-10"]+shownMap["27-11"]+shownMap["27-12"]+shownMap["27-13"]+shownMap["27-14"]+shownMap["27-15"]+shownMap["27-16"]+shownMap["27-17"]+shownMap["27-18"]+shownMap["27-19"]+shownMap["27-20"]+shownMap["27-21"]+shownMap["27-22"]+shownMap["27-23"]+shownMap["27-24"]+shownMap["27-25"]+shownMap["27-26"]+shownMap["27-27"]+shownMap["27-28"]+shownMap["27-29"]+shownMap["27-30"]+shownMap["27-31"]+shownMap["27-32"]+shownMap["27-33"]+shownMap["27-34"]+shownMap["27-35"]+shownMap["27-36"]+shownMap["27-37"]+shownMap["27-38"]+shownMap["27-39"]+"\n"+shownMap["28-0"]+shownMap["28-1"]+shownMap["28-2"]+shownMap["28-3"]+shownMap["28-4"]+shownMap["28-5"]+shownMap["28-6"]+shownMap["28-7"]+shownMap["28-8"]+shownMap["28-9"]+shownMap["28-10"]+shownMap["28-11"]+shownMap["28-12"]+shownMap["28-13"]+shownMap["28-14"]+shownMap["28-15"]+shownMap["28-16"]+shownMap["28-17"]+shownMap["28-18"]+shownMap["28-19"]+shownMap["28-20"]+shownMap["28-21"]+shownMap["28-22"]+shownMap["28-23"]+shownMap["28-24"]+shownMap["28-25"]+shownMap["28-26"]+shownMap["28-27"]+shownMap["28-28"]+shownMap["28-29"]+shownMap["28-30"]+shownMap["28-31"]+shownMap["28-32"]+shownMap["28-33"]+shownMap["28-34"]+shownMap["28-35"]+shownMap["28-36"]+shownMap["28-37"]+shownMap["28-38"]+shownMap["28-39"]+"\n"+shownMap["29-0"]+shownMap["29-1"]+shownMap["29-2"]+shownMap["29-3"]+shownMap["29-4"]+shownMap["29-5"]+shownMap["29-6"]+shownMap["29-7"]+shownMap["29-8"]+shownMap["29-9"]+shownMap["29-10"]+shownMap["29-11"]+shownMap["29-12"]+shownMap["29-13"]+shownMap["29-14"]+shownMap["29-15"]+shownMap["29-16"]+shownMap["29-17"]+shownMap["29-18"]+shownMap["29-19"]+shownMap["29-20"]+shownMap["29-21"]+shownMap["29-22"]+shownMap["29-23"]+shownMap["29-24"]+shownMap["29-25"]+shownMap["29-26"]+shownMap["29-27"]+shownMap["29-28"]+shownMap["29-29"]+shownMap["29-30"]+shownMap["29-31"]+shownMap["29-32"]+shownMap["29-33"]+shownMap["29-34"]+shownMap["29-35"]+shownMap["29-36"]+shownMap["29-37"]+shownMap["29-38"]+shownMap["29-39"]+"\n")
		
		if "Charm of Awareness" in heldInventory:
			move = input("move up, down, right, or left?\n\n8.) Up\n6.) Right\n4.) Left\n2.) Down\n5.) Rest\n\n")
		else:
			move = input("move up, down, right, or left?\n\n8.) Up\n6.) Right\n4.) Left\n2.) Down\n\n")

		#Moving Down		
		if move == "2":
			if curY == lastRow-1 or map2[curY+1][curX] == 0:
				print("\nCannot move down\n")

			elif map2[curY+1][curX] == 1:
				curY+=1

			#Items
			elif map2[curY+1][curX] == 31:
				curY+=1
				print("\nYou found some bandages!\n")
				if len(inventory) <= 3:
					inventory.append("Bandages")
				else:
					inventory.append("Bandages")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1
		
			elif map2[curY+1][curX] == 32:
				curY+=1
				print("\nYou found a Charm of Awareness. Now you can press 5 to rest and gain half of your health and stamina back anywhere on the map, but you may be attacked and have to fight.\n")
				if len(heldInventory) <= 3:
					heldInventory.append("Charm of Awareness")
				else:
					heldInventory.append("Charm of Awareness")
					(inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)[2:4]
				map2[curY][curX] = 1

			elif map2[curY+1][curX] == 33:
				curY+=1
				print("\nYou found some Oily water!\n")
				if len(inventory) <= 3:
					inventory.append("Oily water")
				else:
					inventory.append("Oily water")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			elif map2[curY+1][curX] == 34:
				curY+=1
				print("\nYou found a salt rock!\n")
				if len(heldInventory) <= 3:
					heldInventory.append("Salt rock")
				else:
					heldInventory.append("Salt rock")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			elif map2[curY+1][curX] == 37:
				curY+=1
				print("\nYou found a scalpel!\n")
				if len(heldInventory) <= 3:
					heldInventory.append("Scalpel")
				else:
					heldInventory.append("Scalpel")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			elif map2[curY+1][curX] == 38:
				curY+=1
				print("\nYou found some adrenaline!\n")
				if len(inventory) <= 3:
					inventory.append("Adrenaline")
				else:
					inventory.append("Adrenaline")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			elif map2[curY+1][curX] == 39:
				if "Canteen" in heldInventory:
					curY+=1
					print("You found a puddle of clean looking water and filled your canteen.")
					heldInventory.remove("Canteen")
					heldInventory.append("Full Canteen")
					map2[curY][curX] = 1
				else:
					print("\nTheres a puddle infront of you, you'd rather not get feet wet for no reason.\n")


			#chance encounters
			elif map2[curY+1][curX] == 41:
				curY+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = impFight(Stats, curHealth, curStam, StamBar)
						foes1-=1
						if foes1 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 41:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = giantSlugFight(Stats, curHealth, curStam, StamBar)
						foes1-=1
						if foes1 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 41:
										map2[y][x] = 1

			elif map2[curY+1][curX] == 42:
				curY+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = axeDemonFight(Stats, curHealth, curStam, StamBar)
						for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 21:
										map2[y][x] = 42
						foes2-=1
						if foes2 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 42:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = savageFight(Stats, curHealth, curStam, StamBar)
						for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 21:
										map2[y][x] = 42
						foes2-=1
						if foes2 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 42:
										map2[y][x] = 1

			elif map2[curY+1][curX] == 43:
				curY+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					(Stats, curHealth, curStam, StamBar) = viciousBatFight(Stats, curHealth, curStam, StamBar)
					foes3-=1
					if foes3 == 0:
						for y, outer in enumerate(map2):
							for x, inner in enumerate(outer):
								if map2[y][x] == 43:
									map2[y][x] = 1

			elif map2[curY+1][curX] == 44:
				curY+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						if foes4 == 15 and ("Stale bread") in inventory and ("Full Canteen" and "Salt rock") in heldInventory:
							print("lore")
							inventory.remove("Stale bread" and "Full Canteen" and "Salt rock")
							foes4 = 0
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 44:
										map2[y][x] = 1
						else:
							(Stats, curHealth, curStam, StamBar) = starvedMenFight(Stats, curHealth, curStam, StamBar)
							foes4-=1
							if foes4 == 0:
								for y, outer in enumerate(map2):
									for x, inner in enumerate(outer):
										if map2[y][x] == 44:
											map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = zombieFight(Stats, curHealth, curStam, StamBar)
						foes4-=1
						if foes4 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 44:
										map2[y][x] = 1

			elif map2[curY+1][curX] == 45:
				curY+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = crazedMenFight(Stats, curHealth, curStam, StamBar)
						foes5-=1
						if foes5 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 45:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = skeletonFight(Stats, curHealth, curStam, StamBar)
						foes5-=1
						if foes5 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 45:
										map2[y][x] = 1

			elif map2[curY+1][curX] == 46:
				curY+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = smallGolemFight(Stats, curHealth, curStam, StamBar)
						foes6-=1
						if foes6 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 46:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = bruteFight(Stats, curHealth, curStam, StamBar)
						foes6-=1
						if foes6 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 46:
										map2[y][x] = 1

			#Poison
			elif map2[curY+1][curX] == 5:
				curY+=1
				if "Ventilator" not in heldInventory:
					curHealth = takeDamage((Stats["Health"]/8), Stats, curHealth)
					print("\nThe poison eats away at you. You took ", Stats["Health"]/8, " damage.\nYour health is now ", curHealth, ".\n")

			#Extreme encounter
			elif map2[curY+1][curX] == 70:
				curY+=1
				(Stats, curHealth, curStam, StamBar) = AdomaMap2Fight(Stats, curHealth, curStam, StamBar)
				map2[curY][curX] = 1


		
		#Moving Up

		elif move == "8":
			
			if curY == 1 or map2[curY-1][curX] == 0:
				print("\nCannot move up\n")
			
			elif map2[curY-1][curX] == 1:
				curY-=1

			#Main Encounter
			elif map2[curY-1][curX] == 2:
				if not disillusioned and not hasSword:
					curY-=1
					(Stats, curHealth, curStam, StamBar) = crazedScientistFight(Stats, curHealth, curStam, StamBar)
				elif hasSword:
					print("\nYou approach an intelligent looking man working feverishly. As you get close he shouts 'Go away, I'm busy!'.\n")
				else:
					if "Scalpel" in heldInventory:
						print("\nYou approach a feverishly working man, 'Ooooo! That would be perfect!!, come give me that scalpel at once.' he blurts out as he reaches over and snatches the scalpel from your pouch before scurrying over closer to his shoddily crafted work desk\n")
						curY-=1
						map2[curY][curX] = 1
						map2[curY][curX-1] = 22
						inventory.remove("Scalpel")
					else:
						print("\nYou approach a feverishly working man, 'Wha- who the heck are you. I'm busy, if you aren't going to help go away!' he shouts\n")

			elif map2[curY-1][curX] == 20:
				curY-=1
				choice = input("\nYou see a pitfall in front of you, it looks like you could carefully let yourself down some ledges. \n\n8.) Drop yourself carefully down the opening\n2.) Come back later\n")
				if choice == "8":
					print("\nYou carefully let yourself down the first few ledges, suddenly a ledge snaps along the way and you drop down. You feel fine, however you won't be able to climb back up.\n")
					map3(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)
				elif choice == "2":
					curY+=1
					print("\nYou turn back from the pitfall.\n")
				else:
					choice = input("\nPlease input '8' or '2' only.\n")

			elif map2[curY-1][curX] == 21:
				curY-=1
				if hasSword or Disillusioned:
					(Stats, curHealth, curStam, StamBar) = axeDemonFight(Stats, curHealth, curStam, StamBar)
				else:
					(Stats, curHealth, curStam, StamBar) = savageFight(Stats, curHealth, curStam, StamBar)
				for y, outer in enumerate(map2):
					for x, inner in enumerate(outer):
						if map2[y][x] == 21:
							map2[y][x] = 42

			#Items
			elif  map2[curY-1][curX] == 33:
				curY-=1
				print("\nYou found some oily water!\n")
				if len(inventory) <= 3:
					inventory.append("Oily water")
				else:
					inventory.append("Oily water")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			elif  map2[curY-1][curX] == 35:
				curY-=1
				print("\nYou found an empty canteen!\n")
				if len(heldInventory) <= 3:
					heldInventory.append("Canteen")
				else:
					heldInventory.append("Canteen")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			elif  map2[curY-1][curX] == 36:
				curY-=1
				print("\nYou found some stale bread!\n")
				if len(inventory) <= 3:
					inventory.append("Stale bread")
				else:
					inventory.append("Stale bread")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			#chance encounters
			elif map2[curY-1][curX] == 41:
				curY-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = impFight(Stats, curHealth, curStam, StamBar)
						foes1-=1
						if foes1 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 41:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = giantSlugFight(Stats, curHealth, curStam, StamBar)
						foes1-=1
						if foes1 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 41:
										map2[y][x] = 1

			elif map2[curY-1][curX] == 42:
				curY-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = axeDemonFight(Stats, curHealth, curStam, StamBar)
						for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 21:
										map2[y][x] = 42
						foes2-=1
						if foes2 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 42:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = savageFight(Stats, curHealth, curStam, StamBar)
						for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 21:
										map2[y][x] = 42
						foes2-=1
						if foes2 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 42:
										map2[y][x] = 1

			elif map2[curY-1][curX] == 43:
				curY-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					(Stats, curHealth, curStam, StamBar) = viciousBatFight(Stats, curHealth, curStam, StamBar)
					foes3-=1
					if foes3 == 0:
						for y, outer in enumerate(map2):
							for x, inner in enumerate(outer):
								if map2[y][x] == 43:
									map2[y][x] = 1

			elif map2[curY-1][curX] == 44:
				curY-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if hasSword or disillusioned:	
						(Stats, curHealth, curStam, StamBar) = starvedMenFight(Stats, curHealth, curStam, StamBar)
						foes4-=1
						if foes4 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 44:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = zombieFight(Stats, curHealth, curStam, StamBar)
						foes4-=1
						if foes4 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 44:
										map2[y][x] = 1

			elif map2[curY-1][curX] == 45:
				curY-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = crazedMenFight(Stats, curHealth, curStam, StamBar)
						foes5-=1
						if foes5 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 45:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = skeletonFight(Stats, curHealth, curStam, StamBar)
						foes5-=1
						if foes5 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 45:
										map2[y][x] = 1

			elif map2[curY-1][curX] == 46:
				curY-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = smallGolemFight(Stats, curHealth, curStam, StamBar)
						foes6-=1
						if foes6 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 46:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = bruteFight(Stats, curHealth, curStam, StamBar)
						foes6-=1
						if foes6 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 46:
										map2[y][x] = 1

			#Poison
			elif map2[curY-1][curX] == 5:
				curY-=1
				if "Ventilator" not in heldInventory:
					curHealth = takeDamage((Stats["Health"]/8), Stats, curHealth)
					print("\nThe poison eats away at you. You took ", Stats["Health"]/8, " damage.\nYour health is now ", curHealth, ".\n")

				


		#Moving Right

		elif move == "6":
			
			if curX == lastCol-1 or map2[curY][curX+1] == 0:
				print("\nCannot move right.")
			
			elif map2[curY][curX+1] == 1:
				curX+=1

			#Main Encounter
			elif map2[curY][curX+1] == 20:
				curX+=1
				choice = input("\nYou see a pitfall in front of you, it looks like you could carefully let yourself down some ledges. \n\n6.) Drop yourself carefully down the opening\n4.) Come back later\n")
				if choice == "6":
					print("\nYou carefully let yourself down the first few ledges, suddenly a ledge snaps along the way and you drop down. You feel fine, however you won't be able to climb back up.\n")
					map3()
				elif choice == "4":
					curY+=1
					print("\nYou turn back from the pitfall.\n")
				else:
					choice = input("\nPlease input '6' or '4' only.\n")

			elif map2[curY][curX+1] == 21:
				curX+=1
				if hasSword or Disillusioned:
					(Stats, curHealth, curStam, StamBar) = axeDemonFight(Stats, curHealth, curStam, StamBar)
					foes2-=1
				else:
					(Stats, curHealth, curStam, StamBar) = savageFight(Stats, curHealth, curStam, StamBar)
					foes2-=1
				for y, outer in enumerate(map2):
					for x, inner in enumerate(outer):
						if map2[y][x] == 21:
							map2[y][x] = 42

			#Items
			elif map2[curY][curX+1] == 38:
				curX+=1
				print("\nYou found some adrenaline!\n")
				if len(inventory) <= 3:
					inventory.append("Adrenaline")
				else:
					inventory.append("Adrenaline")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			#chance encounters
			elif map2[curY][curX+1] == 41:
				curX+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = impFight(Stats, curHealth, curStam, StamBar)
						foes1-=1
						if foes1 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 41:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = giantSlugFight(Stats, curHealth, curStam, StamBar)
						foes1-=1
						if foes1 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 41:
										map2[y][x] = 1

			elif map2[curY][curX+1] == 42:
				curX+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = axeDemonFight(Stats, curHealth, curStam, StamBar)
						for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 21:
										map2[y][x] = 42
						foes2-=1
						if foes2 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 42:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = savageFight(Stats, curHealth, curStam, StamBar)
						for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 21:
										map2[y][x] = 42
						foes2-=1
						if foes2 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 42:
										map2[y][x] = 1

			elif map2[curY][curX+1] == 43:
				curX+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					(Stats, curHealth, curStam, StamBar) = viciousBatFight(Stats, curHealth, curStam, StamBar)
					foes3-=1
					if foes3 == 0:
						for y, outer in enumerate(map2):
							for x, inner in enumerate(outer):
								if map2[y][x] == 43:
									map2[y][x] = 1

			elif map2[curY][curX+1] == 44:
				curX+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if hasSword or disillusioned:	
						(Stats, curHealth, curStam, StamBar) = starvedMenFight(Stats, curHealth, curStam, StamBar)
						foes4-=1
						if foes4 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 44:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = zombieFight(Stats, curHealth, curStam, StamBar)
						foes4-=1
						if foes4 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 44:
										map2[y][x] = 1

			elif map2[curY][curX+1] == 45:
				curX+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = crazedMenFight(Stats, curHealth, curStam, StamBar)
						foes5-=1
						if foes5 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 45:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = skeletonFight(Stats, curHealth, curStam, StamBar)
						foes5-=1
						if foes5 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 45:
										map2[y][x] = 1

			elif map2[curY][curX+1] == 46:
				curX+=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = smallGolemFight(Stats, curHealth, curStam, StamBar)
						foes6-=1
						if foes6 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 46:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = bruteFight(Stats, curHealth, curStam, StamBar)
						foes6-=1
						if foes6 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 46:
										map2[y][x] = 1

			#Poison
			elif map2[curY][curX+1] == 5:
				curX+=1
				if "Ventilator" not in heldInventory:
					curHealth = takeDamage((Stats["Health"]/8), Stats, curHealth)
					print("\nThe poison eats away at you. You took ", Stats["Health"]/8, " damage.\nYour health is now ", curHealth, ".\n")

		#Moving Left

		elif move == "4":
			
			if curX == 1 or map2[curY][curX-1] == 0:
				print("\nCannot move left")
			
			elif map2[curY][curX-1] == 1:
				curX-=1

			#Main Encounter
			elif map2[curY][curX-1] == 2:
				if not disillusioned and not hasSword:
					curX-=1
					(Stats, curHealth, curStam, StamBar) = crazedScientistFight(Stats, curHealth, curStam, StamBar)
					map2[curY][curX] = 1
				elif hasSword:
					print("\nYou approach an intelligent looking man working feverishly. As you get close he shouts 'Go away, I'm busy!'.\n")
				else:
					if "Scalpel" in heldInventory:
						print("\nYou approach a feverishly working man, 'Ooooo! That would be perfect!!, come give me that scalpel at once.' he blurts out as he reaches over and snatches the scalpel from your pouch before scurrying over closer to his shoddily crafted work desk\n")
						curX-=1
						map2[curY][curX] = 1
						map2[curY][curX-1] = 22
						inventory.remove("Scalpel")
					else:
						print("\nYou approach a feverishly working man, 'Wha- who the heck are you. I'm busy, if you aren't going to help go away!' he shouts\n")


			elif map2[curY][curX-1] == 22:
				print("\n'Don't bother me!' the scientist shouts\n")
				

			#Items
			elif map2[curY][curX-1] == 3:
				print("\n'I noticed these giant bugs don't seem to mind the poison clouds around here and I've disected them and made these nice little masks out of the part of their body that filters out the posion. You shouuuld be able to put it over your mouth and breath fine in the posion!\n")
				if len(heldInventory) <= 3:
					heldInventory.append("Ventilator")
					map2[curY][curX-1] = 9
				else:
					heldInventory.append("Ventilator")
					(inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)[2:4]
					map2[curY][curX-1] = 9

			elif map2[curY][curX-1] == 9:
				print("\n'well I hardly think you'll need more than one.' the scientist says\n")

			elif map2[curY][curX-1] == 30:
				curX-=1
				print("\nYou found a silver idol!\n")
				if len(heldInventory) <= 3:
					heldInventory.append("Silver Idol")
				else:
					heldInventory.append("Silver Idol")
					(inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)[2:4]
				map2[curY][curX] = 1

			elif map2[curY][curX-1] == 33:
				curX-=1
				print("\nYou found some oily water!\n")
				if len(inventory) <= 3:
					inventory.append("Oily water")
				else:
					inventory.append("Oily water")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			elif map2[curY][curX-1] == 34:
				curX-=1
				print("\nYou found a salt rock!\n")
				if len(heldInventory) <= 3:
					heldInventory.append("Salt rock")
				else:
					heldInventory.append("Salt rock")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			elif map2[curY][curX-1] == 35:
				curX-=1
				print("\nYou found a canteen!\n")
				if len(heldInventory) <= 3:
					heldInventory.append("Canteen")
				else:
					heldInventory.append("Canteen")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			elif map2[curY][curX-1] == 36:
				curX-=1
				print("\nYou found some stale bread!\n")
				if len(inventory) <= 3:
					inventory.append("Stale bread")
				else:
					inventory.append("Stale bread")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			elif map2[curY][curX-1] == 37:
				curX-=1
				print("\nYou found a scalpel!\n")
				if len(heldInventory) <= 3:
					heldInventory.append("Scalpel")
				else:
					heldInventory.append("Scalpel")
					(curHealth, curStam, inventory, heldInventory) = fullInventory(Stats, curHealth, curStam, StamBar, inventory, heldInventory)
				map2[curY][curX] = 1

			#chance encounters
			elif map2[curY][curX-1] == 41:
				curX-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = impFight(Stats, curHealth, curStam, StamBar)
						foes1-=1
						if foes1 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 41:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = giantSlugFight(Stats, curHealth, curStam, StamBar)
						foes1-=1
						if foes1 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 41:
										map2[y][x] = 1

			elif map2[curY][curX-1] == 42:
				curX-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = axeDemonFight(Stats, curHealth, curStam, StamBar)
						for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 21:
										map2[y][x] = 42
						foes2-=1
						if foes2 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 42:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = savageFight(Stats, curHealth, curStam, StamBar)
						for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 21:
										map2[y][x] = 42
						foes2-=1
						if foes2 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 42:
										map2[y][x] = 1

			elif map2[curY][curX-1] == 43:
				curX-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					(Stats, curHealth, curStam, StamBar) = viciousBatFight(Stats, curHealth, curStam, StamBar)
					foes3-=1
					if foes3 == 0:
						for y, outer in enumerate(map2):
							for x, inner in enumerate(outer):
								if map2[y][x] == 43:
									map2[y][x] = 1

			elif map2[curY][curX-1] == 44:
				curX-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if hasSword or disillusioned:	
						(Stats, curHealth, curStam, StamBar) = starvedMenFight(Stats, curHealth, curStam, StamBar)
						foes4-=1
						if foes4 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 44:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = zombieFight(Stats, curHealth, curStam, StamBar)
						foes4-=1
						if foes4 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 44:
										map2[y][x] = 1

			elif map2[curY][curX-1] == 45:
				curX-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = crazedMenFight(Stats, curHealth, curStam, StamBar)
						foes5-=1
						if foes5 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 45:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = skeletonFight(Stats, curHealth, curStam, StamBar)
						foes5-=1
						if foes5 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 45:
										map2[y][x] = 1

			elif map2[curY][curX-1] == 46:
				curX-=1
				encounter = random.randint(1,101)
				if encounter <= 20:
					if disillusioned or hasSword:
						(Stats, curHealth, curStam, StamBar) = smallGolemFight(Stats, curHealth, curStam, StamBar)
						foes6-=1
						if foes6 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 46:
										map2[y][x] = 1
					else:
						(Stats, curHealth, curStam, StamBar) = bruteFight(Stats, curHealth, curStam, StamBar)
						foes6-=1
						if foes6 == 0:
							for y, outer in enumerate(map2):
								for x, inner in enumerate(outer):
									if map2[y][x] == 46:
										map2[y][x] = 1

			#Poison
			elif map2[curY][curX-1] == 5:
				curX-=1
				if "Ventilator" not in heldInventory:
					curHealth = takeDamage((Stats["Health"]/8), Stats, curHealth)
					print("\nThe poison eats away at you. You took ", Stats["Health"]/8, " damage.\nYour health is now ", curHealth, ".\n")
		
		#Resting
		elif move == "5":
			if "Charm of Awareness" in heldInventory:
				if hasSword or disillusioned:
					encounter = random.randint(0,101)
					if encounter <= 20:
						(Stats, curHealth, curStam, StamBar) = crazedMenFight(Stats, curHealth, curStam, StamBar)
					else:
						(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
				else:
					encounter = random.randint(0,101)
					if encounter <= 20:
						(Stats, curHealth, curStam, StamBar) = skeletonFight(Stats, curHealth, curStam, StamBar)
					else:
						(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
			else:
				print("\nPlease input '8' '6' '4' or '2'\n")

		#Correcting
		else:
			if "Charm of Awareness" in heldInventory:
				print("\nPlease input '8' '6' '4' '2' or '5'\n")
			else:
				print("\nPlease input '8' '6' '4' or '2'\n")

	print("\nYou cough and weeze in the posion clouds. Everything goes hazy.\n")
	SystemExit()


	
def skeletonFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def crazedMenFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def giantSlugsFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def impFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def savageFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def axeDemonFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def viciousBatFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def zombieFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def starvedMenFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def bruteFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def smallGolemFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def AdomaMap2Fight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)

def crazedScientistFight(Stats, curHealth, curStam, StamBar):
	print("fight things")
	return(Stats, curHealth, curStam, StamBar)


def clearingIllusions(Stats, curHealth, curStam, StamBar, hasSword, disillusioned):
	
	loop = 0
	move=input("\n\nYou quickly shuffle forward to get distance from the burrow fearful there may be more creatures yet inside. Your body rings out in agonizing pain, missing chunks of flesh and losing blood fast. Even still you progress, ahead you see a blinding light amidst the darkness. When you cross into the light and your vision adjusts you a see a spacious circular room with the narrow pathway you came from behind you and another similar continuation on the other side of the room. The right side of the floor seems to be all water and lining the wall rather than cavern walls of rock is a glistening polished white marble with an occasional lit torch along it. In front of the center of the wall amidst the bath stands a life sized marble statue of young maiden shedding a single tear. As you lock eyes with the statue you feel a strong urge to get into the water and the intensity of the pain you feel from each of your wounds increases immensely more and more each second. Peel away from the statues gaze and move on in the caverns or accept its call and join it in the waters?\n\n8.) Peel away\n6.) Accept\n\n")  
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





def clearingNoIllusions(Stats, curHealth, curStam, StamBar):
	#status for Shadow
	ShadowStats = {
	"Atk": 12,
	"Def": 7,
	"Stam": 4.5,
	"Health": 60,
	}

	ShadowStamBar = ShadowStats["Stam"]*10
	ShadowCurrentStam = ShadowStamBar
	ShadowCurrentHealth = ShadowStats["Health"]

	global firstMaidenDead
	print("\nYou venture into the passage the other direction. Along the way you see a burrow in the cavern wall and a family of immense rats with smooth sleek coats of fur. As intimidating as these large creatures may be they seem friendly enough and they let you pass freely. Further beyond you come into a spacious clearing between the passage you came from and another ahead of you. On the right half of the cave wall is a pool lined with marble, filled with black eerie waters, and at the far end of it is a shadowy figure shaped sort of like a woman with horns. As you notice this creature you close your grip around your sword tighter and stare, and the shadow breaks the stand still in the room with an angry shriek and the water around her stirs up.\n")
	print(combatTutorial)
	statProgress(ShadowCurrentHealth, ShadowCurrentStam, curHealth, curStam)
	while ShadowCurrentHealth > 35 and curHealth > 0:
		choice = input("\nThe waters whirl in unnatural patterns and the shadow cackles maniacally, what will you do?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n\n")
		if choice == "6":
			if ShadowCurrentStam >= 8:
				curHealth = takeDamage(((ShadowStats["Atk"] - Stats["Def"])//2), Stats, curHealth)
				ShadowCurrentStam = fatigueStatus((8-ShadowStats["Stam"]), ShadowStamBar, ShadowCurrentStam)
				curStam = fatigueStatus(-Stats["Stam"], StamBar, curStam)
				statProgress(ShadowCurrentHealth, ShadowCurrentStam, curHealth, curStam)
			else:
				print("\nThe shadowy figure envelopes its lower half in the murky waters and hisses.\n")
				ShadowCurrentStam = fatigueStatus(-2*ShadowStats["Stam"], ShadowStamBar, ShadowCurrentStam)
				statProgress(ShadowCurrentHealth, ShadowCurrentStam, curHealth, curStam)
		elif choice == "8":
			if curStam >= 8:
				ShadowCurrentHealth = takeDamage(Stats["Atk"] - ShadowStats["Def"], ShadowStats, ShadowCurrentHealth)
				curStam = fatigueStatus(8-Stats["Stam"], StamBar, curStam)
				if ShadowCurrentStam >= 8:
					curHealth = takeDamage(ShadowStats["Atk"] - Stats["Def"], Stats, curHealth)
					ShadowCurrentStam = fatigueStatus(8-ShadowStats["Stam"], ShadowStamBar, ShadowCurrentStam)
					statProgress(ShadowCurrentHealth, ShadowCurrentStam, curHealth, curStam)
				else:
					print("\nThe shadow writhes in place trying to dodge your blade, but is held still by the waters wrapped around it.\n")
					ShadowCurrentStam = fatigueStatus(-ShadowStats["Stam"]*2, ShadowStamBar, ShadowCurrentStam)
					statProgress(ShadowCurrentHealth, ShadowCurrentStam, curHealth, curStam)
			else:
				print("\nYou are too fatigued to attack\n")
		elif choice == "4":
			if curStam >= (StamBar-4):
				print("\nYou've no need to rest now.\n")
			else:
				curStam = fatigueStatus(-2*Stats["Stam"], StamBar, curStam)
				if ShadowCurrentStam >= 8:
					curHealth = takeDamage(ShadowStats["Atk"] - Stats["Def"], Stats, curHealth)
					ShadowCurrentStam = fatigueStatus(8-ShadowStats["Stam"], ShadowStamBar, ShadowCurrentStam)
					statProgress(ShadowCurrentHealth, ShadowCurrentStam, curHealth, curStam)
				else:
					print("\nThe shadow rapidly twirls and lowers itself within a bubble of the murky water, leaving only its eyes over the water keeping you in sight while you catch your breath.\n")
					ShadowCurrentStam = fatigueStatus(-2*ShadowStats["Stam"], ShadowStamBar, ShadowCurrentStam)
					statProgress(ShadowCurrentHealth, ShadowCurrentStam, curHealth, curStam)
		elif choice == "2":
			print("\nYou haven't learned any skills yet.\n")
		else:
			choice = input("\nPlease input '8' '6' '4' or '2'")
	

	if curHealth <= 0:
		print("\nThe shadow cackles mockingly while dark bubbles rise from the pool and pop around her. Your vision gets hazy and you collapse.\n")
		SystemExit()

	elif ShadowCurrentHealth <= 35:
		print("\nThe Shadow grabs it's horns firmly and pulls on them while screeching. All of the water rises from the floor, a large amount forming a base around the shadows legs, and the rest hovering in the air formed into something like 10 seperate giant tails. The shadow silences its screech and releases its hands down by its side and stares blankly at you for a moment.... \n\nSuddenly it raises its arms up extended towards you and its fingers start to snap out of their human like shape and extend, and you notice the tails of water move corresponding to the way it moves it's fingers. You brace yourself unsure what to do and then 4 of the tails slam into you far too fast for you to react. The tails hit you in an x pattern and form a ball around you suffocating you, in a mad flail to free yourself you slash at the waters and the sword glows bright, the water around you loses its rigid form and splashes down onto the floor dropping you onto your back.\n")
		curStam = fatigueStatus(12, StamBar, curStam)
		print("\nYour struggle wore you out, your stamina is now ", curStam, "\n")
		choice = input("\nThe tails that struck you are very slowly being pulled back into the water around the shadows legs, do you want to make a dash to try and slice away some or try to prepare to intercept an attack?\n\n8.) Dash forward\n6.) Prepare to intercept\n\n")
		while curHealth > 0:
			if choice == "6":
				print("\nyou stand firm and when a single tail is propelled towards you, you run the glowing blade through it and again watch it lose form and splash down around you.\n")
				loop = 0
				choice = input("Your plan seems to be working, continue to intercept incoming tails or go on the offensive?\n\n8.) Continue intercepting\n6.) Go on the offense\n\n")
				while loop == 0:
					if choice == "8":
						loop+=1
						print("\nYou prepare to repeat your same action and wait for a tail to launch after you. After a short moment the next tail comes flying towards you and you time your motion and start to swing. When the tail and sword are about to collide the tail suddenly buckles up to avoid the blade and two more tails slam into your sides. You cut your way out again but the force the tails slammed into you with was much higher this time and severely injured you.\n")
						curHealth = takeDamage(7, Stats, curHealth)
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
										Stats["Exp"] += 100
										print("\n\nYou gained 100 Exp!")
										Stats = swordCheckLvl(Stats, curHealth, curStam, StamBar)
										(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
										print("\nYou pick yourself up and head into the caverns ahead of you, blade at the ready.\n")
										return(Stats, curHealth, curStam, StamBar)
								elif choice == "6":
									if curStam >= 20:
										loop+=1
										curStam = fatigueStatus(20, StamBar, curStam)
										print("\nYou charge at a dead sprint and land the blow into the chest of the shadow itself, it screams and implodes like an over filled ballon.\n")
										firstMaidenDead = True
										print(", but you hold firm and run the blade through the shadow to the hilt. To your surprise the white aura the sowrd let off earlier surrounds the shadow and then chages sensation from its calm serene feeling to one of a divine, awe inspiring, being casting judgement down on a child that lost its's way. The aura burned angrily and the shadow bellowed in screams, not like the screeches before but truly screams of horror and fear. The shadow slowly ceased to be and as it burned away and shriveled the aura shrank around it until it only wrapped around the blade again and the shadow was entirely gone. The waters collapsed into the pool once more and a black mist rose from it and into the blade, transforming to the white glow of the blade itself, and the pool beneath turned in color to be normal everyday waters.\n")
										Stats["Exp"] += 250
										print("\n\nYou've gained 250 Exp!!")
										Stats = swordCheckLvl(Stats, curHealth, curStam, StamBar)
										print("\nYour heart pounding, body shaking from both exhaustion and internal damage, you collapse face first into the pool of now cleansed waters. You think to yourself for a moment, 'am I going to die here like this? after everything!?' face under water unable to move your body. As you run out of breath, you nearly let the blade slip from your hand and drift away, but before it does the same white aura envelopes you and you feel it mending your body.\n")
										(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
										print("\nAble to move your limbs once more you lift yourself out from the pool of water and gasp for air. after a moment to catch your breath you glance at the passage you've yet to travel down and the blade at your side intensifies its ringing sound. You feel strangely indebted to this sword and accept its desire. You pick yourself up and start to venture down the passageway.\n")
										return(Stats, curHealth, curStam, StamBar)
									elif curStam >= 12:
										loop+=1
										print("\nYou pause for just a moment and as a tail slams forth with great speed, you run under it and charge at the shadow. Before you can reach all the way to it the other tails curl in front of the shadow to protect it. You slash through all 3 successfully, but immediately get slammed in the back by the last tail. Having the wind knocked out of you, you struggle to get back to your feet and the shadow cackles and twirls its last tail over your head.\n")
										curStam = fatigueStatus(12, StamBar, curStam)
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
													(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
													return(Stats, curHealth, curStam, StamBar)
												elif choice == "6":
													loop+=1
													print("\nYou take your time to position your footing and joints to make one swift push forward and stab into the shadow without alerting the shadow itself. Your attack is a success... sort of. You were able to get up and lunge forward without being struck in return, however the watery base at the shadows legs stopped your blades momentum only a few inches into it. The blade starts to shimmer like in the tails before, and the remaining tails collapse around you, but you're blade is still stuck in the waters around the shadow and those waters aren't collapsin like the tails. You lock eyes with the shadow for a brief moment, before it screeches in your face and slams you across the room.\n")
													curHealth = takeDamage(8, Stats, curHealth)
													if curHealth < 1:
														print("\nThe last forceful shove from the shadow was the straw that broke the camels back for you. Your body is too broken down to will forward anymore. Your life fades away...\n")
														SystemExit()
													else:
														print("Disoriented and nearing death you scramble to get to your feet and collect up your sword, but you see that the shadow bolting dwon the chamber you've yet to traverse. You take a moment to collect your things and slouch against the wall for awhile. After a long enough stretch of time to feel sustainable you get up move towards the next passageway\n")
														print("\n\nYou gained 100 exp!")
														Stats["Exp"]+=100
														Stats = swordCheckLvl(Stats, curHealth, curStam, StamBar)
														(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
														return(Stats, curHealth, curStam, StamBar)
												elif choice == "4":
													loop+=1
													print("\nYou try to place your footing down, and push with your arms to spring up swiftly to a stand and then backpedal away, and succeed. However, just as you get up and move to get away the tails looming over you start to pummel down on you with no ability to defend yourself. They slam into you relentlessly until suddenly the shadows face is over your own and its claws rips into your face.\n")
													curHealth = 0
													SystemExit()
												else:
													choice = input("Please input '8', '6', or '4'\n\n")
									else:
										choice = input("It seems you're too fatigued to make the attack, you'll only be able to intercept, please try again.\n\n")
								else:
									choice = input("Please input '8' or '6'\n\n")
					elif choice == "6":
						loop+=1
						#go on the offense, 5 tails
						print("\nYou recognize that the shadow is adapting to your strategy and think that perhaps you need to change it up yourself. You feign a full on charge and then stop in place swiftly pivoting on your right foot to slash around you with your sword, catching 2 tails intended to strike you from behind. The tails splash down and the Shadow screeches, and flails the last 3 tails around.wildly around itself.\n")
						choice = input("\nDo you want to push the momentum or change it up and try something new again?\n8.) Push the momentum\n6.) Try something new again\n\n")
						while loop < 2:
							if choice == "8":
								loop+=1
								print("\nYou continue your offensive push, and the shadow launches 2 tails at you. Before they get in range to slash at they slow significantly, swell up at the tips, and then slam together to capture you in their water. You're able to use the sword to instantly nullify the waters like before, but as you're freed from the waters grip the last tail slams into your skull with great force.\n")
								curHealth = takeDamage(10, Stats, curHealth)
								if curHealth < 1:
									SystemExit()
								else:
									print("\nYou took 10 damage, your health is now ", curHealth)
									print("\n\nimmediately as you hit the ground the tail flails around wildly and slams into your sprawled out body again.\n")
									curHealth = takeDamage(6, Stats, curHealth)
									if curHealth < 1:
										print("The follow up attack from the last tail proved to be too much for you, and you slowly lose consciousness...")
										SystemExit()
									else:
										print("\nYou lost 6 more health, and your health is now ", curHealth, "\n")
										print("\nAs the tail goes to strike at you again you barely manage to lift up your sword and burst the tail before it crushes you. The shadow having lost all of its tails shreeks horrifically before transforming into a dark mist and bolting down the passageway you haven't yet traversed.\n")
										Stats["Exp"]+=100
										Stats = swordCheckLvl(Stats, curHealth, curStam, StamBar)
										(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
										return(Stats, curHealth, curStam, StamBar)
							elif choice == "6":
								loop+=1
								print("\nTrying to think quick what you haven't done yet, you come up with an idea to bait the tails away from the shadow and then javelin tossing the sword into the shadow. You charge forward like before, stop and turn away like before, and as you hear the watery tails surging towards you, you grip the hilt with a c-grip and lock in your elbow. You turn and instantly hurl the blade with an upward arc towards the shadow. The shadow cackles and surges the tails at you knowing you've just tossed away your only means of defending yourself. You recognize that perhaps that wasn't the best idea you've ever had and close your eyes bracing for impact......\n\n but instead you open your ears to the sound of the shadow angrily screeching. the blade landed into the murky waters wrapped around the shadows legs, and all the remaining tails seem to have fallen down. The shadow screeches and jumps out of the water, near instantly gets infront of you and slams you across the room before vanishing through the passageway you've yet to traverse\n")
								Stats["Exp"]+=100
								Stats = swordCheckLvl(Stats, curHealth, curStam, StamBar)
								(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
								return(Stats, curHealth, curStam, StamBar)
							else:
								choice = input("\nPlease input '8' or '6'\n")
					else:
						choice = input("Please input '8' or '6'\n\n")
			elif choice == "8":
				#dash forward, 6 tails
				print("\nYou dash forward at the shadow and it slams all 6 remaining tails into you one at a time in quick succession. You were able to swipe your blade through the first two and the waters dropped to the floor, but the reamining four slammed you down.\n")
				#4 tails left
				curHealth = takeDamage(6, Stats, curHealth)
				if curHealth == 0:
					print("\ntails whirling around overhead, you lie on your back and slowly fade out of consciousness.\n")
					SystemExit()
				else:
					print("\nYou took 6 damage, you have ", curHealth, " health left.\n")
					loop = 0
					choice = input("\nYou get up off the ground, and square up again. Do you want to try dashing in again or play it safer?\n8.) Dash again\n6.) Play it safe\n\n")
					while loop == 0:
						if choice == "8":
							loop+=1
							print("\nYou start to charge forth again and the scene starts to play out the same as before, however you're prepared this time and there are fewer tails to fight through. You succeed, barely, in knocking away all 4 tails, but while you're stumbling and off balance the shadow changes chape into a dark mist and bolts down the passageway you've yet to travel down with a fading shreek\n\n")
							print("\n\nYou gained 100 exp!")
							Stats["Exp"]+=100
							Stats = swordCheckLvl(Stats, curHealth, curStam, StamBar)
							(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
							return(Stats, curHealth, curStam, StamBar)
						elif choice == "6":
							loop+=1
							print("\nYou set yourself in a firm stance and wait for the shadow to make the next move. In time the shadow grows impatient and starts creeping the tails along the floor like snakes around you. The tip of the tails rise up from the ground and feign launching at you, over time starting to unnerve you and get you off your footing. Eventually one of the tails commits to the attack while your watching another tail and knocks you down. While your down all 4 tails simultaneously start to slam into you repeatedly\n")
							curHealth = takeDamage(10, Stats, curHealth)
							if curHealth == 0:
								print("\nThe tails pound at you until you're body is unrecognizable as a human corpse.\n")
								SystemExit()
							else:
								print("\nYour brain starts to shut out the repetitive pain and you collect yourself enough to tighten your grip on the hilt of your blade and suddenly turn and slash down all 4 tails at once. The shadow screeches and turns into a dark mist before vanishing down the passageway you haven't traveled through yet.\n")
								print("\n\nYou gained 100 exp!")
								Stats["Exp"]+=100
								Stats = swordCheckLvl(Stats, curHealth, curStam, StamBar)
								(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
								return(Stats, curHealth, curStam, StamBar)
						else:
							choice = input("\nPlease input '8' or '6'\n\n")
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
				RatCurrentStam = fatigueStatus((6-RatStats["Stam"]), RatStamBar, RatCurrentStam)
				curStam = fatigueStatus(-Stats["Stam"], StamBar, curStam)
				statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
			else:
				print("\nThe rat is busy panting and doesn't attack\n")
				RatCurrentStam = fatigueStatus(-2*RatStats["Stam"], RatStamBar, RatCurrentStam)
				curStam = fatigueStatus(-Stats["Stam"], StamBar, curStam)
				statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
		elif choice == "8":
			if curStam >= 6:
				RatCurrentHealth = takeDamage((Stats["Atk"] - RatStats["Def"]), RatStats, RatCurrentHealth)
				curStam = fatigueStatus((6-Stats["Stam"]), StamBar, curStam)
				if RatCurrentStam >= 6:
					curHealth = takeDamage(RatStats["Atk"] - Stats["Def"], Stats, curHealth)
					RatCurrentStam = fatigueStatus((6-RatStats["Stam"]), RatStamBar, RatCurrentStam)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
				else:
					print("\nThe rat sluggishly takes the blow\n")
					RatCurrentStam = fatigueStatus(-RatStats["Stam"]*2, RatStamBar, RatCurrentStam)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
			else:
				print("\nYou are too fatigued to attack\n")
		elif choice == "4":
			if curStam >= (StamBar-3):
				print("\nYou've no need to rest now.\n")
			else:
				curStam = fatigueStatus(-2*Stats["Stam"], Stambar, curStam)
				if RatCurrentStam >= 6:
					curHealth = takeDamage((RatStats["Atk"] - Stats["Def"]), Stats, curHealth)
					RatCurrentStam = fatigueStatus((6-RatStats["Stam"]), RatStamBar, RatCurrentStam)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
				else:
					print("\nYou both sink down and breathe heavily eyeing each other in anticipation\n")
					RatCurrentStam = fatigueStatus(-2*RatStats["Stam"], RatStamBar, RatCurrentStam)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
		elif choice == "2":
			print("\nYou haven't learned a skill yet\n")
		else:
			choice = input("\nPlease input '8' '6' '4' or '2'\n")
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
	loop = 0
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



def map1():

	#Map information
	map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
		    [0, 0, 0, 0, 1, 0, 0, 0, 0],
		    [0, 0, 0, 1, 1, 1, 0, 0, 0],
		    [0, 0, 1, 1, 1, 1, 25, 0, 0],
		    [0, 0, 0, 1, 23, 1, 0, 0, 0],
		    [0, 0, 0, 0, 1, 0, 0, 0, 0],
		    [0, 0, 0, 0, 24, 0, 0, 0, 0],
		    [0, 0, 0, 0, 1, 0, 0, 0, 0],
		    [0, 0, 0, 0, 1, 0, 0, 0, 0],
		    [0, 0, 0, 0, 20, 0, 0, 0, 0],
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
	inventory = Inventory
	heldInventory = HeldInventory


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
				curY+=1

			elif map1[curY+1][curX] == 20:
				curY+=1
				if ratKilled == False and hasDug == False:
					(Stats, curHealth, curStam, StamBar, hasSword) = digStart(Stats, curHealth, curStam, StamBar, hasSword)
					hasDug = True
				elif enteredClearing == True and hasSword == False and hasDug2 == False:
					(Stats, curHealth, curStam, StamBar, hasSword) = digDisillusioned(Stats, curHealth, curStam, StamBar, hasSword)
					hasDug2 = True

			elif map1[curY+1][curX] == 23:
				curY+=1
		
			elif map1[curY+1][curX] == 24:
				curY+=1
				if ratKilled == True and disillusioned == True and seenDisillusionedRat == False:
					print("Cautiously sneaking past the burrow the rat emerged from earlier you notice the corpse of the rat looks much less feral than before, almost friendly and well groomed.... ")
					seenDisillusionedRat = True
		
		#Moving Up

		elif move == "8":
			
			if curY == 1 or map1[curY-1][curX] == 0:
				print("\nCannot move up")
			
			elif map1[curY-1][curX] == 1:
				curY-=1 
			
			elif map1[curY-1][curX] == 23:
				curY-=1
				if hasSword == False and enteredClearing == False:
					(Stats, curHealth, curStam, StamBar, hasSword, disillusioned) = clearingIllusions(Stats, curHealth, curStam, StamBar, hasSword, disillusioned)
					enteredClearing = True
				elif hasSword == True and enteredClearing == False:
					(Stats, curHealth, curStam, StamBar) = clearingNoIllusions(Stats, curHealth, curStam, StamBar)
					enteredClearing = True
				elif enteredClearing == True and disillusioned == True and seenMaidenLeave == False:
					seenMaidenLeave == True
					print("\nYou note that the statue and the waters from before are missing now.\n")
			
			elif map1[curY-1][curX] == 24:
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
				curX+=1
			
			elif map1[curY][curX+1] == 25:
				curX+=1
				if hasSword == True and firstMaidenDead == True:
					print("This waters gross..")
		

		#Moving Left

		elif move == "4":
			
			if curX == 1 or map1[curY][curX-1] == 0:
				print("\nCannot move left")
			
			else:
				curX-=1
		

		#Correcting

		else:
			print("Please input '8' '6' '4' or '2'")
	


	shownMap = printEnvironment(map1, shownMap, curY, curX, lastRow, lastCol)
	print("\n\n"+shownMap["0-0"]+shownMap["0-1"]+shownMap["0-2"]+shownMap["0-3"]+shownMap["0-4"]+shownMap["0-5"]+shownMap["0-6"]+shownMap["0-7"]+shownMap["0-8"]+"\n"+shownMap["1-0"]+shownMap["1-1"]+shownMap["1-2"]+shownMap["1-3"]+shownMap["1-4"]+shownMap["1-5"]+shownMap["1-6"]+shownMap["1-7"]+shownMap["1-8"]+"\n"+shownMap["2-0"]+shownMap["2-1"]+shownMap["2-2"]+shownMap["2-3"]+shownMap["2-4"]+shownMap["2-5"]+shownMap["2-6"]+shownMap["2-7"]+shownMap["2-8"]+"\n"+shownMap["3-0"]+shownMap["3-1"]+shownMap["3-2"]+shownMap["3-3"]+shownMap["3-4"]+shownMap["3-5"]+shownMap["3-6"]+shownMap["3-7"]+shownMap["3-8"]+"\n"+shownMap["4-0"]+shownMap["4-1"]+shownMap["4-2"]+shownMap["4-3"]+shownMap["4-4"]+shownMap["4-5"]+shownMap["4-6"]+shownMap["4-7"]+shownMap["4-8"]+"\n"+shownMap["5-0"]+shownMap["5-1"]+shownMap["5-2"]+shownMap["5-3"]+shownMap["5-4"]+shownMap["5-5"]+shownMap["5-6"]+shownMap["5-7"]+shownMap["5-8"]+"\n"+shownMap["6-0"]+shownMap["6-1"]+shownMap["6-2"]+shownMap["6-3"]+shownMap["6-4"]+shownMap["6-5"]+shownMap["6-6"]+shownMap["6-7"]+shownMap["6-8"]+"\n"+shownMap["7-0"]+shownMap["7-1"]+shownMap["7-2"]+shownMap["7-3"]+shownMap["7-4"]+shownMap["7-5"]+shownMap["7-6"]+shownMap["7-7"]+shownMap["7-8"]+"\n"+shownMap["8-0"]+shownMap["8-1"]+shownMap["8-2"]+shownMap["8-3"]+shownMap["8-4"]+shownMap["8-5"]+shownMap["8-6"]+shownMap["8-7"]+shownMap["8-8"]+"\n"+shownMap["9-0"]+shownMap["9-1"]+shownMap["9-2"]+shownMap["9-3"]+shownMap["9-4"]+shownMap["9-5"]+shownMap["9-6"]+shownMap["9-7"]+shownMap["9-8"]+"\n"+shownMap["10-0"]+shownMap["10-1"]+shownMap["10-2"]+shownMap["10-3"]+shownMap["10-4"]+shownMap["10-5"]+shownMap["10-6"]+shownMap["10-7"]+shownMap["10-8"]+"\n\n")
	map2(Stats, curHealth, curStam, StamBar, inventory, Inventory, hasSword, disillusioned)


map1()
