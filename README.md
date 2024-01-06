# Advent of Code 2023

These are my solutions.

I try to make them elegant, efficient and _readable_, altough I cannot claim that they are perfectly refined or blazingly fast. I just enjoy the process of wrestling with the puzzles.

## Repository Structure

The solutions to Part 1 and Part 2 of Day N are stored in folder `N/` as `solutionN_1.py` and `solutionN_2.py`. Code that is common between the two parts is found in `toolsN.py`.

The input files are `inputN.test.txt` and `inputN.txt`, or some variation thereof when there are more test or input files.

## Brief Notes

### Day 1: Trebuchet

The one about extracting the (sometimes spelled out) numbers from the input.

I used regular expressions which I think really simplifies the solution, especially in the second part.

### Day 2: Cube Conundrum

The one with the red, blue and green cube game.

### Day 3: Gear ratios

The one with the engine schematic and the labelled parts.

I tried to avoid multiple scans of the schematic. The input lines are processed in pairs, matching for tags and symbols and then combining the match ranges to check for overlaps, in order to detect the parts.

### Day 4: Scratchcards

The one where winning numbers get you more copies of the cards that follow.

I used a dict to keep a tally of how many copies of each scratchcard are available.

### Day 5: If You Give A Seed A Fertilizer

The one where numbers are translated through a series of consecutive maps.

Each map splits its input into ranges and applies a different offset to each range.

In the second part, instead of translating individual numbers through the maps (which would be intractable), translate entire ranges. The trick is to split these ranges when they span the boundaries of a maps' input ranges.

Quite a challenging problem (as evidenced by the visible drop in the Stats and the proportion of silver stars).

### Day 6: Wait For It

The one where you charge and then release a toy boat.

The distance travelled by the toy boat is described by a quadratic function of the charge time. Just solve the appropriate equation directly, rather than simulating the race and its individual time steps.

### Day 7: Camel Cards

The one with the modified version of poker.

I used a `collections.Counter` dict for each hand, which simplified the selection structure required for determining the type of each hand.

### Day 8: Haunted Wasteland

The one where you follow Left/Right instructions in a binary directed graph.

In the second part, there are different starting nodes and each one leads to a separate traversal through the graph. It is key to understand that these traversals are periodic, i.e. they pass through the nodes ending in `'Z'` at regular (but different) time intervals. So instead of following the instructions _simultaneously_ until all traversals synchronise (which would be intractable), it is sufficient to follow the instructions _separately_ and record the individual periods. The least common multiple of these periods is when the traversals will synchronise.

### Day 9: Mirage Maintenance

The one where we extrapolate values using finite differences.

### Day 10: Pipe Maze

The one where you follow the pipes.

To find the area enclosed by the loop I scanned the map row by row. In every row, I kept track of whether or not I was outside or inside the loop (counting the internal points in the latter case). The only subtle point arises when you traverse horizontal boundaries like these: `F--7`, `L--J`, `F--J` and `L--7`. The first two cases are convex boundaries and the inside/outside status when the boundary ends remains the same. In the latter case though, the boundaries are concave and the inside/outside status flips the boundary ends.

### Day 11: Cosmic Expansion

The one where gaps between galaxies expand.

I implemented a single expansion function that accepts the expansion factor as an argument and also works the same for rows and columns, so I provided the same solution for both parts of the puzzle.

### Day 12: Hot Springs

The (tricky) one with the damaged patterns.

I counted the number of different possible arrangements recursively. Each recursive call gives rise to at most two more recursive calls, corresponding to whether or not it is possible to assign the _entire_ next contiguous group of springs to the beginning of the condition record. This essentially boils down to search in a binary tree. Speed is improved by caching the function results.

### Day 13: Point of Incidence

The one with the horizontal and vertical axes of symmetry.

A vertical axis of symmetry must be an axis of symmetry for all rows. Similary, a horizontal axis of symmetry must be an axis of symmetry for all columns. So the search for an axis of symmetry can be narrowed down very quickly as we traverse the rows (or columns) of the input matrix, checking only candidate axes that were not rejected on previous rows (or columns).

For the second part, we count "discrepancies": pairs of positions that are not symmetrical with respect to a candidate axis. A candidate axis for which there only exists a single discrepancy is the result we are looking for.

### Day 14: Parabolic Reflector Dish

The one where you tilt in different directions and measure the "load".

Calculating the load after 1000000000 cycles is intractable. However, the value of the load settles into a periodic pattern after a certain number of cycles so the real question is how that period can be calculated.

My approach was to perform 1000 cycles and to map each load value to the cycle numbers at which it appears. The periodicity there is much clearer (and can easily be used to extract the period by visual inspection). What I did then was to compute the distances between the cycle numbers and _apply a Discrete Fourrier Transform_ to get the period.

### Day 15: Lens Library

The one where you decode instructions to place lenses in boxes.

### Day 16: The Floor Will Be Lava

The one where you reflect and split light beams.

### Day 17: Clumsy Crucible

The one where you find a minimal path under constraints.

This is solved using breadth-first, branch-and-bound search (i.e. all nodes with a cost that exceeds the current best solution are pruned). However, what is interesting in this case is that the moves explored are not single-step moves but rather walk-and-turn moves, i.e. a single move would be "walk 3 steps and turn south". This subtly affects the way search is performed but directly reflects the problem constraints and also makes searching more efficient. 

During search, nodes are expanded using a neighbour generator that is passed as an argument and it's just this generator that differs slightly between the two parts, allowing up to three steps in any direction in the first part and between four and ten steps in the second.

### Day 18: Lavaduct Lagoon

The one where you decode and follow instructions in order to dig a hole (and fill it with lava).

The area of the polygon is calculated using the shoelace formula and then Pick's theorem is used to derive the number of internal points. The number of points on the boundary plus the internal ones is the result. The main program is identical between the two parts, what changes is simply how the raw instructions from the input are interpreted.

### Day 19: Aplenty

The one where you accept or reject records based on a system of rules and conditions.

The rules and the conditions they comprise are essentially a convoluted selection structure, i.e. a sequences of if-elif-else statements on the values of the record attributes. Accepting or rejecting a record boils down to checking the conditions until an accepting or rejecting branch is reached.

For the second part, rather than feeding a specific record with specific values for the attributes through the selection structure, we feed entire _domains_, which we split recursively every time we encounter a condition (which is slightly reminescent of Day 5).

### Day 20: Pulse Propagation

The one where different types of modules send pulses to each other.

An object-oriented approach seemed really natural for this one. All modules have the same interface, i.e. they send pulses to their destination modules and receive pulses from their source modules. So the different modules are all derived from the base `Module` class and the derived classes differ in how they process the pulses they receive. There is also a message queue: all pulses that are to be sent from a source module to a destination module are entered in the queue.

The results required for each of the two parts are computed by a different class called a `Reporter`. All reporters are notified of the events in the message queue: for the first part, the recorder counts low and high pulses. For the second part, the recorder counts button presses and keeps track of when then source modules that will eventually trigger the `rx` module fire a `high` pulse.

Note that these `high` pulses are fired from the specific source modules periodically. Once we now their individual periods, the least common multiple of these periods reveals when they will all fire a `high` pulse simultaneously.

### Day 21: Step Counter

The one where you count the number of reachable points in a (possibly infinite map).

The second part is also to be remembered as the one I wasn't able to solve without searching for hints, so no code is included here for it.

### Day 22: Sand Slabs

The one like Tetris!

I ordered the blocks by (minimal) z-coordinate and "dropped" them to their final position. In order to do so, I kept track of the ceilings, i.e. the maximal z-coordinate at each (x, y) point in the well, to know where each block will land. Both parts of the puzzle can then be solved by computing the set of blocks that each block is supported by.

### Day 23: A Long Walk

The one where you find a _maximal_ path through a maze.

It is straightforward to locate all the junctions in the map and then compute the distances between neighbouring junctions. This is essentially a weighted graph (directed in the case of the first puzzle, because of the slopes) so the puzzle boils down to finding a maximum-weight path from the entry to the exit point that doesn't contain cycles. I used a simple depth-first search for that.

### Day 24: Never Tell Me The Odds

The one with the intersecting hailstone paths.

The fact that the rock path intersects with the hailstone paths implies a relation between them that can be expressed using vector cross products (see more detailed notes in the code). There are 6 unknowns (3 for the coordinates of the rock axis intercept and 3 for the slopes of the rock path) and all it takes is _three_ of the hailstones in order to come up with a system of 6 linear equations and solve for the unknowns.

### Day 25: Snowverload

The one where you partition a graph with three cuts.

I used a simple breadth-first search to compute the shortest paths from a random node to all other nodes from it, the idea being that a large proportion of these paths should contain the three "constrained" edges that hold the two sections of the graph together. I repeated the process for a few random nodes and counted how many times each edge appeared in those paths. The edges with the three highest counts should be the edges that need to be removed.

After the removal, I repeated the same process (computing the shortest path from a random node to all reachable nodes) once more: if the path has been bisected then only a subset of the nodes are reachable and we are able to count them.

## Next year

Build a library to handle common use cases, such as parsing 2D input files or navigating a 2D environment.

