# main.py
# refactor and reimplement using numpy later
import math
import os
import random
import threading
import matplotlib.pyplot as plt

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
    print("Error: File exceeds 256 node limit.\nAborting.")
    exit()

  return coordinates

# maybe implement loaded vs unloaded data point for integrity check
def print_loaded_coordinates(coordinates: list[tuple[float, float]]) -> None:
  for idx, (x, y) in enumerate(coordinates, start = 1): # start idx 1 for clarity
    print(f"{idx:3d}: ({x:.7f}, {y:.7f})")

# python uses binary64 so just let float rip
def compute_distance_matrix(coordinates: list[tuple[float, float]], n: int) -> list[list[float]]:
  # initialize n * n matrix with 0.0
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

  # initial best route and distance
  best_route_so_far = generate_random_route(n)
  best_distance_so_far = compute_route_distance(best_route_so_far, distance_matrix, n)

  print("    Shortest Route Discovered So Far")
  print(f"        {math.ceil(best_distance_so_far)}")

  # start_time = time.time()

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

  # elapsed_time = time.time() - start_time

  # neat trick to erase the newline created by input() in wait_enter_key(), ANSI so kinda hacky
  # https://stackoverflow.com/questions/76236463/python-2-print-overwrite
  print( "\033[F\033[2K", end="", flush=True )

  # Ouput side effect
  if best_distance_so_far > 6000:
    print(f"Warning: Solution is {math.ceil(best_distance_so_far)}, greater than the 6000-meter constraint.")

  return best_route_so_far, best_distance_so_far


def save_route_to_file(route: list[int], distance: float, n: int, input_file_name: str) -> None:
  base_name = os.path.splitext(input_file_name)[0] # remove ".txt" extension from input file name
  out_file_name = f"{base_name}_solution_{math.ceil(distance)}.txt"
  out_path = os.path.join(os.getcwd(), "output", out_file_name)

  os.makedirs(os.path.dirname(out_path), exist_ok = True)

  try:
    with open(out_path, 'w') as file:
      for node in route:
        file.write(f"{node + 1}\n") # each subsequent line is a node index

      # remove last newline character to match output format
      file.truncate(file.tell() - len(os.linesep))
  except Exception as e:
    print(f"Error writing to file: {e}\nAborting.")
    exit()


  print(f"Route written to disk as {out_file_name}")

  return


def run_random_anytime() -> None:
  in_file_name = input("Enter the name of file: ")
  coordinates = load_coordinate_data(in_file_name)

  n = len(coordinates)
  print(f"There are {n} nodes, computing route..")

  distance_matrix = compute_distance_matrix(coordinates, n)

  best_route, best_distance = anytime_random(distance_matrix, n)

  save_route_to_file(best_route, best_distance, n, in_file_name)

  file_name = os.path.join(os.getcwd(), "output", f"{in_file_name}_visualization.png")
  visualize_solution(coordinates, best_route, best_distance, file_name, title="Random Anytime Route")

  return

def visualize_solution(coordinates: list[tuple[float, float]], route: list[int], dist: float, file_name:str, title: str):
  fig, ax = plt.subplots(figsize=(12, 10))
  x_coords = [c[0] for c in coordinates]
  y_coords = [c[1] for c in coordinates]

  for i in range(len(route) - 1):
    from_i = route[i]
    to_i = route[i+1]
    ax.plot([x_coords[from_i], x_coords[to_i]],[y_coords[from_i], y_coords[to_i]],'g-', linewidth=1.5, alpha=0.7, zorder=1)
            
  ax.scatter(x_coords, y_coords, c='blue', s=50, zorder=2, edgecolors='white', linewidths=0.5)
  
  # Start / End nodes indicated via dark green dot
  ax.scatter(x_coords[0], y_coords[0], c='darkgreen', s=150, zorder=3, edgecolors='green', linewidths=2)

  ax.text(0.01, 0.01, f'Length of the solution path is {dist:.1f} meters', transform=ax.transAxes, fontsize=12)
  
  ax.set_title(title, fontsize=18, fontweight='bold', pad=20)

  plt.savefig(file_name)
  print(f"Route saved to disk as {file_name}_visualization.png")
  return


# MAKE SURE: when outputting every BSF/final, USE NEAREST INTEGER CEILING
def main() -> None:
  run_random_anytime()





# main program entry point
if __name__ == "__main__":
  # function runs only when script is executed directly, as opposed to import
  main()
