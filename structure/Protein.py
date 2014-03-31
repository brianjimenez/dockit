'''
Created on Oct 9, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''
import math

class Protein:
    def __init__(self, n_molecules = None):
        if n_molecules == None:
            self.molecules = []
        else:
            self.molecules = n_molecules
    
    def get_chain_ids(self):
        S_chainIds = []
        for mol in self.get_molecules():
            S_chainIds.append(mol.get_chain_id())
        return S_chainIds
    
    def has_chain_id(self, n_chainId):
        result = 0
        for chainId in self.get_chain_ids():
            if chainId == n_chainId:
                result = 1
                break
        return result
    
    def add_molecule(self, molecule):
        self.molecules.append(molecule)
    
    def remove_molecule(self, molecule):
        self.molecules.remove(molecule)
    
    def remove_hydrogens(self):
        for mol in self.molecules:
            mol.remove_hydrogens()
    
    def get_molecules(self):
        return self.molecules
    
    def get_residues(self):
        resList = []
        for mol in self.molecules:
            resList.extend(mol.get_residues())
        return resList
    
    def get_residue(self, chainId, resType, resNumber):
        return self.get_molecule_by_chain_id(chainId).get_residue(resType,resNumber)
    
    def get_atoms(self):
        atomList = []
        for mol in self.molecules:
            atomList.extend(mol.get_atoms())
        return atomList
    
    def get_molecule_by_chain_id(self, chainId):
        result = None
        for mol in self.get_molecules():
            if mol.get_chain_id() == chainId:
                result = mol
                break
        return result
    
    def delete_molecule_by_chain_id(self, chainId):
        # we assume every molecule has a different chain id
        for mol in self.get_molecules():
            if mol.get_chain_id() == chainId:
                self.molecules.remove(mol)
                break
    
    def remove_residue(self, residue):
        mol = self.get_molecule_by_chain_id(residue.get_chain_id())
        mol.remove_residue(residue)
    
    def remove_atom(self, atom):
        mol = self.get_molecule_by_chain_id(atom.get_chain_id())
        mol.remove_atom(atom)
    
    def clone(self):
        newMols = []
        for mol in self.get_molecules():
            newMols.append(mol.clone())
        return Protein (newMols)
    
    def move_to_origin(self):
        xCenter, yCenter, zCenter = self.get_center_of_coordinates()
        self.translate ([-xCenter, -yCenter, -zCenter])
    
    def rotate(self, rotation_matrix):
        """ Apply a rotate to this macromolecule given by the rotation_matrix """
        for atom in self.get_atoms():
            newCoordX = (rotation_matrix[0] * atom.get_x() +
                         rotation_matrix[1] * atom.get_y() +
                         rotation_matrix[2] * atom.get_z())
            newCoordY = (rotation_matrix[3] * atom.get_x() +
                         rotation_matrix[4] * atom.get_y() +
                         rotation_matrix[5] * atom.get_z())
            newCoordZ = (rotation_matrix[6] * atom.get_x() +
                         rotation_matrix[7] * atom.get_y() +
                         rotation_matrix[8] * atom.get_z())
            atom.set_x(newCoordX)
            atom.set_y(newCoordY)
            atom.set_z(newCoordZ)
    
    def translate(self, trans):
        """ Apply an spatial translation to this macromolecule given by the trans vector """ 
        for atom in self.get_atoms():
            atom.set_x(atom.get_x() + trans[0])
            atom.set_y(atom.get_y() + trans[1])
            atom.set_z(atom.get_z() + trans[2])
    
    def get_center_of_coordinates(self):
        """ Calculate the center of coordinates of this macromolecule """
        totalX = 0.0
        totalY = 0.0
        totalZ = 0.0
        for atom in self.get_atoms():
            totalX += atom.get_x()
            totalY += atom.get_y()
            totalZ += atom.get_z()
        numAtoms = float(len(self.get_atoms()))
        xCenter = totalX / numAtoms
        yCenter = totalY / numAtoms
        zCenter = totalZ / numAtoms 
        
        return xCenter, yCenter, zCenter
    
    def assign_masses(self, atomMassDict, types):
        """ Assign a mass value from an atomMassDict dictionary where key is residue-atom """
        atoms = self.get_atoms()
        for atom in atoms:
            key = atom.get_residue_type() + '-' + atom.get_atom_type()
            atomType = types[key]
            atom.set_mass(atomMassDict[atomType])
            if atom.get_amber_type() is None:
                atom.set_amber_type(atomType)
    
    def get_center_of_mass(self):
        """ Get the center of mass of this macromolecule """
        totalX = 0.0
        totalY = 0.0
        totalZ = 0.0
        totalMass = 0.0
        for atom in self.get_atoms():
            mass = atom.get_mass()
            totalX += atom.get_x() * mass
            totalY += atom.get_y() * mass
            totalZ += atom.get_z() * mass
            totalMass += mass
        xCenter = totalX / totalMass
        yCenter = totalY / totalMass
        zCenter = totalZ / totalMass 
    
        return [xCenter, yCenter, zCenter]
    
    def get_coordinates(self):
        x = []
        y = []
        z = []
        for atom in self.get_atoms():
            x.append(atom.get_x())
            y.append(atom.get_y())
            z.append(atom.get_z())     
        return x,y,z
    
    def get_diameter(self):
        x, y, z = self.get_coordinates()
        min_x = min(x)
        max_x = max(x)
        min_y = min(y)
        max_y = max(y)
        min_z = min(z)
        max_z = max(z)
        
        return math.sqrt((max_x-min_x)*(max_x-min_x) + \
                         (max_y-min_y)*(max_y-min_y) + \
                         (max_z-min_z)*(max_z-min_z))
        
    
    def __str__(self):
        output = ""
        molecules = self.get_molecules()
        for molecule in molecules:
            output += "%s" % (str(molecule))
        return output
