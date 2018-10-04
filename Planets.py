from tkinter import *
import math
import time
import random

G = 10
fps = 1000
di = [1500, 700] #The canvas dimentions
def fps_change(val):
	global fps
	fps=int(val)
	
master = Tk()
master.title("Gravity")
widget = Canvas(master, width=di[0], height=di[1], bg="#010101")
widget.pack()
speed = Scale(orient="horizontal", from_=0, to_=1000, command=fps_change)
speed.set(fps)
speed.pack()

class Planet():
	"""
	A Planet Object With Position, Mass, And Velocity. 
	"""
	def __init__(self, position=[0, 0], velocity=[0,0], mass=1):
		super(Planet, self).__init__()
		self.pos, self.velo, self.mass = list(position), list(velocity), float(mass)

	def __getitem__(self, key): return [self.pos, self.velo, self.mass][int(key)]

	def distance(self, other): return math.sqrt((self.pos[0]+other.pos[0])**2+(self.pos[1]-other.pos[0])**2)

	def angle(self, other):
		deltax, deltay = self.pos[0]-other.pos[0], self.pos[1]-other.pos[1]
		if deltax >= 0: return math.atan2(deltax,deltay)+math.pi
		else: return math.atan2(abs(deltax),deltay*-1)

planets_list = []
for x in range(5):
        planets_list.append(Planet([random.randint(di[0]*0.2, di[0]*0.8), random.randint(di[1]*0.2,di[1]*0.8)], [random.random()-0.5, random.random()-0.54], random.random()*10))
planets_list = [Planet([di[0]/2, di[1]*0.3], [1, 0], 1), Planet([di[0]/2, di[1]/2], [0, 0], 1000)]

def main(planets):
	planets = list(planets)
	print (planets[1].velo)
	for current in planets:
		others = list(planets)
		del others[others.index(current)]
		for other in others:
			F, angle = ((G*current[2]*other[2])/(current.distance(other)**2))/current[2], current.angle(other)
			current[1][0], current[1][1] = (current[1][0]+math.sin(angle)*F), (current[1][1]+math.cos(angle)*F)
	for current in planets: current[0][0], current[0][1] = current[0][0]+current[1][0], current[0][1]+current[1][1]
	return planets

def draw_planets(planets, canvas):
	canvas.delete(ALL)
	for m in planets:
		r = math.sqrt(m[2]/3.14159)*2 #The mass used for the radius
		color = "#a6d3f6"
		canvas.create_oval(m[0][0]+r, m[0][1]+r, m[0][0]-r, m[0][1]-r, fill=color, outline="white", width=0)
		canvas.create_line(m.pos[0], m.pos[1], m.pos[0]+m.velo[0]*(10**2), m.pos[1]+m.velo[1]*(10**2), fill="white")
	canvas.update()

def add(event): 
	new = Planet([event.x, event.y], [0, 0], random.random()*10)
	planets_list.append(new)
	return new

while True:
	while fps == 0:
		pass
	time.sleep(1/fps)
	planets_list = main(planets_list)
	draw_planets(planets_list, widget)
	widget.bind("<Button-1>", add)