# main.py
# refactor and reimplement using numpy later

def print_menu(text: str) -> None:
  print(text)

# main program entry point
def main() -> None:
  test_greeting = "hi there"
  print_menu(test_greeting)

if __name__ == "__main__":
  # function runs only when script is executed directly, as opposed to import
  main()