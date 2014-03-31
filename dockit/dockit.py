'''
Created on Oct 9, 2012

@author: Brian Jimenez-Garcia
@contact: brian.jimenez@bsc.es
'''

# Panda3D imports
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties
from panda3d.core import LVecBase4f
from panda3d.core import NodePath, PandaNode, TextNode
from panda3d.core import LightRampAttrib, AmbientLight, DirectionalLight
from panda3d.core import TransparencyAttrib,AntialiasAttrib 
from panda3d.core import CompassEffect
#from pandac.PandaModules import WindowProperties
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenText import OnscreenText

# Dockit imports
from pdbutil.PDBReader import PDBReader
from gui.CPK import CPK
from gui.BFactor import BFactor

# Python imports
import sys

class Dockit(DirectObject):
    ''' Main class of the Dockit! game '''
    # VdW radius scale constant
    radius_scale = 1.5
    # Step to move ligand
    move_step = 50
    # Step to rotate ligand
    rotate_step = 90
    #Instructions
    instructions = ['Dock it!','',
                    'X: a/d','Y: w/s','Z: q/e',
                    'Heading: r/f','Pitch: t/g','Roll: h/y',
                    'Cartoon: c','Control: x','Center: z',
                    'Help: v','Exit: escape']
    
    def __init__(self, width, height, pdb_file1, pdb_file2, full_atom=True, debug=False):
        ''' Build Dockit! '''
        self.multisamples = base.win.getFbProperties().getMultisamples()
        self.cartoon = False
        self.structures = False
        self.help = False
        self.text_on_screen = []
        self.width = width
        self.height = height
        
        # Keyboard events
        self.accept('c', self.toggle_cartoon)
        self.accept('x', self.toggle_control_structures)
        self.accept('z', self.center_camera)
        self.accept('v', self.help_on_screen)
        self.accept('escape', sys.exit)
        self.keyMap = {"a":0, "d":0, "w":0, "s":0, "q":0, "e":0, 
                       "r":0, "f":0, "g":0, "t":0, "h":0, "y":0}
        
        # Load PDB structures
        receptor = PDBReader.read_pdb_from_file(pdb_file1)
        ligand = PDBReader.read_pdb_from_file(pdb_file2)
        receptor.move_to_origin()
        ligand.move_to_origin()
        
        # Background
        base.setBackgroundColor(0.7, 0.7, 0.7, 1.0)
        
        # Load Color maps
        color_map_cpk = CPK()
        color_map_bfactor = BFactor(min_value=-14.0, max_value=8.0, middle_value=0.0)
        
        # Load 3D model
        self.receptor_node = render.attachNewNode("Receptor")
        if full_atom:
            self.load_protein_full_atom(receptor, self.receptor_node, color_map_bfactor)
        else:
            self.load_protein_residue(receptor, self.receptor_node)
        self.receptor_node.reparentTo(render)
        
        self.ligand_node = render.attachNewNode("Ligand")
        if full_atom:
            self.load_protein_full_atom(ligand, self.ligand_node, color_map_cpk)
        else:
            self.load_protein_residue(ligand, self.ligand_node)
        self.ligand_node.reparentTo(render)
        
        # Ambient lights
        self.alight = AmbientLight('alight')
        self.alight.setColor(LVecBase4f(0.162679, 0.162679, 0.169059, 1.0))
        self.alnp = render.attachNewNode(self.alight)
        render.setLight(self.alnp)
        
        # Center receptor and ligand
        self.center_proteins()
        
        # Center camera on complexes
        self.center = loader.loadModel("models/atom_sphere")
        self.center.setColor(0.0, 0.53, 0.0, 1.0)
        self.center_camera()
        
        # DirectionalLight
        self.dlight = DirectionalLight('dlight')
        self.dlight.setColor(LVecBase4f(0.797448, 0.660287, 0.743222, 1.0))
        self.dlight.setShadowCaster(True, 512, 512)
        render.setShaderAuto()
        self.dlnp = render.attachNewNode(self.dlight)
        self.dlnp.setPos(0,-50,0)
        render.setLight(self.dlnp)
        self.dlnp.lookAt(self.center)
        l1 = loader.loadModel("models/Dirlight")
        l1.setColor(1.0, 1.0, 0.0, 1.0)
        l1.setPos(0, -50, 0)
        l1.setScale(1)
        self.lights = [l1]
        
        # Post processing        
        render.setAntialias(AntialiasAttrib.MAuto)
        
        # Show control structures if required
        if self.structures:
            for light in self.lights:
                light.reparentTo(render)
            self.center.reparentTo(render)
            
        # Movement functions
        taskMgr.add(self.ligand_movement, 'ligand_movement') 

        # Key mapping
        self.key_bindings()
        
        # Show frame rate
        if debug:
            base.setFrameRateMeter(True)
    
        # Create two windows from cameras pointing to each molecule
        wx = base.win.getProperties().getXOrigin()
        wy = base.win.getProperties().getYOrigin() 
        
        # Ligand window
        wp = WindowProperties()
        wp.setSize(300,300)
        wp.setOrigin(self.width + wx + 10, wy - 50)
        wp.setTitle('From Ligand')
        self.ligand_view = base.openWindow(props=wp)
        self.cam_ligand = base.camList[1]
        self.cam_ligand.setPos(self.center.getX(), self.center.getY(), self.center.getZ())
        self.cam_ligand.lookAt(self.receptor_node)
        
        # Receptor window
        wp = WindowProperties()
        wp.setSize(300,300)
        wp.setOrigin(self.width + wx + 10, wy + 300)
        wp.setTitle('From Receptor')
        self.receptor_view = base.openWindow(props=wp)
        self.cam_receptor = base.camList[2]
        self.cam_receptor.setPos(self.center.getX(), self.center.getY(), self.center.getZ())
        self.cam_receptor.lookAt(self.ligand_node)

        
    def key_bindings(self):
        ''' Define key bindings '''
        base.accept('a', self.setKey, ["a",1])
        base.accept('a-up', self.setKey, ["a",0])
        base.accept('d', self.setKey, ["d",1])
        base.accept('d-up', self.setKey, ["d",0])
        base.accept('w', self.setKey, ["w",1])
        base.accept('w-up', self.setKey, ["w",0])
        base.accept('s', self.setKey, ["s",1])
        base.accept('s-up', self.setKey, ["s",0])
        base.accept('q', self.setKey, ["q",1])
        base.accept('q-up', self.setKey, ["q",0])
        base.accept('e', self.setKey, ["e",1])
        base.accept('e-up', self.setKey, ["e",0])
        base.accept('f', self.setKey, ["f",1])
        base.accept('f-up', self.setKey, ["f",0])
        base.accept('r', self.setKey, ["r",1])
        base.accept('r-up', self.setKey, ["r",0])
        base.accept('g', self.setKey, ["g",1])
        base.accept('g-up', self.setKey, ["g",0])
        base.accept('t', self.setKey, ["t",1])
        base.accept('t-up', self.setKey, ["t",0])
        base.accept('h', self.setKey, ["h",1])
        base.accept('h-up', self.setKey, ["h",0])
        base.accept('y', self.setKey, ["y",1])
        base.accept('y-up', self.setKey, ["y",0])
        
        
    def ligand_movement(self, task):
        ''' Compute ligand movement depending on key bindings '''
        if (self.keyMap["a"]!=0):
            self.ligand_node.setX(self.ligand_node.getX()-Dockit.move_step * globalClock.getDt())
        if (self.keyMap["d"]!=0):
            self.ligand_node.setX(self.ligand_node.getX()+Dockit.move_step * globalClock.getDt())
        if (self.keyMap["q"]!=0):
            self.ligand_node.setY(self.ligand_node.getY()-Dockit.move_step * globalClock.getDt())
        if (self.keyMap["e"]!=0):
            self.ligand_node.setY(self.ligand_node.getY()+Dockit.move_step * globalClock.getDt())
        if (self.keyMap["w"]!=0):
            self.ligand_node.setZ(self.ligand_node.getZ()-Dockit.move_step * globalClock.getDt())
        if (self.keyMap["s"]!=0):
            self.ligand_node.setZ(self.ligand_node.getZ()+Dockit.move_step * globalClock.getDt())
        if (self.keyMap["r"]!=0):
            self.ligand_node.setH(self.ligand_node.getH()-Dockit.rotate_step * globalClock.getDt())
        if (self.keyMap["f"]!=0):
            self.ligand_node.setH(self.ligand_node.getH()+Dockit.rotate_step * globalClock.getDt())
        if (self.keyMap["g"]!=0):
            self.ligand_node.setP(self.ligand_node.getP()-Dockit.rotate_step * globalClock.getDt())
        if (self.keyMap["t"]!=0):
            self.ligand_node.setP(self.ligand_node.getP()+Dockit.rotate_step * globalClock.getDt())
        if (self.keyMap["h"]!=0):
            self.ligand_node.setR(self.ligand_node.getR()-Dockit.rotate_step * globalClock.getDt())
        if (self.keyMap["y"]!=0):
            self.ligand_node.setR(self.ligand_node.getR()+Dockit.rotate_step * globalClock.getDt())
        return task.cont


    def setKey(self, key, value):
        ''' Record the state of the arrow keys '''
        self.keyMap[key] = value 
        
        
    def load_protein_full_atom(self, protein, node, color_map):
        ''' Display a given protein using spheres models for each atom '''
        atoms = protein.get_atoms()
        self.atom_objects = []
        for atom in atoms:
            a = loader.loadModel("models/atom_sphere")
            a.setPos(atom.get_x(), atom.get_y(), atom.get_z())
            a.setScale(atom.get_radius() / Dockit.radius_scale)
            self.apply_color(a, atom, color_map)
            a.reparentTo(node)
        node.flattenStrong()
        
    
    def load_protein_residue(self, protein, node):
        ''' Display a given protein using spheres models for each atom '''
        residues = protein.get_residues()
        self.residues_objects = []
        for residue in residues:
            r = loader.loadModel("models/atom_sphere")
            x,y,z = residue.get_center_coordinates()
            r.setPos(x, y, z)
            r.setScale(4.0 / Dockit.radius_scale)
            r.setColor(LVecBase4f(1.0, 0.59, 0.0, 1.0))
            r.setColorScale(LVecBase4f(1, 1, 1, 1))
            r.reparentTo(node)
        node.flattenStrong()
        
        
    def apply_color(self, a3d, atom, color_map):
        ''' Apply a color map to the element '''
        if isinstance(color_map, BFactor):
            color = color_map.get_color_by_bfactor(atom.get_b_factor())
        else:
            color = color_map.get_color_by_element(atom.get_element())
        red, green, blue, alpha = color.get_rgba() 
        a3d.setColor(LVecBase4f(red, green, blue, alpha))
        a3d.setColorScale(LVecBase4f(1, 1, 1, 1))
    
    
    def toggle_cartoon(self):
        ''' Use Cartoon ink filter '''
        self.cartoon = not self.cartoon
        if self.cartoon:
            tempnode = NodePath(PandaNode("temp node"))
            tempnode.setAttrib(LightRampAttrib.makeSingleThreshold(0.4, 0.6))
            tempnode.setShaderAuto()
            base.cam.node().setInitialState(tempnode.getState())
            self.separation = 1.3 # Pixels
            self.filters = CommonFilters(base.win, base.cam)
            self.filters.setCartoonInk(separation=self.separation)
            # Currently using MAuto antialias, uncomment to use different
            #render.setAntialias(AntialiasAttrib.MBetter)
            #self.filters.finalQuad.setAntialias(AntialiasAttrib.MBetter)
        else:
            self.filters.cleanup()
            base.cam.node().setInitialState(self.alight.getState())
    
    
    def toggle_control_structures(self):
        ''' Show control structures as lights and center nodes and bounds if required '''
        self.structures = not self.structures
        for light in self.lights:
            if not self.structures:
                light.detachNode()
            else:
                light.reparentTo(render)
        
        if self.structures:
            self.receptor_node.showBounds()
            self.ligand_node.showBounds()
            self.center.reparentTo(render)
            print "Number of multisamples available: %d" % self.multisamples
        else:
            self.receptor_node.hideBounds()
            self.ligand_node.hideBounds()
            self.center.detachNode()
    
    
    def center_proteins(self):
        ''' Move receptor and ligand to a centered position depending on its size '''
        # Center the receptor
        receptor_radius = self.receptor_node.getBounds().getRadius()
        receptor_center = self.receptor_node.getBounds().getCenter()
        self.receptor_node.setPos(0,receptor_radius,0)
        
        # Center the ligand
        ligand_radius = self.ligand_node.getBounds().getRadius()
        self.ligand_node.setPos(receptor_center[0]-receptor_radius-ligand_radius, 
                                receptor_center[1], 
                                receptor_center[2])
        self.ligand_node.lookAt(self.receptor_node)
     
    
    def center_camera(self):
        ''' Center camera on scene '''
        xc, yc, zc = (self.receptor_node.getBounds().getCenter() + self.ligand_node.getBounds().getCenter()) / 2.0
        self.center.setPos(xc, yc, zc)
        ligand_radius = self.ligand_node.getBounds().getRadius()
        receptor_radius = self.receptor_node.getBounds().getRadius()
        scene_center = self.center.getPos()
        base.cam.setPos(scene_center[0], -10-scene_center[1]-2*ligand_radius-2*receptor_radius, scene_center[2])
        base.cam.lookAt(self.center)  
        
        
    def help_on_screen(self):
        ''' Show commands on screen '''
        self.help = not self.help
        if self.help:
            i = 0
            for instruction in Dockit.instructions:
                self.text_on_screen.append(self.__gen_label_text(instruction,i))
                i += 1
        else:
            for text in self.text_on_screen:
                text.destroy()
            del self.text_on_screen[:]
    
    
    def __gen_label_text(self, text, i):
        ''' Auxiliar function to display text line by line '''
        return OnscreenText(text = text, pos = (-1.6, .9-.06*i), fg=(1,1,1,1),
                       align = TextNode.ALeft, scale=0.06, mayChange = 0)
    
