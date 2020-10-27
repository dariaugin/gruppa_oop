import random
import os
import curses
import ctypes
import copy
import pickle
import time

class Map:
    terrain = {"rock":"#","ground":",","water":"~"}
    def __init__(self, height, width, terrainRatio, waterIntervals = [1,8], rockIntervals = [0,1], grassIntervals = [0,3], save = True):        
        self.terrainRatio = terrainRatio
        self.waterIntervals = waterIntervals
        self.rockIntervals = rockIntervals
        self.grassIntervals = grassIntervals
        self.height = height
        self.width = width
        self.square = height * width
        #self.groundObjectsAccomodation = {}
        #self.barriers = []
        self.groundMatrix = []
        self.createField()
        self.placeObj(0)
        self.placeObj(1)
        self.placeObj(2)        
        #self.findFreePlaces()
    
    def createField(self):
        self.groundMatrix = [[Map.terrain["ground"] for _ in range(self.height)] for _ in range(self.width)]  
                
    def placeObj(self, obj):
        percent = self.terrainRatio[obj]
        if obj == 0: 
            self.interval = self.waterIntervals
            terrain = "water"
            multiplier = 30
        elif obj == 1:
            self.interval = self.rockIntervals
            terrain = "rock"
            multiplier = 3
        elif obj == 2:
            self.interval = self.grassIntervals
            grass = range(1, 10)
            multiplier = 4
            
        cellNum = (self.square // 100) * percent
        Oy = range(self.height)
        Ox = range(self.width)
        sigma = range(self.interval[0], self.interval[1]+1)
        if obj == 2:
            self.grassCellNum = cellNum
        while cellNum:
            x = random.choice(Ox)
            y = random.choice(Oy)            
            s = random.choice(sigma)
            maxX = 0
            maxY = 0          
            n = s * cellNum * multiplier
            while n:
                divx = int(random.gauss(x, s))
                divy = int(random.gauss(y, s))
                if (0 <= divy < self.height) and (0 <= divx < self.width):
                    if self.groundMatrix[divx][divy] == Map.terrain["ground"]:
                        cellNum -= 1
                        if obj != 2:
                            self.groundMatrix[divx][divy] = Map.terrain[terrain]
                            #self.groundObjectsAccomodation[(divy,divx)] = 1
                            '''
                            diffX = abs(x - divx)
                            diffY = abs(y - divy)
                            if diffX > maxX:
                                maxX = diffX
                            if diffY > maxY:
                                maxY = diffY
                            '''
                        elif obj == 2:
                            self.groundMatrix[divx][divy] = random.choice(grass)
                if not cellNum:
                    '''
                    if maxX != 0 and maxY != 0:
                        self.barriers.append((x,y,maxX,maxY))
                    '''
                    return None 
                n -= 1  
            '''
            if maxX != 0 and maxY != 0:
                self.barriers.append((x,y,maxX,maxY))
            '''
        
    def saveMap(self, path = "BD"):
        fileList = os.listdir(path)
        fileName = path + "\\" + "mapObj" + str(len(fileList) + 1) + ".txt"
        i = 1
        while True:
            if not os.path.exists(fileName):
                newFile = open(fileName,"wb")
                pickle.dump(self, newFile)
                newFile.close()
                break
            else:
                fileName = path + "\\" + "mapObj" + str(len(fileList) + i) + ".txt"
                
            i += 1
        
    def copyMap(self, n = 1):
        if n == 1:
            objCopy = copy.deepcopy(self)
            return objCopy
        
        else:
            copyList = []
            i = 0
            while i < n:
                copyList.append(copy.deepcopy(self))
                i += 1
            return copyList
    
    @staticmethod
    def loadMap(name, path = "BD"):
        mapFile = open(path+"\\"+name, "rb")
        mapObj = pickle.load(mapFile)
        mapFile.close()
        return mapObj
    
    def rewriteGrass(self):
        for i in range(self.width):
            for j in range(self.height):
                if type(self.groundMatrix[i][j]) is int:
                    self.groundMatrix[i][j] = Map.terrain["ground"]
        
        self.placeObj(2)
      
    def addGrass(self):
        #while self.grassCellNum < 
        pass
    
    def showMapColor(self):
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        
        #color init
        screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        
        #---textures---#
        curses.init_pair(1, 136, 130)      #ground
        curses.init_pair(2, 15, 34)    #grass
        curses.init_pair(3, 159, 27)      #water
        curses.init_pair(4, 240, 243)      #rock
        
        x = 0
        y = 0
        for horline in self.groundMatrix:
            for verline in horline:
                if verline == ",":
                    cp = 1
                elif type(verline) == int:
                    cp = 2
                elif verline == "~":
                    cp = 3
                elif verline == "#":
                    cp = 4
                    
                screen.addstr(y, x, str(verline), curses.color_pair(cp)) 
                x += 1
            
            y += 1
            x = 0 
            
        screen.refresh()
        while True:
            pass
    
    def showMap(self):
        print("Press printing mode(0/1):", end ='')
        bool = int(input())
        if bool:
            self.showMapColor()
        else:
            for i in range(self.width):
                for j in range(self.height):
                    print(self.groundMatrix[i][j],end="")
                print()          

if __name__ == '__main__':
    width = 210
    height = 53
    
    if 10 > width:
        print("Change width(it must be bigger than 10):", end = "")
        width = input()
        
    if 10 > height:
        print("Change height(it must be bigger than 10):", end = "")
        height = input()
    
    start = time.time()  
    mapObj = Map(width, height, [20,3,60])   #[22,5,40]
    finish = time.time()
    print("Duration: ",finish - start," s")
    mapObj.showMap()
         

    
  
