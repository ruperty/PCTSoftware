import unittest
import random
import json
from deap import tools, base, creator

from pct.environments import VelocityModel
from epct.evolvers import EvolverWrapper, CommonToolbox

from pct.functions import HPCTFUNCTION

from eepct.hpct import HPCTArchitecture

from eepct.hpct import HPCTVARIABLE
from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTLEVEL
from eepct.hpct import HPCTEvolver
from eepct.hpct import HPCTIndividual

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)


class TestHPCTMutateTopInputs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        # creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        CommonToolbox.getInstance().set_toolbox(toolbox)

        lower, upper = -100, 100 
        arch = HPCTArchitecture()
        #arch.configure(3)
        arch.configure()
        arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTVARIABLE.PROPERTIES, {'lower': lower, 'upper': upper})
        arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, {'lower': lower, 'upper': upper})
        arch.set(HPCTLEVEL.TOP, HPCTFUNCTION.OUTPUT, HPCTVARIABLE.PROPERTIES, {'lower': lower, 'upper': upper})
        arch.set(HPCTLEVEL.N, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, {'lower': lower, 'upper': upper})
        arch.set(HPCTLEVEL.N, HPCTFUNCTION.OUTPUT, HPCTVARIABLE.PROPERTIES, {'lower': lower, 'upper': upper})

        seed, debug, pop_size, processes, runs, nevals, num_actions=3, 3, 1, 1, 500, 2, 2
        min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit, error_limit = 1, 5, 1, 5, 100

        env = 'VelocityModel' #(name='VM', mass=250, num_links=2, indexes=4)
        env_inputs_indexes=[0,2,1,3]
        zerolevel_inputs_indexes=[0,1]
        toplevel_inputs_indexes=[2,3]
        env_inputs_names=['IP', 'IV', 'IC', 'IF']
        references=[11, 2]
        error_collector_type , error_response_type, error_properties= 'InputsError', 'RootMeanSquareError', 'error:smooth_factor,0.5'

        environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes,
            'toplevel_inputs_indexes':toplevel_inputs_indexes, 'env_inputs_names':env_inputs_names, 'env_name':env, 'num_actions':num_actions, 'references':references}
        # evolve_properties = {'alpha':0.5, 'mu':0.1, 'sigma':0.25, 'indpb':1, 'attr_mut_pb':1}

        hpct_structure_properties ={ 'min_levels_limit':min_levels_limit, 'max_levels_limit':max_levels_limit, 'references':references,
            'min_columns_limit':min_columns_limit, 'max_columns_limit':max_columns_limit, 'lower_float':-100, 'upper_float':100, 'structurepb':1, }    
        hpct_run_properties ={ 'error_collector_type':error_collector_type, 'error_response_type': error_response_type,
            'error_properties':error_properties, 'error_limit': error_limit, 'runs':runs, 'nevals':nevals,
            'history':False, 'hpct_verbose':False,  'debug':debug, 'seed':seed}    

        evolver_properties = {'environment_properties':environment_properties, 
            # 'evolve_properties':evolve_properties,  
            'hpct_structure_properties':hpct_structure_properties,
            'hpct_run_properties':hpct_run_properties,
            # 'individual_properties': individual_properties, 
            'arch': arch}

        evolver = HPCTEvolver(**evolver_properties)

        cls.evr = EvolverWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes)
        #cls.ind = cls.evr.toolbox.individual()



    def test_TopInputs_a_choice3(self):
        random.seed(1)

        ind = self.evr.toolbox.individual()
        #print(ind.get_grid())
        
        link_name_0_A = ind.get_node(1,0).get_function_from_collection(HPCTFUNCTION.PERCEPTION).get_links()[0].name
        link_name_1_A = ind.get_node(1,1).get_function_from_collection(HPCTFUNCTION.PERCEPTION).get_links()[0].name


        ind1 = self.evr.toolbox.mutate(ind)[0]

        grid = ind1.get_grid()
        #print(grid)

        self.assertEqual(grid, [2])

        link_name_0_B = ind1.get_node(0,0).get_function_from_collection(HPCTFUNCTION.PERCEPTION).get_links()[0].name
        self.assertEqual(link_name_0_B, link_name_0_A)
        link_name_1_B = ind1.get_node(0,1).get_function_from_collection(HPCTFUNCTION.PERCEPTION).get_links()[0].name
        self.assertEqual(link_name_1_B, link_name_1_A)

        

        # new_config = ind1.get_config()
        # #print(new_config)
        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IV'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': [8.761143536525351]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IF'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': [-4.968899066068913]}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-5.620977923547004, -1.307037659807477]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [0.9103441346247005, 2.908307251262175]}}}
        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])


    def test_TopInputs_b_choice3(self):
        random.seed(6)
        ind = self.evr.toolbox.individual()
        #print(ind.get_grid())

        ind1 = self.evr.toolbox.mutate(ind)[0]

        grid = ind1.get_grid()
        #print(grid)

        self.assertEqual(grid, [1, 4, 3, 2])


        # new_config = ind1.get_config()
        # #print(new_config)
        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3', 4: 'OL1C4'}, 'weights': [9.250678326552332, 4.808023241840339, -3.2901327019667788, -9.30921698503493, 5.8266496118082465]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': [-0.5359437471745134]}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C0', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [8.45680913570568, 0.6947155402193973, -7.920966723932656]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'PL0C0'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': [1.5025816540094001]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C1', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [3.7108250575765, 2.3481477480169723, -8.148347983033709]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'PL0C0'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': [-1.354511600828272]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L1C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C2', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [5.952973157145679, 5.493082431558354, -1.0705114846402815]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C2', 'value': 0, 'links': {0: 'PL0C0'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C2', 'value': 0, 'links': {0: 'RL1C2', 1: 'PL1C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C2', 'value': 0, 'links': {0: 'CL1C2'}, 'gain': [-8.362546815021123]}}}}, 'col3': {'col': 3, 'node': {'type': 'PCTNode', 'name': 'L1C3', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C3', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [-7.917883529007609, -9.03892123781817, 7.867102532515548]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C3', 'value': 0, 'links': {0: 'PL0C0'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C3', 'value': 0, 'links': {0: 'RL1C3', 1: 'PL1C3'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C3', 'value': 0, 'links': {0: 'CL1C3'}, 'gain': [6.558414436369075]}}}}, 'col4': {'col': 4, 'node': {'type': 'PCTNode', 'name': 'L1C4', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C4', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [8.154588168622439, 7.865892746192081, -0.9603229910593569]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C4', 'value': 0, 'links': {0: 'PL0C0'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C4', 'value': 0, 'links': {0: 'RL1C4', 1: 'PL1C4'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C4', 'value': 0, 'links': {0: 'CL1C4'}, 'gain': 3.876007798356264}}}}}}, 'level2': {'level': 2, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L2C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C0', 'value': 0, 'links': {0: 'OL3C0'}, 'weights': [2.8805286979254285]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C0', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3', 4: 'PL1C4'}, 'weights': [0, 0, 1, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C0', 'value': 0, 'links': {0: 'RL2C0', 1: 'PL2C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C0', 'value': 0, 'links': {0: 'CL2C0'}, 'gain': [-5.021108697127612]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L2C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C1', 'value': 0, 'links': {0: 'OL3C0'}, 'weights': [-8.251725244304911]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C1', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3', 4: 'PL1C4'}, 'weights': [0, 0, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C1', 'value': 0, 'links': {0: 'RL2C1', 1: 'PL2C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C1', 'value': 0, 'links': {0: 'CL2C1'}, 'gain': [7.358880988017803]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L2C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C2', 'value': 0, 'links': {0: 'OL3C0'}, 'weights': [4.319410837787007]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C2', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3', 4: 'PL1C4'}, 'weights': [1, 1, 0, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C2', 'value': 0, 'links': {0: 'RL2C2', 1: 'PL2C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C2', 'value': 0, 'links': {0: 'CL2C2'}, 'gain': [-2.3090800375213982]}}}}}}, 'level3': {'level': 3, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L3C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL3C0', 'value': 0, 'links': {0: 'OL4C0', 1: 'OL4C1'}, 'weights': [0.585701678430557, -6.223135330092039]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL3C0', 'value': 0, 'links': {0: 'PL2C0', 1: 'PL2C1', 2: 'PL2C2'}, 'weights': [1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL3C0', 'value': 0, 'links': {0: 'RL3C0', 1: 'PL3C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL3C0', 'value': 0, 'links': {0: 'CL3C0'}, 'gain': [-6.532587302698481]}}}}}}, 'level4': {'level': 4, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L4C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL4C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL4C0', 'value': 0, 'links': {0: 'IV'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL4C0', 'value': 0, 'links': {0: 'RL4C0', 1: 'PL4C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL4C0', 'value': 0, 'links': {0: 'CL4C0'}, 'gain': [1.226074714188755]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L4C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL4C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL4C1', 'value': 0, 'links': {0: 'IF'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL4C1', 'value': 0, 'links': {0: 'RL4C1', 1: 'PL4C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL4C1', 'value': 0, 'links': {0: 'CL4C1'}, 'gain': [-2.3443547822270663]}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0'}, 'weights': [0.9210378847600997]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0'}, 'weights': [-4.03704464572112]}}}
        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])


    def test_TopInputs_c_choice4(self):
        random.seed(12)
        ind = self.evr.toolbox.individual()
        #ind.draw(file='test_TopInputs_c_choice2_b4.png', node_size=200)
        link_name_0_A = ind.get_node(3,0).get_function_from_collection(HPCTFUNCTION.PERCEPTION).get_links()[0].name
        link_name_1_A = ind.get_node(3,1).get_function_from_collection(HPCTFUNCTION.PERCEPTION).get_links()[0].name
        #print(ind.get_grid())
        ind1 = self.evr.toolbox.mutate(ind)[0]
        #ind1.draw(file='test_TopInputs_c_choice2_b5.png', node_size=200)

        grid = ind1.get_grid()
        #print(grid)

        self.assertEqual(grid, [3, 4, 3, 2])

        link_name_0_B = ind1.get_node(3,0).get_function_from_collection(HPCTFUNCTION.PERCEPTION).get_links()[0].name
        self.assertEqual(link_name_0_B, link_name_0_A)
        link_name_1_B = ind1.get_node(3,1).get_function_from_collection(HPCTFUNCTION.PERCEPTION).get_links()[0].name
        self.assertEqual(link_name_1_B, link_name_1_A)


        # new_config = ind1.get_config()
        # #print(new_config)
        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3', 4: 'OL1C4'}, 'weights': [-9.784170396090143, -2.2490637611086037, -4.945244993222403, 5.818530186981361, 4.129959055090271]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': [2.1621551926783926]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3', 4: 'OL1C4'}, 'weights': [-2.8275386192871674, -3.154899341618921, -5.194421835491314, 1.4500212471774534, -5.766205430377936]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': [0.225990180710502]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L0C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C2', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3', 4: 'OL1C4'}, 'weights': [6.103360998323611, -7.953402044217445, 8.43242050856498, 6.368305358828112, 3.355622722281442]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C2', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C2', 'value': 0, 'links': {0: 'RL0C2', 1: 'PL0C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C2', 'value': 0, 'links': {0: 'CL0C2'}, 'gain': [-5.168266006712631]}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C0', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [2.8605572735254903, 9.242835170264936, 0.7520170222869108]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2'}, 'weights': [0, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': [7.936701961353678]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C1', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [6.571588056375108, -2.399389910504938, -1.4637730046360191]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2'}, 'weights': [1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': [1.7825295379040618]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L1C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C2', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [2.5776382007294107, -8.336878132441962, -6.139087456860711]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C2', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2'}, 'weights': [0, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C2', 'value': 0, 'links': {0: 'RL1C2', 1: 'PL1C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C2', 'value': 0, 'links': {0: 'CL1C2'}, 'gain': [5.6077766061654515]}}}}, 'col3': {'col': 3, 'node': {'type': 'PCTNode', 'name': 'L1C3', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C3', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [7.6049634263684665, -2.0715424943061027, -4.016772370212758]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C3', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2'}, 'weights': [0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C3', 'value': 0, 'links': {0: 'RL1C3', 1: 'PL1C3'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C3', 'value': 0, 'links': {0: 'CL1C3'}, 'gain': [-5.344374541948604]}}}}, 'col4': {'col': 4, 'node': {'type': 'PCTNode', 'name': 'L1C4', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C4', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [0.09775070861960483, 6.1479966710800875, 0.20369273737421745]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C4', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2'}, 'weights': [0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C4', 'value': 0, 'links': {0: 'RL1C4', 1: 'PL1C4'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C4', 'value': 0, 'links': {0: 'CL1C4'}, 'gain': [-8.701204536980956]}}}}}}, 'level2': {'level': 2, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L2C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C0', 'value': 0, 'links': {0: 'OL3C0', 1: 'OL3C1'}, 'weights': [-9.417239613265064, -5.814409987959855]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C0', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3', 4: 'PL1C4'}, 'weights': [0, 1, 1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C0', 'value': 0, 'links': {0: 'RL2C0', 1: 'PL2C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C0', 'value': 0, 'links': {0: 'CL2C0'}, 'gain': [2.3339508455819398]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L2C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C1', 'value': 0, 'links': {0: 'OL3C0', 1: 'OL3C1'}, 'weights': [-1.3868441414069237, -0.2299376156182141]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C1', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3', 4: 'PL1C4'}, 'weights': [1, 1, 1, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C1', 'value': 0, 'links': {0: 'RL2C1', 1: 'PL2C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C1', 'value': 0, 'links': {0: 'CL2C1'}, 'gain': [2.3700418099245555]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L2C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C2', 'value': 0, 'links': {0: 'OL3C0', 1: 'OL3C1'}, 'weights': [-4.498621688255484, -0.3746029909757644]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C2', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3', 4: 'PL1C4'}, 'weights': [1, 0, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C2', 'value': 0, 'links': {0: 'RL2C2', 1: 'PL2C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C2', 'value': 0, 'links': {0: 'CL2C2'}, 'gain': [9.14477413596051]}}}}}}, 'level3': {'level': 3, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L3C01', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL3C0', 'value': 0, 'links': {0: 'OL4C0', 1: 'OL4C1'}, 'weights': [9.420811871872875, 0.45502124543006417]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL3C0', 'value': 0, 'links': {0: 'PL2C0', 1: 'PL2C1', 2: 'PL2C2'}, 'weights': [0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL3C0', 'value': 0, 'links': {0: 'RL3C0', 1: 'PL3C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL3C0', 'value': 0, 'links': {0: 'CL3C0'}, 'gain': -8.941526134551651}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L3C11', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL3C1', 'value': 0, 'links': {0: 'OL4C0', 1: 'OL4C1'}, 'weights': [7.179074714374558, -3.7792141984347927]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL3C1', 'value': 0, 'links': {0: 'PL2C0', 1: 'PL2C1', 2: 'PL2C2'}, 'weights': [1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL3C1', 'value': 0, 'links': {0: 'RL3C1', 1: 'PL3C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL3C1', 'value': 0, 'links': {0: 'CL3C1'}, 'gain': 7.453404845477266}}}}}}, 'level4': {'level': 4, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L4C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL4C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL4C0', 'value': 0, 'links': {0: 'IV'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL4C0', 'value': 0, 'links': {0: 'RL4C0', 1: 'PL4C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL4C0', 'value': 0, 'links': {0: 'CL4C0'}, 'gain': [-4.529981390404267]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L4C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL4C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL4C1', 'value': 0, 'links': {0: 'IF'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL4C1', 'value': 0, 'links': {0: 'RL4C1', 1: 'PL4C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL4C1', 'value': 0, 'links': {0: 'CL4C1'}, 'gain': [8.957554384041881]}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2'}, 'weights': [-2.997717431591156, -6.419638304647778, 4.698263604206876]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2'}, 'weights': [8.045282043222894, -9.585202154072588, -4.7141817381027]}}}
        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])

        # jsonnew = json.dumps(new_config, indent=4)
        # with  open('new.json', "w") as f:
        #     f.write(jsonnew)
        # jsonold = json.dumps(old_config, indent=4)
        # with  open('old.json', "w") as f:
        #     f.write(jsonold)
    


    def test_TopInputs_d_choice4(self):
        random.seed(17)
        ind = self.evr.toolbox.individual()
        #ind.summary()
        ind1 = self.evr.toolbox.mutate(ind)[0]
        grid = ind1.get_grid()
        #print(grid)

        self.assertEqual(grid,  [4, 3, 3, 2, 2])


        # new_config = ind1.get_config()
        # #print(new_config)
        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2'}, 'weights': [-7.80938969967308, -8.975742935194296, -2.533119734251846]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': [5.054853673465254]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2'}, 'weights': [2.939202803599866, 4.005631601075173, 4.991901035805707]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': [-7.075921828932024]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L0C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C2', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2'}, 'weights': [-6.704915279177909, 4.171375710982033, 1.4474264784825603]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C2', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C2', 'value': 0, 'links': {0: 'RL0C2', 1: 'PL0C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C2', 'value': 0, 'links': {0: 'CL0C2'}, 'gain': [9.17420826849613]}}}}, 'col3': {'col': 3, 'node': {'type': 'PCTNode', 'name': 'L0C3', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C3', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2'}, 'weights': [1.494925264212025, 7.788505109190241, 2.9962533378300296]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C3', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C3', 'value': 0, 'links': {0: 'RL0C3', 1: 'PL0C3'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C3', 'value': 0, 'links': {0: 'CL0C3'}, 'gain': [-3.4644588177012077]}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C0', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [6.323811543742289, 8.652831269840412]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3'}, 'weights': [1, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': [-2.2657032393640577]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C1', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [-2.45703788449534, 5.747664513061118]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3'}, 'weights': [1, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': [-5.778185450475766]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L1C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C2', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [-4.107856561297279, 6.2649759008940356]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C2', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3'}, 'weights': [1, 1, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C2', 'value': 0, 'links': {0: 'RL1C2', 1: 'PL1C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C2', 'value': 0, 'links': {0: 'CL1C2'}, 'gain': [2.146687546359635]}}}}}}, 'level2': {'level': 2, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L2C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C0', 'value': 0, 'links': {0: 'OL3C0', 1: 'OL3C1', 2: 'OL3C2'}, 'weights': [7.632814963236692, -3.6526524098312705, -3.1627454002145305]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C0', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2'}, 'weights': [1, 0, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C0', 'value': 0, 'links': {0: 'RL2C0', 1: 'PL2C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C0', 'value': 0, 'links': {0: 'CL2C0'}, 'gain': [7.943313482948237]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L2C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C1', 'value': 0, 'links': {0: 'OL3C0', 1: 'OL3C1', 2: 'OL3C2'}, 'weights': [-8.475482512083644, 9.696463450232894, -9.282060635220901]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C1', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2'}, 'weights': [0, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C1', 'value': 0, 'links': {0: 'RL2C1', 1: 'PL2C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C1', 'value': 0, 'links': {0: 'CL2C1'}, 'gain': [5.109594630121673]}}}}}}, 'level3': {'level': 3, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L3C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL3C0', 'value': 0, 'links': {0: 'OL4C0', 1: 'OL4C1'}, 'weights': [0.06585128912828697, 9.014305675518731]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL3C0', 'value': 0, 'links': {0: 'PL2C0', 1: 'PL2C1'}, 'weights': [1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL3C0', 'value': 0, 'links': {0: 'RL3C0', 1: 'PL3C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL3C0', 'value': 0, 'links': {0: 'CL3C0'}, 'gain': [9.788461629919583]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L3C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL3C1', 'value': 0, 'links': {0: 'OL4C0', 1: 'OL4C1'}, 'weights': [9.925503176427924, 9.056154887388718]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL3C1', 'value': 0, 'links': {0: 'PL2C0', 1: 'PL2C1'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL3C1', 'value': 0, 'links': {0: 'RL3C1', 1: 'PL3C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL3C1', 'value': 0, 'links': {0: 'CL3C1'}, 'gain': [3.558056248258221]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L3C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL3C2', 'value': 0, 'links': {0: 'OL4C0', 1: 'OL4C1'}, 'weights': [5.951617814055488, 8.758833815826202]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL3C2', 'value': 0, 'links': {0: 'PL2C0', 1: 'PL2C1'}, 'weights': [1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL3C2', 'value': 0, 'links': {0: 'RL3C2', 1: 'PL3C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL3C2', 'value': 0, 'links': {0: 'CL3C2'}, 'gain': [6.50514578573755]}}}}}}, 'level4': {'level': 4, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L4C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL4C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL4C0', 'value': 0, 'links': {0: 'IV'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL4C0', 'value': 0, 'links': {0: 'RL4C0', 1: 'PL4C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL4C0', 'value': 0, 'links': {0: 'CL4C0'}, 'gain': [8.709184061359988]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L4C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL4C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL4C1', 'value': 0, 'links': {0: 'IF'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL4C1', 'value': 0, 'links': {0: 'RL4C1', 1: 'PL4C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL4C1', 'value': 0, 'links': {0: 'CL4C1'}, 'gain': [6.74100423538524]}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3'}, 'weights': [3.282071448582645, -1.9913108620627582, -8.25128248619217, -8.758182924531443]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3'}, 'weights': [3.0677847624113292, -5.442364301578194, 0.36651992844169035, -4.8261454577844995]}}}
        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])


    def test_TopInputs_e_choice2(self):
        random.seed(15)
        ind = self.evr.toolbox.individual()
        #ind.summary()
        ind1 = self.evr.toolbox.mutate(ind)[0]
        grid = ind1.get_grid()
        #print(grid)

        self.assertEqual(grid,  [1, 2, 2])

        rlinks = ind1.get_node(1,1).get_function_from_collection(HPCTFUNCTION.REFERENCE).get_links()
        self.assertEqual(rlinks, ['OL2C0', 'OL2C1'])

        plinks = [link.name for link in ind1.get_node(0,0).get_function_from_collection(HPCTFUNCTION.PERCEPTION).get_links()]
        self.assertEqual(plinks, ['IP', 'IC'])


        # new_config = ind1.get_config()
        # #print(new_config)
        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-9.406375848365808, 7.622354721023564]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': [3.4391111786218445]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [2.280967524359344, 5.699480278862259]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': 6.881894129377951}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'IV', 1: 'PL0C1'}, 'weights': [1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': [-4.948519818168476]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'IF', 1: 'PL0C1'}, 'weights': [1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': [-1.0079603448708712]}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-2.676854587813805, -9.652375536171029]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-2.148743640678937, 0.599713250247401]}}}
        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])






class TestHPCTMutateNoTopInputs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        # creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        CommonToolbox.getInstance().set_toolbox(toolbox)


        lower, upper = -100, 100 
        arch = HPCTArchitecture()
        #arch.configure(3)
        arch.configure()
        arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTVARIABLE.PROPERTIES, {'lower': lower, 'upper': upper})
        arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, {'lower': lower, 'upper': upper})
        arch.set(HPCTLEVEL.TOP, HPCTFUNCTION.OUTPUT, HPCTVARIABLE.PROPERTIES, {'lower': lower, 'upper': upper})
        arch.set(HPCTLEVEL.N, HPCTFUNCTION.REFERENCE, HPCTVARIABLE.PROPERTIES, {'lower': lower, 'upper': upper})
        arch.set(HPCTLEVEL.N, HPCTFUNCTION.OUTPUT, HPCTVARIABLE.PROPERTIES, {'lower': lower, 'upper': upper})

        seed, debug, pop_size, processes, runs, nevals, num_actions=8, 3, 1, 1, 500, 2, 2
        min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit, error_limit = 1, 5, 1, 5, 100
        random.seed(seed)

        env = 'VelocityModel' #(name='VM', mass=250, num_links=2, indexes=4)
        env_inputs_indexes=[0,2,1,3]
        zerolevel_inputs_indexes=None
        toplevel_inputs_indexes=None
        #zerolevel_inputs_indexes=[0,1]
        #toplevel_inputs_indexes=[2,3]
        env_inputs_names=['IP', 'IV', 'IC', 'IF']
        references=[11, 2]
        error_collector_type , error_response_type, error_properties= 'InputsError', 'RootMeanSquareError', 'error:smooth_factor,0.5'

        environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes,
            'toplevel_inputs_indexes':toplevel_inputs_indexes, 'env_inputs_names':env_inputs_names, 'env_name':env, 'num_actions':num_actions, 'references':references}
        # evolve_properties = {'alpha':0.5, 'mu':0.1, 'sigma':0.25, 'indpb':1, 'attr_mut_pb':1}

        hpct_structure_properties ={ 'min_levels_limit':min_levels_limit, 'max_levels_limit':max_levels_limit, 'references':references,
            'min_columns_limit':min_columns_limit, 'max_columns_limit':max_columns_limit, 'lower_float':-100, 'upper_float':100, 'structurepb':1, }    
        hpct_run_properties ={ 'error_collector_type':error_collector_type, 'error_response_type': error_response_type,
            'error_properties':error_properties, 'error_limit': error_limit, 'runs':runs, 'nevals':nevals,
            'history':False, 'hpct_verbose':False,  'debug':debug, 'seed':seed}    

        evolver_properties = {'environment_properties':environment_properties, 
            # 'evolve_properties':evolve_properties,  
            'hpct_structure_properties':hpct_structure_properties,
            'hpct_run_properties':hpct_run_properties,
            'arch': arch}

        evolver = HPCTEvolver(**evolver_properties)

        cls.evr = EvolverWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes)



    def test_NoTopInputs_a_choice2(self):
        ind = self.evr.toolbox.individual()
        ind.get_preprocessor()[0].summary()
        print(ind.get_postprocessor()[0].get_links()[0])
        # ind.summary()
        print(ind.get_grid())
        ind1 = self.evr.toolbox.mutate(ind)[0]
        #ind1.get_preprocessor()[0].summary()

        grid = ind1.get_grid()
        print(grid)
        self.assertEqual(grid, [2, 2])


        # new_config = ind1.get_config()
        # # print(new_config)
        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-8.31695586208189, -5.019039494846758]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [0, 1, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': [10.014523483097303]}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'PL0C0'}, 'weights': [0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': [3.191219402175862]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'PL0C0'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': [2.6170267673408714]}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0'}, 'weights': [-2.1319398103481317]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0'}, 'weights': [4.349574145278522]}}}
        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])


    def test_NoTopInputs_b_choice1(self):
        
        random.seed(3)
        ind = self.evr.toolbox.individual()
        ind.get_preprocessor()[0].summary()

        #print(ind.get_grid())
        ind1 = self.evr.toolbox.mutate(ind)[0]
        #ind1.get_preprocessor()[0].summary()

        grid = ind1.get_grid()
        print(grid)
        self.assertEqual(grid, [5, 4, 2])

        # new_config = ind1.get_config()
        # # print(new_config)
        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [2.663898783146826, 8.466757995602205]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [1, 0, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': [-0.45555173464310034]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-2.4614321612161048, 7.702707775489379]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [1, 1, 0, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': [-5.150657090589724]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L0C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C2', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-6.412478406137249, 9.407257476295293]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C2', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [1, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C2', 'value': 0, 'links': {0: 'RL0C2', 1: 'PL0C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C2', 'value': 0, 'links': {0: 'CL0C2'}, 'gain': [-8.897910335066745]}}}}, 'col3': {'col': 3, 'node': {'type': 'PCTNode', 'name': 'L0C3', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C3', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [4.222363326280792, 8.322197714742963]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C3', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [1, 0, 0, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C3', 'value': 0, 'links': {0: 'RL0C3', 1: 'PL0C3'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C3', 'value': 0, 'links': {0: 'CL0C3'}, 'gain': [-1.8078386315669466]}}}}, 'col4': {'col': 4, 'node': {'type': 'PCTNode', 'name': 'L0C4', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C4', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-9.447576731458236, -0.014052989006009708]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C4', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [0, 1, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C4', 'value': 0, 'links': {0: 'RL0C4', 1: 'PL0C4'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C4', 'value': 0, 'links': {0: 'CL0C4'}, 'gain': [-4.482081218783484]}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3', 4: 'PL0C4'}, 'weights': [0, 0, 1, 0, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': [0.8006883662978863]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3', 4: 'PL0C4'}, 'weights': [0, 1, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': [9.63166310199407]}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3', 4: 'OL0C4'}, 'weights': [2.950907927014422, -6.821398329164495, 7.192001738173318, 9.16367343779561, 8.440376853995467]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3', 4: 'OL0C4'}, 'weights': [1.4902972356371096, 4.3185052843372445, -5.742816986138636, 6.897079109154771, 1.6730798476116304]}}}
        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])

    def test_NoTopInputs_c_choice1(self):
        
        random.seed(12)
        ind = self.evr.toolbox.individual()
        ind.get_preprocessor()[0].summary()

        #print(ind.get_grid())
        #ind.summary()
        ind1 = self.evr.toolbox.mutate(ind)[0]
        ind1.get_preprocessor()[0].summary()

        grid = ind1.get_grid()
        print(grid)
        #ind1.summary()
        self.assertEqual(grid, [3, 5, 4, 2])

        
        # new_config = ind1.get_config()
        # # print(new_config)
        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3', 4: 'OL1C4'}, 'weights': [-0.437772829540694, 2.96650856568834, -0.8344690284582381, 7.3450735247412, -5.446190025690012]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [1, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': [-10.04317483278705]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3', 4: 'OL1C4'}, 'weights': [-3.491683861294633, -5.555792507539626, 1.8387534314464158, -5.843562985248649, -0.046603966665701435]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [1, 0, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': [6.634835592659439]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L0C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C2', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3', 4: 'OL1C4'}, 'weights': [6.479523565383442, 3.476676104201791, -5.1321404335536185, 10.006336112086226, -1.4273277861227676]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C2', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [0, 1, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C2', 'value': 0, 'links': {0: 'RL0C2', 1: 'PL0C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C2', 'value': 0, 'links': {0: 'CL0C2'}, 'gain': [-0.9545182139323483]}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C0', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [7.581140162352771, 1.075278637277373]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2'}, 'weights': [0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': [7.863395450539257]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C1', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [2.352403375089234, 3.0833487567682893]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2'}, 'weights': [1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': [1.9189055565798752]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L1C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C2', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [-4.753052855914181, 8.874924522720413]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C2', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2'}, 'weights': [1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C2', 'value': 0, 'links': {0: 'RL1C2', 1: 'PL1C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C2', 'value': 0, 'links': {0: 'CL1C2'}, 'gain': [-1.8573052773028587]}}}}, 'col3': {'col': 3, 'node': {'type': 'PCTNode', 'name': 'L1C3', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C3', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [-5.343618069248909, -2.5727307672429487]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C3', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2'}, 'weights': [0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C3', 'value': 0, 'links': {0: 'RL1C3', 1: 'PL1C3'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C3', 'value': 0, 'links': {0: 'CL1C3'}, 'gain': [6.309979577224233]}}}}, 'col4': {'col': 4, 'node': {'type': 'PCTNode', 'name': 'L1C4', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C4', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1'}, 'weights': [6.784096665319519, -1.3506614280444054]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C4', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2'}, 'weights': [1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C4', 'value': 0, 'links': {0: 'RL1C4', 1: 'PL1C4'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C4', 'value': 0, 'links': {0: 'CL1C4'}, 'gain': [-5.167818625365262]}}}}}}, 'level2': {'level': 2, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L2C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL2C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C0', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3', 4: 'PL1C4'}, 'weights': [1, 1, 0, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C0', 'value': 0, 'links': {0: 'RL2C0', 1: 'PL2C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C0', 'value': 0, 'links': {0: 'CL2C0'}, 'gain': [8.253653563660475]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L2C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL2C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C1', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3', 4: 'PL1C4'}, 'weights': [0, 1, 1, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C1', 'value': 0, 'links': {0: 'RL2C1', 1: 'PL2C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C1', 'value': 0, 'links': {0: 'CL2C1'}, 'gain': [5.1999043916229715]}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2'}, 'weights': [-5.140905704961033, 2.301079065053357, 8.908104818461023]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2'}, 'weights': [8.561458866484122, 6.252986826323702, -6.544744815139277]}}}
        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])


    def test_NoTopInputs_d_choice1(self):
        
        random.seed(16)
        ind = self.evr.toolbox.individual()
        ind.get_preprocessor()[0].summary()
        #ind.summary()

        #ind.save(file='b4.json')
        #ind.draw(file='test_NoTopInputs_d_choice2_b4.png', node_size=200)

        print(ind.get_grid())
        ind1 = self.evr.toolbox.mutate(ind)[0]
        ind1.get_preprocessor()[0].summary()
        #ind1.draw(file='test_NoTopInputs_d_choice2_b5.png', node_size=200)

        grid = ind1.get_grid()
        print(grid)
        self.assertEqual(grid, [4, 5, 2])
        #ind1.summary()


        # new_config = ind1.get_config()
        # #print(new_config)
        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3'}, 'weights': [-9.943617562192884, 7.0915962324995006, 4.195128090176189, -5.295562282198442]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [0, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': [-5.521721758578281]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3'}, 'weights': [8.879083152860108, 1.800706877379698, -9.152350808515854, -5.551052302474902]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [0, 0, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': [2.425418555539077]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L0C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C2', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3'}, 'weights': [-0.9521105728223822, 2.779684894059856, -4.282331124261352, -5.213153564104662]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C2', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [1, 1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C2', 'value': 0, 'links': {0: 'RL0C2', 1: 'PL0C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C2', 'value': 0, 'links': {0: 'CL0C2'}, 'gain': [-3.610883260897136]}}}}, 'col3': {'col': 3, 'node': {'type': 'PCTNode', 'name': 'L0C3', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C3', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2', 3: 'OL1C3'}, 'weights': [-0.4120324470394192, 0.5034184806156243, -6.193488711796459, 1.4170543599240495]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C3', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [0, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C3', 'value': 0, 'links': {0: 'RL0C3', 1: 'PL0C3'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C3', 'value': 0, 'links': {0: 'CL0C3'}, 'gain': [0.9086099976556942]}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C0', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [-5.510826635951858, -6.835617665372547, -6.660512327489004]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3'}, 'weights': [0, 1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': [-3.8101173511895503]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C1', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [4.086126075693587, 4.714842693903639, -8.872730526904501]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3'}, 'weights': [0, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': [-9.449051176365625]}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L1C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C2', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [-0.6965899509895861, 2.7853597969785766, -9.148816485985646]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C2', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3'}, 'weights': [0, 1, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C2', 'value': 0, 'links': {0: 'RL1C2', 1: 'PL1C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C2', 'value': 0, 'links': {0: 'CL1C2'}, 'gain': [0.423531851936261]}}}}, 'col3': {'col': 3, 'node': {'type': 'PCTNode', 'name': 'L1C3', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C3', 'value': 0, 'links': {0: 'OL2C0', 1: 'OL2C1', 2: 'OL2C2'}, 'weights': [8.096095537760108, -9.521288752887, -1.9976431670915868]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C3', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1', 2: 'PL0C2', 3: 'PL0C3'}, 'weights': [1, 1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C3', 'value': 0, 'links': {0: 'RL1C3', 1: 'PL1C3'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C3', 'value': 0, 'links': {0: 'CL1C3'}, 'gain': [-8.98905864263689]}}}}}}, 'level2': {'level': 2, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L2C01', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C0', 'value': 0, 'links': {0: 'OL3C0', 1: 'OL3C1'}, 'weights': [-3.1243689071330616, 6.528930526990592]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C0', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3'}, 'weights': [1, 1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C0', 'value': 0, 'links': {0: 'RL2C0', 1: 'PL2C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C0', 'value': 0, 'links': {0: 'CL2C0'}, 'gain': -5.7481663001288785}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L2C11', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C1', 'value': 0, 'links': {0: 'OL3C0', 1: 'OL3C1'}, 'weights': [-1.7528866569385677, 4.643069903252199]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C1', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3'}, 'weights': [1, 1, 0, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C1', 'value': 0, 'links': {0: 'RL2C1', 1: 'PL2C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C1', 'value': 0, 'links': {0: 'CL2C1'}, 'gain': 1.0586797209962633}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L2C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL2C2', 'value': 0, 'links': {0: 'OL3C0', 1: 'OL3C1'}, 'weights': [3.034433893368327, -1.661102587621837]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C2', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2', 3: 'PL1C3'}, 'weights': [0, 1, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C2', 'value': 0, 'links': {0: 'RL2C2', 1: 'PL2C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C2', 'value': 0, 'links': {0: 'CL2C2'}, 'gain': 9.246947813320606}}}}}}, 'level3': {'level': 3, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L3C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL3C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL3C0', 'value': 0, 'links': {0: 'PL2C0', 1: 'PL2C1', 2: 'PL2C2'}, 'weights': [0, 0, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL3C0', 'value': 0, 'links': {0: 'RL3C0', 1: 'PL3C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL3C0', 'value': 0, 'links': {0: 'CL3C0'}, 'gain': [-5.286691340751763]}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L3C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL3C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL3C1', 'value': 0, 'links': {0: 'PL2C0', 1: 'PL2C1', 2: 'PL2C2'}, 'weights': [0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL3C1', 'value': 0, 'links': {0: 'RL3C1', 1: 'PL3C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL3C1', 'value': 0, 'links': {0: 'CL3C1'}, 'gain': [-1.9738062942633063]}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3'}, 'weights': [-9.067546572245934, 6.919580713180608, 5.100605414924866, -9.153997601104209]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1', 2: 'OL0C2', 3: 'OL0C3'}, 'weights': [7.127976114493126, -1.904533663543041, 7.989831472396298, 3.737458439469359]}}}
        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])


        # jsonnew = json.dumps(new_config, indent=4)
        # with  open('new.json', "w") as f:
        #     f.write(jsonnew)
        # jsonold = json.dumps(old_config, indent=4)
        # with  open('old.json', "w") as f:
        #     f.write(jsonold)
    




if __name__ == '__main__':
    unittest.main()
