

from eepct.hpct import HPCTArchitecture
from eepct.hpct import HPCTControlFunctionCollection
from eepct.hpct import HPCTControlFunctionProperties

from eepct.hpct import HPCTFUNCTION
from eepct.hpct import HPCTARCH
from eepct.hpct import HPCTVARIABLE

lower_float=-5 
upper_float=5

props = {HPCTVARIABLE.TYPE: 'Float', HPCTVARIABLE.FUNCTION_CLASS: 'EAWeightedSum', HPCTVARIABLE.PROPERTIES: {'lower': lower_float, 'upper': upper_float}}
                     

action=HPCTControlFunctionProperties.from_properties(props)

fcoll = HPCTControlFunctionCollection(action=action)
print(fcoll.action)

fcoll.set_function_property( HPCTFUNCTION.ACTION, HPCTVARIABLE.TYPE, 'Binary')

print(fcoll.action)
print()
print(fcoll)



