'''
Created on Oct 16, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''

import sys
import os
if len(sys.argv[1:]) != 2:
    raise SystemExit("usage: %s pdb_file1 pdb_file2" % os.path.basename(sys.argv[0]))

pdb_file1 = sys.argv[1]
pdb_file2 = sys.argv[2]

# Panda3D imports
from pandac.PandaModules import loadPrcFileData
from dockit.dockit import Dockit

width = 900
height = 600

# Change window properties
loadPrcFileData("", "window-title Dock it!")
loadPrcFileData("", "fullscreen 0")
loadPrcFileData("", "win-size %s %s" % (width, height))

import direct.directbase.DirectStart

# Set up a loading screen
from direct.gui.OnscreenText import OnscreenText,TextNode
loadingText=OnscreenText("Loading molecules...",1,fg=(1,1,1,1),
                         pos=(0,0),align=TextNode.ACenter,
                         scale=.07,mayChange=1)
# Render three frames to avoid black screen
base.graphicsEngine.renderFrame() 
base.graphicsEngine.renderFrame()
base.graphicsEngine.renderFrame()

# Load the game
dockit = Dockit(width, height, pdb_file1, pdb_file2)

# Hide loading
loadingText.cleanup() 

run()
