#A simple class Task help us to manage the tasks easier
class Task :
    def __init__( self, name,id, day, month ) :
        self.__name = name
        self.__id = id
        self.day = day
        self.month = month 
        self.done = False
        
    def getID(self) :
        return self.__id
    
    def getName(self) :
        return self.__name
        
    def checkStatus(self) :
        return self.done
    
    def Done(self) :
        self.done = True
        
    def __str__(self) :
        x = ''
        if self.done == False :
            x = 'X'
        else :
            x = 'V'
        return f'{self.__name};{self.__id};{self.day};{self.month};{x}'
    
