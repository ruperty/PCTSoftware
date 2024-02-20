import warnings
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter
from os import sep, path, makedirs
from pct.hierarchy import PCTHierarchy
from pct.yaw_module import get_dataset_from_simu, get_comparaison_metrics, test_trad_control, test_hpct_wind, get_properties, get_indexes
from eepct.hpct import evolve_from_properties
from pct.putils import printtime, NumberStats

import warnings 
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from comet_ml import Experiment, api



# with warnings.catch_warnings():
#     warnings.filterwarnings("ignore",category=DeprecationWarning)
from comet_ml import Artifact

def get_environment_properties(root=None, wt='WindTurbine', property_dir=None, property_file=None):

    filename=wt+sep+property_dir+sep+property_file
    file = root + 'data'+sep+'ga'+sep+ filename

    environment_properties = PCTHierarchy.get_environment_properties(file)

    return environment_properties

def wind_turbine_results(environment_properties=None, experiment=None, root=None, wt='WindTurbine', verbose=None, early=None, min=None,
                         comparisons=False, comparisons_print_plots=False, property_dir=None, property_file=None, plots=None, log_testing_to_experiment=False):

    prefix = property_file[:property_file.find(".properties")]
    filename=wt+sep+property_dir+sep+property_file
    file = root + 'data'+sep+'ga'+sep+ filename

    wind_timeseries,start, stop, model_params,yaw_params,keep_history, rt = get_properties(environment_properties)

    history=True
    if 'range' in environment_properties and environment_properties['range']=='test':
        outdir='c:'+sep+'tmp'+sep+'WindTurbine-test'+sep+prefix+sep
    else:
        outdir='c:'+sep+'tmp'+sep+'WindTurbine'+sep+prefix+sep
    makedirs(outdir, exist_ok=True)

    # lastsepIndex = filename.rfind(sep)
    # propIndex = filename.rfind('.properties')
    # filenamePrefix = filename[lastsepIndex+1:propIndex]
    # draw_file = outdir + 'draw-'+filenamePrefix+'.png'
    draw_file = False
    model_file = outdir + 'res_model.html'


    if experiment:
        artifact = Artifact(property_file, "Properties file")
        artifact.add(file)
        experiment.log_artifact(artifact)

    (res_model, nac_pos_model, power_improvement, power_control, power_simu) = test_hpct_wind(
        file=file,plots=plots,history=history,verbose=verbose,outdir=outdir,early=early,draw_file=draw_file, model_file=model_file,
        environment_properties=environment_properties,
        start_index=model_params['start_index_test'],
        stop_index=model_params['stop_index_test'],
        experiment=experiment,
        datatype='test',
        log_testing_to_experiment=log_testing_to_experiment, min=min
        )

    if comparisons:
        start, stop = get_indexes(model_params, environment_properties)

        (res_baseline_simu, nac_pos_baseline_simu, wind_dir) = test_trad_control(
            model_params['wind_timeseries'],
            model_params['wind_timeseries_not_agg'],
            yaw_params['cycle_period'],
            start, #model_params['start_index_test'],
            stop, #model_params['stop_index_test'],
            experiment=experiment,
            datatype='baseline_simu',
            outdir=outdir
            )

        (res_baseline_logs, nac_pos_baseline_logs, wind_dir) = test_trad_control(
            model_params['wind_timeseries'],
            model_params['wind_timeseries_not_agg'],
            yaw_params['cycle_period'],
            start, #model_params['start_index_test'],
            stop, #model_params['stop_index_test'],
            experiment=experiment,
            datatype='baseline_logs',
            outdir=outdir
            )

    rel_net_prod_change=[]
    net_prod_change=[]
    if comparisons_print_plots and comparisons:
        power_prod_change, conso_yaw_change, net_prod_change, rel_net_prod_change,yaw_error_rel_change = get_comparaison_metrics(wind_dir,power_control,power_simu,nac_pos_model, nac_pos_baseline_simu, yaw_params['yaw_rate_max'], yaw_params['yaw_consumption'], 50)    
        fig, axs = plt.subplots(6, sharex=True, figsize=(15,25), gridspec_kw={'height_ratios': [3, 1, 1,1,1,1]})
        plt.xlabel('time (sec)', fontsize=20)
        plt.xlim(0,(model_params['stop_index_test']- model_params['start_index_test'])*yaw_params['cycle_period'])

        axs[0].plot(range(0,(model_params['stop_index_test']- model_params['start_index_test'])*yaw_params['cycle_period'] ,yaw_params['cycle_period']),wind_dir,label='wind direction')
        axs[0].plot(range(0,(model_params['stop_index_test']- model_params['start_index_test'])*yaw_params['cycle_period'] ,yaw_params['cycle_period']),nac_pos_model,linewidth=4.0, label='nacelle position RL algorithm')
        axs[0].plot(range(0,(model_params['stop_index_test']- model_params['start_index_test'])*yaw_params['cycle_period'],yaw_params['cycle_period'] ),nac_pos_baseline_simu,linewidth=4.0, label='nacelle position simulated baseline algorithm')
        axs[0].plot(range(0,(model_params['stop_index_test']- model_params['start_index_test'])*yaw_params['cycle_period'] ,yaw_params['cycle_period']),nac_pos_baseline_logs,linewidth=4.0, label='nacelle position baseline algorithm from logs')
        axs[0].legend(fontsize=20)
        axs[0].tick_params(labelsize=20)
        axs[0].set_ylabel(ylabel='angle (deg)', fontsize=20)

        axs[1].bar(range(0,(model_params['stop_index_test']- model_params['start_index_test'])*yaw_params['cycle_period'] ,yaw_params['cycle_period']*50),yaw_error_rel_change,500,linewidth=4.0, label='RL alg', align='edge')
        axs[1].get_yaxis().set_major_formatter(FuncFormatter(lambda y, _: "{:.1f}%".format(y)))
        axs[1].legend(fontsize=20)
        axs[1].tick_params(labelsize=20)
        axs[1].set_ylabel(ylabel='yaw misaligment \ndecrease (per cent)', fontsize=20,)

        axs[2].bar(range(0,(model_params['stop_index_test']- model_params['start_index_test'])*yaw_params['cycle_period'] ,yaw_params['cycle_period']*50),power_prod_change,500,linewidth=4.0, label='RL alg', align='edge')
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.1f}%".format(y)))
        axs[2].legend(fontsize=20)
        axs[2].tick_params(labelsize=20)
        axs[2].set_ylabel(ylabel='power output \nincrease (kW)', fontsize=20,)

        axs[3].bar(range(0,(model_params['stop_index_test']- model_params['start_index_test'])*yaw_params['cycle_period'] ,yaw_params['cycle_period']*50),conso_yaw_change,500,linewidth=4.0, label='RL alg', align='edge')
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.1f}%".format(y)))
        axs[3].legend(fontsize=20)
        axs[3].tick_params(labelsize=20)
        axs[3].set_ylabel(ylabel='yaw consumption \nincrease (kW)', fontsize=20,)

        axs[4].bar(range(0,(model_params['stop_index_test']- model_params['start_index_test'])*yaw_params['cycle_period'] ,yaw_params['cycle_period']*50),net_prod_change,500,linewidth=4.0, label='RL alg', align='edge')
        axs[4].legend(fontsize=20)
        axs[4].tick_params(labelsize=20)
        axs[4].set_ylabel(ylabel='net power output \nincrease (kW)', fontsize=20,)

        axs[5].bar(range(0,(model_params['stop_index_test']- model_params['start_index_test'])*yaw_params['cycle_period'] ,yaw_params['cycle_period']*50),rel_net_prod_change,500,linewidth=4.0, label='RL alg', align='edge')
        axs[5].get_yaxis().set_major_formatter(FuncFormatter(lambda y, _: "{:.1f}%".format(y)))
        axs[5].legend(fontsize=20)
        axs[5].tick_params(labelsize=20)
        axs[5].set_ylabel(ylabel='net power output \nincrease (per cent)', fontsize=20,)

        fig.tight_layout()
        plt.savefig(outdir + 'steady_dataset',dpi=600)


        fig, axs = plt.subplots(2, sharex=True)
        axs[0].plot(range(model_params['start_index']*yaw_params['cycle_period'],model_params['stop_index']*yaw_params['cycle_period'], yaw_params['cycle_period'] ),wind_timeseries['wind_direction'][model_params['start_index']:model_params['stop_index']],label='train')
        axs[0].plot(range(model_params['start_index_test']*yaw_params['cycle_period'],model_params['stop_index_test']*yaw_params['cycle_period'],yaw_params['cycle_period'] ),wind_timeseries['wind_direction'][model_params['start_index_test']: model_params['stop_index_test']],label='test')
        plt.xlabel('time (sec)')
        axs[1].plot(range(model_params['start_index']*yaw_params['cycle_period'],model_params['stop_index']*yaw_params['cycle_period'], yaw_params['cycle_period'] ),wind_timeseries['wind_speed'][model_params['start_index']:model_params['stop_index']],label='train')
        axs[1].plot(range(model_params['start_index_test']*yaw_params['cycle_period'],model_params['stop_index_test']*yaw_params['cycle_period'],yaw_params['cycle_period'] ),wind_timeseries['wind_speed'][model_params['start_index_test']: model_params['stop_index_test']],label='test')
        plt.setp(axs[1], ylabel='wind speed (m/s)')
        plt.setp(axs[0], ylabel='wind direction (deg)')
        plt.legend()
        plt.savefig(outdir + 'steady_results',dpi=1000)

    if comparisons:    
        print(res_baseline_simu)
        print(res_baseline_logs)

    print(res_model)

    energy_gain =  100*(res_model['power_control']/res_model['power_trad']-1)

    if experiment:
        experiment.log_metric('pc_test_result', res_model['power_control'])
        experiment.log_metric('yaw_count', res_model['yaw count'])
        experiment.log_metric('mean_ye', res_model['average yaw error'])
        experiment.log_metric('energy_gain', energy_gain)


    return energy_gain, power_improvement, power_prod_change, conso_yaw_change, net_prod_change,rel_net_prod_change,yaw_error_rel_change


def evolve_wt_from_properties(args):

    if args and 'log_experiment' in args and args['log_experiment']:
        env_name=args['env_name']
        filename=args['file']
        root = args['root_path']
        pfile = root + args['configs_dir'] + env_name +sep+ filename + ".properties"

        ep = PCTHierarchy.get_environment_properties(pfile)
        ex_name = ep['series']
        args['experiment_name']= ex_name
        args['project_name'] = args['project_name']+"-" + ex_name

        prefix = filename[2:6]	
        final_ex_name = f'{ex_name[0:1]}-{prefix}-{args["seed"]:02}'

        capi = api.API(api_key=args['api_key'])
        experiment_exists = capi.get( workspace=args['workspace'] + '/' + args['project_name'] +'/' + final_ex_name)

        if experiment_exists:
            print("Experiment", final_ex_name, "already exists in", args['project_name'])
            return


        experiment = Experiment(api_key=args['api_key'],
                                project_name=args['project_name'],
                                workspace=args['workspace'])

        # experiment.log_parameters(model_params)
        # experiment.log_code(path.basename(__file__))	
        experiment.set_name(final_ex_name)
    else:
        experiment = None

    args['experiment']=experiment

    start = printtime('Start')

    filepath, experiment = evolve_from_properties(args)
    if filepath is None:
        return
    
    environment_properties=None
    plots=None
    early=None

    if 'log_testing_to_experiment' in args:
        log_testing_to_experiment = args['log_testing_to_experiment']
    else:
        log_testing_to_experiment = False

    index1=filepath.rindex(sep)
    file = filepath[index1+1:]
    # print(file)
    index2=filepath.rindex(sep, 0, index1)
    property_dir=filepath[index2+1:index1]
    # print(property_dir)
    #configs_root=args['root_path']
    drive=args['drive']

    if environment_properties is None:
        environment_properties = get_environment_properties(root=drive, property_dir=property_dir, property_file=file)
        environment_properties['keep_history'] = True
        environment_properties['range'] = 'test'
        # environment_properties['reward_type']= 'power'
        print(environment_properties)

    wind_turbine_results(environment_properties=environment_properties, experiment=experiment, root=drive, verbose=args['verbosed']['hpct_verbose'], 
                        early=early, comparisons=args['comparisons'], comparisons_print_plots=args['comparisons_print_plots'], min= not args['max'],
                        property_dir=property_dir, property_file=file, plots=plots, log_testing_to_experiment=log_testing_to_experiment)

    end = printtime('End')	
    elapsed = end-start        
    print(f'Elapsed time: {elapsed:4.2f}')
    NumberStats.getInstance().report()
    if experiment:
        experiment.end()


