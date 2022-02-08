import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv


# Input data
# It takes player list and matches information
ipl_match_dict = [
    {"match_between": "MIvsCSK", "series_id": 8048, "match_id": 1216492},
    {"match_between": "DCvsKXIP", "series_id": 8048, "match_id": 1216493},
    {"match_between": "RCBvsSRH", "series_id": 8048, "match_id": 1216534},
    {"match_between": "RRvsCSK", "series_id": 8048, "match_id": 1216496},
    {"match_between": "MIvsKKR", "series_id": 8048, "match_id": 1216508},
    {"match_between": "KXIPvsRCB", "series_id": 8048, "match_id": 1216510},
    {"match_between": "DCvsCSK", "series_id": 8048, "match_id": 1216539},
    {"match_between": "SRHvsKKR", "series_id": 8048, "match_id": 1216545},
    {"match_between": "KXIPvsRR", "series_id": 8048, "match_id": 1216527},
    {"match_between": "RCBvsMI", "series_id": 8048, "match_id": 1216547},
]


player_list = [
    { 'name': 'Rohit Sharma', 'player_type': 'Batsman', 'base_point': 30},
   # { 'name': 'Ravindra Jadeja', 'player_type': 'Batsman', 'base_point': 15},
    
    { 'name': 'David Warner', 'player_type': 'Batsman', 'base_point': 25},
    { 'name': 'Prithvi Shaw', 'player_type': 'Batsman', 'base_point': 20},
    { 'name': 'Dinesh Karthik', 'player_type': 'Batsman', 'base_point': 22},
   # { 'name': 'Kieron Pollard', 'player_type': 'Batsman', 'base_point': 25}, 

]


# Define game rules
# This function defines the game rules and gives scores to each parameter
def define_game_rules():
    admin_name = input("Enter admin name? ")
    print("Welcome to Own Fantasy League {}".format(admin_name) ,"\n")
    print("-----------------------------")
    print("Let's first define the batting rules ","\n")
    score_single = input("How much score per single?: ")
    print("\n")
    score_4s = input("How much score per 4?: ")
    print("\n")
    score_6s = input("How much score per 6?: ")
    print("\n")
    score_50 = input("How much score per half century?: ")
    print("\n")
    score_100 = input("How much score per century?: ")
    print("\n")
    print("Ok great! Batting rules defined","\n")
    #score_dot = input("How much score per dot ball?: ")
    #print("\n")
    #score_wickets = input("How much score per wicket?: ")
    #print("\n")
    #score_maiden = input("How much score per maiden over?: ")
    #print("\n")
    corpus_per_bidder = input("What is the corpus per bidder? ")
    print("\n")
    print("Great {}".format(admin_name))
    print("\n")
    game_rules_dict = {
        'score_4s': float(score_4s),
        'score_6s': float(score_6s),
        'score_single': float(score_single),
        'score_50': float(score_50),
        'score_100': float(score_100),
        #'score_dot': float(score_dot),
        #'score_maiden': float(score_maiden),
        #'score_wickets': float(score_wickets),
        'corpus_per_bidder': float(corpus_per_bidder)
    }
    print(game_rules_dict,"\n")
    confirm = input('Just to confirm, the above data is correct? Press Y for yes and N for no. ') 
    print("\n")
    if confirm == 'Y':
        return game_rules_dict
    elif confirm == 'N':
        print("Oh boy! Let's do it again","\n")
        return define_game_rules()


# Bidders
# This function takes bidders profile as input and generates
# a list of dictionaries which is used as the input for bidding module
def insert_bidders_profile(corpus_per_bidder):
    bidder_list = []
    no_bidder = int(input('How many bidders?: '))
    print("\n")
    for i in range(no_bidder):
        bidder_name = input('Enter bidder{} name: '.format(i+1)) 
        bidder_list.append({
            'bidder_id': i,
            'bidder_name': bidder_name,
            'corpus_per_bidder': corpus_per_bidder
    
        })
        print("\n")
    return bidder_list


# This function checks for ties
def _find_max_bidder(bid_check_list):
    max_var = 0
    count = 0
    bid_when_equal = 0
    for bids in bid_check_list:
        if bids['bid_amount'] > max_var:
            max_var = bids['bid_amount']
            id = int(bids['bidder_id'])
            name = bids['bidder_name']
        elif bids['bid_amount'] == max_var:
            bid_when_equal = bids['bid_amount']
            count += 1
    if max_var > bid_when_equal:
        return [id, max_var, True, name]
    else:
        return ['', '', False, '']


# Bidding module
# This function takes bidder list and player profile and simulates a virtual bid
# Bid is allotted to the max bidder and in case of tie, bid takes place again
def start_bidding(bidder_list, player):
    bid_check_list = []
    print("Bid for player - {}. He is a {}. Base point is {}".format(player['name'], player['player_type'], player['base_point']))
    print("<--------------------------------------------------------------------------------------------->\n")
    for bidder in bidder_list:
        bid_new = float(input('Bidder {}. Please put your bid amount and it should be greater than or equal to {} '.format(bidder['bidder_name'], player['base_point'])))
        print("\n")
        while bid_new < player['base_point']:
            bid_new = float(input('Bidder {}, your bid amount should be greater than base point or equal to- {} '.format(bidder['bidder_name'], player['base_point'])))
        bid_check_list.append({
            'bidder_id': bidder['bidder_id'],
            'bidder_name': bidder['bidder_name'],
            'bid_amount': bid_new
        })
        
    print("<--------------------------------------------------------------------------------------------->\n")    
    check = _find_max_bidder(bid_check_list)
    if not check[2]:
        start_bidding(bidder_list, player)
    else:
        for bidders in bidder_list:
            if check[0] == int(bidders['bidder_id']):
                bidders['corpus_per_bidder'] = bidders['corpus_per_bidder'] - check[1]
    output_dict = {
        'player_name': player['name'],
        'player_type': player['player_type'],
        'player_owner': check[0],
        'bidder_name': check[3]
    }
    return output_dict


# extraction of batting data using bs4
def extract_batting_data(series_id, match_id):
    URL = (
        "https://www.espncricinfo.com/series/"
        + str(series_id)
        + "/scorecard/"
        + str(match_id)
    )
    page = requests.get(URL)
    bs = BeautifulSoup(page.content, "lxml")
    table_body = bs.find_all("tbody")
    batsmen_df = pd.DataFrame(
        columns=["player_name", "Desc", "Runs", "Balls", "4s", "6s", "SR", "Team"]
    )
    for i, table in enumerate(table_body[0:4:2]):
        rows = table.find_all("tr")
        for row in rows[::2]:
            cols = row.find_all("td")
            cols = [x.text.strip() for x in cols]
            if cols[0] == "Extras":
                continue
            if len(cols) > 7:
                batsmen_df = batsmen_df.append(
                    pd.Series(
                        [
                            re.sub(r"\W+", " ", cols[0].split("(c)")[0]).strip(),
                            cols[1],
                            cols[2],
                            cols[3],
                            cols[5],
                            cols[6],
                            cols[7],
                            i + 1,
                        ],
                        index=batsmen_df.columns,
                    ),
                    ignore_index=True,
                )
            else:
                batsmen_df = batsmen_df.append(
                    pd.Series(
                        [
                            re.sub(r"\W+", " ", cols[0].split("(c)")[0]).strip(),
                            cols[1],
                            0,
                            0,
                            0,
                            0,
                            0,
                            i + 1,
                        ],
                        index=batsmen_df.columns,
                    ),
                    ignore_index=True,
                )
    for i in range(2):
        dnb_row = bs.find_all("tfoot")[i].find_all("div")
        for c in dnb_row:
            dnb_cols = c.find_all("span")
            dnb = [x.text.strip().split("(c)")[0] for x in dnb_cols]
            dnb = filter(
                lambda item: item, [re.sub(r"\W+", " ", x).strip() for x in dnb]
            )
            for dnb_batsman in dnb:
                batsmen_df = batsmen_df.append(
                    pd.Series(
                        [dnb_batsman, "DNB", 0, 0, 0, 0, 0, i + 1],
                        index=batsmen_df.columns,
                    ),
                    ignore_index=True,
                )
    return batsmen_df


# extraction of bowling data using bs4
# def extract_bowling_data(series_id, match_id):
#     URL = (
#         "https://www.espncricinfo.com/series/"
#         + str(series_id)
#         + "/scorecard/"
#         + str(match_id)
#     )
#     page = requests.get(URL)
#     bs = BeautifulSoup(page.content, "lxml")
#     table_body = bs.find_all("tbody")
#     bowler_df = pd.DataFrame(
#         columns=[
#             "player_name",
#             "Overs",
#             "Maidens",
#             "Runs",
#             "Wickets",
#             "Econ",
#             "Dots",
#             "4s",
#             "6s",
#             "Wd",
#             "Nb",
#             "Team",
#         ]
#     )
#     for i, table in enumerate(table_body[1:4:2]):
#         rows = table.find_all("tr")
#         for row in rows:
#             cols = row.find_all("td")
#             cols = [x.text.strip() for x in cols]
#             bowler_df = bowler_df.append(
#                 pd.Series(
#                     [
#                         cols[0],
#                         cols[1],
#                         cols[2],
#                         cols[3],
#                         cols[4],
#                         cols[5],
#                         cols[6],
#                         cols[7],
#                         cols[8],
#                         cols[9],
#                         cols[10],
#                         (i == 0) + 1,
#                     ],
#                     index=bowler_df.columns,
#                 ),
#                 ignore_index=True,
#             )
#     return bowler_df


# Run this function to get names of all players
def list_all_players(match_dict):
    name_all = []
    for match in match_dict:
        series_id = match["series_id"]
        match_id = match["match_id"]
        df = extract_batting_data(series_id, match_id)
        names = df["Name"].values.tolist()
        for name in names:
            name_all.append(name)
    return name_all


def calculate_owner_score(ipl_match_dict, game_rules_dict):
    owner_raw_team = pd.read_csv("test.csv")
    owner_summary = []
    for match in ipl_match_dict:
        sum_run = 0
        h_century = 0
        century = 0
        series_id = match["series_id"]
        match_id = match["match_id"]
        match_between = match["match_between"]
        batting_data = extract_batting_data(series_id, match_id)
        merged_df = pd.merge(owner_raw_team, batting_data, on="player_name")
        data = merged_df["player_owner"]
        if len(data) == 0:
            pass
        else:
            owner_id = merged_df["player_owner"][0]
            owner_name = merged_df["bidder_name"][0]
            runs = merged_df["Runs"].values.tolist()
            fours = merged_df["4s"].values.tolist()
            fours = [int(i) for i in fours]
            sixes = merged_df["6s"].values.tolist()
            sixes = [int(i) for i in sixes]
            for run in runs:
                run = int(run)
                sum_run = sum_run + run
                if run >= 50 and run < 100:
                    h_century = h_century + 1
                elif run >= 100:
                    century = century + 1
            output_dict = {
                "owner_id": owner_id,
                "owner_name": owner_name,
                "match": match_between,
                "runs": sum_run,
                "h_century": h_century,
                "century": century,
                "fours": sum(fours),
                "sixes": sum(sixes),
                "pts_sixes":sum(sixes)*game_rules_dict['score_6s'],
                "pts_singles":(sum_run-((4*sum(fours))+(6*sum(sixes))))*game_rules_dict['score_single'],
                "pts_halfcen":h_century*game_rules_dict['score_50'],
                "pts_cen":century*game_rules_dict['score_100'],
                "pts_four":sum(fours)*game_rules_dict['score_4s']
            }
            owner_summary.append(output_dict)
    

    keys = owner_summary[0].keys()
    with open('Final_output.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(owner_summary)
    return owner_summary


def print_total_score(owner_score):
    for data in owner_score:
        total_score = data['pts_singles'] + data['pts_halfcen'] + data['pts_four'] + data['pts_sixes'] + data['pts_cen']
        print('{} your score is {}'.format(data['owner_name'], total_score))
    return None


gamerules = define_game_rules()
bidder_list = insert_bidders_profile(gamerules['corpus_per_bidder'])
bidder_dict_list = []
field_names = ['player_name', 'player_owner', 'player_type', 'bidder_name']
for player in player_list:
    bidder_dict = start_bidding(bidder_list, player)
    bidder_dict_list.append(bidder_dict)
print(bidder_dict_list)
with open('test.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(bidder_dict_list)
p_data = calculate_owner_score(ipl_match_dict, gamerules)
print_total_score(p_data)




