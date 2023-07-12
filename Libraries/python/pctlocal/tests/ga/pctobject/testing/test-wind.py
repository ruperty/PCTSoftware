
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from yaw_RL_module import YawEnv, get_dataset_from_simu




steps=1

test = 1


if test ==1:


    power_curve = pd.read_excel('testfiles/power_curve.xlsx')
    dataset_file = 'testfiles/steady_wind.csv'
    (wind_timeseries, wind_timeseries_not_agg) = get_dataset_from_simu(dataset_file,
                                                                   cycle_period=10,
                                                                   rolling_average_duration=20)


    yaw_params = {
        'yaw_rate_max': 0.3,
        'yaw_consumption':18,
        'rated_speed': 14,
        'ref_speed': power_curve['ref_v'].to_list(),
        'ref_power': power_curve['ref_P'].to_list(),
        'cycle_period': 10,
        'w2': 40,
        }

    model_params = {
        'wind_timeseries': wind_timeseries,
        'wind_timeseries_not_agg': wind_timeseries_not_agg,
        'start_index': 100,
        'stop_index': 1100,    
        'start_index_test': 1100,
        'stop_index_test': 2100,
        'filter_duration': 1,
        'yaw_params': yaw_params,
        'ancestors': 12,
        'training_steps': 500000,
        }

    model_params["wind_timeseries"],
    model_params["start_index"],
    model_params["stop_index"],
    model_params["ancestors"],
    model_params["filter_duration"],
    model_params["yaw_params"]


    env = YawEnv(wind_timeseries, model_params['start_index'], model_params['stop_index'], model_params['ancestors'], model_params['filter_duration'], yaw_params, keep_history=True)
    observation = env.reset()
    done = False
    score, i = 0, 0

    
    while not done:
        i += 1
        action = 1 
        observation, reward, done, info = env.step(action)
        score += reward
        
        #self.env.seed(seed)
        env.close()

    print(observation)
    print(score)

