# drone-tsp-optimization
AI solution for finding optimal drone routes for pheromone distribution in orchards using TSP optimization.

## Usage
1. Place coordinate files in `/data` directory
2. Run `python src/main.py`
3. Enter filename when prompted (e.g. `32Almonds.txt`)
4. Press Enter to stop optimization and save results

## Output Files
- Output files are placed inside `/output` folder. If it doesn't exist, it will be created after the need to place the files inside by the program.
- `[filename]_SOLUTION_[distance].txt`: Node visitation order
- `[filename]_SOLUTION_[distance].png`: Route visualization

## Dependencies
- Python 3.10+
- matplotlib (`pip install matplotlib`)
