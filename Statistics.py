import numpy as np
from matplotlib import pyplot as plt
#from random import random

class Statistics:
    #method for creating singleton specific
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Statistics, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.startSimulationData = {} 
        self.simulationsData = {}
        
    #writing data methods
    def writeMapData(self, environment):
        self.mapData = [height, width, terrainRatio]      
        
    def writeSimulationData(self, simulation, simulNum, hunterNums, preyNums):
        try:
            self.simulationsData[simulNum][0] += len(hunterNums)
            self.simulationsData[simulNum][1].extend(hunterNums)  
            self.simulationsData[simulNum][2].extend(preyNums)
        except:
            self.startSimulationsData[simulNum] = (len(simulation.animalList), simulation.occupyPercent,simulation.sidesRatio,simulation.hunterRatio,simulation.preyRatio)
            self.simulationsData[simulNum] = (len(hunterNum),hunterNums,preyNums)
    
    #load/save methods      
    def saveStatistics(self, path = "BD"):
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
    
    @staticmethod
    def loadStatistics(name, path="BD"):
        statFile = open(path+"\\"+name, "rb")
        statObj = pickle.load(statFile)
        statFile.close()
        return statObj    
    
    #diagram showing methods          
    def HuntAndPrayPerTime(self, simNum):
        fig, ax = plt.subplots()
        
        x1 = range(self.simulationData[simNum][0])
        y1 = [sum(lis) for lis in self.simulationData[simNum][1]]
        y2 = [sum(lis) for lis in self.simulationData[simNum][2]]
        '''
        x1 = range(100)
        y1 = [int(random()*10)for _ in range(100)]
        y2 = [int(random()*10)for _ in range(100)]
        '''
        ax.plot(x1, y1)
        ax.plot(x1, y2)

        plt.title("Simulation {} history of animal population".format(simNum))
        plt.xlabel("Time(days)")
        plt.ylabel("Side num")
        plt.legend(('Hunters','Pray'))
            
        plt.show()        
    
    def HuntersPerTime(self, simNum):
        x = range(self.simulationData[simNum][0])
        huntersNums = self.simulationData[simNum][1]
        '''
        x = range(1, 4)
        huntersNums = [[10,12,4],[17,15,2],[20,14,10]]
        '''
        speciesAmount = [[j[i] for j in huntersNums] for i in range(3)]
        fig, ax = plt.subplots()
        
        ax.stackplot(x, speciesAmount)
        
        plt.title("Simulation {} history of hunters population".format(simNum))
        plt.xlabel("Time(days)")
        plt.ylabel("Hunters num")        
        fig.set_figwidth(12)    
        fig.set_figheight(6)    
        fig.set_facecolor('floralwhite')
        ax.set_facecolor('seashell')
        plt.legend(('Hedgehog','Snake','Weasel'))
        plt.show()        
    
    def PrayPerTime(self, simNum):
        x = range(self.simulationData[simNum][0])
        prayNums = self.simulationData[simNum][2]
        '''
        x = range(1, 4)
        prayNums = [[10,12,4],[17,15,2],[20,14,10]]
        '''
        speciesAmount = [[j[i] for j in prayNums] for i in range(3)]
        fig, ax = plt.subplots()
        
        ax.stackplot(x, speciesAmount)
        
        plt.title("Simulation {} history of pray population".format(simNum))
        plt.xlabel("Time(days)")
        plt.ylabel("Pray num")        
        fig.set_figwidth(12)    
        fig.set_figheight(6)    
        fig.set_facecolor('floralwhite')
        ax.set_facecolor('seashell')
        plt.legend(('Mouse', 'Frog', 'FlightlessBird'))
        plt.show()        
    
    def HuntToPrayPerTime(self, simNum, reverse = False):
        if reverse:
            ratioName = "pray/hunter"
            arr1Id = 2
            arr2Id = 1            
        else:
            ratioName = "hunter/pray"
            arr1Id = 1
            arr2Id = 2
        fig, ax = plt.subplots()
        x1 = range(self.simulationData[simNum][0])
        y1 = [sum(lis) for lis in self.simulationData[simNum][arr1Id]]
        y2 = [sum(lis) for lis in self.simulationData[simNum][arr2Id]]
        y3 = [y1[i] / y2[i] for i in x1]
        '''
        x1 = range(100)
        y1 = [int(random()*10)for _ in range(100)]
        y2 = [int(random()*10)for _ in range(100)]
        y3 = [y1[i] / (y2[i] + 0.00001) for i in x1]
        '''
        ax.plot(x1, y3)

        plt.title("Simulation {} history of {} ratio".format(simNum, ratioName))
        plt.xlabel("Time(days)")
        plt.ylabel("Ratio size")
            
        plt.show()        
    
    def BarDiagramHunters(self, time):
        keys = self.simulationsData.keys()
        hunterNums = []
        for key in keys:
            hunterNums.append(self.simulationsData[key][1][time])
            
        speciesAmount = [[j[i] for j in hunterNums] for i in range(3)]
        ind = np.arange(len(keys))
        width = 0.2
        ind = np.arange(3)
        
        ''' <- delete this and run method
        speciesAmount = [[10,12,4],[17,15,2],[20,14,10]]
        speciesAmount = [[j[i] for j in speciesAmount] for i in range(3)]      
        '''
    
        p1 = plt.bar(ind, speciesAmount[0], width, color = "green")
        p2 = plt.bar(ind, speciesAmount[1], width, bottom = speciesAmount[0], color = "red")
        p3 = plt.bar(ind, speciesAmount[2], width, bottom = [x+y for x, y in zip(speciesAmount[0], speciesAmount[1])], color = "blue")

        plt.title("Simulations comparison by hunters num on the {} day".format(time))
        plt.xlabel("Simulation num")
        plt.ylabel("Hunters num")
        plt.xticks(ind, keys)     
        plt.legend((p1[0], p2[0], p3[0]), ('Hedgehog','Snake','Weasel'))
        
        plt.show()        
    
    def BarDiagramPray(self, time):
        keys = self.simulationsData.keys()
        prayNums = []
        for key in keys:
            prayNums.append(self.simulationsData[key][2][time])
        
        speciesAmount = [[j[i] for j in prayNums] for i in range(3)]
        ind = np.arange(len(keys))
        width = 0.2
        ind = np.arange(3)       

        p1 = plt.bar(ind, speciesAmount[0], width, color = "green")
        p2 = plt.bar(ind, speciesAmount[1], width, bottom = speciesAmount[0], color = "red")
        p3 = plt.bar(ind, speciesAmount[2], width, bottom = [x+y for x, y in zip(speciesAmount[0], speciesAmount[1])], color = "blue")
        
        plt.title("Simulations comparison by pray num on the {} day".format(time))
        plt.xlabel("Simulation num")
        plt.ylabel("Pray num")
        plt.xticks(ind, keys)     
        plt.legend((p1[0], p2[0], p3[0]), ('Mouse', 'Frog', 'FlightlessBird'))
        
        plt.show()          
    
    def BarDiagramTotalTime(self):
        keys = self.simulationsData.keys()
        totals = []
        for key in keys:
            totals.append(self.simulationsData[key][0])
    
        fig, ax = plt.subplots()
        ax.bar(keys, totals)
            
        plt.title("Simulations comparison by total time")
        plt.xlabel("Simulation num")
        plt.ylabel("Total time of simulation")        
        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        fig.set_figwidth(12)    
        fig.set_figheight(6)    
            
        plt.show()    
    
    def Lotki_Volterra(self):
        pass
    
if __name__ == "__main__":
    DataCollector = Statistics()
    #DataCollector.BarDiagramTotalTime()
    #DataCollector.HuntersPerTime(10)
    #DataCollector.HuntAndPrayPerTime(10)
    #DataCollector.HuntToPrayPerTime(10)