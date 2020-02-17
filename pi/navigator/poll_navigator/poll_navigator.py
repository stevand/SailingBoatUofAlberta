from threading import Thread
from .. import AbstractNavigator
from .voter import WaypointVoter, WindVoter, ChannelVoter, ManueverVoter
from pi.navutils import dist
from time import sleep


def navigate(interval, nav, driver, helmsman):
    while True:
        if nav.enabled:
            next_waypoint = nav.get_waypoint()
            boat = driver.get_position()
            while next_waypoint and dist(boat, next_waypoint) < nav.waypoint_dist:
                nav.del_waypoint()
                nav._prev = next_waypoint
                next_waypoint = nav.get_waypoint()
                print("going to:", next_waypoint)

            if next_waypoint:
                helmsman.maximize_speed = True
                goto = nav.poll()
                helmsman.turn(goto)
                nav.curr_heading = goto
                print("Chosen heading:", goto)
                print(*nav.headings[goto])
                # print(goto, helmsman.desired_heading)
            else:
                print('minimizing speed')
                helmsman.maximize_speed = False 
        sleep(interval)


class PollNavigator(AbstractNavigator):
    def __init__(self, driver, helmsman, interval=0.3, num_headings=180, **kwargs):
        super().__init__(driver, helmsman, **kwargs)
        # constructs all necessary voters and their weights
        self._prev = driver.get_position()
        self.curr_heading = -1 #initialized to impossible value
        self._voters = [
            WaypointVoter(driver, self.get_waypoint),
            WindVoter(driver),
            ChannelVoter(driver, lambda: (self._prev, self.get_waypoint())),
            ManueverVoter(driver, lambda: self.curr_heading)
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
            self.headings[heading] = [voter.vote(heading)
                                         for voter in self._voters]
            self.headings[heading].insert(0, sum(self.headings[heading]))
            if best_heading == -1 or self.headings[best_heading][0] < self.headings[heading][0]:
                best_heading = heading
        return best_heading
