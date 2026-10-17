import random

ratings = {
    "Argentina" : 1877,
    "Spain": 1874,
    "France" : 1828,
    "Portugal" : 1767,
    "Brazil" : 1765,
    "Morocco" : 1755,
    "Netherlands" : 1753,
    "Belgium" : 1742,
    "Germany" : 1735,
    "Croatia" : 1714,
    "Italy" : 1704,
    

}

def win_probablility(R_a, R_b):
    win = 1 / (1 + 10 ** ((R_b - R_a) / 400))
    return win


#simulating a match
def simulate_A_match(team_a, team_b):
    Rating_a = ratings[team_a]
    Rating_b = ratings[team_b]

    probability_A = win_probablility(Rating_a, Rating_b)

    if random.random() < probability_A:
        return team_a
    else:
        return team_b


#updating settings
def update_ratings(team_a, team_b, winner, k = 30):
    ra = ratings[team_a]
    rb = ratings[team_b]

    #defining ea and eb
    ea = win_probablility(ra, rb)
    eb = 1 - ea

    #sa and sb
    sa = 1 if winner == team_a else 0 
    sb = 1 - sa

    #updating the number of ratings as the no fo matches progresses
    ratings[team_a] = ra + k * (sa - ea)
    ratings[team_b] = rb  + k * (sb - eb)


#running the simulation:
def run_simulation(num_of_matches = 1000000):
    #get team list
    team_list = list(ratings.keys())

    #sampling any two random teams for a match
    for _ in range(num_of_matches):
        team_A , team_B = random.sample(team_list, 2)

        winner = simulate_A_match(team_A, team_B)
        update_ratings(team_A, team_B, winner)


#final calling the damn function
run_simulation(1000000)
print("FINAL  RATINGS: ")
for Team, ratings in ratings.items():
    print(f"{Team} : {round(ratings, 2)}")