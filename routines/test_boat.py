from time import sleep
from threading import Thread
import locator

def exec():

    done = False

    def handle_input(task):
        while True:
            command = input().strip().lower()
            if command == 'y':
                break
            elif command == 'n':
                print('Failed at: ', task)
                done = True
                exit()

    print("Performing physical tests for ASV")
    
    driver = locator.get_driver()
    print("Driver loaded sucessfully\n")

    print("Testing sails.")
    for angle in [90, 60, 30, 0]:
        driver.set_sail(angle)
        print("Were the sails set to {} degrees? (y/n)".format(angle))
        handle_input('Setting sail')
    print("Sail tests passed.\n")
    sleep(1)

    print("Testing rudder.")
    for angle in [-45, -15, 15, 45]:
        driver.set_rudder(angle)
        print("Was the rudder set to {} degrees? (y/n)".format(angle))
        handle_input('Setting rudder')
    print("Rudder tests passed.\n")
    sleep(1)

    def angle_diff(a1, a2):
        a = a1 - a2
        if a > 180:
            a -= 360
        if a < -180:
            a += 360
        return abs(a)

    print("Testing windex.")
    num_trials = 4
    trial = 1
    for direction, angle in [('forwards', 360), ('left', 270), ('backwards', 180), ('right', 90)]:
        print("Trial {}/{}. Point the windex {}.".format(trial, num_trials, direction))
        print('Waiting 3 seconds.')
        sleep(3)
        read_angle = driver.get_wind_dir()
        print('Windex reports angle of {} degrees, expected angle of {} degrees.'.format(read_angle, angle))
        if angle_diff(read_angle, angle) > 30:
             print('Failed at : Windex test')
             done = True
             exit()
    print("Windex tests passed.\n")

    print('Success! All tests passed!')
    done = True

    def is_done():
        return done
    
    def cleanup():
        pass

    return True, is_done, cleanup
