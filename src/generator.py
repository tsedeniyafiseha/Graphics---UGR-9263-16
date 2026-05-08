"""Maze generator using stack-based depth-first search (mouse algorithm)."""

import random
from typing import List, Tuple, Optional, Callable, Set
from src.maze import Maze


class MazeGenerator:
    """
    Generate proper mazes using stack-based depth-first search.
    
    The generator uses the "mouse algorithm" where a virtual mouse traverses
    the maze grid, removing walls as it visits new cells. When the mouse
    reaches a dead end (no unvisited neighbors), it backtracks using a stack
    until it finds a cell with unvisited neighbors.
    
    This algorithm guarantees a proper maze:
    - Every cell is reachable from every other cell
    - Exactly one path exists between any two cells (no cycles)
    - Exactly N-1 walls are removed for N cells
    """
    
    def __init__(self, maze: Maze, callback: Optional[Callable] = None, bonus_cycles: bool = False) -> None:
        """
        Initialize maze generator.
        
        Args:
            maze: Reference to maze being generated
            callback: Optional callback function called after each step for visualization
            bonus_cycles: If True, randomly create cycles by removing extra walls (1 in 20 chance)
        """
        self.maze = maze
        self.callback = callback
        self.bonus_cycles = bonus_cycles
        self.visited: Set[Tuple[int, int]] = set()
        self.stack: List[Tuple[int, int]] = []
        self.current_cell: Optional[Tuple[int, int]] = None
    
    def generate(self, start_cell: Optional[Tuple[int, int]] = None) -> None:
        """
        Generate maze starting from given cell (random if None).
        
        This method runs the complete generation algorithm until the maze
        is fully generated. For step-by-step visualization, use the step()
        method instead.
        
        Args:
            start_cell: Starting cell coordinates (row, col), random if None
        """
        # Initialize generation
        if start_cell is None:
            start_cell = self._select_random_cell()
        
        self.current_cell = start_cell
        self.visited.add(start_cell)
        self.stack.append(start_cell)
        
        # Run generation until complete
        while not self.step():
            pass
        
        # Select start and end cells after generation
        self._select_start_end_cells()
    
    def step(self) -> bool:
        """
        Execute one step of generation algorithm.
        
        Returns:
            True if generation is complete (stack is empty), False otherwise
        """
        # Check if generation is complete
        if not self.stack:
            return True
        
        # Get unvisited neighbors of current cell
        unvisited_neighbors = self._get_unvisited_neighbors(self.current_cell)
        
        if unvisited_neighbors:
            # Choose random unvisited neighbor
            neighbor = self._select_random_neighbor(unvisited_neighbors)
            
            # Remove wall between current cell and neighbor
            self.maze.remove_wall(self.current_cell, neighbor)
            
            # Bonus: Maybe create a cycle by removing an additional wall
            if self.bonus_cycles:
                self._maybe_create_cycle()
            
            # Mark neighbor as visited
            self.visited.add(neighbor)
            
            # Push current cell onto stack
            self.stack.append(self.current_cell)
            
            # Move to neighbor
            self.current_cell = neighbor
        else:
            # Dead end - backtrack
            self.current_cell = self.stack.pop()
        
        # Call visualization callback if provided
        if self.callback:
            self.callback()
        
        # Generation not complete yet
        return False
    
    def _get_unvisited_neighbors(self, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Return list of unvisited adjacent cells.
        
        Args:
            cell: Cell coordinates (row, col)
            
        Returns:
            List of unvisited neighbor cell coordinates
        """
        neighbors = self.maze.get_neighbors(cell)
        return [n for n in neighbors if n not in self.visited]
    
    def _select_random_neighbor(self, neighbors: List[Tuple[int, int]]) -> Tuple[int, int]:
        """
        Randomly select one neighbor from list.
        
        Args:
            neighbors: List of neighbor cell coordinates
            
        Returns:
            Randomly selected neighbor cell coordinates
        """
        return random.choice(neighbors)
    
    def _select_random_cell(self) -> Tuple[int, int]:
        """
        Select a random cell from the maze.
        
        Returns:
            Random cell coordinates (row, col)
        """
        row = random.randint(0, self.maze.rows - 1)
        col = random.randint(0, self.maze.cols - 1)
        return (row, col)
    
    def _select_start_end_cells(self) -> None:
        """
        Select random start and end cells after generation completes.
        
        If bonus_cycles is enabled, selects interior cells (not on boundaries).
        Otherwise, selects any random cells.
        
        Ensures start and end cells are different.
        """
        if self.bonus_cycles:
            # Select interior cells for bonus mode
            start = self._select_interior_cell()
            end = self._select_interior_cell()
            
            # Ensure start and end are different
            while end == start:
                end = self._select_interior_cell()
        else:
            # Select any random cells
            start = self._select_random_cell()
            end = self._select_random_cell()
            
            # Ensure start and end are different
            while end == start:
                end = self._select_random_cell()
        
        self.maze.set_start_end(start, end)
    
    def _select_interior_cell(self) -> Tuple[int, int]:
        """
        Select a random interior cell (not on any boundary).
        
        Returns:
            Random interior cell coordinates (row, col)
        """
        # Ensure maze is large enough for interior cells
        if self.maze.rows < 3 or self.maze.cols < 3:
            # Fall back to random cell if maze too small
            return self._select_random_cell()
        
        row = random.randint(1, self.maze.rows - 2)
        col = random.randint(1, self.maze.cols - 2)
        return (row, col)
    
    def _maybe_create_cycle(self) -> None:
        """
        Bonus feature: Randomly create a cycle by removing an additional wall.
        
        Has a 5% (1 in 20) probability of removing an extra wall between
        the current cell and a random neighbor that still has a wall.
        This creates cycles in the maze, making it more complex.
        """
        # 5% chance (1 in 20)
        if random.random() < 0.05:
            # Get all neighbors with walls still present
            neighbors_with_walls = []
            for neighbor in self.maze.get_neighbors(self.current_cell):
                if self.maze.has_wall(self.current_cell, neighbor):
                    neighbors_with_walls.append(neighbor)
            
            # If there are walls to remove, pick one randomly
            if neighbors_with_walls:
                extra_neighbor = random.choice(neighbors_with_walls)
                self.maze.remove_wall(self.current_cell, extra_neighbor)
