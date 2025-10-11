# main.py
# refactor and reimplement using numpy later

import os

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
          # raise ValueError("Incorrect file format. Expected IEEE 754 floating point.")
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

def print_loaded_coordinates(coordinates: list[tuple[float, float]]) -> None:
  for idx, (x, y) in enumerate(coordinates, start = 1): # start idx 1 for clarity
    print(f"{idx:3d}: ({x:.7f}, {y:.7f})")

def main() -> None:
  file_name = input("ComputeDronePath\nEnter the name of file: ")

  coordinates = load_coordinate_data(file_name)
  n = len(coordinates)

  print(f"There are {n} nodes, computing route..")
  # print_loaded_coordinates(coordinates)





  # start computation calls here or something





# main program entry point
if __name__ == "__main__":
  # function runs only when script is executed directly, as opposed to import
  main()