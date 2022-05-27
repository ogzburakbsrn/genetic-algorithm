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
