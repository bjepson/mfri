#!/usr/bin/env python

from mayavi import mlab
from tvtk.api import tvtk
from PIL import Image
import numpy as np
import argparse

def save_to_image(fig, filename):

    # Take a screenshot the current image with a transparent background
    img_map = mlab.screenshot(figure=fig, mode='rgba', antialiased=True)

    # Save the screenshjot as a file
    img = Image.fromarray(np.array(img_map * 255, dtype=np.uint8))

    # Crop the image to remove excess background
    img = img.crop(img.getbbox())
    img.save(filename)

if __name__ == "__main__":

    args = argparse.ArgumentParser()
    args.add_argument("--stl", type=str,
                      help="Path to the STL file", required=True)
    args.add_argument("--color", nargs=3, type=int,
                      help="Color of the mesh in RGB format (0-255)", 
                      default=[237,28,36])
    args = args.parse_args()

    mlab.options.offscreen = True  # Enable offscreen rendering

    # Read the STL file
    reader = tvtk.STLReader(file_name=args.stl)
    reader.update()

    # Visualize the mesh in red
    data = reader.output
    fig = mlab.figure(size=(800, 800))
    color = tuple(round(c/255,2) for c in (args.color))
    mlab.pipeline.surface(mlab.pipeline.add_dataset(data), 
                          color=color)

    # Render the robot from different angles and save the images
    mlab.view(azimuth=-45, elevation=90, distance=80, focalpoint=(0, 0, 0))
    save_to_image(fig, "rendered_left.png")

    mlab.view(azimuth=-135, elevation=90, distance=80, focalpoint=(0, 0, 0))
    save_to_image(fig, "rendered_right.png")

    mlab.view(azimuth=-100, elevation=90, distance=80, focalpoint=(0, 0, 0))
    save_to_image(fig, "rendered_front.png")

    mlab.close(fig)

