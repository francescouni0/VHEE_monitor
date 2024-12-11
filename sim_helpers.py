import opengate as gate
from opengate.geometry.volumes import RepeatParametrisedVolume, BoxVolume
from opengate.actors.digitizers import *
def add_collimator_he(sim, head, debug):
    name = head.name
    mm = gate.g4_units.mm
  
    """gate.fatal(
        f"the Intevo HE collimator is not implemented yet. Need to move the shielding ..."
    )"""

    colli = sim.add_volume("Box", f"{name}_he_collimator")
    colli.mother = name
    colli.size = [82.5 * mm, 120 * mm, 350 * mm]
    colli.translation = [130 * mm, 0, 0]
    colli.color  = [0.5, 0.5, 0.5, 1]
    colli.material = "Lead"
    shield = sim.add_volume("Box", f"{name}_he_shield")
    shield.mother = name
    shield.size = [30 * mm, 120 * mm, 350 * mm]
    shield.translation = [186.25 * mm, 0, 0]
    shield.color = [1, 0.5, 0.5, 1]
    shield.material = "Lead"
    

    """
    #########################################################################
    #
    # 	Type	|	Diameter	|	Septial thickness	|	No. of holes
    # -----------------------------------------------------------------------
    # 	hex		|	4.0 mm		|	2.0 mm 				|	8000
    #
    #	y spacing	= diameter + septial = 6.0 mm
    #	z spacing	= 2 * (diameter + septial) * sin(60) = 10.39230485 mm
    #
    #	y translation	= y spacing / 2 = 3.0 mm
    #	z translation	= z spacing / 2 = 5.196152423 mm
    #
    # 	(this translation from 0,0 is split between hole1 and hole2)
    #
    #	Nholes y	= (No. of holes / sin(60))^0.5 = 96.11245657
    #	Nholes z	= (No. of holes * sin(60))^0.5 = 83.23582901
    #
    #########################################################################
    """

    # hexagon
    #hole = sim.add_volume("Hexagon", f"{name}_collimator_hole1")
    #hole.height = 80 * mm
    #hole.radius = 2.0 * mm
    #hole.material = "G4_AIR"
    #hole.mother = colli.name
    
    
    #square
    #grandezza effettiva
    hole = sim.add_volume("Box", f"{name}_collimator_hole2")
    hole.size = [2.5 * mm, 2.5* mm, 82.5 * mm]
    hole.material = "G4_AIR"
    hole.mother = colli.name
    
    
    # parameterised holes
    size = [1, 24, 60]
     #traslazione tra coppie di buchi (distanza dal centro)
    tr = [0, 5 * mm, 5 * mm, 0]
    rot = Rotation.from_euler("y", 90, degrees=True).as_matrix()
    #implementa offset diagonale
    offset = [0, -1.5*2 * mm * 2, -2.598076212*2 * mm * 2, 0]
    start= [-(x - 1) * y / 2.0 for x, y in zip(size, tr)]
    repeat_colli_hole(sim, hole, size, tr, rot,start, offset)
    
    

    
    

    return colli




def repeat_colli_hole(sim, hole, size, tr, rot,start, offset):
    holep = RepeatParametrisedVolume(repeated_volume=hole)
    holep.linear_repeat = size
    holep.translation = tr[0:3]
    holep.rotation = rot
    holep.start = start
    # do it twice, with the following offset se 1 no offset
    holep.offset_nb = 1
    holep.offset = offset
    sim.volume_manager.add_volume(holep)
    return holep
