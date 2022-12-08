

from eepct.hpct import HPCTArchitecture
from eepct.hpct import HPCTControlFunctionCollection

from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTARCH
from eepct.hpct import HPCTLEVEL
from eepct.hpct import HPCTVARIABLE


arch = HPCTArchitecture()

arch.configure()
print(arch)
print()



arch.set(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION, HPCTVARIABLE.PROPERTIES, {'lower': -50, 'upper': 50})
arch.set(HPCTLEVEL.ZEROTOP, HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary')
print(arch)

