import opengate as gate
from sim_helpers import *
import uproot


if __name__ == "__main__":
    #import opengate_core as gate_core
    #am = gate_core.GateDigiAttributeManager.GetInstance()
    #print(am.GetAvailableDigiAttributeNames())
    sim = gate.Simulation()

    sim.verbose_level = gate.logger.DEBUG
    sim.running_verbose_level = gate.logger.RUN
    sim.g4_verbose = False
    sim.g4_verbose_level = 1
    sim.visu = False
    sim.visu_type = "vrml_file_only"
    sim.visu_filename="gate_visu.wrl"
    sim.random_engine = "MersenneTwister"
    sim.random_seed = "auto"
    sim.output_dir = "output"
    sim.number_of_threads = 1

    sim.progress_bar = True

    print(sim)



    m = gate.g4_units.m
    cm = gate.g4_units.cm
    cm3 = gate.g4_units.cm3
    keV = gate.g4_units.keV
    MeV = gate.g4_units.MeV
    mm = gate.g4_units.mm
    Bq = gate.g4_units.Bq
    gcm3 = gate.g4_units.g / cm3
    s=gate.g4_units.s



    world = sim.world
    world.size = [1 * m, 1 * m, 1 * m]
    world.material = "G4_AIR"
    
    sim.volume_manager.material_database.add_material_nb_atoms(
        "BGO", ["Bi", "Ge", "O"], [4, 3, 12], 7.13 * gcm3
    )
    
    sim.volume_manager.material_database.add_material_nb_atoms( "G4_PLEXIGLASS  ", 
        ["C", "H", "O"], [5, 8, 2], 1.19 * gcm3
    )
    
    
    #BOX
    pmmacyl = sim.add_volume("Box", "pmmacyl")
    pmmacyl.size = [3 * cm, 3 * cm, 5 * cm]
    pmmacyl.translation = [0 * cm, 0 * cm, 0 * cm]
    pmmacyl.material = "G4_PLEXIGLASS  "
    pmmacyl.color = [-5, 0, 1, 1]  # this is RGBa (a=alpha=opacity), so blue here
    
    sim.physics_manager.physics_list_name =  "QGSP_BERT_HP_EM0"
    sim.physics_manager.enable_decay = True
    
    
    source = sim.add_source('GenericSource', 'Default')
    source.half_life = 1218 * gate.g4_units.s
    source.activity=60*gate.g4_units.Bq
    source.particle = 'e+'
    source.energy.type = 'C11'  # F18 or Ga68 or C11 ...    
    source.position.type = "box"
    source.position.size = [3 * cm, 3 * cm, 5 * cm]
    ##source.position.translation = [8 * cm, 8 * cm, 30 * cm]
    source.direction.type = "iso"
    #starting_activity = 1
    #half_life = 1218 
    #times = np.linspace(0, 3000, num=2, endpoint=True) 
    #decay = np.log(2) / half_life
    #activities = [starting_activity * np.exp(-decay * t) for t in times]
    #source.tac_times = times
    #source.tac_activities = activities
    print(source.tac_activities)

    stats = sim.add_actor("SimulationStatisticsActor", "stats")
    stats.track_types_flag = True
    stats.output_filename = "stats.txt"
    
    
    # create detector
    crystal = sim.add_volume("Box", "crystal")
    crystal.size = [20 * mm, 20* mm, 15 * mm]
    crystal.material = "BGO"
    crystal.mother = "world"
    crystal.translation = ([-25*mm, 0, 10*mm],[25*mm, 0, 10*mm])
    crystal.color = [1, 0.65, 0, 1]  # this is RGBa (a=alpha=opacity), so orange here

    hc = sim.add_actor("DigitizerHitsCollectionActor", "Hits")
    hc.attached_to = crystal.name
    hc.authorize_repeated_volumes = True
    hc.output_filename = f"Hits.root"
    hc.attributes = [
        "PostPosition",
        "TotalEnergyDeposit",
        "PreStepUniqueVolumeID",
        "GlobalTime",
    ]
    sc = sim.add_actor("DigitizerReadoutActor", "Singles")
    sc.authorize_repeated_volumes = True
    sc.output_filename = f"Singles.root"
    sc.input_digi_collection = "Hits"
    sc.discretize_volume = crystal.name
    sc.policy = "EnergyWeightedCentroidPosition"
 
    sim.run_timing_intervals =[ [0*s,3000*s]]
    sim.run()
