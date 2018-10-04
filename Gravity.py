from tkinter import *
import math
import random
import time

window = Tk()
window.title("Gravity")
can = Canvas(window, width=600, height=600)
fr = Frame(window)
can.pack()
fr.pack()
obs = []
for x in range(random.randint(10,20)):
	comp = []
	for s in range(2): comp.append(random.randint(100,500))
	for s in range(2): comp.append(random.uniform(-0.1,0.1))
	obs.append(comp)
obs = [[300, 300, -0.1, 0], [300, 250, 0.1, 0]]
def angle(ox, oy, tx, ty): #This function returns the angle point 1 will face to be towards point 2
	deltx, delty = float(ox)-float(tx), float(oy)-float(ty)
	if deltx >= 0: return math.atan2(abs(deltx),delty)+math.pi
	else: return math.atan2(abs(deltx),delty*-1)
def dis(ox, oy, tx, ty): #This function returns the distance between point 1 and point 2
	x, y = abs(ox-tx), abs(oy-ty)
	return max(x*x+y*y, 0.1)
def tick(num): #This function runs a tick
	render(num)
	grav()
	move()
	can.update()
	time.sleep(0.00001)
	can.delete(ALL)
def render(num):
	for r in obs: 
		can.create_oval(r[0]+1, r[1]+1, r[0]-1, r[1]-1, tag=str(num), fill="black")
def grav():
	for r in range(len(obs)):
		data, x, y = list(tuple(obs)), obs[r][0], obs[r][1]
		del data[r]
		for t in range(len(data)):
			tx, ty = data[t][0], data[t][1]
			F, an = 1.0/dis(x, y, tx, ty), angle(x, y, tx, ty)
			obs[r].insert(2, obs[r].pop(2)+math.sin(an)*F)
			obs[r].insert(3, obs[r].pop(3)+math.cos(an)*F)
def move():
	for x in obs:
		x.insert(0, x.pop(0)+x[1])
		x.insert(1, x.pop(1)+x[2])
count = 0
while True:
    tick(count)
    can.delete()
    count += 1

window.mainloop()