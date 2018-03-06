
# coding: utf-8

# In[ ]:


import random

class World:
    
    
    def __init__(self, length=10, width=10, abundance = 5):
        self.length = length
        self.width = width
        self.abundance = abundance
        self.turn = 0
        self.creatures = []
        self.food = []
        self.map = [[" " for i in range(length)] for j in range(width)]
        
    
    def set_food(self, Food):
        self.map[Food.location[0]][Food.location[1]] = "X" 
        self.food.append(Food)
    
    
    def food_eaten(self, creature_location):
        for i in self.food:
            if creature_location == i.location:
                food_value = i.value
                self.food.remove(i)
                self.update()
                return food_value
        self.update()
    
    def generate_food(self):
        print("yee")
        food_x = random.randint(0, self.width-1)
        food_y = random.randint(0, self.length-1)
        while(self.map[food_x][food_y] != " "):
            food_x = random.randint(0, self.length-1)
            food_y = random.randint(0, self.width-1)
        food = Food(food_x, food_y)
        self.set_food(food)
        
    
    def get_map_piece(self, length, width, center):
        map_piece = [[" " for i in range(length)] for j in range(width)]
        for i in range(length):
            for j in range(width):
                if((center[0]-int(length/2))+i > self.length-1 or (center[1]-int(width/2))+j > self.width-1):
                    map_piece[i][j] = "|"
                elif((center[0]-int(length/2))+i < 0 or (center[1]-int(width/2))+j < 0):
                    map_piece[i][j] = "|"
                else:
                     map_piece[i][j] = self.map[(center[0]-int(length/2))+i][(center[1]-int(width/2))+j]
        return map_piece
        
    
    def print_map(self):
        #for i in range(self.length):
            #print("_", end=" ")
        for i in range(self.length):
            print("|", end=" ")
            for j in range(self.width):
                print(self.map[j][i], end=" ")
            print("|")
        #for i in range(self.length):
            #print("_", end=" ")
    
    
    def add_creature(self, creature):
        self.creatures.append(creature)
        self.update()
    
    
    
    def integrate(self, time):
        for i in range(time):
            for j in self.creatures:
                if j.food > 0:
                    j.live()                
            self.turn += 1
            print("Time:", i)
            self.update()
        
    
    def update(self):
        self.map = [[" " for i in range(self.length)] for j in range(self.width)]
        for j in self.food:
            self.map[j.location[0]][j.location[1]] = "X"
        for i in self.creatures:
            if self.map[i.location[0]][i.location[1]] == " ":
                self.map[i.location[0]][i.location[1]] = "O"
            else:
                self.map[i.location[0]][i.location[1]] = "*"
        if self.turn % (20/self.abundance) == 0:
            self.generate_food()
        self.print_map()
        print()

