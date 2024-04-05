class Entry:
    beta = 0.9

    def __init__(self, name, entry_type) -> None:
        self.name = name
        self.entry_type = entry_type
        self.costs = []
        self.points = []
        self.averages = []
        self.weightedValues = []
        self.isActive = True

    def get_name(self):
        return self.name

    def set_name(self, value):
        self.name = value

    def get_entry_type(self):
        return self.entry_type

    def set_entry_type(self, value):
        self.entry_type = value

    def get_cost(self):
        return self.costs[-1]

    def add_cost(self, value):
        self.costs.append(value)

    def get_points(self):
        return sum(self.points)

    def add_points(self, value):
        self.points.append(value)

    def get_isActive(self):
        return self.isActive

    def set_isActive(self, value):
        self.isActive = value

    def add_average(self):
        self.averages.append(sum(self.points) / len(self.points))

    def get_average_cost(self):
        return sum(self.costs) / len(self.costs)

    def equate_vt(self, data, index):
        index = index - 1
        return (self.beta * self.averages[index]) + ((1 - self.beta) * data)

    def calculate_weighted_values(self):

        for i, average in enumerate(self.averages):
            if i == 0:
                vt = (self.beta * 0) + ((1 - self.beta) * average)
                self.weightedValues.append(vt)
            else:
                vt = self.equate_vt(average, i)
                self.weightedValues.append(vt)

    def get_weighted_value(self):
        return self.weightedValues[-1]

    def __str__(self) -> str:
        return f"Name: {self.name}, Current Cost: {self.get_cost()}, Average Cost: {self.get_average_cost():.2f}, Fantasy Points: {self.get_points()}, Current Weighted Value: {self.get_weighted_value():.2f}"
