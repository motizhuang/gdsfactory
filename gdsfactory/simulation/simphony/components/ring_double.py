from simphony.models import Subcircuit

from gdsfactory.simulation.simphony.components.coupler_ring import coupler_ring
from gdsfactory.simulation.simphony.components.straight import (
    straight as straight_function,
)
from gdsfactory.simulation.simphony.plot_circuit import plot_circuit
from gdsfactory.simulation.simphony.types import ModelFactory


def ring_double(
    wg_width: float = 0.5,
    gap1: float = 0.2,
    gap2: float = 0.2,
    length_x: float = 4,
    radius: float = 5,
    length_y: float = 2,
    coupler: ModelFactory = coupler_ring,
    straight: ModelFactory = straight_function,
) -> Subcircuit:
    r"""Return double bus ring Model made of two couplers (ct: top, cb: bottom)
    connected with two vertical straights (yl: left, wr: right)

    .. code::

         --==ct==--
          |      |
          wl     wr length_y
          |      |
         --==cb==-- gap

          length_x


           ---=========---
        o2    length_x    o3
             /         \
            /           \    halfring2
           |             |
           o3           o2 ___
                            |
          wl            wr  | length_y
                           _|_
           o2            o3
           |             |
            \           /    halfring1
             \         /
           ---=========---
        o1    length_x    o4



    .. plot::
      :include-source:

      import gdsfactory as gf

      c = gf.components.ring_double(width=0.5, gap=0.2, length_x=4, radius=5, length_y=2)
      c.plot()


    .. plot::
        :include-source:

        import gdsfactory.simulation simphony as gs
        import gdsfactory.simulation.simphony.components as gc

        c = gc.ring_double()
        gs.plot_circuit(c)
    """

    straight = straight(length=length_y) if callable(straight) else straight
    halfring1 = (
        coupler(length_x=length_x, radius=radius, gap=gap1, wg_width=wg_width)
        if callable(coupler)
        else coupler
    )
    halfring2 = (
        coupler(length_x=length_x, radius=radius, gap=gap2, wg_width=wg_width)
        if callable(coupler)
        else coupler
    )
    halfring1.rename_pins("o1", "o2c", "o3c", "o4")
    halfring2.rename_pins("o3", "o2c", "o3c", "o2")

    # the interface method will connect all of the pins with matching names
    # between the two components together
    # halfring1.interface(halfring2)
    halfring1["o2c"].connect(halfring2["o3c"])
    halfring1["o3c"].connect(halfring2["o2c"])

    # bundling the circuit as a Subcircuit allows us to interact with it as if it were a component
    return halfring1.circuit.to_subcircuit()


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    c = ring_double()
    plot_circuit(c)
    plt.show()
