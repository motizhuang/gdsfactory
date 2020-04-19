"""
a container creates a new component that contains the original component inside with some extra elements:

it makes sure that some of the important settings are copied from the original component to the new component

"""

import functools
from inspect import signature
import pp


def container(component_function):
    """ decorator for creating a new component that copies some properties from the original component

    Functions decorated with container will return a new component if you pass suffix kwarg

    .. plot::
      :include-source:

      import pp

      @pp.container
      def add_padding(component):
          w, h = component.xsize, component.ysize
          c = pp.Component()
          points = [[w, h], [w, 0], [0, 0], [0, h]]
          c.add_polygon(points, layer=layer)
          return c

      c = pp.c.waveguide()
      cp = add_padding(c)
      pp.plotgds(c)

    """

    @functools.wraps(component_function)
    def wrapper(*args, **kwargs):
        old = None
        if "component" not in kwargs:
            if args and isinstance(args[0], pp.Component):
                old = args[0]
            else:
                raise ValueError(
                    f"containers require a component keyword argument, or first non keyword argument"
                )
        old = old or kwargs.get("component")
        new = component_function(*args, **kwargs)

        sig = signature(component_function)
        new.settings.update(**{p.name: p.default for p in sig.parameters.values()})
        new.ports = new.ports or old.ports.copy()
        new.settings["component"] = old.settings.copy()
        new.test_protocol = new.test_protocol or old.test_protocol.copy()
        new.data_analysis_protocol = (
            new.data_analysis_protocol or old.data_analysis_protocol.copy()
        )
        return new

    return wrapper


@container
def add_padding(
    component, padding=50, x=None, y=None, layers=[pp.LAYER.PADDING], suffix="p"
):
    """ adds padding layers to component"""
    c = pp.Component(name=f"{component.name}_{suffix}")
    c << component
    x = x or padding
    y = y or padding
    points = [
        [c.xmin - x, c.ymin - y],
        [c.xmax + x, c.ymin - y],
        [c.xmax + x, c.ymax + y],
        [c.xmin - x, c.ymax + y],
    ]
    for layer in layers:
        c.add_polygon(points, layer=layer)
    return c


def test_container():
    old = pp.c.waveguide()
    suffix = "p"
    name = f"{old.name}_{suffix}"
    new = add_padding(component=old, suffix=suffix)
    assert new != old, f"new component {new} should be different from {old}"
    assert new.name == name, f"new name {new.name} should be {name}"
    assert len(new.ports) == len(
        old.ports
    ), f"new component {len(new.ports)} ports should match original {len(old.ports)} ports"
    # assert len(new.settings) == len(
    #     old.settings
    # ), f"new component {new.settings} settings should match original {old.settings} settings"
    return new


def test_container2():
    old = pp.c.waveguide()
    suffix = "p"
    name = f"{old.name}_{suffix}"
    new = add_padding(old, suffix=suffix)
    assert new != old, f"new component {new} should be different from {old}"
    assert new.name == name, f"new name {new.name} should be {name}"
    assert len(new.ports) == len(
        old.ports
    ), f"new component {len(new.ports)} ports should match original {len(old.ports)} ports"
    return new


def test_container3():
    old = pp.c.waveguide()
    suffix = "p"
    name = f"{old.name}_{suffix}"
    new = add_padding(component2=old, suffix=suffix)
    assert new != old, f"new component {new} should be different from {old}"
    assert new.name == name, f"new name {new.name} should be {name}"
    assert len(new.ports) == len(
        old.ports
    ), f"new component {len(new.ports)} ports should match original {len(old.ports)} ports"
    return new


if __name__ == "__main__":
    c = test_container3()
    pp.show(c)
