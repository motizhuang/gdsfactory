import matplotlib.pyplot as plt
from simphony.libraries import siepic
from simphony.simulators import SweepSimulator

if __name__ == "__main__":

    gc_input = siepic.GratingCoupler()
    y_splitter = siepic.YBranch()
    wg_long = siepic.Waveguide(length=150e-6)
    wg_short = siepic.Waveguide(length=50e-6)
    y_recombiner = siepic.YBranch()
    gc_output = siepic.GratingCoupler()

    # next we connect the components to each other
    # you can connect pins directly:
    y_splitter["pin1"].connect(gc_input["pin1"])

    # or connect components with components:
    # (when using components to make connections, their first unconnected pin will
    # be used to make the connection.)
    y_splitter.connect(wg_long)

    # or any combination of the two:
    y_splitter["pin3"].connect(wg_short)
    # y_splitter.connect(wg_short["pin1"])

    # when making multiple connections, it is often simpler to use `multiconnect`
    # multiconnect accepts components, pins, and None
    # if None is passed in, the corresponding pin is skipped
    y_recombiner.multiconnect(gc_output, wg_short, wg_long)

    simulator = SweepSimulator(1500e-9, 1600e-9)
    simulator.multiconnect(gc_input, gc_output)

    f, p = simulator.simulate()
    plt.plot(f, p)
    plt.title("MZI")
    plt.tight_layout()
    plt.show()

    # c = mzi()
    # plot_circuit(c)
    # plt.show()
