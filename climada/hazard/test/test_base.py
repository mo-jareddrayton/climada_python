"""
Test Exposure base class.
"""

import unittest
import numpy as np
from scipy import sparse

from climada.hazard.base import Hazard
from climada.hazard.centroids.base import Centroids

class TestLoader(unittest.TestCase):
    """Test loading funcions from the Hazard class"""

    @staticmethod
    def good_hazard():
        """Define well a hazard"""
        haz = Hazard()
        haz.centroids = Centroids()
        haz.centroids.region_id = np.array([1, 2])
        haz.centroids.id = np.array([1, 2])
        haz.centroids.coord = np.array([[1, 2], [1, 2]])
        haz.event_id = np.array([1, 2, 3])
        haz.event_name = ['A', 'B', 'C']
        haz.frequency = np.array([1, 2, 3])
        # events x centroids
        haz.intensity = sparse.csr_matrix([[1, 2], [1, 2], [1, 2]])
        haz.fraction = sparse.csr_matrix([[1, 2], [1, 2], [1, 2]])

        return haz

    def test_check_wrongCentroids_fail(self):
        """Wrong hazard definition"""
        haz = self.good_hazard()
        haz.centroids.region_id = np.array([1, 2, 3, 4])

        with self.assertRaises(ValueError) as error:
            haz.check()
        self.assertEqual('Invalid Centroids.region_id size: 2 != 4', \
                         str(error.exception))

    def test_check_wrongFreq_fail(self):
        """Wrong hazard definition"""
        haz = self.good_hazard()
        haz.frequency = np.array([1, 2])

        with self.assertRaises(ValueError) as error:
            haz.check()
        self.assertEqual('Invalid Hazard.frequency size: 3 != 2', \
                         str(error.exception))

    def test_check_wrongInten_fail(self):
        """Wrong hazard definition"""
        haz = self.good_hazard()
        haz.intensity = sparse.csr_matrix([[1, 2], [1, 2]])

        with self.assertRaises(ValueError) as error:
            haz.check()
        self.assertEqual('Invalid Hazard.intensity row size: 3 != 2', \
                         str(error.exception))

    def test_check_wrongFrac_fail(self):
        """Wrong exposures definition"""
        haz = self.good_hazard()
        haz.fraction = sparse.csr_matrix([[1], [1], [1]])

        with self.assertRaises(ValueError) as error:
            haz.check()
        self.assertEqual('Invalid Hazard.fraction column size: 2 != 1', \
                         str(error.exception))

    def test_check_wrongEvName_fail(self):
        """Wrong exposures definition"""
        haz = self.good_hazard()
        haz.event_name = ['M']

        with self.assertRaises(ValueError) as error:
            haz.check()
        self.assertEqual('Invalid Hazard.event_name size: 3 != 1', \
                         str(error.exception))

    def test_load_notimplemented(self):
        """Load function not implemented"""
        haz = Hazard()
        with self.assertRaises(NotImplementedError):
            haz.load('filename')

    def test_read_notimplemented(self):
        """Read function not implemented"""
        haz = Hazard()
        with self.assertRaises(NotImplementedError):
            haz.read('filename')

    def test_constructfile_notimplemented(self):
        """Constructor from file not implemented"""
        with self.assertRaises(NotImplementedError):
            Hazard('filename')

if __name__ == '__main__':
    unittest.main()
