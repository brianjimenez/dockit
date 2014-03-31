'''
Created on Oct 10, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''

class Color:
    
    def __init__(self, red=0., green=0., blue=0., alpha=1.0):
        self.__red = red
        self.__green = green
        self.__blue = blue
        self.__alpha = alpha
        
    def get_rgba(self):
        return self.__red, self.__green, self.__blue, self.__alpha
    
    def get_red(self):
        return self.__red
    
    def get_blue(self):
        return self.__blue
    
    def get_green(self):
        return self.__green
    
    def get_alpha(self):
        return self.__alpha

# Useful predefined colors
White = Color(1.0, 1.0, 1.0, 1.0)
Black = Color(0.0, 0.0, 0.0, 1.0) 
Carbon = Color(0.17, 0.17, 0.18, 1.0)
Red = Color(0.95, 0.03, 0.01, 1.0)
Blue = Color(0.01, 0.03, 0.95, 1.0)
Sky = Color(0.233, 0.686, 1.0, 1.0)
Yellow = Color(1.0, 1.0, 0.0, 1.0)
Green = Color(0.0, 0.53, 0.0, 1.0)
Pink = Color(0.53, 0.12, 0.36, 1.0)
DarkRed = Color(0.59, 0.13, 0.0, 1.0)
Violet = Color(0.46, 0.0, 1.0, 1.0)
DarkViolet = Color(0.39, 0.0, 0.73, 1.0)
Cyan = Color(0.0, 1.0, 1.0, 1.0)
Orange = Color(1.0, 0.59, 0.0, 1.0)
Peach = Color(1.0, 0.66, 0.46, 1.0)
DarkGreen = Color(0.0, 0.46, 0.0, 1.0)
Gray = Color(0.59, 0.59, 0.59, 1.0)
DarkOrange = Color(0.86, 0.46, 0.0, 1.0)