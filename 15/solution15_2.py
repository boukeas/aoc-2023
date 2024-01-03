from collections import defaultdict
from sys import argv

from tools15 import hash, parse_file


def parse_instruction(instruction):
    """
    Parse the string corresponding to an instruction and return a triplet
    containing:
    - the operation to be performed (either '-' or '=')
    - the label
    - the focal length of the lens in the case of a '=' operation or
      None otherwise
    """
    if instruction[-1] == '-':
        return ('-', instruction[:-1], None)
    else:
        return ('=', instruction[:-2], int(instruction[-1]))


def remove(boxes, label):
    """
    Given the current state of the `boxes`, remove the lens
    with the specified `label` from the corresponding box
    """
    box_index = hash(label)
    labels, lenses = boxes[box_index]
    try:
        lens_index = labels.index(label)
    except ValueError:
        pass
    else:
        labels.pop(lens_index)
        lenses.pop(lens_index)


def add(boxes, label, focal_length):
    """
    Given the current state of the `boxes`, add the lens
    with the specified `label` to the corresponding box
    """
    box_index = hash(label)
    labels, lenses = boxes[box_index]
    try:
        # find the index of the label in the box
        lens_index = labels.index(label)
    except ValueError:
        # new lens (label), added to the back of the box
        labels.append(label)
        lenses.append(focal_length)
    else:
        # existing lens (label), replaced by new focal length
        lenses[lens_index] = focal_length


def power(boxes):
    """
    Return the total focusing power of the lenses in the boxes:

    > The focusing power of a single lens is the result of multiplying:
    > - One plus the box number of the lens in question.
    > - The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
    > - The focal length of the lens.
    """
    return sum(
        (1 + box_index) * slot * lens
        for box_index, contents in boxes.items()
        for slot, lens in enumerate(contents[1], start=1)
    )


if __name__ == '__main__':
    with open(argv[1]) as file:
        instructions = parse_file(file.read())

    boxes = defaultdict(lambda: ([], []))
    for instruction in instructions:
        operation, label, number = parse_instruction(instruction)
        if operation == '-':
            remove(boxes, label)
        else:
            add(boxes, label, number)

    result = power(boxes)
    print(result)
