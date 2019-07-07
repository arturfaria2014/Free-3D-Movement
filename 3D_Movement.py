import pygame, sys, math


#this function is used for transforming points via the 2D rotation matrix, an equation
# of the form A = Matrix*B where B is the original point, Matrix is the 2D rotation matrix
# and A is the transformed point.
def planetf(position, angle):
    x,y = position
    return x*math.cos(angle)-y*math.sin(angle), y*math.cos(angle)+x*math.sin(angle)


#Camera class
class Cam:
    
    #super function for initializing main values of class
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    # function that applies a change on the azimuth and polar angles
    def events(self,event):
        
        if event.type == pygame.MOUSEMOTION:
            x,y = event.rel; x/=200; y/=200
            self.rot[0]+=y 
            self.rot[1]+=x
            #self.update_rot()
 
    #function which updates the position of the camera
    def update(self,dt,key):
        s = dt*10
 
        if key[pygame.K_LSHIFT]: self.pos[1]+=s
        if key[pygame.K_SPACE]: self.pos[1]-=s
 
        x,y = s*math.sin(self.rot[1]),s*math.cos(self.rot[1])
        
        
        if key[pygame.K_w]: 
            self.pos[0]+=x 
            self.pos[2]+=y
        
        if key[pygame.K_s]: 
            self.pos[0]-=x 
            self.pos[2]-=y
        
        if key[pygame.K_a]: 
            self.pos[0]-=y
            self.pos[2]+=x
        
        if key[pygame.K_d]: 
            self.pos[0]+=y 
            self.pos[2]-=x
        
        

cam = Cam((0, 0, -5))

pygame.init()

#screen dimensions
w = 400
h = 400

#center of screen
cx = w//2
cy = h//2

screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

#vertices and edges of the cube we are trying to render
verts = (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1), (1,-1,1), (1,1,1),(-1,1,1)
edges = (0,1),(1,2),(3,2),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)
 

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)

#game main loop logic
while True:

    dt = clock.tick()/1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        cam.events(event)
    
    screen.fill((255,255,255)) 
    
    facecolor = (255, 0, 0)
    
    #storing points and drawing them using the line function
    for edge in edges:
        points = []
        for x,y,z in (verts[edge[0]], verts[edge[1]]):
            
            x -= cam.pos[0]
            y -= cam.pos[1]
            z -= cam.pos[2]
            
            x,z=planetf((x,z), cam.rot[1])
            y,z=planetf((y,z), cam.rot[0])
            
            z+=5
            f=200/z
            x,y = x*f, y*f
            points += [(cx+int(x),cy+int(y))]
        pygame.draw.line(screen, (0,0,0), points[0], points[1], 1)
      
        

    pygame.display.flip()
    key = pygame.key.get_pressed()
    cam.update(dt, key)