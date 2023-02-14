import unittest
import random
from deap import tools, base, creator

from pct.environments import VelocityModel

from epct.evolvers import EvolverWrapper, CommonToolbox
from pct.functions import HPCTFUNCTION


from eepct.hpct import HPCTVARIABLE
from eepct.hpct import HPCTARCH
from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTLEVEL
from eepct.hpct import HPCTEvolver
from eepct.hpct import HPCTIndividual

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)


class TestHPCTIndividual1Level(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        #creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        #creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        CommonToolbox.getInstance().set_toolbox(toolbox)

        seed,  pop_size,  processes,   num_actions=1, 1,  1,   2
        # min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit, error_limit=1,2,1,3, 100

        random.seed(seed)
        # env = VelocityModel(name='VM', mass=250, num_links=2, indexes=4)
        env = 'VelocityModel'
        env_inputs_indexes=[0,2,1,3]
        zerolevel_inputs_indexes=[0,1]
        toplevel_inputs_indexes=[2,3]
        env_inputs_names=['IP', 'IV', 'IC', 'IF']
        references=[11, 2]
        error_collector_type , error_response_type, error_properties= 'InputsError', 'RootMeanSquareError', 'error:smooth_factor,0.5'

        error_limit=100 
        runs=1
        nevals=1
        debug=0

        environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes,
            'toplevel_inputs_indexes':toplevel_inputs_indexes, 'env_inputs_names':env_inputs_names, 'env_name':env, 'num_actions':num_actions, 'references':references}
        #evolve_properties = {'alpha':0.5, 'mu':0.1, 'sigma':0.25, 'attr_mut_pb':1, 'attr_cx_uniform_pb':0.5}

        # hpct_structure_properties ={ 'min_levels_limit':min_levels_limit, 'max_levels_limit':max_levels_limit,
        #     'min_columns_limit':min_columns_limit, 'max_columns_limit':max_columns_limit, 'lower_float':-100, 'upper_float':100, 'structurepb':1, }    
        hpct_run_properties ={ 'error_collector_type':error_collector_type, 'error_response_type': error_response_type,
            'error_properties':error_properties, 'error_limit': error_limit, 'runs':runs, 'nevals':nevals,
            'history':False, 'hpct_verbose':False,  'debug':debug, 'seed':seed}    


        hpct_architecture_properties ={
                HPCTARCH.HIERARCHY:{
                    HPCTFUNCTION.PERCEPTION: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-1, 'upper':1}},
                    HPCTFUNCTION.REFERENCE: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-5, 'upper':5}},
                    HPCTFUNCTION.COMPARATOR: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'Subtract', HPCTVARIABLE.PROPERTIES: None},
                    HPCTFUNCTION.OUTPUT: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAProportional', HPCTVARIABLE.PROPERTIES:{'lower':-2, 'upper':2}},
                    HPCTFUNCTION.ACTION: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-50, 'upper':50}},
                    HPCTARCH.LEVELS: { 
                        HPCTLEVEL.ZERO: { HPCTFUNCTION.PERCEPTION: {HPCTVARIABLE.TYPE: 'Binary', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:None}},
                        HPCTLEVEL.ZEROTOP: { HPCTFUNCTION.PERCEPTION: {HPCTVARIABLE.TYPE: 'Binary', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:None},
                                            HPCTFUNCTION.REFERENCE: {HPCTVARIABLE.TYPE: 'Literal', HPCTVARIABLE.FUNCTION_CLASS: 'EAConstant', HPCTVARIABLE.PROPERTIES:None}},
                        HPCTLEVEL.TOP: { HPCTFUNCTION.REFERENCE: {HPCTVARIABLE.TYPE: 'Literal', HPCTVARIABLE.FUNCTION_CLASS: 'EAConstant', HPCTVARIABLE.PROPERTIES:None}}
                    }
                }         
            }

        evolver_properties = {'environment_properties':environment_properties, 
            #'evolve_properties':evolve_properties,
            #'hpct_structure_properties':hpct_structure_properties,
            'hpct_run_properties':hpct_run_properties,
            #'individual_properties': individual_properties,
            'hpct_architecture_properties':hpct_architecture_properties}

        evolver = HPCTEvolver(**evolver_properties)

        cls.evr = EvolverWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes)
        cls.ind = cls.evr.toolbox.individual()

    def test_hpctind_create1(self):

        #self.ind.build_links()
        pwts = self.ind.get_node(0,0).get_function_from_collection(HPCTFUNCTION.PERCEPTION).weights
        self.assertEqual(pwts, [1])
        #self.assertEqual(pwts, [0, 1, 0, 1])

        ref = self.ind.get_node(0,0).get_function_from_collection(HPCTFUNCTION.REFERENCE).value
        self.assertEqual(ref, 11)

        ref = self.ind.get_node(0,1).get_function_from_collection(HPCTFUNCTION.REFERENCE).value
        self.assertEqual(ref, 2)

        out = self.ind.get_node(0,0).get_function_from_collection(HPCTFUNCTION.OUTPUT).gain
        self.assertAlmostEqual(out, -1.5283251853157558)

        act = self.ind.get_postprocessor()[0].weights
        self.assertEqual(act, [-12.03847766762722, -29.00451936285229])

        new_config = self.ind.get_config()
        # print(new_config)
        old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VelocityModel', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VelocityModel'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VelocityModel'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VelocityModel'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VelocityModel'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IV'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': -1.5283251853157558}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IF'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': -0.11101902569553346}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-12.03847766762722, -29.00451936285229]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-1.2143343475852433, 39.33170425576351]}}}

        for old, new in zip(old_config, new_config):
            self.assertEqual(old_config[old], new_config[new])
        #self.assertEqual(new_config, old_config)

        
    def test_hpctind_evaluate1(self):
        #self.ind.summary()
        self.ind.fitness.values = self.evr.toolbox.evaluate(self.ind)
        print (self.ind.fitness)  
        self.assertAlmostEqual(self.ind.fitness.values[0], 1)


    def test_hpctind_mutate1(self):
        ind1 = self.evr.toolbox.mutate(self.ind)[0]

        new_config = ind1.get_config()
        #old_config =  {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VelocityModel', 'value': [9.659475450093897, 9.659475450093897, 9.659475450093897, 9.659475450093897], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 9.659475450093897, 'links': {0: 'VelocityModel'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 9.659475450093897, 'links': {0: 'VelocityModel'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 9.659475450093897, 'links': {0: 'VelocityModel'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 9.659475450093897, 'links': {0: 'VelocityModel'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-0.6103836995543688, 0.08426488249981823]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': 1.113770460000583}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-0.10306479537741797, -4.70425036033093]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': -1.8260508385738903}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 9.659475450093897, 'links': {0: 'IV'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 1.3405245499061031, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': -2.048757431155565, 'links': {0: 'CL1C0'}, 'gain': -1.9765429835869597}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 9.659475450093897, 'links': {0: 'IF'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': -7.659475450093897, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0.850347501808282, 'links': {0: 'CL1C1'}, 'gain': -0.03762236490061298}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 1.9539925233402755e-13, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [20.338208860383602, 48.3187717309674]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 35.933492974273385, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [9.31837303800576, -10.640031362208603]}}}
        #old_config =  {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VelocityModel', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VelocityModel'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VelocityModel'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VelocityModel'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VelocityModel'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [4.391670189485865, 0.5285957629296512]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': -0.6171983411649902}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [4.522444552911937, 4.26506623785866]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': -0.3352802444226155}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'IV'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': -1.7615314121456638}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'IF'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': -0.27775448863631413}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [41.62698355052942, 42.21885624698875]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-39.99997289038728, 12.9352904800649]}}}
        old_config =  {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VelocityModel', 'value': [1.0, 1.0, 1.0, 1.0], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 1.0, 'links': {0: 'VelocityModel'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 1.0, 'links': {0: 'VelocityModel'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 1.0, 'links': {0: 'VelocityModel'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 1.0, 'links': {0: 'VelocityModel'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-0.6103836995543688, 0.08426488249981823]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': 1.113770460000583}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-0.10306479537741797, -4.70425036033093]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': -1.8260508385738903}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C0', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 1.0, 'links': {0: 'IV'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': -1.0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 1.5283251853157558, 'links': {0: 'CL1C0'}, 'gain': -1.9765429835869597}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C1', 'value': 0, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 1.0, 'links': {0: 'IF'}, 'weights': [1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': -1.0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0.11101902569553346, 'links': {0: 'CL1C1'}, 'gain': -0.03762236490061298}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': -21.618762092727053, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [20.338208860383602, 48.3187717309674]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 2.5106697186112275, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [9.31837303800576, -10.640031362208603]}}}
        
        #print(new_config)

        for old, new in zip(old_config, new_config):
            # print(old_config[old])
            # print(new_config[new])
            # print()
            self.assertEqual(old_config[old], new_config[new])
        #self.assertEqual(new_config, old_config)


    def test_hpctind_mate1(self):        
        ind1 = self.evr.toolbox.individual()   
        ind2 = self.evr.toolbox.individual()   

        child1, child2 = self.evr.toolbox.mate(ind1, ind2)

        child1list = child1.get_parameters_list()
        # print(child1.get_grid())
        # print(child1list)

        self.assertEqual(child1list[0][1][0],  [-74.01984766894066, -13.074895138985516])
        self.assertEqual(child1list[1][1][0], [[-4.694100169664464, -4.745541390065392]])

        self.assertEqual(child1list[1][0][2][0], [-1.4961250874332077])
        self.assertEqual(child1list[1][1][2][0], [0.9899421953346605])

        child2list = child2.get_parameters_list()
        # print(child2.get_grid())
        # print(child2list)

        self.assertEqual(child2list[0][1][0], [69.57458880501405, -23.137944344276367])
        self.assertEqual(child2list[1][1][0], [[2]])

        self.assertEqual(child2list[1][0][2][0], [0.7842049936023605])
        self.assertEqual(child2list[1][1][2][0], [0.9846855170041007])



class TestHPCTIndividual2Level(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        # creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        CommonToolbox.getInstance().set_toolbox(toolbox)

        seed=7
        random.seed(seed)
        pop_size=1
        processes=1

        env = 'VelocityModel' #(name='VM', mass=250, num_links=2, indexes=4)
        env_inputs_indexes=[0,2,1,3]
        zerolevel_inputs_indexes=[0,1]
        toplevel_inputs_indexes=[2,3]
        env_inputs_names=['IP', 'IV', 'IC', 'IF']
        num_actions=2
        references=[11, 2]

        error_limit=100 
        
        nevals=1
        debug=0
        error_collector_type , error_response_type, error_properties= 'InputsError', 'RootMeanSquareError', 'error:smooth_factor,0.5'

        environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes,
            'toplevel_inputs_indexes':toplevel_inputs_indexes, 'env_inputs_names':env_inputs_names, 'env_name':env, 'num_actions':num_actions, 'references':references}

        hpct_run_properties ={ 'error_collector_type':error_collector_type, 'error_response_type': error_response_type,
            'error_properties':error_properties, 'error_limit': error_limit,  'nevals':nevals,
            'history':False, 'hpct_verbose':False,  'debug':debug, 'seed':seed}    


        hpct_architecture_properties ={
                HPCTARCH.HIERARCHY:{
                    HPCTFUNCTION.PERCEPTION: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-1, 'upper':1}},
                    HPCTFUNCTION.REFERENCE: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-5, 'upper':5}},
                    HPCTFUNCTION.COMPARATOR: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'Subtract', HPCTVARIABLE.PROPERTIES: None},
                    HPCTFUNCTION.OUTPUT: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAProportional', HPCTVARIABLE.PROPERTIES:{'lower':-2, 'upper':2}},
                    HPCTFUNCTION.ACTION: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-50, 'upper':50}},
                    HPCTARCH.LEVELS: { 
                        HPCTLEVEL.ZERO: { HPCTFUNCTION.PERCEPTION: {HPCTVARIABLE.TYPE: 'Binary', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:None}},
                        HPCTLEVEL.ZEROTOP: { HPCTFUNCTION.PERCEPTION: {HPCTVARIABLE.TYPE: 'Binary', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:None},
                                            HPCTFUNCTION.REFERENCE: {HPCTVARIABLE.TYPE: 'Literal', HPCTVARIABLE.FUNCTION_CLASS: 'EAConstant', HPCTVARIABLE.PROPERTIES:None}},
                        HPCTLEVEL.TOP: { HPCTFUNCTION.REFERENCE: {HPCTVARIABLE.TYPE: 'Literal', HPCTVARIABLE.FUNCTION_CLASS: 'EAConstant', HPCTVARIABLE.PROPERTIES:None}}
                    }
                }         
            }

        evolver_properties = {'environment_properties':environment_properties, 
            # 'evolve_properties':evolve_properties,
            # 'hpct_structure_properties':hpct_structure_properties,
            'hpct_run_properties':hpct_run_properties,
            # 'individual_properties': individual_properties,
            'hpct_architecture_properties':hpct_architecture_properties}

        evolver = HPCTEvolver(**evolver_properties)

        cls.evr = EvolverWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes)
        cls.ind = cls.evr.toolbox.individual()


    def test_hpctind_create2(self):

        #self.ind.build_links()
        #self.ind.summary()
        pwts = self.ind.get_node(0,0).get_function_from_collection(HPCTFUNCTION.PERCEPTION).weights
        self.assertEqual(pwts, [1, 0])

        ref = self.ind.get_node(1,0).get_function_from_collection(HPCTFUNCTION.REFERENCE).value
        self.assertEqual(ref, 11)

        ref = self.ind.get_node(1,1).get_function_from_collection(HPCTFUNCTION.REFERENCE).value
        self.assertEqual(ref, 2)

        out = self.ind.get_node(0,0).get_function_from_collection(HPCTFUNCTION.OUTPUT).gain
        self.assertAlmostEqual(out, -0.5372443323496578)

        act = self.ind.get_postprocessor()[0].weights
        self.assertEqual(act, [-43.014457642538105])

        config = self.ind.get_config()
        #print(config)
        # self.assertEqual(config, {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1'}, 'weights': [-4.275637133324572, 0.35882004306689197]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IC'}, 'weights': [1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': -0.5372443323496578}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'IV'}, 'weights': [-0.8840021504505864]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': 0.02974293275768103}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'IF'}, 'weights': [-0.9250086831160302]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': -0.2654172653504565}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0'}, 'weights': [-43.014457642538105]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0'}, 'weights': [-40.928698665613496]}}})

    def test_hpctind_evaluate2(self):
        self.ind.fitness.values = self.evr.toolbox.evaluate(self.ind)
        #print (self.ind.fitness)  
        self.assertAlmostEqual(self.ind.fitness.values[0], 0.09854161276138362)

    def test_hpctind_mutate2(self):
        grid = self.ind.get_grid()
        #print(grid)
        ind1 = self.evr.toolbox.mutate(self.ind)[0]

        grid = ind1.get_grid()
        print(grid)

        new_config = ind1.get_config()
        # print(new_config)
        self.assertEqual(grid, [3, 2])
        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [-1.323886625894743, -1.323886625894743, -1.323886625894743, -1.323886625894743], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': -1.323886625894743, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': -1.323886625894743, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': -1.323886625894743, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': -1.323886625894743, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 1.1703186242437238, 'links': {0: 'IV'}, 'weights': [-0.7769658240928187]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 9.829681375756277, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0.2923635521885485, 'links': {0: 'CL0C0'}, 'gain': 0.3980632894789101}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL0C1', 'value': 2, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 1.2246066244138207, 'links': {0: 'IF'}, 'weights': [-0.6920915426501287]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0.7753933755861793, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': -0.20580278931894314, 'links': {0: 'CL0C1'}, 'gain': 0.07356398034828948}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': -2.5656447608155576e-14, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-43.02097253704061, 19.52953662736593]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': -2.4412373665403226e-14, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-41.24072847349662, 9.436987710501846]}}}

        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])


    def test_hpctind_mate2(self):        
            ind1 = self.evr.toolbox.individual()   
            ind2 = self.evr.toolbox.individual()   

            child1, child2 = self.evr.toolbox.mate(ind1, ind2)

            child1list = child1.get_parameters_list()
            # print(child1.get_grid())
            self.assertEqual(child1.get_grid(), [1, 2])    


            self.assertIsNotNone(child1list[0][1][0])
            self.assertIsNotNone(child1list[1][0][0][0])

            self.assertIsNotNone(child1list[1][0][1][0])
            self.assertIsNotNone(child1list[1][0][2][0])

            # self.assertEqual(child1list[0][1][0], [-38.220776192163164])
            # self.assertEqual(child1list[1][0][0][0], [0.7710294861749869, -1.0331952534921984])
            # self.assertEqual(child1list[1][0][1][0], [1, 0])
            # self.assertEqual(child1list[1][0][2][0], [1.9050204223716802])


            child2list = child2.get_parameters_list()
            # print(child2.get_grid())
            
            self.assertEqual(child2.get_grid(), [2])    


            self.assertIsNotNone(child2list[0][1][0])
            # self.assertEqual(child2list[0][1][0],[-0.3585504886508204, 3.1720246580185716])

class TestHPCTIndividual3Level(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        # creator.create("Individual", HPCTIndividual, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        CommonToolbox.getInstance().set_toolbox(toolbox)

        seed=5
        random.seed(seed)
        debug=3
        pop_size=1
        gens=40
        processes=1
        runs, nevals = 500, 2

        env = 'VelocityModel' #(name='VM', mass=250, num_links=2, indexes=4)
        env_inputs_indexes=[0,2,1,3]
        env_inputs_names=['IP', 'IV', 'IC', 'IF']
        zerolevel_inputs_indexes=None
        toplevel_inputs_indexes=None
        num_actions=2
        references=[11]
        error_collector_type , error_response_type, error_properties= 'InputsError', 'RootMeanSquareError', 'error:smooth_factor,0.5'
        error_limit = 100
        min_levels_limit, max_levels_limit, min_columns_limit, max_columns_limit=1,3,1,3

        environment_properties = {'env_inputs_indexes': env_inputs_indexes, 'zerolevel_inputs_indexes':zerolevel_inputs_indexes,
            'toplevel_inputs_indexes':toplevel_inputs_indexes, 'env_inputs_names':env_inputs_names, 'env_name':env, 'num_actions':num_actions, 'references':references}
        # evolve_properties = {'alpha':0.5, 'mu':0.1, 'sigma':0.25, 'structurepb':0, 'attr_mut_pb':1, 'attr_cx_uniform_pb':0.5 }
        hpct_structure_properties ={ 'min_levels_limit':min_levels_limit, 'max_levels_limit':max_levels_limit, 'references':references,
            'min_columns_limit':min_columns_limit, 'max_columns_limit':max_columns_limit}    
        hpct_run_properties ={ 'error_collector_type':error_collector_type, 'error_response_type': error_response_type,
            'error_properties':error_properties, 'error_limit': error_limit, 'runs':runs, 'nevals':nevals,
            'history':False, 'hpct_verbose':False,  'debug':debug, 'seed':seed}    


        hpct_architecture_properties ={
                HPCTARCH.HIERARCHY:{
                    HPCTFUNCTION.PERCEPTION: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-1, 'upper':1}},
                    HPCTFUNCTION.REFERENCE: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-5, 'upper':5}},
                    HPCTFUNCTION.COMPARATOR: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'Subtract', HPCTVARIABLE.PROPERTIES: None},
                    HPCTFUNCTION.OUTPUT: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAProportional', HPCTVARIABLE.PROPERTIES:{'lower':-2, 'upper':2}},
                    HPCTFUNCTION.ACTION: {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:{'lower':-50, 'upper':50}},
                    HPCTARCH.LEVELS: { 
                        HPCTLEVEL.ZERO: { HPCTFUNCTION.PERCEPTION: {HPCTVARIABLE.TYPE: 'Binary', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:None}},
                        HPCTLEVEL.ZEROTOP: { HPCTFUNCTION.PERCEPTION: {HPCTVARIABLE.TYPE: 'Binary', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES:None},
                                            HPCTFUNCTION.REFERENCE: {HPCTVARIABLE.TYPE: 'Literal', HPCTVARIABLE.FUNCTION_CLASS: 'EAConstant', HPCTVARIABLE.PROPERTIES:None}},
                        HPCTLEVEL.TOP: { HPCTFUNCTION.REFERENCE: {HPCTVARIABLE.TYPE: 'Literal', HPCTVARIABLE.FUNCTION_CLASS: 'EAConstant', HPCTVARIABLE.PROPERTIES:None}}
                    }
                }         
            }

        evolver_properties = {'environment_properties':environment_properties, 
            # 'evolve_properties':evolve_properties,
            'hpct_structure_properties':hpct_structure_properties,
            'hpct_run_properties':hpct_run_properties,
            # 'individual_properties': individual_properties,
            'hpct_architecture_properties':hpct_architecture_properties}

        evolver = HPCTEvolver(**evolver_properties)

        cls.evr = EvolverWrapper(evolver=evolver, pop_size=pop_size, toolbox=toolbox, processes=processes)
        cls.ind = cls.evr.toolbox.individual()


    def test_hpctind_create3(self):
        config = self.ind.get_config()
        # print(self.ind.get_grid())
        #self.ind.build_links()
        #self.ind.summary()
        pwts = self.ind.get_node(0,0).get_function_from_collection(HPCTFUNCTION.PERCEPTION).weights
        self.assertEqual(pwts, [1, 0,1,0])

        ref = self.ind.get_node(2,0).get_function_from_collection(HPCTFUNCTION.REFERENCE).value
        self.assertEqual(ref, 11)

        rwts = self.ind.get_node(1,1).get_function_from_collection(HPCTFUNCTION.REFERENCE).weights
        self.assertEqual(rwts, [-4.982251377974654])

        out = self.ind.get_node(0,0).get_function_from_collection(HPCTFUNCTION.OUTPUT).gain
        self.assertAlmostEqual(out, -0.12372380887134504)

        out = self.ind.get_node(1,1).get_function_from_collection(HPCTFUNCTION.OUTPUT).gain
        self.assertAlmostEqual(out, 1.4856189788971284)

        out = self.ind.get_node(1,2).get_function_from_collection(HPCTFUNCTION.OUTPUT).gain
        self.assertAlmostEqual(out, 1.4896310617472075)

        act = self.ind.get_postprocessor()[0].weights
        self.assertEqual(act, [-29.522048546620717, 44.09760010879991])

        # config = self.ind.get_config()
        # #print(config)
        # self.assertEqual(config,  {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [1, 1, 1, 1], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 0, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 0, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 0, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 0, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2'}, 'weights': [1.489745531369242, 4.009004917506227, -3.8679403534685566]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [1, 0, 1, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': 0, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 0, 'links': {0: 'CL0C0'}, 'gain': -0.12372380887134504}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': 0, 'links': {0: 'OL1C0', 1: 'OL1C1', 2: 'OL1C2'}, 'weights': [-4.868858104110978, -2.8327019953615187, -2.205176339888897]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 0, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [0, 1, 0, 0]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': 0, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': 0, 'links': {0: 'CL0C1'}, 'gain': 1.6653814872342076}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C0', 'value': 0, 'links': {0: 'OL2C0'}, 'weights': [2.9714699143120447]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [0.5314509032582835, -0.6807915752839235]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 0, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 0, 'links': {0: 'CL1C0'}, 'gain': -1.4449303264043873}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L1C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C1', 'value': 0, 'links': {0: 'OL2C0'}, 'weights': [-4.982251377974654]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C1', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [0.2349050409322333, -0.7466015348994606]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C1', 'value': 0, 'links': {0: 'RL1C1', 1: 'PL1C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C1', 'value': 0, 'links': {0: 'CL1C1'}, 'gain': 1.4856189788971284}}}}, 'col2': {'col': 2, 'node': {'type': 'PCTNode', 'name': 'L1C2', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL1C2', 'value': 0, 'links': {0: 'OL2C0'}, 'weights': [4.824211088259252]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C2', 'value': 0, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [-0.5810872350097642, -0.5690376615505355]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C2', 'value': 0, 'links': {0: 'RL1C2', 1: 'PL1C2'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C2', 'value': 0, 'links': {0: 'CL1C2'}, 'gain': 1.4896310617472075}}}}}}, 'level2': {'level': 2, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L2C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL2C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL2C0', 'value': 0, 'links': {0: 'PL1C0', 1: 'PL1C1', 2: 'PL1C2'}, 'weights': [-0.421389664506147, 0.922955977900167, 0.07844693774162126]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL2C0', 'value': 0, 'links': {0: 'RL2C0', 1: 'PL2C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL2C0', 'value': 0, 'links': {0: 'CL2C0'}, 'gain': 0.7113219090023692}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-29.522048546620717, 44.09760010879991]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': 0, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [19.06419411069082, 46.65643123171954]}}})


    def test_hpctind_evaluate3(self):
        self.ind.fitness.values = self.evr.toolbox.evaluate(self.ind)
        #print (self.ind.fitness)  
        self.assertAlmostEqual(self.ind.fitness.values[0],  106.29358254687388)


    def test_hpctind_mutate3(self):
        grid = self.ind.get_grid()
        # print(grid)
        self.assertEqual(grid, [2,3,1])
        ind1 = self.evr.toolbox.mutate(self.ind)[0]

        grid = ind1.get_grid()
        # print(grid)
        self.assertEqual(grid, [2,1])


        # new_config = ind1.get_config()
        # # print(new_config)

        # old_config = {'type': 'Individual', 'name': 'pcthierarchy', 'pre': {'pre0': {'type': 'VelocityModel', 'name': 'VM', 'value': [524.7394545110875, 524.7394545110875, 524.7394545110875, 524.7394545110875], 'links': {0: 'Action1', 1: 'Action2'}, 'mass': 250}, 'pre1': {'type': 'IndexedParameter', 'name': 'IP', 'value': 524.7394545110875, 'links': {0: 'VM'}, 'index': 0}, 'pre2': {'type': 'IndexedParameter', 'name': 'IV', 'value': 524.7394545110875, 'links': {0: 'VM'}, 'index': 2}, 'pre3': {'type': 'IndexedParameter', 'name': 'IC', 'value': 524.7394545110875, 'links': {0: 'VM'}, 'index': 1}, 'pre4': {'type': 'IndexedParameter', 'name': 'IF', 'value': 524.7394545110875, 'links': {0: 'VM'}, 'index': 3}}, 'levels': {'level0': {'level': 0, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L0C0', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C0', 'value': -74.94564118324979, 'links': {0: 'OL1C0'}, 'weights': [1.6341416211578872]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C0', 'value': 1049.478909022175, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [0, 1, 0, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C0', 'value': -1124.4245502054248, 'links': {0: 'RL0C0', 1: 'PL0C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C0', 'value': 139.11808813986408, 'links': {0: 'CL0C0'}, 'gain': -0.026775552495458613}}}}, 'col1': {'col': 1, 'node': {'type': 'PCTNode', 'name': 'L0C1', 'refcoll': {'0': {'type': 'EAWeightedSum', 'name': 'RL0C1', 'value': -4243.250035423188, 'links': {0: 'OL1C0'}, 'weights': [-4.641686357807641]}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL0C1', 'value': 524.7394545110875, 'links': {0: 'IP', 1: 'IV', 2: 'IC', 3: 'IF'}, 'weights': [1, 0, 1, 1]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL0C1', 'value': -4767.989489934275, 'links': {0: 'RL0C1', 1: 'PL0C1'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL0C1', 'value': -7940.521427863814, 'links': {0: 'CL0C1'}, 'gain': 1.732928642515625}}}}}}, 'level1': {'level': 1, 'nodes': {'col0': {'col': 0, 'node': {'type': 'PCTNode', 'name': 'L1C0', 'refcoll': {'0': {'type': 'EAConstant', 'name': 'RL1C0', 'value': 11, 'links': {}}}, 'percoll': {'0': {'type': 'EAWeightedSum', 'name': 'PL1C0', 'value': -289.80936012676045, 'links': {0: 'PL0C0', 1: 'PL0C1'}, 'weights': [-0.38235925239252005, 1.4550452218646581]}}, 'comcoll': {'0': {'type': 'Subtract', 'name': 'CL1C0', 'value': 300.80936012676045, 'links': {0: 'RL1C0', 1: 'PL1C0'}}}, 'outcoll': {'0': {'type': 'EAProportional', 'name': 'OL1C0', 'value': 213.97228829114843, 'links': {0: 'CL1C0'}, 'gain': 0.3905924822259278}}}}}}}, 'post': {'post0': {'type': 'EAWeightedSum', 'name': 'Action1', 'value': -354264.9895330735, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [-29.407667283181695, 43.96042688761685]}, 'post1': {'type': 'EAWeightedSum', 'name': 'Action2', 'value': -367824.2177065169, 'links': {0: 'OL0C0', 1: 'OL0C1'}, 'weights': [18.737472543473398, 46.79491542025264]}}}

        # for old, new in zip(old_config, new_config):
        #     # print(old_config[old])
        #     # print(new_config[new])
        #     # print()
        #     self.assertEqual(old_config[old], new_config[new])


    def test_hpctind_mate3(self):        
            ind1 = self.evr.toolbox.individual()   
            ind2 = self.evr.toolbox.individual()   

            child1, child2 = self.evr.toolbox.mate(ind1, ind2)

            child1list = child1.get_parameters_list()
            # print(child1.get_grid())
            # print(child1list)

            self.assertIsNotNone(child1list[0][1][0])

            child2list = child2.get_parameters_list()
            # print(child2.get_grid())
            #print(child2list)

            self.assertIsNotNone(child2list[0][1][0])


if __name__ == '__main__':
    unittest.main()
