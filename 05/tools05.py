import re
from typing import Iterable, NamedTuple


class Range(NamedTuple):
    start: int
    end: int


class MapEntry(NamedTuple):
    """
    A `MapEntry` represents a translation from a range of location numbers
    to a new range with a specific offset.
    """
    range: Range
    offset: int = 0

    @classmethod
    def from_file_entry(cls, destination_start: int, source_start: int, length: int):
        """
        Map entries in the input file are represented somewhat
        counter-intuitively so this class method creates a MapEntry from
        that input representation.
        """
        return cls(
            range=Range(source_start, source_start + length),
            offset=destination_start-source_start
        )

    def translate(self, number):
        """
        Translate the location `number` through the map entry,
        i.e. displace the number by the offset, as long as
        the number is within the map entry's input range.
        """
        if self.range.start <= number < self.range.end:
            return number + self.offset
        else:
            raise ValueError


class Map:
    """
    A Map is essentially a collection of `MapEntry`s. It translates any
    location number to a new one, using the appropriate map entry, the
    map entry with an input range that contains the location number.
    """

    def __init__(self, source: str, destination: str, entries):
        self.source = source
        self.destination = destination
        self.entries = sorted(entries, key=lambda entry: entry.range.start)

    @classmethod
    def from_file_entries(cls, source: str, destination: str, entries):
        return cls(
            source=source,
            destination=destination,
            entries=(MapEntry.from_file_entry(*entry) for entry in entries)
        )

    def translate(self, number):
        for entry in self.entries:
            try:
                return entry.translate(number)
            except ValueError:
                pass
        return number

    def translate_ranges(self, ranges: Iterable[Range]):
        """
        Translate an iterable of ranges through the map.

        The result is another iterable of ranges, possibly more than the
        original ones, since the original ones can be split when they hit
        the boundaries of the map entries

        Note: The `ranges` need to be *sorted* by their start location.
        Internally, the map entries are also sorted so the translation
        resembles a merge-sort, i.e. only one range and map entry are
        considered at a time.
        """
        input_range_iterator = iter(ranges)
        map_entry_iterator = iter(self.entries)
        # examine one input range and map entry at a time
        # (assuming input ranges and map entries are sorted)
        input_range = next(input_range_iterator)
        map_entry = next(map_entry_iterator)
        while True:
            if input_range.start < map_entry.range.start:
                # the input range starts before the map entry
                if input_range.end <= map_entry.range.start:
                    # the input range ends before the map entry begins:
                    # return the entire input range: all locations in this
                    # range are untranslated
                    yield input_range
                    try:
                        # advance to the next input range
                        input_range = next(input_range_iterator)
                    except StopIteration:
                        break
                else:
                    # return a range that is truncated up until the start of
                    # the map range: locations in these range are untranslated
                    yield Range(
                        start=input_range.start,
                        end=map_entry.range.start
                    )
                    input_range = input_range._replace(start=map_entry.range.start)
            elif input_range.start > map_entry.range.end:
                # the input range starts after the map entry ends:
                # return nothing
                try:
                    # advance to the next map entry
                    map_entry = next(map_entry_iterator)
                except StopIteration:
                    yield input_range
                    yield from input_range_iterator
                    break
            elif input_range.end <= map_entry.range.end:
                # the input range ends before the map entry ends:
                # return the entire input range *translated*
                yield Range(
                    start=input_range.start + map_entry.offset,
                    end=input_range.end + map_entry.offset
                )
                try:
                    # advance to the next input range
                    input_range = next(input_range_iterator)
                except StopIteration:
                    break
            else:
                # the input range ends after the map entry ends:
                # return *part* of the input range (up to the end of
                # the map range) *translated*...
                yield Range(
                    start=input_range.start + map_entry.offset,
                    end=map_entry.range.end + map_entry.offset
                )
                # and truncate the input range so that its start
                # now coincides with the end of the current map range
                input_range = input_range._replace(start=map_entry.range.end)
                try:
                    # advance to the next map range
                    map_entry = next(map_entry_iterator)
                except StopIteration:
                    yield input_range
                    yield from input_range_iterator
                    break


def parse_file(lines):
    line_iterator = iter(lines)
    # process first line
    line = next(line_iterator)
    seeds = [int(number) for number in line[7:].split()]
    # skip empty line
    line = next(line_iterator)
    # process the rest of the lines, i.e. the maps
    maps = []
    done = False
    while not done:
        line = next(line_iterator)
        # first line of a map
        source, destination = re.match(r'([a-z]+)-to-([a-z]+) map:', line).groups()
        # remaining lines contain the map entries
        entries = []
        line = next(line_iterator).strip()
        while len(line) > 0:
            entries.append([int(number) for number in line.split()])
            try:
                line = next(line_iterator).strip()
            except StopIteration:
                done = True
                break
        maps.append(Map.from_file_entries(source, destination, entries))
    return seeds, maps
