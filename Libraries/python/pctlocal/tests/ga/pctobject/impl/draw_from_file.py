


import argparse
from os import sep, makedirs
from eepct.hpct import HPCTIndividual


def drawit(filename=None, outdir=None, move=None, funcdata=False, font_size=6, node_size=200):

    lastsepIndex = filename.rfind(sep)
    propIndex = filename.rfind('.properties')
    filenamePrefix = filename[lastsepIndex+1:propIndex]
    draw_file = outdir + sep + 'draw-'+filenamePrefix+'.png'

    etype =filename[filename[0:lastsepIndex].rfind(sep)+1:lastsepIndex]

    hpct, hep = HPCTIndividual.from_properties_file(filename)
    env_name = hpct.get_environment().get_name()
    hname = env_name + '\n' + etype + '\nscore=' + f'{float(filenamePrefix[3:10]):0.3f}'
    hpct.set_name(hname)
    hpct.set_suffixes()
    # print(hpct.formatted_config(3))
    hpct.draw(file=draw_file, move=move, with_edge_labels=True, font_size=font_size, node_size=node_size, funcdata=funcdata)
    print('Image saved to '+draw_file)


# python -m impl.draw_from_file -f "G:\My Drive\data\ga\MountainCarContinuousV0\MC00-ReferencedInputsError-RootMeanSquareError-Mode00\ga-000.385-s064-2x2-m000-f46606db9aa4aabc0af650882cabb6ac.properties" -o "G:\My Drive\data\ga\MountainCarContinuousV0\MC00-ReferencedInputsError-RootMeanSquareError-Mode00\f46606db9aa4aabc0af650882cabb6ac" -m "{'IV':[0.15,0.2],'IP':[-0.8,0.1], 'OL0C0sm':[-0.4,-0.2],'OL0C1sm':[0,-0.2],'OL0C2sm':[0.4,-0.2], 'OL1C0sm':[0,-0.1], 'MountainCarContinuousV0':[-.7,-0.5], 'Action1ws':[-0.4,-0.3]}"

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help="file name")
    parser.add_argument('-o', '--outdir', type=str, help="directory to save drawing")
    parser.add_argument('-t', '--font_size',  type=int, help="font size", default="6")
    parser.add_argument('-n', '--node_size',  type=int, help="node size", default="200")
    parser.add_argument("-m", "--move", type=str, help="node positioning")
    parser.add_argument("-d", "--funcdata", help="include function labels", action="store_true")

    args = parser.parse_args()

    drawit(filename=args.file, outdir=args.outdir, funcdata=args.funcdata, font_size=args.font_size, node_size=args.node_size, move=eval(args.move))

