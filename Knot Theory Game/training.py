from knot import Knot, GameResult
from agent import Agent 
from randomPlayer import RandomPlayer
import csv
from itertools import combinations
import json




# pd_code = [[1,4, 2, 5], [3, 8, 4, 9], [5, 10, 6, 1], [9, 6, 10, 7], [7, 2, 8, 3]]
# pd_code = [[1, 4, 2, 5], [3, 10, 4, 11], [5, 14, 6, 1], [7, 12, 8, 13], [11, 8, 12, 9], [13, 6, 14, 7], [9, 2, 10, 3]]
# pd_code = [[1,4,2,5], [9, 12, 10, 13], [3, 11, 4, 10], [11,3,12,2], [5,16,6,1], [7,14,8,15], [13,8,14,9], [15,6,16,7]]

def generate_policy(knot_name, pd_code):
    p1 = Agent("Unknotter")
    p2 = Agent("Knotter")


    st = Knot(p1, p2, pd_code)

    print("training...")
    st.simulation(pd_code, 10000)

    p1.savePolicy(knot_name) 
    p2.savePolicy(knot_name)

def load_players(knot_name):
    knotter = Agent("Knotter", q_init=0)
    knotter.loadPolicy("./Policies/policy_" + knot_name + "_Knotter")
    unknotter = Agent("Unknotter", q_init=0)
    unknotter.loadPolicy("./Policies/policy_" + knot_name + "_Unknotter")
    random_player = RandomPlayer("Random")
    players = [knotter, unknotter, random_player]
    return list(combinations(players, 2))


def trial(p1, p2, pd_code):
    knot = Knot(p1, p2, pd_code)
    result = knot.play()
    with open('Results.csv', mode='a') as Results:
        result_writer = csv.writer(Results)
        result_writer.writerow([p1.name, p2.name, result])


def random_trial(p1,p2, pd_code):
    no_of_random_wins = 0
    random_p1 = False
    if p1.name == "Random":
        random_p1 = True
    for i in range(1000):
        knot = Knot(p1, p2, pd_code)
        result = knot.play()
        if result == "Random":
            no_of_random_wins += 1
    if no_of_random_wins > 1000 - no_of_random_wins:
        winner = "Random"
        proportion_of_wins = no_of_random_wins/1000
    else:
        winner = p2.name if random_p1 else p1.name
        proportion_of_wins = 1- (no_of_random_wins/1000)
    with open('Results.csv', mode='a') as Results:
        result_writer = csv.writer(Results)
        result_writer.writerow([p1.name, p2.name, winner, proportion_of_wins])

def play_knot(knot_name, pd_code):
    generate_policy(knot_name, pd_code)
    combinations = load_players(knot_name)
    with open('Results.csv', mode='a') as Results:
        result_writer = csv.writer(Results)
        result_writer.writerow([knot_name+":"])
    print("Playing all combinations...")
    for combination in combinations:
        player_1 = combination[0]
        player_2 = combination[1]
        if player_1.name == "Random" or player_2.name == "Random":
            random_trial(player_1,player_2, pd_code)
            random_trial(player_2,player_1, pd_code)
        else:
            trial(player_1, player_2, pd_code)
            trial(player_2, player_1, pd_code)

# trefoil = [[1, 4, 2, 5], [3, 6, 4, 1], [5, 2, 6, 3]]
# play_knot("trefoil", trefoil)

with open('knotinfo.csv') as csvfile:
    readCSV = csv.reader(csvfile,  delimiter=',')
    next(readCSV)
    for row in readCSV:
        pd_code_string = row[1].replace(';', ',')
        pd_code = json.loads(pd_code_string)
        print("KNOT:", row[0])
        play_knot(row[0], pd_code)
        print("DONE.")
       




