import csv

class Traveling:

  def __init__(self):
    self.map = {}
    self.heuristics = {}

  # go through csv and return some useful maps
  def parse(self):
    with open('MapInfo.csv', 'r') as file:
      reader = list(csv.reader(file))

      header_row = reader[0]
      cities_map = {}
      heuristics = {}

      # go through each city in the file 
      for i in range(1, len(reader)):
        row = reader[i]
        city = row[0]

        # map city -> heuristic for later use 
        heuristics[city] = int(row[1])

        # map city -> list of neighboring cities 
        cities_map[city] = []
        for j in range(2, len(row)):
          if row[j] != '':
            cities_map[city].append((header_row[j], int(row[j])))

      # store these maps as instance variables 
      self.cities_map = cities_map
      self.heuristics = heuristics
    
  # allow the user to input start and end states
  def init_states(self):
    self.parse()
    
    start = input("Where would you like to start? ")
    while start not in self.cities_map: 
      start = input("Please enter a valid city: ")

    goal = input("Where would you like to go? ")
    while start not in self.cities_map: 
      goal = input("Please enter a valid city: ")
    print("")

    return [start, goal]

  # return the list of neihbors to the current city
  def get_actions(self, curr_state): 
    return self.cities_map[curr_state]
  
  # lookup heuristic of the current city
  def get_heuristic(self, curr_state): 
    return self.heuristics[curr_state]
  
  def test(self, curr_state, goal_state):
    return curr_state == goal_state
  
  def pretty_print(self, curr_state):
    print(curr_state)


    


  

  