import locator
import tkinter as tk
import sim.plot_canvas as plot
from sim.sim_interface import SimulatorInterface 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sim.sim_runner as sim_runner

def exec():
    sim_interface = locator.get_sim_interface(frame_time = 250)
    assert isinstance(sim_interface, SimulatorInterface)
    root = tk.Tk()
    start_frame = sim_interface.current_frame()
    fig = plot.setup(start_frame)
    plotcanvas = FigureCanvasTkAgg(fig, root)
    plotcanvas.get_tk_widget().grid(column=1, row=1)

    #initializes driver, which gets it's data from the simulator
    driver = locator.get_driver()

    #initializes the helmsman
    helmsman = locator.get_helmsman()
    helmsman.rudder_controller_enabled = False
    helmsman.sail_controller_enabled = False
    driver.set_sail(0)
    helmsman.turn(0)

    #creates getters for the env/control from the driver
    get_control = sim_runner.make_control_getter(driver)
    get_env = sim_runner.make_env_getter(driver)

    def progress():
        nonlocal root, sim_interface
        plot.updplot(sim_interface.simulate(get_control(), get_env()))
        print(sim_interface.current_frame())
        root.after(250, progress)

    root.after(250, progress)
    root.mainloop()

    blocking = True

    def is_done():
        return False

    def cleanup():
        pass

    return blocking, is_done, cleanup