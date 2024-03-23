

import time, csv

# import warnings 
# with warnings.catch_warnings():
#     warnings.filterwarnings("ignore",category=DeprecationWarning)
#     from comet_ml import Experiment


from deap import base, creator
from os import makedirs, sep

from epct.po_architecture import HPCTLEVEL, HPCTVARIABLE
from pct.functions import HPCTFUNCTION

from epct.evolvers import  CommonToolbox
from epct.po_evolvers import HPCTEvolveProperties
from epct.environment_processing import EnvironmentProcessingFactory


# logger = logging.getLogger(__name__)




class HPCTGenerateEvolvers(object):
    "Generate files of evolver properties, from array of options."
    def __init__(self, iters=0, envs=None, collection=None, configs=None, properties=None, varieties=None, common_configs=None):
        if common_configs:
            self.common_configs=common_configs
        else:
            self.common_configs={}

        if iters>0:
            for env in envs:
                makedirs('configs' + sep + env, exist_ok=True)

            for env in envs:
                num_actions = varieties[env]['num_actions']
                nevals = varieties[env]['nevals']
                archs = varieties[env]['archs']
                for arch in archs:
                    key = '_'.join((env,arch['name']))
                    print(key)
                    config = configs[key]
                    self.generate_option_files(iters, env, num_actions, arch, config, nevals, properties, collection)

    def generate_option_files(self, iters, env, num_actions, arch, config, nevals, error_properties, environment_properties, collection, args, fname_list, fargs, cmdline=None):
        "Generate properties file based upon architecture type."
        #print('arch', arch)
        import os
        arch_name = arch['name']
        # inputs_names = arch['inputs_names']
        ppars = ''

        collectors=collection[env]['arch'][arch_name]['collectors']
        responses=collection[env]['arch'][arch_name]['responses']
        structs=collection[env]['arch'][arch_name]['structs']

        #print('collection', collection)

        #print('config', config)
        for collector in collectors:
            for response in responses:
                    for struct in structs:
                        desc, filename = self.description(collector,response,  f'Mode{struct["mode"]:02}', arch_name)
                        if len(fargs)>0:
                            fname_list.append(f'{filename} {fargs}')
                        else:
                            fname_list.append(filename)
                        fpars = self.fixed_parameters(env, arch, num_actions, environment_properties)
                        cpars = self.configurable_parameters( config, collector, response, nevals)
                        ppars = self.additional_properties(error_properties, response, collector)
                        spars = self.structure_parameters(collector,response,  struct, arch_name)
                        # display = f'### Display\n\ninputs_names = {inputs_names}\n'
                        
                        text = '\n'.join((desc, fpars, cpars, ppars, spars))
                        filedir = f'configs{sep}{env}'
                        makedirs(filedir, exist_ok=True)
                        filepath = f'configs{sep}{env}{sep}{filename}.properties'
                        self.write_to_file(filepath, text)
                        # cmd = f'python examples{sep}evolve.py {env} {filename} -p 666X' # -i {iters}'
                        flist = [filename]
                        cmd = f'python -m {cmdline} {env} "{flist}" {fargs} {args}'
                        print(cmd, end='\n')
                        # print(f'set WW_CONFIG={filename}')
                
    def get_arch_types_from_shortcode(self, codes):
        rtn = ""
        
        arr = codes.split('^')
        for code in arr:
            if code == 'scTopVars':
                rtn = rtn + "zerotop^ref^Float~EAVariable~{ 'lower_float': -1,'upper_float': 1}|top^ref^Float~EAVariable~{ 'lower_float': -1,'upper_float': 1}"
            
            if code == 'scActBinSig':
                delimiter = ""
                if len(rtn)>0:
                    delimiter = "|"
                rtn = rtn + delimiter + "zero^act^Binary~EASigmoidSmoothWeightedSum~{ 'lower_float': -1,'upper_float': 1, 'lower_range':0, 'upper_range':100, 'lower_slope' : 0, 'upper_slope': 50}"

        return rtn


    def process_archtypes(self, arch_types):
        if arch_types.startswith('['):
            return eval(arch_types)

        if arch_types.startswith('sc'):
            arch_types = self.get_arch_types_from_shortcode(arch_types)

        lookup = {'zero': HPCTLEVEL.ZERO,'zerotop': HPCTLEVEL.ZEROTOP, 'top': HPCTLEVEL.TOP, 
                  'ref': HPCTFUNCTION.REFERENCE, 'per': HPCTFUNCTION.PERCEPTION, 'com': HPCTFUNCTION.COMPARATOR, 
                  'out': HPCTFUNCTION.OUTPUT, 'act': HPCTFUNCTION.ACTION  }

        arr = arch_types.split('|')
        # print(arr)
        all = []
        for item in arr:
            elements = item.split('^')
            level = lookup[elements[0]]
            func = lookup[elements[1]]
            values = elements[2].split('~')
            var = [level, func, HPCTVARIABLE.TYPE, values[0]]
            cls = [level, func, HPCTVARIABLE.FUNCTION_CLASS, values[1]]
            props = [level, func, HPCTVARIABLE.PROPERTIES, eval(values[2])]
            all.append(var)
            all.append(cls)
            all.append(props)

        pass
        return all

    def get_config_value(self, record, key):
        if key in record:
            value = record[key]
        else:
            if key in self.common_configs:
                value = self.common_configs[key]
            else:
                raise Exception(f'Config value for <{key}> must be specified in csv file or on cmd line.')

        return value

    def process_csv(self, file, args="", cmdline=None, initial_index=1, batch=1000):
        with open(file, 'r', encoding='utf-16') as csvfile:
            reader = csv.reader(csvfile)
            fname_list = []
            batches = []
            actr=initial_index
            for row in reader:
                # print(row)
                if reader.line_num==1:
                    header = row
                else:
                    record = {}
                    for ctr, item in enumerate(header):
                        record[item] = row[ctr]
                        
                    #print(record)

                    arch_name = self.get_config_value(record, 'arch_name')
                    aname = f'{arch_name}{actr:04}'

                    arch_props = {}
                    arch_props['collectors']=[record['error_collector']]
                    arch_props['responses']=[record['error_response']]
                    structs = {}
                    if record['arch_types'] == '':
                        structs['types'] = []
                    else:
                        structs['types'] = self.process_archtypes(record['arch_types']) 
                    structs['mode'] = eval(record['arch_mode'])  
                    arch_props['structs']=[structs]
                    arch_config={}
                    arch_config[aname]=arch_props
                    archs={}
                    archs['arch']=arch_config                
                    collection={}
                    
                    env = self.get_config_value(record, 'env')
                    collection[env]=archs
                    #print()
                    #print(collection)
                    
                    config={}
                    seed = self.get_config_value(record, 'seed')
                    config['seed'] = seed

                    # if record['seed'] == '':
                    #     config['seed'] = None
                    # else:
                    #     config['seed']=eval(record['seed'])

                    config['pop_size'] = self.get_config_value(record, 'pop_size')
                    config['gens']= self.get_config_value(record, 'gens')
                    config['attr_mut_pb']= self.get_config_value(record, 'attr_mut_pb')
                    config['structurepb']= self.get_config_value(record, 'structurepb')
                    config['runs']= self.get_config_value(record, 'runs')
                    config['lower_float']= self.get_config_value(record, 'lower_float') 
                    config['upper_float']= self.get_config_value(record, 'upper_float')
                    config['min_levels_limit']= self.get_config_value(record, 'min_levels_limit')
                    config['min_columns_limit']= self.get_config_value(record, 'min_columns_limit')
                    config['max_levels_limit']= self.get_config_value(record, 'max_levels_limit')
                    config['max_columns_limit']= self.get_config_value(record, 'max_columns_limit')
                    early_termination = self.get_config_value(record, 'early_termination')
                    config['early_termination'] = early_termination 

                    if early_termination == 'TRUE':
                        config['early_termination']=True 
                    if early_termination == 'FALSE':
                        config['early_termination']=False

                    error_limit = self.get_config_value(record, 'error_limit')

                    if error_limit == '':
                        config['error_limit']=None    
                    else:
                        config['error_limit']=error_limit

                    config['p_crossover']= self.get_config_value(record, 'p_crossover')
                    config['p_mutation']= self.get_config_value(record, 'p_mutation')
                    
                    ep = self.get_config_value(record, 'error_properties')                     
                    if ep is None or ep == '':
                        error_properties=None
                    else:
                        error_properties=eval(record['error_properties']) 

                    envp = self.get_config_value(record, 'environment_properties')    
                    if envp is None or envp == '':
                        environment_properties=None
                    else:
                        environment_properties=envp 
                    
                    arch={}
                    arch['name']=aname
                    arch['env_inputs_indexes']=eval(record['env_inputs_indexes'])
                    if len(record['zerolevel_inputs_indexes']) > 0:
                        arch['zerolevel_inputs_indexes']=eval(record['zerolevel_inputs_indexes'])
                    if len(record['toplevel_inputs_indexes']) > 0:
                        arch['toplevel_inputs_indexes']=eval(record['toplevel_inputs_indexes'])
                    arch['references']=eval(record['references'])
                    arch['env_inputs_names']=record['env_inputs_names']

                    fargs = record['args']

                    num_actions = self.get_config_value(record, 'num_actions')
                    num_evals = self.get_config_value(record, 'num_evals')

                    self.generate_option_files(1, env, num_actions, arch, config, num_evals, error_properties, environment_properties, collection, args, fname_list, fargs, cmdline=cmdline)
                    if ((actr - initial_index)+1) % batch == 0:
                        cmd = f'python -m {cmdline} {env} "{fname_list}" {args}'
                        batches.append(cmd)
                        # print(cmd, end='\n')
                        fname_list = []

                    actr=actr+1

            cmd = f'python -m {cmdline} {env} "{fname_list}" {args}'
            batches.append(cmd)

            for cmd in batches:
                print()
                print(cmd, end='\n')
            pass



    def additional_properties(self, error_properties, response, collector):
        "Add additional properties such as error function parameters."
        ppars = ''

        if error_properties is None:
            return ppars                        
            
        
        if len(error_properties)>0:
            ppars='### Additional properties\n\n'

        ctr = 1
        for  prop in error_properties:
            value = error_properties[prop]
            if response == 'SmoothError' and prop == 'error:smooth_factor':
                propstr = f'property{ctr} = {prop},{value}'        
                ppars = ''.join((ppars, propstr, '\n'))
                ctr+=1
            
            if collector == 'ReferencedInputsError' and  prop == 'error:referenced_inputs':
                propstr = f'property{ctr} = {prop},{value}'        
                ppars = ''.join((ppars, propstr, '\n'))
                ctr+=1
                

        return ppars                        

    def environment_properties(self, environment_properties):
        "Add additional environment properties."
        epars = ''

        if environment_properties is None:
            return epars                        
            
        epars=f'### Environment properties\n\nenvironment_properties={environment_properties}'

        return epars                        


    def write_to_file(self, file, text):
        "Write text to file."
        f = open(file, "w")
        f.write(text)
        f.close()

    def structure_parameters(self, collector,response,  struct, arch):
        "Add the hierarchy architecture configuration and additional parameters."
        header = '### Structure\n\n'
        header = header + '# modes - pattern of nodes at particular levels, zero, n, top and zerotop\n'
        header = header + '# the mode numbers refer to:\n'
        header = header + '# 0 - per:bin-ws, ref:flt-ws, com:sub, out:flt-ws\n'

        mode = struct['mode']
        # if struct == 'SmoothWeightedSum':
        #     modes = [6, 6, 5, 5]
            
        mstr = f'mode = {mode}'
        type_num = 1
        types = ''

        for type in struct['types']:
            if len(type)>4:
                types = ''.join((types, f'type{type_num} = HPCTLEVEL.{type[0].name}^HPCTFUNCTION.{type[1].name}^HPCTVARIABLE.{type[2].name}^{type[3]}^HPCTVARIABLE.{type[4].name}^{type[5]}^HPCTVARIABLE.{type[6].name}^{type[7]}\n'))
            else:
                types = ''.join((types, f'type{type_num} = HPCTLEVEL.{type[0].name}^HPCTFUNCTION.{type[1].name}^HPCTVARIABLE.{type[2].name}^{type[3]}\n'))            
            type_num += 1

        types = types + '\n\n\n\n'
            
        
        rtn = '\n'.join((header, mstr, types))
        return rtn


    def configurable_parameters(self,  config, collector, response, nevals):  
        "Main configuration parameters of environment evolution."
        header = ''.join(("### Configurable parameters\n\n# Randomisation seed to reproduce results\n# Size of population\n", 
                        "# Number of generations\n# Probability that an attribute will be mutated\n# Probability that the structure will be mutated\n",
                        "# Number of runs of environment\n# Lower limit of float values\n# Upper limit of float values\n",
                        "# Initial limit of levels\n# Initial limit of columns\n# Lower limit of levels\n# Lower limit of columns\n",
                        "# Limit of error on which to terminate individual evaluation\n# Probability for crossover\n# Probability for mutating an individual\n# Number of times the evaulation is run (with different random seeds)\n# Type of errors collected\n# Error function\n\n"))

        text = ''
        for key in config.keys():
            value = config[key]
            text = ''.join((text, key, ' = ', f'{value}', '\n'))
        
        text = ''.join((header, text, f'nevals = {nevals}\nerror_collector_type = {collector}\nerror_response_type = {response}\n'))
        
        #f'seed = {seed}\nPOPULATION_SIZE = {POPULATION_SIZE}\nMAX_GENERATIONS = {MAX_GENERATIONS}\nattr_mut_pb={attr_mut_pb}\nstructurepb={structurepb}\nruns={runs}\nlower_float = {lower_float}\nupper_float = {upper_float}\nlevels_limit = {levels_limit}\ncolumns_limit = {columns_limit}\nerror_limit = {error_limit}\np_crossover = {p_crossover}\np_mutation = {p_mutation}\nnevals = {nevals}\nerror_collector = {error_collector}\nerror_response = {error_response}\n'
        return text
        

    def description(self, collector,response, mode, arch):
        "Define the description and filename."
        filename = '-'.join((arch, collector,response, mode))
        desc = '-'.join((collector,response, mode))
        rtn = ''.join(('\n### Description:\n\n','desc = ', desc,'\n', 'arch_name = ', arch, '\n'))
        return rtn, filename

    def fixed_parameters(self, env, option, num_actions, environment_properties):  
        "List the fixed parameters of the environment."
        header = '### Environment parameters\n\n# Full list of input indexes from environment\n# List of input indexes from environment for zero level if not full\n# List of input indexes from environment for top level# List of reference values\n# Number of actions\n# Display names for environment inputs\n\n'
        
        text1 = f'env_name = {env}\n' 
        text1 = text1 + f'env_inputs_indexes = {self.get_parameter(option, "env_inputs_indexes")}\n'
        text1 = text1 + f'zerolevel_inputs_indexes = {self.get_parameter(option, "zerolevel_inputs_indexes")}\n'
        text1 = text1 + f'toplevel_inputs_indexes = {self.get_parameter(option, "toplevel_inputs_indexes")}\n'
        text1 = text1 + f'references = {self.get_parameter(option, "references")}\n'
        text1 = text1 + f'num_actions = {num_actions}\n'
        text1 = text1 + f'env_inputs_names = {self.get_parameter(option, "env_inputs_names")}\n'
        
        if environment_properties is not None:
            text1 = text1 + f'environment_properties={environment_properties}\n'
        
        return ''.join((header,text1))    

    def get_parameter(self, pdict, name, default=None):
        "Get a parameter from a dictionary."
        if name in pdict:
            return pdict[name]

        return default
    

    
    
