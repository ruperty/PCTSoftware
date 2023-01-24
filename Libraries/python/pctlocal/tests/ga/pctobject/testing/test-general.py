
from pct.putils import FunctionsList
from pct.functions import Constant

test = 1

if test == 1:
    # simple delete
    c = Constant(11)
    FunctionsList.getInstance().report()
    FunctionsList.getInstance().delete_function(c.namespace, c.name)
    FunctionsList.getInstance().report()



