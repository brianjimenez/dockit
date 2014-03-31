'''
Created on Oct 10, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''

from gui import Color
from gui.ColorMap import ColorMap

class CPK(ColorMap):
    
    def __init__(self):
        super(CPK, self).__init__()
        self.__atom_color = {'H':Color.White, 'C':Color.Carbon, 'N':Color.Sky, 'O':Color.Red,
                             'F':Color.Green, 'Cl':Color.Green, 'Br':Color.DarkRed, 'I':Color.DarkViolet,
                             'He':Color.Cyan, 'Ne':Color.Cyan, 'Ar':Color.Cyan, 'Xe':Color.Cyan,
                             'Kr':Color.Cyan, 'P':Color.Orange, 'S':Color.Yellow, 'B':Color.Peach,
                             'Li':Color.Violet, 'Na':Color.Violet, 'K':Color.Violet, 'Rb':Color.Violet,
                             'Cs':Color.Violet, 'Be':Color.DarkGreen, 'Mg':Color.DarkGreen, 'Ca':Color.DarkGreen,
                             'Sr':Color.DarkGreen, 'Ba':Color.DarkGreen, 'Ra':Color.DarkGreen,
                             'Ti':Color.Gray, 'Fe':Color.Orange
                             }
        
    
    def get_color_by_element(self, element):
        try:
            return self.__atom_color[element]
        except:
            return Color.Pink