import minescript
from math import *
import sys
import keyboard
import time


class Colors:
    turret = [0,255,255]
    trail = [166,214,8]

def direction(yaw,pitch):
    yaw = radians(yaw)
    pitch = radians(pitch)
    return [-cos(pitch) * sin(yaw),-sin(pitch), cos(pitch) * cos(yaw)]

def particle(pos,color):
    x,y,z = pos
    r,g,b = [i/255 for i in color]
    minescript.execute(f"particle minecraft:dust {r} {g} {b} 1 {x} {y} {z}")

def magnitude(vec):
    return sqrt(sum([i**2 for i in vec]))

def normalize(vec):
    m = magnitude(vec)
    return [i/m for i in vec]

def aimtotarget(turret_pos,n=30):
    look = normalize(direction(*minescript.player_orientation()))
    player_pos = minescript.player_position()
    player_pos[1]+=1.5
    try:
        target = minescript.player_get_targeted_block(64)[0]
        target[1]+=1
    except:
        target = [player_pos[i]+look[i]*(n-1) for i in range(3)]
    trail_dir = normalize([target[i]-turret_pos[i] for i in range(3)])
    return trail_dir
    

class Game:
    def __init__(self):
        self.running = True
        self.turrets = []
        self.shootangles = []
        self.aiming = False
    def add_turret(self):
        x,y,z = minescript.player_get_targeted_block()[0]
        y+=2
        self.turrets.append([x,y,z])
    def remove_turret(self):
        self.turrets.pop()

def shoot(pos,motion,power=5):
    x,y,z = pos
    dx,dy,dz = [i*power for i in motion]
    minescript.execute(f"summon minecraft:arrow {x} {y} {z} {{Motion:[{dx},{dy},{dz}]}}")

def checkinput(event,game):
    key = event.name
    if key == "k":
        game.running = False
    elif key == "p":
        game.add_turret()
    elif key == "o":
        game.remove_turret()
    elif key == "i":
        game.aiming = not game.aiming
    elif key == "m":
        for i in range(len(game.turrets)):
            shoot(game.turrets[i],game.shootangles[i])



def main():
    game = Game()
    n=10
    keyboard.on_press(lambda event:checkinput(event,game))
    while game.running:
        time.sleep(0.5)
        aims = [aimtotarget(t) for t in game.turrets]
        game.shootangles = aims
        for turret in range(len(game.turrets)):
            particle(game.turrets[turret],Colors.turret)
            if game.aiming:
                t_trails = [[game.turrets[turret][i]+game.shootangles[turret][i]*u for i in range(3)]for u in range(n)]
                for t in t_trails:
                    particle(t,Colors.trail)

    sys.exit()

    

if __name__ == "__main__":
    main()