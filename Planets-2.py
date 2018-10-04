from tkinter import *
import math
import time
import random

G = 5.5 #The gravitational constant
fps = 1000 #The fps (only kind of works)
di = [1500, 700] #The canvas dimentions

def fps_change(val): #Used for the fps changing slider
	global fps
	fps = int(val)
	print (fps)
	return fps

def grav_change(val): #Used for the slider that changes G
	global G
	G = int(val)
	print (G)
	return G

LINES = 0 #Velocity lines   #0 for off, 1 for on
CENTER = 0 #Center the screen on the first planet   #0 for off, 1 for on
	
master = Tk() #The Tkinter window
master.title("Gravity")

widget = Canvas(master, width=di[0], height=di[1], bg="#010101") #The canvas that everything shows up on
widget.pack()

gravity = Scale(master, orient="horizontal", from_=0, to_=1000, command=grav_change) #The slider for changing G
gravity.set(G)
gravity.pack(fill=X)

speed = Scale(master, orient="horizontal", from_=1, to_=1000, command=fps_change) #The slider for changing the fps
speed.set(fps)
speed.pack(side=LEFT)

#center = Checkbutton(master, text="Center on first planet", variable=CENTER)


class Planet():
	"""
	A Planet Object With Position, Mass, And Velocity. 
	"""
	def __init__(self, position=[0, 0], velocity=[0,0], mass=1): #Initilize each planet with a [x, y] position, [x, y] velocity, and a mas
		super(Planet, self).__init__()
		self.pos, self.velo, self.mass = list(position), list(velocity), float(mass)
		self.radius = math.sqrt(self.mass/3.14159)*2

	def __getitem__(self, key): return [self.pos, self.velo, self.mass][int(key)] #Make the attributes of the planet addressable

	def distance(self, other): return math.sqrt((self.pos[0]+other.pos[0])**2+(self.pos[1]-other.pos[0])**2) #Calculate the distance from the planet to another, take a planet as input (A^2+B^2=C^2)

	def angle(self, other): #Calculate the angle from the planet to another, take a planet as input
		deltax, deltay = self.pos[0]-other.pos[0], self.pos[1]-other.pos[1] #Fid the x and y difference between the two planets 
		if deltax >= 0: return math.atan2(deltax,deltay)+math.pi
		else: return math.atan2(abs(deltax),deltay*-1)

planets_list = []
for x in range(5): #Randomly creates planets
        planets_list.append(Planet([random.randint(di[0]*0.2, di[0]*0.8), random.randint(di[1]*0.2,di[1]*0.8)], [random.random()-0.5, random.random()-0.54], random.random()*10))

#A few presets
#planets_list = [Planet([di[0]/2, di[1]/2], [0, 0], 1000), Planet([di[0]/1.9, di[1]/2], [0, 1], 1)]
#planets_list = [Planet([di[0]/2, di[1]/2], [0, 0], 1000)]
#planets_list = []

def main(planets): #
	for x in range(len(planets)):
		current = planets[x]

		for other in planets[x+1:]:

			F, angle = (max(G, 0.00000000000000001)*current[2]*other[2])/(current.distance(other)**2), current.angle(other) #Fints the angle and force between to two planets being compared

			current.velo[0], current.velo[1] = (current.velo[0]+math.sin(angle)*(F/current.mass)), (current.velo[1]+math.cos(angle)*(F/current.mass)) #Updates the current planet's velocity to take in to account the planet it was just compared to
			other.velo[0], other.velo[1] = (other.velo[0]+math.sin((angle+3.14159)%6.283185)*(F/other.mass)), (other.velo[1]+math.cos((angle+3.14159)%6.283185)*(F/other.mass)) #Updates the compared to 

		current.pos[0], current.pos[1] = current.pos[0]+current.velo[0]/10, current.pos[1]+current.velo[1]/10
	return planets

def draw_planets(planets, canvas): #Draws each planet on the canvas then updates the canvas to show them
	canvas.delete(ALL)
	offset = off()
	for m in planets:
		r = m.radius
		color = "#a6d3f6"
		canvas.create_oval(m[0][0]+r-offset[0], m[0][1]+r-offset[1], m[0][0]-r-offset[0], m[0][1]-r-offset[1], fill=color, outline="white", width=0) #
		if LINES: canvas.create_line(m.pos[0]-offset[0], m.pos[1]-offset[1], m.pos[0]+m.velo[0]*(10**1)-offset[0], m.pos[1]+m.velo[1]*(10**1)-offset[1], fill="white")
	canvas.update()

def add(event): #If the canvas is clicked records where
	global new
	new = [event.x, event.y]

def add2(event): #Once a canvas click is let go calculates the velocity from the mouse drag and creates a planet
	global new
	offset = off() #Gets the offset incase of centering
	new = Planet([new[0]+offset[0], new[1]+offset[1]], [(event.x-new[0])/40, (event.y-new[1])/40], random.random()*100)
	planets_list.append(new)

def off(): return [(planets_list[0].pos[0]-di[0]/2)*CENTER, (planets_list[0].pos[1]-di[1]/2)*CENTER] #Calculates how much to offset planets if centering is turned on

while True:
	try:
		while fps == 0:
			pass
		time.sleep(1/fps)
		planets_list = main(planets_list)
		draw_planets(planets_list, widget)
		widget.bind("<Button-1>", add)
		widget.bind("<ButtonRelease-1>", add2)
	except:
		break
