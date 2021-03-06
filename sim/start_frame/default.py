from sim.frame import Frame
default = Frame.from_dict({
    "state": {
        "s_force": 0,
        "r_force": 0,
        "omega": 0,
        "theta": 0,
        "v": 0,
        "x": -2,
        "y": -2,
        "time": 0
    },
    "control": {
        "s_angle": 0,
        "r_angle": 0
    },
    "env": {
        "V": 0.5
    }
})
