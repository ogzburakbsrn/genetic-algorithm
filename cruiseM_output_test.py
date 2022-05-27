import math
import sys
from icos import ICOS_Connection


def read_cycle(file_name):
    cycle_file = file_name
    cycle_time = []
    cycle_velocity = []

    with open(cycle_file, encoding="utf-8", newline='') as file:
        file.readline()
        file.readline()
        for row in file:
            time, velocity, _, _, _, _, _ = row.strip('\n').split(',')
            cycle_time.append(float(time))
            cycle_velocity.append(float(velocity))
    return cycle_time, cycle_velocity


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
        math.ceil(
            end_time * calc_frequency))  # ceil to always end with a full timestep, even if end time is not aligned
    couple_step_size = icos.getModelDefsSpecial()['TimeStep']

    cycle_time, cycle_velocity = read_cycle(
        'C:\\Users\\u26j49\\Desktop\\Projects\\Code\\genetic-algorithm\\WLTC_3b_automatic.csv')

    if couple_step_size < 1 / calc_frequency:
        error_string = "internal timestep is <" + str(1 / calc_frequency) \
                       + "s>. Provided coupling step size <" + str(couple_step_size) \
                       + "s> is smaller. Which is not allowed, aborting Simulation!"
        icos.sendWarningMsg(2, error_string)
        print(error_string)
        sys.exit(-2)

    step_number = 1

    for x in range(micro_steps + 1):  # MAIN LOOP FOR CALCULATIONS
        time_step = (float(x) / calc_frequency)
        cruise_input = icos.getScalarInput("from_cruiseM", time_step)

        if time_step - int(time_step) == 0:
            output1 = cycle_velocity[int(time_step)]
        else:
            last_integer = math.floor(time_step)
            next_integer = math.ceil(time_step)
            output1 = (cycle_velocity[next_integer] - cycle_velocity[last_integer]) * (time_step - last_integer) + \
                      cycle_velocity[last_integer]

        icos.postScalarOutput("to_cruiseM", time_step, output1)
        icos.postScalarOutput("list_output", time_step, cruise_input)


if __name__ == "__main__":
    main()
