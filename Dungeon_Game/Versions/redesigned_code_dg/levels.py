import random
from characters import Foe

class Levels:

	floor_events = {
		1: {},
		2: {},
		3: {},
		4: {},
		5: {},
	}

	floor_conditions = {
		1: {
			'enteredClearing': False,
			'ratKilled': False,
			'metNoIllusionRats': False,
			'hasDug': False,
			'hasDug2': False,
			'seenMaidenLeave': False,
			'swordDepth': 3,
		},
		2: {
			'foes1': 15,
			'foes2': 15,
			'foes3': 40,
			'foes4': 15,
			'foes5': 15,
			'foes6': 15,
			'hasScalpel': False,
		},
		3: {
			'turns': 0,
			'minotaurDead': False,
			'hunter10': False,
			'hunter11': False,
			'hunter20': False,
			'hunter21': False,
			'hunter30': False,
			'hunter31': False,
			'hunter40': False,
			'hunter41': False,
			'hunter50': False,
			'hunter51': False,
			'hunter60': False,
			'hunter61': False,
			'hunter70': False,
			'hunter71': False,
			'hunter80': False,
			'hunter81': False,
			'hunter90': False,
			'hunter91': False,
		},
		4: {
			"foes1": 15,
			"foes2": 15,
			"foes3": 40,
			"foes4": 15,
		},
		5: {
			'killedEveryGuard': True,
		},
	}

	def __init__(self, level=1):
		self.level = level
		self.setEvents()

	def death(self, kinter, sentence):
		kinter.eventMessage(sentence)
		kinter.takeInput('\nYou died, press any button to close the game..')
		kinter.window.destroy()

#############################################################################################################################################################
############################################################## EVENTS #######################################################################################
#############################################################################################################################################################

############################################################## COMMON #######################################################################################

	def open_tile(self, kwargs):
		if self.level == 3:
			self.floor_conditions[self.level]['turns'] += 1
			# on turn count stuffs

	def next_map(self, kwargs):
		self.level += 1
		kwargs['curMap'].changeLevel(kwargs['curMap'].level+1)
		kwargs['curMap'].printEnvironment()
		kwargs['kinter'].Update_Map(kwargs['curMap'])

	def pickup_item(self, kwargs):
		item_list = {
			2: {
				(17,35): ('bandages', 0),
				(25,8): ('oily water', 0),
				(8,14): ('salt rock', 0),
				(9,1): ('canteen', 1),
				(26,3): ('stale bread', 0),
				(28,32): ('adrenaline', 0),
			},
			3: {},
			4: {},
		}
		# add item_list[self.level][(kwargs['curMap'].curY,kwargs['curMap'].curX)] to inventory
		item = item_list[self.level][(kwargs['curMap'].curY,kwargs['curMap'].curX)]
		if item[1]:
			if len(kwargs['hero'].heldInventory) < 3:
				kwargs['hero'].add_item(item)
			else:
				pressed = kwargs['kinter'].takeInput(f'\nYou found a {item[0]} but you don\'t have room to hold it. Do you want to drop\n8.) the {item[0]}\n6.) {kwargs['hero'].heldInventory[0]}\n4.) {kwargs['hero'].heldInventory[1]}\n2.) {kwargs['hero'].heldInventory[2]}')
				while pressed not in ['8', '6', '4', '2']:
					pressed = kwargs['kinter'].takeInput()
				if pressed != '8':
					index = 0 if pressed == '6' else 1 if pressed == '4' else 2
					kwargs['hero'].heldInventory[index] = item[0]
		else:
			if len(kwargs['hero'].inventory) < 3:
				kwargs['hero'].add_item(item)
			else:
				pressed = kwargs['kinter'].takeInput(f'\nYou found some {item[0]} but you don\'t have room to hold it. Do you want to drop\n8.) the {item[0]}\n6.) {kwargs['hero'].inventory[0]}\n4.) {kwargs['hero'].inventory[1]}\n2.) {kwargs['hero'].inventory[2]}')
				while pressed not in ['8', '6', '4', '2']:
					pressed = kwargs['kinter'].takeInput()
				if pressed != '8':
					index = 0 if pressed == '6' else 1 if pressed == '4' else 2
					kwargs['hero'].inventory[index] = item[0]
		kwargs['kinter'].updateInventory(kwargs['hero'])
		kwargs['curMap'].mapData[kwargs['curMap'].curY][kwargs['curMap'].curX] = 1

############################################################## LEVEL ONE #######################################################################################

	def rat_encounter(self, kwargs):
		if kwargs['hero'].hasSword and not self.floor_conditions[self.level]['ratKilled']:
			kwargs["kinter"].eventMessage("\nAlong the way you see a burrow in the cavern wall and a family of immense rats with smooth sleek coats of fur. As intimidating as these large creatures may be they seem friendly enough and they let you pass freely.\n") 
			kwargs['curMap'].mapData[kwargs['curMap'].curY][kwargs['curMap'].curX] = 1
		elif (kwargs['hero'].disillusioned or kwargs['hero'].hasSword) and self.floor_conditions[self.level]['ratKilled']:
			kwargs["kinter"].eventMessage("\nCautiously sneaking past the burrow the rat emerged from earlier you notice the corpse of the rat looks much less feral than before, almost friendly and well groomed....\n")
			kwargs['curMap'].mapData[kwargs['curMap'].curY][kwargs['curMap'].curX] = 1
		elif self.floor_conditions[self.level]['ratKilled']:
			pass
		else:
			kwargs["kinter"].eventMessage("\n\nAs you walk along the passageway you notice a large hole near the ground ahead on your right side. You cautiously approach and peer in but can't see anything but darkness. You begin to walk along your path again, but short after feel a sudden chill. Nervously you peer slowly over your shoulder and spot a shadow a couple feet long, and it begins to snarl back at you. As it approaches to strike you get a more clear picture, it is an immense rat with tufts of fur missing and jagged teeth. In this cavern you don't think you'll be able to outrun it and fearfully prepare to fight for your life.")
			topCombatSentence = "The rat is gnarling viciously, what action will you take?"
			fatiguedSentence = "\nThe rat is busy panting and doesn't attack\n"
			OppStats = {
				"Name": 'Rat',
				"Atk": 2,
				"Def": 5,
				"Stam": 1.5,
				"Health": 20,
				"Skills": [],
			}
			rat = Foe(OppStats, 6, topCombatSentence, fatiguedSentence)
			kwargs['hero'].basic_combat(rat, kwargs['kinter'])

			if kwargs['hero'].curHealth == 0:
				self.death(kwargs['kinter'], "\n\nYou feel the warmth of your own blood leaving your insides and running across your flesh. You come to terms with the fact that you died not knowing who you are or how you got to this cave, food for a feral rat creature.\n\nGAME OVER")
			else:
				self.floor_conditions[self.level]['ratKilled'] = True
				kwargs['hero'].Stats["Exp"] += 25
				kwargs['kinter'].eventMessage("\nYou're shaking from a mix of blood loss and adrenaline as you stand over the now dead rat.\n\nYou gained 25 exp!")	

	def dig(self, kwargs):

		def depth_0(kwargs):
			kwargs['hero'].acquire_sword()
			if kwargs['hero'].disillusioned:
				kwargs['kinter'].eventMessage("\nYou struggle to pull out rock after rock from the pile honing all of your focus in on the sound resonating in your head and shrugging off the pain as the rocks dig into your flesh. Your hands start to bleed and ache as you work through the rocks but it's nothing compared to the pain from the clearing earlier and you keep digging through. The ringing becomes higher and higher pitched as you remove more rocks around it and eventually you see a couple broken chain links scattered aroud and pick up your pace. Finally you unveil a shimmering silver blade and pick it out of the rubble. The ring intensifies and resonates inside of your body and mind, meanwhile the silver blade glows white brighter and brighter by the second until you can no longer see anything but white around you, and then suddenly the light fades out and the ringing stops. You look at the blade and a white sheen dances along the surface with a gentle sound resonating quietly for only a brief moment and then its nothing more than a beautifully smithed sword. Gripping the sword tightly you feel a new energy flowing through you!\n")
			else:
				kwargs['kinter'].eventMessage('\nYou finally uncover what appears to be a brilliantly crafted shimmering blade. Hoisting it out of the heap you feel a warmth shoot out of the blade and into your hand and rippling through your body.\nYou have new stats!\n\n')
			kwargs['kinter'].updateStatus(kwargs['hero'])
			kwargs['curMap'].mapData[kwargs['curMap'].curY][kwargs['curMap'].curX] = 1

		def depth_1(kwargs):
			self.floor_conditions[self.level]['swordDepth'] -= 1
			kwargs['hero'].takeDamage(2)
			kwargs['kinter'].updateStatus(kwargs['hero'])
			kwargs['kinter'].eventMessage('\nYou dig feverishly thorugh the pile and the ringing you\'ve been hearing resonates in a higher and higher tone as you do so, several stones into the process you notice the skin wearing off of your hands rubbing them raw.\nYour health drops another 2 points, it is now '+str(kwargs['hero'].curHealth))
			pressed = kwargs['kinter'].takeInput('\nDo you still continue or give up?\n\n8.) Continue\n6.) Give up\n\n')
			if pressed == '8':
				depth_0(kwargs)
			elif pressed == '6':
				return

		def depth_2(kwargs):
			self.floor_conditions[self.level]['swordDepth'] -= 1
			kwargs['hero'].takeDamage(4)
			kwargs['kinter'].updateStatus(kwargs['hero'])
			kwargs['kinter'].eventMessage('\nAs you peel out rocks a large rock falls down on top of you and strikes the back of your head.\nYour health drops 4 points, it is now '+str(kwargs['hero'].curHealth))
			pressed = kwargs['kinter'].takeInput('\nDo you still continue or give up?\n\n8.) Continue\n6.) Give up\n\n')
			if pressed == '8':
				depth_1(kwargs)
			elif pressed == '6':
				return

		depths = {
			2: depth_2,
			1: depth_1,
			0: depth_0,
		}

		if kwargs['hero'].disillusioned:
			pressed = kwargs['kinter'].takeInput('\n\nMaking it back to where the cave seems to have given in you look at the pile of boulders and rocks, and hear that low ringing thunderously rolling out from the cracks. Do you begin digging out rocks or turn away?\n\n8.) Dig\n6.) Turn away')
			if pressed == '8':
				depth_0(kwargs)
		elif self.floor_conditions[self.level]['swordDepth'] == 3:
			kwargs['kinter'].eventMessage("\nYou eye up the mound of rocks and boulders and designate a few that you feel you can pull out from the weight of the others. As you start to work them out all you seem to be achieving is having more rocks come down in their place from the collapsed ceiling.")
			self.floor_conditions[self.level]['swordDepth'] -= 1
			pressed = kwargs['kinter'].takeInput("\nDo you want to continue digging into the rocks or give up?\n\n8.) Continue digging\n6.) Give up\n\n")
			if pressed == '8':
				depth_2(kwargs)
		else:
			pressed = kwargs['kinter'].takeInput('\nDo you want to pick up where you left off?\n\n8.) Continue\n6.) Give up\n\n')
			if pressed == '8':
				depths[self.floor_conditions[self.level]['swordDepth']](kwargs)

	def maiden_encounter(self, kwargs):

		def resolve(kwargs, exp):
			kwargs['hero'].Stats['Exp'] += exp
			kwargs['hero'].updateLevel()
			kwargs['hero'].restRecovery()
			kwargs['kinter'].updateStatus(kwargs['hero'])

		if kwargs['hero'].hasSword:
			kwargs['kinter'].eventMessage("\nYou venture into the passage the other direction. Along the way you see a burrow in the cavern wall and a family of immense rats with smooth sleek coats of fur. As intimidating as these large creatures may be they seem friendly enough and they let you pass freely. Further beyond you come into a spacious clearing between the passage you came from and another ahead of you. On the right half of the cave wall is a pool lined with marble, filled with black eerie waters, and at the far end of it is a shadowy figure shaped sort of like a woman with horns. As you notice this creature you close your grip around your sword tighter and stare, and the shadow breaks the stand still in the room with an angry shriek and the water around her stirs up.\n")
			topCombatSentence = "\nThe waters whirl in unnatural patterns and the shadow cackles maniacally, what will you do?\n\n8.) Attack\n6.) Defend\n4.) Rest\n2.) Skills\n5.) Items\n\n"
			fatiguedSentence = "\nThe shadowy figure envelopes its lower half in the murky waters and hisses.\n"
			endCombatSentence = "\nYou defended yourself from the Imps attack\n"
			#status for Shadow
			OppStats = {
			"name": 'Water Maiden',
			"Atk": 12,
			"Def": 8,
			"Stam": 4.5,
			"Health": 25,
			"Skills": [],
			}
			maiden = Foe(OppStats, 8, topCombatSentence, fatiguedSentence)
			kwargs['hero'].basic_combat(maiden, kwargs['kinter'])
			if kwargs['hero'].curHealth == 0:
				self.death(kwargs['kinter'], "\nThe shadow cackles mockingly while dark bubbles rise from the pool and pop around her. Your vision gets hazy and you collapse.\n")
			else:
				kwargs['kinter'].eventMessage("\nThe Shadow grabs it's horns firmly and pulls on them while screeching. All of the water rises from the floor, a large amount forming a base around the shadows legs, and the rest hovering in the air formed into something like 10 seperate giant tails. The shadow silences its screech and releases its hands down by its side and stares blankly at you for a moment.... \n\nSuddenly it raises its arms up extended towards you and its fingers start to snap out of their human like shape and extend, and you notice the tails of water move corresponding to the way it moves it's fingers. You brace yourself unsure what to do and then 4 of the tails slam into you far too fast for you to react. The tails hit you in an x pattern and form a ball around you suffocating you, in a mad flail to free yourself you slash at the waters and the sword glows bright, the water around you loses its rigid form and splashes down onto the floor dropping you onto your back.\n\n")
				kwargs['hero'].fatigueStatus(8)
				kwargs['kinter'].eventMessage(f"Your struggle wore you out, your stamina is now {kwargs['hero'].curStam}")
				kwargs['kinter'].updateStatus(kwargs['hero'])
				while curHealth > 0:
					pressed = kwargs['kinter'].takeInput("\n\nThe tails that struck you are very slowly being pulled back into the water around the shadows legs, do you want to make a dash to try and slice away some or try to prepare to intercept an attack?\n\n8.) Dash forward\n6.) Prepare to intercept\n\n")
					while pressed not in ['8', '6']:
						pressed = kwargs['kinter'].takeInput("")
					if pressed == '6':
						kwargs['kinter'].eventMessage("\nyou stand firm and when a single tail is propelled towards you, you run the glowing blade through it and again watch it lose form and splash down around you.\n")
						pressed = kwargs['kinter'].takeInput("\nYour plan seems to be working, continue to intercept incoming tails or go on the offensive?\n\n8.) Continue intercepting\n6.) Go on the offense\n")
						while pressed not in ['8', '6']:
							pressed = kwargs['kinter'].takeInput("")
						if pressed == '8':
							kwargs['hero'].takeDamage(4)
							kwargs['kinter'].eventMessage(f"\nYou prepare to repeat your same action and wait for a tail to launch after you. After a short moment the next tail comes flying towards you and you time your motion and start to swing. When the tail and sword are about to collide the tail suddenly buckles up to avoid the blade and two more tails slam into your sides. You cut your way out again but the force the tails slammed into you with was much higher this time and severely injured you.\n\nyou took 6 damage, your health dropped to {kwargs['hero'].curHealth}\n")
							kwargs['kinter'].updateStatus(kwargs['hero'])
							if kwargs['hero'].curHealth == 0:
								self.death(kwargs['kinter'], "\nThe blast from the tails likely broke some ribs and caused internal bleeding. You struggle to hold yourself up but inevitably collapse. The shadow cackles softly and the tails wrap around your legs and drag you into the murky waters around its legs. Everything goes black.\n")
							else:
								pressed = kwargs['kinter'].takeInput("\nThe shadows face distorts rapidly while making a constant spastic clicking noise. With only 4 tails left it seems to be getting antsy, do you want to prepare to intercept again or charge?\n\n8.) Prepare to intercept\n6.) Charge\n\n")
								while pressed not in ['8', '6']:
									pressed = kwargs['kinter'].takeInput("")
								if pressed == '8':
									kwargs['hero'].takeDamage(5)
									kwargs['kinter'].updateStatus(kwargs['hero'])
									kwargs['kinter'].eventMessage(f"\nThe shadow whips its head forward and screeches, slamming the remaining 4 tails directly into you. You slash you're blade through the oncoming torrent, and find you're unable to nullify all four tails momentum at once and take a heavy blow. however, as you tumble along the ground you see the tails all collapse down.\n\nYou took another 8 damage, your health drOpped to {kwargs['hero'].curHealth}\n")										
									if kwargs['hero'].curHealth == 0:
										self.death(kwargs['kinter'], "\nYou see that you were able to knock out the last 4 tails, and the shadow is breaking down, however you can no longer move your body and a raging pain stings along your chest. You taste your own blood filling your mouth, and resign yourself to your fate.\n")
									else:
										kwargs['kinter'].eventMessage("\nThe shadow makes a sad chirping noise, then loses form and becomes nothing more than a dark mist. It slowly spreads wide infront of you, and then in an instant picks all of the waters drOpped from the tails off the ground and back into itself, and bolts away like a massive arrow of water, down into the passageway you've yet to venture into. Holding your blade forth anticipating its return, you stand stoicly, yet after a long pause you decide it's likely not coming back and decide to rest and give your body a chance to recover. You slouch down against the cave wall in the clearing and take a breath. Suddenly, your blade glistens white again and cloaks you in it's aura.\n\nYou gained 100 Exp!")
										resolve(kwargs, 100)
										kwargs['kinter'].eventMessage("\nYou pick yourself up and eye the entrace to the caverns ahead of you, blade at the ready.\n")
								elif pressed == '6':
									if kwargs['hero'].curStam >= 12:
										kwargs['hero'].fatigueStatus(12)
										kwargs['kinter'].eventMessage("\nYou charge at a full sprint and land the blow into the chest of the shadow itself before it could stop you, it screams and implodes like an over filled ballon.\n You hold firm and run the blade through the shadow to the hilt. To your surprise the white aura the sword let off earlier surrounds the shadow and then chages sensation from its calm serene feeling to one of a divine awe inspiring being casting judgement down on a child that lost its's way. The aura burned angrily and the shadow bellowed in screams, not like the screeches before but truly screams of horror and fear. The shadow slowly ceased to be and as it burned away and shriveled the aura shrank around it until it only wrapped around the blade again and the shadow was entirely gone. The waters collapsed into the pool once more and a black mist rose from it and into the blade, transforming to the white glow of the blade itself, and the pool beneath turned in color to be normal everyday waters.\n\nYou've gained 250 Exp!!")
										kwargs['hero'].firstMaidenDead = True
										kwargs['kinter'].eventMessage( "\nYour heart pounding, body shaking from both exhaustion and internal damage, you collapse face first into the pool of now cleansed waters. You think to yourself for a moment, 'am I going to die here like this? after everything!?' face under water unable to move your body. As you run out of breath, you nearly let the blade slip from your hand and drift away, but before it does the same white aura envelopes you and you feel it mending your body.\n")
										resolve(kwargs, 250)
										kwargs['kinter'].eventMessage("\nAble to move your limbs once more you lift yourself out from the pool of water and gasp for air. after a moment to catch your breath you glance at the passage you've yet to travel down and the blade at your side intensifies its ringing sound. You feel strangely indebted to this sword and accept its desire. You pick yourself up and start to venture down the passageway.\n")
									elif kwargs['hero'].curStam >= 8:
										kwargs['hero'].fatigueStatus(8)
										kwargs['hero'].takeDamage(4)
										kwargs['kinter'].eventMessage("\nYou pause for just a moment and as a tail slams forth with great speed, you run under it and charge at the shadow. Before you can reach all the way to it the other tails curl in front of the shadow to protect it. You slash through all 3 successfully, but immediately get slammed in the back by the last tail. Having the wind knocked out of you, you struggle to get back to your feet and the shadow cackles and twirls its last tail over your head.\n")
										kwargs['kinter'].eventMessage(f"\nYou took 6 damage, and lost 12 stamina. Your health is now: {kwargs['hero'].curHealth} and your stamina is now: {kwargs['hero'].curStam}\n")
										if kwargs['hero'].curHealth == 0:
											self.death(kwargs['kinter'], "\nYour consciousness fades out as you're continuosly wailed on by the last tail, the force rippling waves in the shallow pool of water around you.\n")
										else:
											pressed = kwargs['kinter'].takeInput("You know you need to move before that tail hanging over head strikes again, and you know you're in a vulnerable position, but you struggle to move at all let alone quickly. You quickly run some ideas through your mind and realize you have limited options. You could try rolling over and swinging your blade along the way in a wide arc to try and take out the last tail, you could try and get a footing and quickly spring forward to stab into the shadow, or you could try to quickly spring backwards and prepare to defend yourself, what will you do?\n\n8.) Roll\n6.) Stab\n4.) Spring backwards\n\n")
											while pressed not in ['8', '6', '4']:
												pressed = kwargs['kinter'].takeInput("")
											if pressed == '8':
												kwargs['kinter'].eventMessage("\nYou tuck the blade in against your side, and slowly get your arm into a stiff straight position. Then, swiftly and simultaneously you push your arm out perpendicular to your body and roll letting your body weight drag your arm across with you in an arc. You successfully take out the last tail, but now lay flat on your back, sword at a full arms distance from your abdomen, with the shadow looming over you a mere foot or so away. You should be in mortal danger, yet the shadow has lost it's own composure and is stumbling back whilst screeching. Suddenly it reaccumulates all the waters fallen from the tails into itself, losing its humanoid form, and then bolts away as a mass of black liquid. You take the Opportunity to stand and brace for it's return, but several moments pass with no further action. You cautiously decide to lower your guard and take a chance to rest.\n\nYou gained 100 exp!")
												resolve(kwargs, 100)
											elif pressed == '6':
												kwargs['kinter'].eventMessage("\nYou take your time to position your footing and joints to make one swift push forward and stab into the shadow without alerting the shadow itself. Your attack is a success... sort of. You were able to get up and lunge forward without being struck in return, however the watery base at the shadows legs stOpped your blades momentum only a few inches into it. The blade starts to shimmer like in the tails before, and the remaining tails collapse around you, but you're blade is still stuck in the waters around the shadow and those waters aren't collapsin like the tails. You lock eyes with the shadow for a brief moment, before it screeches in your face and slams you across the room.\n")
												kwargs['hero'].takeDamage(4)
												if kwargs['hero'].curHealth == 0:
													self.death(kwargs['kinter'], "\nThe last forceful shove from the shadow was the straw that broke the camels back for you. Your body is too broken down to will forward anymore. Your life fades away...\n")
												else:
													kwargs['kinter'].eventMessage("Disoriented and nearing death you scramble to get to your feet and collect up your sword, but you see that the shadow bolting dwon the chamber you've yet to traverse. You take a moment to collect your things and slouch against the wall for awhile. After a long enough stretch of time to feel sustainable you get up move towards the next passageway\n\nYou gained 100 Exp!")
													resolve(kwargs, 100)
											elif pressed == '4':
												self.death(kwargs['kinter'], "\nYou try to place your footing down, and push with your arms to spring up swiftly to a stand and then backpedal away, and succeed. However, just as you get up and move to get away the tails looming over you start to pummel down on you with no ability to defend yourself. They slam into you relentlessly until suddenly the shadows face is over your own and its claws rips into your face.\n")
									else:
										self.death(kwargs['kinter'], '\nYou start your charge and notice that your own movement has become slow and ragged and you attempt to push harder but end up fumbling over yourself and falling onto your face. The shade takes advantage of the opportunity and repeatedly slams your face into the rocky floor well beyond the point at which you were no longer recognizable...')
						elif pressed == '6':
							kwargs['kinter'].eventMessage("\nYou recognize that the shadow is adapting to your strategy and think that perhaps you need to change it up yourself. You feign a full on charge and then stop in place swiftly pivoting on your right foot to slash around you with your sword, catching 2 tails intended to strike you from behind. The tails splash down and the Shadow screeches, and flails the last 3 tails around.wildly around itself.\n")
							pressed = kwargs['kinter'].takeInput("\nDo you want to push the momentum or change it up and try something new again?\n8.) Push the momentum\n6.) Try something new again\n\n")
							while pressed not in ['8', '6']:
								pressed = kwargs['kinter'].takeInput("")
							if pressed == '8':
								kwargs['kinter'].eventMessage("\nYou continue your offensive push, and the shadow launches 2 tails at you. Before they get in range to slash at they slow significantly, swell up at the tips, and then slam together to capture you in their water. You're able to use the sword to instantly nullify the waters like before, but as you're freed from the waters grip the last tail slams into your skull with great force.\n")
								kwargs['hero'].takeDamage(6)
								if kwargs['hero'].curHealth == 0:
									self.death(kwargs['kinter'], '\nThe blow was too much for your already brittle body to take and your concious fades away..')
								else:
									kwargs['kinter'].eventMessage(f"\nYou lost 6 more health, and your health is now {kwargs['hero'].curHealth}\n\nAs the tail goes to strike at you again you barely manage to lift up your sword and burst the tail before it crushes you. The shadow having lost all of its tails shreeks horrifically before transforming into a dark mist and bolting down the passageway you haven't yet traversed.\n")
									resolve(kwargs, 100)
							elif pressed == '6':
								kwargs['kinter'].eventMessage("\nTrying to think quick what you haven't done yet, you come up with an idea to bait the tails away from the shadow and then javelin tossing the sword into the shadow. You charge forward like before, stop and turn away like before, and as you hear the watery tails surging towards you, you grip the hilt with a c-grip and lock in your elbow. You turn and instantly hurl the blade with an upward arc towards the shadow. The shadow cackles and surges the tails at you knowing you've just tossed away your only means of defending yourself. You recognize that perhaps that wasn't the best idea you've ever had and close your eyes bracing for impact......\n\n but instead you open your ears to the sound of the shadow angrily screeching. the blade landed into the murky waters wrapped around the shadows legs, and all the remaining tails seem to have fallen down. The shadow screeches and jumps out of the water, near instantly gets infront of you and slams you across the room before vanishing through the passageway you've yet to traverse\n")
								resolve(kwargs, 100)
					elif pressed == '8':
						kwargs['kinter'].eventMessage("\nYou dash forward at the shadow and it slams all 6 remaining tails into you one at a time in quick succession. You were able to swipe your blade through the first two and the waters drOpped to the floor, but the reamining four slammed you down.\n")
						kwargs['hero'].takeDamage(4)
						if kwargs['hero'].curHealth == 0:
							self.death(kwargs['kinter'], "\ntails whirling around overhead, you lie on your back and slowly fade out of consciousness.\n")
						else:
							kwargs['kinter'].eventMessage(f"\nYou took 6 damage, you have {kwargs['hero'].curHealth} health left.\n")
							kwargs['kinter'].updateStatus(kwargs['hero'])
							pressed = kwargs['kinter'].takeInput("\nYou get up off the ground, and square up again. Do you want to try dashing in again or play it safer?\n8.) Dash again\n6.) Play it safe\n\n")
							while pressed not in ['8', '6']:
								pressed = kwargs['kinter'].takeInput("")
							if pressed == '8':
								kwargs['kinter'].eventMessage("\nYou start to charge forth again and the scene starts to play out the same as before, however you're prepared this time and there are fewer tails to fight through. You succeed, barely, in knocking away all 4 tails, but while you're stumbling and off balance the shadow changes chape into a dark mist and bolts down the passageway you've yet to travel down with a fading shreek\n\nYou gained 100 exp!")
								resolve(kwargs, 100)
							elif pressed == '6':
								kwargs['kinter'].eventMessage("\nYou set yourself in a firm stance and wait for the shadow to make the next move. In time the shadow grows impatient and starts creeping the tails along the floor like snakes around you. The tip of the tails rise up from the ground and feign launching at you, over time starting to unnerve you and get you off your footing. Eventually one of the tails commits to the attack while your watching another tail and knocks you down. While your down all 4 tails simultaneously start to slam into you repeatedly\n")
								kwargs['hero'].takeDamage(6)
								if kwargs['hero'].curHealth == 0:
									self.death(kwargs['kinter'], "\nThe tails pound at you until you're body is unrecognizable as a human corpse.\n")
								else:
									kwargs['kinter'].eventMessage("\nYour brain starts to shut out the repetitive pain and you collect yourself enough to tighten your grip on the hilt of your blade and suddenly turn and slash down all 4 tails at once. The shadow screeches and turns into a dark mist before vanishing down the passageway you haven't traveled through yet.\nYou gained 100 exp!")
									resolve(kwargs, 100)
		else:
			kwargs['kinter'].eventMessage("\n\nYou quickly shuffle forward to get distance from the burrow fearful there may be more creatures yet inside. Your body rings out in agonizing pain, missing chunks of flesh and losing blood fast. Even still you progress, ahead you see a blinding light amidst the darkness. When you cross into the light and your vision adjusts you a see a spacious circular room with the narrow pathway you came from behind you and another similar continuation on the other side of the room. The right side of the floor seems to be all water and lining the wall rather than cavern walls of rock is a glistening polished white marble with an occasional lit torch along it. In front of the center of the wall amidst the bath stands a life sized marble statue of young maiden shedding a single tear. As you lock eyes with the statue you feel a strong urge to get into the water and the intensity of the pain you feel from each of your wounds increases immensely more and more each second.")
			pressed = kwargs['kinter'].takeInput("\nPeel away from the statues gaze and move on in the caverns or accept its call and join it in the waters?\n\n8.) Peel away\n6.) Accept\n\n")
			while pressed not in ['8', '6']:
				pressed = kwargs['kinter'].takeInput("")
			if pressed == '6':
				kwargs['kinter'].eventMessage("\nAs you step into the water you can see the single tear on the maiden change form from stone to liquid and drip into the water. The water begins to feel warmer and you notice a slight shimmer along the surface. Suddenly the water bursts into a glaring golden color and rises up around you, encapsualting you in it. At first you struggle against the water in fear of drowning but as you flail around you see that your wounds are closing up and as though you've never endured a hardship in your life. You give in to the comforting aura and let out a gasp to find you can still breathe.\n")
				kwargs['hero'].maidenEncounter()
				kwargs['kinter'].updateStatus(kwargs['hero'])
				kwargs['kinter'].eventMessage("\nThe shimmering gold color settles and slowly fades in the water around you and soon it all falls to the pool again beneath you. Suddenly two torches flare up on either side of the entrance to the narrow passageway across from where you entered this opening. You glance back to the statue of the maiden and see that it has changed and she is smiling sweetly now instead of crying, and holds an arm up pointing to the passageway. You take hold of the meaning and venture forth into the cavern again.\n")
			elif pressed == '8':
				kwargs['kinter'].eventMessage("\nYou peel your eyes away from the maidens and step back, suddenly you feel a horrendous stinging pain all across your body and you're certain it isn't from your existing wounds. You fumble in agony and lose your footing until you collapse against the wall Opposite the pool of water, when you open your eyes and glance back at the pool the maiden statue appears different. She now has an arm raised pointing at you, and the other into the waters with a stern frown and sharp eyes.\n")
				kwargs['hero'].takeDamage(2)
				kwargs['kinter'].updateStatus(kwargs['hero'])
				kwargs['kinter'].eventMessage(f"\nThe stinging pain running along your skin takes its toll, your health drops to {kwargs['hero'].curHealth}\n")
				if kwargs['hero'].curHealth == 0:
					self.death(kwargs['kinter'], "\nYour body goes limp and your vision fades away. The lashing pain you suddenly felt untop added to your existing wounds proved fatal.\n")
				else:
					pressed = kwargs['kinter'].takeInput("Do you accept the demand or ignore it?\n\n8.) Ignore\n6.) Accept\n\n")
					while pressed not in ['8', '6']:
						pressed = kwargs['kinter'].takeInput("")
					if pressed == '6':
						kwargs['kinter'].eventMessage("\nFearfully you crawl to the waters, roll yourself in, and sink down. You feel your wounds and pain fading from your body, the holes of flesh bitten off of you sealing up. Lifelessly you lay at the bottom of the pool, but as the last of your wounds seals itself and you still lie there the water itself surges and throws you beside the pools edge. After a fit of coughing for a moment you look up and see that again the statue has changed and now stands hands down and cupped together, face directed at the passage way youve yet ventured in with a beaming smile. Torches on either side of the entrance flare up and you collect yourself and venture into it hesitantly taking glances at the statue behind you.\n")
						kwargs['hero'].maidenEncounter()
						kwargs['kinter'].updateStatus(kwargs['hero'])
						kwargs['kinter'].eventMessage("\nThe shimmering gold color settles and slowly fades in the water around you and soon it all falls to the pool again beneath you. Suddenly two torches flare up on either side of the entrance to the narrow passageway across from where you entered this opening. You glance back to the statue of the maiden and see that it has changed and she is smiling sweetly now instead of crying, and holds an arm up pointing to the passageway. You take hold of the meaning and venture forth into the cavern again.\n")
					elif pressed == '8':
						kwargs['kinter'].eventMessage("\nThe stinging pain you felt before intensifies to what can only be described as the most horrendously agonizing sensation you've ever felt in your life. Were you to lacerate your own body along every inch of it, douse yourself with a batch of a citrusy liquid, and then light yourself ablaze, even still it could not compare the pain ringing out across your entire body. You freeze in place, the pain so great your brain entirely shut down to protect you from going insane. While your mind is blacked out from reality your consciousness drifts into a vision like a sort of dream. You see a family around a table, amongst them is an individual that resembles yourself, perhaps more groomed in appearance with a little more fat on your build and slightly less aged but it's certainly the same face you saw looking back in the pond before. The whole family seems to be enjoying themself bantering and sharing a moment together yet everytime theres a lull you can read an expression of teror across their faces. You hear a knocking at the door a few meters from the table and see everyones face freeze up besides your own look alike. They push their seat away from the table, stand, and walk to another room within the small home before returning with a sword tucked into a scabbard and held down into it with chains. Before they open the door they pull on the handle as if to draw the blade and although the chains prevent that it does partially click out of the scabbard and reveal a shimmering silver blade that resonates out a calming ringing sound. They stare for a moment then click it back in and opens the front door, through which you view a gathering of men with black cloaks, silver garnished, with a bright silver mask. The apparent leader of the group stands ahead of the others, adorned with even more silver decorations along their cloak and mask, and gestures your double to join them. After they do, the leader extends his arms out infront of himself and peers at the blade they hold. They clench their fist and grimace, but still lay the blade across the leaders arms, after which the others form a circle around them and start walking away and the leader peers in on the family for a while before shutting the door. The family all hurriedly clusters together and seem to be grieving in eachothers arms... As you wonder why?, what happened to your lookalike?, who were those cloaked people? and so many more questions you start to come back into reality and scream out at the pain across your body. It's died down and is no longer even a fraction of what it had been but still the pain is agonizing and your snaps out of the dreamlike sight you had viewed before and the memory of it becomes fuzzy. You recollect yourself mentally and stand shakily, before lies the pond full of black waters with the statue showing an incredibly angered face directed at you. To your right is the passage you came from, and as you peer into its darkness you hear the same faint ringing you heard before. To your left the passageway you've yet to venture into, silent and dark as the abyss.\n")
						kwargs['hero'].takeDamage(6)
						kwargs['kinter'].updateStatus(kwargs['hero'])
						kwargs['kinter'].eventMessage(f"\nThe agonizing pain ringing across your body finally comes to a stop but it's certainly left its mark, your health falls to {kwargs['hero'].curHealth}\n")
						if kwargs['hero'].curHealth == 0:
							self.death(kwargs['kinter'], "\nYour vision starts to go fuzzy and fade out and your body goes limp. For a moment you think you are going to see more of this dreamscape you peered into before, however you quickly come to terms with the fact that this is not the case but rather your life itself is coming to an end.\n")
						else:
							kwargs['hero'].disillusioned = True
							pressed = kwargs['kinter'].takeInput("Do you finally embrace the waters, or leave it?\n\n8.) Embrace\n6.) leave\n\n")
							while pressed not in ['8', '6']:
								pressed = kwargs['kinter'].takeInput("")
							if pressed == '8':
								kwargs['kinter'].eventMessage("\nYou wade into the black waters and watch as a shadowy mist wraps around the statue and change its appearance to a beaming smile and holding it's hands up and together like in prayer. The water wraps around your body and all of your wounds and your fatigue are cured, you can see where your wounds had been is a flowing black fluid joining and mixing into the lighter black water. When you're fully recovered the water falls back into the pool splashing around you and again you see a shadowy mist wrap around the statue and change it to be looking fondly at the passageway you haven't traversed through and pointing an arm to it.\n")
								kwargs['hero'].acceptedMaiden = True
							elif pressed == '6':
								kwargs['kinter'].eventMessage("\nCurious about the ringing noise you've been hearing you consider heading back to where you came from and following the noise.\n\n")

############################################################## LEVEL TWO #######################################################################################

	def scientist_encounter(self, kwargs):
		#fight scientist / talk to scientist
		pass

	def conditional_encounter(self, kwargs):
		if self.floor_conditions[self.level]['foes2'] == 15:
			# fight axe demon
			pass

	def acquire_mask(self, kwargs):
		# push the character back to the tile they came from? otherwise just make it 1 i guess
		if not kwargs['hero'].hasMask:
			kwargs['hero'].hasMask = True

	def acquire_idol(self, kwargs):
		kwargs['hero'].hasIdol = True
		kwargs['curMap'].mapData[kwargs['curMap'].curY][kwargs['curMap'].curX] = 1

	def acquire_charm(self, kwargs):
		kwargs['hero'].hasCharm = True
		kwargs['kinter'].b5.config(state='normal')
		kwargs['kinter'].eventMessage("\nYou found a Charm of Awareness. Now you can press 5 to rest and gain half of your health and stamina back anywhere on the map, but you may be attacked and have to fight.\n")
		kwargs['curMap'].mapData[kwargs['curMap'].curY][kwargs['curMap'].curX] = 1

	def acquire_scalpel(self, kwargs):
		self.floor_conditions[self.level]['hasScalpel'] = True
		kwargs['kinter'].eventMessage('\n')
		kwargs['curMap'].mapData[kwargs['curMap'].curY][kwargs['curMap'].curX] = 1

	def acquire_water(self, kwargs):
		if 'canteen' in kwargs['hero'].heldInventory:
			# put water in canteen
			kwargs['hero'].heldInventory[kwargs['hero'].heldInventory.index('canteen')] = 'filled canteen'
			kwarg['kinter'].updateInventory(kwargs['hero'])
		else:
			kwargs['kinter'].eventMessage("\nYour feet get wet as you step into a small pool of water trickling down from the cavern walls.\n")

	def random_encounter(self, kwargs):
		# make individual ones for the 6 encounter zones
		pass

	def poison_tile(self, kwargs):
		if not kwargs['hero'].hasMask:
			kwargs['hero'].takeDamage(kwargs['hero'].Stats['Health']/8)
			kwargs['kinter'].updateStatus(kwargs['hero'])
			kwargs['kinter'].eventMessage(f"\nThe poison eats away at you. You took {kwargs['hero'].Stats['Health']/8} damage.\nYour health is now {kwargs['hero'].curHealth}.\n")
	
	def adoma_encounter(self, kwargs):
		pass

	def tile_event(self, **kwargs):
		self.floor_events[self.level][kwargs['curMap'].mapData[kwargs['curMap'].curY][kwargs['curMap'].curX]](kwargs)

	def setEvents(self):
		self.floor_events[1] = {
			1: self.open_tile,
			20: self.dig,
			24: self.rat_encounter,
			23: self.maiden_encounter,
			21: self.next_map,
		}
		self.floor_events[2] = {
			1: self.open_tile,
			2: self.scientist_encounter,
			20:	self.next_map,
			21: self.conditional_encounter,
			3: self.acquire_mask,
			30: self.pickup_item,
			31: self.acquire_idol,
			32: self.acquire_charm,
			33: self.acquire_scalpel,
			34: self.acquire_water,
			40: self.random_encounter,
			5: self.poison_tile,
			90: self.adoma_encounter,
		}