from threading import Thread
from .. import AbstractNavigator
from .voter import WaypointVoter, WindVoter
from pi.navutils import dist
from time import sleep


def navigate(interval, nav, driver, helmsman):
    while True:
        if nav.enabled:
            next_waypoint = nav.get_waypoint()
            boat = driver.get_position()
            while next_waypoint and dist(boat, next_waypoint) < nav.waypoint_dist:
                print("next")
                nav.del_waypoint()
                next_waypoint = nav.get_waypoint()

            if next_waypoint:
                helmsman.maximize_speed = True
                goto = nav.poll()
                helmsman.turn(goto)
                print("Chosen heading:", goto)
                # print(goto, helmsman.desired_heading)
            else:
                print('minimizing speed')
                helmsman.maximize_speed = False 
        sleep(interval)


class PollNavigator(AbstractNavigator):
    def __init__(self, driver, helmsman, interval=0.3, num_headings=180, **kwargs):
        super().__init__(driver, helmsman, **kwargs)
        # constructs all necessary voters and their weights
        self._voters = [
            WaypointVoter(driver, self.get_waypoint),
            WindVoter(driver)
        ]
        # constructs a dictionary that holds approval for each candidate heading
        self.headings = {2*i: 0 for i in range(num_headings)}
        helmsman.maximize_speed = True
        thread = Thread(target=navigate, daemon=True,
                        args=[interval, self, driver, helmsman])
        thread.start()

    def poll(self):
        """Polls all voters and returns the heading with the highest approval"""
        best_heading = -1
        for heading in self.headings.keys():
            self.headings[heading] = sum(voter.vote(heading)
                                         for voter in self._voters)
            if best_heading == -1 or self.headings[best_heading] < self.headings[heading]:
                best_heading = heading
        return best_heading
