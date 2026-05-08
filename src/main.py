"""Main program for maze generator and solver with visualization."""

import argparse
import sys
import os
import pygame

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.maze import Maze
from src.generator import MazeGenerator
from src.solver import MazeSolver
from src.display import MazeDisplay


def main():
    """
    Main program orchestration for maze generation and solving.
    
    Workflow:
    1. Parse command-line arguments for configuration
    2. Initialize maze, display, and generator
    3. Generate maze with real-time visualization
    4. Display complete maze with start/end markers
    5. Solve maze with real-time visualization
    6. Display final solution path
    7. Wait for user to close window
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Maze Generator and Solver')
    parser.add_argument('--rows', type=int, default=20, help='Number of rows (default: 20)')
    parser.add_argument('--cols', type=int, default=30, help='Number of columns (default: 30)')
    parser.add_argument('--cell-size', type=int, default=25, help='Cell size in pixels (default: 25)')
    parser.add_argument('--bonus', action='store_true', help='Enable bonus mode (cycles, interior start/end)')
    parser.add_argument('--gen-delay', type=int, default=50, help='Delay between generation steps in ms (default: 50)')
    parser.add_argument('--solve-delay', type=int, default=100, help='Delay between solving steps in ms (default: 100)')
    
    args = parser.parse_args()
    
    # Configuration
    ROWS = args.rows
    COLS = args.cols
    CELL_SIZE = args.cell_size
    BONUS_CYCLES = args.bonus
    GEN_DELAY = args.gen_delay
    SOLVE_DELAY = args.solve_delay
    
    print(f"Initializing {ROWS}x{COLS} maze...")
    print(f"Bonus mode: {'enabled' if BONUS_CYCLES else 'disabled'}")
    
    # Initialize components
    maze = Maze(ROWS, COLS)
    display = MazeDisplay(maze, CELL_SIZE)
    generator = MazeGenerator(maze, bonus_cycles=BONUS_CYCLES)
    
    # Phase 1: Generate maze with visualization
    print("Generating maze...")
    
    # Initialize generation
    generator.current_cell = generator._select_random_cell()
    generator.visited.add(generator.current_cell)
    generator.stack.append(generator.current_cell)
    
    generation_complete = False
    while not generation_complete:
        # Execute one generation step
        generation_complete = generator.step()
        
        # Update display
        display.draw_maze()
        if generator.current_cell:
            display.draw_mouse(generator.current_cell)
        display.update()
        
        # Delay for visibility
        pygame.time.delay(GEN_DELAY)
        
        # Handle quit events
        if not display.handle_events():
            display.cleanup()
            return
    
    # Select start and end cells after generation
    generator._select_start_end_cells()
    
    print(f"Maze generation complete!")
    print(f"Start: {maze.start_cell}, End: {maze.end_cell}")
    
    # Phase 2: Display complete maze with start/end markers
    display.draw_maze()
    display.draw_start_end()
    display.update()
    
    # Pause to show complete maze
    pygame.time.delay(2000)
    
    # Handle events during pause
    if not display.handle_events():
        display.cleanup()
        return
    
    # Phase 3: Solve maze with visualization
    print("Solving maze...")
    
    solver = MazeSolver(maze)
    
    # Initialize solving
    solver.current_cell = maze.start_cell
    solver.visited.add(solver.current_cell)
    solver.stack.append(solver.current_cell)
    
    solving = True
    while solving:
        # Execute one solving step
        status = solver.step()
        
        # Update display
        display.draw_maze()
        display.draw_start_end()
        
        # Draw dead ends (blue dots)
        for dead_end in solver.dead_ends:
            display.draw_dead_end(dead_end)
        
        # Draw current mouse position (red dot)
        if solver.current_cell:
            display.draw_mouse(solver.current_cell)
        
        display.update()
        
        # Delay for visibility
        pygame.time.delay(SOLVE_DELAY)
        
        # Handle quit events
        if not display.handle_events():
            display.cleanup()
            return
        
        # Check if solving is complete
        if status == 'found':
            solving = False
            print("Solution found!")
        elif status == 'no_solution':
            solving = False
            print("No solution exists (this should not happen in a proper maze)")
            display.cleanup()
            return
    
    # Phase 4: Display final solution path
    print(f"Solution path length: {len(solver.get_solution_path())} cells")
    
    # Draw final solution
    display.draw_maze()
    display.draw_start_end()
    
    # Draw solution path in yellow
    for cell in solver.get_solution_path():
        # Don't overwrite start and end cells
        if cell != maze.start_cell and cell != maze.end_cell:
            display.draw_cell(cell, display.COLORS['path'])
    
    # Redraw start and end on top
    display.draw_start_end()
    
    display.update()
    
    print("Solution displayed. Close window to exit.")
    
    # Phase 5: Wait for user to close window
    running = True
    while running:
        if not display.handle_events():
            running = False
        pygame.time.delay(100)
    
    # Cleanup
    display.cleanup()
    print("Program terminated.")


if __name__ == "__main__":
    main()
