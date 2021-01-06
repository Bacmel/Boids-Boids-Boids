import numpy as np
from math import cos, sin, atan2, pi
import matplotlib.pyplot as plt


def circular_mean(X, I):
    """Compute the circular mean of the given set of values X in I.

    Args:
        X (list[float]): The set of values.
        I (tuple[float,float]): The range these values are in.

    Returns:
        float: The circular mean.
    """
    assert I[0] < I[1]
    lenI = I[1] - I[0]
    pulse = 2 * pi / lenI
    sum_cos = 0.
    sum_sin = 0.
    for x in X:
        sum_cos += cos(pulse * x)
        sum_sin += sin(pulse * x)
    return atan2(sum_sin, sum_cos) / pulse


if __name__ == "__main__":
    vs = np.array([np.array([-5, 4]), np.array([4, -5])])
    mean_v = np.array([circular_mean(vs[:, 0], (-5, 5)),
                       circular_mean(vs[:, 1], (-5, 5))])
    print(f"vs: {vs}")
    print(f"mean: {mean_v}")

    for v in vs:
        plt.plot(v[0], v[1], '.k')
    plt.plot(mean_v[0], mean_v[1], '.g')
    plt.show()
