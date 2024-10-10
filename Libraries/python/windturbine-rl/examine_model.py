#!/usr/bin/python
# -*- coding: utf-8 -*-
from yaw_RL_module import *

model_file='C:\\Users\\ruper\\Versioning\\PCTSoftware\\Libraries\\python\\windturbine-rl\\results\\steady\\1104-028-20241009-214610\\steady_wind.zip'


model_name = model_file.split('.')[0]
print('model_name', model_name)
model = PPO.load(model_name)

# Print the architecture of the policy network
print(model.policy)

# Print detailed architecture of the policy network
for name, layer in model.policy.named_children():
    print(f"Layer: {name}")
    print(layer)
