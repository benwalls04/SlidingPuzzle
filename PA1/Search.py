import heapq
from Traveling import Traveling
from SlidingPuzzle import SlidingPuzzle

class Search: 
  
  class Node: 

    def __init__(self, parent, state, path_cost, heuristic):
        self.parent = parent
        self.state = state
        self.path_cost = path_cost
        self.heuristic = heuristic
        ## avoid populating actions until they are needed
        self.actions = None

    def __lt__(self, other):
      ## consistent ordering for when pq encounters a tie 
      return self.state < other.state
    
    def get_path(self): 
      curr = self
      path = []

      ## backtrack with the parents of each node in the class
      while curr.parent is not None:
        path.append(curr.state)
        curr = curr.parent

      ## add root node
      path.append(curr.state)

      return path[::-1]
    
  def __init__(self, start, goal):
    self.goal = goal
    self.start = start
  
  def update_cost(self, pq, node, new_cost):
    for i, (cost, curr_node) in enumerate(pq):
      if curr_node.state == node.state:
        pq[i] = (new_cost, node)
        heapq.heapify(pq)  
        break

  def search(self, problem, add_heuristic): 
    ## represent explored "as a map from state -> best-cost
    ## allows for quick lookup when checking for a more optimal path to the same node
    explored = {}

    curr = self.Node(None, self.start, 0, problem.my_heuristic(self.start))
    frontier = [(0, curr)]

    while True: 
      (cost, curr) = heapq.heappop(frontier)

      ## before expanding, check if we are at the goal state
      if problem.test(curr.state, self.goal):
        return [curr.get_path(), len(explored)]
      
      explored[curr.state] = curr.path_cost

      ## iterate all possible next "child" states from the current stae 
      curr.actions = problem.get_actions(curr.state)
      for action in curr.actions:
        (child_state, action_cost) = action

        child_cost = curr.path_cost + action_cost

        ## ensure child state hasn't been explored
        if child_state not in explored: 
          explored[child_state] = child_cost

          ## UCS can be represented as A* where all heuristics = 0 
          child_heuristic = 0
          if add_heuristic:
            child_heuristic = problem.get_heuristic(child_state)

          ## add child node to the pq with path cost + action cost + heurisitc 
          child_node = self.Node(curr, child_state, child_cost, child_heuristic)
          heapq.heappush(frontier, (child_cost + child_heuristic, child_node))

        ## if child has been explored, check if this path is better, and replace 
        elif child_cost < explored[child_state]: 
          self.update_cost(frontier, child_node, child_cost)

      ## leave the loop when there are no actions to make
      if len(frontier) == 0: 
        break

    ## return some dummy values to indicate a failure
    return [-1, -1]
  
if __name__=="__main__":
  valid_input = {"1", "2", "3"}
  print("Welcome to the searcher")
  while True:
    print("For the Traveling Problem type 1")
    print("For the Sliding Puzzle type 2")
    user_input = input("To quit, type 3\n")
    while user_input not in valid_input:
      user_input = input("Please Enter 1, 2, or 3")

    if user_input == "3":
      break

    problem = Traveling()
    if (user_input == "2"):
      problem = SlidingPuzzle()

    [start, goal] = problem.init_states()
    searcher = Search(start, goal)

    [path, n_expansions] = searcher.search(problem, False)
    print(f"\nStarting state: ")
    problem.pretty_print(start)

    if path == -1: 
      print(f"Unsolvable.. Try Again\n")
      continue
    
    print(f"\nWith UCS, you reached the goal after {n_expansions} expansions")

    [path, n_expansions] = searcher.search(problem, True)
    print(f"With A*, you reached the goal after {n_expansions} expansions\n")
    print(f"You took the following path of length {len(path)}:")
    for item in path:
      problem.pretty_print(item)
    print("-------------")

    user_input = None