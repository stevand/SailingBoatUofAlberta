import sys
from importlib import import_module
from time import sleep
import locator
import routines.run_server as run_server

config_path = sys.argv[1]
locator.load_config(config_path)

routines = locator.get_config()['routines']
# stores functions that check if non-blocking routines are done
routines_done = [] 
# stores clean up functions for non-blocking routines
routines_cleanup = []

def terminate():
    for cleanup in routines_cleanup:
        cleanup()
    exit()

# runs all cleanup functions and exits if there is a keyboard interrupt
def block():
    try:
        sleep(0.1)
    except KeyboardInterrupt:
        terminate()


# routines are executed in the order they are specified in the config file
for routine in routines:
    # imports routine script
    try:
        routine_script = import_module('.' + routine, package='routines')
    except ModuleNotFoundError:
        print('No routine found for "{}"'.format(routine))
        print('Terminating')
        terminate()

    # executes routine
    blocking, is_done, cleanup = routine_script.exec(locator)

    # waits until routine is finished if it is blocking
    if blocking:
        while not is_done():
            block()
        cleanup()
    else:
        routines_cleanup.append(cleanup)
        routines_done.append(is_done)

# blocks until all routines are finished
while not all((is_done() for is_done in routines_done)):
    block()