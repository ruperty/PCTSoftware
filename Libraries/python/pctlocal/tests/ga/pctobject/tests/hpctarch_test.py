import unittest


from eepct.hpct import HPCTArchitecture
from eepct.hpct import HPCTARCH
from eepct.hpct import HPCTLEVEL

from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTVARIABLE


class TestHPCTArchConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # hpct_architecture_properties ={
        #         HPCTARCH.HIERARCHY:{
        #             HPCTFUNCTION.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-1, 'upper':1}},
        #             HPCTFUNCTION.REFERENCE: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-5, 'upper':5}},
        #             HPCTFUNCTION.COMPARATOR: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'Subtract', HPCTVARIABLE.PROPERTIES: None},
        #             HPCTFUNCTION.OUTPUT: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAProportional', HPCTVARIABLE.PROPERTIES:{'lower':-2, 'upper':2}},
        #             HPCTFUNCTION.ACTION: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-50, 'upper':50}},
        #             HPCTARCH.LEVELS: { 
        #                 HPCTLEVEL.ZERO: { HPCTFUNCTION.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Binary', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:None}},
        #                 HPCTLEVEL.ZEROTOP: { HPCTFUNCTION.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Binary', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:None},
        #                                     HPCTFUNCTION.REFERENCE: {HPCTARCH.VARIABLE_TYPE: 'Literal', HPCTARCH.FUNCTION_CLASS: 'EAConstant', HPCTVARIABLE.PROPERTIES:None}},
        #                 HPCTLEVEL.TOP: { HPCTFUNCTION.REFERENCE: {HPCTARCH.VARIABLE_TYPE: 'Literal', HPCTARCH.FUNCTION_CLASS: 'EAConstant', HPCTVARIABLE.PROPERTIES:None}}
        #             }
        #         }         
        #     }
        # cls.arch = HPCTArchitecture(arch=hpct_architecture_properties)
        cls.arch = HPCTArchitecture()
        
        cls.arch.configure() 
        cls.arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTVARIABLE.PROPERTIES, {'lower': -50, 'upper': 50})
        cls.arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, {'lower': -5, 'upper': 5})
        cls.arch.set(HPCTLEVEL.TOP, HPCTFUNCTION.OUTPUT, HPCTVARIABLE.PROPERTIES, {'lower': -2, 'upper': 2})
        cls.arch.set(HPCTLEVEL.N, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, {'lower': -5, 'upper': 5})
        cls.arch.set(HPCTLEVEL.N, HPCTFUNCTION.OUTPUT, HPCTVARIABLE.PROPERTIES, {'lower': -2, 'upper': 2})

        cls.arch1 = HPCTArchitecture()
        #cls.arch1.configure(1)
        cls.arch1.configure()
        cls.arch1.set(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION, HPCTVARIABLE.PROPERTIES, {'lower': -50, 'upper': 50})
        cls.arch1.set(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.OUTPUT, HPCTVARIABLE.PROPERTIES, {'lower': -2, 'upper': 2})




    def test_hpctarch_1level(self):

        c1, v1, p1 = self.arch1.get_function_properties(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.PERCEPTION)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -10, 'upper': 10})

        c1, v1, p1 = self.arch1.get_function_properties(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -50, 'upper': 50})

        c1, v1, p1 = self.arch1.get_function_properties(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.REFERENCE)
        self.assertEqual(c1, 'EAConstant')
        self.assertEqual(v1, 'Literal')
        self.assertEqual(p1, None)

        c1, v1, p1 = self.arch1.get_function_properties(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.OUTPUT)
        self.assertEqual(c1, 'EAProportional')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -2, 'upper': 2})

        c1, v1, p1 = self.arch1.get_function_properties(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.COMPARATOR)
        self.assertEqual(c1, 'Subtract')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, None)

    def test_hpctarch_3levels(self):

        c1, v1, p1 = self.arch.get_function_properties(HPCTLEVEL.ZERO, HPCTFUNCTION.PERCEPTION)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -10, 'upper': 10})

        c1, v1, p1 = self.arch.get_function_properties(HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -50, 'upper': 50})

        c1, v1, p1 = self.arch.get_function_properties(HPCTLEVEL.ZERO, HPCTFUNCTION.REFERENCE)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -5, 'upper': 5})

        c1, v1, p1 = self.arch.get_function_properties(HPCTLEVEL.TOP, HPCTFUNCTION.OUTPUT)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAProportional')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -2, 'upper': 2} )

        c1, v1, p1 = self.arch.get_function_properties(HPCTLEVEL.TOP, HPCTFUNCTION.REFERENCE)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAConstant')
        self.assertEqual(v1, 'Literal')
        self.assertEqual(p1, None)

        #c1, v1, p1 = arch.get_function_properties(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.REFERENCE)
        #print(c1, v1, p1)

        c1, v1, p1 = self.arch.get_function_properties(HPCTLEVEL.N, HPCTFUNCTION.REFERENCE)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -5, 'upper': 5})

        c1, v1, p1 = self.arch.get_function_properties(HPCTLEVEL.N, HPCTFUNCTION.OUTPUT)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAProportional')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -2, 'upper': 2})



if __name__ == '__main__':
    unittest.main()
