from euler_sim2 import EulerSimulator
from sim_interface import SimulatorInterface
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import plot_canvas as plot
import json
import tkinter as tk
import threading
from time import sleep

def get_params():
    with open('sim_params.json', mode='r') as param_file:
        sim_params = json.load(param_file)
    return sim_params

def get_start_state():
    with open('start_state.json', mode='r') as start_state_file:
        start_state = EulerSimulator.state(**json.load(start_state_file))
    return start_state

# Returns default (constant) control getter
def default_control():
    return EulerSimulator.control(
        s_angle = 1,
        r_angle = 0
        )

# Returns default (constant) env getter
def default_env():
    return EulerSimulator.env(
        V = 0.5
    )


def run_sim(get_control=None, get_env=None):
    sim_params = get_params()
    start_state = get_start_state()

    esim = EulerSimulator(**sim_params) #constructs an euler simulator with the loaded params
    simulator = SimulatorInterface(esim, 500, start_state) #construcs an interface that will return frames 100ms apart

    if get_control == None:
        get_control = default_control

    if get_env == None:
        get_env = default_env
    
    thread = threading.Thread(target=sim_thread, args=[simulator, get_control, get_env])
    thread.start()

    show(simulator.frame_generator())

def sim_thread(simulator, get_control, get_env, delay=0):
    print('starting thread')
    for i in range(100):
        sleep(delay)
        print(simulator.simulate(get_control(), get_env()))
    with open('log.json', 'w') as log:
        log.writelines(simulator.export_frames())

def show(frames):
    root= tk.Tk()
    fig = plot.setup(next(frames))
    plotcanvas = FigureCanvasTkAgg(fig, root)
    plotcanvas.get_tk_widget().grid(column=1, row=1)
    ani = animation.FuncAnimation(fig, plot.updplot, frames=frames, interval=100, blit=False)
    root.mainloop()

if __name__ == "__main__":
    run_sim()
    