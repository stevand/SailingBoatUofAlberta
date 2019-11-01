from euler_sim2 import EulerSimulator
from sim_interface import SimulatorInterface
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import plot_canvas as plot
import json
import tkinter as tk

def get_params():
    with open('sim_params.json', mode='r') as param_file:
        sim_params = json.load(param_file)
    return sim_params

def get_start_state():
    with open('start_state.json', mode='r') as start_state_file:
        start_state = EulerSimulator.state(**json.load(start_state_file))
    return start_state

def run_sim():
    sim_params = get_params()
    start_state = get_start_state()

    esim = EulerSimulator(**sim_params) #constructs an euler simulator with the loaded params
    simulator = SimulatorInterface(esim, 100, start_state) #construcs an interface that will return frames 100ms apart

    control = EulerSimulator.control(
        s_angle = 1,
        r_angle = 0.5
    )

    env = EulerSimulator.env(
        V = 0.5
    )

    for i in range(500):
        print('State num:', i)
        print(simulator.simulate(control, env))
    
    show(simulator.frames())

def show(frames):
    root= tk.Tk()
    fig = plot.setup(frames[0])
    plotcanvas = FigureCanvasTkAgg(fig, root)
    plotcanvas.get_tk_widget().grid(column=1, row=1)
    ani = animation.FuncAnimation(fig, plot.updplot, frames=frames, interval=50, blit=False)
    root.mainloop()

if __name__ == "__main__":
    run_sim()
    