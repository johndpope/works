''' toggle collision dection with C
    shoot on the giant monsters and watch the yellow impact 'wounds'
    '''
from constants018 import *

class Lifebar(pygame.sprite.Sprite):
    def __init__(self,boss):
        self.groups = allgroup,lifebargroup
        self.boss = boss
        self._layer = self.boss._layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.oldpercent = 0
        self.paint()
    def paint(self):
        self.image = pygame.Surface( (self.boss.rect.width,7) )
        self.rect = self.image.get_rect()
        self.image.set_colorkey(black)
        pygame.draw.rect(self.image,green,(0,0,self.boss.rect.width,7),1)
    def update(self,seconds):
        self.percent = self.boss.hitpoints/self.boss.hitpointsfull
        if self.percent != self.oldpercent:
            self.paint()
            # fill black
            pygame.draw.rect(self.image,black,(1,1,self.rect.width-2,5) )
            pygame.draw.rect(self.image,green,(1,1,int(self.rect.width*self.percent),5) )
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.rect.centerx
        self.rect.centery = self.boss.rect.top - 10
        if self.boss.hitpoints < 1: self.kill()

class Bird(pygame.sprite.Sprite):
    images = []
    birds = {}  # dictionary for saving bird objects
    number = 0
    waittime = 1.0 # seconds
    def __init__(self,layer=4):
        if getClassName(self) == 'Monster':
            self.groups = birdgroup,allgroup
        else:
            self.groups = birdgroup, allgroup, gravitygroup
        self_layer = layer
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.pos = Vector(random.randint(50, screenwidth-50), random.randint(25,screenheight-25) )
        self.screen = screen.get_rect()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width/2
        self.delta = Vector(0,0) #self.dx, self.dy = 0.0, 0.0
        self.frags = 25
        self.number = Bird.number
        Bird.number += 1
        Bird.birds[self.number] = self
        self.mass = 100

    def kill(self):
        for a in range(self.frags):
            RedFragment(self.pos)
        pygame.sprite.Sprite.kill(self)
    def checkArea(self):
        if self.screen.contains(self.rect): return
        # OUT OF SCREEN
        w,h = self.rect.width, self.rect.height
        if self.rect.right > self.screen.right:
            self.pos.x = self.screen.right - w/2
            self.delta.x *= -0.5
        if self.rect.left < self.screen.left:
            self.pos.x = self.screen.left + w/2
            self.delta.x *= -0.5
        if self.rect.top < self.screen.top:
            self.pos.y = self.screen.top + h/2
            self.delta.y *= -0.5
        if self.rect.bottom > self.screen.bottom:
            self.pos.y = self.screen.bottom - h/2
            self.delta.y *= -0.5
    def move(self,seconds):
        #self.x += self.dx * seconds
        #self.y += self.dy * seconds
        self.pos = self.delta * seconds
        self.checkArea()
    def update(self, seconds):
        # move
        self.move(seconds)
        # rotating
        if self.delta.x != 0 or self.delta.y != 0:
            ratio = self.delta.y/self.delta.x
            if self.delta.x > 0: # moving right
                self.angle = -90 - atan(ratio)/pi * 180 
            else: # moving left
                self.angle = 90 - atan(ratio)/pi * 180
        self.rect.center = self.pos.x, self.pos.y
        # check health
        if self.hitpoints <= 0: self.kill()

class Monster(Bird):
    def __init__(self,image):
        self.image = image
        Bird.__init__(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.hitpoints = 1000.0
        self.hitpointsfull = 1000.0
        Lifebar(self)
    def update(self,time):
        if random.randint(1,60) == 1:
            self.delta = Vector( random.randint(-100,100), random.randint(-50,50) )
        Bird.update(self,time)

class Player(Bird):
    def __init__(self):
        self.image = Bird.images[0]
        self.image0 = Bird.images[0]
        Bird.__init__(self,layer=5)
        self.hitpoints = 100.0
        self.hitpointsfull = 100.0
        self.pos = Vector(screenrect.center)
        self.angle = 0
        self.speed = 20.0 
        self.rotatespeed = 1.0
        self.frags = 100
        Lifebar(self)
        self.cooldowntime = 0.08 # seconds
        self.cooldown = 0.0
        self.damage = 5
        self.shots = 0
        self.mass = 400.0
    def kill(self):
        bombsound.play()
        Bird.kill(self)
    def update(self, seconds):
        pressedkeys = pygame.key.get_pressed()
        self.direction = Vector(0,0)
        rad = self.angle*GRAD
        if pressedkeys[pygame.K_k]: # go upward(forward)
            self.direction = Vector( -sin(rad),-cos(rad) )
        if pressedkeys[pygame.K_j]: # go downward(backward)
            self.direction = Vector( sin(rad),cos(rad) )

        if self.cooldown > 0:
            self.cooldown -= seconds
        else:
            if pressedkeys[pygame.K_SPACE]:
                lasersound.play()
                self.shots += 1
                Bullet(self, -sin(rad), -cos(rad) )
            self.cooldown = self.cooldowntime
        # move
        self.delta = self.direction * self.speed
        self.pos  += self.delta * seconds
        self.checkArea()
        # rotate
        if pressedkeys[pygame.K_a]: # turn left, counterclockwise
            self.angle += self.rotatespeed
        if pressedkeys[pygame.K_d]:
            self.angle += -self.rotatespeed
        self.oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect(center= self.oldcenter)
        print self.pos
        self.rect.center = tuple(self.pos) #.x, self.pos.y
        if self.hitpoints <= 0:
            self.kill()


class Fragment(pygame.sprite.Sprite):
    """generic Fragment class. Inherits to blue Fragment (implosion),
       red Fragment (explosion), smoke (black) and shots (purple)"""
    def __init__(self, pos, layer = 9):
        self._layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = Vector(0,0)
        self.fragmentmaxspeed = FRAGMENTMAXSPEED# try out other factors !

    def init2(self):  # split the init method into 2 parts for better access from subclasses
        self.image = pygame.Surface((10,10))
        self.image.set_colorkey((0,0,0)) # black transparent
        pygame.draw.circle(self.image, self.color, (5,5), random.randint(2,5))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos #if you forget this line the sprite sit in the topleft corner
        self.time = 0.0
        
    def update(self, seconds):
        self.time += seconds
        if self.time > self.lifetime:
            self.kill() 
        self.pos += self.delta * seconds
        #self.pos.y += self.delta.y * seconds
        self.rect.center = self.pos #.x, self.pos.y

class RedFragment(Fragment):
    """explodes outward from (killed) Bird"""
    def __init__(self,pos):
        self.groups = allgroup, stuffgroup, fragmentgroup, gravitygroup
        Fragment.__init__(self,pos)
        #red-only part -----------------------------
        self.color = (random.randint(25,255),0,0) # red            
        self.pos = pos
        #self.pos[0] = pos[0]
        #self.pos[1] = pos[1]
        self.dx = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
        self.dy = random.randint(-self.fragmentmaxspeed,self.fragmentmaxspeed)
        self.lifetime = 1 + random.random()*3 # max 3 seconds
        self.init2() # continue with generic Fragment class
        self.mass = 48.0
        
       
class Wound(Fragment):
    """yellow impact wound that shows the exact location of the hit"""
    def __init__(self, pos, victim):
        self.color = ( random.randint(200,255), random.randint(200,255), random.randint(0,50))
        self.groups = allgroup, stuffgroup
        Fragment.__init__(self, pos, 7) # layer
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.lifetime = 1 + random.random()*2 # max 3 seconds
        Fragment.init2(self)
        self.victim = victim
    
    def update(self,time):
        self.dx = self.victim.dx
        self.dy = self.victim.dy
        Fragment.update(self, time)
       
class Bullet(Fragment):
    """a bullet flying in the direction of the BigBird's heading. May 
       be subject to gravity"""
    def __init__(self, boss, dx, dy):
        self.color = (200,0,200)
        self.boss = boss
        self.groups = allgroup, bulletgroup, gravitygroup
        Fragment.__init__(self, self.boss.rect.center, 3) # layer behind Bird
        self.pos = self.boss.pos
        #self.pos[0] = self.boss.pos[0]
        #self.pos[1] = self.boss.pos[1]
        self.lifetime = 5 # 5 seconds
        self.image = pygame.Surface((4,20))
        self.image.set_colorkey((0,0,0)) # black transparent
        pygame.draw.rect(self.image, self.color, (0,0,4,20) )
        pygame.draw.rect(self.image, (10,0,0), (0,0,4,4)) # point
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = self.boss.rect.center
        self.image = pygame.transform.rotate(self.image, self.boss.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.boss.rect.center
        self.time = 0.0
        self.bulletspeed = 250.0 # pixel per second ?
        self.bulletarc = 0.05 # perfect shot has 0.0
        arc = self.bulletspeed * self.bulletarc
        self.delta = Vector()
        self.delta.x = dx * self.bulletspeed + random.random()*2*arc -arc
        self.delta.y = dy * self.bulletspeed + random.random()*2*arc -arc
        self.mass = 25.0
        self.angle = self.boss.angle
        
    def update(self, time):
        Fragment.update(self,time)
        #--------- rotate into direction of movement ------------
        if self.delta.x != 0 and self.delta.y!=0:
            ratio = self.delta.y / self.delta.x
            if self.delta.x > 0:
                self.angle = -90 - atan(ratio)/pi*180.0 # in grad
            else:
                self.angle = 90 - atan(ratio)/pi*180.0 # in grad
        self.image = pygame.transform.rotozoom(self.image0,self.angle,1.0)

# load images into classes (class variable !). if not possible, draw ugly images
Bird.images.append(pygame.image.load(os.path.join(folder,"babytux.png")))
Bird.images.append(pygame.image.load(os.path.join(folder,"crossmonster.png")))
Bird.images.append(pygame.image.load(os.path.join(folder,"xmonster.png")))
        # ------------
for bird in Bird.images:
    bird = bird.convert_alpha()

def main():
    collision = 'rect'
    screentext = Text()
    screentext2 = Text('collision detection: %s' %collision,(200,0))
    othergroup = []
    mainloop = True
    player = Player()
    #dummy = Monster(Bird.images[1])
    #dummy2 = Monster(Bird.images[2])
    overtime = 15
    gameover = False
    hits = 0
    quota = 0
    gametime = 120
    playtime = 0
    gravity = True

    while mainloop:
        seconds = clock.tick(fps)
        playtime += seconds
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    mainloop = False
                if e.key == pygame.K_g:
                    gravity = not gravity
                if e.key == pygame.K_p:
                    printSpritelist()
                if e.key == pygame.K_c:
                    if collision == 'rect':
                        collision = 'circle'
                    elif collision == 'circle':
                        collision = 'mask'
                    elif collision == 'mask':
                        collision = 'rect'
                    screentext2.newMsg('collision detection: %s',collision)

        pygame.display.set_caption("fps: %.2f gravity: %s" % (clock.get_fps(), gravity) )

        for bird in birdgroup:
            if collision =='rect':
                crashgroup = pygame.sprite.spritecollide(bird,bulletgroup,False,pygame.sprite.collide_rect)
            if collision =='circle':
                crashgroup = pygame.sprite.spritecollide(bird,bulletgroup,False,pygame.sprite.collide_circle)
            if collision =='mask':
                crashgroup = pygame.sprite.spritecollide(bird,bulletgroup,False,pygame.sprite.collide_mask)
            # test for collision with bullet
            for bullet in crashgroup:
                if bullet.boss.number != bird.number:
                    hitsound.play()
                    bird.hitpoints -= bullet.boss.damage
                    Wound(bullet.rect.center,bird)
                    bullet.kill()
        if gravity:
            for thing in gravitygroup:
                thing.pos.y += FORCEOFGRAVITY

        # ----------- clear, draw , update, flip -----------------  
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)           
        pygame.display.flip()         

if __name__ == "__main__":
    main()
