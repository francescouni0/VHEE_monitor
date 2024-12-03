#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path
import importlib
import requests
from tqdm import tqdm
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# plot capabilities
import matplotlib.pyplot as plt
from ipywidgets import interact
from matplotlib.cm import ScalarMappable

# scientific computing functions (matrix/vector)
import numpy as np

# module to deal with images
import SimpleITK as sitk


def resample_image_like(img, like_img, default_pixel_value=-1000, linear=True):
    # Create a resampler object
    resampler = sitk.ResampleImageFilter()

    # Set the resampler parameters from img1
    resampler.SetSize(like_img.GetSize())
    resampler.SetOutputSpacing(like_img.GetSpacing())
    resampler.SetOutputOrigin(like_img.GetOrigin())
    resampler.SetOutputDirection(like_img.GetDirection())
    resampler.SetDefaultPixelValue(default_pixel_value)

    # Use the identity transform - we only resample in place
    resampler.SetTransform(sitk.Transform())

    # Set the interpolation method to Linear
    if linear:
        resampler.SetInterpolator(sitk.sitkLinear)

    # Execute the resampling
    resampled_img = resampler.Execute(img)

    return resampled_img


def show_itk_3d_image(image, **kwargs):
    npa = sitk.GetArrayViewFromImage(image)
    if "image2" in kwargs:
        kwargs["image2"] = sitk.GetArrayFromImage(kwargs["image2"])
    show_nparray_3d_image(npa, **kwargs)


"""
import importlib
import exercices_helpers
importlib.reload(exercices_helpers)
from exercices_helpers import *
"""


def show_nparray_3d_image(
    image,
    image2=None,
    rot90=(0, 0, 0),
    figsize=(8, 5),
    opacity=1,
    threshold=0.001,
):
    fig, ax = plt.subplots(1, 3, figsize=figsize)
    starting_slices = np.array(image.shape) / 2

    def show_img(sx=starting_slices[1], sy=starting_slices[2], sz=starting_slices[0]):
        ax[0].imshow(np.rot90(image[:, sx, :], rot90[0]), cmap=plt.cm.gray)
        ax[1].imshow(np.rot90(image[:, :, sy], rot90[1]), cmap=plt.cm.gray)
        ax[2].imshow(np.rot90(image[sz, :, :], rot90[2]), cmap=plt.cm.gray)

    def show_img_fusion(
        sx=starting_slices[1],
        sy=starting_slices[2],
        sz=starting_slices[0],
        opacity=opacity,
    ):
        show_img(sx, sy, sz)
        a = np.rot90(image2[:, sx, :], rot90[0])
        b = np.ma.masked_where(a <= threshold, a)
        ax[0].imshow(b, alpha=opacity, cmap=plt.cm.hot)
        a = np.rot90(image2[:, :, sy], rot90[1])
        b = np.ma.masked_where(a <= threshold, a)
        ax[1].imshow(b, alpha=opacity, cmap=plt.cm.hot)
        a = np.rot90(image2[sz, :, :], rot90[2])
        b = np.ma.masked_where(a <= threshold, a)
        ax[2].imshow(b, alpha=opacity, cmap=plt.cm.hot)

    # color scale
    vmin = np.min(image)
    vmax = np.max(image)
    sm = ScalarMappable(cmap=plt.cm.gray, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = plt.colorbar(sm, ax=ax, location="left")
    cbar.set_label("Image")

    if image2 is not None:
        # color scale
        vmin = np.min(image2)
        vmax = np.max(image2)
        sm = ScalarMappable(cmap=plt.cm.hot, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        cbar = plt.colorbar(sm, ax=ax, location="right")
        cbar.set_label("Fusion")
        interact(
            show_img_fusion,
            sx=(0, image.shape[1] - 1),
            sy=(0, image.shape[2] - 1),
            sz=(0, image.shape[0] - 1),
            opacity=(0, 1, 0.1),
        )
    else:
        interact(
            show_img,
            sx=(0, image.shape[1] - 1),
            sy=(0, image.shape[2] - 1),
            sz=(0, image.shape[0] - 1),
        )


def download_file(url, local_filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(
        total=total_size, unit="B", unit_scale=True, desc=local_filename, ncols=80
    )

    os.makedirs(os.path.dirname(local_filename), exist_ok=True)

    temp_filename = local_filename + ".part"
    with open(temp_filename, "wb") as temp_file:
        for data in response.iter_content(chunk_size=block_size):
            progress_bar.update(len(data))
            temp_file.write(data)

    progress_bar.close()
    # Move the temporary file to the final location if download is successful
    os.rename(temp_filename, local_filename)


def parse_directory_listing(directory_url):
    response = requests.get(directory_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract file names from the HTML content
    file_links = soup.find_all("a", href=True)

    # Filter out unwanted entries
    files = [link["href"] for link in file_links if not link["href"].startswith("?")]
    files = [f for f in files if "~" not in f]

    return files


def sync_from_remote_url_recursive(remote_url, local_base_directory, relative_path=""):
    remote_files = parse_directory_listing(remote_url)

    for remote_file in remote_files:
        remote_file_url = urljoin(remote_url, remote_file)
        local_file_path = os.path.join(
            local_base_directory, relative_path, os.path.basename(remote_file)
        )

        if remote_file.endswith("/"):
            # It's a directory, create it locally and recurse into it
            os.makedirs(local_file_path, exist_ok=True)
            sync_from_remote_url_recursive(
                remote_file_url,
                local_base_directory,
                os.path.join(relative_path, remote_file),
            )
        else:
            # It's a file, download it if it doesn't exist locally
            if not os.path.exists(local_file_path):
                download_file(remote_file_url, local_file_path)
                print(f"Downloaded {local_file_path}")
            # else:
            #    print(f"Skipping {remote_file_url} as it already exists locally")
