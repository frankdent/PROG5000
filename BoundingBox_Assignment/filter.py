'''
Command line application that will determine whether points are inside
a bounding box
'''

__author__ = "François d'Entremont"

import os
import argparse

from pyproj.crs import CRS

import bbox

parser = argparse.ArgumentParser(
    description='Parse bounding box arguments: identifier and filename')
# An argument for the identifier of the box that will be used
parser.add_argument('identifier', type=str,
                    help='The name of the bounding box')
# An argument for the filename that will be used
parser.add_argument('file_pts', type=str,
                    help='The name of the file containing the points' +
                    'including the extension')
# Parse the arguments
args = parser.parse_args()
identifier = args.identifier
file_pts = args.file_pts

# strip the file extension from the string
file_pts_strip = os.path.splitext(file_pts)[0]

# bbox_file stores the filename (without the extension) of the csv and proj
# files containing the information for the bounding boxes. They should have
# the same name with different extensions and be stored in the same directory
# as the filter.py file.
bbox_file = 'bounds'

# This will throw an error if a file or identifier could not be found.
try:
    # Open the points prj file, extract the coordinates and crs.
    with (open(f'{file_pts_strip}.prj', 'r') as prj_file):
        crs_from_file = prj_file.read()
    points_crs = CRS.from_wkt(crs_from_file)

    # Create a bounding box object from bbox_file using the chosen identifier.
    box = bbox.BoundingBox.bb_from_csv(f'{bbox_file}', identifier)

    # Transform the bounding box object into the same coordinate system as the
    # points data.
    box_transform = box.transform_to(points_crs)

    # Print the output
    print(box_transform.pts_in_bbox(file_pts_strip))
except:
    print('File or identifier could not be found')
