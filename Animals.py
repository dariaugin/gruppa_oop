from abc import ABC, abstractmethod
import os, keyboard, random, sys, copy, time
import Map
import asyncio

class bodyCell:
    def __init__(self, life, coord, symbol, direct = "back"):
        self.symbol = symbol
        self.life = life
        self.x = coord[1]
        self.y = coord[0]
        self.localDirect = direct
        animalMatrix[self.y][self.x] = symbol                
        cellDict[(self.y, self.x)] = self 
    
    def update(self, dxy, nextDirect):
        self.localDirect = nextDirect
        animalMatrix[self.y][self.x] = None                  
        cellDict.pop((self.y, self.x)) 
        self.y = Animal.limiter(self.y + dxy[0], "height")
        self.x = Animal.limiter(self.x + dxy[1], "width")
        animalMatrix[self.y][self.x] = self.symbol           
        cellDict[(self.y, self.x)] = self 
        
    def clear(self):
        animalMatrix[self.y][self.x] = None
        if mapObj.groundMatrix[self.y][self.x] == ",":
            mapObj.groundMatrix[self.y][self.x] = 0
        elif mapObj.groundMatrix[self.y][self.x] == "~":
            cellDict.pop((self.y, self.x)) 
            return None
        mapObj.groundMatrix[self.y][self.x] += int(self.life / 4)  
        cellDict.pop((self.y, self.x)) 
       
class Animal(ABC):
    bodyIncreaseProbabilityGrowSpeed = 2
    reproduceProbabilitySpeedGrow = 2
    directs = ["forward","back","left","right"]
    directCodes = {"forward":(0, 1),"back":(1, 1),"left":(0, 0),"right":(1, 0)}
    directUncodes = {(0, 1):"forward",(1, 1):"back",(0, 0):"left",(1, 0):"right"}
    coordChangeDict = {"forward":(-1, 0),"back":(1, 0),"left":(0, -1),"right":(0, 1),"stop":(0, 0)}
    def __init__(self):
        self.moveFuncDict = {"forward":self.forward,"back":self.back,"left":self.left,"right":self.right,"stop":(0,0)}
        #--characteristics--
        self.cellLife = random.randint(*self.__class__.intervalCellLife)
        self.fullness = random.randint(*self.__class__.intervalFullness)
        self.damage = random.randint(*self.__class__.intervalDamage)     
        #--body--
        self.cellList = []
        #--curr_values--
        self.minCellLife = None
        self.currFullness = self.fullness
        self.reproduceProbability = 0
    
    def constructBody(self, coords):
        global animalList
        for i in range(self.__class__.startLeng):
            self.cellList.append(bodyCell(self.cellLife,(coords[1]-i,coords[0]), self.symbol))
        
    async def move(self, direct):
        if direct == "stop":
            return None
        dxy = self.moveFuncDict[direct] 
        currDirect = self.cellList[0].localDirect
        #print()#
        #print(self.cellList[0].localDirect, self.cellList[0].y, self.cellList[0].x)#
        delta, headDirect = dxy()                                           
        if str(mapObj.groundMatrix[Animal.limiter(self.cellList[0].y + delta[0], "height")][Animal.limiter(self.cellList[0].x + delta[1], "width")]) in self.waylessGround:
            return None
        elif animalMatrix[Animal.limiter(self.cellList[0].y + delta[0], "height")][Animal.limiter(self.cellList[0].x + delta[1], "width")] != None:
            return None
    
        direct = self.cellList[0].localDirect = headDirect
        self.cellList[0].update(delta, direct)  
        #print(self.cellList[0].localDirect, self.cellList[0].y, self.cellList[0].x)#
        for i in range(1, len(self.cellList)):
            dxy = Animal.coordChangeDict[currDirect]
            tmp = self.cellList[i].localDirect
            #print("ooooooooooooo")#
            #print(tmp, self.cellList[i].y, self.cellList[i].x)#
            self.cellList[i].update(dxy, currDirect)
            #print(self.cellList[i].localDirect, self.cellList[i].y, self.cellList[i].x)#
            currDirect = tmp      
            #print('/////////')#
    
    async def reproduce(self):
        if self.reproduceProbability < 100:
            self.reproduceProbability += Animal.reproduceProbabilitySpeedGrow
        else:
            self.reproduceProbability = 100
            
        chance = random.randint(0, 100)
        if chance < self.reproduceProbability:        
            x = self.cellList[-1].x
            y = self.cellList[-1].y
            baby = self.__class__()
            direct = self.cellList[-1].localDirect
            for i in range(self.__class__.startLeng):
                deltaCellCoords = Animal.coordChangeDict[direct]
                i = Animal.limiter(y + deltaCellCoords[0], "height")
                j = Animal.limiter(x + deltaCellCoords[1], "width")      
                if animalMatrix[i][j] == None and str(mapObj.groundMatrix[i][j]) not in self.waylessGround:
                    baby.cellList.append(bodyCell(self.cellLife,(i,j), self.symbol, direct))
                    y, x = i, j
                else:
                    del baby
                    return None
            
            self.reproduceProbability = 0                    
            self.currFullness -= baby.cellLife * self.__class__.startLeng
            if self.currFullness < 0:
                for i in range(len(self.cellList)):
                    self.cellList[i].life += self.currFullness
                self.currFullness = 5
                
            animalList.append(baby) 
            
    async def hunger(self):
        if self.currFullness != 0:
            self.currFullness -= 1
        else:
            for cell in self.cellList:
                cell.life -= 1        
            
    def death(self, animID):
        for cell in self.cellList:
            cell.clear()
        animalList.pop(animID)
        
    def forward(self):
        return Animal.coordChangeDict[self.cellList[0].localDirect], self.cellList[0].localDirect
        
    def back(self):
        directID = Animal.directCodes[self.cellList[0].localDirect]
        directID1 = (not directID[0], directID[1])
        return Animal.coordChangeDict[Animal.directUncodes[directID1]], Animal.directUncodes[directID1]
        
    def left(self):
        directID = Animal.directCodes[self.cellList[0].localDirect]
        directID1 = (not (bool(directID[0]) ^ bool(directID[1])), not directID[1])
        return Animal.coordChangeDict[Animal.directUncodes[directID1]], Animal.directUncodes[directID1]
    
    def right(self):
        directID = Animal.directCodes[self.cellList[0].localDirect]
        directID1 = (bool(directID[0]) ^ bool(directID[1]), not directID[1])       
        return Animal.coordChangeDict[Animal.directUncodes[directID1]], Animal.directUncodes[directID1]
    
    @staticmethod
    def limiter(num, axis):
        if num < 0:
            num = getattr(mapObj, axis) - 1 
        elif num >= getattr(mapObj, axis):
            num = 0         
        return num
        
class Hunter(Animal):
    def __init__(self):
        super().__init__()
        self.bodyIncreaseProbability = 0
        
    async def decisionMaking(self, animID):
        direct = random.choice(Animal.directs)
        self.minCellLife = min([cell.life for cell in self.cellList])
        if self.minCellLife == 0: 
            self.death(animID)
            return None
        await self.move(direct)
        dxy = Animal.coordChangeDict[self.cellList[0].localDirect]
        if animalMatrix[Animal.limiter(self.cellList[0].y + dxy[0], "height")][Animal.limiter(self.cellList[0].x + dxy[1], "width")] != None and self.currFullness < self.fullness:      #0.1*fullness   
            await self.eat()
        await self.hunger()
    
    async def eat(self):
        dxy = Animal.coordChangeDict[self.cellList[0].localDirect]
        y = Animal.limiter(self.cellList[0].y + dxy[0], "height")
        x = Animal.limiter(self.cellList[0].x + dxy[1], "width")
        if cellDict[(y,x)].life > self.damage:
            cellDict[(y,x)].life -= self.damage
            increase = self.damage
        else:
            increase = cellDict[(y,x)].life
            cellDict[(y,x)].life = 0
            
        self.currFullness += increase
        if self.currFullness >= self.fullness:
            self.currFullness = self.fullness
            if self.minCellLife < self.cellLife:
                await self.treat()
            else:
                await self.reproduce()
                pass
                
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
        i = Animal.limiter(y + deltaCellCoords[0], "height")
        j = Animal.limiter(x + deltaCellCoords[1], "width")
        if animalMatrix[i][j] == None and str(mapObj.groundMatrix[i][j]) not in self.waylessGround:
            self.bodyIncreaseProbability = 0
            self.cellList.append(bodyCell(self.cellLife,(i,j), self.symbol, self.cellList[-1].localDirect))         
    
class Hedgehog(Hunter):   
    startLeng = 1
    maxLeng = 2
    intervalCellLife = (10,50)
    intervalFullness = (10,30)
    intervalDamage = (4,12)
    def __init__(self):
        super().__init__()
        self.waylessGround = ("#", "~")
        self.currFullness = self.fullness
        self.symbol = "H"

class Snake(Hunter):
    startLeng = 1#2
    maxLeng = 10
    intervalCellLife = (20,100)
    intervalFullness = (10,50)
    intervalDamage = (4,20)
    def __init__(self):
        super().__init__()
        self.waylessGround = ("#", "~")
        self.currFullness = self.fullness
        self.symbol = "S"     
    
class Weasel(Hunter):
    startLeng = 1#2
    maxLeng = 3
    intervalCellLife = (15,60)
    intervalFullness = (10,40)
    intervalDamage = (4,16)
    def __init__(self):
        super().__init__()
        self.waylessGround = ("#")
        self.currFullness = self.fullness
        self.symbol = "W"   

class Prey(Animal):
    def __init__(self):
        super().__init__()
        
    async def decisionMaking(self, animID):
        direct = random.choice(Animal.directs)
        self.minCellLife = min([cell.life for cell in self.cellList])
        if self.minCellLife == 0: 
            self.death(animID)
            return None        
        await self.move(direct)
        dxy = Animal.coordChangeDict[self.cellList[0].localDirect]
        if type(mapObj.groundMatrix[Animal.limiter(self.cellList[0].y + dxy[0], "height")][Animal.limiter(self.cellList[0].x + dxy[1], "width")]) == int and self.currFullness < self.fullness:   
            await self.eat()
        await self.hunger()
    
    async def eat(self):
        dxy = Animal.coordChangeDict[self.cellList[0].localDirect]
        y = Animal.limiter(self.cellList[0].y + dxy[0], "height")
        x = Animal.limiter(self.cellList[0].x + dxy[1], "width")
        if mapObj.groundMatrix[y][x] > self.damage:
            mapObj.groundMatrix[y][x] -= self.damage
            increase = self.damage
        else:
            increase = mapObj.groundMatrix[y][x]
            mapObj.groundMatrix[y][x] = ","
            mapObj.grassCellNum -= 1
            
        self.currFullness += increase
        if self.currFullness > self.fullness:
            self.currFullness = self.fullness  
            if self.minCellLife < self.cellLife:
                await self.treat()
            else:
                await self.reproduce()
                pass
             
    async def treat(self):
        bodyLen = len(self.cellList)
        for i in range(bodyLen):
            self.cellList[i].life += 1
        self.currFullness -= bodyLen            

class Mouse(Prey):
    startLeng = 1
    intervalCellLife = (10,40)
    intervalFullness = (5,30)
    intervalDamage = (2,6)
    def __init__(self):
        super().__init__()
        self.waylessGround = ("#", "~")
        self.currFullness = self.fullness
        self.symbol = "m"
    
class Frog(Prey):
    startLeng = 1
    stages = []
    state = []     
    intervalCellLife = (10,40)
    intervalFullness = (5,30)
    intervalDamage = (2,6)
    def __init__(self):
        super().__init__()
        self.waylessGround = ("#")
        self.currFullness = self.fullness
        self.symbol = "f"
    
class FlightlessBird(Prey):
    startLeng = 1
    stages = []
    state = []    
    intervalCellLife = (15,70)
    intervalFullness = (5,40)
    intervalDamage = (4,9)
    def __init__(self):
        super().__init__()
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
    def initBiota(occupyPercent, environment, sidesRatio=[20,80], hunterRatio=[33,33,34], preyRatio=[33,33,34]):
        if sum(sidesRatio) != 100 or len(sidesRatio) != 2 or 0 < occupyPercent > 100:
            raise Exception 
        mapMatr = environment.groundMatrix
        totalNum = 0
        last = 0
        curr = AnimalPlacer.maxStartLen
        if environment.height % AnimalPlacer.maxStartLen != 0:
            openPlaceHeight = environment.height - (environment.height % AnimalPlacer.maxStartLen)
        else:
            openPlaceHeight = environment.height
        while curr <= openPlaceHeight:
            linePlaces = environment.width
            AnimalPlacer.animalAccomodation.append([])
            for i in range(environment.width):
                needAdd = 1
                for j in range(last, curr):
                    if mapMatr[j][i] == "#" or mapMatr[j][i] == "~":
                        linePlaces -= 1
                        needAdd = 0 
                        break        
                if needAdd:
                    AnimalPlacer.animalAccomodation[-1].append((i,j))
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
        random.shuffle(animalList)
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
    
    def initAnimalMatrix(environment):
        height, width = environment.height, environment.width
        animalMatrix = [[None for _ in range(width)] for _ in range(height)]        
        return animalMatrix
    
    @staticmethod
    def placeAllAnimals(animalList, occupyPercent):
        occupyRatio = occupyPercent / 100
        totalNum = len(animalList)
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
                animal = animalList[currAnimalNum]
                animal.constructBody(coords)
                freeLinePlace -= 1
                currAnimalNum += 1
                t += 1
            k += 1
        
        diff = totalNum - currAnimalNum
        if diff != 0:
            animalNum = len(animalList)
            i = 1
            while len(animalList[-i].cellList) == 0:
                randY = random.randint(0, lineNum-1)
                while len(AnimalPlacer.animalAccomodation[randY]) == 0:
                    randY = random.randint(0, lineNum-1)
                freeLinePlace = len(AnimalPlacer.animalAccomodation[randY])
                randX = random.randint(0, freeLinePlace-1)
                coords = AnimalPlacer.animalAccomodation[randY].pop(randX)
                animalList[-i].constructBody(coords)
                i += 1
                if i > animalNum:
                    break
        
        return animalMatrix 
    
    @staticmethod
    def showAnimalData(animalList):
        i = 1
        for animal in animalList:
            print(i,". ",animal.symbol, end=": ")
            for cell in animal.cellList:
                print("(", cell.y, ",", cell.x, ")", end=" | ")
            print(animal.cellLife," | ",animal.cellList[0].localDirect)
            i += 1
    
    @staticmethod
    def showMap(mapMatrix, animalMatrix, height, width, needShow = [1, 1, 1]):
        if needShow[0]:
            print("mapMatrix:")
            for i in range(height):
                for j in range(width):
                    print(mapMatrix[i][j],end="")
                print()        
        if needShow[1]:
            print("animalMatrix:")
            for i in range(height):
                for j in range(width):
                    if animalMatrix[i][j] != None:
                        print(animalMatrix[i][j],end="")
                    else:
                        print(" ",end="")
                print()   
            
        resultMatrix = copy.deepcopy(mapMatrix)
        for i in range(height):
            for j in range(width):
                if animalMatrix[i][j] != None:
                    resultMatrix[i][j] = animalMatrix[i][j]        
            
        if needShow[2]:
            print("resultMatrix:")
            for i in range(height):
                for j in range(width):
                    print(resultMatrix[i][j],end="")
                print() 
                
    @staticmethod
    def simulationControl(mapMatrix, animalMatrix, animalList, height, width, needShow = [1, 1, 1]):
        AnimalPlacer.showMap(mapObj.groundMatrix, animalMatrix, height, width, needShow)
        AnimalPlacer.showAnimalData(animalList)
        cellCoords = cellDict.keys()
        print(len(cellCoords), cellCoords)        
    
    @staticmethod
    def composeResultMatrix(environment):
        resultMatrix = copy.deepcopy(environment.groundMatrix)
        for i in range(height):
            for j in range(width):
                if animalMatrix[i][j] != None:
                    resultMatrix[i][j] = animalMatrix[i][j]
        
        resultList = []
        for row in resultMatrix:
            resultList.extend(row)
           
        resultStr = ''.join([str(elem) for elem in resultList]) + ' '
        return resultStr   

def sendResolution(width, height):
    resolution = '{} {}'.format(width, height)
    flow = open("buffer.txt", 'w')
    flow.write(resolution)
    flow.close()
    
def sendData(data):
    flow = open("buffer.txt", 'w')
    flow.write(data)
    flow.close() 
    
def sendSignal(signal):
    flow = open("signal.txt", 'w')
    flow.write(signal)
    flow.close()     
    
def getData():
    flow = open("buffer.txt", 'r')
    data = flow.read()
    flow.close()        
    return data

def closeProgram():
    sendSignal("close")
    sys.exit()

async def passCycle(animalList):
    i = 0
    for animal in animalList:
        await animal.decisionMaking(i)
        i += 1    

if __name__ == "__main__":
    occupyPercent = 10
    resolution = input("Resolution(WxH): ") #235 130
    width, height = [int(elem) for elem in resolution.split(' ')]
    
    while True:
        if 10 > width or 10 > height:
            print("Change width or height(it must be bigger than 10): ", end = "")
            width, height = [int(elem) for elem in input().split(' ')]
            continue
        break
          
    mapObj = Map.Map(height, width, [20,3,60])
    print("Map obj created...")
    cellDict = {}
    animalList, speciesAmount, totalNum = AnimalPlacer.initBiota(occupyPercent, mapObj)
    animalMatrix = AnimalPlacer.initAnimalMatrix(mapObj)
    animalMatrix = AnimalPlacer.placeAllAnimals(animalList, occupyPercent)
    print("All animals placed...")
    
    sendResolution(width, height)
    sendSignal("open")
    os.startfile(r'C:\\Users\\UserFree\\Desktop\\2_course\\OOP\\Hunters_&_pray\\GraphicView\\x64\\Debug\\GraphicView.exe')
    
    #Simulation
    start = 0
    day = 0
    while True:   
        if keyboard.is_pressed('q'):
            closeProgram()
        if not getData(): 
            #start = time.time()
            #AnimalPlacer.simulationControl(mapObj.groundMatrix, animalMatrix, animalList, height, width, [0, 1, 0])
            #direct = input("Next direct:")
            
            asyncio.run(passCycle(animalList))
            
            if day % 20 == 0:
                mapObj.addGrass()
            day += 1
            resultStr = AnimalPlacer.composeResultMatrix(mapObj)
            #input()
            sendData(resultStr)
            #print(time.time() - start)
            #start = time.time()