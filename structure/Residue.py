'''
Created on Oct 9, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''

class Residue:
    def __init__(self, n_atoms = None):
        if n_atoms == None:
            self.atoms = []
        else:
            self.atoms = n_atoms
    
    def get_residue_number(self):
        try:
            result = self.get_atoms()[0].get_residue_number()
        except:
            result = None
        return result
    
    def get_residue_type(self):
        try:
            result = self.get_atoms()[0].get_residue_type()
        except:
            result = None
        return result
    
    def get_chain_id(self):
        try:
            result = self.get_atoms()[0].get_chain_id()
        except:
            result = None
        return result
    
    def get_residue_type_1_letter (self):
        resType = self.get_residue_type()
        if (resType == "ALA"): res = "A"
        elif (resType == "ARG"): res = "R"
        elif (resType == "ASN"): res = "N"
        elif (resType == "ASP"): res = "D"
        elif (resType == "CYS") or (resType == "CYX"): res = "C"
        elif (resType == "GLU"): res = "E"
        elif (resType == "GLN"): res = "Q"
        elif (resType == "GLY"): res = "G"
        elif (resType == "HIS") or (resType == "HIP") or (resType == "HID") or (resType == "HIE"): res = "H"
        elif (resType == "ILE"): res = "I"
        elif (resType == "LEU"): res = "L"
        elif (resType == "LYS"): res = "K"
        elif (resType == "MET"): res = "M"
        elif (resType == "PHE"): res = "F"
        elif (resType == "PRO"): res = "P"
        elif (resType == "SER"): res = "S"
        elif (resType == "THR"): res = "T"
        elif (resType == "TRP"): res = "W"
        elif (resType == "TYR"): res = "Y"
        elif (resType == "VAL"): res = "V"
        else: print "Residue has no 1 letter equivalent --> " + resType
        return res
    
    def add_atom (self, atom):
        self.atoms.append(atom)
    
    def remove_atom (self, atom):
        self.atoms.remove(atom)
    
    def remove_hydrogens (self):
        noH = []
        for atom in self.atoms:
            if atom.get_atom_type()[0] != 'H':
                noH.append(atom)
        self.atoms = noH
    
    def get_atoms(self):
        return self.atoms
    
    def set_chain_id(self, n_chainId):
        for atom in self.get_atoms():
            atom.set_chain_id(n_chainId)
    
    def set_residue_type(self, n_residueType):
        for atom in self.get_atoms():
            atom.set_residue_type(n_residueType)
    
    def clone (self):
        newAtoms = []
        for atom in self.get_atoms():
            newAtoms.append(atom.clone())
        return Residue (newAtoms)
    
    def has_alpha_carbon (self):
        res = 0
        for atom in self.get_atoms():
            if (atom.get_atom_type() == "CA"):
                res = 1
                break
        return res
    
    def get_alpha_carbon (self):
        for atom in self.get_atoms():
            if (atom.get_atom_type() == "CA"):
                return atom
    
    def get_center_coordinates(self):
        """ Calculate the center of coordinates of this residue """
        totalX = 0
        totalY = 0
        totalZ = 0
        for atom in self.get_atoms():
            totalX += atom.get_x()
            totalY += atom.get_y()
            totalZ += atom.get_z()
        
        xCenter = totalX / len(self.get_atoms())
        yCenter = totalY / len(self.get_atoms())
        zCenter = totalZ / len(self.get_atoms())
        
        return xCenter, yCenter, zCenter
    
    def __str__(self):
        output = ""
        atoms = self.get_atoms()
        for atom in atoms:
            output += "%4s  %s" % (self.get_residue_type(), str(atom))
        return output   