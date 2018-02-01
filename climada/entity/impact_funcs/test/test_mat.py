"""
Test imp_funcsFuncsExcel class.
"""

import unittest

import climada.util.hdf5_handler as hdf5
from climada.entity.impact_funcs.source_mat import ImpactFuncsMat
from climada.util.constants import ENT_DEMO_MAT

class TestReader(unittest.TestCase):
    """Test reader functionality of the imp_funcsFuncsExcel class"""

    def test_demo_file_pass(self):
        """ Read demo excel file"""
        # Read demo excel file
        imp_funcs = ImpactFuncsMat()
        description = 'One single file.'
        imp_funcs.read(ENT_DEMO_MAT, description)

        # Check results
        n_funcs = 2
        hazard = 'TC'
        first_id = 1
        second_id = 3

        self.assertEqual(len(imp_funcs._data), 1)
        self.assertEqual(len(imp_funcs._data[hazard]), n_funcs)

        # first function
        self.assertEqual(imp_funcs._data[hazard][first_id].id, 1)
        self.assertEqual(imp_funcs._data[hazard][first_id].name,
                         'Tropical cyclone default')
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity_unit, \
                         'm/s')

        self.assertEqual(imp_funcs._data[hazard][first_id].intensity.shape, \
                         (9,))
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity[0], 0)
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity[1], 20)
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity[2], 30)
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity[3], 40)
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity[4], 50)
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity[5], 60)
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity[6], 70)
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity[7], 80)
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity[8], 100)

        self.assertEqual(imp_funcs._data[hazard][first_id].mdd.shape, (9,))
        self.assertEqual(imp_funcs._data[hazard][first_id].mdd[0], 0)
        self.assertEqual(imp_funcs._data[hazard][first_id].mdd[8], 0.41079600)

        self.assertEqual(imp_funcs._data[hazard][first_id].paa.shape, (9,))
        self.assertEqual(imp_funcs._data[hazard][first_id].paa[0], 0)
        self.assertEqual(imp_funcs._data[hazard][first_id].paa[8], 1)

        # second function
        self.assertEqual(imp_funcs._data[hazard][second_id].id, 3)
        self.assertEqual(imp_funcs._data[hazard][second_id].name,
                         'TC Building code')
        self.assertEqual(imp_funcs._data[hazard][first_id].intensity_unit, \
                         'm/s')

        self.assertEqual(imp_funcs._data[hazard][second_id].intensity.shape, \
                         (9,))
        self.assertEqual(imp_funcs._data[hazard][second_id].intensity[0], 0)
        self.assertEqual(imp_funcs._data[hazard][second_id].intensity[1], 20)
        self.assertEqual(imp_funcs._data[hazard][second_id].intensity[2], 30)
        self.assertEqual(imp_funcs._data[hazard][second_id].intensity[3], 40)
        self.assertEqual(imp_funcs._data[hazard][second_id].intensity[4], 50)
        self.assertEqual(imp_funcs._data[hazard][second_id].intensity[5], 60)
        self.assertEqual(imp_funcs._data[hazard][second_id].intensity[6], 70)
        self.assertEqual(imp_funcs._data[hazard][second_id].intensity[7], 80)
        self.assertEqual(imp_funcs._data[hazard][second_id].intensity[8], 100)

        self.assertEqual(imp_funcs._data[hazard][second_id].mdd.shape, (9,))
        self.assertEqual(imp_funcs._data[hazard][second_id].mdd[0], 0)
        self.assertEqual(imp_funcs._data[hazard][second_id].mdd[8], 0.4)

        self.assertEqual(imp_funcs._data[hazard][second_id].paa.shape, (9,))
        self.assertEqual(imp_funcs._data[hazard][second_id].paa[0], 0)
        self.assertEqual(imp_funcs._data[hazard][second_id].paa[8], 1)

        # general information
        self.assertEqual(imp_funcs.tag.file_name, ENT_DEMO_MAT)
        self.assertEqual(imp_funcs.tag.description, description)

class TestGets(unittest.TestCase):
    """Test functions to retrieve specific variables"""

    def setUp(self):
        self.imp = hdf5.read(ENT_DEMO_MAT)
        self.imp = self.imp[ImpactFuncsMat().sup_field_name]
        self.imp = self.imp[ImpactFuncsMat().field_name]

    def test_rows_pass(self):
        """Check get_funcs_rows."""
        funcs = ImpactFuncsMat().get_funcs_rows(self.imp, ENT_DEMO_MAT)
        self.assertEqual(len(funcs), 2)
        
        self.assertEqual(len(funcs['Tropical cyclone default']), 9)
        self.assertEqual(len(funcs['TC Building code']), 9)
        for i in range(9):
            self.assertEqual(funcs['Tropical cyclone default'][i], i)
            self.assertEqual(funcs['TC Building code'][i], 9 + i)

    def test_hazard_pass(self):
        """Check get_imp_fun_hazard."""
        funcs = ImpactFuncsMat().get_funcs_rows(self.imp, ENT_DEMO_MAT)
        haz_type = ImpactFuncsMat().get_imp_fun_hazard(
                self.imp, funcs['TC Building code'], ENT_DEMO_MAT)
        self.assertEqual(haz_type, 'TC')

        haz_type = ImpactFuncsMat().get_imp_fun_hazard(
                self.imp, funcs['Tropical cyclone default'], ENT_DEMO_MAT)
        self.assertEqual(haz_type, 'TC')

    def test_id_pass(self):
        """Check get_imp_fun_id."""
        funcs = ImpactFuncsMat().get_funcs_rows(self.imp, ENT_DEMO_MAT)
        fun_id = ImpactFuncsMat().get_imp_fun_id(
                self.imp, funcs['TC Building code'])
        self.assertEqual(fun_id, 3)

        fun_id = ImpactFuncsMat().get_imp_fun_id(
                self.imp, funcs['Tropical cyclone default'])
        self.assertEqual(fun_id, 1)

    def test_unit_pass(self):
        """Check get_imp_fun_unit"""
        funcs = ImpactFuncsMat().get_funcs_rows(self.imp, ENT_DEMO_MAT)
        fun_unit = ImpactFuncsMat().get_imp_fun_unit(self.imp, \
                                 funcs['TC Building code'], ENT_DEMO_MAT)
        self.assertEqual(fun_unit, 'm/s')

        fun_unit = ImpactFuncsMat().get_imp_fun_unit(self.imp, \
                                 funcs['Tropical cyclone default'], \
                                 ENT_DEMO_MAT)
        self.assertEqual(fun_unit, 'm/s')

if __name__ == '__main__':
    unittest.main()
