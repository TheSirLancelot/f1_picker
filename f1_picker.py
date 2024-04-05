import itertools
from urllib.request import urlopen
import json
import pandas as pd
from Entry import Entry

NUMBER_OF_DRIVERS = 5
NUMBER_OF_CONSTRUCTORS = 2
RACE_WEEK = 4

# for each race week, add any new entries and set their points/costs
entries = []
names = []
for i in range(1, RACE_WEEK + 1):
    url = f"https://fantasy.formula1.com/feeds/drivers/{i}_en.json"
    response = urlopen(url)
    data_json = json.loads(response.read())
    data_json = data_json["Data"]["Value"]

    for player in data_json:
        if player["FUllName"] not in names:
            entry = Entry(
                player["FUllName"],  # full name
                player["PositionName"],  # driver or constructor
            )
            names.append(player["FUllName"])
            entries.append(entry)
        for e in entries:
            if e.get_name() == player["FUllName"]:
                e.add_cost(float(player["Value"]))
                if player["RacePoints"]:
                    e.add_points(float(player["GamedayPoints"]))
                    e.add_average()
                if player["IsActive"] == "0":
                    e.set_isActive(False)
                else:
                    e.set_isActive(True)

# calc each player's exponentially weighted value
for e in entries:
    e.calculate_weighted_values()

# grab list of active drivers and constructors
drivers = []
constructors = []
for e in entries:
    if e.get_entry_type() == "DRIVER" and e.isActive is True:
        drivers.append(e)
    else:
        constructors.append(e)

# combos of 5 diff drivers
driver_combo = list(
    itertools.combinations(drivers, NUMBER_OF_DRIVERS)
)  # Θ(k * (n choose k))

# combos of 2 diff constructors
constructors_combo = list(
    itertools.combinations(constructors, NUMBER_OF_CONSTRUCTORS)
)  # Θ(k * (n choose k))

# cartesian product of both combos
cartesian_product = list(itertools.product(driver_combo, constructors_combo))  # O(m*n)

# loop and find total cost and weighted values
options = []
for team in cartesian_product:  # Θ(m*n) again?
    combined = team[0] + team[1]
    total_cost = 0.0
    for i in range(NUMBER_OF_DRIVERS + NUMBER_OF_CONSTRUCTORS):
        total_cost += combined[i].get_cost()
    if 100 >= total_cost >= 85:
        weight = 0.0
        for entry in combined:
            weight += entry.get_weighted_value()
        options.append((weight, total_cost, combined))

# sort by weighted value
sorted_options = sorted(options, key=lambda x: -x[0])  # O(n log n)

# print(sorted_options[0])
print(
    f"Weighted Value: {sorted_options[0][0]:.2f}\nRemaining Budget: {100 - sorted_options[0][1]:.1f}\nTeam: "
)
winning_team = sorted_options[0][2]

# sort team by type and name
winning_team = sorted(winning_team, key=lambda x: (x.get_entry_type(), x.get_name()))

# create table for pandas
table = []
for e in winning_team:
    table.append(
        [
            e.get_name(),
            e.get_cost(),
            e.get_average_cost(),
            e.get_points(),
            e.get_weighted_value(),
        ]
    )

df = pd.DataFrame(table, columns=["Name", "Cost", "Avg Cost", "Points", "Weight"])
print(df.round(2))
