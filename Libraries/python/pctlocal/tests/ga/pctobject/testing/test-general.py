
from pct.putils import FunctionsList
from pct.functions import Constant

test = 2
if test == 0:
    str_list = ['a', 'b']
    formatted = ' '.join(str_list)
    print(formatted)
        
if test == 1:
    # simple delete
    c = Constant(11)
    FunctionsList.getInstance().report()
    FunctionsList.getInstance().delete_function(c.namespace, c.name)
    FunctionsList.getInstance().report()


def format_list(alist, formatted):
    if isinstance(alist[0], float):
        # str_list = ['[']
        # str_list.append([f'{num:0.3f}' for num in alist])
        # str_list.append(']')
        return [round(num,3) for num in alist]
    else:
        for item in alist:    
            formatted.append(format_list(item, formatted))
            
    
            
                            
if test == 2:
    lists =  [[-0.20280445403006664, -0.30561588932079725], [-1.109996740904304, -0.31602389805294073, -0.5475055584320996]]
    formatted=[]
    format_list(lists,formatted)
    print(formatted)