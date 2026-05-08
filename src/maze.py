"""Maze data structure for representing rectangular mazes with wall arrays."""

from typing import List, Tuple, Optional


class Maze:
    """
    Represents a rectangular maze using north and east wall arrays.
    
    The maze uses two 2D arrays to encode walls:
    - north_wall[r][c]: 1 if wall exists on north side of cell [r,c], 0 if removed
    - east_wall[r][c]: 1 if wall exists on east side of cell [r,c], 0 if removed
    
    Cells are represented as (row, col) tuples where:
    - Row 0 is the top row
    - Column 0 is the leftmost column
    - Valid ranges: 0 <= row < rows, 0 <= col < cols
    """
    
    def __init__(self, rows: int, cols: int) -> None:
        """
        Initialize maze with all walls present.
        
        Args:
            rows: Number of rows (R) in the maze, must be >= 2
            cols: Number of columns (C) in the maze, must be >= 2
            
        Raises:
            ValueError: If rows < 2 or cols < 2
        """
        if rows < 2 or cols < 2:
            raise ValueError("Maze dimensions must be at least 2x2")
        
        self.rows = rows
        self.cols = cols
        
        # Initialize all walls to 1 (present)
        # north_wall[r][c] represents the wall on the north side of cell [r,c]
        self.north_wall: List[List[int]] = [[1 for _ in range(cols)] for _ in range(rows)]
        
        # east_wall[r][c] represents the wall on the east side of cell [r,c]
        self.east_wall: List[List[int]] = [[1 for _ in range(cols)] for _ in range(rows)]
        
        # Start and end cells (to be set later)
        self.start_cell: Optional[Tuple[int, int]] = None
        self.end_cell: Optional[Tuple[int, int]] = None
    
    def _validate_cell(self, cell: Tuple[int, int]) -> None:
        """
        Validate that a cell is within maze bounds.
        
        Args:
            cell: Cell coordinates (row, col)
            
        Raises:
            IndexError: If cell coordinates are out of bounds
        """
        row, col = cell
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Cell coordinates out of bounds")
    
    def _are_adjacent(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> bool:
        """
        Check if two cells are adjacent (differ by 1 in exactly one coordinate).
        
        Args:
            cell1: First cell coordinates (row, col)
            cell2: Second cell coordinates (row, col)
            
        Returns:
            True if cells are adjacent, False otherwise
        """
        r1, c1 = cell1
        r2, c2 = cell2
        
        # Adjacent means differ by 1 in exactly one coordinate
        row_diff = abs(r1 - r2)
        col_diff = abs(c1 - c2)
        
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)
    
    def remove_wall(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> None:
        """
        Remove wall between two adjacent cells.
        
        Determines which wall to remove based on relative positions:
        - If cell2 is north of cell1: remove north_wall[cell1.row][cell1.col]
        - If cell2 is south of cell1: remove north_wall[cell2.row][cell2.col]
        - If cell2 is east of cell1: remove east_wall[cell1.row][cell1.col]
        - If cell2 is west of cell1: remove east_wall[cell2.row][cell2.col]
        
        Args:
            cell1: First cell coordinates (row, col)
            cell2: Second cell coordinates (row, col)
            
        Raises:
            IndexError: If either cell is out of bounds
            ValueError: If cells are not adjacent
        """
        self._validate_cell(cell1)
        self._validate_cell(cell2)
        
        if not self._are_adjacent(cell1, cell2):
            raise ValueError("Cells must be adjacent to remove wall")
        
        r1, c1 = cell1
        r2, c2 = cell2
        
        # Determine which wall to remove based on relative positions
        if r2 == r1 - 1:  # cell2 is north of cell1
            self.north_wall[r1][c1] = 0
        elif r2 == r1 + 1:  # cell2 is south of cell1
            self.north_wall[r2][c2] = 0
        elif c2 == c1 + 1:  # cell2 is east of cell1
            self.east_wall[r1][c1] = 0
        elif c2 == c1 - 1:  # cell2 is west of cell1
            self.east_wall[r2][c2] = 0
    
    def has_wall(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> bool:
        """
        Check if wall exists between two adjacent cells.
        
        Args:
            cell1: First cell coordinates (row, col)
            cell2: Second cell coordinates (row, col)
            
        Returns:
            True if wall exists (value is 1), False if removed (value is 0)
            
        Raises:
            IndexError: If either cell is out of bounds
            ValueError: If cells are not adjacent
        """
        self._validate_cell(cell1)
        self._validate_cell(cell2)
        
        if not self._are_adjacent(cell1, cell2):
            raise ValueError("Cells must be adjacent to check wall")
        
        r1, c1 = cell1
        r2, c2 = cell2
        
        # Determine which wall to check based on relative positions
        if r2 == r1 - 1:  # cell2 is north of cell1
            return self.north_wall[r1][c1] == 1
        elif r2 == r1 + 1:  # cell2 is south of cell1
            return self.north_wall[r2][c2] == 1
        elif c2 == c1 + 1:  # cell2 is east of cell1
            return self.east_wall[r1][c1] == 1
        elif c2 == c1 - 1:  # cell2 is west of cell1
            return self.east_wall[r2][c2] == 1
        
        return True  # Should never reach here if adjacency check passed
    
    def get_neighbors(self, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Return list of valid adjacent cells (within bounds).
        
        Adjacent cells are those that differ by 1 in exactly one coordinate:
        - North: [row-1, col]
        - South: [row+1, col]
        - East: [row, col+1]
        - West: [row, col-1]
        
        Args:
            cell: Cell coordinates (row, col)
            
        Returns:
            List of adjacent cell coordinates that are within maze bounds
            
        Raises:
            IndexError: If cell is out of bounds
        """
        self._validate_cell(cell)
        
        row, col = cell
        neighbors = []
        
        # Check north neighbor
        if row > 0:
            neighbors.append((row - 1, col))
        
        # Check south neighbor
        if row < self.rows - 1:
            neighbors.append((row + 1, col))
        
        # Check east neighbor
        if col < self.cols - 1:
            neighbors.append((row, col + 1))
        
        # Check west neighbor
        if col > 0:
            neighbors.append((row, col - 1))
        
        return neighbors
    
    def get_accessible_neighbors(self, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Return list of adjacent cells accessible without walls.
        
        Args:
            cell: Cell coordinates (row, col)
            
        Returns:
            List of adjacent cell coordinates that are accessible (no wall between)
            
        Raises:
            IndexError: If cell is out of bounds
        """
        self._validate_cell(cell)
        
        neighbors = self.get_neighbors(cell)
        accessible = []
        
        for neighbor in neighbors:
            if not self.has_wall(cell, neighbor):
                accessible.append(neighbor)
        
        return accessible
    
    def set_start_end(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """
        Set start and end cell positions.
        
        Args:
            start: Start cell coordinates (row, col)
            end: End cell coordinates (row, col)
            
        Raises:
            IndexError: If either cell is out of bounds
            ValueError: If start and end are the same cell
        """
        self._validate_cell(start)
        self._validate_cell(end)
        
        if start == end:
            raise ValueError("Start and end cells must be different")
        
        self.start_cell = start
        self.end_cell = end
