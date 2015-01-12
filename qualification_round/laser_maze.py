# -*- coding: utf-8 -*-
"""
Standard mazes lose their mystery as one grows older. But throw in some lasers,
and suddenly you've got yourself a recipe for cross-generational appeal. The
object in any maze is to find your way from your starting point to some goal.
In a Laser Maze you must additionally contend with laser turrets.

A laser turret is a stationary pillar that both blocks your movement and fires
lasers from one side. Every time you take a step (either up, down, left, or
right), every laser turret in the maze then rotates 90 degrees clockwise, and
then shoots a momentary laser blast in the direction that it is facing.
Needless to say, if you find yourself in the path of one of these lasers, you
won't be around long enough to find a way out. A wall is a stationary pillar
that blocks your movement, but does not fire lasers.

Lasers are powerful, but they do not pass through walls or laser turrets. The
laser turrets respond to your movements, so you can't stand still and wait for
the turrets to turn. If you reach the goal, but are immediately shot by a
laser, your efforts will have been in vain, so make sure you reach the goal
safely.

Input

Input begins with an integer T, the number of mazes you'll explore. For each
maze, there is first a line containing two integers, M and N, the height and
width of the maze, respectively. The next M lines contain N characters each,
describing the maze:

. (empty space)
# (wall)
S (starting position)
G (goal)
< > ^ v (laser turrets)

The four symbols for laser turrets signify turrets that are initially
pointing left, right, up, or down respectively before you take your first step.

Output

For the ith maze, print a line containing "Case #i: " followed by the smallest
number of steps necessary to get to the exit without being hit by a laser, or
the string "impossible'' if there is no way to reach the goal safely.

Constraints
1 ≤ T ≤ 100
1 ≤ M, N ≤ 100
Each maze will contain exactly one 'S' and exactly one 'G'.

5
2 5
##^##
S...G
2 5
##v##
S...G
1 5
S..G<
1 6
S...G<
5 5
S....
.....
.>v..
.^<..
....G

Case #1: 6
Case #2: 4
Case #3: 3
Case #4: impossible
Case #5: 8
"""


def print_case(case, cost):
    print "Case #%d: %s" % (case,
                            str(cost) if cost is not None else 'impossible')


class Node:
    def __init__(self, row, column, maze_char):
        self.row = row
        self.column = column
        self.maze_char = maze_char
        self.neighbors = []
        self.found_states = {}

    def here_before(self, laser_state, cost):
        # We don't want to come here again with the same state but more cost
        current_cost = self.found_states.get(tuple(laser_state))
        if current_cost and current_cost <= cost:
            return True
        return False


class Graph:
    laser_chars = '^>v<'

    def __init__(self, m, n, lines):
        self.maze = []
        self.m = m
        self.n = n
        self.start = self.goal = self.current = self.cost = None
        # import ipdb; ipdb.set_trace()
        for row, line in enumerate(lines):
            maze_row = []
            for column, maze_char in enumerate(line):
                if maze_char == 'S':
                    self.start = (row, column)
                elif maze_char == 'G':
                    self.goal = (row, column)
                # Start and Goal are empty spaces as well.
                if maze_char in 'SG':
                    maze_char = '.'
                # maze_char can be any one of #.^>v<
                maze_row.append(Node(row, column, maze_char))
            self.maze.append(maze_row)
        # Maze is almost done, let's construct the arcs
        for r_index, row in enumerate(self.maze):
            for c_index, node in enumerate(row):
                for step in (-1, 1):
                    next_r = r_index + step
                    if next_r >= 0 and next_r < m:
                        next_node = self.maze[next_r][c_index]
                        if next_node.maze_char == '.':
                            node.neighbors.append(next_node)
                    next_c = c_index + step
                    if next_c >= 0 and next_c < n:
                        next_node = self.maze[r_index][next_c]
                        if next_node.maze_char == '.':
                            node.neighbors.append(next_node)

    def advance_lasers(self, laser_state):
        clockwise = '^>v<'
        new_state = []
        for state in laser_state:
            new_state.append(
                clockwise[(clockwise.index(state) + 1) % len(clockwise)]
            )
        return new_state

    def do_we_die(self, cur_node, laser_state):
        # Check all lasers and see if they kill us at cur_node
        laser_index = 0
        for i in xrange(self.m):
            for j in xrange(self.n):
                maze_char = self.maze[i][j].maze_char
                if maze_char not in self.laser_chars:
                    continue
                # Current state of the maze char
                cur_maze_char = laser_state[laser_index]
                laser_index += 1
                if cur_maze_char in '>v':
                    step = 1
                    if cur_maze_char == '>':
                        stop = self.n
                    else:
                        stop = self.m
                else:
                    step = stop = -1

                if cur_maze_char in '><':
                    for col_index in xrange(j + step, stop, step):
                        check_node = self.maze[i][col_index]
                        # If another laser or wall, it stops working
                        if check_node.maze_char != '.':
                            break
                        if cur_node.row == i and cur_node.column == col_index:
                            return True
                else:
                    for row_index in xrange(i + step, stop, step):
                        check_node = self.maze[row_index][j]
                        if check_node.maze_char != '.':
                            break
                        if cur_node.row == row_index and cur_node.column == j:
                            return True
        return False

    def dfs(self, cur_node, cost, laser_state):
        # Are we there yet? :)
        if (cur_node.row, cur_node.column) == self.goal:
            if not self.cost or cost < self.cost:
                self.cost = cost
            return
        # We record here laser_state and cost so that we can check later
        # and not get in a loop.
        cur_node.found_states[tuple(laser_state)] = cost
        # Assume we are moving to a new place
        cost += 1
        laser_state = self.advance_lasers(laser_state)
        for neighbor in cur_node.neighbors:
            # Check if there's a loop here.
            if neighbor.here_before(laser_state, cost):
                continue
            # Check if we die here.
            if self.do_we_die(neighbor, laser_state):
                continue
            self.dfs(neighbor, cost, laser_state)

    def solve(self):
        start_node = self.maze[self.start[0]][self.start[1]]
        laser_state = []
        for i in xrange(self.m):
            for j in xrange(self.n):
                maze_char = self.maze[i][j].maze_char
                if maze_char in self.laser_chars:
                    laser_state.append(maze_char)
        self.dfs(start_node, 0, laser_state)

    def print_maze(self):
        for row in self.maze:
            print "".join(map(lambda n: n.maze_char, row))
        print "S is at %d, %d" % self.start
        print "G is at %d, %d" % self.goal


if __name__ == '__main__':
    input_file = open('laser_maze.txt', 'r')
    number_of_cases = int(input_file.readline())
    for case in xrange(1, number_of_cases + 1):
        m, n = map(lambda x: int(x), input_file.readline().split())
        lines = []
        for _ in range(m):
            lines.append(input_file.readline().strip())
        graph = Graph(m, n, lines)
        graph.solve()
        print_case(case, graph.cost)

    input_file.close()
