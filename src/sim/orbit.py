import numpy as np
def orbit_state(t_s: float, period_s: float = 5400.0, alt_km: float = 500.0):
    """
    Simple equatorial circular orbit.
    t_s is simulation time in seconds.
    """
    angle = 2.0 * np.pi * (t_s % period_s) / period_s
    lat = 0.0
    lon = np.degrees(angle) % 360.0 - 180.0
    return {"lat": lat, "lon": lon, "alt_km": alt_km}