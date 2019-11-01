import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import euler_simplified2 as e1
from euler_sim2 import EulerSimulator
import json

with open('sim_params.json', mode='r') as param_file:
    sim_params = json.load(param_file)

with open('start_state.json', mode='r') as start_state_file:
    start_state = EulerSimulator.state(**json.load(start_state_file))

control = EulerSimulator.control(
    s_angle=0,
    r_angle=0
)
env = EulerSimulator.env(
    V = 1
)

sim = EulerSimulator(**sim_params)

print('start state:', start_state)
print('next state:', sim.simulate(start_state, env, control, 2000))