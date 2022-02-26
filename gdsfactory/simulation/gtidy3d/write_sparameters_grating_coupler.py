import time

import numpy as np
import pandas as pd
import tidy3d as td
from omegaconf import OmegaConf

from gdsfactory.config import logger, sparameters_path
from gdsfactory.serialization import clean_value_json
from gdsfactory.simulation.get_sparameters_path import (
    get_sparameters_path_tidy3d as get_sparameters_path,
)
from gdsfactory.simulation.gtidy3d.get_results import _executor, get_results
from gdsfactory.simulation.gtidy3d.get_simulation_grating_coupler import (
    get_simulation_grating_coupler,
)
from gdsfactory.types import Component, List, PathType


def write_sparameters_grating_coupler(
    component: Component,
    dirpath: PathType = sparameters_path,
    overwrite: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """Get sparameter matrix from a gdsfactory grating coupler.

    TODO: Simulates each time using a different input port, right now it
    only launches from fiber and measures field inside the waveguide.

    it assumes grating coupler waveguide port is facing to the left (west)

    Args:
        component: grating coupler gdsfactory Component to simulate.
        dirpath: directory to store sparameters in CSV.
        overwrite: overwrites stored Sparameter CSV results.

    Keyword Args:
        port_extension: extend ports beyond the PML.
        layer_stack: contains layer numbers (int, int) to thickness, zmin.
        thickness_pml: PML thickness (um).
        xmargin: left/right distance from component to PML.
        xmargin_left: left distance from component to PML.
        xmargin_right: right distance from component to PML.
        ymargin: left/right distance from component to PML.
        ymargin_top: top distance from component to PML.
        ymargin_bot: bottom distance from component to PML.
        zmargin: thickness for cladding above and below core.
        clad_material: material for cladding.
        box_material:
        substrate_material:
        port_waveguide_name: input port name.
        port_margin: margin on each side of the port.
        distance_source_to_monitors: in (um) source goes before monitors.
        port_waveguide_offset: mode solver workaround.
            positive moves source forward, negative moves source backward.
        resolution: in pixels/um (20: for coarse, 120: for fine)
        wavelength_start: in (um).
        wavelength_stop: in (um).
        wavelength_points: number of wavelengths.
        plot_modes: plot source modes.
        num_modes: number of modes to plot.
        run_time_ps: make sure it's sufficient for the fields to decay.
            defaults to 10ps and counts on the automatic shutoff to stop earlier if needed.
        fiber_port_name:
        fiber_xoffset: fiber center xoffset to fiber_port_name
        fiber_z: fiber zoffset from grating zmax
        fiber_mfd: fiber mode field diameter (um)
        fiber_angle_deg: fiber_angle in degrees with respect to normal.
        material_name_to_tidy3d: dict of material stack materil name to tidy3d.

    """
    filepath = get_sparameters_path(
        component=component,
        dirpath=dirpath,
        **kwargs,
    )
    filepath_sim_settings = filepath.with_suffix(".yml")
    if filepath.exists() and not overwrite:
        logger.info(f"Simulation loaded from {filepath!r}")
        return pd.read_csv(filepath)

    start = time.time()
    sim = get_simulation_grating_coupler(component, **kwargs)
    sim_data = get_results(sim)
    sim_data = sim_data.result()

    direction_inp = "+"
    direction_out = "-"

    monitor_entering = (
        sim_data.monitor_data["waveguide"]
        .amps.sel(direction=direction_inp)
        .values.flatten()
    )
    monitor_exiting = (
        sim_data.monitor_data["waveguide"]
        .amps.sel(direction=direction_out)
        .values.flatten()
    )
    r = monitor_exiting / monitor_entering
    ra = np.unwrap(np.angle(r))
    rm = np.abs(r)

    t = monitor_exiting
    ta = np.unwrap(np.angle(t))
    tm = np.abs(t)

    sp = {}
    freqs = sim_data.monitor_data["waveguide"].amps.sel(direction="+").f
    sp["wavelengths"] = td.constants.C_0 / freqs.values
    sp["s11a"] = sp["s22a"] = ra
    sp["s11m"] = sp["s22m"] = rm

    sp["s12a"] = sp["s21a"] = ta
    sp["s12m"] = sp["s21m"] = tm

    end = time.time()
    df = pd.DataFrame(sp)
    df.to_csv(filepath, index=False)
    kwargs.update(compute_time_seconds=end - start)
    kwargs.update(compute_time_minutes=(end - start) / 60)

    filepath_sim_settings.write_text(OmegaConf.to_yaml(clean_value_json(kwargs)))
    logger.info(f"Write simulation results to {str(filepath)!r}")
    logger.info(f"Write simulation settings to {str(filepath_sim_settings)!r}")
    return df


def write_sparameters_grating_coupler_batch(
    components: List[Component], **kwargs
) -> List[pd.DataFrame]:
    """Returns Sparameters for a list of components
    runs batch of component simulations in paralell.

    Args:
        components: list of components

    """
    sp = [
        _executor.submit(write_sparameters_grating_coupler, component, **kwargs)
        for component in components
    ]
    return [spi.result() for spi in sp]


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    import gdsfactory as gf

    c = gf.components.grating_coupler_elliptical_arbitrary(
        widths=[0.343] * 25, gaps=[0.345] * 25
    )
    df = write_sparameters_grating_coupler(c)
    # t = df.s12m
    # print(f"Transmission = {t}")
    plt.plot(df.wavelengths, df.s12m)