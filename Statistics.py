import numpy as np
from matplotlib import pyplot as plt
from random import random
#-----------------------added
import os
import pickle

class Statistics:
    #method for creating singleton specific
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Statistics, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.startSimulationsData = {} 
        self.simulationsData = {}
        
    #writing data methods
    def writeMapData(self, environment):
        self.mapData = [environment.height, environment.width, environment.terrainRatio]      
        
    def writeSimulationData(self, simulation, hunterNums, preyNums):
        try:
            self.simulationsData[simulation.ID][0] += len(hunterNums)
            self.simulationsData[simulation.ID][1].extend(hunterNums)  
            self.simulationsData[simulation.ID][2].extend(preyNums)
        except:
            self.startSimulationsData[simulation.ID] = [simulation.totalNum, simulation.occupyPercent,simulation.sidesRatio,simulation.hunterRatio,simulation.preyRatio]
            self.simulationsData[simulation.ID] = [len(hunterNums),hunterNums,preyNums]   
    
    def saveStatistics(self):
        path = "statistics_directory"
        if not os.path.isdir("statistics_directory"):
            os.mkdir("statistics_directory")
        fileList = os.listdir(path)
        fileName = path + "\\" + "map_st_Obj" + str(len(fileList) + 1) + ".txt"
        i = 1
        while True:
            if not os.path.exists(fileName):
                newFile = open(fileName,"wb")
                pickle.dump(self, newFile)
                newFile.close()
                break
            
            else:
                fileName = path + "\\" + "map_st_Obj" + str(len(fileList) + i) + ".txt"
                
            i += 1


    @staticmethod
    def loadStatistics(name):
        path = "statistics_directory"
        if os.path.isdir("statistics_directory"):
            statFile = open(path+"\\"+name, "rb")
            statObj = pickle.load(statFile)
            statFile.close()
            return statObj    

    #diagram showing methods          
    def HuntAndPreyPerTime(self, simNum):
        
        fig, ax = plt.subplots()
        
        x1 = range(self.simulationsData[simNum][0])
        y1 = [sum(lis) for lis in self.simulationsData[simNum][1]]
        y2 = [sum(lis) for lis in self.simulationsData[simNum][2]]

        ax.plot(x1, y1)
        ax.plot(x1, y2)

        plt.title("Simulation {} history of animal population".format(simNum))
        plt.xlabel("Time(cycles)")
        plt.ylabel("Side num")
        plt.legend(('Hunters','Prey'))
            
        plt.show()        
    
    def HuntersPerTime(self, simNum):
        x = range(self.simulationsData[simNum][0])
        huntersNums = self.simulationsData[simNum][1]

        speciesAmount = [[j[i] for j in huntersNums] for i in range(3)]
        fig, ax = plt.subplots()
        
        ax.stackplot(x, speciesAmount)
        
        plt.title("Simulation {} history of hunters population".format(simNum))
        plt.xlabel("Time(cycles)")
        plt.ylabel("Hunters num")        
        fig.set_figwidth(12)    
        fig.set_figheight(6)    
        fig.set_facecolor('floralwhite')
        ax.set_facecolor('seashell')
        plt.legend(('Hedgehog','Snake','Weasel'))
        plt.show()        
    
    def PreyPerTime(self, simNum):        
        x = range(self.simulationsData[simNum][0])
        preyNums = self.simulationsData[simNum][2]

        speciesAmount = [[j[i] for j in preyNums] for i in range(3)]
        fig, ax = plt.subplots()
        
        ax.stackplot(x, speciesAmount)
        
        plt.title("Simulation {} history of prey population".format(simNum))
        plt.xlabel("Time(cycles)")
        plt.ylabel("Prey num")        
        fig.set_figwidth(12)    
        fig.set_figheight(6)    
        fig.set_facecolor('floralwhite')
        ax.set_facecolor('seashell')
        plt.legend(('Mouse', 'Frog', 'FlightlessBird'))
        plt.show()        
    
    def HuntToPreyPerTime(self, simNum, reverse = False):
        if reverse:
            ratioName = "prey/hunter"
            arr1Id = 2
            arr2Id = 1            
        else:
            ratioName = "hunter/prey"
            arr1Id = 1
            arr2Id = 2
        fig, ax = plt.subplots()
        
        x1 = range(self.simulationsData[simNum][0])
        y1 = [sum(lis) for lis in self.simulationsData[simNum][arr1Id]]
        y2 = [sum(lis) for lis in self.simulationsData[simNum][arr2Id]]
        if y2[-1] == 0:
            return None
        y3 = [y1[i] / y2[i] for i in x1]

        ax.plot(x1, y3)

        plt.title("Simulation {} history of {} ratio".format(simNum, ratioName))
        plt.xlabel("Time(cycles)")
        plt.ylabel("Ratio size")
            
        plt.show()        
    
    def BarDiagramHunters(self, time):
        keys = self.simulationsData.keys()
        hunterNums = []
        for key in list(keys):
            hunterNums.append(self.simulationsData[key][1][time - 1])
         
        speciesAmount = [[j[i] for j in hunterNums] for i in range(3)]
        ind = np.arange(len(keys))
        width = 0.2
    
        p1 = plt.bar(ind, speciesAmount[0], width, color = "green")
        p2 = plt.bar(ind, speciesAmount[1], width, bottom = speciesAmount[0], color = "red")
        p3 = plt.bar(ind, speciesAmount[2], width, bottom = [x+y for x, y in zip(speciesAmount[0], speciesAmount[1])], color = "blue")

        plt.title("Simulations comparison by hunters num on the {} cycle".format(time))
        plt.xlabel("Simulation num")
        plt.ylabel("Hunters num")
        plt.xticks(np.arange(len(keys)), list(keys))    
        plt.legend((p1[0], p2[0], p3[0]), ('Hedgehog','Snake','Weasel'))
        
        plt.show()        
    
    def BarDiagramPrey(self, time):
        keys = self.simulationsData.keys()
        preyNums = []
        for key in list(keys):
            preyNums.append(self.simulationsData[key][2][time - 1])
        
        speciesAmount = [[j[i] for j in preyNums] for i in range(3)]

        width = 0.2
        ind = np.arange(len(keys))       

        p1 = plt.bar(ind, speciesAmount[0], width, color = "green")
        p2 = plt.bar(ind, speciesAmount[1], width, bottom = speciesAmount[0], color = "red")
        p3 = plt.bar(ind, speciesAmount[2], width, bottom = [x+y for x, y in zip(speciesAmount[0], speciesAmount[1])], color = "blue")
        
        plt.title("Simulations comparison by prey num on the {} cycle".format(time))
        plt.xlabel("Simulation num")
        plt.ylabel("Prey num")
        plt.xticks(np.arange(len(keys)), list(keys))    
        plt.legend((p1[0], p2[0], p3[0]), ('Mouse', 'Frog', 'FlightlessBird'))
        
        plt.show()          
    
    def BarDiagramTotalTime(self):
        keys = self.simulationsData.keys()
        totals = []
        for key in keys:
            totals.append(self.simulationsData[key][0])
        
        keys = range(6)
        totals = [10,12,2,4,8,7]
        fig, ax = plt.subplots()
        ax.bar(keys, totals)
            
        plt.title("Simulations comparison by total time")
        plt.xlabel("Simulation num")
        plt.ylabel("Total time of simulation(cycles)")        
        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        fig.set_figwidth(12)    
        fig.set_figheight(6)    
            
        plt.show()    
    
    def Lotki_Volterra(self):
        pass