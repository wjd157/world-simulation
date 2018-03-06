
# coding: utf-8

# In[ ]:


import random

class Creature:
    size = [1,1]
   
    
    # Initialize creature class
    def __init__(self, x=0, y=0, name="creature", health=100, food=100):
        self.location = [x, y]
        self.vision = []
        self.food = food
        self.name = name
        self.health = health
        self.food_spots = []
        self.vision_strength = 2
        self.state = ""
    
    def status(self):
        print(self.name)
        print("Health: ", self.health)
        print("Food: ", self.food)
        print("Location: ", self.location)
        print("Known Food Locations: ", self.food_spots)
        print("Current State: ", self.state)
        print("Line of Sight: ")
        for i in range(len(self.vision)):
            for j in range(len(self.vision[0])):
                print(self.vision[j][i], end=" ")
            print()
    
    
    def live(self):
        self.update_vision()
        self.food += -5
        if self.food > 0:
            self.find_food()
        else:
            self.state = "Dead"
        print()
    
    # find_food moves creature to food
    def find_food(self):
        if self.food_spots:
            self.go_to_food()
        else:
            self.state = "Searching"
            direction = random.randint(0,1)
            step = random.randint(0,1)
            move_possible = self.viable_move(step, direction)
            while(move_possible == False):
                direction = random.randint(0,1)
                step = random.randint(0,1)
                move_possible = self.viable_move(step, direction)
            if step == 0:
                self.move(-1,direction)
            else:
                self.move(1,direction)
            self.update_vision()
            
    
    # update_vision updates the sight line of the creature 
    def update_vision(self):
        self.vision = world.get_map_piece(self.vision_strength * 2 + 1, self.vision_strength*2 + 1, self.location)
        for i in range(self.vision_strength * 2 + 1):
            for j in range(self.vision_strength*2 + 1):
                if (self.vision[i][j] == "X" or self.vision[i][j] == "*") and ([i-self.walls_in_sight([i,j],'y'),j-self.walls_in_sight([i,j],'x')] not in self.food_spots):
                    #print("before: ", i,j, " ", self.vision[i][j])
                    #print([i-self.walls_in_sight([i,j],'y'),j-self.walls_in_sight([i,j],'x')])
                    self.food_spots.append([i-self.walls_in_sight([i,j],'y'),j-self.walls_in_sight([i,j],'x')])
                    
                
    # no_food_in_sight checks if there is food in the current sight line
    def no_food_in_sight(self):
        for i in range(len(self.vision)):
            for j in range(len(self.vision[0])):
                if self.vision[i][j] == "X" or self.vision[i][j] == "*":
                    return False
        return True
       
        
    def move(self, step, direction):
        if direction == 0:
            self.location[0] += step
        elif direction == 1:
            self.location[1] += step
    
    def viable_move(self, step, direction):
        if direction == 0:
            if self.location[0] + step >= world.width or self.location[0] + step <= 0:
                return False
        elif direction == 1:
            if self.location[1] + step >= world.length or self.location[1] + step <= 0:
                return False
        else:
            return True
        
    
    def walls_in_sight(self, cord, x_or_y):
        wall = 0
        if x_or_y == 'x':
            for i in range(self.vision_strength):
                if self.vision[cord[0]][i] == "|" and i + 1 != "|":
                    wall += 1
            if self.location[1] > self.vision_strength:
                wall += -(self.location[1] - self.vision_strength)
        else:
            for i in range(self.vision_strength):
                if self.vision[i][cord[1]] == "|" and i != 4:
                    wall += 1
            if self.location[0] > self.vision_strength:
                wall += -(self.location[0] - self.vision_strength)
        return wall
    
    def move_towards_food(self, move_time, fastest_time):
        if self.location != move_time[fastest_time]:
            not_done = True
            x_or_y = random.randint(0,1)
            if x_or_y == 0 and self.location[0] != move_time[fastest_time][0]:
                if self.location[0] < move_time[fastest_time][0]:
                    self.move(1, 0)
                elif self.location[0] > move_time[fastest_time][0]:
                    self.move(-1, 0)
                not_done = False
            elif self.location[1] != move_time[fastest_time][1]: 
                if self.location[1] < move_time[fastest_time][1]:
                    self.move(1, 1)
                elif self.location[1] > move_time[fastest_time][1]:
                    self.move(-1, 1)
                not_done = False
            if(not_done):
                if x_or_y == 1 and self.location[1] != move_time[fastest_time][1]:
                    if self.location[1] < move_time[fastest_time][1]:
                        self.move(1, 1)
                    elif self.location[1] > move_time[fastest_time][1]:
                        self.move(-1, 1)
                elif self.location[0] != move_time[fastest_time][0]:
                    if self.location[0] < move_time[fastest_time][0]:
                        self.move(1, 0)
                    elif self.location[0] > move_time[fastest_time][0]:
                        self.move(-1, 0)
        else:
            self.eat()
    
    # moves creature on top of the food     
    def go_to_food(self):
        move_time = {}
        for i in self.food_spots:
            time = abs(i[0] - self.location[0]) + abs(i[1]- self.location[1])
            move_time[time] = i
        fastest_time = min(move_time)
        self.state = "Going to " + str(move_time[fastest_time])
        self.move_towards_food(move_time, fastest_time)

    
    # creature eats food
    def eat(self):
        if self.vision[2][2] == "*":
            self.food += world.food_eaten(self.location)
            self.food_spots.remove(self.location)
        self.update_vision()
                    
    

