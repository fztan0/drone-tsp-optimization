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
def initialize_distance_matrix(coordinates: list[tuple[float, float]], n: int) -> list[list[float]]:
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

def print_distance_matrix(distance_matrix: list[list[float]], n: int) -> None:
  for i in range(n):
    for j in range(n):
      print(f"{distance_matrix[i][j]:.7f}", end = " ")
    print()

def compute_route_distance(route: list[int], distance_matrix: list[list[float]], n: int) -> float:
  total_distance = 0.0
  num_edges = n - 1 # we want how many edges, not nodes

  for i in range(num_edges):
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


# MAKE SURE: when outputting every BSF/final, USE NEAREST INTEGER CEILING
def anytime_random(distance_matrix: list[list[float]], n: int) -> tuple[list[int], float, float]:
  global enter_key_flag

  best_route_so_far = generate_random_route(n)
  best_distance_so_far = compute_route_distance(best_route_so_far, distance_matrix, n)

  print("    Shortest Route Discovered So Far")
  print(f"        {math.ceil(best_distance_so_far)}")

  start_time = time.time()

  # spawn a thread to listen for 'Enter' key press and change while loot flag
  listener_thread = threading.Thread(target = wait_enter_key)
  listener_thread.start()

  while not enter_key_flag:
    new_route = generate_random_route(n)
    new_distance = compute_route_distance(new_route, distance_matrix, n)

    if new_distance < best_distance_so_far:
      best_route_so_far = new_route
      best_distance_so_far = new_distance

      print(f"        {math.ceil(best_distance_so_far)}")


  elapsed_time = time.time() - start_time

  return best_route_so_far, best_distance_so_far, elapsed_time





def main() -> None:
  file_name = input("ComputeDronePath\nEnter the name of file: ")

  coordinates = load_coordinate_data(file_name)
  n = len(coordinates)

  print(f"There are {n} nodes, computing route..")

  distance_matrix = initialize_distance_matrix(coordinates, n)

  # start computation calls here or something
  best_route, best_distance, elapsed_time = anytime_random(distance_matrix, n)

  print(f"        {math.ceil(best_distance)}")


  # MAKE SURE: when outputting every BSF/final, USE NEAREST INTEGER CEILING




# main program entry point
if __name__ == "__main__":
  # function runs only when script is executed directly, as opposed to import
  main()