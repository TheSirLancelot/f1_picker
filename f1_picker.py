import itertools
from urllib.request import urlopen
import json

NUMBER_OF_DRIVERS = 5
NUMBER_OF_CONSTRUCTORS = 2
RACE_WEEK = 3


class Entry:

    def __init__(self, name, entry_type, cost, points) -> None:
        self.name = name
        self.entry_type = entry_type
        self.cost = cost
        self.points = points

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_entry_type(self):
        return self.entry_type

    def set_entry_type(self, value):
        self.entry_type = value

    def get_cost(self):
        return self.cost

    def set_cost(self, value):
        self.cost = value

    def get_points(self):
        return self.points

    def set_points(self, value):
        self.points = value

    def __str__(self) -> str:
        return f"Name: {self.name}, Cost: {self.cost}, Points: {self.points:.2f}%"


url = f"https://fantasy.formula1.com/feeds/drivers/{RACE_WEEK}_en.json"
response = urlopen(url)
data_json = json.loads(response.read())
data_json = data_json["Data"]["Value"]

entries = []
for line in data_json:
    if line["IsActive"] == "1":
        entries.append(
            Entry(
                line["FUllName"],  # full name
                line["PositionName"],  # driver or constructor
                float(line["Value"]),  # cost
                float(line["OverallPpints"]),  # points
            )
        )

total_driver_points = 0.0
total_constructor_points = 0.0
for e in entries:
    if e.get_entry_type() == "DRIVER":
        total_driver_points += e.get_points()
    else:
        total_constructor_points += e.get_points()

for e in entries:
    if e.get_entry_type() == "DRIVER":
        e.set_points((e.get_points() / total_driver_points) * 100.0)
    else:
        e.set_points((e.get_points() / total_constructor_points) * 100.0)

drivers = []
constructors = []
for e in entries:
    if e.get_entry_type() == "DRIVER":
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
            weight += entry.get_points()
        options.append((weight, total_cost, combined))

# sort by weighted value
sorted_options = sorted(options, key=lambda x: -x[0])  # O(n log n)

# print(sorted_options[0])
print(
    f"Weighted Value: {sorted_options[0][0]:.2f}\nRemaining Budget: {100 - sorted_options[0][1]:.1f}\nTeam: "
)
for e in sorted_options[0][2]:
    print(f"\t{e}")
