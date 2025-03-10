from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, CallbackList, BaseCallback
import gym
import torch as th
from torch import nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import warnings
warnings.simplefilter(action="ignore", category=UserWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)
from comet_ml import Experiment, Artifact, OfflineExperiment
import math
import scipy as sc
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.tools as tls
import scipy.interpolate
import os
from matplotlib.ticker import FuncFormatter


def get_yaw_count(nacelle_position_diff):
    '''
    
    Parameters
    ----------
    nacelle_position_diff : Pandas series of nacelle position increment 
        

    Returns
    -------
    number of yaw actuations
    '''
    yaw_count = 0
    for i in range(1, len(nacelle_position_diff)):
        if nacelle_position_diff[i - 1] == 0 and nacelle_position_diff[i] != 0:
            yaw_count += 1
        elif nacelle_position_diff[i - 1] > 0 and nacelle_position_diff[i] < 0:
            yaw_count += 1
        elif nacelle_position_diff[i - 1] < 0 and nacelle_position_diff[i] > 0:
            yaw_count += 1
    return yaw_count

           
    

def get_time_yawing(nacelle_position_diff):
    '''
    Parameters
    ----------
    nacelle_position_diff : Pandas series of nacelle position increment 
        

    Returns
    -------
    time spent yawing in percent
    '''
    time_yawing_count = 0
    for i in range(0, len(nacelle_position_diff)):
        if nacelle_position_diff[i] != 0:
            time_yawing_count += 1
    return 100* time_yawing_count / len(nacelle_position_diff)

  



def oriented_angle(angle):
    '''
    Parameters
    ----------
    angle 

    Returns
    -------
    oriented angle in range [-180,179]

    '''
    angle = ((angle + 180) % 360) - 180
    return angle


def get_dataset_from_simu(path="dataset.csv", cycle_period=10, rolling_average_duration=20):
    '''
    returns output dataset obtained of CYCA-S
    '''
    pd.options.plotting.backend = "plotly"
    df = pd.read_csv(path, delimiter=",")
    df["wind_direction"] = [oriented_angle(ang) for ang in df["wind_direction"]]
    wind_dir = (df["wind_direction"].rolling(cycle_period).mean().iloc[::cycle_period])
    df["nacelle position"] = [oriented_angle(ang) for ang in df["nacellePosition"]]
    df["nacelle position logs"] = [oriented_angle(ang) for ang in df["nacelle position logs"]]
    nac_pos = (df["nacelle position"].rolling(cycle_period).mean().iloc[::cycle_period])
    nac_pos_logs = (df["nacelle position logs"].rolling(cycle_period).mean().iloc[::cycle_period])
    wind_speed = (df["wind_speed"].rolling(cycle_period).mean().iloc[::cycle_period])
    wind_timeseries = pd.DataFrame(
        {
            "nacelle_pos_baseline_simu": nac_pos.to_list(),
            'nacelle_pos_baseline_logs':nac_pos_logs.to_list(),
            "wind_speed": wind_speed.to_list(),
            "wind_direction": wind_dir.to_list(),
        }
    )
    
    
    wind_timeseries_not_agg = pd.DataFrame(
        {
            "nacelle_pos_baseline_simu": df["nacelle position"].to_list(),
            'nacelle_pos_baseline_logs':df["nacelle position logs"].to_list(),
        }
    )
    

    wind_timeseries = wind_timeseries.dropna().reset_index(drop=True)
    wind_timeseries["time"] = wind_timeseries.index
    return wind_timeseries, wind_timeseries_not_agg


def test_trad_control(wind_timeseries, wind_timeseries_not_agg,agg, start, end, experiment=None,datatype='baseline_simu'):
    '''
    test CYCA-S and CYCA-L

    '''
    file = f'res-{datatype}.html'
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(range(0,(end-start)*10,10), wind_timeseries["wind_direction"][start:end], label="wind direction (deg)")
    ax.plot(range(0,(end-start)*10,10), wind_timeseries["nacelle_pos_" + datatype][start:end], label="nacelle position (deg)")
    if experiment:
        experiment.log_curve(
            "wind_direction",
            range(0, end-start),
            wind_timeseries["wind_direction"][start:end],
            overwrite = True,
        )
    if experiment:
        experiment.log_curve(
            "nacelle_pos_"+datatype,
            range(0,  end-start),
            wind_timeseries["nacelle_pos_" + datatype][start:end],
            overwrite = True,
        )

    plt.legend()
    plotly_fig = tls.mpl_to_plotly(fig)
    plotly_fig.write_html(file)

    if experiment:
        # experiment.log_html(open("res.html").read()) 
        experiment.log_html(open(file,encoding='utf-8').read()) # added ,encoding='utf-8'

    average_yaw_error = (oriented_angle(wind_timeseries["wind_direction"][start:end] - wind_timeseries["nacelle_pos_" + datatype][start:end]).abs().mean())
    nacelle_position_diff = oriented_angle(wind_timeseries["nacelle_pos_" + datatype][start:end].diff(1).dropna())
    nacelle_position_not_agg_diff = oriented_angle(wind_timeseries_not_agg["nacelle_pos_" + datatype][start*agg:end*agg].diff(1).dropna())
    angle_covered = sum(abs(nacelle_position_diff))
    yaw_count = get_yaw_count(nacelle_position_diff.to_list())
    time_yawing = get_time_yawing(nacelle_position_not_agg_diff.to_list())

    if experiment:
        experiment.log_metrics(
            {
                "start_trad": start,
                "end_trad": end,
                "average yaw error_"+ datatype: average_yaw_error,
                "angle covered_trad_"+ datatype: angle_covered,
                "yaw count_trad_"+ datatype: yaw_count,
                "time_yawing_trad_"+ datatype: time_yawing,
            }
        )

    return {
        "start": start,
        "end": end,
        "average yaw error_"+ datatype: average_yaw_error,
        "angle covered_trad_"+ datatype: angle_covered,
        "yaw count_trad_"+ datatype: yaw_count,
        "time_yawing_trad_"+ datatype: time_yawing,
    }, \
    wind_timeseries["nacelle_pos_" + datatype][start:end].to_list(), \
    wind_timeseries["wind_direction"][start:end].to_list()
    




def test_model(model,wind_timeseries,start_index,stop_index,ancestors,filter_duration,yaw_parameters,experiment=None,datatype='test', prefix=""):
    '''
    test RLYCA
    '''
    env = YawEnv(wind_timeseries,start_index,stop_index,ancestors,filter_duration,yaw_parameters,keep_history=True)
    observation = env.reset()
    done = False
    score, i = 0, 0

    file = f'res_model{prefix}.html'
    while not done:
        i += 1
        encoded = np.stack([observation])
        action, states = model.predict(encoded)
        observation, reward, done, info = env.step(action)
        score += reward

    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(range(0,len(env.history["wind_direction"])*10,10),env.history["wind_direction"], label="wind direction (deg)")
    ax.plot(range(0,len(env.history["wind_direction"])*10,10),env.history["yaw angle after actuation"], label="nacelle position (deg)")
    plt.legend()
    plotly_fig = tls.mpl_to_plotly(fig)
    plotly_fig.write_html(file)


    average_yaw_error = env.history["yaw error after actuation"].abs().mean()
    nacelle_position_diff = oriented_angle(env.history["yaw angle after actuation"].diff(1).dropna())
    angle_covered = sum(abs(nacelle_position_diff))
    yaw_count = get_yaw_count(nacelle_position_diff.to_list())
    time_yawing = get_time_yawing(nacelle_position_diff.to_list())
    
    if experiment and datatype=='test' :
        # experiment.log_html(open("res_model.html").read(), clear=True) 
        experiment.log_html(open(file,encoding='utf-8').read(), clear=True) # added ,encoding='utf-8'
        
    if experiment :
        experiment.log_curve(
        "nacelle_pos_"+datatype,
        range(0, stop_index-start_index),
        env.history["yaw angle after actuation"],
        overwrite = True,
        )
        experiment.log_metrics(
            {
                "start_index_"+datatype: start_index,
                "stop_index_"+datatype: stop_index,
                "power_trad_"+datatype: env.history["power_trad"].sum(),
                "power_no_loss_"+datatype: env.history["power_no_loss"].sum(),
                "power_control_"+datatype: env.history["power_control"].sum(),
                "average yaw error_"+datatype: average_yaw_error,
                "average reward_"+datatype: score,
                "angle covered_"+datatype: angle_covered,
                "yaw count_"+datatype: yaw_count,
                "time_yawing_"+datatype: time_yawing,
            }
        )



    return {
        "start_index": start_index,
        "stop_index": stop_index,
        "power_trad": env.history["power_trad"].sum(),
        "power_no_loss": env.history["power_no_loss"].sum(),
        "power_control": env.history["power_control"].sum(),
        "average yaw error": average_yaw_error,
        "average reward": score,
        "angle covered": angle_covered,
        "yaw count": yaw_count,
        "time_yawing": time_yawing,
        }, \
        env.history["yaw angle after actuation"].to_list(), \
        (env.history["power_control"]-env.history["power_trad"])/env.history["power_trad"],  \
        env.history["power_control"], \
        env.history["power_trad"],
    



class YawEnv(Env):
    def __init__(
        self,
        wind_timeseries,
        start_index,
        stop_index,
        ancestors,
        filter_duration,
        params,
        keep_history=False,
    ):

        self.wind_timeseries = wind_timeseries
        self.start_index = start_index
        self.stop_index = stop_index
        self.wind_speed_avg = wind_timeseries['wind_speed'][start_index:stop_index].mean()
        self.wind_speed_std = wind_timeseries['wind_speed'][start_index:stop_index].std()
        self.keep_history = keep_history
        self.filter_duration = filter_duration
        self.yaw_rate_max = params["yaw_rate_max"]
        self.cycle_period = params["cycle_period"]
        self.w2 = params["w2"]
        self.episode_len = stop_index - start_index
        self.history = None
        self.ref_speed = params["ref_speed"]
        self.ref_power = params["ref_power"]
        self.rated_speed = params["rated_speed"]
        self.state = None
        self.step_since_last_0 = None
        self.step_since_last_2 = None
        self.index_wind_timeseries = None
        self.power_curve = sc.interpolate.interp1d(
            self.ref_speed,
            self.ref_power,
            bounds_error=False,
            fill_value=(0, self.ref_power[-1]),
        )

        self.ancestors = ancestors
        # print(self.episode_len, " points in simulation dataset")
        self.action_space = Discrete(3)

        # Observation space : Represents environment **after yaw actuation**

        # action
        # yaw error
        # wind direction
        # standardized wind speed
        self.observation_space = Box(
            np.array([[0, -180, -180, 0] for _ in range(self.ancestors)]),
            np.array([[3, 179, 179, 10] for _ in range(self.ancestors)]),
            shape=(self.ancestors, 4),
        )


    def step(self, action):
        """
        Apply yaw control action and compute reward obtained **after yaw actuation**
        """

        # iterate to the next wind direction conditions
        self.index_wind_timeseries += 1
        done = False
        increment = self.yaw_rate_max * self.cycle_period
        yaw_angle_change = 0

        if action == 0:
            yaw_angle_change = -increment
        if action == 2:
            yaw_angle_change = increment

        self.yaw_angle = oriented_angle(self.yaw_angle + yaw_angle_change)
        new_yaw_error = oriented_angle(self.yaw_angle - self.wind_timeseries["wind_direction"][self.index_wind_timeseries])
        new_state = np.zeros((self.ancestors, 4))
        new_state[:-1, :] = self.state[1:, :]
        new_state[-1, :] = np.array(
            [
                action,
                new_yaw_error,
                self.wind_timeseries["wind_direction"][self.index_wind_timeseries],
                (self.wind_timeseries["wind_speed"][self.index_wind_timeseries]-self.wind_speed_avg)/self.wind_speed_std,
            ]
        )

        self.state = new_state
        reward = -self.wind_timeseries["wind_speed"][self.index_wind_timeseries]**3 \
                * oriented_angle(self.yaw_angle - self.wind_timeseries["wind_direction"][self.index_wind_timeseries:self.index_wind_timeseries+12].mean()) ** 2    \
                + self.w2 * (self.step_since_last_2 > self.filter_duration and self.step_since_last_0 > self.filter_duration)




        if self.keep_history:
            power_control = self.get_power(self.wind_timeseries["wind_speed"][self.index_wind_timeseries],new_yaw_error)
            power_no_loss = self.get_power(self.wind_timeseries["wind_speed"][self.index_wind_timeseries], 0)
            power_trad = self.get_power(self.wind_timeseries["wind_speed"][self.index_wind_timeseries],oriented_angle(self.wind_timeseries["nacelle_pos_baseline_simu"][self.index_wind_timeseries] - self.wind_timeseries["wind_direction"][self.index_wind_timeseries]), )
            new_history = {
                "index": self.index_wind_timeseries,
                "power_control": power_control,
                "power_no_loss": power_no_loss,
                "power_trad": power_trad,
                "yaw error after actuation": new_yaw_error,
                "yaw angle after actuation": self.yaw_angle,
                "wind_direction": self.wind_timeseries["wind_direction"][
                    self.index_wind_timeseries
                ],
            }
            self.history = self.history.append(new_history, ignore_index=True)

        if action == 1:

            self.step_since_last_0 += 1
            self.step_since_last_2 += 1

        elif action == 0:

            self.step_since_last_0 = 0
            self.step_since_last_2 += 1

        elif action == 2:

            self.step_since_last_2 = 0
            self.step_since_last_0 += 1

        # stop at the end of the timeseries

        if self.index_wind_timeseries == self.stop_index - 1:
            done = True

        return self.state, reward, done, {}
    
    

    def get_power(self, wind_speed, yaw_error):
        '''
        return power produced as a function of the yaw error and yaw speed usign the power curve 
        '''
        if yaw_error < -90 or yaw_error > 90: return 0
        power = self.power_curve(wind_speed)
        if wind_speed < self.rated_speed:
            yaw_eror_rad = yaw_error * math.pi / 180
            power *= math.cos(yaw_eror_rad) ** 3
        return (power * self.cycle_period) / 3600

    def reset(self):
        '''
        reset the environment and return initial state
        '''
        self.index_wind_timeseries = self.start_index
        self.yaw_angle = self.wind_timeseries["nacelle_pos_baseline_simu"][self.index_wind_timeseries]
        self.step_since_last_2 = 0
        self.step_since_last_0 = 0

        # reset state :

        if self.keep_history:
            self.history = pd.DataFrame(
                {
                "index": [self.index_wind_timeseries],
                "yaw error after actuation": [oriented_angle(self.wind_timeseries["nacelle_pos_baseline_simu"][self.index_wind_timeseries] - self.wind_timeseries["wind_direction"][self.index_wind_timeseries])],
                "yaw angle after actuation": [self.wind_timeseries["nacelle_pos_baseline_simu"][self.index_wind_timeseries]],
                "wind_direction": [self.wind_timeseries["wind_direction"][self.index_wind_timeseries]],
                }
            )

        self.state = np.array(
            [
                [
                    1,
                    oriented_angle(self.wind_timeseries["nacelle_pos_baseline_simu"][index] - self.wind_timeseries["wind_direction"][index]),
                    self.wind_timeseries["wind_direction"][index],
                    (self.wind_timeseries["wind_speed"][index]-self.wind_speed_avg)/self.wind_speed_std,
                ]
                
            for index in range(self.start_index + 1 - self.ancestors, self.start_index + 1)
            ]
        )

        return self.state






class Cometlogger(BaseCallback):

    """
    Custom callback to plot additional values in comet.
    """

    def __init__(self, experiment, model_params,eval_freq=10000):

        super(Cometlogger, self).__init__()
        self.model_params = model_params
        self.eval_freq = eval_freq
        self.experiment = experiment

    def _on_step(self) -> bool:
        model_params = self.model_params
        if self.eval_freq > 0 and self.n_calls % self.eval_freq == 0:
            res, _ , _, _, _= test_model(
                self.model,
                model_params["wind_timeseries"],
                model_params["start_index"],
                model_params["stop_index"],
                model_params["ancestors"],
                model_params["filter_duration"],
                model_params["yaw_params"],
                experiment=self.experiment,
                datatype='train',
            )




            print("----------------------------------")

            for k, v in res.items():

                print("{}: {}".format(k, v))

            print("----------------------------------")

        return True

def get_comparaison_metrics(wind_direction,power_control,power_simu,res_model, res_baseline_simu, yaw_rate, yaw_power, width_bin) :
    res_model_diff = pd.Series(res_model).diff(1).fillna(0)
    res_baseline_simu_diff = pd.Series(res_baseline_simu).diff(1).fillna(0)
    wind_direction =pd.Series(wind_direction)
    power_prod_change = []
    conso_yaw_change = []
    net_prod_change = []
    rel_net_prod_change = []
    yaw_error_rel_change = []


    for i in range(0,len(power_control),width_bin) :
        power_simu_bin = power_simu[i:i+width_bin].sum()
        power_control_bin = power_control[i:i+width_bin].sum()
        angle_covered_model = res_model_diff[i:i+width_bin].abs().sum()
        angle_covered_simu = res_baseline_simu_diff[i:i+width_bin].abs().sum()
        angle_covered_change = angle_covered_model - angle_covered_simu
        time_yawing_change = angle_covered_change / yaw_rate 
        consumption_change = time_yawing_change/3600 * yaw_power
        power_change_bin = (power_control_bin - power_simu_bin)
        power_prod_change.append(power_change_bin)
        conso_yaw_change.append(consumption_change)
        net_prod_change.append(power_change_bin-consumption_change)
        rel_net_prod_change.append(100 * (power_change_bin-consumption_change)/power_simu_bin)
        yaw_error_model = abs(oriented_angle(wind_direction[i:i+width_bin]-res_model[i:i+width_bin])).mean()
        yaw_error_simu = abs(oriented_angle(wind_direction[i:i+width_bin]-res_baseline_simu[i:i+width_bin])).mean()
        yaw_error_rel_change.append(100 * (yaw_error_simu-yaw_error_model)/yaw_error_simu)

        
    
    return power_prod_change, conso_yaw_change, net_prod_change,rel_net_prod_change,yaw_error_rel_change
        
        
        
