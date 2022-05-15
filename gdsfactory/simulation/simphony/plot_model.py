from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import speed_of_light
from simphony import Model


def plot_model(
    model: Model,
    pin_in: str = "o1",
    pins: Optional[List[str]] = None,
    wavelengths=None,
    logscale: bool = True,
    fig=None,
    phase: bool = False,
) -> None:
    """Plot simphony Sparameters for a model

    Args:
        model: simphony model.
        pin_in: input pin name.
        pins: list of pins.
        wavelengths: (m).
        logscale: True plots in dB.
        fig: figure.
        phase: plots phase.

    .. plot::
        :include-source:

        import gdsfactory.simulation simphony as gs
        import gdsfactory.simulation.simphony.components as gc

        c = gc.mmi1x2()
        gs.plot_model(c)
    """
    m = model() if callable(model) else model

    if wavelengths is None:
        if hasattr(m, "wavelengths"):
            wavelengths = m.wavelengths
        else:
            wavelengths = np.linspace(1520e-9, 1580e-9, 2000)

    f = speed_of_light / wavelengths
    s = m.s_parameters(freqs=f)
    pins_model = [pin if isinstance(pin, str) else pin.name for pin in m.pins]
    pins = pins or pins_model

    if not isinstance(pins, (tuple, set, list)):
        raise ValueError(f"pins {pins!r} need to be a tuple, set or list")

    for pin in pins:
        if pin not in pins_model:
            raise ValueError(f"{pin!r} not in {pins_model}")

    if pin_in not in pins_model:
        raise ValueError(f"pin_in = {pin_in!r} not in {pins_model}")

    pin_in_index = pins_model.index(pin_in)

    fig = fig or plt.subplot()
    ax = fig.axes

    for pin_out in pins:
        pin_out_index = pins_model.index(pin_out)
        if phase:
            y = np.angle(s[:, pin_out_index, pin_in_index])
            ylabel = "angle (rad)"
        else:
            y = np.abs(s[:, pin_out_index, pin_in_index]) ** 2
            y = 10 * np.log10(y) if logscale else y
            ylabel = "|S (dB)|" if logscale else "|S|"
        ax.plot(wavelengths * 1e9, y, label=pin_out)
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel(ylabel)
    plt.legend()
    plt.show()
    return ax


if __name__ == "__main__":
    from gdsfactory.simulation.simphony.components.coupler_ring_siepic import (
        coupler_ring_siepic,
    )

    m = coupler_ring_siepic()

    # from gdsfactory.simulation.simphony.components.mmi1x2 import  mmi1x2
    # m = mmi1x2()
    # w = np.linspace(1520, 1570, 1024) * 1e-9

    # plot_model(coupler, pin_in="n1")
    # plt.legend()
    # plt.show()

    # m = straight()
    plot_model(m, phase=False)
    plt.show()
