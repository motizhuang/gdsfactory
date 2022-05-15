"""SIEPIC coupler sample."""

from simphony.libraries import siepic


def coupler_ring_siepic(
    gap: float = 0.2,
    radius: float = 10.0,
    width: float = 0.5,
    thickness: float = 0.22,
    length_x: float = 5.0,
    **kwargs,
):
    r"""Return simphony Directional coupler model.

    Args:
        gap: ring gap (um).
        radius: bend radius (um).
        width: waveguide width.
        thickness: (nm).
        length_x: coupling length (nm).


    .. code::

               n2            n4
               |             |
                \           /
                 \         /
               ---=========---
            n1    length_x    n3



    .. plot::
        :include-source:

        import gdsfactory as gf

        c = gf.components.coupler(gap=0.2, length=10)
        c.plot()

    .. plot::
        :include-source:

        import gdsfactory.simulation.simphony.components as gc
        import gdsfactory.simulation simphony as gs

        c = gc.coupler()
        gs.plot_model(c)

    """

    model = siepic.HalfRing(
        gap=gap * 1e-6,
        radius=radius * 1e-6,
        width=width * 1e-6,
        thickness=thickness * 1e-6,
        length_x=length_x * 1e-6,
    )
    model.rename_pins("o1", "o2", "o3", "o4")
    return model


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    from gdsfactory.simulation.simphony import plot_model

    c = siepic.HalfRing(
        gap=200e-9, radius=12e-6, width=500e-9, thickness=220e-9, couple_length=0.0
    )
    plot_model(c)
    print(c)
    plt.show()
