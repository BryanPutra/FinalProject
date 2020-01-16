import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(0, 0, 255)): # dirnx is direction x
        self.position = start
        self.dirnx = 1 # start with the snake moving
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx          # direction x
        self.dirny = dirny          # direction y
        self.position = (self.position[0] + self.dirnx, self.position[1] + self.dirny) # this is to move the self.position[0] which is the x of the cube by adding the direction that is given by pressing the key

    def draw(self, surface, eyes=False):
        distance = self.w // self.rows  # which is 25
        i = self.position[0]            # row ( the x )
        j = self.position[1]            # column ( the y )
        pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2)) #distance -2 is the area, i * distance + 1 is x y
        if eyes:
            center = distance // 2 # the center of the cube
            radius = 3 # radius of the eye
            eye1 = (i * distance + center - radius, j * distance + 8) # i * distance is the position x + center - radius is the position of the circle inside the cube
            eye2 = (i * distance + distance - radius * 2, j * distance + 8) # same as top but the second eye
            pygame.draw.circle(surface, (0, 0, 0), eye1, radius) # draws the eye
            pygame.draw.circle(surface, (0, 0, 0), eye2, radius) # draws the second eye
    # def drawobstacle(self, surface):
    #     distance = self.w // self.rows
    #     distancerect = (self.w // self.rows) * 2  <------ NEVER MIND THIS CODE I FAILED
    #     k = self.position[0]
    #     l = self.position[1]
    #     pygame.draw.rect(surface, self.color, (k * distance + 1, l * distance + 1, distancerect // 2, distancerect * 1.5 - 2))


class Snake(object):
    body = []       #list of cubes that will be the body
    turns = {}      #this is where i store the positions of the head of the snake and why is below

    def __init__(self, color, position):
        self.color = color
        self.head = Cube(position)      #this is so we know the head's position at all times
        self.body.append(self.head)     #append the head to the first list of the body
        self.dirnx = 1                  #so when the game starts it immediately moves first before the given command not just stay still
        self.dirny = 0

    def move(self):
        for event in pygame.event.get():        # so we can close the game
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:     # if the left key is pressed then it moves left by moving the x -1 and y 0
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny] # to remember the way the head turns so that the tail can also turn after the main head has turned directions
                    # so the key is the current position of the head of the snake, and it is equal to what direction it is turning to
                    # so when we turn it creates and adds it to the turns list
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1          # if the right key is pressed then it moves left by adding the x 1 and y 0
                    self.dirny = 0
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny] # the same as the top

                elif keys[pygame.K_UP]:     # if the up key is pressed then it moves left by moving the x 0 and y -1
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:   # if the down key is pressed then it moves left by moving the x 0 and y -1
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):   #look through the list of positions that we have on the snake, i is the index and c is cube
            pos = c.position[:] # for each cube, grabs the position copy all the elements in the position index
            if pos in self.turns:# if the position is in the turns dictionary
                turn = self.turns[pos]# the turn that we chose the turn list at the index
                c.move(turn [0], turn[1])# give the cube the direction x and y after we pressed a direction button
                if i == len(self.body) - 1:# if we are in the last cube
                    self.turns.pop(pos)# if we dont remove the turn the turn will activate when we hit the position that was in our last tail
            else:
                if c.dirnx == -1 and c.position[0] <= 0: #if snake is moving left and the position x is less than or equal to 0
                    c.position = (c.rows - 1, c.position[1]) #change the position to the right side of the screen
                elif c.dirnx == 1 and c.position[0] >= c.rows - 1:
                    c.position = (0, c.position[1])
                elif c.dirny == 1 and c.position[1] >= c.rows - 1:
                    c.position = (c.position[0], 0)
                elif c.dirny == -1 and c.position[1] <= 0:
                    c.position = (c.position[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny) #if it is not on the edge of each x y it will continue moving just as it is told

    def reset(self, position): # to reset everything back to where and when it started
        self.head = Cube(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 1
        self.dirny = 0

    def addCube(self):
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny
        if dx == 1 and dy == 0:     # if the last cube is moving to the right
            self.body.append(Cube((tail.position[0] - 1, tail.position[1]))) # adds a cube 1 less than the current position of the last tail
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.position[0] + 1, tail.position[1]))) # basically same as above but in different positions
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.position[0], tail.position[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.position[0], tail.position[1] + 1)))
        self.body[-1].dirnx = dx    #for the tail to follow its head again
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body): # for every index, cube in the body list
            if i == 0: # if index 0 which is the first cube
                c.draw(surface, True)   # give eyes for the first cube which is the head
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBetween = w // rows  # how big each squares in the grid
    x = 0
    y = 0
    for i in range(rows):
        x = x + sizeBetween
        y = y+ sizeBetween
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w)) #draw column (x,0) biar gambar ga geser ke bawah and (x,w) draw till the end of the y
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y)) #draw rows (0,y) biar gambar ga keser ke kanan and (w,y) draw till the end of the x
def redrawWindow(surface): # this function is for drawing everything in this code
    global rows, width, s
    screen.fill((0, 0, 0))
    s.draw(surface)
    food.draw(surface)
    food2.draw(surface)
    food3.draw(surface)
    for i in obstacles:
        i.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomFood(rows, s):
    positions = s.body

    while True:
        x = random.randrange(rows) # randomize
        y = random.randrange(rows) # randomize
        if len(list(filter(lambda c: c.position == (x,y), positions))) > 0:
            # if the length of the list of the filtered list of positions(the snake body's), if the list of positions is the same as the randomly generated (x,y) then it continue the loop until it finds the position which doesnt touch the snake
            # the > 0 means that if there really is something in the len() it means that it is true and it returned a list
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True) # shows the text on the top
    root.withdraw()

    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def createObstacles(obsAmount):
    newObstacles = []
    for i in range(obsAmount):
        newObstacles.append(Cube(randomFood(rows, s), color=(255, 255, 255)))
    return newObstacles

def main():
    global screen, width, rows, s, food, obstacle, food2, food3, position, obstacles
    obstacleAmount = 10
    width = 500
    rows = 20       # squares that are used in the game in a single line so the total should be 20x20 = 400 squares (empty cubes)
    screen = pygame.display.set_mode((width, width)) # set the screen
    pygame.display.set_caption("Nub Snake") # write the title
    s = Snake((0, 0, 255), (10, 10)) # make the snake object
    food = Cube(randomFood(rows, s), color=(220, 20, 60)) # food object
    food2 = Cube(randomFood(rows, s), color=(255, 0, 0))
    food3 = Cube(randomFood(rows, s), color=(255, 0, 0))
    obstacles = createObstacles(obstacleAmount)
    clock = pygame.time.Clock() # this is for in the while loop
    while True:
        clock.tick(10)              # to get 10 fps rather than more i tried if more than that its too fast
        s.move()                    # call the move function for the snake to move
        if s.body[0].position == food.position:    # if the s.body[0].position which is the head of the snake is the same as the food position which means that when the head hits the food
            s.addCube()                            # call the addCube function for the snake which is for the snake to grow longer as it eats food
            food = Cube(randomFood(rows, s), color=(220, 20, 60))# to add in an another food after a food has been eaten in random cube
            food2 = Cube(randomFood(rows, s), color=(255, 0, 0))
            food3 = Cube(randomFood(rows, s), color=(255, 0, 0))
            obstacles = createObstacles(obstacleAmount) # to rerandom the obstacles's position

        if s.body[0].position == food2.position:  # if the head hits the food2 it will rerandom again but the obstacles wont be randomed only the food
            food = Cube(randomFood(rows, s), color=(220, 20, 60))
            food2 = Cube(randomFood(rows, s), color=(255, 0, 0))
            food3 = Cube(randomFood(rows, s), color=(255, 0, 0))

        if s.body[0].position == food3.position:  # same as food2
            food = Cube(randomFood(rows, s), color=(220, 20, 60))
            food2 = Cube(randomFood(rows, s), color=(255, 0, 0))
            food3 = Cube(randomFood(rows, s), color=(255, 0, 0))

        for i in obstacles: # for every things in the obstacles list
            if s.body[0].position == i.position: # if the head position is equal to the position of things in the obstacles list which are the obstacles
                print("Score: " + str(len(s.body))) # print the score, the score is the length of the snake's body
                message_box("You Lost!", "Try Again") # make a message box
                s.reset((10, 10)) # resets the snake in the position 10 10 which is in the middle
                food = Cube(randomFood(rows, s), color=(220, 20, 60))
                food2 = Cube(randomFood(rows, s), color=(255, 0, 0))
                food3 = Cube(randomFood(rows, s), color=(255, 0, 0))
                obstacles = createObstacles(obstacleAmount)
            redrawWindow(screen) # redraw the whole thing

        for x in range(len(s.body)): #loop through every cube in the snake body
            if s.body[x].position in list(map(lambda z:z.position, s.body[x + 1:])): #if the position is in a list of all the position
                print("Score: " + str(len(s.body)))
                message_box("You Lost!", "Try Again")
                s.reset((10, 10))
                food = Cube(randomFood(rows, s), color=(220, 20, 60))# to add in an another food after a food has been eaten in random cube
                food2 = Cube(randomFood(rows, s), color=(255, 0, 0))
                food3 = Cube(randomFood(rows, s), color=(255, 0, 0))
                obstacles = createObstacles(obstacleAmount) # rerandom obstacles
                break
        redrawWindow(screen) # redraw the whole thing

main()

