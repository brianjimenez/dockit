'''
Created on Oct 10, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''

from gui.Color import Color
from gui.Color import Red
from gui.Color import Blue
from gui.Color import White
from gui.ColorMap import ColorMap

class BFactor(ColorMap):
    
    tolerance = 0.05        # 5% tolerance
    minimum = 0.4           # Minimum value for color (from 0.0 to 1.0)
    top_color = Red
    bottom_color = Blue
    
    def __init__(self, min_value, max_value, middle_value):
        super(BFactor, self).__init__()
        self.__min = min_value
        self.__max = max_value
        self.__middle = middle_value
        self.__interval = abs(self.__min) + abs(self.__max)
        self.__mid_up = self.__middle + self.__interval * BFactor.tolerance
        self.__mid_down = self.__middle - self.__interval * BFactor.tolerance
        self.__up_step = (BFactor.top_color.get_red() - BFactor.minimum)/(self.__max-self.__mid_up)
        self.__down_step = (BFactor.bottom_color.get_blue() - BFactor.minimum)/abs(self.__min-self.__mid_down)
        
        
    def get_color_by_bfactor(self, bfactor):
        if bfactor > self.__mid_up:
            r, g, b, a = BFactor.top_color.get_rgba()
            r = BFactor.minimum + self.__up_step*bfactor
            return Color(r,g,b,a)
        elif bfactor < self.__mid_down:
            r, g, b, a = BFactor.bottom_color.get_rgba()
            b = BFactor.minimum + self.__down_step*abs(bfactor)
            return Color(r,g,b,a)
        else:
            return White
        