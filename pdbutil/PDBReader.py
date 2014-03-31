'''
Created on Oct 9, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''

from util.StringUtil import StringUtil
from structure.Protein import Protein
from structure.Molecule import Molecule
from structure.Residue import Residue
from structure.Atom import Atom
import re

class PDBReader:
    
    ELEMENT = re.compile('[A-Za-z ][A-Za-z]')
    
    @staticmethod
    def read_atom_line(line):
        ''' Read a line from a PDB file starting with ATOM '''
        elem = StringUtil.cstrip(line[76:78])
        if not PDBReader.ELEMENT.match(elem):
            elem = StringUtil.cstrip(line[12:14])
        
        x = float(line[30:38])
        y = float(line[38:46])
        z = float(line[46:54])
        
        return Atom (StringUtil.cstrip(line[0:6]),      # label
                     int(line[6:11]),                   # atom number
                     StringUtil.cstrip(line[12:16]),    # atom name
                     StringUtil.cstrip(line[16]),       # alternative atom
                     StringUtil.cstrip(line[17:21]),    # residue name
                     StringUtil.cstrip(line[21]),       # chain id
                     int(line[22:26]),                  # residue number
                     line[26],                          # resExt
                     x,                                 # X coordinate
                     y,                                 # Y coordinate
                     z,                                 # Z coordinate
                     float(line[54:60]),                # occupancy
                     float(line[60:66]),                # B-Factor
                     elem)                              # element
    
    
    @staticmethod
    def read_pdb_from_file(file_name):
        ''' Read atom PDB file_name '''
        lines = file(file_name).readlines()
        
        protein = Protein()
        last_chain = "dummy"
        last_residue = 9999999999
        last_residue_ext = "!" #dummy
        new_mol = 0
        num_line = 0
        numModels = 0
      
        for line in lines:
            num_line += 1
            try:
                if line[0:6] == "MODEL ":
                    numModels += 1
                if (line[0:4] == "ATOM") and numModels <= 1: 
                    line = line[:-1]
                    atom = PDBReader.read_atom_line (line)
                    
                    if (last_chain != atom.get_chain_id()):
                        mol = Molecule(atom.get_chain_id())
                        protein.add_molecule(mol)
                        new_mol = 1
    
                    if (last_residue != atom.get_residue_number()) or (last_residue_ext != atom.get_residue_ext()) or (new_mol):
                        res = Residue()
                        mol.add_residue(res)
                        new_mol = 0
                    
                    res.add_atom(atom)
                    
                    last_residue = atom.get_residue_number()
                    last_chain = atom.get_chain_id()
                    last_residue_ext = atom.get_residue_ext()
            except Exception, e:
                raise Exception('Problem reading %s file at line %s: %s' % (str(file_name), str(num_line), str(e)))
        return protein