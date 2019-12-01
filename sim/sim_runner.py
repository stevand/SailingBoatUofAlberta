from sim.euler_sim2 import EulerSimulator
from sim.sim_interface import SimulatorInterface
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import sim.plot_canvas as plot
import json
import tkinter as tk
import threading
from math import pi
from time import sleep
from .frame import Frame

DISPLAY_INTERVAL = 100  # time interval between subsequent frames are displayed


def get_params():
    with open('sim/sim_params.json', mode='r') as param_file:
        sim_params = json.load(param_file)
    return sim_params


def get_start_state():
    with open('sim/start_state.json', mode='r') as start_state_file:
        start_state = Frame.fromjson(''.join(start_state_file.readlines()), EulerSimulator)
    return start_state


def load_sim():
    """Initializes and returns a simulator interface and simulator from saved params and start state."""
    sim_params = get_params()
    start_state = get_start_state()

    esim = EulerSimulator(**sim_params)  # constructs an euler simulator with the loaded params
    sim_interface = SimulatorInterface(esim, 100, start_state)  # constructs an interface that will return frames 500ms apart

    return sim_interface, esim


def make_control_getter(driver):
    """Generates a get_control function from the given boat driver that returns the current control as a named tuple that can be used by the simulator"""

    def get_control():
        sail_dir = driver.get_sail()
        if driver.get_wind_dir_rel() < 0: # makes sure sail is pointing in opposite direction to wind
            sail_dir = -1 * sail_dir
        return EulerSimulator.control(
            s_angle=sail_dir / 180 * pi,
            r_angle=driver.get_rudder() / 180 * pi
        )

    return get_control


def make_env_getter(driver):
    """Generates a get_env function from the given boat driver that returns the current environment as a named tuple
    that can be used by the simulator"""

    def get_env():
        return EulerSimulator.env(
            V=driver.get_wind_speed()
        )

    return get_env


# Returns default (constant) control getter
def default_control():
    return EulerSimulator.control(
        s_angle=pi/2,
        r_angle=0
    )


# Returns default (constant) env getter
def default_env():
    return EulerSimulator.env(
        V=0.5
    )


def run_sim(sim_interface, get_control=None, get_env=None, frame_delay=0, num_frames=200, verbose=False, log_file=None):
    """
    Runs the simulator for the given number of frames and saves data to log.json.

    Parameters:
        sim_interface (SimulatorInterface): The interface that will be used to display and simulate frames
        get_control (() -> EulerSimulator.control): A callback that returns the control that will be used in the simulation. Default: default_control.
        get_env (() -> EulerSimulator.env): A callback that returns the environment that will be used in the simulation. Default: default_env.
        frame_delay (int): The time in ms to wait between frames. Default: 0.
        num_frames (int): The number of frames that the simulator will be run for. Default: 100
    """
    if get_control == None:
        get_control = default_control

    if get_env == None:
        get_env = default_env

    frame_delay_ms = frame_delay / 1000

    sim_interface.simulate(get_control(), get_env())
    thread = threading.Thread(target=sim_thread, args=[sim_interface, get_control, get_env, frame_delay_ms, num_frames, verbose, log_file],
                              daemon=True)
    thread.start()



def display_run(sim_interface, speed_factor=1, get_control=None, get_env=None, num_frames=200, verbose=False, log_file=None):
    """
    Simultaneously runs and displays the frames of sim_interface, allowing for a real time view of the simulation. Data saved to log.json.

    Parameters:
        sim_interface (SimulatorInterface): The interface that will be used to display and simulate frames
        speed_factor (float): How many times faster the simulator will run compared to real time. Default: 1.
        get_control (() -> EulerSimulator.control): A callback that returns the control that will be used in the simulation. Default: default_control.
        get_env (() -> EulerSimulator.env): A callback that returns the environment that will be used in the simulation. Default: default_env.
    
    Returns:
        root: The root of the tkinter window that has been created
    """
    sim_interface.set_interval(DISPLAY_INTERVAL * speed_factor)
    run_sim(sim_interface, get_control=get_control, get_env=get_env, frame_delay=DISPLAY_INTERVAL,
            num_frames=num_frames, verbose=verbose, log_file=log_file)
    
    return display(sim_interface)

def display(sim_interface):
    """Displays all existing frames in the sim_interface. Does not generate any new frames. Used for replaying saved
    frames. """
    return show(sim_interface.frame_generator())


# Thread that simulates new frames, sleeping for sleep_time between each one.
# Frames are saved to log.json at end.
def sim_thread(sim_interface, get_control, get_env, sleep_time, num_frames, verbose, log_file):
    print('starting thread')
    for i in range(num_frames):
        sim_interface.simulate(get_control(), get_env())
        if verbose:
            print(sim_interface.current_frame())
        sleep(sleep_time)
    if log_file:
        print('saving data to ', log_file)
        with open(log_file, 'w') as log:
            log.writelines(sim_interface.export_frames())


# Starts a tkinter window that displays the frames yielded by the frame_gen
def show(frame_gen):
    print('starting simulator')
    root = tk.Tk()
    fig = plot.setup(next(frame_gen))
    plotcanvas = FigureCanvasTkAgg(fig, root)
    plotcanvas.get_tk_widget().grid(column=1, row=1)
    ani = animation.FuncAnimation(fig, plot.updplot, frames=frame_gen, interval=DISPLAY_INTERVAL, blit=False)
    #root.mainloop()
    return root


if __name__ == "__main__":
    sim_interface, esim = load_sim()
    display_run(sim_interface)
