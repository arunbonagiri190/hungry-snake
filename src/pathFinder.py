import gui_components

class PathFinder:
    def __init__(self, window):
        self.window = window
        self.snake_movement_size = gui_components.SNAKE_MOVEMENT_SIZE
        self.height = gui_components.HEIGHT
        self.width = gui_components.WIDTH
    
    def find(self):

        # get apple location(head)
        loc_food = self.window.food.getXandY()

        # get snake lacation(head)
        loc_snake = self.window.snake.body[0]
        #print('food: ',loc_food,'\n','snake: ',loc_snake)
        
        route = self.getRoute(loc_food, loc_snake)

        if self.verifyRoute(route):
            return []
        else:
            return route
    
    def verifyRoute(self, route):
        points = self.directionsToPoints(route)

        for direction in points:
            
            if direction in self.window.snake.body:
                return True
            
            if (direction[0]+self.snake_movement_size)<=0 or direction[0]>= self.width or (direction[1]+self.snake_movement_size)<=0 or direction[1]>= self.height:
                return True
        
        return False
    
    def directionsToPoints(self, route):
        points = []

        # get snake location head
        # loop thourgh route
        # convert each direction in point based on the snake location

        loc_snake = self.window.snake.body[0]

        for direction in route:
            if direction == 'w':
                x, y = loc_snake[0], loc_snake[1]-self.snake_movement_size

            elif direction == 'a':
                x, y = loc_snake[0]-self.snake_movement_size, loc_snake[1]

            elif direction == 'd':
                x, y = loc_snake[0]+self.snake_movement_size, loc_snake[1]

            elif direction == 's':
                x, y = loc_snake[0], loc_snake[1]+self.snake_movement_size
            
            loc_snake = [x, y]
            points.append(loc_snake)
            
        return points
    
    def getRoute(self, loc_food, loc_snake):
        route = []
        middle_point = [loc_food[0], loc_snake[1]]

        if self.window.snake.last_direction in ['a', 'd']:
            route = self.moveYDirection(loc_food, loc_snake, middle_point, route)
            route = self.moveXDirection(loc_food, loc_snake, middle_point, route)

        elif self.window.snake.last_direction in ['w', 's']:
            route = self.moveXDirection(loc_food, loc_snake, middle_point, route)
            route = self.moveYDirection(loc_food, loc_snake, middle_point, route)
        
        return route
        
    def moveXDirection(self, loc_food, loc_snake, middle_point, route):
        # food left side of snake
        if loc_food[0]<loc_snake[0]:
            for _ in range(abs(middle_point[0]-loc_snake[0])//20):
                    route.append('a')
        
        # food ride side of snake
        elif loc_food[0]>loc_snake[0]:
            for _ in range(abs(middle_point[0]-loc_snake[0])//20):
                route.append('d')
        
        return route

    def moveYDirection(self, loc_food, loc_snake, middle_point, route):
        # food is the up side of snake
        if loc_food[1]<loc_snake[1]:
            for _ in range(abs(middle_point[1]-loc_food[1])//20):
                route.append('w')
        
        # food is the down side of snake
        elif loc_food[1]>loc_snake[1]:
            for _ in range(abs(middle_point[1]-loc_food[1])//20):
                route.append('s')
        
        return route
