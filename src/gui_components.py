from tkinter import *
import random

WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
COLOR = 'black'

SNAKE_MOVEMENT_SIZE = GRID_SIZE
SNAKE_COLOR = 'white'
FOOD_COLOR = 'red'

########## GUI interface ##########
class Window:

    def __init__(self, controller):    
        self.window = Tk()
        self.window.title("Hungry Snake")
        self.window.resizable(False, False)

        self.canvas = Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.configure(background=COLOR)
        
        self.snake = Snake(self.canvas)
        self.snake.makeNewSnake()

        self.food = Food(self.canvas)
        self.food.makeRectangle(self.snake.body)
    
        self.controller = controller
        self.controller.set_window(self)

        self.window.bind('<KeyPress>', self.controller.on_key_press)
        self.canvas.pack()
        self.window.mainloop()
    
    def update(self, direction):
        
        self.snake.move(direction)
        
        #print('food: ',self.food.getXandY(), '\nsnake: ', self.snake.body)
        #print('overlap: ', self.canvas.find_overlapping(self.food.x-FOOD_SIZE, self.food.y-FOOD_SIZE, self.food.x+FOOD_SIZE, self.food.y+FOOD_SIZE))

        if self.snake.body_reff[0] in [o for o in self.canvas.find_overlapping(self.food.x, self.food.y, self.food.x+GRID_SIZE, self.food.y+GRID_SIZE)]:
            #print('collision')
            self.food.dismiss()
            self.food.makeRectangle(self.snake.body)
            self.snake.grow()
        
            

########## Snake ##########
class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.last_direction = 'd'
        self.tailDirection = 'd'
        self.oppositeDirection = {'a':'d', 'd':'a', 'w':'s', 's':'w'}
    
    def makeRectangle(self, x, y):
        return Canvas.create_rectangle(self.canvas, x, y, x+GRID_SIZE, y+GRID_SIZE, fill=SNAKE_COLOR, width=0)

    def makeNewSnake(self):
        self.x = random.randint(0, (WIDTH//GRID_SIZE)-1) * GRID_SIZE
        self.y = random.randint(0, (HEIGHT//GRID_SIZE)-1) * GRID_SIZE
        self.body = []
        self.body_reff = []

        for i in range(3):
            self.body_reff.append(self.makeRectangle(self.x-(i*GRID_SIZE), self.y))
            self.body.append([self.x-(i*GRID_SIZE), self.y])

    def getTailDirection(self):
        z = self.body[-1]
        y = self.body[-2]
        # up
        if z[1]-GRID_SIZE == y[1]:
            return 'w'
        # down
        elif z[1]+GRID_SIZE == y[1]:
            return 's'
        # left
        elif z[0]-GRID_SIZE == y[0]:
            return 'a'
        # right
        elif z[0]+GRID_SIZE == y[0]:
            return 'd'

    def grow(self):

        td = self.getTailDirection()
        
        if td == 'a':
            m = self.body[-1][0]-GRID_SIZE
            n = self.body[-1][1]
        elif td == 'd':
            m = self.body[-1][0]+GRID_SIZE
            n = self.body[-1][1]
        elif td == 'w':
            m = self.body[-1][0]
            n = self.body[-1][1]-GRID_SIZE
        else:#elif td == 's':
            m = self.body[-1][0]
            n = self.body[-1][1]+GRID_SIZE

        self.body_reff.append(self.makeRectangle(m, n))
        self.body.append([m, n])

    def deleteWholeSnake(self):
        for i in self.body_reff:
            self.canvas.delete(i)
        
        self.body_reff.pop()
        self.body.pop()

    def deleteTail(self):
        self.canvas.delete(self.body_reff[-1])
        self.body_reff.pop()
        self.body.pop()
    
    def move(self, direction):
        x, y = -1, -1

        if direction == 'w':
            x, y = self.body[0][0], self.body[0][1]-SNAKE_MOVEMENT_SIZE

        elif direction == 'a':
            x, y = self.body[0][0]-SNAKE_MOVEMENT_SIZE, self.body[0][1]

        elif direction == 'd':
            x, y = self.body[0][0]+SNAKE_MOVEMENT_SIZE, self.body[0][1]

        elif direction == 's':
            x, y = self.body[0][0], self.body[0][1]+SNAKE_MOVEMENT_SIZE
        
        if (x+GRID_SIZE)<=0 or x>= WIDTH or (y+GRID_SIZE)<=0 or y>= HEIGHT:
            pass
        elif [x, y] in self.body:
            if self.oppositeDirection[direction] != direction:
                self.deleteWholeSnake()
                self.makeNewSnake()
                self.last_direction = 'd'
                self.tailDirection = 'd'
                
        else:
            if x > -1 or y > -1:
                self.body_reff.insert(0, self.makeRectangle(x, y))
                self.body.insert(0, [x, y])
                self.deleteTail()
                self.last_direction = direction
        

########## Food ##########
class Food:
    def __init__(self, canvas):
        self.x, self.y = 0, 0
        self.canvas = canvas

    def getXandY(self):
        return [self.x, self.y]

    def makeRectangle(self, snake_body_loc):
        self.x = random.randint(0, (WIDTH//GRID_SIZE)-1) * GRID_SIZE
        self.y = random.randint(0, (HEIGHT//GRID_SIZE)-1) * GRID_SIZE

        if [self.x, self.y] in snake_body_loc:
            self.makeRectangle(snake_body_loc)
        else:
            self.ref = Canvas.create_rectangle(self.canvas, self.x, self.y, self.x+GRID_SIZE, self.y+GRID_SIZE, fill=FOOD_COLOR, width=0)
    
    def dismiss(self):
        self.canvas.delete(self.ref)
