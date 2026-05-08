Tsedeniya Fiseha | UGR/9263/16  |  section-2 

https://www.loom.com/share/be5ae2eaed8442a391b27c879608709c

# Maze Generator and Solver

A Python-based maze generator and solver that creates proper rectangular mazes using a stack-based depth-first search algorithm and solves them using backtracking. The system provides real-time visualization of both the generation and solving processes using Pygame.

## Features

- **Proper Maze Generation**: Creates mazes where every cell is reachable from every other cell with exactly one unique path (no cycles, no unreachable cells)
- **Stack-Based DFS Algorithm**: Uses the "mouse algorithm" for systematic maze generation
- **Real-Time Visualization**: Watch the maze being generated and solved step-by-step
- **Backtracking Solver**: Finds paths from start to end using a stack-based backtracking algorithm
- **Visual Indicators**:
  - Red dot: Current mouse position during generation/solving
  - Blue dots: Dead ends encountered during solving
  - Green cell: Start position
  - Red cell: End position
  - Yellow cells: Final solution path
- **Configurable Parameters**: Customize maze size, cell size, and animation speed
- **Bonus Features** (optional): Cycle creation and interior start/end positions

## Installation

### Requirements

- Python 3.8 or higher
- Pygame for visualization
- Hypothesis and pytest for testing (optional, for development)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd maze-generator-solver
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pygame
pip install hypothesis pytest  # Optional, for running tests
```

## Usage

### Basic Usage

Run the maze generator and solver with default settings (20x30 maze):

```bash
python src/main.py
```

### Custom Configuration

Customize maze dimensions and visualization parameters:

```bash
# Create a 10x15 maze with larger cells
python src/main.py --rows 10 --cols 15 --cell-size 40

# Create a 50x50 maze with faster animation
python src/main.py --rows 50 --cols 50 --gen-delay 10 --solve-delay 20

# Enable bonus mode (cycles and interior start/end)
python src/main.py --bonus
```

### Command-Line Arguments

- `--rows`: Number of rows in the maze (default: 20)
- `--cols`: Number of columns in the maze (default: 30)
- `--cell-size`: Size of each cell in pixels (default: 25)
- `--gen-delay`: Delay between generation steps in milliseconds (default: 50)
- `--solve-delay`: Delay between solving steps in milliseconds (default: 100)
- `--bonus`: Enable bonus mode with cycles and interior start/end positions

## Algorithm Explanations

### Maze Generation: Stack-Based Depth-First Search (Mouse Algorithm)

The maze generator uses a stack-based depth-first search algorithm, often called the "mouse algorithm" because it simulates a mouse exploring a maze:

1. **Initialization**: Start with all walls present (a grid of isolated cells)
2. **Random Start**: Place the mouse at a randomly selected starting cell
3. **Mark as Visited**: Mark the starting cell as visited and push it onto the stack
4. **Main Loop**: While the stack is not empty:
   - Get all unvisited neighbors of the current cell
   - **If unvisited neighbors exist**:
     - Randomly select one unvisited neighbor
     - Remove the wall between the current cell and the selected neighbor
     - Mark the neighbor as visited
     - Push the current cell onto the stack (for backtracking)
     - Move the mouse to the neighbor cell
   - **If no unvisited neighbors** (dead end):
     - Pop a cell from the stack
     - Move the mouse back to that cell (backtracking)
5. **Termination**: When the stack is empty, all cells have been visited
6. **Start/End Selection**: Randomly select start and end cells

**Why This Works**: This algorithm guarantees a proper maze because:
- Every cell is visited exactly once (no cycles)
- Exactly N-1 walls are removed for N cells (tree structure)
- All cells are connected through the removed walls (full connectivity)

### Maze Solving: Backtracking Algorithm

The maze solver uses a stack-based backtracking algorithm to find a path from start to end:

1. **Initialization**: Place the mouse at the start cell
2. **Mark as Visited**: Mark the start cell as visited
3. **Main Loop**: While the current cell is not the end cell:
   - Get all unvisited accessible neighbors (adjacent cells without walls)
   - **If unvisited accessible neighbors exist**:
     - Randomly select one neighbor
     - Mark the neighbor as visited
     - Push the current cell onto the stack (to maintain the path)
     - Move the mouse to the neighbor cell
   - **If no unvisited accessible neighbors** (dead end):
     - Mark the current cell as a dead end (blue dot)
     - Pop a cell from the stack
     - Move the mouse back to that cell (backtracking)
4. **Termination**: When the end cell is reached, extract the solution path from the stack

**Why This Works**: In a proper maze (no cycles), there is exactly one path between any two cells. The backtracking algorithm explores all possible paths and is guaranteed to find the unique solution.

## Data Structure

The maze uses a wall-based representation with two 2D arrays:

### Wall Arrays

- **`northWall[R][C]`**: Represents walls on the north side of each cell
  - `northWall[r][c] = 1`: Wall exists on the north side of cell [r, c]
  - `northWall[r][c] = 0`: Wall has been removed
  
- **`eastWall[R][C]`**: Represents walls on the east side of each cell
  - `eastWall[r][c] = 1`: Wall exists on the east side of cell [r, c]
  - `eastWall[r][c] = 0`: Wall has been removed

### Wall Representation Logic

```
Cell coordinates: [row, col]
- Row 0 is the top row
- Column 0 is the leftmost column

Wall between adjacent cells:
- Cell [r, c] and [r-1, c] (north): northWall[r][c]
- Cell [r, c] and [r+1, c] (south): northWall[r+1][c]
- Cell [r, c] and [r, c-1] (west): eastWall[r][c-1]
- Cell [r, c] and [r, c+1] (east): eastWall[r][c]
```

### Visual Diagram

```
     northWall[r][c]
    ─────────────────
    |               |
    |   Cell[r,c]   | eastWall[r][c]
    |               |
    ─────────────────
   northWall[r+1][c]
```

### Boundary Handling

- Outer walls (maze boundaries) are implicit and always present
- `northWall[0][c]` represents the top boundary
- `eastWall[r][cols-1]` represents the right boundary
- South and west boundaries are handled by the grid structure

## Testing

The project includes comprehensive tests using pytest and property-based testing with Hypothesis.

### Running Tests

Run all tests:
```bash
pytest tests/
```

Run specific test categories:
```bash
# Unit tests only
pytest tests/unit/

# Property-based tests only
pytest tests/property/

# Integration tests only
pytest tests/integration/
```

### Test Coverage

Generate a coverage report:
```bash
pytest --cov=src --cov-report=html tests/
```

View the coverage report by opening `htmlcov/index.html` in a browser.

### Test Structure

- **Unit Tests** (`tests/unit/`): Test individual components (Maze, Generator, Solver, Display)
- **Property Tests** (`tests/property/`): Verify universal correctness properties across many random inputs
- **Integration Tests** (`tests/integration/`): Test end-to-end workflows

## Bonus Features

### Cycle Creation ✅ **IMPLEMENTED**

When bonus mode is enabled with `--bonus`, the generator has a 5% probability (1 in 20 chance) of creating cycles by removing additional walls during generation. This makes the maze more complex and prevents simple wall-following strategies from working.

**How it works:**
- After each normal wall removal, there's a 5% chance to remove one more random wall
- This creates loops/cycles in the maze structure
- The maze is no longer a pure tree structure

**Why it matters:**
- Defeats the "shoulder-to-the-wall" traversal method
- Makes the maze significantly more challenging
- Creates multiple paths between some cells

### Interior Start/End Positions ✅ **IMPLEMENTED**

In bonus mode, the start and end cells are placed in interior positions (not on the maze boundaries), making the maze more challenging to solve.

**How it works:**
- Start cell is selected from interior positions (not on any edge)
- End cell is also selected from interior positions
- Both are at least 1 cell away from any boundary

**Why it matters:**
- Combined with cycles, this completely defeats wall-following algorithms
- The "shoulder-to-the-wall" rule only works when start/end are on boundaries
- Creates a more realistic maze-solving challenge

### How to Enable Bonus Mode

```bash
# Enable bonus features
python run_maze.py --bonus

# Bonus mode with custom size
python run_maze.py --bonus --rows 20 --cols 30

# Bonus mode with faster animation
python run_maze.py --bonus --gen-delay 30 --solve-delay 50
```

### Demonstrating Wall-Following Failure

With bonus mode enabled:
1. The maze will have cycles (loops)
2. Start and end are in the interior
3. The simple "keep your hand on the left wall" strategy will fail
4. You might walk in circles and never reach the end
5. The backtracking solver still works because it marks visited cells

**Try it yourself:**
```bash
python run_maze.py --bonus --rows 15 --cols 20 --cell-size 35
```

Watch how the solver encounters more dead ends and backtracks more frequently due to the cycles!

## Demo Video

A demonstration video showing the maze generation and solving process is available at:

**[Demo Video Link]** _(To be added after recording)_

The demonstration shows:
- Dynamic maze generation with walls being removed progressively
- The red dot (mouse) moving through the maze during generation
- The maze solver with the red dot indicating current position
- Blue dots appearing at dead ends during backtracking
- The final solution path highlighted in yellow

## Project Structure

```
maze-generator-solver/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore file
├── src/                              # Source code
│   ├── __init__.py
│   ├── maze.py                       # Maze data structure
│   ├── generator.py                  # Maze generation algorithm
│   ├── solver.py                     # Maze solving algorithm
│   ├── display.py                    # Pygame display system
│   └── main.py                       # Main program orchestration
└── tests/                            # Test suite
    ├── __init__.py
    ├── unit/                         # Unit tests
    │   ├── test_maze.py
    │   ├── test_generator.py
    │   ├── test_solver.py
    │   └── __init__.py
    ├── property/                     # Property-based tests
    │   ├── test_properties_maze.py
    │   └── __init__.py
    └── integration/                  # Integration tests
        └── __init__.py
```

## Development

### Code Organization

The codebase follows a modular architecture with clear separation of concerns:

- **Maze (`src/maze.py`)**: Core data structure for representing mazes with wall arrays
- **Generator (`src/generator.py`)**: Maze generation using stack-based DFS
- **Solver (`src/solver.py`)**: Maze solving using backtracking
- **Display (`src/display.py`)**: Pygame-based visualization system
- **Main (`src/main.py`)**: Program orchestration and workflow management

### Incremental Development

The project was developed incrementally with clear commit history showing:
1. Project structure and dependencies setup
2. Core maze data structure implementation
3. Maze generation algorithm
4. Display system with Pygame
5. Maze solving algorithm
6. Integration and testing
7. Documentation and demonstration

### Future Enhancements

Potential improvements and extensions:
- Dead end wall placement during solving
- Multiple solving algorithms (A*, Dijkstra's, BFS)
- Maze export/import functionality
- Different maze generation algorithms (Prim's, Kruskal's)
- 3D maze generation and visualization
- Performance optimizations for very large mazes

## License

This project was created as part of a Computer Graphics course assignment.

## Author

Created for CG Assignment 1: Building and Running Mazes

---

**Note**: This implementation demonstrates proper maze generation and solving algorithms with real-time visualization. The code is well-documented with docstrings and comments explaining the algorithm steps and data structure design.
