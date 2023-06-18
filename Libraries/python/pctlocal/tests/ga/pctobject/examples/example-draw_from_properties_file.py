from os import sep, makedirs

from cutils.paths import get_gdrive
from eepct.hpct import HPCTIndividual

test = 0


def drawit(datum, funcdata=False, env_name=None):
    root = get_gdrive() 

    filename = datum[1]
    dir = datum[2]
    move = datum[3]
    filepath = dir + sep + filename + '.properties'
    # hname = env_name + '\n' + dir + '\nscore=' + f'{float(filename[3:10]):0.3f}'
    hname = env_name + ' ' + dir + ' score=' + f'{float(filename[3:10]):0.3f}'
    font_size, node_size = 6, 200
    file = get_gdrive() + 'data'+sep+'ga'+sep+env_name + sep + filepath

    end = len(filename)
    outdir =  root + 'data'+sep+'ga'+sep + env_name + sep + dir+ sep + filename[end-32:end]

    # outdir = 'output' + sep + dir
    # makedirs(outdir, exist_ok=True)
    draw_file = outdir + sep + 'draw-'+filename+'.png'

    hpct, hep = HPCTIndividual.from_properties_file(file)
    hpct.set_name(hname)
    hpct.set_suffixes()
    # print(hpct.formatted_config(3))
    hpct.draw(file=draw_file, move=move, with_edge_labels=True,
              font_size=font_size, node_size=node_size, funcdata=funcdata)
    print('Image saved to '+draw_file)


data = [
    [0, 'ga-000.115-s001-2x3-m000-4292b6128e13ac2df54fd2c05a34292e', 'Std00-InputsError-RootMeanSquareError-Mode00',
        {'CartPoleV1': [-0.6, -0.4], 'ICV': [0, -0.1], 'ICP': [0,  -0.1], 'IPV': [0.0, -0.1], 'IPA': [0.0, -0.1], 'Action1ws': [-0.3, -0.4]}],
    [1, 'ga-000.116-s001-1x1-m000-6bd76f9ddbae2f74dc89419548c380c2', 'Std01-InputsError-RootMeanSquareError-Mode00',
     {'CartPoleV1': [-1, 0.2], 'ICV': [-0.4, 0.3], 'ICP': [-0.2,  0.4],         'IPV': [0, 0.5], 'IPA': [0.2, 0.6], 'Action1ws': [-1, 0.2], 'OL0C0p': [0, 0.1]}],
    [2, 'ga-000.115-s001-3x3-m001-8d51aa0f1ee8987d5ff5e661b62d62f7', 'Std00-InputsError-RootMeanSquareError-Mode01',
        {'CartPoleV1': [-0.4, -0.5], 'ICV': [0, -0.1], 'ICP': [0,  -0.1],           'IPV': [0.0, -0.1], 'IPA': [0.0, -0.1], 'Action1ws': [-0.25, -0.3]}],
    [3, 'ga-000.123-s001-1x1-m001-d1be23c359e86c3de89401d212089832', 'Std01-InputsError-RootMeanSquareError-Mode01',
     {'CartPoleV1': [-1, 0.2], 'ICV': [-0.4, 0.3], 'ICP': [-0.2,  0.4],           'IPV': [0, 0.5], 'IPA': [0.2, 0.6], 'Action1ws': [-1, 0.2], 'OL0C0p': [0, 0.1]}],
    [4, 'ga-000.002-s001-1x1-m000-e520958366bfba4b869fe767b36f60da', 'Std00-TotalError-RootMeanSquareError-Mode00',
     {'CartPoleV1': [-1, 0.2], 'ICV': [-0.4, 0.3], 'ICP': [-0.2,  0.4],           'IPV': [0, 0.5], 'IPA': [0.2, 0.6], 'Action1ws': [-1, 0.2], 'OL0C0p': [0, 0.1]}],
    [5, 'ga-000.011-s001-1x1-m000-8bd4af6075e0ed84db5abff8863e120c', 'Std01-TotalError-RootMeanSquareError-Mode00',
        {'CartPoleV1': [-1, 0.2], 'ICV': [-0.4, 0.3], 'ICP': [-0.2,  0.4],           'IPV': [0, 0.5], 'IPA': [0.2, 0.6], 'Action1ws': [-1, 0.2], 'OL0C0p': [0, 0.1]}],
    [6, 'ga-000.063-s001-2x1-m001-a21ecb826145632a9624ba199d9e93bb', 'Std00-TotalError-RootMeanSquareError-Mode01',
        {'CartPoleV1': [-0.6, 0], 'ICV': [-0.2, 0.3], 'ICP': [0,  0.4],  'IPV': [0.2, 0.5], 'IPA': [0.4, 0.6], 'Action1ws': [-0.65, 0], 'OL0C0p': [0, 0.1]}],
    [7, 'ga-000.065-s001-1x1-m001-a902324b273132c2a0481cc2f48e68a5', 'Std01-TotalError-RootMeanSquareError-Mode01',
        {'CartPoleV1': [-1, 0.2], 'ICV': [-0.4, 0.3], 'ICP': [-0.2,  0.4],           'IPV': [0, 0.5], 'IPA': [0.2, 0.6], 'Action1ws': [-1, 0.2], 'OL0C0p': [0, 0.1]}],

    [8, 'ga-000.116-s001-1x1-m000-c046ca4614c64a3fd02baca87d33992e', 'Std02-InputsError-RootMeanSquareError-Mode00',
        {'CartPoleV1': [-1, 0.2], 'ICV': [-0.4, 0.3], 'ICP': [-0.2,  0.4],           'IPV': [0, 0.5], 'IPA': [0.2, 0.6], 'Action1ws': [-1, 0.2], 'OL0C0p': [0, 0.1]}],
    [9, 'ga-000.123-s001-1x1-m001-3c4731f243d746771f7cb639d8f0095a', 'Std02-InputsError-RootMeanSquareError-Mode01',
     {'CartPoleV1': [-1, 0.2], 'ICV': [-0.4, 0.3], 'ICP': [-0.2,  0.4],           'IPV': [0, 0.5], 'IPA': [0.2, 0.6], 'Action1ws': [-1, 0.2], 'OL0C0p': [0, 0.1]}],

    [10, 'ga-000.130-s001-2x1-m002-9729cd44431b1958b69da786b4ba4f00', 'Std00-InputsError-RootMeanSquareError-Mode02',
     {'CartPoleV1': [-0.6, -0.1], 'ICV': [-0.3, 0.1], 'ICP': [-0.1,  0.2], 'IPV': [0.1, 0.3], 'IPA': [0.3, 0.4], 'Action1ws': [-0.65, 0]}],
    [11, 'ga-000.113-s001-1x1-m000-cfe004e44e94d469055bc00d7aac892f', 'Std03-InputsError-RootMeanSquareError-Mode00',
     {'CartPoleV1': [-1, 0.2], 'ICV': [-0.4, 0.3], 'ICP': [-0.2,  0.4],           'IPV': [0, 0.5], 'IPA': [0.2, 0.6], 'Action1ws': [-1, 0.2], 'OL0C0p': [0, 0.1]}],
    [12, 'ga-000.114-s001-1x1-m000-e951b3484d28b6fa411d2879d3269abf', 'Std03-InputsError-RootMeanSquareError-Mode00',
     {'CartPoleV1': [-1, 0.2], 'ICV': [-0.4, 0.3], 'ICP': [-0.2,  0.4],           'IPV': [0, 0.5], 'IPA': [0.2, 0.6], 'Action1ws': [-1, 0.2], 'OL0C0p': [0, 0.1]}]



]


if test == 100:
    for datum in data:
        drawit(datum)


if test == 0:
    env_name = 'CartPoleV1'
    funcdata = True
    drawit(data[12], env_name=env_name, funcdata=funcdata)
