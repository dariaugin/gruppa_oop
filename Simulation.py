import Animal, Map, Statistics
from Communicator import Communicator
import keyboard, random, copy, math, asyncio

def sin(day, T):
    return abs(math.sin(day * (math.pi / T) % math.pi))

class Simulation:
    mode={"sin":sin,"const":None}  #T=30
    def __init__(self, ID, statistics, environment, occupyPercent, sidesRatio=[20,80], hunterRatio=[33,33,34], preyRatio=[33,33,34], display = False, maxDayNum = 10, grassUpdateFrequency=7, T=30,sunMode = "const", communicator = None,):
        self.environment = environment
        self.ID = ID
        self.statistics = statistics
        self.communicator = Communicator()
        self.statistics.writeMapData(self.environment)
        self.occupyPercent = occupyPercent
        self.sidesRatio = sidesRatio
        self.hunterRatio = hunterRatio
        self.preyRatio = preyRatio
        self.display = display
        self.cycles = 0
        self.days = 0
        self.minProductivity = self.environment.grassCellNum // 5
        self.grassUpdateFrequency = grassUpdateFrequency
        self.maxDayNum = maxDayNum
        self.T = T
        self.sunMode = self.__class__.mode[sunMode] 
        self.cellDict = {}
        
        Animal.AnimalPlacer.initBiota(self)
        Animal.AnimalPlacer.initAnimalMatrix(self)        
        Animal.AnimalPlacer.placeAllAnimals(self)
            
    def run(self):  
        if self.display:
            self.communicator.sendResolution(self.environment.width, self.environment.height)
            self.communicator.sendSignal("open")
            self.communicator.runGraphic()
        
        self.maxProductivity = self.environment.startGrassAmount
        amountListHunter = []
        amountListPrey = []
       
        while True:   
            if self.totalNum <= 1 or keyboard.is_pressed('q') or self.cycles / self.grassUpdateFrequency > self.maxDayNum:
                self.communicator.closeProgram()
                break
            
            if not self.communicator.getData(): 
                #self.simulationControl([0, 1, 0])#
                amountListHunter.append(copy.copy(self.speciesAmount[0]))
                amountListPrey.append(copy.copy(self.speciesAmount[1])) 
                asyncio.run(self.passCycle())
                if self.cycles % self.grassUpdateFrequency == 0:
                    self.statistics.writeSimulationData(self, amountListHunter, amountListPrey)
                    amountListHunter = []
                    amountListPrey = []                    
                    self.sunActivityFunc()
                    self.environment.addGrass()
                    self.days += 1
                    
                self.cycles += 1
                if self.display:
                    resultStr = self.composeResultMatrix()
                    self.communicator.sendData(resultStr) 
                
    def sunActivityFunc(self):
        if self.sunMode == None:
            return None
        self.environment.startGrassAmount = self.maxProductivity * self.sunMode(self.days, self.T)
        if self.environment.startGrassAmount < self.minProductivity:
            self.environment.startGrassAmount = self.minProductivity
    
    async def passCycle(self):
        i = 0
        for animal in self.animalList:
            await animal.activityProcess(i)
            i += 1     
                
    def showAnimalData(self):
        i = 1
        for animal in self.animalList:
            print(i,". ",animal.symbol, end=": ")
            for cell in animal.cellList:
                print("(", cell.y, ",", cell.x, ")", end=" | ")
            print(animal.cellLife," | ",animal.cellList[0].localDirect)
            i += 1
    
    def showMap(self, needShow = [1, 1, 1]):
        if needShow[0]:
            print("mapMatrix:")
            for i in range(self.environment.height):
                for j in range(self.environment.width):
                    print(self.environment.groundMatrix[i][j],end="")
                print()        
        if needShow[1]:
            print("animalMatrix:")
            for i in range(self.environment.height):
                for j in range(self.environment.width):
                    if self.animalMatrix[i][j] != None:
                        print(self.animalMatrix[i][j],end="")
                    else:
                        print(" ",end="")
                print()   
            
        resultMatrix = copy.deepcopy(self.environment.groundMatrix)
        for i in range(self.environment.height):
            for j in range(self.environment.width):
                if self.animalMatrix[i][j] != None:
                    resultMatrix[i][j] = self.animalMatrix[i][j]        
            
        if needShow[2]:
            print("resultMatrix:")
            for i in range(self.environment.height):
                for j in range(self.environment.width):
                    print(resultMatrix[i][j],end="")
                print() 
                
    def simulationControl(self, needShow = [1, 1, 1]):
        self.showMap(needShow)
        self.showAnimalData()
        cellCoords = self.cellDict.keys()
        print(len(cellCoords), cellCoords)        
    
    def composeResultMatrix(self):
        resultMatrix = copy.deepcopy(self.environment.groundMatrix)
        for i in range(self.environment.height):
            for j in range(self.environment.width):
                if self.animalMatrix[i][j] != None:
                    resultMatrix[i][j] = self.animalMatrix[i][j]
        
        resultList = []
        for row in resultMatrix:
            resultList.extend(row)
           
        resultStr = ''.join([str(elem) for elem in resultList]) + ' '
        return resultStr       
                
if __name__=='__main__':
    dayNum = 100
    occupyPercent = 20
    resolution = input("Resolution(WxH): ") #max: 235 130
    width, height = [int(elem) for elem in resolution.split(' ')]
    
    while True:
        if 10 > width or 10 > height:
            print("Change width or height(it must be bigger than 10): ", end = "")
            width, height = [int(elem) for elem in input().split(' ')]
            continue
        break
    
    stat = Statistics.Statistics()
    mapObj = Map.Map(width, height, [20,3,60])
    comm = Communicator()
    mapObj.showMapGraphic()
    sim = Simulation(0, stat, mapObj, occupyPercent, communicator = comm, grassUpdateFrequency=20, maxDayNum = dayNum, display=True)
    sim.run()    