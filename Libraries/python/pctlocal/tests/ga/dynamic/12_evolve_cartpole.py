#!/usr/bin/env python
# coding: utf-8

# In[1]:




# # Evolve Cartpole
# > Examples of evolving Cartpole perceptual control hierarchies.

# In[2]:


#export 
from epct.evolvers import evolve_from_properties_file

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)


# In[3]:


online=False
debug=False


# In[4]:


#gui
online=True
debug=True


# In[5]:


if online and not debug:
    verbose = {'evolve_verbose':1}
    print_properties=True
    gens=None
    pop_size=None
else:
    gens=1
    pop_size = 4
    verbose = {}
    print_properties=False


# In[6]:


filename = 'ga-001.444-3344-397818342161201780.properties'


# In[7]:


out,evr,score = evolve_from_properties_file(filename, gens=gens, pop_size=pop_size, full_dir='/mnt/c/tmp', 
    draw=True, verbose=verbose, print_properties=print_properties)


# In[ ]:


print(score)


# In[ ]:


if online and not debug:
    assert score == 1.4439277168113878
else:
    assert score == 47.314969196199556


# In[ ]:





# In[ ]:



