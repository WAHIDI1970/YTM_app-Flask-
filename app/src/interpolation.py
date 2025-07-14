import numpy as np
from scipy.interpolate import interp1d

def interpolate_rate(x: np.ndarray,
                     y: np.ndarray,
                     x_new: np.ndarray,
                     method: str = "linear",
                     extrapolate: bool = True) -> np.ndarray:
    fill = "extrapolate" if extrapolate else None
    f = interp1d(x, y, kind=method,
                 fill_value=fill,
                 bounds_error=not extrapolate)
    return f(x_new)
