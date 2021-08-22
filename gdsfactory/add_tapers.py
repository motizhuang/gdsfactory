from typing import Callable, List, Optional, Tuple

import gdsfactory as gf
from gdsfactory.cell import cell
from gdsfactory.component import Component, ComponentReference
from gdsfactory.components.taper import taper as taper_function
from gdsfactory.port import Port
from gdsfactory.types import ComponentFactory


def get_ports_and_tapers(
    component: Component,
    taper: ComponentFactory = taper_function,
    select_ports: Optional[Callable] = None,
) -> Tuple[List[Port], List[ComponentReference]]:
    """returns ports and taper elements for a component"""
    ports = []
    elements = []

    taper = gf.call_if_func(taper)
    ports = select_ports(component.ports) if select_ports else component.ports

    for port in component.ports.copy().values():
        if port.name in ports.key():
            taper_ref = taper.ref()
            taper_ref.connect(taper_ref.ports["o2"].name, port)
            elements.append(taper_ref)
            ports.append(taper_ref.ports["o1"])
    return ports, elements


@cell
def add_tapers(
    component: Component,
    taper: ComponentFactory = taper_function,
    select_ports: Optional[Callable] = None,
) -> Component:
    """returns component optical tapers for component"""

    c = gf.Component()

    ports = select_ports(component.ports) if select_ports else component.ports

    for port_name, port in ports.copy().items():
        if port.name in ports.keys():
            taper_ref = c << taper(width2=port.width)
            taper_ref.connect(taper_ref.ports["o2"].name, port)
            c.add_port(name=port_name, port=taper_ref.ports["o1"])
        else:
            c.add_port(name=port_name, port=port)
    c.add_ref(component)
    c.auto_rename_ports()
    return c


if __name__ == "__main__":
    c0 = gf.components.straight(width=2)
    # t = gf.components.taper(width2=2)
    c1 = add_tapers(component=c0)
    c1.show()

    # print(cc.ports.keys())
    # print(cc.settings.keys())
    # cc.show()

    # ports, elements = add_taper_elements(component=c, taper=t)
    # c.ports = ports
    # c.add(elements)
    # c.show()
    # print(c.ports)