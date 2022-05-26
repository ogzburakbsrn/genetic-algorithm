import math
import sys

from icos import ICOS_Connection


def main():
    try:
        # if running the example in embedded mode set the port to the same number as in the
        # Model.CONNECT UI
        icos = ICOS_Connection(port=0)
    except Exception as exc:
        print(str(exc))
        sys.exit(-1)

    end_time = icos.getEndTime()
    calc_frequency = 100.0
    micro_steps = int(
        math.ceil(end_time * calc_frequency))  # ceil to always end with a full timestep, even if end time is not aligned
    couple_stepsize = icos.getModelDefsSpecial()['TimeStep']
    if couple_stepsize < 1 / calc_frequency:
        error_string = "internal timestep is <" + str(1 / calc_frequency) \
                      + "s>. Provided coupling step size <" + str(couple_stepsize) \
                      + "s> is smaller. Which is not allowed, aborting Simulation!"
        icos.sendWarningMsg(2, error_string)
        print(error_string)
        sys.exit(-2)

    output1 = 10
    step_number = 1
    list_values = [0, 0, 0, 0, 0, 0, 0, 0, 10, 20, 30, 15, 15, 20, 50, 10, 42, 19, 36, 13]

    for x in range(micro_steps + 1):
        tstep = (float(x) / calc_frequency)
        step_number += 1
        list_value = list_values[step_number]
        output1 = icos.getScalarInput("from_cruiseM", tstep)

        output1 *= x

        icos.postScalarOutput("to_cruiseM", tstep, output1)
        icos.postScalarOutput("list_output", tstep, list_value)

if __name__ == "__main__":
    main()
