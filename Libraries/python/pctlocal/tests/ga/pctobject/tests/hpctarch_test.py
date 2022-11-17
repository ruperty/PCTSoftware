import unittest


from eepct.hpct import HPCTArchitecture
from eepct.hpct import HPCTARCH




class TestHPCTArchConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # hpct_architecture_properties ={
        #         HPCTARCH.HIERARCHY:{
        #             HPCTARCH.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES:{'lower':-1, 'upper':1}},
        #             HPCTARCH.REFERENCE: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES:{'lower':-5, 'upper':5}},
        #             HPCTARCH.COMPARATOR: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'Subtract', HPCTARCH.VARIABLE_PROPERTIES: None},
        #             HPCTARCH.OUTPUT: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAProportional', HPCTARCH.VARIABLE_PROPERTIES:{'lower':-2, 'upper':2}},
        #             HPCTARCH.ACTION: {HPCTARCH.VARIABLE_TYPE: 'Float', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES:{'lower':-50, 'upper':50}},
        #             HPCTARCH.LEVELS: { 
        #                 HPCTARCH.ZERO: { HPCTARCH.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Binary', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES:None}},
        #                 HPCTARCH.ZEROTOP: { HPCTARCH.PERCEPTION: {HPCTARCH.VARIABLE_TYPE: 'Binary', HPCTARCH.FUNCTION_CLASS: 'EAWeightedSum', HPCTARCH.VARIABLE_PROPERTIES:None},
        #                                     HPCTARCH.REFERENCE: {HPCTARCH.VARIABLE_TYPE: 'Literal', HPCTARCH.FUNCTION_CLASS: 'EAConstant', HPCTARCH.VARIABLE_PROPERTIES:None}},
        #                 HPCTARCH.TOP: { HPCTARCH.REFERENCE: {HPCTARCH.VARIABLE_TYPE: 'Literal', HPCTARCH.FUNCTION_CLASS: 'EAConstant', HPCTARCH.VARIABLE_PROPERTIES:None}}
        #             }
        #         }         
        #     }
        # cls.arch = HPCTArchitecture(arch=hpct_architecture_properties)
        cls.arch = HPCTArchitecture()
        cls.arch.configure()
        cls.arch.set(HPCTARCH.ZERO, HPCTARCH.ACTION, HPCTARCH.VARIABLE_PROPERTIES, {'lower': -50, 'upper': 50})
        cls.arch.set(HPCTARCH.ZERO, HPCTARCH.REFERENCE, HPCTARCH.VARIABLE_PROPERTIES, {'lower': -5, 'upper': 5})
        cls.arch.set(HPCTARCH.TOP, HPCTARCH.OUTPUT, HPCTARCH.VARIABLE_PROPERTIES, {'lower': -2, 'upper': 2})
        cls.arch.set(HPCTARCH.N, HPCTARCH.REFERENCE, HPCTARCH.VARIABLE_PROPERTIES, {'lower': -5, 'upper': 5})
        cls.arch.set(HPCTARCH.N, HPCTARCH.OUTPUT, HPCTARCH.VARIABLE_PROPERTIES, {'lower': -2, 'upper': 2})

        cls.arch1 = HPCTArchitecture()
        cls.arch1.configure(1)
        cls.arch1.set(HPCTARCH.ZEROTOP, HPCTARCH.ACTION, HPCTARCH.VARIABLE_PROPERTIES, {'lower': -50, 'upper': 50})
        cls.arch1.set(HPCTARCH.ZEROTOP, HPCTARCH.OUTPUT, HPCTARCH.VARIABLE_PROPERTIES, {'lower': -2, 'upper': 2})




    def test_hpctarch_1level(self):

        c1, v1, p1 = self.arch1.get_function_properties(HPCTARCH.ZEROTOP, HPCTARCH.PERCEPTION)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Binary')
        self.assertEqual(p1, None)

        c1, v1, p1 = self.arch1.get_function_properties(HPCTARCH.ZEROTOP, HPCTARCH.ACTION)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -50, 'upper': 50})

        c1, v1, p1 = self.arch1.get_function_properties(HPCTARCH.ZEROTOP, HPCTARCH.REFERENCE)
        self.assertEqual(c1, 'EAConstant')
        self.assertEqual(v1, 'Literal')
        self.assertEqual(p1, None)

        c1, v1, p1 = self.arch1.get_function_properties(HPCTARCH.ZEROTOP, HPCTARCH.OUTPUT)
        self.assertEqual(c1, 'EAProportional')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -2, 'upper': 2})

        c1, v1, p1 = self.arch1.get_function_properties(HPCTARCH.ZEROTOP, HPCTARCH.COMPARATOR)
        self.assertEqual(c1, 'Subtract')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, None)

    def test_hpctarch_3levels(self):

        c1, v1, p1 = self.arch.get_function_properties(HPCTARCH.ZERO, HPCTARCH.PERCEPTION)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Binary')
        self.assertEqual(p1, None)

        c1, v1, p1 = self.arch.get_function_properties(HPCTARCH.ZERO, HPCTARCH.ACTION)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -50, 'upper': 50})

        c1, v1, p1 = self.arch.get_function_properties(HPCTARCH.ZERO, HPCTARCH.REFERENCE)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -5, 'upper': 5})

        c1, v1, p1 = self.arch.get_function_properties(HPCTARCH.TOP, HPCTARCH.OUTPUT)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAProportional')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -2, 'upper': 2} )

        c1, v1, p1 = self.arch.get_function_properties(HPCTARCH.TOP, HPCTARCH.REFERENCE)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAConstant')
        self.assertEqual(v1, 'Literal')
        self.assertEqual(p1, None)

        #c1, v1, p1 = arch.get_function_properties(HPCTARCH.ZEROTOP, HPCTARCH.REFERENCE)
        #print(c1, v1, p1)

        c1, v1, p1 = self.arch.get_function_properties(HPCTARCH.N, HPCTARCH.REFERENCE)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAWeightedSum')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -5, 'upper': 5})

        c1, v1, p1 = self.arch.get_function_properties(HPCTARCH.N, HPCTARCH.OUTPUT)
        #print(c1, v1, p1)
        self.assertEqual(c1, 'EAProportional')
        self.assertEqual(v1, 'Float')
        self.assertEqual(p1, {'lower': -2, 'upper': 2})



if __name__ == '__main__':
    unittest.main()
