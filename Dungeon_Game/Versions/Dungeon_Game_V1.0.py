#Written by Robert W. Radford
#V1.0
#21Jan2020

#Hero's status
TeroLvl = 1
TeroExp = 0 
TeroAtk = 4
TeroDef = 2
TeroStam = 3
TeroHealth = 25
TeroStamBar = TeroStam*10
TeroFatigue = 0
TeroCurrentStam = TeroStamBar
TeroCurrentHealth = TeroHealth
ExpPoint = 50
ExpToLevel = ExpPoint - TeroExp

#Hero's sword status
swordLvl = 1
swordExp = 0 
swordAtk = 12
swordDef = 6
swordStam = 4
swordHealth = 40
swordStamBar = swordStam*10
swordFatigue = 0
swordCurrentStam = swordStamBar
swordCurrentHealth = swordHealth
swordPoint = 50
swordToLevel = swordPoint - swordExp       

#functionality variables
loop1 = 0

#status for rat
RatAtk = 6
RatDef = 2
RatStam = 1.5
RatStamBar = RatStam*10
RatFatigue = 0
RatCurrentStam = RatStamBar
RatHealth = 20
RatDamage = 0
RatCurrentHealth = RatHealth

#Regularly called text
combatInvalidChoice = "Please choose from the available actions 'attack' 'defend' 'rest' 'run'"
combatTutorial="You can type, 'attack' to attack the opponent, 'defend' to reduce your damage received,\n'rest' to get double stamina returned, 'run' to flee if eligible.\n"
def TeroStatus():
        global TeroLvl
        global TeroAtk
        global TeroDef
        global TeroCurrentHealth
        global TeroHealth
        global TeroCurrentStam
        global TeroStamBar
        print("\n\nLevel: " + str(TeroLvl) + "\nAttack: " + str(TeroAtk) + "\nDefense: " + str(TeroDef) + "\nHealth: " + str(TeroCurrentHealth) + "/" + str(TeroHealth) + "\nStamina: " + str(TeroCurrentStam) + "/" + str(TeroStamBar) + "\n\n")

def swordStatus():
        global swordLvl
        global swordAtk
        global swordDef
        global swordCurrentHealth
        global swordHealth
        global swordCurrentStam
        global swordStamBar
        print("\n\nLevel: " + str(swordLvl) + "\nAttack: " + str(swordAtk) + "\nDefense: " + str(swordDef) + "\nHealth: " + str(swordCurrentHealth) + "/" + str(swordHealth) + "\nStamina: " + str(swordCurrentStam) + "/" + str(swordStamBar) + "\n\n")


#StatusAdjustmentFunctions

def CheckLvl():
	global TeroLvl
	global TeroExp
	LvlPre = TeroLvl
	print(LvlPre)
	if TeroExp < 50:
		TeroLvl = 1
	elif TeroExp < 100:
		TeroLvl = 2
	elif TeroExp < 150:
		TeroLvl = 3
	elif TeroExp < 250:
		TeroLvl = 4
	elif TeroExp < 400:
		TeroLvl = 5
	elif TeroExp < 600:
		TeroLvl = 6
	elif TeroExp < 1000:
		TeroLvl = 7
	else:
		TeroLvl = 8
	LvlNow = TeroLvl
	print(LvlNow)
	if LvlPre != LvlNow:
		print("Congratulations! Leveled up")
		global ExpPoint
		if TeroLvl==1:
			ExpPoint=50
		elif TeroLvl==2:
			ExpPoint=100
		elif TeroLvl==3:
			ExpPoint=150
		elif TeroLvl==4:
			ExpPoint=250
		elif TeroLvl==5:
			ExpPoint=400
		elif TeroLvl==6:
			ExpPoint=600
		else:
			TeroLvl=7
			ExpPoint=1000
		global ExpToLevel
		ExpToLevel = ExpPoint - TeroExp
		print("Exp to next level: " + str(ExpToLevel))
		NewStats()

def NewStats():
	global TeroAtk
	global TeroLvl
	if TeroLvl == 2:
		TeroAtk = 6
	elif TeroLvl == 3:
		TeroAtk = 9
	elif TeroLvl == 4:
		TeroAtk = 12
	elif TeroLvl == 5:
		TeroAtk = 15
	elif TeroLvl == 6:
		TeroAtk = 18
	elif TeroLvl == 7:
		TeroAtk = 22
	elif TeroLvl == 8:
		TeroAtk = 28
	global TeroDef
	if TeroLvl == 2:
		TeroDef = 3
	elif TeroLvl == 3:
		TeroDef = 4
	elif TeroLvl == 4:
		TeroDef = 6
	elif TeroLvl == 5:
		TeroDef = 8
	elif TeroLvl == 6:
		TeroDef = 11
	elif TeroLvl == 7:
		TeroDef = 14
	elif TeroLvl == 8:
		TeroDef = 18
	global TeroStam
	if TeroLvl == 1:
		TeroStam = 3
	elif TeroLvl == 2:
		TeroStam = 3
	elif TeroLvl == 3:
		TeroStam = 3
	elif TeroLvl == 4:
		TeroStam = 3
	elif TeroLvl == 5:
		TeroStam = 4
	elif TeroLvl == 6:
		TeroStam = 5
	elif TeroLvl == 7:
		TeroStam = 6
	elif TeroLvl == 8:
		TeroStam = 8
	global TeroHealth
	if TeroLvl == 2:
		TeroHealth = 30
	elif TeroLvl == 3:
		TeroHealth = 35
	elif TeroLvl == 4:
		TeroHealth = 45
	elif TeroLvl == 5:
		TeroHealth = 60
	elif TeroLvl == 6:
		TeroHealth = 80
	elif TeroLvl == 7:
		TeroHealth = 100
	elif TeroLvl == 8:
		TeroHealth = 135
	TeroStatus()

def swordCheckLvl():
	global swordLvl
	global swordExp
	LvlPre = swordLvl
	print(LvlPre)
	if swordExp < 50:
		swordLvl = 1
	elif swordExp < 100:
		swordLvl = 2
	elif swordExp < 150:
		swordLvl = 3
	elif swordExp < 250:
		swordLvl = 4
	elif swordExp < 400:
		swordLvl = 5
	elif swordExp < 600:
		swordLvl = 6
	elif swordExp < 1000:
		swordLvl = 7
	else:
		swordLvl = 8
	LvlNow = swordLvl
	print(LvlNow)
	if LvlPre != LvlNow:
		print("Congratulations! Leveled up")
		global swordPoint
		if swordLvl==1:
			swordPoint=50
		elif swordLvl==2:
			swordPoint=100
		elif swordLvl==3:
			swordPoint=150
		elif swordLvl==4:
			swordPoint=250
		elif swordLvl==5:
			swordPoint=400
		elif swordLvl==6:
			swordPoint=600
		else:
			swordLvl=7
			swordPoint=1000
		global swordToLevel
		swordToLevel = swordPoint - swordExp
		print("Exp to next level: " + str(swordToLevel))
		swordNewStats()

def swordNewStats():
	global swordAtk
	global swordLvl
	if swordLvl == 2:
		swordAtk = 18
	elif swordLvl == 3:
		swordAtk = 27
	elif swordLvl == 4:
		swordAtk = 36
	elif swordLvl == 5:
		swordAtk = 45
	elif swordLvl == 6:
		swordAtk = 54
	elif swordLvl == 7:
		swordAtk = 66
	elif swordLvl == 8:
		swordAtk = 84
	global swordDef
	if swordLvl == 2:
		swordDef = 9
	elif swordLvl == 3:
		swordDef = 12
	elif swordLvl == 4:
		swordDef = 18
	elif swordLvl == 5:
		swordDef = 24
	elif swordLvl == 6:
		swordDef = 33
	elif swordLvl == 7:
		swordDef = 42
	elif swordLvl == 8:
		swordDef = 54
	global swordStam
	if swordLvl == 1:
		swordStam = 4
	elif swordLvl == 2:
		swordStam = 4
	elif swordLvl == 3:
		swordStam = 4
	elif swordLvl == 4:
		swordStam = 4
	elif swordLvl == 5:
		swordStam = 5
	elif swordLvl == 6:
		swordStam = 7
	elif swordLvl == 7:
		swordStam = 9
	elif swordLvl == 8:
		swordStam = 11
	global swordHealth
	if swordLvl == 2:
		swordHealth = 50
	elif swordLvl == 3:
		swordHealth = 60
	elif swordLvl == 4:
		swordHealth = 80
	elif swordLvl == 5:
		swordHealth = 100
	elif swordLvl == 6:
		swordHealth = 130
	elif swordLvl == 7:
		swordHealth = 160
	elif swordLvl == 8:
		swordHealth = 200
	swordStatus()

def TeroTakeDamage(TeroDamage):
	global TeroCurrentHealth
	TeroCurrentHealth = min(max(TeroCurrentHealth - TeroDamage, 0), TeroHealth)

def TeroFatigueStatus(TeroFatigue):
	global TeroCurrentStam
	TeroCurrentStam = min(max(TeroCurrentStam - TeroFatigue, 0), TeroStamBar)

def swordTakeDamage(swordDamage):
	global swordCurrentHealth
	swordCurrentHealth = min(max(swordCurrentHealth - swordDamage, 0), swordHealth)

def swordFatigueStatus(swordFatigue):
	global swordCurrentStam
	swordCurrentStam = min(max(swordCurrentStam - swordFatigue, 0), swordStamBar)

def maidenEncounter():
	global TeroCurrentHealth
	global TeroCurrentStam
	global TeroHealth
	global TeroStamBar
	TeroCurrentHealth = min(max(TeroCurrentHealth + TeroHealth, 0), TeroHealth)
	TeroCurrentStam = min(max(TeroCurrentStam + TeroStamBar, 0), TeroStamBar)
	TeroStatus()

def restRecovery():
	global TeroCurrentHealth
	global TeroCurrentStam
	global TeroHealth
	global TeroStamBar
	TeroCurrentHealth = min(max(TeroCurrentHealth + (TeroHealth/2), 0), TeroHealth)
	TeroCurrentStam = min(max(TeroCurrentStam + (TeroStamBar/2), 0), TeroStamBar)
	TeroStatus()

def swordRestRecovery():
	global swordCurrentHealth
	global swordCurrentStam
	global swordHealth
	global swordStamBar
	swordCurrentHealth = min(max(swordCurrentHealth + (swordHealth/2), 0), swordHealth)
	swordCurrentStam = min(max(swordCurrentStam + (swordStamBar/2), 0), swordStamBar)
	swordStatus()

def RatTakeDamage(RatDamage):
	global RatCurrentHealth
	RatCurrentHealth = min(max(RatCurrentHealth - RatDamage, 0), RatHealth)

def RatFatigueStatus(RatFatigue):
	global RatCurrentStam
	RatCurrentStam = min(max(RatCurrentStam - RatFatigue, 0), RatStamBar)

#EncounterFunctions
def cavern2Illusions():
	print("yo")

def cavern2Disillusioned():
	print("yo")

def cavern2NoIllusions():
	print("yo")

def cavern2HalfIllusions():
	print("yo")

def ratFight():
	print("As you walk along the passageway you notice a large hole near the ground ahead on your right side.\nYou cautiously approach and peer in but can't see anything but darkness.\nYou begin to walk along your path again, but short after feel a sudden chill.\nNervously you peer slowly over your shoulder and spot a shadow a couple feet long, and it begins to snarl back at you.\nAs it approaches to strike you get a more clear picture, it is an immense rat with tufts of fur missing and jagged teeth.\nIn this cavern you don't think you'll be able to outrun it and fearfully prepare to fight for your life.\n\n")
	print(combatTutorial)
	def statProgress():
		print("Rat HP:      " + str(RatCurrentHealth) + "                     " + "Tero HP:      " + str(TeroCurrentHealth))
		print("Rat Stamina: " + str(RatCurrentStam) + "                   " + "Tero Stamina: " + str(TeroCurrentStam))
	statProgress()
	while RatCurrentHealth > 0 and TeroCurrentHealth > 0:
		choice = input("The rat is gnarling viciously, what action will you take?\n")
		if choice == "defend":
			if RatCurrentStam >= 6:
				TeroTakeDamage(((RatAtk - TeroDef)//2))
				RatFatigueStatus(6)
				RatFatigueStatus(-RatStam)
				TeroFatigueStatus(-TeroStam)
				statProgress()
			else:
				print("The rat is busy panting and doesn't attack")
				RatFatigueStatus(-2*RatStam)
				statProgress()
		elif choice == "attack":
			if TeroCurrentStam >= 6:
				RatTakeDamage(TeroAtk - RatDef)
				TeroFatigueStatus(6)
				TeroFatigueStatus(-TeroStam)
				if RatCurrentStam >= 6:
					TeroTakeDamage(RatAtk - TeroDef)
					RatFatigueStatus(6)
					RatFatigueStatus(-RatStam)
					statProgress()
				else:
					print("The rat sluggishly takes the blow")
					RatFatigueStatus(-RatStam*2)
					statProgress()
			else:
				print("You are too fatigued to attack")
		elif choice == "rest":
			if TeroCurrentStam >= (TeroStamBar-3):
				print("You've no need to rest now.")
			else:
				TeroFatigueStatus(-2*TeroStam)
				if RatCurrentStam >= 6:
					TeroTakeDamage(RatAtk - TeroDef)
					RatFatigueStatus(6)
					RatFatigueStatus(-RatStam)
					statProgress()
				else:
					print("You both sink down and breathe heavily eyeing each other in anticipation")
					RatFatigueStatus(-2*RatStam)
					statProgress()
		elif choice == "run":
			print("You cannot escape in these tight caverns")
		else:
			print(combatInvalidChoice)
	if TeroCurrentHealth <= 0:
		print("You feel the warmth of your own blood leaving your insides and running across your flesh.\nYou come to terms with the fact that you died not knowing who you are or how you got to this cave, food for a feral rat creature.")
		SystemExit()
	else:
		print("\nYou're shaking from a mix of blood loss and adrenaline as you stand over the now dead rat.\n")
		global TeroExp
		TeroExp += 50
		print("Gained 50 exp!")
		CheckLvl()

def firstMaidenFight():
	print("yo")


def main():
	loop1 = 0
	move=input("You wake up naked and alone in a cave system.\nLooking around, you see a narrow passageway in front and behind you.\nFrom behind you theres a constant low ringing sound but you can only make out a caved in wall of rocks, in front of you is a silent and empty, dark passgeway.\nDo you want to progress forward or dig through the rocks?\n")	
	while loop1 == 0:
		if move == "progress":
			loop1+=1
			ratFight()
			move=input("\n\nYou quickly shuffle forward to get distance from the burrow fearful there may be more creatures yet inside.\nYour body rings out in agonizing pain missing chunks of flesh and losing blood fast but still you progress.\nAhead you see a blinding light amidst the darkness.\nWhen you cross into the light and your vision adjusts you a see a spacious circular room with the narrow pathway you came from behind you and another similar continuation on the other side of the room.\nThe right side of the floor seems to be all water and lining the of the wall rather than cavern walls of rock is a glistening polished white marble with an occasional lit torch along it.\nIn front of the center of the wall amidst the bath stands a life sized marble statue of young maiden shedding a single tear.\nAs you lock eyes with the statue you feel a strong urge to get into the water and the intensity of the pain you feel from each of your wounds increases immensely more and more each second.\nPeel away from the statues gaze and move on in the caverns or accept its call and join it in the waters?\n")	
			while loop1 < 2:
				if move == "accept":
					loop1+=1
					print("As you step into the water you can see the single tear on the maiden change form from stone to liquid and drip into the water.\nThe water begins to feel warmer and you notice a slight shimmer along the surface.\nSuddenly the water bursts into a glaring golden color and rises up around you, encapsualting you in it.\nAt first you struggle against the water in fear of drowning but as you flail around you see that your wounds are closing up and as though you've never endured a hardship in your life.\nYou give in to the comforting aura and let out a gasp to find you can still breathe.\n")
					maidenEncounter()
					print("The shimmering gold color settles and slowly fades in the water around you and soon it all falls to the pool again beneath you.\nSuddenly two torches flare up on either side of the entrance to the narrow passageway across from where you entered this opening.\nYou glance back to the statue of the maiden and see that it has changed and she is smiling sweetly now instead of crying, and holds an arm up pointing to the passageway. You take hold of the meaning and venture forth into the cavern again.\n")
					cavern2Illusions()
				elif move == "peel away":
					loop1+=1
					print("You peel your eyes away from the maidens and step back, suddenly you feel a horrendous stinging pain all across your body and you're certain it isn't from your existing wounds.\nYou fumble in agony and lose your footing until you collapse against the wall opposite the pool of water, when you open your eyes and glance back at the pool the maiden statue appears different.\nShe now has an arm raised pointing at you, and the other into the waters with a stern frown and sharp eyes.\n")
					TeroTakeDamage(2)
					print("The stinging pain running along your skin takes its toll, your health drops to ",TeroCurrentHealth,"\n")
					if TeroCurrentHealth < 1:
						print("Your body goes limp and your vision fades away. The lashing pain you suddenly felt untop added to your existing wounds proved fatal.")
						SystemExit()
					move = input("Do you accept the demand or ignore it?\n")
					while loop1 < 3:
						if move == "accept":
							print("Fearfully you crawl to the waters, roll yourself in, and sink down.\nYou feel your wounds and pain fading from your body, the holes of flesh bitten off of you sealing up.\nLifelessly you lay at the bottom of the pool, but as the last of your wounds seals itself and you still lie there the water itself surges and throws you beside the pools edge.\nAfter a fit of coughing for a moment you look up and see that again the statue has changed and now stands hands down and cupped together, face directed at the passage way youve yet ventured in with a beaming smile.\nTorches on either side of the entrance flare up and you collect yourself and venture into it hesitantly taking glances at the statue behind you.\n")
							loop1+=1
							maidenEncounter()
							cavern2Illusions()
						elif move == "ignore":
							loop1+=1
							print("The stinging pain you felt before intensifies to what can only be described as the most horrendously agonizing sensation you've ever felt in your life.\nWere you to lacerate your own body along every inch of it, douse yourself with a batch of a citrusy liquid, and then light yourself ablaze, even still it could not compare the pain ringing out across your entire body.\nYou freeze in place, the pain so great your brain entirely shut down to protect you from going insane.\nWhile your mind is blacked out from reality your consciousness drifts into a vision like a sort of dream.\nYou see a family around a table, amongst them is an individual that resembles yourself, perhaps more groomed in appearance with a little more fat on your build and slightly less aged but it's certainly the same face you saw looking back in the pond before.\nThe whole family seems to be enjoying themself bantering and sharing a moment together yet everytime theres a lull you can read an expression of terror across their faces.\nYou hear a knocking at the door a few meters from the table and see everyones face freeze up besides your own look alike.\n They push their seat away from the table, stand, and walk to another room within the small home before returning with a sword tucked into a scabbard and held down into it with chains.\nBefore they open the door they pull on the handle as if to draw the blade and although the chains prevent that it does partially click out of the scabbard and reveal a shimmering silver blade that resonates out a calming ringing sound.\nThey stare for a moment then click it back in and opens the front door, through which you view a gathering of men with black cloaks, silver garnished, with a bright silver mask.\nThe apparent leader of the group stands ahead of the others, adorned with even more silver decorations along their cloak and mask, and gestures your double to join them.\nAfter they do, the leader extends his arms out infront of himself and peers at the blade they hold.\nThey clench their fist and grimace, but still lay the blade across the leaders arms, after which the others form a circle around them and start walking away and the leader peers in on the family for a while before shutting the door.\nThe family all hurriedly clusters together and seem to be grieving in eachothers arms...\nAs you wonder why?, what happened to your lookalike?, who were those cloaked people? and so many more questions you start to come back into reality and scream out at the pain across your body.\nIt's died down and is no longer even a fraction of what it had been but still the pain is agonizing and your snaps out of the dreamlike sight you had viewed before and the memory of it becomes fuzzy.\nYou recollect yourself mentally and stand shakily, before lies the pond full of black waters with the statue showing an incredibly angered face directed at you.\n To your right is the passage you came from, and as you peer into its darkness you hear the same faint ringing you heard before.\nTo your left the passageway you've yet to venture into, silent and dark as the abyss.\n")
							TeroTakeDamage(4)
							print("The agonizing pain ringing across your body finally comes to a stop but it's certainly left its mark, your health falls to ",TeroCurrentHealth,"\n")
							if TeroCurrentHealth < 1:
								print("Your vision starts to go fuzzy and fade out and your body goes limp. For a moment you think you are going to see more of this dreamscape you peered into before, however you quickly come to terms with the fact that this is not the case but rather your life itself is coming to an end.")
								SystemExit()
							move = input("Do you finally embrace the waters, head back the way you came, or progress through the caverns?\n")
							while loop1 < 4:
								if move == "embrace":
									loop1+=1
									print("You wade into the black waters and watch as a shadowy mist wraps around the statue and change its appearance to a beaming smile and holding it's hands up and together like in prayer.\nThe water wraps around your body and all of your wounds and your fatigue are cured, you can see where your wounds had been is a flowing black fluid joining and mixing into the lighter black water.\nWhen you're fully recovered the water falls back into the pool splashing around you and again you see a shadowy mist wrap around the statue and change it to be looking fondly at the passageway you haven't traversed through and pointing an arm to it.\n")
									maidenEncounter()
									cavern2HalfIllusions()
								elif move == "head back":
									loop1+=1
									move = input("Curious about the ringing noise you've been hearing you head back to where you came from and follow the noise.\nCautiously sneaking past the burrow the rat emerged from earlier you notice the corpse of the rat looks much less feral than before, almost friendly well groomed....\nMaking it back to where the cave seems to have given in you look at the pile of boulders and rocks, and hear that low ringing thunderously rolling out from the cracks.\nDo you begin digging out rocks or turn away?\n")
									while loop1 < 5:
										if move == "dig":
											loop1+=1
											print("You struggle to pull out rock after rock from the pile honing in on the origin of the sound.\nYour hands start to bleed and ache as you work through the rocks but it's nothing compared to the pain from the clearing earlier and you keep digging through.\nThe ringing becomes higher and higher pitched as you remove more rocks around it and eventually you see a couple broken chain links scattered aroud and pick up your pace.\nFinally you unveil a shimmering silver blade and pick it out of the rubble.\nThe ring intensifies and resonates inside of your body and mind, meanwhile the silver blade glows white brighter and brighter by the second until you can no longer see anything but white around you, and then suddenly the light fades out and the ringing stops.\nYou look at the blade and a white sheen dances along the surface with a gentle sound resonating quietly for only a brief moment and then its nothing more than a beautifully smithed sword.\nGripping the sword tightly you feel a new energy flowing through you!\n")
											swordRestRecovery()
											print("Feeling invigorated you confidently walk into the next passageway, noting along the way the statue in the waters from before is missing now.")
											cavern2NoIllusions()
										elif move == "turn back":
											print("Listening to the resonating sound calling out for you from under the rubble you stop and decide maybe you would be better off leaving it in its place.\nYou rest for a moment and then head back the clearing and into the caverns ahead.\n")
											loop1+=1
											restRecovery()
											cavern2Disillusioned()
										else:
											move = input("please input 'dig' or 'turn back'\n")
								elif move == "progress":
									loop1+=1
									print("You decide to continue your path down the next passageway, but before setting down it decide that you should first rest and tend to your wound a little.\n")
									restRecovery()
									print("Feeling at least a little bit better you pick yourself up and slowly progress into the next passageway.\n")
									cavern2Disillusioned()
								else:
									move = input("please answer 'embrace', 'head back', or 'progress'\n") 
						else:
							move = input("Please answer 'accept' or 'ignore'\n")
				else:
					move = input("Please answer 'peel away' or 'accept'\n")
				 
		elif move == "dig":
			loop1+=1
			move = input("You eye up the mound of rocks and boulders and designate a few that you feel you can pull out from the weight of the others.\nAs you start to work them out all you seem to be achieving is having more rocks come down in their place from the collapsed ceiling.\nDo you want to continue digging into the rocks or give up?\n")
			while loop1 == 1:
				if move == "continue":
					loop1+=1
					print("As you peel out rocks a large rock falls down on top of you and strikes the back of your head.")
					TeroTakeDamage(4)
					print("Your health drops 4 points, it is now ",TeroCurrentHealth)
					move = input("Do you still continue or give up?\n")
					while loop1 == 2:
						if move == "continue":
							loop1+=1
							print("You dig feverishly thorugh the pile and the ringing you've been hearing resonates in a higher and higher tone as you do so, several stones into the process you notice the skin wearing off of your hands rubbing them raw.")
							TeroTakeDamage(2)
							print("Your health drops another 2 points, it is now ",TeroCurrentHealth)
							move = input("Do you still continue or give up?\n")
							while loop1 == 3:
								if move == "continue":
									loop1+=1
									print("You finally uncover what appears to be a brilliantly crafted shimmering blade.\nHoisting it out of the heap you feel a warmth shoot out of the blade and into your hand and rippling through your body.\n")
									swordRestRecovery()
									print("You venture into the passage the other direction. Along the way you see a burrow in the cavern wall and a family of immense rats with smooth sleek coats of fur. As intimidating as these large creatures may be they seem friendly enough and they let you pass freely.\nFurther beyond you come into a spacious clearing between the passage you came from and another ahead of you.\n On the right half of the cave wall is a pool lined with marble, filled with black eerie waters, and at the far end of it is a shadowy figure shaped sort of like a woman with horns. As you notice this creature you close your grip around your sword tighter and stare, and the shadow breaks the stand still in the room with an angry shriek and the water around her stirs up.")
									firstMaidenFight()
								elif move == "give up":
									loop1+=1
									print("You give up on trying to work through all this rubble and turn back to go through the passage way behind you")
									ratFight()
								else:
									print("Please input 'continue' or 'give up'.")
						elif move == "give up":
							loop1+=1
							print("You give up on trying to work through all this rubble and turn back to go through the passage way behind you")
							ratFight()
						else:
							print("Please input 'continue' or 'give up'\n")
				elif move == "give up":
					loop1+=1
					print("You give up on trying to work through all this rubble and turn back to go through the passage way behind you")
					ratFight()
				else:
					move = input("Please input 'continue' or 'give up'\n")

		else:
			move = input("please answer 'progress' or 'dig'\n")

main()
