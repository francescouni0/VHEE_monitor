import opengate as gate
from sim_helpers import *
import random
import argparse


# this first line is required at the beginning of all scripts
if __name__ == "__main__":
    """
    Create a simulation object. The class is 'gate.Simulation'.
    The single object that will contain all parameters of the simulation is called 'sim' here.
    """
    sim = gate.Simulation()

    """
    Main global options.
    The 'sim' object contains a structure called 'user_info' that gather all global options.
    For shorter coding, we call it 'ui'
    - the verbosity means : texts that are displayed during the simulation run (mostly for debug
    - 'visu', if ON, display a windows with a 3D view of the scene.
    - random_engine and random_seed control the pseudo random engine. We recommend MersenneTwister.
      A seed can be specified, e.g. 123456, for reproducible simulation. Or you can use 'auto', an random seed
      will be generated.
    """
    sim.verbose_level = gate.logger.DEBUG
    sim.running_verbose_level = gate.logger.RUN
    sim.g4_verbose = False
    sim.g4_verbose_level = 1
    sim.visu = False
    sim.visu_type = "vrml_file_only"
    sim.visu_filename="gate_visu.wrl"
    sim.random_engine = "MersenneTwister"
    sim.random_seed = "auto"
    sim.output_dir = "/home/francesco/gate/VHEE_monitor/output"
    sim.number_of_threads = 1

    sim.progress_bar = True

    print(sim)

    """
    Units. Get some default units from G4. To define a value with a unit, e.g. do:
    x = 123 * cm
    """
    m = gate.g4_units.m
    cm = gate.g4_units.cm
    cm3 = gate.g4_units.cm3
    keV = gate.g4_units.keV
    MeV = gate.g4_units.MeV
    mm = gate.g4_units.mm
    Bq = gate.g4_units.Bq
    gcm3 = gate.g4_units.g / cm3

    """
    Set the world size (like in the Gate macro). World is the only volume created by default.
    It is described by a dict-like structure, accessible by sim.world.
    The size is set as a 3D vector. Default material is G4_AIR.
    """
    world = sim.world
    world.size = [1 * m, 1 * m, 1 * m]
    world.material = "G4_AIR"
    

    """
    A simple water box volume is created. It is inserted into the simulation with 'add_volume'.
    This function return a dict-like structure (called 'pmmacyl' here) with various parameters
    (size, position in the world, material). Note that, like in Geant4, the coordinate system
    of all volumes is the one of the mother volume (here the world).
    """
    
    # create the material lead
    sim.volume_manager.material_database.add_material_nb_atoms( "G4_PLEXIGLASS  ", 
        ["C", "H", "O"], [5, 8, 2], 1.19 * gcm3
    )
    
    sim.volume_manager.material_database.add_material_nb_atoms(
        "Lead", ["Pb"], [1], 11.4 * gcm3
    )
    sim.volume_manager.material_database.add_material_nb_atoms(
        "BGO", ["Bi", "Ge", "O"], [4, 3, 12], 7.13 * gcm3
    )
    #CYLINDER
    pmmacyl = sim.add_volume("TubsVolume", "pmmacyl")
    pmmacyl.rmin = 0
    pmmacyl.rmax = 12 * cm
    pmmacyl.dz = 15 * cm
    pmmacyl.translation = [0 * cm, 0 * cm, 0 * cm]
    pmmacyl.material = "G4_PLEXIGLASS  "
    pmmacyl.color = [-5, 0, 1, 1]
    
    #INSERT

    #insert = sim.add_volume("TubsVolume", "pmmacyl_insert")
    #insert.mother = "pmmacyl"
    #insert.rmin = 0
    #insert.rmax = 6 * cm
    #insert.dz = 0 * cm
##
    ### Place insert at random Z within cylinder
    ##half_dz = (pmmacyl.dz - insert.dz) / 2
    ##random_z = random.uniform(-half_dz, half_dz)
    #insert.translation = [0, 0, 35*mm]
##
    #insert.material = "G4_AIR"  #"G4_LUNG_ICRP"
    #insert.color = [1, 0, 0, 1]
    
    #BOX
    #pmmacyl = sim.add_volume("Box", "pmmacyl")
    #pmmacyl.size = [20 * cm, 20 * cm, 30 * cm]
    #pmmacyl.translation = [0 * cm, 0 * cm, 0 * cm]
    #pmmacyl.material = "G4_PLEXIGLASS  "
    #pmmacyl.color = [-5, 0, 1, 1]  # this is RGBa (a=alpha=opacity), so blue here
    
    
    
    #colli=add_collimator_he(sim, world, False)


    #sim.add_parallel_world("parallel_world")
    # create detector
    #crystal = sim.add_volume("Box", "crystal")
    #crystal.size = [3 * mm, 3* mm, 2.5 * mm]
    #crystal.material = "BGO"
    #crystal.mother = "parallel_world"
    #crystal.translation = [-200*mm, 0, 0]
#
    #crystal.color = [0, 1, 0, 1]  # this is RGBa (a=alpha=opacity), so green here
    #
    #    # parameterised crystals
    #size = [1, 20, 30]
    # #traslazione tra coppie di buchi (distanza dal centro)
    #tr_cry = [0, 10 * mm, 10 * mm, 0]
    #rot_cry = Rotation.from_euler("y", 90, degrees=True).as_matrix()
    #start_cry = [-(x - 1) * y / 2.0 for x, y in zip(size, tr_cry)]
    #start_cry[0] = +271.25 * mm
#
    ##implementa offset diagonale
    #offset_cry = [0, -1.5*2 * mm * 2, -2.598076212*2 * mm * 2, 0]
    #repeat_colli_hole(sim, crystal, size, tr_cry, rot_cry,start_cry, offset_cry)

    

    #CREATE COLLIMATOR



    # another other volume
    #myobject = sim.add_volume("Box", "lead_box")
    #myobject.mother = "pmmacyl"
    #myobject.size = [3 * cm, 3 * cm, 3 * cm]
    #myobject.translation = [2 * cm, 2 * cm, 3 * cm]
    #myobject.material = "Lead"
    #myobject.color = [1, 1, 0, 1]  # this is RGBa (a=alpha=opacity), so yellow here

    
    """
    The physic list and production cuts
    """
    sim.physics_manager.physics_list_name =  "QGSP_BERT_HP_EM0"       #"G4EmStandardPhysics_option1"
    sim.physics_manager.set_production_cut("world", "gamma", 1 * mm)
    sim.physics_manager.set_production_cut("world", "electron", 1 * mm)
    sim.physics_manager.set_production_cut("world", "positron", 1 * mm)
    sim.physics_manager.set_production_cut("world", "proton", 1 * mm)
    sim.physics_manager.set_production_cut("pmmacyl", "gamma", 15 * mm)
    sim.physics_manager.set_production_cut("pmmacyl", "electron", 5 * mm)
    sim.physics_manager.set_production_cut("pmmacyl", "positron", 10 * mm)
    sim.physics_manager.set_production_cut("pmmacyl", "proton", 10 * mm)
    #sim.physics_manager.set_production_cut("world_he_collimator", "gamma", 0.02* mm)


   



    """
    A source of particles. The shoot gammas are 1 MeV, emitted from a 10 mm disc
    and are focused towards a point located at 20 cm.   
    """
    source = sim.add_source("GenericSource", "mysource")
    source.particle = "e-"
    parser = argparse.ArgumentParser()
    parser.add_argument('--energy', type=float, default=150, help='Energy in MeV')
    args = parser.parse_args()

    source.energy.mono = args.energy * MeV
    source.position.type = "disc"
    source.position.radius = 4 * mm
    source.position.translation = [0, 0, -50 * cm]
    source.direction.type = "momentum"
    source.direction.momentum = [0, 0, 1]
    source.n = 10000
    """
    Add a single scorer (called 'actor'), of type 'SimulationStatisticsActor'.
    This simple scorer stores the number or Run/Events/Track/Steps of the simulation.
    We recommend to always add such actor.
    The flag 'track_types_flag' gives more detailed results about the tracks (particle type)
    """
    stats = sim.add_actor("SimulationStatisticsActor", "stats")
    stats.track_types_flag = True
    stats.output_filename = "stats.txt"

    """
    # Optional : verbose
    sim.visu = False
    sim.g4_verbose = True
    sim.g4_verbose_level = 1
    sim.add_g4_command_after_init("/tracking/verbose 2")
    """
      # dose actor 1: depth edep
    # dose actor 1: depth edep
    
    #if source.n >=99999:
    #depth_dose = sim.add_actor("DoseActor", "dose")
    #depth_dose.attached_to = "pmmacyl"
    #depth_dose.output_filename = f"dose3d_{args.energy}.mhd"
    #depth_dose.spacing = [120 * mm, 120 * mm, 1 * mm]
    #depth_dose.size = [1, 1, 300]
    #depth_dose.dose.active = True
    #depth_dose.dose_uncertainty.active = True
    #    
#
    #
    #
    #    # dose actor 2: edep profile
    #    lateral_edep = sim.add_actor("DoseActor", "lateral_edep")
    #    lateral_edep.attached_to = "pmmacyl"
    #    lateral_edep.output_filename = "doselat.mhd"
    #    lateral_edep.spacing = [0.5 * mm, 40 * cm, 40 * cm]
    #    lateral_edep.size = [100, 1, 1]
    #    lateral_edep.edep_uncertainty.active = True
        

        
    #hc = sim.add_actor("DigitizerHitsCollectionActor", f"Hits_{crystal.name}")
    #hc.attached_to = crystal.name
    #hc.output_filename = "spect_data.root"
    #hc.attributes = [
    #    "PostPosition",
    #    "PreKineticEnergy",
    #    "TotalEnergyDeposit",
    #    "PreDirection",
    #    'PreStepUniqueVolumeID',
    #    'GlobalTime']
    #
    #sc = sim.add_actor("DigitizerAdderActor", "Singles")
    #sc.output_filename = 'spect_hits.root'
    #sc.input_digi_collection = "Hits_crystal"
    #sc.policy = "EnergyWeightedCentroidPosition"
    ## sc.policy = "EnergyWinnerPosition"
    #sc.group_volume = crystal.name
        
    #ps= sim.add_actor("PhaseSpaceActor", "PhaseSpace")
    #ps.output_filename = f"phase_space{args.energy}.root"
    #ps.attached_to = "pmmacyl"
    #ps.steps_to_store = " exiting "
    #ps.attributes = [
    #"KineticEnergy",
    #"PostPosition",
    #"PrePosition",
    #"PreDirection",
    #"EventPosition",
    #]
    #f = sim.add_filter("ParticleFilter", "f")
    #f.particle = "gamma"
    #ps.filters.append(f)
    
    
    hc = sim.add_actor("DigitizerHitsCollectionActor", f"Hits_{crystal.name}")
    hc.attached_to = crystal.name
    hc.output_filename = "spect_data.root"
    hc.attributes = [
        "PostPosition",
        "PreKineticEnergy",
        "TotalEnergyDeposit",
        "PreDirection",
        'PreStepUniqueVolumeID',
        'GlobalTime']
    
    
    c11 = sim.add_actor("DigitizerAdderActor", "HitsC11")
    c11.attached_to = pmmacyl
    
    c11.output_filename = "C11.root"
    c11.attributes = [
        "PostPosition"]
    c11.policy = "EnergyWinnerPosition"
    fil=sim.add_filter("ParticleFilter", "f")
    fil.particle = "e+"
    c11.filters.append(fil)
    
    
        

    
    """
    Start the simulation ! You can relax and drink coffee.
    """
    sim.run()

    """
    Now the simulation is terminated. The results can be displayed.
    """    
    print(stats)
    
    
    
