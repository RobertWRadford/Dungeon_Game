from tkinter import *
import ctypes
from gameplay import setup

def launchApp():
	keySet, resolution, user32 = ["8, 6, 4, 2, 5"], [], ctypes.windll.user32
	resolution.append(user32.GetSystemMetrics(0))
	resolution.append(user32.GetSystemMetrics(1))

	def keyChoice():

		def closed():
			keys_btn.config(command=keyChoice)
			keys.destroy()

		def set_nums():
			wasd.deselect()
			nums_bool.set(True)
			wasd_bool.set(False)
			
		def set_wasd():
			nums.deselect()
			nums_bool.set(False)
			wasd_bool.set(True)

		def store():
			keySet[0] = "8, 6, 4, 2, 5" if nums_bool.get() else "W, A, S, D, R"
			keys_btn.config(command=keyChoice)
			keys.destroy()
			
		nums_bool, wasd_bool = BooleanVar(), BooleanVar()
		
		keys = Toplevel()
		keys.configure(bg='dim gray')
		keys.title('Key sets')
		keysPush = '160x110+'+str(int(resolution[0])//2-80)+'+'+str(int(resolution[1])//2-5)
		keys.geometry(keysPush)

		keys_btn.config(command=lambda:None)

		checkButtonsFrame = Frame(keys, bg='dim gray')
		checkButtonsFrame.grid()

		nums = Checkbutton(checkButtonsFrame, text="8, 6, 4, 2, 5", bg='dim gray', fg='black', variable=nums_bool, command=set_nums)
		nums.grid(columnspan=13, pady=3, padx=3, sticky="w")

		wasd = Checkbutton(checkButtonsFrame, text="W, A, S, D, R", bg='dim gray', fg='black', variable=wasd_bool, command=set_wasd)
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
		setup(keySet[0], resolution)
		
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

	keys_btn = Button(launchFrame, text="Set keys", bg='gray9',fg='red4', command=keyChoice)
	keys_btn.grid(row=3, column=18, columnspan=14, pady=3, sticky="we")

	launch_btn = Button(launchFrame, text="Launch game", bg='gray9',fg='red4', command=goToMap1)
	launch_btn.grid(row=4, column=18, columnspan=14, pady=3, sticky="we")

	launch.mainloop()

if __name__ == "__main__":
	launchApp()