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
output_folder = Path('/media/francesco/HP P500/francesco/traindataset')

a=[]

for i in range(50, 250):
    f_d_edep = output_folder / f"dose3d_{i}.0_dose.mhd"
    d_edep = sitk.GetArrayFromImage(sitk.ReadImage(str(f_d_edep))).reshape(-1)

    n = len(d_edep)
    x = np.linspace(0, n, n)
    y = d_edep

    histdose, _ = np.histogram(x, weights=y, bins=50)
    histdose = (histdose / np.max(histdose)) * 100

    f = uproot.open(f"/media/francesco/HP P500/francesco/traindataset/phase_space{i}.0.root")
    ph = f['PhaseSpace']
    pre_dir = ph.arrays(['PreDirection_X','PreDirection_Y','PreDirection_Z'])
    pre_dir_x = np.array(pre_dir['PreDirection_X'])
    pre_dir_y = np.array(pre_dir['PreDirection_Y'])
    pre_dir_z = np.array(pre_dir['PreDirection_Z'])

    angle_with_z = np.arccos(pre_dir_z / np.linalg.norm([pre_dir_x, pre_dir_y, pre_dir_z], axis=0)) * 180 / np.pi
    angle_mask = np.logical_and(angle_with_z > 88, angle_with_z < 92)
    filtered_ppz_angle = np.array(ph['PostPosition_Z'].array())[angle_mask]
    filtered_ppy_angle = np.array(ph['PostPosition_Y'].array())[angle_mask]

    h, xedges, yedges = np.histogram2d(filtered_ppz_angle, filtered_ppy_angle, bins=(50, 1),
                                       range=[[-149, 149], [-58, 58]])
    h = h.reshape((50))
    histgamma = (h / np.max(h)) * 100
    ar_i=np.array([i])
    ar_i = np.full(50, i)
    row_data = np.vstack((histdose,ar_i, histgamma)).T
    if i == 50:
        a = row_data
    else:
        a = np.vstack((a, row_data))
        

print(np.shape(a))
with open("dataset_matr.txt", "w") as f:
    np.savetxt(f, a, fmt="%f")
#z=np.linspace(-150, 150, 50)
#
#plt.plot(z, a[:50, 0], label='dose',color='green')
#plt.plot(z,a[:50, 2], label='gamma',color='blue')
#plt.show()