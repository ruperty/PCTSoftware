

from eepct.hpct import HPCTArchitecture
from eepct.hpct import HPCTARCH

arch = HPCTArchitecture()
arch.configure()
print(arch)
print()

arch.set(HPCTARCH.ZERO, HPCTARCH.ACTION, HPCTARCH.VARIABLE_PROPERTIES, {'lower': -50, 'upper': 50})
arch.set(HPCTARCH.ZERO, HPCTARCH.ACTION, HPCTARCH.VARIABLE_TYPE, 'Binary')
print(arch)

test 