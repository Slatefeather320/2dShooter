import pygame, random, math, tkinter
width = 600; height = 600
window = pygame.display.set_mode((width, height)) 
pygame.display.set_caption('2D Shooter Engine v1.9')
fps = 90
dt = 1/fps
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 16)

print("Hi, this game is currently nowhere close to playable | I would recomend enabling test mode from commands. Press Z for commands.")

class Player:
    def __init__(self,xpos,ypos):
        self.pos = pygame.Vector2()
        self.pos.x = xpos
        self.pos.y = ypos
        self.speed = 200*dt
        self.maxLaser = 0
        self.moveState = "none"
        self.money = 0
        self.UI = True
        self.health = 100
        self.ammo = 20
    def render(self):
        pygame.draw.circle(window, (255,255,255), self.pos, 22)
        if self.UI:
            moneyText = font.render(str(p.money), True, (250,250,200))
            window.blit(moneyText,(p.pos.x-50,p.pos.y+20))
            healthText = font.render(str(p.health), True, (200,250,250))
            window.blit(healthText,(p.pos.x+20,p.pos.y+20))
            ammoText = font.render(str(p.ammo), True, (255,220,220))
            window.blit(ammoText,(p.pos.x-10,p.pos.y+30))
    def renderLaserRecursive(self,previousStart, previousEnd,i):
        if i>0:
            i-= 1
            laserVect = pygame.Vector2()
            laserVect = previousEnd-previousStart
            boucePoint = pygame.Vector2()
            y1 = previousStart.y
            y2 = previousEnd.y
            x1 = previousStart.x
            x2 = previousEnd.x
            try:
                m = (y2-y1)/(x2-x1)
            except:
                m = math.inf
            if m==0:
                m=0.00000000000000000000001 #I don't think devision by m should ever happen when m=0 but better safe then sorry
            if x1 == 0:
                x1 = 0.0000000000000000000000001
            # y - y1 = m*(x - x1) is the equation of line
            if x2>width and y2 > height: #rightwall-floor quadrant
                if m > ((height - y1) / (width - x1)): #floor
                    boucePoint.y = height
                    boucePoint.x = x1 + ((boucePoint.y-y1)/m)
                    laserVect.y *= -1
                else: #rightwall
                    boucePoint.x = width
                    boucePoint.y = y1 + m*(boucePoint.x-x1)
                    laserVect.x *= -1
            elif x2<0 and y2> height: #leftwall-floor quadrant
                if (((height-y1)/x1))>abs(m): #leftwall
                    boucePoint.x = 0
                    boucePoint.y = y1 + m*(boucePoint.x-x1)
                    laserVect.x *= -1
                else: #floor
                    boucePoint.y = height
                    boucePoint.x = x1 + ((boucePoint.y-y1)/m)
                    laserVect.y *= -1
            elif x2 > width and y2 < 0: #rightwall-ceiling quadrant
                if(y1/(width-x1))>abs(m): #rightwall
                    boucePoint.x = width
                    boucePoint.y = y1 + m*(boucePoint.x-x1)
                    laserVect.x *= -1
                else: #ceiling 
                    boucePoint.y = 0
                    boucePoint.x = x1 + ((boucePoint.y-y1)/m)
                    laserVect.y *= -1
            elif x2<0 and y2<0: #leftwall-ceiling quadrant
                if y1/x1>m: #leftwall
                    boucePoint.x = 0
                    boucePoint.y = y1 + m*(boucePoint.x-x1)
                    laserVect.x *= -1
                else: #ceiling
                    boucePoint.y = 0
                    boucePoint.x = x1 + ((boucePoint.y-y1)/m)
                    laserVect.y *= -1
            elif previousEnd.x > width: #then we know x=width, solve for y | rightwall
                boucePoint.x = width
                boucePoint.y = y1 + m*(boucePoint.x-x1)
                laserVect.x *= -1
            elif previousEnd.x < 0: #then we know x=0, solve for y | leftwall
                boucePoint.x = 0
                boucePoint.y = y1 + m*(boucePoint.x-x1)
                laserVect.x *= -1
            elif previousEnd.y > height: #y=heigh | -y1 = m(x-x1) | floor
                boucePoint.y = height
                boucePoint.x = x1 + ((boucePoint.y-y1)/m)
                laserVect.y *= -1
            elif previousEnd.y < 0: #y=heigh | -y1 = m(x-x1) | ceiling 
                boucePoint.y = 0
                boucePoint.x = x1 + ((boucePoint.y-y1)/m)
                laserVect.y *= -1
            pygame.draw.line(window,(255,0,0),boucePoint,boucePoint+laserVect,2)
            self.renderLaserRecursive(boucePoint,boucePoint+laserVect,i)
    def renderLaser(self):
        if self.maxLaser>0:
            laserVect = pygame.Vector2()
            laserVect = ((mousePos-self.pos).normalize())*width*1.5
            pygame.draw.line(window,(255,0,0),self.pos,self.pos+laserVect,2)
            self.renderLaserRecursive(self.pos,self.pos+laserVect,self.maxLaser-1)
    def moveUp(self):
        if self.moveState == "full" or self.moveState == "line":
            if not (self.pos.y<0):
                self.pos.y -= self.speed
    def moveDown(self):
        if self.moveState == "full" or self.moveState == "line":
            if not (self.pos.y>height):
                self.pos.y += self.speed
    def moveLeft(self):
        if self.moveState == "full":
            if not (self.pos.x<0):
                self.pos.x -= self.speed
    def moveRight(self):
        if self.moveState == "full":
            if not (self.pos.x>width):
                self.pos.x += self.speed
    def main(self):
        self.renderLaser()
        self.render()
        
class Bullets:
    def __init__(self):
        self.number = 0
        self.poss = []
        self.velocitys = []
        self.bounces = []
        self.dead = []
        self.framesSinceLastShoot = 0
        self.throughs = []

        self.speed = 1000*dt
        self.maxBounce = 1
        self.cooldown = 0.4
        self.MaxThrough = 0
    def new(self):
        self.number += 1
        mypos = pygame.Vector2()
        mypos[:] = p.pos.x, p.pos.y
        self.poss.append(mypos)
        velocity = pygame.Vector2()
        velocity = self.speed*((mousePos - mypos).normalize())
        self.velocitys.append(velocity)
        self.bounces.append(self.maxBounce)
        self.throughs.append(self.MaxThrough)
    def newSplat(self,amount):
        for i in range(0,amount):
            self.number += 1
            mypos = pygame.Vector2()
            mypos[:] = p.pos.x, p.pos.y
            self.poss.append(mypos)
            velocity = pygame.Vector2()
            angle = (2*math.pi/amount)*i
            velocity[:] = self.speed*math.cos(angle),self.speed*math.sin(angle)
            self.velocitys.append(velocity)
            self.bounces.append(self.maxBounce)
            self.throughs.append(self.MaxThrough)
    def kill(self):
        killed = 0
        for i in self.dead:
            self.poss.pop(i-killed)
            self.velocitys.pop(i-killed)
            self.bounces.pop(i-killed)
            self.throughs.pop(i-killed)
            self.number -= 1
            killed+=1
        self.dead = []
    def move(self):
        self.framesSinceLastShoot += 1
        for i in range(0,self.number):
            self.poss[i] += self.velocitys[i]
            if self.bounces[i]>0:
                if self.poss[i].x > width:
                    self.velocitys[i].x *= -1
                    self.bounces[i] -= 1
                if self.poss[i].y > height:
                    self.velocitys[i].y *= -1
                    self.bounces[i] -= 1
                if self.poss[i].x < 0:
                    self.velocitys[i].x *= -1
                    self.bounces[i] -= 1
                if self.poss[i].y < 0:
                    self.velocitys[i].y *= -1
                    self.bounces[i] -= 1
            else:
                self.dead.append(i)
    def shoot(self):
        if self.framesSinceLastShoot*dt > self.cooldown and p.ammo > 0:
            self.new()
            self.framesSinceLastShoot = 0
            p.ammo -= 1
    def render(self):
        for i in range(0,self.number):
            pygame.draw.circle(window, (150,150,200), self.poss[i], 10)
    def main(self):
        self.kill()
        self.move()
        self.render()
    def clear(self):
        self.dead = range(0,self.number)

class Enemy:
    def __init__(self):
        self.values = []
        self.number = 0
        self.poss = []
        self.dead = []
        self.modes = []
        self.lerpStage = []
        self.currentTargets = []
        self.timeToLerp = 300
    def kill(self):
        killed = 0
        for i in self.dead:
            self.poss.pop(i-killed)
            self.values.pop(i-killed)
            self.modes.pop(i-killed)
            self.lerpStage.pop(i-killed)
            self.currentTargets.pop(i-killed)
            self.number -= 1
            killed+=1
        self.dead = []
    def spawnAt(self,point, value):
        self.number += 1
        self.poss.append(point)
        self.values.append(value)
        self.modes.append("static")
        self.lerpStage.append(0)
        self.currentTargets.append("none")
    def spawnRandom(self):
        point = pygame.Vector2()
        point[:] = random.randint(0,width),random.randint(0,height)
        self.number += 1
        self.poss.append(point)
        self.values.append(random.randint(4,8)) 
        self.modes.append("static")
        self.lerpStage.append(0)
        self.currentTargets.append("none")
    def collisions(self):
        for i in range(0,self.number):
            for bi in range(0,b.number):
                vect = self.poss[i] - b.poss[bi]
                if vect.length() < 20:
                    p.money += self.values[i]
                    self.dead.append(i)
                    if b.throughs[bi]>0:
                        b.throughs[bi] -= 1
                    else:
                        if bi not in b.dead: #i have no idea why this game doesnt work without this check, ideally there is noreason the same bullet should be appended to dead twice but sometimes it is
                            b.dead.append(bi)
                    break
    def spawnAttacker(self):
        self.number += 1
        self.poss.append(pygame.Vector2(width,height/2))
        self.values.append(random.randint(4,8))
        self.modes.append("attacker")
        self.lerpStage.append(0)
        self.currentTargets.append(pygame.Vector2(width - 30, random.randint(0,height)))
    def chooseTarget(self, index):
        self.lerpStage[index] = 0
        if self.poss[index][0] > p.pos.x+30:
            self.currentTargets[index] = pygame.Vector2(self.poss[index].x - 30, random.randint(0,height))
        else:
            self.currentTargets[index] = pygame.Vector2(self.poss[index].x - (self.poss[index]-p.pos).normalize().x*15 , self.poss[index].y - (self.poss[index]-p.pos).normalize().y*30)
        if (self.poss[index] - p.pos).magnitude() < 30:
            print("hitreg")
    def attack(self):
        for i in range(0,self.number):
            if self.modes[i] == "attacker":
                self.poss[i] = pygame.Vector2.lerp(self.poss[i],self.currentTargets[i],self.lerpStage[i]/self.timeToLerp)
                self.lerpStage[i] += 1
                if self.lerpStage[i] > 99:
                    self.chooseTarget(i)
    def render(self):
        for i in range(0,self.number):
            pygame.draw.circle(window, (230,150,150), self.poss[i], 20)
    def main(self):
        self.kill()
        self.collisions()
        self.attack()
        self.render()

class Menu:
    def __init__(self):
        self.command = []
        self.commands = ["pspeed","espeed","bspeed","lasers","bounces","through","cooldown","width","height","exit","clearall","splat","french","pmove","test","help"]
    def makeCommand(self):
        global width, height, running, window
        print("Command Menu | type 'help' for help")
        self.command = str(input(">")).lstrip().lower().split()
        if self.command[0] in self.commands:
            try:
                if self.command[0] == "pspeed":
                    p.speed = int(self.command[1])*dt
                if self.command[0] == "bspeed":
                    b.speed = int(self.command[1])*dt
                if self.command[0] == "bounces":
                    b.maxBounce = int(self.command[1])
                if self.command[0] == "through":
                    b.MaxThrough = int(self.command[1])
                if self.command[0] == "lasers":
                    p.maxLaser = int(self.command[1])
                if self.command[0] == "cooldown":
                    b.cooldown = float(self.command[1])
                if self.command[0] == "height":
                    height = int(self.command[1])
                    window = pygame.display.set_mode((width, height)) 
                if self.command[0] == "width":
                    width = int(self.command[1])
                    window = pygame.display.set_mode((width, height)) 
                if self.command[0] == "exit":
                    running = False
                if self.command[0] == "clearall":
                    b.clear()
                if self.command[0] == "splat":
                    if len(self.command) > 1:
                        b.newSplat(int(self.command[1]))
                    else:
                        b.newSplat(360)
                if self.command[0] == "french":
                    if self.command[1] == "exit":
                        print("oui oui bye bye") 
                        running = False
                    else:
                        print("french what")
                if self.command[0]=="pmove":
                    if self.command[1].lower() in ["full","line","none"]:
                        p.moveState = self.command[1].lower()
                    else:
                        print("invalid move state, please choose from Full, Line, or None")
                        self.makeCommand()
                if self.command[0]=="test":
                    p.speed = 600*dt
                    p.maxLaser = 3
                    p.health = 100
                    p.moveState = "full"
                    b.cooldown = 0.08
                    b.speed = 2400*dt
                    b.MaxThrough = 5
                    b.maxBounce = 3
                    p.health = math.inf
                    p.money = math.inf
                    p.ammo = math.inf
                if self.command[0] == "help":
                    print('''Commands:
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
> splat 500''')
                    self.makeCommand()
            except:
                print("invalid command")
                self.makeCommand()
        else:
            print("invalid command")
            self.makeCommand()

class Shop:
    def __init__(self):
        self.note = ""
    def buyAmmo(self):
        if p.money > 100:
            p.money -= 100
            p.ammo += 30
        else:
            self.note = "Not Enough Money"
        self.window.destroy()
        self.open()
    def open(self):
        self.window = tkinter.Tk()
        self.lable = tkinter.Label(text="Shop")
        self.money = ""
        self.money = tkinter.Label(text=("money: "+str(p.money))).pack()
        self.noticeLable = tkinter.Label(text=self.note).pack()
        self.buyButton = tkinter.Button(text="Buy Ammo (30 for 100)",width=10,height=1,command=self.buyAmmo).pack()
        self.closeButton = tkinter.Button(text="Close",width=10,height=1,command=self.window.destroy).pack()
        self.window.mainloop()
        self.note = ""
        
p = Player(width/8,height/2)
b = Bullets()
e = Enemy()
m = Menu()
shop = Shop()
mousePos = pygame.Vector2()
running = True
while running:
    pygame.time.Clock().tick(fps)
    mousePos[:] = pygame.mouse.get_pos()
    mouseState= pygame.mouse.get_pressed()
    window.fill((0,0,0))
    p.main()
    b.main()
    e.main()
    pygame.display.update()

    if mouseState[0]:
        b.shoot()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:    
        p.moveUp()
    if keys[pygame.K_DOWN]:    
        p.moveDown()
    if keys[pygame.K_LEFT]:    
        p.moveLeft()
    if keys[pygame.K_RIGHT]:    
        p.moveRight()
    if keys[pygame.K_w]:    
        p.moveUp()
    if keys[pygame.K_s]:    
        p.moveDown()
    if keys[pygame.K_a]:    
        p.moveLeft()
    if keys[pygame.K_d]:    
        p.moveRight()
    if keys[pygame.K_e]:
        e.spawnRandom()
    for event in pygame.event.get():   
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                b.shoot()
            if event.key == pygame.K_z:
                m.makeCommand()
            if event.key == pygame.K_x:
                shop.open()
            if event.key == pygame.K_c:
                p.UI = not p.UI
            if event.key == pygame.K_v:
                p.speed = 600*dt
                p.maxLaser = 3
                p.health = 100
                p.moveState = "full"
                b.cooldown = 0.08
                b.speed = 2400*dt
                b.MaxThrough = 5
                b.maxBounce = 3
            if event.key == pygame.K_r:
                e.spawnAttacker()
