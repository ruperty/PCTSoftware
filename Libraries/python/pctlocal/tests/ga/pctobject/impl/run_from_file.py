
import argparse
from os import sep, listdir
from cutils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual, HPCTEvolveProperties

# py -m impl.run_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\ga-000.548-s013-2x2-m004-5a08e6cdc09769db0267a14f0634b051.properties"
# py -m impl.run_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC06-ReferencedInputsError-RootMeanSquareError-Mode03\ga-000.554-s068-2x2-m003-5342c97128d9ad23a0fea14a6d9c05e5.properties"
# py -m impl.run_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC04-ReferencedInputsError-RootMeanSquareError-Mode02\ga-000.632-s072-2x2-m002-89f5392f56c60cdc79cf108aa20461ce.properties"
# python -m impl.run_from_file -f "G:\My Drive\data\ga\testfiles\ga-000.334-s068-2x2-6655-8193255f62b3d17188329b5537b3631d-pctobject.properties"



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help="file name")
    parser.add_argument('-r', '--runs', type=int, help="number of runs", default="500")
    parser.add_argument('-e', '--early', help="early termination", action="store_true")
    parser.add_argument('-d', '--display', help="display environment", action="store_false")

    args = parser.parse_args()
    file = args.file 
    runs = args.runs 
    early = args.early 
    render = args.display


    # file = 'G:\My Drive\data\ga\MountainCarContinuousV0\MC00-ReferencedInputsError-RootMeanSquareError-Mode03\ga-000.631-s066-2x2-m003-eb57dceed66c7697c01c54617cb106ff.properties'
    # file = 'G:\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\ga-000.548-s013-2x2-m004-5a08e6cdc09769db0267a14f0634b051.properties'

    score = HPCTIndividual.run_from_file(file, render=render, history=False, move=None, plots=None, hpct_verbose= False, runs=None, outdir=None, early_termination=early)
     
    
    print(f'Score={score:0.3f}')




