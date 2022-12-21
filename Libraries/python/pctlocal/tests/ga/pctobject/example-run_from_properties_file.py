

from utils.paths import  get_gdrive
from eepct.hpct import HPCTIndividual
from pct.architectures import run_from_properties_file
   

file = get_gdrive() + 'data/ga/CartPoleV1/Std-InputsError-RootMeanSquareError-Mode00/ga-000.120-s001-2x3-m0-1690507d808f9d94e8722020c75a1e62.properties'

#ga-000.121-s001-3x4-m0-924f41bf8c5ff68654b05da500579fea.properties'
#ga-000.124-s001-1x1-m0-a8ab4cf3151b29a13abb2680bc574781.properties'
#ga-000.124-s001-1x1-m0-8b0d9b3da7c984766efd233b07bec593.properties'
#ga-000.124-s001-1x1-m0-5cb8a3bb27767c9f0cd9f6df498bcc59.properties'

hpct = HPCTIndividual.from_properties_file(file)

hpct.set_name('Cartpole')
hpct.set_suffixes()
config = hpct.get_config()

runs=500
render=True
draw=False

# plots = [ {'plot_items': {'PL0C0ws':'per','RL0C0c':'ref','IPA':'pa'}, 'title':'Goal'},
# {'plot_items': {'Action1ws':'out'}, 'title':'Output'}]   
# plots=[]

ind, score = HPCTIndividual.run_from_config(config, render=True,  error_collector_type='InputsError', error_response_type='RootMeanSquareError', error_properties=None, error_limit=100, steps=500, verbose=False)

    # ind = HPCTIndividual.from_config(config)
    # env = ind.get_preprocessor()[0]
    # env.set_render(True)
    # error_collector_type , error_response_type, error_properties= 'InputsError', 'RootMeanSquareError', 'error:smooth_factor,0.5'
    # error_collector = BaseErrorCollector.collector(error_response_type, error_collector_type, 100)
    # ind.draw(file='test_hpct_from_config_3.png', node_size=200, font_size=10, with_edge_labels=True)
    # ind.set_error_collector(error_collector)
    # ind.run(steps=500, verbose=False)
    # env.close()   
    # score=ind.get_error_collector().error()
    
print("Best Score: %0.3f" % score)
ind.summary()
print(ind.get_parameters_list())





