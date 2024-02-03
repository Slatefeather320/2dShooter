# 2dShooter
I have been working on porting an old Scratch game to python. In the process of doing so, I have made this 2d shooter game engine in the process. 

Version 1.8 3/2/2024
needs python, pygame, and tkinter to run

Controls:
wasd or arrow keys to move around
space or left click to shoot
e to spawn enemies at random position
z to open commands in terminal
x to open shop (feature not fully implimented)
c to toggle ui

Commands:
pspeed [x] | Changes player speed to x 
bspeed [x] | Changes bullet speed to x
lasers [x] | Changes how many times laser bounces off wall to x, set to 0 or negitive value for no laser
bounces [x] | Changes how many times bullets can bounce of walls before disappearing
through [x] | Changes how many enemies the bullets can go through before disappearing to x
cooldown [x] | Changes number of seconds between consecutive shots when mouse is held down to x seconds. Can be set to 0 to remove
width [x] | Changes width of window
height [x] | Changes width of window 
exit | Exits program
clearall | Removes all bullets currently on screen
splat | Spawns 360 bullets forming a circle around the player shooting in all dierctions
splat [x] | Spawns x bullets forming a circle around the player shooting in all dierctions 
french exit | Exits the program in French
pmove [move state] | enter "none","line" or "full" as movestates to change degree of movement player has. 
test | enables test mode, infinite ammo, infinite money etc.

Example command:
> splat 500
