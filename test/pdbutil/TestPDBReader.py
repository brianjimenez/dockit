'''
Created on Oct 9, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''

import os
from nose.tools import *
from pdbutil.PDBReader import PDBReader

class TestPDBReader:
   
    def setUp(self):
        self.golden_data_path = os.path.normpath(os.path.dirname(os.path.realpath(__file__))) + '/golden_data/'

    def tearDown(self):
        pass
    
    def test_read_pdb_from_file(self):
        protein = PDBReader.read_pdb_from_file(os.path.join(self.golden_data_path, "1YU8.pdb"))
        atoms = protein.get_atoms()
        assert 508 == len(atoms)
        
