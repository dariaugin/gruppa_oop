from abc import ABC, abstractmethod
import os

class Mediator(ABC):
    @abstractmethod
    def sendResolution(self, width, height):
        pass
    
    @abstractmethod     
    def runGraphic(self):
        pass
    
    @abstractmethod  
    def sendData(self, data):
        pass 
    
    @abstractmethod   
    def sendSignal(self, signal):
        pass    
    
    @abstractmethod    
    def getData(self):
        pass
    
    @abstractmethod
    def closeProgram(self):
        pass    

class Communicator(Mediator):
    #method for creating singleton specific
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Communicator, cls).__new__(cls)
            
        return cls.instance    
    
    def __init__(self): 
        pass
        
    def sendResolution(self, width, height):
        resolution = '{} {}'.format(width, height)
        flow = open("buffer.txt", 'w')
        flow.write(resolution)
        flow.close()
         
    def runGraphic(self):
        os.startfile("GraphicView.exe")
       
    def sendData(self, data):
        flow = open("buffer.txt", 'w')
        flow.write(data)
        flow.close() 
        
    def sendSignal(self, signal):
        flow = open("signal.txt", 'w')
        flow.write(signal)
        flow.close()     
        
    def getData(self):
        flow = open("buffer.txt", 'r')
        data = flow.read()
        flow.close()        
        return data
    
    def closeProgram(self):
        self.sendSignal("close")