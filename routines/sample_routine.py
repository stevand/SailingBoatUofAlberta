"""
This is a sample routine. 
To run this routine, run the following command from the project's top directory:

python manager.py configs/sample_routine.json

"""
from threading import Thread
from time import sleep
import locator # import the locator to get access instances

def exec():
    """
    All routines return:
        blocking (bool): Whether or not the manager should wait until this routine is finished 
        before starting the next

        is_done (function): Returns true if the routine has finished

        cleanup (function): Performs any necessary cleanup once the routine finishes or is
        interrupted
    """
    # If your routine is quick, you can just run it right on the main thread
    print('Executing quick sample routine')

    # You can access instances of the boat driver or helmsman (and more) from the locator
    driver = locator.get_driver()
    driver.get_sail()

    # If the routine is non-blocking and takes some time, it should run on a seperate thread.
    # Keep track of whether or not the routine has finished.
    done = False
    def run():
        nonlocal done
        print('Starting long sample routine')
        sleep(2)
        print('Finished long sample routine')
        done = True

    thread = Thread(target=run, daemon=True)
    thread.start()

    # Some long routines can't be run on a seperate thread (ex: if they are using Tkinter).
    # In that case, be aware that your routine will block and keyboard interrupts may not work.

    # Whether or not the process is blocking should be returned
    blocking = False

    # Function that returns true only when the routine is complete
    def is_done():
        return done

    # Function that performs any necessary cleanup
    def cleanup():
        print('Performing cleanup')

    return blocking, is_done, cleanup