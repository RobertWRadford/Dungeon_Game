#Written by Robert W. Radford
#V1.0
#21Jan2020
#V1.1 - Split main() code into more functions to clear up clutter
#26Jan2020
#V2.0 - Stats changed to dictionary, and skills/items lists are added (not implemented)
#03Feb2020
#V2.5 - Resolved all global variables calls to local scope
#04Feb2020 

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

#hidden conditionals
firstMaidenDead = False
firstMaidenFought = False

#Regularly called text
combatInvalidChoice = "Please choose from the available actions 'attack' 'defend' 'rest' 'skills'"
combatTutorial="You can type, 'attack' to attack the opponent, 'defend' to reduce your damage received, 'rest' to get double stamina returned, or 'skills' to view your skills menu.\n"

def printStatus(Stats, curHealth, curStam, StamBar):
	print("\n\nLevel: " + str(Stats["Lvl"]) + "\nAttack: " + str(Stats["Atk"]) + "\nDefense: " + str(Stats["Def"]) + "\nHealth: " + str(curHealth) + "/" + str(Stats["Health"]) + "\nStamina: " + str(curStam) + "/" + str(StamBar) + "\n\n")

def statProgress(OppCurHealth, OppCurStam, curHealth, curStam):
	print("Opponent HP:      " + str(OppCurHealth) + "                     " + "Your HP:      " + str(curHealth))
	print("Opponent Stamina: " + str(OppCurStam) + "                   " + "Your Stamina: " + str(curStam) + "\n")

def TeroSkillMenu(Stats):
	tokens = TeroCurrentTokens
	if tokens == 0:
		return("none")
	else:
		n = TeroSkillTokens
		i = 0
		while i < n:
			print(Stats["Skills"][i]+" ")
		choice = input("You have ", tokens, " skill points left. What do you want to do?")
		return(choice)

def swordSkillMenu(Stats):
	tokens = swordCurrentTokens
	if tokens == 0:
		return("none")
	else:
		n = swordSkillTokens
		i = 0
		while i < n:
			print(Stats["Skills"][i]+" ")
		choice = input("You have ", tokens, " skill points left. What do you want to do?")
		return(choice)


#StatusAdjustmentFunctions
def CheckLvl(Stats):
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
		print("Congratulations! Leveled up")
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
		print("Exp to next level: " + str(expToLevel))
		NewStats(Stats)
		return(Stats)
	else:
		print("Exp to next level: " + str(expToLevel))
		return(Stats)

def NewStats(Stats):
	if Stats["Lvl"] == 2:
		Stats["Atk"] = 6
		Stats["Def"] = 3
		Stats["Stam"] = 3
		Stats["Health"] = 30
		#Heavy Blow deals 1.5* attack stat
		Stats["Skills"].append("Heavy Blow")
		print("You learned a new skill, Heavy Blow")

	elif Stats["Lvl"] == 3:
		Stats["Atk"] = 9
		Stats["Def"] = 4
		Stats["Stam"] = 3
		Stats["Health"] = 35
		#Counter skill blends pros of attack and defend
		Stats["Skills"].append("Counter")
		print("You learned a new skill, Counter")

	elif Stats["Lvl"] == 4:
		Stats["Atk"] = 12
		Stats["Def"] = 6
		Stats["Stam"] = 3
		Stats["Health"] = 45
		#Meditate skill restores 1.5* rest actions stam
		Stats["Skills"].append("Meditate")
		print("You learned a new skill, Meditate")

	elif Stats["Lvl"] == 5:
		Stats["Atk"] = 15
		Stats["Def"] = 8
		Stats["Stam"] = 4
		Stats["Health"] = 60
		#Pierce skill deals normal attack after reducing opponents def, stacks 3 times max
		Stats["Skills"].append("Shatter")
		print("You learned a new skill, Shatter")

	elif Stats["Lvl"] == 6:
		Stats["Atk"] = 18
		Stats["Def"] = 11
		Stats["Stam"] = 5
		Stats["Health"] = 80
		#Grapple does an attack selection ignoring the opponents input and dealing stamina damage instead of health
		Stats["Skills"].append("Grapple")
		print("You learned a new skill, Grapple")

	elif Stats["Lvl"] == 7:
		Stats["Atk"] = 22
		Stats["Def"] = 14
		Stats["Stam"] = 6
		Stats["Health"] = 100
		#Flurry uses 3-5 attacks in one turn, consequently 3-5 stamina lots however.
		Stats["Skills"].append("Flurry")
		print("You learned a new skill, Flurry")

	elif Stats["Lvl"] == 8:
		Stats["Atk"] = 28
		Stats["Def"] = 18       
		Stats["Stam"] = 8
		Stats["Health"] = 135
		#Atemi forces the opponent into its largest attack, and redirects it onto its self. 
		Stats["Skills"].append("Atemi")
		print("You learned a new skill, Atemi")
	return(Stats)

def swordCheckLvl(Stats):
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
		print("Congratulations! Leveled up")
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
		print("Exp to next level: " + str(sToLevel))
		swordNewStats(Stats)
		return(Stats)
	else:
		print("Exp to next level: " + str(sToLevel))
		return(Stats)


def swordNewStats(Stats):
	if Stats["Lvl"] == 2:
		Stats["Atk"] = 18
		Stats["Def"] = 10
		Stats["Stam"] = 4
		Stats["Health"] = 50
		#Datotsu skill is a 2 handed overhead strike that deals 1.5* normal attack damage
		Stats["Skills"].append("Datotsu")
		print("You learned a new skill, Datotsu")
	elif Stats["Lvl"] == 3:
		Stats["Atk"] = 27
		Stats["Def"] = 14
		Stats["Stam"] = 4
		Stats["Health"] = 60
		#Haya-suburi skill evades the opponents attack and deals out one attack damage
		Stats["Skills"].append("Haya-suburi")
		print("You learned a new skill, Haya-Suburi")
	elif Stats["Lvl"] == 4:
		Stats["Atk"] = 36
		Stats["Def"] = 19
		Stats["Stam"] = 4
		Stats["Health"] = 80
		#Mokuso restores 3* stam return
		Stats["Skills"].append("Mokuso")
		print("You learned a new skill, Mokuso")
	elif Stats["Lvl"] == 5:
		Stats["Atk"] = 45
		Stats["Def"] = 24
		Stats["Stam"] = 5
		Stats["Health"] = 100
		#pierce skill is normal attack ignoring opponent defense
		Stats["Skills"].append("Pierce")
		print("You learned a new skill, Pierce")
	elif Stats["Lvl"] == 6:
		Stats["Atk"] = 54
		Stats["Def"] = 32
		Stats["Stam"] = 7
		Stats["Health"] = 130
		#Drain skill uses blades magic to sap the opponents stamina
		Stats["Skills"].append("Drain")
		print("You learned a new skill, Drain")
	elif Stats["Lvl"] == 7:
		Stats["Atk"] = 66
		Stats["Def"] = 42
		Stats["Stam"] = 9
		Stats["Health"] = 160
		#Regenerate uses sword magic to heal self
		Stats["Skills"].append("Regenerate")
		print("You learned a new skill, Regenerate")
	elif Stats["Lvl"] == 8:
		Stats["Atk"] = 84
		Stats["Def"] = 54
		Stats["Stam"] = 11
		Stats["Health"] = 200
		#Kachinuki is a multi-round choice that locks in attacks until stamina is too low to attack, 
		#and prevents health going below 1 until resolved
		Stats["Skills"].append("Kachinuki")
		print("You learned a new skill, Kachinuki")	
	return(Stats)


def takeDamage(damage, Stats, curHealth):
	curHealth = min(max(curHealth - damage, 0), Stats["Health"])
	return(curHealth)


def fatigueStatus(fatigue, curStam, StamBar):
	curStam = min(max(curStam - fatigue, 0), StamBar)
	return(curStam)

def maidenEncounter(Stats, curHealth, curStam, StamBar):
	curHealth = min(max(curHealth + (Stats["Health"]), 0), Stats["Health"])
	curStam = min(max(curStam + StamBar, 0), StamBar)
	printStatus(Stats, curHealth, curStam, StamBar)
	return(curHealth, curStam)

def restRecovery(Stats, curHealth, curStam, StamBar):
	curHealth = min(max(curHealth + (Stats["Health"]/2), 0), Stats["Health"])
	curStam = min(max(curStam + (StamBar/2), 0), StamBar)
	printStatus(Stats, curHealth, curStam, StamBar)
	return(curHealth, curStam)


#EncounterFunctions
def cavern2Illusions(Stats, curHealth, curStam, StamBar):
	print("yo")



def cavern2Disillusioned(Stats, curHealth, curStam, StamBar):
	print("yo")



def cavern2NoIllusions(Stats, curHealth, curStam, StamBar):
	print("yo")



def cavern2HalfIllusions(Stats, curHealth, curStam, StamBar):
	print("yo")



def clearingIllusions(Stats, curHealth, curStam, StamBar):
	loop = 0
	move=input("\n\nYou quickly shuffle forward to get distance from the burrow fearful there may be more creatures yet inside. Your body rings out in agonizing pain missing chunks of flesh and losing blood fast but still you progress. Ahead you see a blinding light amidst the darkness. When you cross into the light and your vision adjusts you a see a spacious circular room with the narrow pathway you came from behind you and another similar continuation on the other side of the room. The right side of the floor seems to be all water and lining the of the wall rather than cavern walls of rock is a glistening polished white marble with an occasional lit torch along it. In front of the center of the wall amidst the bath stands a life sized marble statue of young maiden shedding a single tear. As you lock eyes with the statue you feel a strong urge to get into the water and the intensity of the pain you feel from each of your wounds increases immensely more and more each second. Peel away from the statues gaze and move on in the caverns or accept its call and join it in the waters?\n")	
	while loop == 0:
			if move == "accept":
				loop+=1
				print("As you step into the water you can see the single tear on the maiden change form from stone to liquid and drip into the water. The water begins to feel warmer and you notice a slight shimmer along the surface. Suddenly the water bursts into a glaring golden color and rises up around you, encapsualting you in it. At first you struggle against the water in fear of drowning but as you flail around you see that your wounds are closing up and as though you've never endured a hardship in your life. You give in to the comforting aura and let out a gasp to find you can still breathe.\n")
				(curHealth, curStam) = maidenEncounter(Stats, curHealth, curStam, StamBar) 
				print("The shimmering gold color settles and slowly fades in the water around you and soon it all falls to the pool again beneath you. Suddenly two torches flare up on either side of the entrance to the narrow passageway across from where you entered this opening. You glance back to the statue of the maiden and see that it has changed and she is smiling sweetly now instead of crying, and holds an arm up pointing to the passageway. You take hold of the meaning and venture forth into the cavern again.\n")
				cavern2Illusions(Stats, curHealth, curStam, StamBar)
			elif move == "peel away":
				loop+=1
				print("You peel your eyes away from the maidens and step back, suddenly you feel a horrendous stinging pain all across your body and you're certain it isn't from your existing wounds. You fumble in agony and lose your footing until you collapse against the wall opposite the pool of water, when you open your eyes and glance back at the pool the maiden statue appears different. She now has an arm raised pointing at you, and the other into the waters with a stern frown and sharp eyes.\n")
				curHealth = takeDamage(2, Stats, curHealth)
				print("The stinging pain running along your skin takes its toll, your health drops to ",curHealth,"\n")
				if TeroCurrentHealth < 1:
					print("Your body goes limp and your vision fades away. The lashing pain you suddenly felt untop added to your existing wounds proved fatal.")
					SystemExit()
				move = input("Do you accept the demand or ignore it?\n")
				while loop == 1:
					if move == "accept":
						print("Fearfully you crawl to the waters, roll yourself in, and sink down. You feel your wounds and pain fading from your body, the holes of flesh bitten off of you sealing up. Lifelessly you lay at the bottom of the pool, but as the last of your wounds seals itself and you still lie there the water itself surges and throws you beside the pools edge. After a fit of coughing for a moment you look up and see that again the statue has changed and now stands hands down and cupped together, face directed at the passage way youve yet ventured in with a beaming smile. Torches on either side of the entrance flare up and you collect yourself and venture into it hesitantly taking glances at the statue behind you.\n")
						loop+=1
						(Stats, curHealth, curStam, StamBar) = maidenEncounter(Stats, curHealth, curStam, StamBar)
						cavern2Illusions(Stats, curHealth, curStam, StamBar)
					elif move == "ignore":
						loop+=1
						print("The stinging pain you felt before intensifies to what can only be described as the most horrendously agonizing sensation you've ever felt in your life. Were you to lacerate your own body along every inch of it, douse yourself with a batch of a citrusy liquid, and then light yourself ablaze, even still it could not compare the pain ringing out across your entire body. You freeze in place, the pain so great your brain entirely shut down to protect you from going insane. While your mind is blacked out from reality your consciousness drifts into a vision like a sort of dream. You see a family around a table, amongst them is an individual that resembles yourself, perhaps more groomed in appearance with a little more fat on your build and slightly less aged but it's certainly the same face you saw looking back in the pond before. The whole family seems to be enjoying themself bantering and sharing a moment together yet everytime theres a lull you can read an expression of terror across their faces. You hear a knocking at the door a few meters from the table and see everyones face freeze up besides your own look alike. They push their seat away from the table, stand, and walk to another room within the small home before returning with a sword tucked into a scabbard and held down into it with chains. Before they open the door they pull on the handle as if to draw the blade and although the chains prevent that it does partially click out of the scabbard and reveal a shimmering silver blade that resonates out a calming ringing sound. They stare for a moment then click it back in and opens the front door, through which you view a gathering of men with black cloaks, silver garnished, with a bright silver mask. The apparent leader of the group stands ahead of the others, adorned with even more silver decorations along their cloak and mask, and gestures your double to join them. After they do, the leader extends his arms out infront of himself and peers at the blade they hold. They clench their fist and grimace, but still lay the blade across the leaders arms, after which the others form a circle around them and start walking away and the leader peers in on the family for a while before shutting the door. The family all hurriedly clusters together and seem to be grieving in eachothers arms... As you wonder why?, what happened to your lookalike?, who were those cloaked people? and so many more questions you start to come back into reality and scream out at the pain across your body. It's died down and is no longer even a fraction of what it had been but still the pain is agonizing and your snaps out of the dreamlike sight you had viewed before and the memory of it becomes fuzzy. You recollect yourself mentally and stand shakily, before lies the pond full of black waters with the statue showing an incredibly angered face directed at you. To your right is the passage you came from, and as you peer into its darkness you hear the same faint ringing you heard before. To your left the passageway you've yet to venture into, silent and dark as the abyss.\n")
						curHealth = takeDamage(4, Stats, curHealth)
						print("The agonizing pain ringing across your body finally comes to a stop but it's certainly left its mark, your health falls to ",curHealth,"\n")
						if TeroCurrentHealth < 1:
							print("Your vision starts to go fuzzy and fade out and your body goes limp. For a moment you think you are going to see more of this dreamscape you peered into before, however you quickly come to terms with the fact that this is not the case but rather your life itself is coming to an end.")
							SystemExit()
						move = input("Do you finally embrace the waters, head back the way you came, or progress through the caverns?\n")
						while loop == 2:
							if move == "embrace":
								loop+=1
								print("You wade into the black waters and watch as a shadowy mist wraps around the statue and change its appearance to a beaming smile and holding it's hands up and together like in prayer. The water wraps around your body and all of your wounds and your fatigue are cured, you can see where your wounds had been is a flowing black fluid joining and mixing into the lighter black water. When you're fully recovered the water falls back into the pool splashing around you and again you see a shadowy mist wrap around the statue and change it to be looking fondly at the passageway you haven't traversed through and pointing an arm to it.\n")
								(Stats, curHealth, curStam, StamBar) = maidenEncounter(Stats, curHealth, curStam, StamBar)
								cavern2HalfIllusions(Stats, curHealth, curStam, StamBar)
							elif move == "head back":
								loop+=1
								move = input("Curious about the ringing noise you've been hearing you head back to where you came from and follow the noise. Cautiously sneaking past the burrow the rat emerged from earlier you notice the corpse of the rat looks much less feral than before, almost friendly well groomed.... Making it back to where the cave seems to have given in you look at the pile of boulders and rocks, and hear that low ringing thunderously rolling out from the cracks. Do you begin digging out rocks or turn away?\n")
								while loop == 3:
									if move == "dig":
										loop+=1
										print("You struggle to pull out rock after rock from the pile honing in on the origin of the sound. Your hands start to bleed and ache as you work through the rocks but it's nothing compared to the pain from the clearing earlier and you keep digging through. The ringing becomes higher and higher pitched as you remove more rocks around it and eventually you see a couple broken chain links scattered aroud and pick up your pace. Finally you unveil a shimmering silver blade and pick it out of the rubble. The ring intensifies and resonates inside of your body and mind, meanwhile the silver blade glows white brighter and brighter by the second until you can no longer see anything but white around you, and then suddenly the light fades out and the ringing stops. You look at the blade and a white sheen dances along the surface with a gentle sound resonating quietly for only a brief moment and then its nothing more than a beautifully smithed sword. Gripping the sword tightly you feel a new energy flowing through you!\n")
										(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
										print("Feeling invigorated you confidently walk into the next passageway, noting along the way the statue in the waters from before is missing now.")
										cavern2NoIllusions(Stats, curHealth, curStam, StamBar)
									elif move == "turn back":
										print("Listening to the resonating sound calling out for you from under the rubble you stop and decide maybe you would be better off leaving it in its place. You rest for a moment and then head back the clearing and into the caverns ahead.\n")
										loop+=1
										(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
										cavern2Disillusioned(Stats, curHealth, curStam, StamBar)
									else:
										move = input("please input 'dig' or 'turn back'\n")
							elif move == "progress":
								loop+=1
								print("You decide to continue your path down the next passageway, but before setting down it decide that you should first rest and tend to your wound a little.\n")
								(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
								print("Feeling at least a little bit better you pick yourself up and slowly progress into the next passageway.\n")
								cavern2Disillusioned(Stats, curHealth, curStam, StamBar)
							else:
								move = input("please answer 'embrace', 'head back', or 'progress'\n") 
					else:
						move = input("Please answer 'accept' or 'ignore'\n")
			else:
				move = input("Please answer 'peel away' or 'accept'\n")



def clearingNoIllusions(Stats, curHealth, curStam, StamBar):
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
	global firstMaidenFought

	print("You venture into the passage the other direction. Along the way you see a burrow in the cavern wall and a family of immense rats with smooth sleek coats of fur. As intimidating as these large creatures may be they seem friendly enough and they let you pass freely. Further beyond you come into a spacious clearing between the passage you came from and another ahead of you. On the right half of the cave wall is a pool lined with marble, filled with black eerie waters, and at the far end of it is a shadowy figure shaped sort of like a woman with horns. As you notice this creature you close your grip around your sword tighter and stare, and the shadow breaks the stand still in the room with an angry shriek and the water around her stirs up.")
	print(combatTutorial)
	statProgress(ShadowCurrentHealth, ShadowCurrentStam, curHealth, curStam)
	while ShadowCurrentHealth > 35 and curHealth > 0:
		choice = input("\nThe waters whirl in unnatural patterns and the shadow cackles maniacally, what will you do?\n")
		if choice == "defend":
			if ShadowCurrentStam >= 8:
				curHealth = takeDamage(((ShadowStats["Atk"] - Stats["Def"])//2), Stats, curHealth)
				ShadowCurrentStam = fatigueStatus((8-ShadowStats["Stam"]), ShadowCurrentStam, ShadowStamBar)
				curStam = fatigueStatus(-Stats["Stam"], curStam, StamBar)
				statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
			else:
				print("The shadowy figure envelopes its lower half in the murky waters and hisses.\n")
				ShadowCurrentStam = fatigueStatus(-2*ShadowStats["Stam"], ShadowCurrentStam, ShadowStamBar)
				statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
		elif choice == "attack":
			if curStam >= 8:
				ShadowCurrentHealth = takeDamage(Stats["Atk"] - Stats["Def"], ShadowStats, ShadowCurrentHealth)
				curStam = fatigueStatus(8-Stats["Stam"], curStam, StamBar)
				if ShadowCurrentStam >= 8:
					curHealth = takeDamage(ShadowStats["Atk"] - Stats["Def"], Stats, curHealth)
					ShadowCurrentStam = fatigueStatus(8-ShadowStats["Stam"], ShadowCurrentStam, ShadowStamBar)
					statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
				else:
					print("The shadow writhes in place trying to dodge your blade, but is held still by the waters wrapped around it.")
					ShadowCurrentStam = fatigueStatus(-ShadowStats["Stam"]*2, ShadowCurrentStam, ShadowStamBar)
					statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
			else:
				print("You are too fatigued to attack")
		elif choice == "rest":
			if curStam >= (StamBar-4):
				print("You've no need to rest now.")
			else:
				curStam = fatigueStatus(-2*Stats["Stam"], curStam, StamBar)
				if ShadowCurrentStam >= 8:
					curHealth = takeDamage(ShadowStats["Atk"] - Stats["Def"], Stats, curHealth)
					ShadowCurrentStam = fatigueStatus(8-ShadowStats["Stam"], ShadowCurrentStam, ShadowStamBar)
					statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
				else:
					print("The shadow rapidly twirls and lowers itself within a bubble of the murky water, leaving only its eyes over the water keeping you in sight while you catch your breath.")
					ShadowCurrentStam = fatigueStatus(-2*ShadowStats["Stam"], ShadowCurrentStam, ShadowStamBar)
					statProgress(ShadowCurHealth, ShadowCurrentStam, curHealth, curStam)
		elif choice == "skills":
			print("You haven't learned any skills yet.")
		else:
			print(combatInvalidChoice)
	if curHealth <= 0:
		print("The shadow cackles mockingly while dark bubbles rise from the pool and pop around her. Your vision gets hazy and you collapse.")
		SystemExit()

	elif ShadowCurrentHealth < 35:
		print("The Shadow grabs it's horns firmly and pulls on them while screeching. All of the water rises from the floor, a large amount forming a base around the shadows legs, and the rest hovering in the air formed into something like 10 seperate giant tails. The shadow silences its screech and releases its hands down by its side and stares blankly at you for a moment.... \n\nSuddenly it raises its arms up extended towards you and its fingers start to snap out of their human like shape and extend, and you notice the tails of water move corresponding to the way it moves it's fingers. You brace yourself unsure what to do and then 4 of the tails slam into you far too fast for you to react. The tails hit you in an x pattern and form a ball around you suffocating you, in a mad flail to free yourself you slash at the waters and the sword glows bright, the water around you loses its rigid form and splashes down onto the floor dropping you onto your back.")
		curStam = fatigueStatus(12, curStam, StamBar)
		print("\nYour struggle wore you out, your stamina is now ", curStam)
		choice = input("\nThe tails that struck you are very slowly being pulled back into the water around the shadows legs, do you want to make a dash to try and slice away some or try to prepare to intercept an attack?\n")
		while curHealth > 0 or firstMaidenFought == False:
			if choice == "intercept":
				print("you stand firm and when a single tail is propelled towards you, you run the glowing blade through it and again watch it lose form and splash down around you.\n")
				loop = 0
				choice = input("Your plan seems to be working, continue to intercept incoming tails or go on the offensive?\n")
				while loop == 0:
					if choice == "intercept":
						loop+=1
						print("You prepare to repeat your same action and wait for a tail to launch after you. After a short moment the next tail comes flying towards you and you time your motion and start to swing. When the tail and sword are about to collide the tail suddenly buckles up to avoid the blade and two more tails slam into your sides. You cut your way out again but the force the tails slammed into you with was much higher this time and severely injured you.\n")
						curHealth = takeDamage(6, Stats, curHealth)
						print("you took 6 damage, your health dropped to ", curHealth)
						if curHealth == 0:
							print("The blast from the tails likely broke some ribs and caused internal bleeding. You struggle to hold yourself up but inevitably collapse. The shadow cackles softly and the tails wrap around your legs and drag you into the murky waters around its legs. Everything goes black.\n")
							SystemExit()
						else:
							while loop == 1:
								choice = input("The shadows face distorts rapidly while making a constant spastic clicking noise. With only 4 tails left it seems to be getting antsy, do you want to prepare to intercept again or charge?\n")
								if choice == "intercept":
									loop+=1
									print("The shadow whips its head forward and screeches, slamming the remaining 4 tails directly into you. You slash you're blade through the oncoming torrent, and find you're unable to nullify all four tails momentum at once and take a heavy blow. however, as you tumble along the ground you see the tails all collapse down.\n")
									curHealth = takeDamage(8, Stats, curHealth)
									print("You took another 8 damage, your health dropped to ", curHealth)
									if curHealth == 0:
										print("You see that you were able to knock out the last 4 tails, and the shadow is breaking down, however you can no longer move your body and a raging pain stings along your chest. You taste your own blood filling your mouth, and resign yourself to your fate.")
										SystemExit()
									else:
										print("\nThe shadow makes a sad chirping noise, then loses form and becomes nothing more than a dark mist. It slowly spreads wide infront of you, and then in an instant picks all of the waters dropped from the tails off the ground and back into itself, and bolts away like a massive arrow of water, down into the passageway you've yet to venture into. Holding your blade forth anticipating its return, you stand stoicly, yet after a long pause you decide it's likely not coming back and decide to rest and give your body a chance to recover. You slouch down against the cave wall in the clearing and take a breath. Suddenly, your blade glistens white again and cloaks you in it's aura.\n")
										firstMaidenFought == True
										Stats["Exp"] += 100
										print("You gained 100 Exp!")
										Stats = swordCheckLvl(Stats)
										(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
										print("You pick yourself up and head into the caverns ahead of you, blade at the ready.")
										cavern2NoIllusions(Stats, curHealth, curStam, StamBar)
								elif choice == "charge":
									if curStam >= 20:
										loop+=1
										print("You charge at a dead sprint and land the blow into the chest of the shadow itself, as you do so it reacts by slamming its tails into your back with huge force one at a time")
										curStam = fatigueStatus(20, curStam, StamBar)
										curHealth = takeDamage(8, Stats, curHealth)
										if curHealth == 0:
											print("yo")
											SystemExit()
										else:
											firstMaidenDead = True
											firstMaidenFought = True
											print(", but you hold firm and run the blade through the shadow to the hilt. To your surprise the white aura the sowrd let off earlier surrounds the shadow and then chages sensation from its calm serene feeling to one of a divine, awe inspiring, being casting judgement down on a child that lost its's way. The aura burned angrily and the shadow bellowed in screams, not like the screeches before but truly screams of horror and fear. The shadow slowly ceased to be and as it burned away and shriveled the aura shrank around it until it only wrapped around the blade again and the shadow was entirely gone. The waters collapsed into the pool once more and a black mist rose from it and into the blade, transforming to the white glow of the blade itself, and the pool beneath turned in color to be normal everyday waters.\n")
											Stats["Exp"] += 250
											print("\nYou've gained 250 Exp!!\n")
											Stats = swordCheckLvl(Stats)
											print("Your heart pounding, body shaking from both exhaustion and internal damage, you collapse face first into the pool of now cleansed waters. You think to yourself for a moment, 'am I going to die here like this? after everything!?' face under water unable to move your body. As you run out of breath, you nearly let the blade slip from your hand and drift away, but before it does the same white aura envelopes you and you feel it mending your body.\n")
											(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
											print("Able to move your limbs once more you lift yourself out from the pool of water and gasp for air. after a moment to catch your breath you glance at the passage you've yet to travel down and the blade at your side intensifies its ringing sound. You feel strangely indebted to this sword and accept its desire. You pick yourself up and start to venture down the passageway.\n")
											cavern2NoIllusions(Stats, curHealth, curStam, StamBar)
									elif curStam >= 12:
										loop+=1
										print("You pause for just a moment and as a tail slams forth with great speed, you run under it and charge at the shadow. Before you can reach all the way to it the other tails curl in front of the shadow to protect it. You slash through all 3 successfully, but immediately get slammed in the back by the last tail. Having the wind knocked out of you, you struggle to get back to your feet and the shadow cackles and twirls its last tail over your head.\n")
										curStam = fatigueStatus(12, curStam, StamBar)
										curHealth = takeDamage(6, Stats, curHealth)
										print("\nYou took 6 damage, and lost 12 stamina. Your health is now: ", curHealth, " and your stamina is now: ", curStam)
										if curHealth == 0:
											print("Your consciousness fades out as you're continuosly wailed on by the last tail, the force rippling waves in the shallow pool of water around you.")
											SystemExit()
										else:
											choice = input("You know you need to move before that tail hanging over head strikes again, and you know you're in a vulnerable position, but you struggle to move at all let alone quickly. You quickly run some ideas through your mind and realize you have limited options. You could try rolling over and swinging your blade along the way in a wide arc to try and take out the last tail, you could try and get a footing and quickly spring forward to stab into the shadow, or you could try to quickly spring backwards and prepare to defend yourself, what will you do?\n")
											while loop == 2:
												if choice == "roll":
													loop+=1
													print("You tuck the blade in against your side, and slowly get your arm into a stiff straight position. Then, swiftly and simultaneously you push your arm out perpendicular to your body and roll letting your body weight drag your arm across with you in an arc. You successfully take out the last tail, but now lay flat on your back, sword at a full arms distance from your abdomen, with the shadow looming over you a mere foot or so away. You should be in mortal danger, yet the shadow has lost it's own composure and is stumbling back whilst screeching. Suddenly it reaccumulates all the waters fallen from the tails into itself, losing its humanoid form, and then bolts away as a mass of black liquid. You take the opportunity to stand and brace for it's return, but several moments pass with no further action. You cautiously decide to lower your guard and take a chance to rest.")
													print("\n\nYou gained 100 exp!")
													Stats["Exp"]+=100
													Stats = swordCheckLvl(Stats)
													(curHealth, curStam) = swordRestRecovery(Stats, curHealth, curStam, StamBar)
												elif choice == "stab":
													loop+=1
													print("You take your time to position your footing and joints to make one swift push forward and stab into the shadow without alerting the shadow itself. YO ")
												elif choice == "defend":
													loop+=1
													print("yo")
												else:
													choice = input("\nPlease input 'roll', 'stab', or 'defend'")
									else:
										choice = input("It seems you're too fatigued to make the attack, you'll only be able to intercept, please try again.\n")

								else:
									choice = input("Please input 'intercept' or 'charge'")
					elif choice == "offensive":
						loop+=1
					else:
						choice = input("Please input 'intercept' or 'offensive'\n")
			elif choice == "dash":
				print("yo")

			else:
				choice = input("Please input 'intercept' or 'dash'")

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

	print("As you walk along the passageway you notice a large hole near the ground ahead on your right side. You cautiously approach and peer in but can't see anything but darkness. You begin to walk along your path again, but short after feel a sudden chill. Nervously you peer slowly over your shoulder and spot a shadow a couple feet long, and it begins to snarl back at you. As it approaches to strike you get a more clear picture, it is an immense rat with tufts of fur missing and jagged teeth. In this cavern you don't think you'll be able to outrun it and fearfully prepare to fight for your life.\n\n")
	print(combatTutorial)
	statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
	while RatCurrentHealth > 0 and curHealth > 0:
		choice = input("The rat is gnarling viciously, what action will you take?\n")
		if choice == "defend":
			if RatCurrentStam >= 6:
				curHealth = takeDamage(((RatStats["Atk"] - Stats["Def"])//2), Stats, curHealth)
				RatCurrentStam = fatigueStatus((6-RatStats["Stam"]), RatCurrentStam, RatStamBar)
				curStam = fatigueStatus(-Stats["Stam"], curStam, StamBar)
				statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
			else:
				print("The rat is busy panting and doesn't attack")
				RatCurrentStam = fatigueStatus(-2*RatStats["Stam"], RatCurrentStam, RatStamBar)
				curStam = fatigueStatus(-Stats["Stam"], curStam, StamBar)
				statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
		elif choice == "attack":
			if curStam >= 6:
				RatCurrentHealth = takeDamage((Stats["Atk"] - RatStats["Def"]), RatStats, RatCurrentHealth)
				curStam = fatigueStatus((6-Stats["Stam"]), curStam, StamBar)
				if RatCurrentStam >= 6:
					curHealth = takeDamage(RatStats["Atk"] - Stats["Def"], Stats, curHealth)
					RatCurrentStam = fatigueStatus((6-RatStats["Stam"]), RatCurrentStam, RatStamBar)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
				else:
					print("The rat sluggishly takes the blow")
					RatCurrentStam = fatigueStatus(-RatStats["Stam"]*2, RatCurrentStam, RatStamBar)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
			else:
				print("You are too fatigued to attack")
		elif choice == "rest":
			if curStam >= (StamBar-3):
				print("You've no need to rest now.")
			else:
				curStam = fatigueStatus(-2*Stats["Stam"], curStam, Stambar)
				if RatCurrentStam >= 6:
					curHealth = takeDamage((RatStats["Atk"] - Stats["Def"]), Stats, curHealth)
					RatCurrentStam = fatigueStatus((6-RatStats["Stam"]), RatCurrentStam, RatStamBar)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
				else:
					print("You both sink down and breathe heavily eyeing each other in anticipation")
					RatCurrentStam = fatigueStatus(-2*RatStats["Stam"], RatCurrentStam, RatStamBar)
					statProgress(RatCurrentHealth, RatCurrentStam, curHealth, curStam)
		elif choice == "skills":
			print("You haven't learned a skill yet")
		else:
			print(combatInvalidChoice)
	if curHealth <= 0:
		print("You feel the warmth of your own blood leaving your insides and running across your flesh. You come to terms with the fact that you died not knowing who you are or how you got to this cave, food for a feral rat creature.")
		SystemExit()
	else:
		print("\nYou're shaking from a mix of blood loss and adrenaline as you stand over the now dead rat.\n")
		Stats["Exp"] += 50
		print("Gained 50 exp!")
		Stats = CheckLvl(Stats)
		print(Stats)
		clearingIllusions(Stats, curHealth, curStam, StamBar)


def digStart(Stats, curHealth, curStam, StamBar):
	loop = 0
	move = input("You eye up the mound of rocks and boulders and designate a few that you feel you can pull out from the weight of the others. As you start to work them out all you seem to be achieving is having more rocks come down in their place from the collapsed ceiling. Do you want to continue digging into the rocks or give up?\n")
	while loop == 0:
		if move == "continue":
			loop+=1
			print("As you peel out rocks a large rock falls down on top of you and strikes the back of your head.")
			curHealth = takeDamage(4, Stats, curHealth)
			print("Your health drops 4 points, it is now ",curHealth)
			move = input("Do you still continue or give up?\n")
			while loop == 1:
				if move == "continue":
					loop+=1
					print("You dig feverishly thorugh the pile and the ringing you've been hearing resonates in a higher and higher tone as you do so, several stones into the process you notice the skin wearing off of your hands rubbing them raw.")
					curHealth = takeDamage(2, Stats, curHealth)
					print("Your health drops another 2 points, it is now ",curHealth)
					move = input("Do you still continue or give up?\n")
					while loop == 2:
						if move == "continue":
							loop+=1
							print("You finally uncover what appears to be a brilliantly crafted shimmering blade. Hoisting it out of the heap you feel a warmth shoot out of the blade and into your hand and rippling through your body.\n")
							curHealth = swordCurrentHealth
							curStam = swordCurrentStam
							StamBar = swordStamBar
							Stats = swordStats
							(curHealth, curStam) = restRecovery(Stats, curHealth, curStam, StamBar)
							clearingNoIllusions(Stats, curHealth, curStam, StamBar)
						elif move == "give up":
							loop+=1
							print("You give up on trying to work through all this rubble and turn back to go through the passage way behind you")
							ratFight(Stats, curHealth, curStam, StamBar)
						else:
							print("Please input 'continue' or 'give up'.")
				elif move == "give up":
					loop+=1
					print("You give up on trying to work through all this rubble and turn back to go through the passage way behind you")
					ratFight(Stats, curHealth, curStam, StamBar)
				else:
					print("Please input 'continue' or 'give up'\n")
		elif move == "give up":
			loop+=1
			print("You give up on trying to work through all this rubble and turn back to go through the passage way behind you")
			ratFight(Stats, curHealth, curStam, StamBar)
		else:
			move = input("Please input 'continue' or 'give up'\n")


def main():
	Stats = TeroStats
	curHealth = TeroCurrentHealth
	curStam = TeroCurrentStam
	StamBar = TeroStamBar
	loop = 0
	move = input("You wake up alone in a cave system wearing only a shredded up cheap tunic. Looking around, you see a narrow passageway in front and behind you. From behind you theres a constant low ringing sound but you can only make out a caved in wall of rocks, in front of you is a silent and empty, dark passgeway. Do you want to progress forward or dig through the rocks?\n")	
	while loop == 0:
		if move == "progress":
			loop+=1
			ratFight(Stats, curHealth, curStam, StamBar)
		elif move == "dig":
			loop+=1
			digStart(Stats, curHealth, curStam, StamBar)
		else:
			move = input("please answer 'progress' or 'dig'\n")

main()
