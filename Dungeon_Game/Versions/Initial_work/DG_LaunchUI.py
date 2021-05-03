from tkinter import *

def map1(keySet):
	
	def button8():
		buttonPressed[0] = "8"

	def button6():
		buttonPressed[0] = "6"

	def button4():
		buttonPressed[0] = "4"

	def button2():
		buttonPressed[0] = "2"

	def button5():
		buttonPressed[0] = "5"


	gameWindow = Tk()
	gameWindow.title('Dungeon Game')
	gameWindow.geometry("900x600")

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
	else:
		button8Text.set("╔═════╗\n║         8         ║\n╚═════╝")
	b8 = Button(buttonsFrame, textvariable=button8Text, bg='black', fg = 'white', command=button8)
	b8.grid(column=19, columnspan=8, row=1, pady=6)

	button6Text = StringVar()
	if keySet == "W, A, S, D, R":
		button6Text.set("╔═════╗\n║         D         ║\n╚═════╝")
	else:
		button6Text.set("╔═════╗\n║         6         ║\n╚═════╝")
	b6 = Button(buttonsFrame, textvariable=button6Text, bg='black', fg = 'white', command=button6)
	b6.grid(column=29, columnspan=8, row=2, padx=6, pady=6)

	button4Text = StringVar()
	if keySet == "W, A, S, D, R":
		button4Text.set("╔═════╗\n║         A         ║\n╚═════╝")
	else:
		button4Text.set("╔═════╗\n║         4         ║\n╚═════╝")
	b4 = Button(buttonsFrame, textvariable=button4Text, bg='black', fg = 'white', command=button4)
	b4.grid(column=9, columnspan=8, row=2, padx=6, pady=6)

	button2Text = StringVar()
	if keySet == "W, A, S, D, R":
		button2Text.set("╔═════╗\n║         S         ║\n╚═════╝")
	else:
		button2Text.set("╔═════╗\n║         2         ║\n╚═════╝")
	b2 = Button(buttonsFrame, textvariable=button2Text, bg='black', fg = 'white', command=button2)
	b2.grid(column=19, columnspan=8, row=3, pady=6)

	button5Text = StringVar()
	if keySet == "W, A, S, D, R":
		button5Text.set("╔═════╗\n║         R         ║\n╚═════╝")
	else:
		button5Text.set("╔═════╗\n║         5         ║\n╚═════╝")
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
