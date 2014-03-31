DockIt!
=======

DockIt uses Panda3D game engine (https://www.panda3d.org/) to display two proteins, a receptor and a ligand, and lets the user move one of the proteins to try to dock it on the other.
I developed this prototype as a side project for my thesis.

Steps to use it
---------------

1. Download panda3d game engine and make sure 'panda3d' is in your PYTHONPATH.
2. Execute: python main.py pdb_data/1PPE_r_u.pdb pdb_data/1PPE_l_u.pdb (pdb_data contains two example PDB structures)

Controlling the protein
-----------------------

* X-axis: a/d
* Y-axis: w/s
* Z-axis: q/e
* Heading: r/f
* Pitch: t/g
* Roll: h/y
* Cartoon mode: c
* Show control structures: x
* Center proteins: z
* Help: v
* Exit: escape


Screenshots
-----------

![DockIt](/media/dockit_1.png)
![DockIt](/media/dockit_2.png)
