import math
def telemetry_state(t_s: float):
    roll = 5.0*math.sin(t_s/200.0)
    pitch = 3.0*math.sin(t_s/140.0)
    yaw = 8.0*math.sin(t_s/90.0)

    # faking the power -oscillating between 40 and 100
    soc = 70.0 + 30.0*math.sin(t_s/400.0)

    # faking ground contact - 10 minutes in contact and 10 minutes out
    cycle = int(t_s//600.0)%2 == 0
    in_contact = cycle

    return {
        "attitude": {
            "roll": roll,
            "pitch": pitch,
            "yaw": yaw
        },
        "power": {"soc": soc,
                  "gen_w": 120.0 if in_contact else 80.0},
        "link":{'in_contact': in_contact}
    }

    