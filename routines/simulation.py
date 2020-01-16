import tkinter as tk
import sim.plot_canvas as plot
from sim.sim_interface import SimulatorInterface 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sim.sim_runner as sim_runner

def exec(locator):
    sim_interface = locator.get_sim_interface()
    assert isinstance(sim_interface, SimulatorInterface)
    root = tk.Tk()
    start_frame = sim_interface.current_frame()
    fig = plot.setup(start_frame)
    plotcanvas = FigureCanvasTkAgg(fig, root)
    plotcanvas.get_tk_widget().grid(column=1, row=1)

    get_control = sim_runner.default_control
    get_env = sim_runner.default_env

    def progress():
        nonlocal root, sim_interface
        plot.updplot(sim_interface.simulate(get_control(), get_env()))
        print(sim_interface.current_frame())
        root.after(2000, progress)

    root.after(2000, progress)
    root.mainloop()

    blocking = True

    def is_done():
        return False

    def cleanup():
        pass

    return blocking, is_done, cleanup
    