"""Straight Doped PIN waveguide."""

import gdsfactory as gf
from gdsfactory.components.extension import extend_ports
from gdsfactory.components.straight import straight
from gdsfactory.components.taper import taper_strip_to_ridge
from gdsfactory.cross_section import rib

straight_rib = gf.partial(straight, cross_section=rib)


straight_rib_with_strip_tapers = gf.partial(
    extend_ports,
    component=straight_rib,
    extension_factory=taper_strip_to_ridge,
    port1="E0",
    port2="W0",
)


if __name__ == "__main__":
    c = straight_rib()
    c = straight_rib_with_strip_tapers()
    c.show()