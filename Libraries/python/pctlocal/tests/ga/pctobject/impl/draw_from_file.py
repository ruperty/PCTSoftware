


import argparse
from os import sep, makedirs
from epct.po_evolvers import HPCTIndividual


def drawit(filename=None, outdir=None, move=None, funcdata=False, font_size=6, node_size=200, suffixes=False):

    lastsepIndex = filename.rfind(sep)
    propIndex = filename.rfind('.properties')
    filenamePrefix = filename[lastsepIndex+1:propIndex]
    draw_file = outdir + sep + 'draw-'+filenamePrefix+'.png'

    etype =filename[filename[0:lastsepIndex].rfind(sep)+1:lastsepIndex]

    hpct, hep = HPCTIndividual.from_properties_file(filename)
    env_name = hpct.get_environment().get_name()
    hname = env_name + '\n' + etype + '\nscore=' + f'{float(filenamePrefix[3:10]):0.3f}'
    hpct.set_name(hname)
    hpct.validate_links()
    if suffixes:
        hpct.set_suffixes()
    print(hpct.formatted_config(3))
    # hpct.summary()
    hpct.draw(file=draw_file, move=move, with_edge_labels=True, font_size=font_size, node_size=node_size, funcdata=funcdata)
    print('Image saved to '+draw_file)

    hpct.consolidate()
    move={}
    draw_file = outdir + sep + 'draw-'+filenamePrefix + '_A' +'.png'
    hpct.draw(file=draw_file, move=move, with_edge_labels=True, font_size=font_size, node_size=node_size, funcdata=funcdata)
    print(hpct.formatted_config(3))
    # hpct.summary()
    print('Image saved to '+draw_file)



# python -m impl.draw_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC00-ReferencedInputsError-RootMeanSquareError-Mode00\ga-000.385-s064-2x2-m000-f46606db9aa4aabc0af650882cabb6ac.properties" -o "G:\My Drive\data\ga\MountainCarContinuousV0\MC00-ReferencedInputsError-RootMeanSquareError-Mode00\f46606db9aa4aabc0af650882cabb6ac" -m "{'IV':[0.15,0.2],'IP':[-0.8,0.1], 'OL0C0p':[-0.4,-0.2],'OL0C1p':[0,-0.2], 'OL1C0p':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]}"
# python -m impl.draw_from_file -f "C:\Users\ruper\My Drive\data\ga\MountainCarContinuousV0\MC00-ReferencedInputsError-RootMeanSquareError-Mode00\ga-000.385-s064-2x2-m000-f46606db9aa4aabc0af650882cabb6ac.properties" -o "C:\Users\ruper\My Drive\data\ga\MountainCarContinuousV0\MC00-ReferencedInputsError-RootMeanSquareError-Mode00\f46606db9aa4aabc0af650882cabb6ac" -m "{'IV':[0.15,0.2],'IP':[-0.8,0.1], 'OL0C0p':[-0.4,-0.2],'OL0C1p':[0,-0.2], 'OL1C0p':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]}"

# python -m impl.draw_from_file -f "/mnt/c/Users/ruper/My Drive/data/ga/MountainCarContinuousV0/MC00-ReferencedInputsError-RootMeanSquareError-Mode00/ga-000.385-s064-2x2-m000-f46606db9aa4aabc0af650882cabb6ac.properties" -o "/mnt/c/Users/ruper/My Drive/data/ga/MountainCarContinuousV0/MC00-ReferencedInputsError-RootMeanSquareError-Mode00/f46606db9aa4aabc0af650882cabb6ac" -m "{'IV':[0.15,0.2],'IP':[-0.8,0.1], 'OL0C0p':[-0.4,-0.2],'OL0C1p':[0,-0.2], 'OL1C0p':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]}"

# python -m impl.draw_from_file -f "/mnt/c/Users/ruper/My Drive/data/ga/MountainCarContinuousV0/MC00-ReferencedInputsError-RootMeanSquareError-Mode00/ga-000.385-s064-2x2-m000-f46606db9aa4aabc0af650882cabb6ac.properties" -o "/mnt/c/Users/ruper/My Drive/data/ga/MountainCarContinuousV0/MC00-ReferencedInputsError-RootMeanSquareError-Mode00/f46606db9aa4aabc0af650882cabb6ac" -m "{'IV':[0.15,0.2],'IP':[-0.8,0.1], 'OL0C0p':[-0.4,-0.2],'OL0C1p':[0,-0.2], 'OL1C0p':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]}"

# python -m impl.draw_from_file -f "c:\Users\ruper\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\ga-000.331-s032-2x2-m004-cdf7cc1497ad143c0b04a3d9e72ab783.properties" -o "c:\Users\ruper\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\cdf7cc1497ad143c0b04a3d9e72ab783" -m "{'IV':[0, 0.05],'IP':[-0.6, 0.3],  'OL0C0sm':[-0.28, -0.2],'OL0C1sm':[0.28, -0.2], 'OL1C0sm':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]}"
# python -m impl.draw_from_file -f "c:\Users\ruper\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\ga-000.331-s032-2x2-m004-cdf7cc1497ad143c0b04a3d9e72ab783.properties" -o "c:\Users\ruper\My Drive\data\ga\MountainCarContinuousV0\MC08-ReferencedInputsError-RootMeanSquareError-Mode04\cdf7cc1497ad143c0b04a3d9e72ab783" -m "{}" -d

# python -m impl.draw_from_file -f "testfiles\ga-000.326-s066-2x3-6655-a6abebd2c88246e9f77dd8623eac6e3e.properties" -o "/tmp" -m "{}" -d



"""
python -m impl.draw_from_file -f "G:\My Drive\data\ga\ARC\FitnessError-MovingAverageError-Mode07\ga-000.000-s001-1x1-m007-ARC0095-ae36ff1d4ff2c88b9b856d6d2a540eb6-consolidated.properties" -o "/tmp"  -m "{}" -d -t 12 -n 400

python -m impl.draw_from_file -f 'C:/Users/ryoung/Versioning/python/nbdev/pct/nbs/testfiles/MountainCar/MountainCar-cdf7cc1497ad143c0b04a3d9e72ab783.properties' -o "/tmp" -m "{'IV':[0, 0.05],'IP':[-0.6, 0.3],  'OL0C0sm':[-0.28, -0.2],'OL0C1sm':[0.28, -0.2], 'OL1C0sm':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]}"


"""

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help="file name")
    parser.add_argument('-o', '--outdir', type=str, help="directory to save drawing")
    parser.add_argument('-t', '--font_size',  type=int, help="font size", default="6")
    parser.add_argument('-n', '--node_size',  type=int, help="node size", default="200")
    parser.add_argument("-m", "--move", type=str, help="node positioning")
    parser.add_argument("-d", "--funcdata", help="include function labels", action="store_true")
    parser.add_argument("-s", "--suffixes", help="add function suffixes", action="store_true")

    args = parser.parse_args()

    if args.move is None:
        move = {}
    else:
        move = eval(args.move)

    drawit(filename=args.file, outdir=args.outdir, funcdata=args.funcdata, font_size=args.font_size, node_size=args.node_size, move=move, suffixes=args.suffixes)

