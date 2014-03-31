'''
Created on Oct 9, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''

class Atom:
    
    vdw_radius = {'C':1.9080, 'N':1.8240, 'O':1.6612, 'S':2.0000}
    
    def __init__(self, n_label = None, n_atomNumber = None, n_atomType = None, n_atalt = None, 
                 n_resType = None, n_chainId = None, n_resNumber = None, n_resExt = None, 
                 n_coordX = None, n_coordY = None, n_coordZ = None, n_occ = None, n_b = None, 
                 n_elem = None, n_mass = 0., n_amberType = None):
        self.__label = n_label
        self.__atom_number = n_atomNumber 
        self.__atom_type = n_atomType
        self.__alternative = n_atalt
        self.__residue_type = n_resType
        self.__chain_id = n_chainId
        self.__residue_number = n_resNumber
        self.__residue_ext = n_resExt
        self.__x = n_coordX
        self.__y = n_coordY
        self.__z = n_coordZ
        self.__occupancy = n_occ
        self.__b_factor = n_b
        self.__element = n_elem
        self.__mass = n_mass
        self.__amber_type = n_amberType

    def get_label (self):
        return self.__label
    
    def set_label (self, n_label):
        self.__label = n_label
    
    def get_atom_number (self):
        return self.__atom_number
    
    def set_atom_number (self, n_atomNumber):
        self.__atom_number = n_atomNumber
    
    def get_atom_type (self):
        return self.__atom_type
    
    def set_atom_type (self, n_atomType):
        self.__atom_type = n_atomType
    
    def get_atom_alternative (self):
        return self.__alternative
    
    def set_atom_alternative (self, n_atalt):
        self.__alternative = n_atalt
    
    def get_residue_type (self):
        return self.__residue_type
    
    def set_residue_type (self, n_residueType):
        self.__residue_type = n_residueType
    
    def get_chain_id (self):
        return self.__chain_id
    
    def set_chain_id (self, n_chainId):
        self.__chain_id = n_chainId
    
    def get_residue_number (self):
        return self.__residue_number
    
    def set_residue_number (self, n_resNumber):
        self.__residue_number = n_resNumber
    
    def get_residue_ext (self):
        return self.__residue_ext
    
    def set_residue_ext (self, n_resExt):
        self.__residue_ext = n_resExt
    
    def get_x (self):
        return self.__x
    
    def set_x (self, n_coordX):
        self.__x = n_coordX
    
    def get_y (self):
        return self.__y
    
    def set_y (self, n_coordY):
        self.__y = n_coordY
    
    def get_z (self):
        return self.__z
    
    def set_z (self, n_coordZ):
        self.__z = n_coordZ
    
    def get_occupancy (self):
        return self.__occupancy
    
    def set_occupancy (self, n_occ):
        self.__occupancy = n_occ
    
    def get_b_factor (self):
        return self.__b_factor
    
    def set_b_factor (self, n_b):
        self.__b_factor = n_b
    
    def get_element (self):
        return self.__element
    
    def set_element (self, n_elem):
        self.__element = n_elem
    
    def get_mass(self):
        return self.__mass
    
    def set_mass(self, n_mass):
        self.__mass = n_mass
    
    def get_amber_type(self):
        return self.__amber_type
    
    def set_amber_type(self, n_amberType):
        self.__amber_type = n_amberType
    
    def clone (self):
        return Atom (self.get_label(),
                    self.get_atom_number(),
                    self.get_atom_type(),
                    self.get_atom_alternative(),
                    self.get_residue_type(),
                    self.get_chain_id(),
                    self.get_residue_number(),
                    self.get_residue_ext(),
                    self.get_x(),
                    self.get_y(),
                    self.get_z(),
                    self.get_occupancy(),
                    self.get_b_factor(),
                    self.get_element())
    
    def get_radius(self):
        element = self.get_element()
        try:
            return Atom.vdw_radius[element]
        except:
            return 1.0
    
    def __str__ (self):
        return "%4s %3.8f %3.8f %3.8f\n" % (self.get_atom_type(), 
                                            self.get_x(), 
                                            self.get_y(), 
                                            self.get_z())