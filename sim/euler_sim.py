from simulator import Simulator
from collections import namedtuple
from math import cos, sin

class EulerSimulator(Simulator):
    """Simulator that works by finding numerical approximations for the differential equations outlined 
    in "Sailboat as a Windmill" through a naive approach with Euler's method.
    
    The state contains the following properties:
        x:          Position of boat on east-west axis
        y:          Position of boat on north-south axis
        theta:      Heading relative to north
        omega:      Angular velocity of boat
        v:          Speed of the boat
        a:          Speed of true wind
        a_ap:       Speed of apparent wind    
        psi:        True wind direction  
        psi_ap:      Apparent wind direction
        s_angle:    Sail angle
        r_angle:    Rudder angle
        s_force:    Force on sail
        r_force:    Force on rudder
    """

    state = namedtuple('state', [
        'x',
        'y',
        'theta',
        'omega'
        'v',
        'a',
        'psi',
        'psi_ap',
        's_angle',
        'r_angle',
        's_force',
        'r_force'
    ])

    def __init__(self, step_size, dc=None, fric_t=None, fric_a=None, s_lift=None, r_lift=None, p6=None, p7=None, p8=None, m=None, mmi=None):
        """Initialize the simulator with the following parameters:
        step_size:          Time step size (in ms) when using Euler's method
        dc:                 Drift coefficient
        fric_t:             Tangential friction
        fric_a:             Angular friction
        s_lift:             Sail lift
        r_lift:             Rudder lift
        p6, p7, p8:         Geometric coefficients (see paper)
        m:                  Mass of boat
        mmi:                Mass moment of inertia
        """
        self.step_size = step_size
        self.dc = dc
        self.fric_t = fric_t
        self.fric_a = fric_a
        self.s_lift = s_lift
        self.r_lift = r_lift
        self.p6 = p6
        self.p7 = p7
        self.p8 = p8
        self.m = m
        self.mmi = mmi

    def simulate(self, prev_state, interval):
        fullsteps = interval // self.step_size
        for _ in range(fullsteps):
            prev_state = self.next_state(prev_state, self.step_size)

        if interval % self.step_size > 0:
            prev_state = self.next_state(prev_state, interval % self.step_size)         

    def next_state(self, prev_state, step):
        if not isinstance(prev_state, self.state):
            raise Exception('prev_state must be of type given by self.state')

        ps = prev_state._asdict()
        next_state = self.state(
            x = self.x(step, **ps),
            y = self.y(step, **ps),
            theta = self.theta(step, **ps),
            v = self.v(step, **ps),
            s_force = self.s_force(**ps)
            r_force = self.r_force(**ps)
        )
        return next_state

    def x(self, step, x=None, v=None, theta=None, psi=None, a=None):
        x_dot = v * cos(theta) + self.dc * a * cos(psi)
        return x + x_dot * step / 1000

    def y(self, step, y=None, v=None, theta=None, psi=None, a=None):
        y_dot = v * sin(theta) + self.dc * a * sin(psi)
        return y + y_dot * step / 1000

    def theta(self, step, theta, omega):
        theta_dot = omega
        return theta + theta_dot * step / 1000

    def v(self, step, s_angle=None, s_force=None, r_angle=None, r_force=None, fric_t=None, v=None, m=None):
        v_dot = (s_force * sin(s_angle) - r_force * sin(r_angle) - fric_t * v**2) / m
        return v + v_dot * step / 1000

    def s_force(self, a_ap=None, s_angle=None, psi_ap=None):
        return self.s_lift * a_ap * sin(s_angle - psi_ap)

    def r_force(self, v=None, r_angle=None):
        return self.r_lift * v * sin(r_angle)