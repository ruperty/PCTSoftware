from comet_ml import Experiment

from os import sep, path
from epct.evolve import evolve_setup


experiment = Experiment(api_key='WVBkFFlU4zqOyfWzk5PRSQbfD',
                        project_name='test',
                        workspace='wind-turbine')



experiment.log_code(path.basename(__file__))
name = 'import-test'
experiment.set_name(name)




experiment.end()




