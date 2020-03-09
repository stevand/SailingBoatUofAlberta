import locator

helmsman = locator.get_helmsman()

#rudder controller enabled
rc_enabled_dependency = ['helmsman','rudder_controller_enabled']
def rc_enabled_callback(rc_enabled):
    helmsman.rudder_controller_enabled = bool(rc_enabled)

#rudder controller desired heading
desired_heading_dependency = ['helmsman', 'desired_heading']
def desired_heading_callback(desired_heading):
    helmsman.turn(desired_heading)

#sail controller enabled
sc_enabled_dependency = ['helmsman', 'sail_controller_enabled']
def sc_enabled_callback(sc_enabled):
    helmsman.sail_controller_enabled = bool(sc_enabled)

#sail controller maximize speed
maximize_speed_dependency = ['helmsman', 'maximize_speed']
def maximize_speed_callback(maximize_speed):
    helmsman.maximize_speed = bool(maximize_speed)

helmsman_subscriptions = [
    (rc_enabled_callback, rc_enabled_dependency),
    (desired_heading_callback, desired_heading_dependency),
    (sc_enabled_callback, sc_enabled_dependency),
    (maximize_speed_callback, maximize_speed_dependency)
]