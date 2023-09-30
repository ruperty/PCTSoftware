
import argparse
from os import sep, listdir
from cutils.paths import  get_gdrive
from pct.hierarchy import PCTHierarchy

# py -m impl.run_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\ga-000.548-s013-2x2-m004-5a08e6cdc09769db0267a14f0634b051.properties"
# py -m impl.run_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC06-ReferencedInputsError-RootMeanSquareError-Mode03\ga-000.554-s068-2x2-m003-5342c97128d9ad23a0fea14a6d9c05e5.properties"
# python -m impl.run_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC04-ReferencedInputsError-RootMeanSquareError-Mode02\ga-000.632-s072-2x2-m002-89f5392f56c60cdc79cf108aa20461ce.properties"
# python -m impl.run_from_file -f "G:\My Drive\data\ga\testfiles\ga-000.334-s068-2x2-6655-8193255f62b3d17188329b5537b3631d-pctobject.properties"

# python -m impl.run_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC04-ReferencedInputsError-RootMeanSquareError-Mode02\ga-000.380-s008-2x2-m002-90b3f2cfd2a1cb0235ad8f8178608f35.properties"

# python -m impl.run_from_file -f "c:\Users\ruper\My Drive\data\ga\MountainCarContinuousV0\MC00-ReferencedInputsError-RootMeanSquareError-Mode00\ga-000.385-s064-2x2-m000-f46606db9aa4aabc0af650882cabb6ac.properties"

# python -m impl.run_from_file -f "c:\Users\ruper\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\ga-000.331-s032-2x2-m004-cdf7cc1497ad143c0b04a3d9e72ab783.properties"
# python -m impl.run_from_file -f "c:\Users\ruper\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\ga-000.331-s032-2x2-m004-cdf7cc1497ad143c0b04a3d9e72ab783.properties" -p "[{'plot_items': {'IP':'ip', 'IV':'iv'},'title':'Inputs'}, {'plot_items': {'OL0C1sm':'out1'}, 'title':'Output1'}, {'plot_items': {'OL0C0sm':'out0', 'OL0C2sm':'out2'}, 'title':'Output'}, {'plot_items': {'Action1ws':'act'}, 'title':'Action'}]"

# python -m impl.run_from_file -f "G:\My Drive\data\ga\Pendulum\PM09-RewardError-RootMeanSquareError-Mode04\ga-001.997-s093-3x5-m004-117f9e29a6b0cb384d1ff062f4042bc3.properties"

# python -m impl.run_from_file -f "G:\My Drive\data\ga\WindTurbine\RewardError-RootMeanSquareError-Mode00\ga-10029.013-s001-5x5-m000-WT02-b4354dca23203327d0d71349f5990f93.properties" -p "[ {'plot_items': {'IWD':'wd'}, 'title':'Wind'},  {'plot_items': {'Action1ws':'out'}, 'title':'Output'}]" -o "c:/tmp" -ep "{'series': 'steady', 'zero_threshold': 1, 'range':'test'}"



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help="file name")
    parser.add_argument('-r', '--runs', type=int, help="number of runs", default="500")
    parser.add_argument('-e', '--early', help="early termination", action="store_true")
    parser.add_argument('-d', '--display', help="display environment", action="store_false")
    parser.add_argument("-v", "--verbose", help="print output ", action="store_true")
    parser.add_argument("-s", "--seed", type=int, help="seed value", default="1")
    parser.add_argument("-p", "--plots", type=str, help="plots definition")
    parser.add_argument('-o', '--outdir', type=str, help="directory to save plots")
    parser.add_argument('-ep', '--eprops', type=str, help="environment properties")

    args = parser.parse_args()

    eprops = None
    if args.eprops is not None:
        eprops = eval(args.eprops)
    plots = args.plots
    if plots is not None:
        plots=eval(plots)
        history=True
    else:
        history=False

    try:
        hierarchy, score = PCTHierarchy.run_from_file(args.file, env_props=eprops, seed=args.seed, render=args.display, move=None, plots=plots, history=history, hpct_verbose= args.verbose, runs=None, outdir=args.outdir, early_termination=args.early)
        print(f'Score={score:0.3f}')
    except FileNotFoundError:
        print(f'File {args.file} does not exist.')
    




