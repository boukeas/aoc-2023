from math import sqrt


def distance(race_time, charge_time):
    """
    Return the distance that would be travelled given the race time and
    the charge time
    """
    return charge_time * (race_time - charge_time)


def winning_combinations_simple(race_time, record_distance):
    """
    Return the number of winning combinations naively, by iterating
    over the different charge times and calculating the number of
    times that the travelled distance exceeds the record distance.
    """
    combinations = 0
    beating = False
    for charge_time in range(race_time+1):
        if distance(race_time, charge_time) > record_distance:
            beating = True
            combinations += 1
        elif beating:
            break
    return combinations


def winning_combinations(race_time, record_distance):
    """
    Return the number of winning combinations by solving a quadratic equation

    The distance travelled is:
    charge_time * (race_time - charge_time)

    This distance needs to be greater than the `record_distance`:
    charge_time * (race_time - charge_time) > record_distance

    Solving this quadratic inequality provides floating point estimates
    for the shortest and longest charge times, that are then corrected
    to the closest integers that yield winning combinations.
    """
    sqrt_d = sqrt(race_time * race_time - 4 * record_distance)
    shortest = int((race_time - sqrt_d) / 2)
    if distance(race_time, shortest) < record_distance:
        shortest += 1
    elif distance(race_time, shortest) > record_distance:
        shortest -= 1
    longest = int((race_time + sqrt_d) / 2)
    if distance(race_time, longest) < record_distance:
        longest -= 1
    elif distance(race_time, longest) > record_distance:
        longest += 1
    combinations = longest - shortest
    return combinations
