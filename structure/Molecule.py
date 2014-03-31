'''
Created on Oct 9, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''

class Molecule:
    def __init__(self, n_chainId, n_residues = None):
        self.__chain_id = n_chainId
        if n_residues == None:
            self.residues = []
        else:
            self.residues = n_residues
    
    def add_residue (self, residue):
        self.residues.append(residue)
    
    def remove_residue (self, residue):
        self.residues.remove(residue)
    
    def remove_atom (self, atom):
        for res in self.get_residues():
            if res.get_atoms().count(atom) > 0:
                res.remove_atom(atom)
                break
    
    def remove_hydrogens (self):
        for res in self.residues:
            res.remove_hydrogens()
    
    def get_chain_id(self):
        return self.__chain_id
    
    def get_residues(self):
        return self.residues
    
    def get_residue(self, resType, resNumber):
        result = None
        for res in self.get_residues():
            if ((res.get_residue_number() == int(resNumber)) and (res.get_residue_type() == resType.upper())):
                result = res
                break
        return result
    
    def get_atoms(self):
        atomList = []
        for res in self.residues:
            atomList.extend(res.get_atoms())
        return atomList
    
    def set_chain_id(self, n_chainId):
        self.__chain_id = n_chainId
        for res in self.get_residues():
            res.set_chain_id(n_chainId)
    
    def clone (self):
        newResidues = []
        for res in self.get_residues():
            newResidues.append(res.clone())
        return Molecule (self.get_chain_id(), newResidues)
    
    def get_residue_types (self):
        strType = ""
        for res in self.get_residues():
            strType += res.get_residue_type_1_letter()
        return strType
    
    def get_center_of_coordinates(self):
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
        residues = self.get_residues()
        for residue in residues:
            output += "%s" % (str(residue))
        return output