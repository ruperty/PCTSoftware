

from pct.functions import BaseFunction
from pct.putils import FunctionsList
from epct.functions import EAConstant

from participant.participant import Wrestler

class WebotsWrestler(BaseFunction):
    "A function that creates and runs a Webots Wrestler robot."
    
    def __init__(self, render=False, value=0, name="Wrestler", seed=None, links=None, new_name=True, 
                 early_termination=True, namespace=None):    
        super().__init__(name=name, value=value, links=links, new_name=new_name, namespace=namespace)
        self.robot = Wrestler()
        self.early_termination=early_termination
        
        
    def __call__(self, verbose=False):        
        super().__call__(verbose)

        self.robot()
                
        return self.value

    def early_terminate(self):
        if self.early_termination:
            if self.really_done:
                raise Exception(f'1000: OpenAIGym Env: {self.env_name} has terminated.')
            if self.done:
                self.reward = 0
                self.really_done = True
                
    def process_input(self):
        force = min(max(self.input, self.min_action), self.max_action)
        self.input=[force]
        
    def process_values(self):
        reward = self.obs[1]
        if reward > 90:
            reward = 0
        self.reward = - reward
        pos = self.value[0] + 1.2
        self.value = np.append(self.value, pos)

    def summary(self, extra=False):
        super().summary("", extra=extra)
        
    def get_graph_name(self):
        return super().get_graph_name() 

    def get_config(self, zero=1):
        "Return the JSON  configuration of the function."
        config = {"type": type(self).__name__,
                    "name": self.name}
        
        if isinstance(self.value, np.ndarray):
            config["value"] = self.value.tolist() * zero
        else:
            config["value"] = self.value * zero
        
        ctr=0
        links={}
        for link in self.links:
            func = FunctionsList.getInstance().get_function(self.namespace, link)
            try:
                links[ctr]=func.get_name()
            except AttributeError:
                #raise Exception(f' there is no function called {link}, ensure it exists first.')            
                print(f'WARN: there is no function called {link}, ensure it exists first.')            
                links[ctr]=func
                
            ctr+=1
        
        config['links']=links

        config["env_name"] = self.env_name
        #config["values"] = self.value
        config["reward"] = self.reward
        config["done"] = self.done
        config["info"] = self.info
    
    
    class Factory:
        def create(self, seed=None): return WebotsWrestler(seed=seed)
    class FactoryWithNamespace:
        def create(self, namespace=None, seed=None): return WebotsWrestler(namespace=namespace, seed=seed)          