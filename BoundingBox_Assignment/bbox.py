'''
Defining a class for a bounding box.
'''

__author__ = "François d'Entremont"

from os import environ

environ['PROJ_LIB'
        ] = r'C:\Users\w0483484\.conda\envs\prog5000\Library\share\proj'

from pyproj import Transformer
from pyproj.crs import CRS
import csv


class BoundingBox:
    """
        A class to represent a bounding box.

        Attributes
        ----------
            id : str
                The name of the bounding box
            min_axis_0 : float
                the minimum value for axis 0
            min_axis_1 : float
                The minimum value for axis 1
            max_axis_0 : float
                The maximum value for axis 0
            max_axis_1 : float
                The maximum value for axis 1
            crs : CRS
                The coordinate reference system (CRS) as a pyproj CRS object
    """

    def __init__(self, id: str, min_axis_0: float, min_axis_1: float,
                 max_axis_0: float, max_axis_1: float, crs: CRS):
        """
        Constructs all the necessary attributes for the bounding box object.

        Parameters
        ----------
            id : str
                The name of the bounding box
            min_axis_0 : float
                The minimum value for axis 0
            min_axis_1 : float
                The minimum value for axis 1
            max_axis_0 : float
                The maximum value for axis 0
            max_axis_1 : float
                The maximum value for axis 1
            crs : CRS
                The coordinate reference system (CRS) as a pyproj CRS object
        """
        self._id: str = id
        self._min_axis_0: float = min_axis_0
        self._min_axis_1: float = min_axis_1
        self._max_axis_0: float = max_axis_0
        self._max_axis_1: float = max_axis_1
        self._crs = crs

    @classmethod
    def bb_from_csv(cls, file_name: str, id: str):
        """This class method is used to create a bounding box from a csv and 
        proj file of the same name. The min and max values and crs are
        extracted and a bounding box is returned.

        Parameters
        ----------
            file_name: str
                The name of the file containing the bounding boxes without the
                extension
            id: str
                The name of the bounding box
        """
        with (open(f'{file_name}.csv', 'r') as open_csv,
              open(f'{file_name}.prj', 'r') as prj_file):
            reader = csv.reader(open_csv)
            next(reader)
            for row in reader:
                if id == row[0]:
                    min_axis_0, min_axis_1, max_axis_0, max_axis_1 = row[1], \
                        row[2], row[3], row[4]
                    break
            crs_from_file = prj_file.read()
            crs_from_file = CRS.from_wkt(crs_from_file)
            return cls(id, min_axis_0, min_axis_1, max_axis_0, max_axis_1,
                       crs_from_file)

    def transform_to(self, new_crs: CRS):
        """This function takes a bounding box and returns a bounding box
        with coordinates transformed to a new crs. The coordinate axis order
        from the crs will be respected in order to match the csv file order.

        Parameters
        ----------
            new_crs: CRS
                The coordinate reference system (CRS) of the new CRS as a
                pyproj CRS object
        """
        t = Transformer.from_crs(self._crs, new_crs)
        self._min_axis_0, self._min_axis_1 = t.transform(self._min_axis_0,
                                                         self._min_axis_1)
        self._max_axis_0, self._max_axis_1 = t.transform(self._max_axis_0,
                                                         self._max_axis_1)
        self._crs = new_crs
        return BoundingBox(self._id, self._min_axis_0, self._min_axis_1,
                           self._max_axis_0, self._max_axis_1, new_crs)

    def contains(self, x: float, y: float):
        """This function checks to see if a coordinate is inside the bounding
        box object and returns a boolean True or False

        Parameters
        ----------
            x: float
                The x-coordinate
            y: float
                The y-coordinate
        """
        if float(self._min_axis_0) <= x <= float(self._max_axis_0) and \
                float(self._min_axis_1) <= y <= float(self._max_axis_1):
            return True
        else:
            return False

    def pts_in_bbox(self, file_pts_strip: str):
        """This function returns a line of text for each point inside the box.
        The csv and proj files are read, the coordinates and crs are
        extracted, and a check is made on each point to see if they are within
        the bounds.

        Parameters
        ----------
            file_pts_strip: str
                The name of the file containing the points data without the
                extension
        """
        with (open(f'{file_pts_strip}.csv', 'r') as csv_points,
              open(f'{file_pts_strip}.prj', 'r') as prj_file):
            crs_from_file = prj_file.read()
            crs_from_file = CRS.from_wkt(crs_from_file)
            points_data = []
            csv_reader = csv.reader(csv_points)
            for row in csv_reader:
                points_data.append((row[0], row[1], row[2]))
            console_out = ""
            for i in points_data:
                if self._min_axis_0 <= float(i[0]) <= self._max_axis_0 and \
                        self._min_axis_1 <= float(i[1]) <= self._max_axis_1:
                    console_out += f'Bounding box {self._id} ' + \
                        f'contains {i[2]}\n'
            return console_out

    def __str__(self) -> str:
        """This function returns a string representation of the object when
        the bounding box object is converted into a string.
        """
        return f'BBOX: [id: {self._id}, min_axis_1: {self._min_axis_0}, ' + \
            f'min_axis_0: {self._min_axis_1}, max_axis_1: ' + \
            f'{self._max_axis_0}, max_axis_0: {self._max_axis_1}, ' + \
            f'CRS: {self._crs}]'