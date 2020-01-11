#%%
import sys
import numpy as np

if len(sys.argv) == 1:
    input_file = "../../data/final_round_2014/sample_input.txt"
    submission_file = "../../data/final_round_2014/sample_output.txt"
elif len(sys.argv) == 3:
    input_file = sys.argv[1]
    submission_file = sys.argv[2]
else:
    print("provide arguments")
    sys.exit(0)

with open(input_file) as f:
    line = f.readline().split()
    num_junctions = int(line[0])
    num_street = int(line[1])
    T = float(line[2])
    num_car = int(line[3])
    S = int(line[4])

    JUNCTIONS = []
    for _ in range(num_junctions):
        JUNCTIONS.append([float(i) for i in f.readline().split()])

    STREETS = [[[] for _ in range(num_junctions)] for _ in range(num_junctions)]
    for _ in range(num_street):
        specs = [int(i) for i in f.readline().split()]
        STREETS[specs[0]][specs[1]] = [specs[3], specs[4]]
        if specs[2] == 2:
            STREETS[specs[1]][specs[0]] = [specs[3], specs[4]]
    

#%%
with open(submission_file) as ff:
    lines = ff.readlines()
    lines = list(map(int, lines))
    C = int(lines[0])

    # the number of cars in the fleet C has to match 
    # the number of cars indicated in the problem input
    assert C == num_car

    pointer = 1
    for i in range(C):
        Vi = int(lines[pointer])
        J = lines[pointer + 1 : pointer + Vi + 1]
        # the first junction on each itinerary has to be 
        # the starting junction S indicated in the input file
        assert J[0] == S   
        total_time = 0
        score = 0
        is_visited = np.zeros((num_junctions, num_junctions))
        if len(J) != 1:
            for first, second in zip(J, J[1:]):

                # for each consecutive pair of junctions on the itinerary, 
                # a street connecting these junctions has to exist in the input file, 
                # if the street is one­directional, it has to be traversed in the correct direction
                assert len(STREETS[first][second]) > 0
                if is_visited[first][second] == 0:
                    score += STREETS[first][second][1]
                is_visited[first][second] = 1
                is_visited[second][first] = 1

                total_time += STREETS[first][second][0]

        pointer = pointer + Vi + 1

    # total time for each itinerary has to be lower or equal to T
    assert total_time <= T

    # be sure there is no more line
    assert pointer == len(lines)

print("submission file is valid and the score is %d" % score)
