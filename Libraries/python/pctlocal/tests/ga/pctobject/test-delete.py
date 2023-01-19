import sys
import gc
from pct.putils import FunctionsList
from pct.functions import Constant, Proportional

def list_gc_functions():
    objs = gc.get_objects()
    for obj in objs:
        if  obj.__class__.__name__.find('function') >= 0:
            print(obj.__class__.__name__, obj)
    

def list_gc():
    objs = gc.get_objects()
    for obj in objs:
        print(obj)
        print()
        
def list_gc_dicts(name):
    print('--- gc dict')
    objs = gc.get_objects()
    ctr = 0
    for obj in objs:
        if isinstance(obj, dict):
            name = name.lower()
            if name in obj:
                print(obj)
                ctr = ctr + 1
    if ctr ==0:
        print('--- gc dict none found')
    else:
        print('--- gc dict end')

def list_gc_id(oid):
    print('--- gc id')
    objs = gc.get_objects()
    ctr = 0
    for obj in objs:
        if isinstance(obj, dict) and len(obj)==1:
            for item in obj.items():
                objv = obj[item[0]]
                if not isinstance(objv, dict):
                    #print('objv', objv)
                    ooid = id(objv)
                    if oid == ooid:
                        print(obj)
                        ctr = ctr + 1
    if ctr ==0:
        print('--- gc id none found')
    else:
        print('--- gc id end')
        
        
test = 0

if test == 0:
    # simple delete
    c = Constant(11)
    cid=id(c)
    FunctionsList.getInstance().report()
    print("refs", sys.getrefcount(c))
    #list_gc_functions()
    list_gc_dicts('Constant')
    print(hex(cid))
    list_gc_id(cid)
    
    FunctionsList.getInstance().remove_function(c.namespace, c.name)
    print("refs", sys.getrefcount(c))
    r1 = gc.get_referrers(c)
    del c
    FunctionsList.getInstance().report()
    list_gc_dicts('Constant')
    list_gc_id(cid)
    
        
    #c.summary(extra=True)


if test == 1:
    # simple delete
    c = Constant(11)
    FunctionsList.getInstance().report()
    FunctionsList.getInstance().delete_function(c.namespace, c.name)
    FunctionsList.getInstance().report()
    
    c.summary(extra=True)

if test == 2:
    # delete with reference
    c = Constant(11)
    p = Proportional(links=c, namespace=c.namespace)
    FunctionsList.getInstance().report()
    FunctionsList.getInstance().delete_function(c.namespace, c.name)
    print()
    FunctionsList.getInstance().report()
    c.summary(extra=True)


