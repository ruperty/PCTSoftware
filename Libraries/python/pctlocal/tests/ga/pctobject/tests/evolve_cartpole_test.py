


import unittest
import os

from eepct.hpct import HPCTEvolveProperties
from utils.paths import get_root_path, get_gdrive
from deap import base, creator
from epct.evolvers import CommonToolbox
from eepct.hpct import HPCTIndividual

toolbox = base.Toolbox()
CommonToolbox.getInstance().set_toolbox(toolbox)


class TestEvolveCartpole(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)        
        cls.pop_size = 4
        cls.gens = 1        
        debug= 0 #0 #3 # details of population in each gen, inc. mutate and merge
        hpct_verbose= False #True # log of every control system iteration
        evolve_verbose =  1 #2 # output of evolve iterations, 2 for best of each gen
        cls.verbose={ 'debug': debug, 'evolve_verbose': evolve_verbose, 'hpct_verbose':hpct_verbose}
        cls.prefix = get_root_path() + 'Versioning'+os.sep+'PCTSoftware'+os.sep+'Libraries'+os.sep+'python'+os.sep+'pctlocal'+os.sep+'tests'+os.sep+'ga'+os.sep+'pctobject'+os.sep+'configs'+os.sep+'CartPoleV1'+os.sep+''
        cls.suffix = ".properties"


    def test_std00_IE_RMS_mode00(self):
        filename = 'Std00-InputsError-RootMeanSquareError-Mode00'        
        file = self.prefix + filename + self.suffix

        hep = HPCTEvolveProperties()

        output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
        print(score)
        
        self.assertAlmostEqual(score, 16.949603136533007)
        

    def test_std00_IE_RMS_mode01(self):
        filename = 'Std00-InputsError-RootMeanSquareError-Mode01'        
        file = self.prefix + filename + self.suffix

        hep = HPCTEvolveProperties()

        output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
        print(score)
        
        self.assertAlmostEqual(score, 25.052665371959325)
        
        
    def test_std00_TE_RMS_mode00(self):
        filename = 'Std00-TotalError-RootMeanSquareError-Mode00'        
        file = self.prefix + filename + self.suffix

        hep = HPCTEvolveProperties()

        output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
        print(score)
        
        self.assertAlmostEqual(score, 19.307275966656576)        
        
    def test_std00_TE_RMS_mode01(self):
        filename = 'Std00-TotalError-RootMeanSquareError-Mode01'        
        file = self.prefix + filename + self.suffix

        hep = HPCTEvolveProperties()

        output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
        print(score)
        
        self.assertAlmostEqual(score, 5.263805245212976)        
                
                
                
        
        
    def test_std01_IE_RMS_mode00(self):
        filename = 'Std01-InputsError-RootMeanSquareError-Mode00'        
        file = self.prefix + filename + self.suffix

        hep = HPCTEvolveProperties()

        output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
        print(score)
        
        self.assertAlmostEqual(score, 18.79305613192372)    
        
        
            
    def test_std01_IE_RMS_mode01(self):
        filename = 'Std01-InputsError-RootMeanSquareError-Mode01'        
        file = self.prefix + filename + self.suffix

        hep = HPCTEvolveProperties()

        output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
        print(score)
        
        self.assertAlmostEqual(score, 22.10562580760481)    
        
            
    def test_std01_TE_RMS_mode00(self):
        filename = 'Std01-TotalError-RootMeanSquareError-Mode00'        
        file = self.prefix + filename + self.suffix

        hep = HPCTEvolveProperties()

        output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
        print(score)
        
        self.assertAlmostEqual(score, 19.56707031226311)        
        
    def test_std01_TE_RMS_mode01(self):
        filename = 'Std01-TotalError-RootMeanSquareError-Mode01'        
        file = self.prefix + filename + self.suffix

        hep = HPCTEvolveProperties()

        output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
        print(score)
        
        self.assertAlmostEqual(score,  5.263805245212976)        
        
    def test_std02_IE_RMS_mode00(self):
        filename = 'Std02-InputsError-RootMeanSquareError-Mode00'        
        file = self.prefix + filename + self.suffix

        hep = HPCTEvolveProperties()

        output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
        print(score)
        
        self.assertAlmostEqual(score, 18.833059591366965)    
        
            
    def test_std02_IE_RMS_mode01(self):
        filename = 'Std02-InputsError-RootMeanSquareError-Mode01'        
        file = self.prefix + filename + self.suffix

        hep = HPCTEvolveProperties()

        output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
        print(score)
        
        self.assertAlmostEqual(score, 19.93341868149284)        
        
        
            
    # def test_std00_TE_RMS_mode01(self):
    #     filename = ''        
    #     file = self.prefix + filename + self.suffix

    #     hep = HPCTEvolveProperties()

    #     output_file, evr, score = hep.evolve_from_properties_file(file=file, print_properties=True, verbose=self.verbose, toolbox=toolbox, pop_size=self.pop_size, gens=self.gens)
    #     print(score)
        
    #     self.assertAlmostEqual(score, 0.1197538059583196)        
        
        
        
        
        
                