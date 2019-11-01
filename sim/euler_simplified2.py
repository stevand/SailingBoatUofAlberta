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
        omega       Angular speed of the boat
        v:          Speed of the boat
        s_angle:    Sail angle
        r_angle:    Rudder angle
        s_force:    Force on sail
        r_force:    Force on rudder
    """

    state = namedtuple('state', [
        'x',
        'y',
        'theta',
        'omega',
        'v',
        's_angle',
        'r_angle',
        's_force',
        'r_force'
    ])

    def __init__(self, step_size, beta=None, V=None, fric_t=None, fric_a=None, s_lift=None, r_lift=None, r_s=None, r_r=None, L=None, m=None, J=None):
        """Initialize the simulator with the following parameters:
        step_size:          Time step size (in ms) when using Euler's method
        beta:               Drift coefficient
        V:                  Wind speed
        fric_t:             Tangential friction
        fric_a:             Angular friction
        s_lift:             Sail lift
        r_lift:             Rudder lift
        r_s:                Distance from G to mast
        r_r:                Distance from G to rudder
        L:                  Distance between mast and rudder
        m:                  Mass of boat
        J:                  Angular inertia
        """
        self.step_size = step_size
        self.beta = beta
        self.V = V
        self.fric_t = fric_t
        self.fric_a = fric_a
        self.s_lift = s_lift
        self.r_lift = r_lift
        self.r_s = r_s
        self.r_r = r_r
        self.L = L
        self.m = m
        self.J = J

    def simulate(self, interval):
        self.euler_f()
        """
        fullsteps = round(interval // self.step_size)
        state = prev_state

        for _ in range(fullsteps):
            state = self.euler_f(state)

        return state"""

    def euler_f(self):
        self.state.s_force=self.s_lift *( self.V*cos(self.state.theta+self.state.s_angle)-self.state.v*sin(self.state.s_angle))
        self.state.r_force=self.r_lift * self.state.v * sin(self.state.r_angle)
        x_dot = self.state.v * cos(self.state.theta)
        y_dot = self.state.v * sin(self.state.theta) - self.beta * self.V
        theta_dot = self.state.omega
        v_dot = (self.state.s_force * sin(self.state.s_angle) - self.state.r_force * sin(self.state.r_angle) - self.fric_t * self.state.v) / self.m
        omega_dot =(self.state.s_force * (self.L-self.r_s*cos(self.state.s_angle)) - self.state.r_force * self.r_r* cos(self.state.r_angle) - self.fric_a * self.state.omega) / self.J
        self.state.x=self.state.x+x_dot*self.step_size
        self.state.y=self.state.y+y_dot*self.step_size
        self.state.v=self.state.v+v_dot*self.step_size
        self.state.theta=self.state.theta+theta_dot*self.step_size
        self.state.omega=self.state.omega+omega_dot*self.step_size
        return 1
 