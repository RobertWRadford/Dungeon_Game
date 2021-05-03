from tkinter import filedialog
from characters import Combatant, Hero
from maps import Map
from levels import Levels
from kinter import GameWindow
import pickle

def makeWindow(hero, curMap, level, keySet, resolution):

	game = GameWindow(keySet, resolution)

	def gamePlay(hero, curMap, level):

		def updateMap(curMap):
			curMap.printEnvironment()
			game.Update_Map(curMap)

		state = 'normal' if hero.hasCharm else 'disabled'
		game.b5.config(state=state)

		game.updateStatus(hero)
		updated = False
		while hero.curHealth > 0:
			if not updated:
				updateMap(curMap)
				updated=False
			pressed = game.takeInput("\nmove up, down, right, or left?\n\n8.) Up\n6.) Right\n4.) Left\n2.) Down\n\n")

			movements = {
				'2': [1,0,'down'],
				'4': [0,-1,'left'],
				'6': [0,1,'right'],
				'8': [-1,0,'up'],
				'0': [0,0,'rest'],
			}

			if pressed in movements:

				#check for inbounds
				if 0 < curMap.curY+movements[pressed][0] < curMap.lastRow and 0 < curMap.curX+movements[pressed][1] < curMap.lastCol:

					#check for impassable terrain
					if curMap.mapData[curMap.curY+movements[pressed][0]][curMap.curX+movements[pressed][1]] == 0:
						game.eventMessage(f"\nCannot move {movements[pressed][2]}")

					else:
						curMap.curY+=movements[pressed][0]
						curMap.curX+=movements[pressed][1]
						updateMap(curMap)
						level.tile_event(curMap=curMap, kinter=game, hero=hero)
						hero.fatigueStatus(-.5*hero.Stats['Stam'])
						hero.takeDamage(-1*(hero.Stats['Health']//20))
						game.updateStatus(hero)

	def saveGame(hero, curMap, level):
		askName = filedialog.asksaveasfilename(initialdir = "../Dungeon_Game/savefiles",  filetypes = (("pkl","*.pkl"),("all files","*.*")))
		if '.pkl' not in askName:
			askName+='.pkl'
		with open(askName, 'wb') as pickled_file:
			data = {
				'hero': hero,
				'map': curMap,
				'level': level,
			}
			pickle.dump(data, pickled_file)

	def loadGame():
		askName = filedialog.askopenfilename(initialdir = "../Dungeon_Game/savefiles", filetypes = (("pkl","*.pkl"),("all files","*.*")))
		with open(askName, 'rb') as pickled_file:
			loadedData = pickle.load(pickled_file)
			gamePlay(loadedData['hero'], loadedData['map'], loadedData['level'])

	game.saveMenu.entryconfigure(0, command=lambda: saveGame(hero, curMap, level))
	game.loadMenu.entryconfigure(0, command=lambda: loadGame())

	gamePlay(hero, curMap, level)

	game.window.mainloop()

def setup(keySet, resolution):
	hero = Hero({
		"Name": 'Hero',
		"Lvl": 1,
		"Exp": 0,
		"Atk": 3,
		"Def": 4,
		"Stam": 3,
		"Health": 25,
		"ExpPoint": 50,
		"Skills": [],
	})
	curMap = Map()
	level = Levels()
	makeWindow(hero, curMap, level, keySet, resolution)
	
	
	