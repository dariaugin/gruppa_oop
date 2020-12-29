from abc import ABC, abstractmethod
import random, copy
import asyncio

class BodyCell:
    def __init__(self, owner, life, coord, symbol, direct = "back"):
        self.owner = owner
        self.symbol = symbol
        self.life = life
        self.x = coord[1]
        self.y = coord[0]
        self.localDirect = direct
        self.simulation = owner.simulation
        self.simulation.animalMatrix[self.y][self.x] = symbol                
        self.simulation.cellDict[(self.y, self.x)] = self 
    
    def update(self, dxy, nextDirect):
        self.localDirect = nextDirect
        self.simulation.animalMatrix[self.y][self.x] = None                  
        self.simulation.cellDict.pop((self.y, self.x)) 
        self.y = self.owner.limiter(self.y + dxy[0], "height")
        self.x = self.owner.limiter(self.x + dxy[1], "width")
        self.simulation.animalMatrix[self.y][self.x] = self.symbol           
        self.simulation.cellDict[(self.y, self.x)] = self 
        
    def clear(self):
        self.simulation.animalMatrix[self.y][self.x] = None
        if self.simulation.environment.groundMatrix[self.y][self.x] == ",":
            self.simulation.environment.groundMatrix[self.y][self.x] = 0
        elif self.simulation.environment.groundMatrix[self.y][self.x] == "~":
            self.simulation.cellDict.pop((self.y, self.x)) 
            return None
        self.simulation.environment.groundMatrix[self.y][self.x] += int(self.life / 4)  
        self.simulation.cellDict.pop((self.y, self.x)) 
       
class Animal(ABC):
    bodyIncreaseProbabilityGrowSpeed = 2
    reproduceProbabilitySpeedGrow = 4
    directs = ["forward","back","left","right"]
    
    coordChangeDict = {"forward":(-1, 0),"back":(1, 0),"left":(0, -1),"right":(0, 1),"stop":(0, 0)}
    def __init__(self, simulation, parent=None):
        if parent == None:
            self.cellLife = random.randint(*self.__class__.intervalCellLife)
            self.fullness = random.randint(*self.__class__.intervalFullness)
            self.damage = random.randint(*self.__class__.intervalDamage)     
            
        else:
            r = [random.randint(-2, 2) for _ in range(3)] 
            if self.__class__.intervalCellLife[0] <= parent.cellLife + r[0] <= self.__class__.intervalCellLife[1]:
                self.cellLife = parent.cellLife + r[0]
            else:
                self.cellLife = parent.cellLife
                
            if self.__class__.intervalFullness[0] <= parent.fullness + r[1] <= self.__class__.intervalFullness[1]:
                self.fullness = parent.fullness + r[1]
            else:
                self.fullness = parent.fullness            

            if self.__class__.intervalDamage[0] <= parent.damage + r[2] <= self.__class__.intervalDamage[1]:
                self.damage = parent.damage + r[2]
            else:
                self.damage = parent.damage        
            
        self.simulation = simulation
        self.cellList = []
        self.minCellLife = None
        self.currFullness = self.fullness
        self.reproduceProbability = 0
    
    def constructBody(self, coords):
        for i in range(self.__class__.startLeng):
            self.cellList.append(BodyCell(self, self.cellLife,(coords[1]-i,coords[0]), self.symbol))
    
    async def move(self, direct):
        if direct == "stop":
            return None
        
        delta = Animal.coordChangeDict[direct]
        y = self.limiter(self.cellList[0].y + delta[0], "height")
        x = self.limiter(self.cellList[0].x + delta[1], "width")
        if str(self.simulation.environment.groundMatrix[y][x]) in self.waylessGround:
            self.cellList[0].localDirect = direct
            return None
        elif self.simulation.animalMatrix[y][x] != None:
            self.cellList[0].localDirect = direct
            return None        
        
        self.cellList[0].update(Animal.coordChangeDict[direct], direct)
    
    async def reproduce(self):
        if self.reproduceProbability < 100:
            self.reproduceProbability += Animal.reproduceProbabilitySpeedGrow
            
        else:
            self.reproduceProbability = 100
            
        chance = random.randint(0, 100)
        if chance < self.reproduceProbability:        
            x = self.cellList[-1].x
            y = self.cellList[-1].y
            baby = self.__class__(self.simulation, self)
            direct = self.cellList[-1].localDirect
            for i in range(self.__class__.startLeng):
                deltaCellCoords = Animal.coordChangeDict[direct]
                i = self.limiter(y + deltaCellCoords[0], "height")
                j = self.limiter(x + deltaCellCoords[1], "width")      
                if self.simulation.animalMatrix[i][j] == None and str(self.simulation.environment.groundMatrix[i][j]) not in self.waylessGround:
                    baby.cellList.append(BodyCell(self, self.cellLife,(i,j), self.symbol, direct))
                    y, x = i, j
                    self.simulation.speciesAmount[self.__class__.side][self.__class__.ID] += 1
                    self.simulation.totalNum += 1
                else:
                    del baby
                    return None
            
            self.reproduceProbability = 0                    
            self.currFullness -= int(baby.cellLife * self.__class__.startLeng * 0.5)
            if self.currFullness < 0:
                for i in range(len(self.cellList)):
                    self.cellList[i].life += self.currFullness
                self.currFullness = 5
                
            self.simulation.animalList.append(baby) 
            
    async def hunger(self):
        if self.currFullness != 0:
            self.currFullness -= 1
        else:
            for cell in self.cellList:
                cell.life -= 1        
            
    def death(self, animID):
        for cell in self.cellList:
            cell.clear()
        self.simulation.animalList.pop(animID)
        self.simulation.speciesAmount[self.__class__.side][self.__class__.ID] -= 1
        self.simulation.totalNum -= 1
    
    def limiter(self, num, axis):
        if num < 0:
            num = getattr(self.simulation.environment, axis) - 1 
        elif num >= getattr(self.simulation.environment, axis):
            num = 0         
        return num
        
class Hunter(Animal):
    def __init__(self, simulation, parent=None):
        super().__init__(simulation, parent)
        self.bodyIncreaseProbability = 0
        
    async def activityProcess(self, animID):
        self.minCellLife = min([cell.life for cell in self.cellList])
        if self.minCellLife == 0: 
            self.death(animID)
            return None
        
        direct = self.decisionMaking()
        await self.move(direct)
        dxy = Animal.coordChangeDict[self.cellList[0].localDirect]
        if self.simulation.animalMatrix[self.limiter(self.cellList[0].y + dxy[0], "height")][self.limiter(self.cellList[0].x + dxy[1], "width")] != None and self.currFullness < self.fullness:      #0.1*fullness   
            await self.eat()
        #
        elif type(self.simulation.environment.groundMatrix[self.limiter(self.cellList[0].y + dxy[0], "height")][self.limiter(self.cellList[0].x + dxy[1], "width")]) == int and self.currFullness < (self.fullness // 2.5):   
            await self.eat()
        #
        await self.hunger()
        
    def decisionMaking(self):
        chance = random.randint(0,100)
        if chance > 70:
            return random.choice(Animal.directs)
        
        directs = copy.copy(Animal.directs)
        random.shuffle(directs)
        for d in directs:
            dxy = Animal.coordChangeDict[d]
            y = self.limiter(self.cellList[0].y + dxy[0], "height")
            x = self.limiter(self.cellList[0].x + dxy[1], "width")
            anm = self.simulation.animalMatrix[y][x]
            gnd = self.simulation.environment.groundMatrix[y][x]
            if anm != None:
                if self.simulation.cellDict[(y, x)].owner.side:
                    return d
            
                elif self.minCellLife > (self.cellLife / 2):
                    return d
                
                continue
            
            elif gnd == "#":
                continue
            
            elif type(gnd) == int or gnd == ",":
                return d
            
            elif type(self).__name__ == "Weasel":
                return d
                
        return "stop"
    
    async def eat(self):
        dxy = Animal.coordChangeDict[self.cellList[0].localDirect]
        y = self.limiter(self.cellList[0].y + dxy[0], "height")
        x = self.limiter(self.cellList[0].x + dxy[1], "width")
        try:
            if self.simulation.cellDict[(y,x)].life > self.damage:
                self.simulation.cellDict[(y,x)].life -= self.damage
                increase = self.damage
            else:
                increase = self.simulation.cellDict[(y,x)].life
                self.simulation.cellDict[(y,x)].life = 0
        
        except:
            #
            if self.simulation.environment.groundMatrix[y][x] > self.damage:
                self.simulation.environment.groundMatrix[y][x] -= self.damage
                increase = self.damage
            else:
                increase = self.simulation.environment.groundMatrix[y][x]
                self.simulation.environment.groundMatrix[y][x] = ","
                self.simulation.environment.grassCellNum -= 1
            #
        self.currFullness += increase
        if self.currFullness > self.fullness:
            self.currFullness = self.fullness
        
        if self.currFullness > (self.fullness // 2):
            #self.currFullness = self.fullness
            if self.minCellLife < self.cellLife:
                await self.treat()
            else:
                await self.reproduce()
                
            if len(self.cellList) >= self.__class__.maxLeng:
                return None
            
            if self.bodyIncreaseProbability < 100:
                self.bodyIncreaseProbability += Animal.bodyIncreaseProbabilityGrowSpeed
            else:
                self.bodyIncreaseProbability = 100
                
            chance = random.randint(0, 100)
            return None
            if chance < self.bodyIncreaseProbability:
                await self.grow()
             
    async def treat(self):
        bodyLen = len(self.cellList)
        for i in range(bodyLen):
            self.cellList[i].life += 1
        self.currFullness -= bodyLen        
                        
    async def grow(self):
        x = self.cellList[-1].x
        y = self.cellList[-1].y
        deltaCellCoords = Animal.coordChangeDict[self.cellList[-1].localDirect]
        i = self.limiter(y + deltaCellCoords[0], "height")
        j = self.limiter(x + deltaCellCoords[1], "width")
        if self.simulation.animalMatrix[i][j] == None and str(self.simulation.environment.groundMatrix[i][j]) not in self.waylessGround:
            self.bodyIncreaseProbability = 0
            self.cellList.append(BodyCell(self, self.cellLife,(i,j), self.symbol, self.cellList[-1].localDirect))         
    
class Hedgehog(Hunter):
    side = 0
    ID = 0
    startLeng = 1
    maxLeng = 2
    intervalCellLife = (20,60)
    intervalFullness = (40,120)
    intervalDamage = (8,16)
    def __init__(self, simulation, parent=None):
        super().__init__(simulation, parent)
        self.waylessGround = ("#", "~")
        self.currFullness = self.fullness
        self.symbol = "H"

class Snake(Hunter):
    side = 0
    ID = 1
    startLeng = 1#2
    maxLeng = 10
    intervalCellLife = (30,110)
    intervalFullness = (40,160)
    intervalDamage = (8,24)
    def __init__(self, simulation, parent=None):
        super().__init__(simulation, parent)
        self.waylessGround = ("#", "~")
        self.currFullness = self.fullness
        self.symbol = "S"     
    
class Weasel(Hunter):
    side = 0
    ID = 2
    startLeng = 1#2
    maxLeng = 3
    intervalCellLife = (25,70)
    intervalFullness = (40,140)
    intervalDamage = (8,20)
    def __init__(self, simulation, parent=None):
        super().__init__(simulation, parent)
        self.waylessGround = ("#")
        self.currFullness = self.fullness
        self.symbol = "W"   

class Prey(Animal):
    def __init__(self, simulation, parent=None):
        super().__init__(simulation, parent)
        
    async def activityProcess(self, animID):
        self.minCellLife = min([cell.life for cell in self.cellList])
        if self.minCellLife == 0: 
            self.death(animID)
            return None  
        
        direct = self.decisionMaking()
        await self.move(direct)
        dxy = Animal.coordChangeDict[self.cellList[0].localDirect]
        if type(self.simulation.environment.groundMatrix[self.limiter(self.cellList[0].y + dxy[0], "height")][self.limiter(self.cellList[0].x + dxy[1], "width")]) == int and self.currFullness < self.fullness:   
            await self.eat()
        await self.hunger()
    
    def decisionMaking(self):
        chance = random.randint(0,100)
        if chance > 70:
            return random.choice(Animal.directs)        
        
        variants = {}
        buffer = []
        for d in Animal.directs:
            dxy = Animal.coordChangeDict[d]
            y = self.limiter(self.cellList[0].y + dxy[0], "height")
            x = self.limiter(self.cellList[0].x + dxy[1], "width")
            anm = self.simulation.animalMatrix[y][x]
            gnd = self.simulation.environment.groundMatrix[y][x]
            if gnd == ",":
                gnd = 0
                
            if anm != None or gnd == "#":
                continue
            
            elif type(gnd) == int:
                variants[gnd] = d 
                buffer.append(d)

            elif gnd == "~" and type(self).__name__ == "Frog":
                variants[0] = d 
                buffer.append(d)
            
        if len(variants) != 0:
            v = variants.keys()
            if len(v) == len(buffer):
                return variants[max(v)]
            
            else:
                return random.choice(buffer)

        return "stop"   
    
    async def eat(self):
        dxy = Animal.coordChangeDict[self.cellList[0].localDirect]
        y = self.limiter(self.cellList[0].y + dxy[0], "height")
        x = self.limiter(self.cellList[0].x + dxy[1], "width")
        if self.simulation.environment.groundMatrix[y][x] > self.damage:
            self.simulation.environment.groundMatrix[y][x] -= self.damage
            increase = self.damage
        else:
            increase = self.simulation.environment.groundMatrix[y][x]
            self.simulation.environment.groundMatrix[y][x] = ","
            self.simulation.environment.grassCellNum -= 1
            
        self.currFullness += increase
        if self.currFullness > self.fullness:
            self.currFullness = self.fullness  
            if self.minCellLife < self.cellLife:
                await self.treat()
            else:
                await self.reproduce()
             
    async def treat(self):
        bodyLen = len(self.cellList)
        for i in range(bodyLen):
            self.cellList[i].life += 1
        self.currFullness -= bodyLen            

class Mouse(Prey):
    side = 1
    ID = 0
    startLeng = 1
    intervalCellLife = (30,60)
    intervalFullness = (20,60)
    intervalDamage = (4,8)
    def __init__(self, simulation, parent=None):
        super().__init__(simulation, parent)
        self.waylessGround = ("#", "~")
        self.currFullness = self.fullness
        self.symbol = "m"
    
class Frog(Prey):
    side = 1
    ID = 1
    startLeng = 1
    stages = []
    state = []     
    intervalCellLife = (30,60)
    intervalFullness = (20,60)
    intervalDamage = (4,8)
    def __init__(self, simulation, parent=None):
        super().__init__(simulation, parent)
        self.waylessGround = ("#")
        self.currFullness = self.fullness
        self.symbol = "f"
    
class FlightlessBird(Prey):
    side = 1
    ID = 2
    startLeng = 1
    stages = []
    state = []    
    intervalCellLife = (35,90)
    intervalFullness = (20,70)
    intervalDamage = (4,9)
    def __init__(self, simulation, parent=None):
        super().__init__(simulation, parent)
        self.waylessGround = ("#", "~")
        self.currFullness = self.fullness
        self.symbol = "b"
    
class AnimalPlacer:
    hunterSpecies = [Hedgehog,Snake,Weasel]
    praySpecies = [Mouse,Frog,FlightlessBird] 
    animalStartLen = list(map(lambda x: x.startLeng, hunterSpecies))
    animalStartLen.extend(list(map(lambda x: x.startLeng, praySpecies)))
    maxStartLen = max(animalStartLen)   
    animalAccomodation = []
    
    @staticmethod
    def initBiota(simulation):#occupyPercent, environment, sidesRatio=[20,80], hunterRatio=[33,33,34], preyRatio=[33,33,34]):
        if sum(simulation.sidesRatio) != 100 or len(simulation.sidesRatio) != 2 or 0 > simulation.occupyPercent > 100:
            raise Exception 
        
        simulation.totalNum = 0
        last = 0
        curr = AnimalPlacer.maxStartLen
        if simulation.environment.height % AnimalPlacer.maxStartLen != 0:
            openPlaceHeight = simulation.environment.height - (simulation.environment.height % AnimalPlacer.maxStartLen)
        else:
            openPlaceHeight = simulation.environment.height
        while curr <= openPlaceHeight:
            linePlaces = simulation.environment.width
            AnimalPlacer.animalAccomodation.append([])
            for i in range(simulation.environment.width):
                needAdd = 1
                for j in range(last, curr):
                    if simulation.environment.groundMatrix[j][i] == "#" or simulation.environment.groundMatrix[j][i] == "~":
                        linePlaces -= 1
                        needAdd = 0 
                        break        
                if needAdd:
                    AnimalPlacer.animalAccomodation[-1].append((i,j))
            simulation.totalNum += linePlaces
            last = curr
            curr += AnimalPlacer.maxStartLen
            
        simulation.totalNum = int(simulation.totalNum * 0.01 * simulation.occupyPercent)    
        simulation.speciesAmount = []  # [0] - hunters, [1] - prey
        animalList, amount = AnimalPlacer.initOneSide(simulation, "Hunter", simulation.hunterRatio, int(simulation.totalNum * 0.01 * simulation.sidesRatio[0]))
        simulation.speciesAmount.append(amount)
        tmpList, amount = AnimalPlacer.initOneSide(simulation, "Prey", simulation.preyRatio, int(simulation.totalNum * 0.01 * simulation.sidesRatio[1]))
        simulation.speciesAmount.append(amount)
        animalList.extend(tmpList) 
        simulation.animalList = animalList
        random.shuffle(simulation.animalList)
    
    @staticmethod    
    def initOneSide(simulation, side, animalRatio, sideTotalNum):
        if sum(animalRatio) != 100:
            raise Exception
        aList = []
        amount = [0,0,0]
        if side == "Hunter":
            Species = AnimalPlacer.hunterSpecies
        else:
            Species = AnimalPlacer.praySpecies       
        i = 0
        speciesNum = len(amount)
        while i < speciesNum - 1:
            amount[i] = int(animalRatio[i] * 0.01 * sideTotalNum)
            i += 1
            
        amount[-1] = sideTotalNum - sum(amount)
        i = 0
        for animalNum in amount:
            j = 0
            while j < animalNum:
                creature = Species[i]
                aList.append(creature(simulation))
                j += 1
            i += 1
        random.shuffle(aList)
        return aList, amount
    
    @staticmethod
    def initAnimalMatrix(simulation):
        height, width = simulation.environment.height, simulation.environment.width
        simulation.animalMatrix = [[None for _ in range(width)] for _ in range(height)]        
    
    @staticmethod
    def placeAllAnimals(simulation):
        occupyRatio = simulation.occupyPercent / 100
        totalNum = len(simulation.animalList)
        lineNum = len(AnimalPlacer.animalAccomodation)
        k = 0
        currAnimalNum = 0
        while k < lineNum:
            freeLinePlace = len(AnimalPlacer.animalAccomodation[k])
            necessaryPlaceNum = int(occupyRatio * freeLinePlace)
            t = 0
            while t < necessaryPlaceNum: 
                if currAnimalNum == totalNum:
                    break
                randId = random.randint(0,freeLinePlace-1)
                coords = AnimalPlacer.animalAccomodation[k].pop(randId)
                animal = simulation.animalList[currAnimalNum]
                animal.constructBody(coords)
                freeLinePlace -= 1
                currAnimalNum += 1
                t += 1
            k += 1
        
        diff = totalNum - currAnimalNum
        if diff != 0:
            animalNum = len(simulation.animalList)
            i = 1
            while len(simulation.animalList[-i].cellList) == 0:
                randY = random.randint(0, lineNum-1)
                while len(AnimalPlacer.animalAccomodation[randY]) == 0:
                    randY = random.randint(0, lineNum-1)
                freeLinePlace = len(AnimalPlacer.animalAccomodation[randY])
                randX = random.randint(0, freeLinePlace-1)
                coords = AnimalPlacer.animalAccomodation[randY].pop(randX)
                simulation.animalList[-i].constructBody(coords)
                i += 1
                if i > animalNum:
                    break
                
        AnimalPlacer.animalAccomodation = []