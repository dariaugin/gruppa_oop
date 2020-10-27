from abc import ABC, abstractmethod
import random
import Map

class bodyCell:
    def __init__(self, life, coord):
        self.life = life
        self.x = coord[0]
        self.y = coord[1]
       
class Animal(ABC):
    def __init__(self):
        self.cellList = []
        self.hunger = None    
    
    @abstractmethod
    def constructBody(self):
        pass
        
    @abstractmethod
    def move(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass
    
    @abstractmethod
    def reproduce(self):
        pass
    
    @abstractmethod
    def death(self):
        pass
        
class Hunter(Animal):
    def __init__(self):
        super().__init__()
    
class Hedgehog(Hunter):   
    startLeng = 1
    def __init__(self):
        super().__init__()
        
    def constructBody(self):
        pass
        
    def move(self):
        pass
    
    def eat(self):
        pass
    
    def reproduce(self):
        pass
    
    def death(self):
        pass    

class Snake(Hunter):
    startLeng = 2
    def __init__(self):
        super().__init__()
        
    def constructBody(self):
        pass
        
    def move(self):
        pass
    
    def eat(self):
        pass
    
    def reproduce(self):
        pass
    
    def death(self):
        pass      
    
class Weasel(Hunter):
    startLeng = 2
    def __init__(self):
        super().__init__()
        
    def constructBody(self):
        pass
        
    def move(self):
        pass
    
    def eat(self):
        pass
    
    def reproduce(self):
        pass
    
    def death(self):
        pass      

class Prey(Animal):
    def __init__(self):
        super().__init__()

class Mouse(Prey):
    startLeng = 1
    def __init__(self):
        super().__init__()  
    
    def constructBody(self):
        pass
        
    def move(self):
        pass
    
    def eat(self):
        pass
    
    def reproduce(self):
        pass
    
    def death(self):
        pass      
    
class Frog(Prey):
    startLeng = 1
    stages = []
    state = []     
    def __init__(self):
        super().__init__() 
    
    def constructBody(self):
        pass
        
    def move(self):
        pass
    
    def eat(self):
        pass
    
    def reproduce(self):
        pass
    
    def death(self):
        pass      
    
class FlightlessBird(Prey):
    startLeng = 1
    stages = []
    state = []    
    def __init__(self):
        super().__init__()
    
    def constructBody(self):
        pass
        
    def move(self):
        pass
    
    def eat(self):
        pass
    
    def reproduce(self):
        pass
    
    def death(self):
        pass      
        
class AnimalPlacer:
    hunterSpecies = [Hedgehog,Snake,Weasel]
    praySpecies = [Mouse,Frog,FlightlessBird] 
    animalStartLen = list(map(lambda x: x.startLeng, hunterSpecies))
    animalStartLen.extend(list(map(lambda x: x.startLeng, praySpecies)))
    maxStartLen = max(animalStartLen)   
    groundObjectsAccomodation = {}
    
    @staticmethod
    def initBiota(occupyPercent, environment, sidesRatio=[20,80], hunterRatio=[33,33,34], preyRatio=[33,33,34]):
        if sum(sidesRatio) != 100 or len(sidesRatio) != 2 or 0 < occupyPercent > 100:
            raise Exception 
        mapMatr = environment.groundMatrix
        totalNum = 0
        last = 0
        curr = AnimalPlacer.maxStartLen
        while curr < environment.height:
            linePlaces = environment.width
            for i in range(environment.width):
                for j in range(last, curr):
                    if mapMatr[i][j] == "#" or mapMatr[i][j] == "~":
                        AnimalPlacer.groundObjectsAccomodation[(i,last)] = 1
                        linePlaces -= 1
                        break
            totalNum += linePlaces
            last = curr
            curr += AnimalPlacer.maxStartLen
            
        totalNum = int(totalNum * 0.01 * occupyPercent)    
        speciesAmount = []  # [0] - hunters, [1] - prey
        animalList, amount = AnimalPlacer.initOneSide("Hunter", hunterRatio, int(totalNum * 0.01 * sidesRatio[0]))
        speciesAmount.append(amount)
        tmpList, amount = AnimalPlacer.initOneSide("Prey", preyRatio, int(totalNum * 0.01 * sidesRatio[1]))
        speciesAmount.append(amount)
        animalList.extend(tmpList)    
        return animalList, speciesAmount, totalNum
    
    @staticmethod    
    def initOneSide(side, animalRatio, totalNum):
        if sum(animalRatio) != 100:
            raise Exception
        animalList = []
        speciesAmount = [0,0,0]
        if side == "Hunter":
            Species = AnimalPlacer.hunterSpecies
        else:
            Species = AnimalPlacer.praySpecies       
        i = 0
        speciesNum = len(speciesAmount)
        while i < speciesNum - 1:
            speciesAmount[i] = int(animalRatio[i] * 0.01 * totalNum)
            i += 1
            
        speciesAmount[-1] = totalNum - sum(speciesAmount)
        i = 0
        for animalNum in speciesAmount:
            j = 0
            while j < animalNum:
                creature = Species[i]
                animalList.append(creature())
                j += 1
            i += 1
        random.shuffle(animalList)
        return animalList, speciesAmount
    
    @staticmethod
    def placeAllAnimals(environment, animalList, occupyPercent):
        density = int(100 / occupyPercent)
        height, width = environment.height, environment.width
        animalMatrix = [[None for _ in range(height)] for _ in range(width)]
        totalNum = len(animalList)
        delimiter = 1       
        last = 0
        curr = AnimalPlacer.maxStartLen
        while totalNum > 0: #curr < height
            delimiter = not delimiter
            start = delimiter * density
            for i in range(start - 1, width, density):
                try:
                    AnimalPlacer.groundObjectsAccomodation[(i,last)]
                except:
                    if animalMatrix[i][last] == None:
                        animalMatrix[i][last] = "#"
                        totalNum -= 1 
            last = curr
            curr += AnimalPlacer.maxStartLen
            if curr >= height:
                curr = curr % height
                density += 1
        return animalMatrix    

if __name__ == "__main__":
    occupyPercent = 100
    width = 50#220
    height = 25#50
    
    if 10 > width:
        print("Change width(it must be bigger than 10):", end = "")
        width = input()
        
    if 10 > height:
        print("Change height(it must be bigger than 10):", end = "")
        height = input()
        
    mapObj = Map.Map(width, height, [50,3,0])#[20,3,60])
    mapObj.showMap()
    animalList, speciesAmount, totalNum = AnimalPlacer.initBiota(occupyPercent, mapObj)
    animalMatrix = AnimalPlacer.placeAllAnimals(mapObj, animalList, occupyPercent)
    
    for i in range(mapObj.width):
        for j in range(mapObj.height):
            if animalMatrix[i][j] != None:
                print(animalMatrix[i][j],end="")
            else:
                print(" ",end="")
        print()       
      
