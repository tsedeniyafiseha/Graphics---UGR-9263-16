"""Maze solver using backtracking algorithm."""

import random
from typing import List, Tuple, Optional, Callable, Set
from src.maze import Maze


class MazeSolver:
    """
    Solve mazes using backtracking algorithm.
    
    The solver uses a stack-based backtracking approach where a virtual mouse
    explores the maze from the start cell to the end cell. When the mouse
    reaches a dead end (no unvisited accessible neighbors), it backtracks
    using a stack until it finds a cell with unexplored paths.
    
    Dead ends are marked with blue dots during visualization, and the current
    position is marked with a red dot.
    """
    
    def __init__(self, maze: Maze, callback: Optional[Callable] = None) -> None:
        """
        Initialize maze solver.
        
        Args:
            maze: Reference to maze being solved
            callback: Optional callback function called after each step for visualization
        """
        self.maze = maze
        self.callback = callback
        self.visited: Set[Tuple[int, int]] = set()
        self.stack: List[Tuple[int, int]] = []
        self.current_cell: Optional[Tuple[int, int]] = None
        self.dead_ends: Set[Tuple[int, int]] = set()
        self.solution_path: List[Tuple[int, int]] = []
        self.solved: bool = False
    
    def solve(self) -> bool:
        """
        Solve maze from start to end cell.
        
        This method runs the complete solving algorithm until the end cell
        is reached or no solution exists. For step-by-step visualization,
        use the step() method instead.
        
        Returns:
            True if solution found, False otherwise
        """
        # Validate start and end cells are set
        if self.maze.start_cell is None or self.maze.end_cell is None:
            raise ValueError("Start and end cells must be set and valid")
        
        # Initialize solving
        self.current_cell = self.maze.start_cell
        self.visited.add(self.current_cell)
        # Note: Don't push start_cell to stack initially
        # It will be pushed when we move to the first neighbor
        
        # Run solving until complete
        while True:
            status = self.step()
            if status == 'found':
                self.solved = True
                return True
            elif status == 'no_solution':
                return False
    
    def step(self) -> str:
        """
        Execute one step of solving algorithm.
        
        Returns:
            'found' if end cell reached
            'backtrack' if backtracking from dead end
            'continue' if moving to new cell
            'no_solution' if no solution exists (stack empty before reaching end)
        """
        # Check if we've reached the end
        if self.current_cell == self.maze.end_cell:
            self._extract_solution_path()
            return 'found'
        
        # Get unvisited accessible neighbors
        unvisited_accessible = self._get_unvisited_accessible_neighbors(self.current_cell)
        
        if unvisited_accessible:
            # Choose random unvisited accessible neighbor
            neighbor = random.choice(unvisited_accessible)
            
            # Mark neighbor as visited
            self.visited.add(neighbor)
            
            # Push current cell onto stack (to maintain path)
            self.stack.append(self.current_cell)
            
            # Move to neighbor
            self.current_cell = neighbor
            
            # Call visualization callback if provided
            if self.callback:
                self.callback()
            
            return 'continue'
        else:
            # Dead end - mark current cell as dead end
            if self.current_cell != self.maze.start_cell:
                self.dead_ends.add(self.current_cell)
            
            # Backtrack
            if not self.stack:
                # No solution exists (should not happen in proper maze)
                return 'no_solution'
            
            self.current_cell = self.stack.pop()
            
            # Call visualization callback if provided
            if self.callback:
                self.callback()
            
            return 'backtrack'
    
    def _get_unvisited_accessible_neighbors(self, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Return list of unvisited neighbors accessible without walls.
        
        Args:
            cell: Cell coordinates (row, col)
            
        Returns:
            List of unvisited accessible neighbor cell coordinates
        """
        accessible_neighbors = self.maze.get_accessible_neighbors(cell)
        return [n for n in accessible_neighbors if n not in self.visited]
    
    def _is_dead_end(self, cell: Tuple[int, int]) -> bool:
        """
        Check if cell is a dead end (no unvisited accessible neighbors).
        
        Args:
            cell: Cell coordinates (row, col)
            
        Returns:
            True if cell is a dead end, False otherwise
        """
        unvisited_accessible = self._get_unvisited_accessible_neighbors(cell)
        return len(unvisited_accessible) == 0
    
    def _extract_solution_path(self) -> None:
        """
        Extract solution path from stack when end cell is reached.
        
        The stack contains the path from start to current position,
        but may include backtracking. We need to extract only the
        actual path from start to end.
        """
        # The stack contains cells in the order they were pushed
        # When we reach the end, the stack has the complete path
        # including the current cell
        self.solution_path = self.stack.copy()
        self.solution_path.append(self.current_cell)
    
    def get_solution_path(self) -> List[Tuple[int, int]]:
        """
        Return the solution path from start to end.
        
        Returns:
            List of cell coordinates forming the solution path
            Empty list if no solution found yet
        """
        return self.solution_path
