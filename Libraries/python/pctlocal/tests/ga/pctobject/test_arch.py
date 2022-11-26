

from eepct.hpct import HPCTArchitecture
from eepct.hpct import HPCTControlFunctionCollection

from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTARCH
from eepct.hpct import HPCTLEVEL


fcoll = HPCTControlFunctionCollection()
fcoll.set_function_property( HPCTFUNCTION.ACTION, HPCTARCH.VARIABLE_TYPE, 'Binary')

arch = HPCTArchitecture()
arch.configure()
print(arch)
print()



#arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTARCH.VARIABLE_PROPERTIES, {'lower': -50, 'upper': 50})
arch.set(HPCTLEVEL.ZERO, HPCTFUNCTION.ACTION, HPCTARCH.VARIABLE_TYPE, 'Binary')
print(arch)

