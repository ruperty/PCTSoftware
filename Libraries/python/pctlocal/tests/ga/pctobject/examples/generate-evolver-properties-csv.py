# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 2023

@author: ryoung
"""

import os

from eepct.hpct import HPCTGenerateEvolvers

from eepct.hpct import HPCTLEVEL
from eepct.hpct import HPCTVARIABLE
from pct.functions import HPCTFUNCTION

test = 1

if test == 1:
    file = 'configs'+ os.sep + 'configs-cp.csv'

if test == 2:
    file = 'configs'+ os.sep + 'configs-ww.csv'




hge = HPCTGenerateEvolvers()  

hge.process_csv(file)
