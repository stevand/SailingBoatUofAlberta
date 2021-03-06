from .simulator import Simulator
from collections import namedtuple
from math import cos, sin, pi


class EulerSimulator(Simulator):
    """Simulator that works by finding numerical approximations for the differential equations outlined 
    in "Sailboat Model" through a naive approach with Euler's method.

    The state is a named tuple that contains the following properties:
        x:          Position of boat on east-west axis
        y:          Position of boat on north-south axis
        theta:      Heading relative to north
        omega:      Angular velocity of boat
        v:          Speed of the boat
        s_angle:    Sail angle
        r_angle:    Rudder angle
        time:       Current time in seconds

    The environment is a named tuple that contains:
        V:          Speed of true wind

    The control is a named tuple that contains:
        s_force:    Force on sail
        r_force:    Force on rudder
    """

    state = namedtuple('state', [
        'x',
        'y',
        'theta',
        'omega',
        'v',
        's_force',
        'r_force',
        'time'
    ])

    env = namedtuple('env', [
        'V',
    ])

    control = namedtuple('control', [
        's_angle',
        'r_angle'
    ])

    def __init__(self, step_size, beta=None, fric_t=None, fric_a=None, s_lift=None, r_lift=None, r_s=None, r_r=None,
                 L=None, m=None, J=None):
        """Initialize the simulator with the following parameters:
        step_size:          Time step size (in ms) when using Euler's method
        beta:               Drift coefficient
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
        self.fric_t = fric_t
        self.fric_a = fric_a
        self.s_lift = s_lift
        self.r_lift = r_lift
        self.r_s = r_s
        self.r_r = r_r
        self.L = L
        self.m = m
        self.J = J

    def simulate(self, prev_state, env, control, interval):
        fullsteps = interval // self.step_size

        state = prev_state

        # Simulates all full steps
        for _ in range(fullsteps):
            dt = self.step_size / 1000  # convert ms to seconds
            state = self.next_state(state, env, control, dt)

        # Simulates remainder (if the interval is not multiple of step_size)
        if interval % self.step_size > 0:
            dt = (interval % self.step_size) / 1000
            state = self.next_state(state, env, control, dt)

        return state

    def next_state(self, prev_state, env, control, dt):
        # if not isinstance(prev_state, self.state):
        #    raise Exception('prev_state must be of type given by self.state')

        prev_state = prev_state._asdict()
        env = env._asdict()
        control = control._asdict()
        next_state = self.state(
            x=self.x(dt, **prev_state, **env, **control),
            y=self.y(dt, **prev_state, **env, **control),
            theta=self.theta(dt, **prev_state, **env, **control),
            v=self.v(dt, **prev_state, **env, **control),
            omega=self.omega(dt, **prev_state, **env, **control),
            s_force=self.s_force(**prev_state, **env, **control),
            r_force=self.r_force(**prev_state, **env, **control),
            time=self.time(dt, **prev_state, **env, **control)
        )
        return next_state

    # gets next x position
    def x(self, dt, x=None, v=None, theta=None, **kwargs):
        x_dot = v * cos(theta)
        return x + x_dot * dt

    # gets next y position
    def y(self, dt, y=None, v=None, theta=None, V=None, **kwargs):
        y_dot = v * sin(theta) - self.beta * V
        return y + y_dot * dt

    # gets next heading theta
    def theta(self, dt, theta, omega, **kwargs):
        theta_dot = omega
        return (theta + theta_dot * dt) % (2*pi)  # theta stays within [0, 2pi]

    # gets next tangential velocity v
    def v(self, dt, s_angle=None, s_force=None, r_angle=None, r_force=None, v=None, **kwargs):
        v_dot = (s_force * sin(s_angle) - r_force *
                 sin(r_angle) - self.fric_t * v ** 2) / self.m
        return v + v_dot * dt

    # gets next rotational acceleration omega
    def omega(self, dt, s_angle=None, s_force=None, r_force=None, r_angle=None, omega=None, v=None, **kwargs):
        omega_dot = (s_force * (self.L - self.r_s * cos(s_angle)) +
                     -1 * r_force * self.r_r * cos(r_angle) - self.fric_a * omega) / self.J
        """print('a: {} b: {} c: {} net {} cur: {}'.format(
            round(s_force * (self.L - self.r_s * cos(s_angle)), 4),
            round(-1 * r_force * self.r_r * cos(r_angle), 4),
            round(-1 * self.fric_a * omega, 4),
            round(omega_dot, 4),
            round(omega, 4)
        ))"""
        return omega + omega_dot * dt

    def time(self, dt, time=None, **kwargs):
        return time + dt

    # intermediate link variables
    def link(self, prev_state, env, control):
        return {
            's_force': self.s_force(**prev_state, **env, **control),
            'r_force': self.r_force(**prev_state, **env, **control)
        }

    # gets the sail force
    def s_force(self, s_angle=None, V=None, theta=None, v=None, **kwargs):
        return self.s_lift * V * cos(theta + s_angle) - v * sin(s_angle)

    # gets the ruder force
    def r_force(self, v=None, r_angle=None, **kwargs):
        return self.r_lift * v * sin(r_angle)
