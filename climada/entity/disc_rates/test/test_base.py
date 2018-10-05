"""
Test DiscRates class.
"""
import os
import unittest
import numpy as np

from climada.entity.disc_rates.base import DiscRates
from climada.entity.disc_rates.source import READ_SET

DATA_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'test', 'data')
ENT_TEST_XLS = os.path.join(DATA_DIR, 'demo_today.xlsx')

class TestChecker(unittest.TestCase):
    """Test discount rates attributes checker"""

    def test_check_wrongRates_fail(self):
        """Wrong discount rates definition"""
        disc_rate = DiscRates()
        disc_rate.rates = np.array([3,4])
        disc_rate.years = np.array([1])

        with self.assertLogs('climada.util.checker', level='ERROR') as cm:
            with self.assertRaises(ValueError):
                disc_rate.check()
        self.assertIn('Invalid DiscRates.rates size: 1 != 2.', cm.output[0])

class TestConstructor(unittest.TestCase):
    """Test discount rates attributes."""
    def test_attributes_all(self):
        """All attributes are defined"""
        disc_rate = DiscRates()
        self.assertTrue(hasattr(disc_rate, 'years'))
        self.assertTrue(hasattr(disc_rate, 'rates'))

    def test_get_def_vars(self):
        """ Test def_source_vars function."""
        self.assertTrue(DiscRates.get_def_file_var_names('xls') ==
                        READ_SET['XLS'][0])
        self.assertTrue(DiscRates.get_def_file_var_names('.mat') ==
                        READ_SET['MAT'][0])

class TestAppend(unittest.TestCase):
    """Check append function"""
    def test_append_to_empty_same(self):
        """Append DiscRates to empty one."""
        disc_rate = DiscRates()
        disc_rate_add = DiscRates()
        disc_rate_add.tag.file_name = 'file1.txt'
        disc_rate_add.tag.description = 'descr1'
        disc_rate_add.years = np.array([2000, 2001, 2002])
        disc_rate_add.rates = np.array([0.1, 0.2, 0.3])

        disc_rate.append(disc_rate_add)
        disc_rate.check()

        self.assertTrue(np.array_equal(disc_rate.years, disc_rate_add.years))
        self.assertTrue(np.array_equal(disc_rate.rates, disc_rate_add.rates))
        self.assertTrue(np.array_equal(disc_rate.tag.file_name, \
                                       disc_rate_add.tag.file_name))
        self.assertTrue(np.array_equal(disc_rate.tag.description, \
                                       disc_rate_add.tag.description))

    def test_append_equal_same(self):
        """Append the same DiscRates. The inital DiscRates is obtained."""
        disc_rate = DiscRates()
        disc_rate.tag.file_name = 'file1.txt'
        disc_rate.tag.description = 'descr1'
        disc_rate.years = np.array([2000, 2001, 2002])
        disc_rate.rates = np.array([0.1, 0.2, 0.3])

        disc_rate_add = DiscRates()
        disc_rate_add.tag.file_name = 'file1.txt'
        disc_rate_add.tag.description = 'descr1'
        disc_rate_add.years = np.array([2000, 2001, 2002])
        disc_rate_add.rates = np.array([0.1, 0.2, 0.3])

        disc_rate.append(disc_rate_add)
        disc_rate.check()

        self.assertTrue(np.array_equal(disc_rate.years, disc_rate_add.years))
        self.assertTrue(np.array_equal(disc_rate.rates, disc_rate_add.rates))
        self.assertTrue(np.array_equal(disc_rate.tag.file_name, disc_rate_add.tag.file_name))
        self.assertEqual(disc_rate.tag.description, disc_rate_add.tag.description)

    def test_append_different_append(self):
        """Append DiscRates with same and new values. The rates with repeated
        years are overwritten."""
        disc_rate = DiscRates()
        disc_rate.tag.file_name = 'file1.txt'
        disc_rate.tag.description = 'descr1'
        disc_rate.years = np.array([2000, 2001, 2002])
        disc_rate.rates = np.array([0.1, 0.2, 0.3])

        disc_rate_add = DiscRates()
        disc_rate_add.tag.file_name = 'file2.txt'
        disc_rate_add.tag.description = 'descr2'
        disc_rate_add.years = np.array([2000, 2001, 2003])
        disc_rate_add.rates = np.array([0.11, 0.22, 0.33])

        disc_rate.append(disc_rate_add)
        disc_rate.check()

        self.assertTrue(np.array_equal(disc_rate.years, \
                                       np.array([2000, 2001, 2002, 2003])))
        self.assertTrue(np.array_equal(disc_rate.rates, \
                                       np.array([0.11, 0.22, 0.3, 0.33])))
        self.assertTrue(np.array_equal(disc_rate.tag.file_name, 'file1.txt + file2.txt'))
        self.assertTrue(np.array_equal(disc_rate.tag.description, 'descr1 + descr2'))

class TestReadParallel(unittest.TestCase):
    """Check read function with several files"""

    def test_read_two_pass(self):
        """Both files are readed and appended."""
        descriptions = ['desc1','desc2']
        disc_rate = DiscRates([ENT_TEST_XLS, ENT_TEST_XLS], descriptions)
        self.assertEqual(disc_rate.tag.file_name, ENT_TEST_XLS)
        self.assertEqual(disc_rate.tag.description, 'desc1 + desc2')
        self.assertEqual(disc_rate.years.size, 51)

class TestSelect(unittest.TestCase):
    """Test select method """
    def test_select_pass(self):
        """Test select right time range."""
        disc_rate = DiscRates()
        disc_rate.tag.file_name = 'file1.txt'
        disc_rate.tag.description = 'descr1'
        disc_rate.years = np.arange(2000, 2050)
        disc_rate.rates = np.arange(disc_rate.years.size)

        year_range = np.arange(2010, 2020)
        sel_disc = disc_rate.select(year_range)

        self.assertTrue(np.array_equal(sel_disc.years, year_range))
        self.assertTrue(np.array_equal(sel_disc.rates, disc_rate.rates[10:20]))

    def test_select_wrong_pass(self):
        """Test select wrong time range."""
        disc_rate = DiscRates()
        disc_rate.tag.file_name = 'file1.txt'
        disc_rate.tag.description = 'descr1'
        disc_rate.years = np.arange(2000, 2050)
        disc_rate.rates = np.arange(disc_rate.years.size)

        year_range = np.arange(2050, 2060)
        self.assertEqual(None, disc_rate.select(year_range))

class TestNetPresValue(unittest.TestCase):
    """Test select method """
    def test_net_present_value_pass(self):
        """Test net_present_value right time range."""
        disc_rate = DiscRates()
        disc_rate.tag.file_name = 'file1.txt'
        disc_rate.tag.description = 'descr1'
        disc_rate.years = np.arange(2000, 2050)
        disc_rate.rates = np.ones(disc_rate.years.size)*0.02

        val_years = np.ones(23)*6.512201157564418e9
        res = disc_rate.net_present_value(2018, 2040, val_years)
        self.assertEqual(res, 1.215049630691397e+11)

    def test_net_present_value_wrong_pass(self):
        """Test net_present_value wrong time range."""
        disc_rate = DiscRates()
        disc_rate.tag.file_name = 'file1.txt'
        disc_rate.tag.description = 'descr1'
        disc_rate.years = np.arange(2000, 2050)
        disc_rate.rates = np.arange(disc_rate.years.size)
        val_years = np.ones(11)*6.512201157564418e9
        self.assertEqual(None, disc_rate.net_present_value(2050, 2060, val_years))

# Execute Tests
TESTS = unittest.TestLoader().loadTestsFromTestCase(TestChecker)
TESTS.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAppend))
TESTS.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConstructor))
TESTS.addTests(unittest.TestLoader().loadTestsFromTestCase(TestReadParallel))
TESTS.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSelect))
TESTS.addTests(unittest.TestLoader().loadTestsFromTestCase(TestNetPresValue))
unittest.TextTestRunner(verbosity=2).run(TESTS)
