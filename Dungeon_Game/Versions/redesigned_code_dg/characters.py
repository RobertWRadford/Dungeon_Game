class Combatant:

	def __init__(self, stats, stamToAtk):
		self.Stats = stats
		self.curHealth = stats["Health"]
		self.curStam = stats["Stam"]*10
		self.curTokens = len(stats['Skills'])
		self.stamToAtk = stamToAtk

	def takeDamage(self, damage):
		self.curHealth = min(max(self.curHealth - damage, 0), self.Stats["Health"])

	def fatigueStatus(self, fatigue):
		self.curStam = min(max(self.curStam - fatigue, 0), self.Stats["Stam"]*10)

class Foe(Combatant):

	def __init__(self, stats, stamToAtk, topCombatSentence, fatigueSentence):
		super().__init__(stats, stamToAtk)
		self.topCombatSentence = topCombatSentence
		self.fatigueSentence = fatigueSentence

class Hero(Combatant):

	def __init__(self, stats):
		super().__init__(stats, stats['Stam']*2)
		self.inventory = []
		self.heldInventory = []
		#story progression conditionals
		self.acceptedMaiden = False
		self.firstMaidenDead = False
		self.AdomaDead = False
		self.hasCharm = False
		self.hasIdol = False
		self.hasMask = False
		self.hasSword = False
		self.disillusioned = False

	def maidenEncounter(self):
		self.acceptedMaiden = True
		self.curTokens = len(self.Stats["Skills"])
		self.curHealth = min(max(self.curHealth + (self.Stats["Health"]), 0), self.Stats["Health"])
		self.curStam = min(max(self.curStam + self.Stats['Stam']*10, 0), self.Stats['Stam']*10)

	def restRecovery(self):
		self.curTokens = len(self.Stats["Skills"])
		self.curHealth = min(max(self.curHealth + (self.Stats["Health"]/2), 0), self.Stats["Health"])
		self.curStam = min(max(self.curStam + (self.Stats['Stam']*10/2), 0), self.Stats['Stam']*10)

	def expToLvl(self):
		return max(100-self.Stats['Exp'], 0)

	### Use item should be here, and maybe a hero specific overwrite of use skills ###

	def updateLevel(self):

		if self.Stats['Lvl'] == 8:
			return

		handSkills = ["Heavy_Blow", "Counter", "Meditate", "Shatter", "Grapple", "Flurry", "Atemi"]
		swordSkills = ["Datotsu", "Haya_Suburi", "Mokuso", "Pierce", "Drain", "Regenerate", "Kachinuki"]

		while self.Stats['Exp'] >= 100:
			self.Stats['Lvl'] += 1
			self.Stats['Exp'] -= 100
			
			self.Stats["Atk"] = int(self.Stats["Atk"]*1.2)
			self.Stats["Def"] = int(self.Stats["Def"]*1.2)
			self.Stats["Stam"] = int(self.Stats["Stam"]*1.2)
			self.Stats["Health"] = int(self.Stats["Health"]*1.2)
			if self.hasSword:
				self.Stats['Skills'].append(swordSkills[self.Stats['Lvl']-1])
				self.stamToAtk = self.Stats['Stam']*3
			else:
				self.Stats['Skills'].append(handSkills[self.Stats['Lvl']-1])
				self.stamToAtk = self.Stats['Stam']*2

	def add_item(self, item):
		if item[1]:
			self.heldInventory.append(item[0])
		else:
			self.inventory.append(item[0])

	def acquire_sword(self):

		self.hasSword = True

		swordSkills = ["Datotsu", "Haya_Suburi", "Mokuso", "Pierce", "Drain", "Regenerate", "Kachinuki"]

		for i in range(len(self.Stats['Skills'])):
			self.Stats['Skills'][i] = swordSkills[i]

		multiplier = 1.2*(self.Stats['Lvl']-1) if self.Stats['Lvl']>1 else 1
		self.Stats['Atk'] += 3*(multiplier)
		self.Stats['Def'] += 1*(multiplier)
		self.Stats['Stam'] += 2*(multiplier)
		self.Stats['Health'] += 10*(multiplier)
		self.curHealth += 10*(multiplier)
		self.curStam += 2*(multiplier)
		self.stamToAtk = self.Stats['Stam']*3

	def basic_combat(self, opponent, kinter):
		combatTutorial = "\nYou can press, '8' to attack the Opponent, '6' to reduce your damage received, '4' to get double stamina returned, '2' to view your skills menu, or '5' to view your item menu.\n" if kinter.keySet == "8, 6, 4, 2, 5" else "\nYou can press, 'W' to attack the Opponent, 'D' to reduce your damage received, 'A' to get double stamina returned, 'S' to view your skills menu, or 'R' to view your item menu.\n"
		turn = 0
		kinter.b5.config(state='normal')

		while opponent.curHealth > 0 and self.curHealth > 0:
			kinter.updateStatus(self)
			kinter.eventMessage(f"\nOpponent HP:      {str(opponent.curHealth)}\nOpponent Stamina: {str(opponent.curStam)}\n\n{opponent.topCombatSentence}")
			pressed = kinter.takeInput(combatTutorial)
			
			opp_defending = False if opponent.curStam >= opponent.stamToAtk else True
			self_defending = False
			self_took_action = False
			self_attacked = False

			if turn != 0 and turn%3 == 0 and self.curTokens <= len(self.Stats["Skills"]):
				self.curTokens+=1

			if pressed == '6':
				if opponent.curStam >= opponent.stamToAtk:
					turn+=1
					self_defending, self_took_action = True, True
				else:
					kinter.eventMessage("\nYou're opponent can't attack.\n")

			elif pressed == '8':
				if self.curStam >= self.stamToAtk:
					turn+=1
					self_attacked, self_took_action = True, True
				else:
					kinter.eventMessage("\nYou are too fatigued to attack.\n")

			elif pressed == '4':
				if self.curStam >= (self.Stats["Stam"]*10)-self.Stats["Stam"]:
					kinter.eventMessage("\nYou've no need to rest now.\n")
				else:
					turn+=1
					self_took_action = True
					self.fatigueStatus(-.5*self.Stats["Stam"])
					
			elif pressed == '2':
				if self.curTokens == 0:
					kinter.eventMessage("\nYou do not have any skill points to use.\n")
				else:					
					skill = self.useSkill()
					if skill != "Back":
						turn+=1
						self_took_action = True
						### use skill :? ###

			elif pressed == '5':
				if len(inventory) == 0:
					kinter.eventMessage("\nYou don't have an item to use.\n")
				else:
					item = self.useItemCombat()
					turn+=1
					self_took_action = True
					### use item :? ###

			if self_took_action:

				self.fatigueStatus(-.5*self.Stats["Stam"])

				if self_attacked:
					self.fatigueStatus(self.stamToAtk)
					if opponent.curStam >= opponent.stamToAtk:
						opponent.takeDamage(max((self.Stats['Atk']*self.stamToAtk)//opponent.Stats['Def'], 1))
						self.takeDamage(max((opponent.Stats['Atk']*opponent.stamToAtk)//self.Stats['Def'], 1))
						opponent.fatigueStatus(opponent.stamToAtk)
					else:
						opponent.takeDamage(max((self.Stats['Atk']*self.stamToAtk)//(2*opponent.Stats['Def']), 1))

				elif self_defending:
					self.takeDamage(max((opponent.Stats['Atk']*opponent.stamToAtk)//(2*self.Stats['Def']), 1))
					opponent.fatigueStatus(opponent.stamToAtk)

				else:
					if opponent.curStam >= opponent.stamToAtk:
						self.takeDamage(max((opponent.Stats['Atk']*opponent.stamToAtk)//self.Stats['Def'], 1))
						opponent.fatigueStatus(opponent.stamToAtk)
					else:
						opponent.fatigueStatus(-.5*self.Stats['Stam'])

				opponent.fatigueStatus(-.5*self.Stats['Stam'])
		kinter.updateStatus(self)
		if self.hasCharm == False:
			kinter.b5.config(state='disabled')

