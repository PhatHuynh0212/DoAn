class TSPBacktracking:
    def __init__(self, locations): 
        self.locations = locations
        self.num_locations = len(locations)
        self.visited = []
        self.path = []
        self.distance = 0

    def solve_tsp(self, start):
        self.visited = [False] * self.num_locations
        self.path = []
        self.distance = 0
        self.visited[start] = True
        self.path.append(start)
        current = start

        for _ in range(self.num_locations - 1):
            next_city = self.find_nearest_location(current)
            self.visited[next_city] = True
            self.path.append(next_city)
            self.distance += self.locations[current][next_city]
            current = next_city
        self.distance += self.locations[current][start]
        self.path.append(start)
        return self.path , self.distance

    def find_nearest_location(self, city):
        nearest_location = None
        min_distance = float('inf')
        for i in range(self.num_locations):
            if not self.visited[i] and self.locations[city][i] < min_distance:
                nearest_location = i
                min_distance = self.locations[city][i]
        return nearest_location