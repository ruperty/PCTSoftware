

from eepct.hpct import HPCTArchitecture, HPCTIndividual

from utils.paths import  get_gdrive

from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTARCH
from eepct.hpct import HPCTLEVEL
from eepct.hpct import HPCTVARIABLE



file = get_gdrive() + 'data/ga/CartPoleV1/Std-InputsError-RootMeanSquareError-Mode00/ga-000.124-s001-1x1-m0-a8ab4cf3151b29a13abb2680bc574781.properties'
hpct = HPCTIndividual.from_properties_file(file)


arch = hpct.arch
print(arch)


# arch.configure()
# print(arch)
# print()



# arch.set(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION, HPCTVARIABLE.PROPERTIES, {'lower': -50, 'upper': 50})
# arch.set(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.OUTPUT, HPCTVARIABLE.TYPE, 'Binary')
# print(arch)

