# main.py
# refactor and reimplement using numpy later
import math
import os
import random
import threading
import time

enter_key_flag = False

def load_coordinate_data(file_name: str) -> list[tuple[float, float]]:
  # assuming we are firing from project root
  file_name = os.path.join(os.getcwd(), "data", file_name)

  coordinates = []

  try:
    with open(file_name, 'r') as file:
      for line in file:
        parts = line.strip().split() # split default ANY whitespace

        # how strict are you about file format? is it just number of columns, or even the value standards (not in IEEE 754)
        if len(parts) != 2:
          raise ValueError("Incorrect file format. Expected two column per line.")

        # default ValueError should be descriptive for float conversion failure
        x, y = map(float, parts)
        coordinates.append((x, y))
  except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.\nAborting.")
    exit()
  except ValueError as e:
    print(f"Error: {e}\nAborting.")
    exit()

  if len(coordinates) > 256:
    print("Error: File exceeds 256 node limit.")
    exit()

  return coordinates

# maybe implement loaded vs unloaded data point for integrity check
def print_loaded_coordinates(coordinates: list[tuple[float, float]]) -> None:
  for idx, (x, y) in enumerate(coordinates, start = 1): # start idx 1 for clarity
    print(f"{idx:3d}: ({x:.7f}, {y:.7f})")

# python uses binary64 so just let float rip
def initialize_distance_matrix(coordinates: list[tuple[float, float]]) -> list[list[float]]:
  n = len(coordinates)

  distance_matrix = [[0.0 for _ in range(n)] for _ in range(n)]

  for i in range(n):
    (x1, y1) = coordinates[i] # current point

    for j in range(i + 1, n): # upper triangle only since Euclidean distance is a metric and therefore symmetric HOLY CS171 KNOWLEDGE KICKING IN
      x2, y2 = coordinates[j]

      distance_between_two_points = ((((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5)

      distance_matrix[i][j] = distance_between_two_points

      # might as well fill in the lower triangle too
      # leave this assignment for now, see if we can later optimize by completely avoiding invoking lower triangle access
      distance_matrix[j][i] = distance_between_two_points

  return distance_matrix

def print_distance_matrix(distance_matrix: list[list[float]]) -> None:
  n = len(distance_matrix)

  for i in range(n):
    for j in range(n):
      print(f"{distance_matrix[i][j]:.7f}", end = " ")
    print()

def compute_route_distance(route: list[int], distance_matrix: list[list[float]]) -> float:
  total_distance = 0.0
  n = len(route) - 1 # we want how many edges, not nodes

  for i in range(n):
    from_node = route[i]
    to_node = route[i + 1]

    total_distance += distance_matrix[from_node][to_node]

  return total_distance

# used some online tool to check duplicate values, seems fine
def generate_random_route(n: int) -> list[int]:
  # using random.sample() because it seems safer(?), creates new lsit instead of random.shuffle() in place
  middle = random.sample(range(1, n), n - 1) # for sequence [1, n), pick k = n - 1 (ALL) items without replacement
  return [0] + middle + [0] # "always returning to the starting point (the recharge bay)"

def wait_enter_key() -> None:
  global enter_key_flag
  input() # input() already waits for 'Enter' sooooo
  enter_key_flag = True








def main() -> None:
  file_name = input("ComputeDronePath\nEnter the name of file: ")

  coordinates = load_coordinate_data(file_name)
  n = len(coordinates)

  print(f"There are {n} nodes, computing route..")
  # print_loaded_coordinates(coordinates)

  #distance_matrix = initialize_distance_matrix(coordinates)
  # print_distance_matrix(distance_matrix)

  #random_route = generate_random_route(n)
  #computed_distance = compute_route_distance(random_route, distance_matrix)

  #print(f"Random route distance: {computed_distance:.7f}")

  #print("Random route sequence:", *(node + 1 for node in random_route)) #route starts at 1 not 0

  # start computation calls here or something
  print(f"    Shortest Route Discovered So Far")
  distance_matrix = initialize_distance_matrix(coordinates)
  random_route = generate_random_route(n)
  computed_distance = compute_route_distance(random_route, distance_matrix)
  bestSoFar = math.ceil(computed_distance)
  print(f"        {bestSoFar}")
  enter_key = threading.Thread(target=wait_enter_key)
  enter_key.start()
  while True:
    random_route = generate_random_route(n)
    computed_distance = compute_route_distance(random_route, distance_matrix)
    # MAKE SURE: when outputting every BSF/final, USE NEAREST INTEGER CEILING
    if(math.ceil(bestSoFar) > math.ceil(computed_distance)):
      bestSoFar = math.ceil(computed_distance)
      print(f"        {bestSoFar}") # need to implement threading
    if enter_key_flag == True:
      if bestSoFar > 6000:
        print(f"Warning: Solution is {bestSoFar}, greater than the 6000-meter constraint.")
      saveRoute = random_route
      break
  outputFile = f"{file_name}_SOLUTION_{bestSoFar}.txt"
  #might be different depending on the os. this accounts for this
  remove_newLine = len(os.linesep)
  with open(outputFile, "w") as file:
    for location in saveRoute:
      file.write(f"{location+1}\n")
    #Truncates the file to remove the new line character
    file.truncate(file.tell() - remove_newLine)
  print(f"Route written to disk as {file_name}_SOLUTION_{bestSoFar}.txt")

  




# main program entry point
if __name__ == "__main__":
  # function runs only when script is executed directly, as opposed to import
  main()