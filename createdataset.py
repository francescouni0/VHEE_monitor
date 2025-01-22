import matplotlib.pyplot as plt
import seaborn as sns
import hyperspy.api as hs

# Module with scientific computing functions (matrix/vector)
import numpy as np                

# Modules with reading/write folder/file functions
import os
from pathlib import Path
import SimpleITK as sitk

# module to deal with images
import uproot

# The following command display the current working directory (where jupyter has been launched)
cwd = os.getcwd()
folder = Path()

# Display the content of a folder
output_folder = Path('./output')


for i in range(100, 103):
    f_d_edep = output_folder / f"dose3d_{i}.0_dose.mhd"
    d_edep = sitk.GetArrayFromImage(sitk.ReadImage(str(f_d_edep))).reshape(-1)

    n = len(d_edep)
    x = np.linspace(0, n, n)
    y = d_edep
    plt.scatter(x, y, color='green', label='Dose')
    plt.show()

    histdose, bin_edges = np.histogram(x, weights=y, bins=50)
    histdose = (histdose / np.max(histdose)) * 100
    bin_edges = np.linspace(-150, 150, len(bin_edges))
    plt.plot(bin_edges[1:], histdose, color='green', label='Dose')
    plt.legend()
    plt.show()

    f = uproot.open(f"output/phase_space{i}.0.root")
    ph = f['PhaseSpace']
    ppx = ph['PostPosition_X'].array()
    ppy = ph['PostPosition_Y'].array()
    ppz = ph['PostPosition_Z'].array()
    pre_dir_x = np.array(ph.arrays()['PreDirection_X'])
    pre_dir_y = np.array(ph.arrays()['PreDirection_Y'])
    pre_dir_z = np.array(ph.arrays()['PreDirection_Z'])

    angle_with_z = np.arccos(pre_dir_z / np.linalg.norm([pre_dir_x, pre_dir_y, pre_dir_z], axis=0)) * 180 / np.pi
    ppz = np.array(ppz)
    ppy = np.array(ppy)
    ppx = np.array(ppx)
    angle_mask = np.logical_and(angle_with_z > 88, angle_with_z < 92)
    filtered_ppz_angle = ppz[angle_mask]
    filtered_ppy_angle = ppy[angle_mask]
    filtered_ppx_angle = ppx[angle_mask]

    h, xedges, yedges = np.histogram2d(filtered_ppz_angle, filtered_ppy_angle, bins=(50, 1), range=[[-149, 149], [-58, 58]])
    h = np.reshape(h, (50))
    histgamma = (h / np.max(h)) * 100
    bin_edges_g = np.linspace(-150, 150, len(xedges))
    plt.plot(bin_edges_g[1:], histgamma, color='blue', label='gamma')
    plt.legend()
    plt.show()
