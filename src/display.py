"""Pygame display system for maze visualization."""

import pygame
from typing import Tuple, Dict
from src.maze import Maze


class MazeDisplay:
    """
    Display system for rendering mazes and algorithm progress using Pygame.
    
    Provides real-time visualization of maze generation and solving with
    color-coded indicators for mouse position, dead ends, start/end cells,
    and solution paths.
    """
    
    # Color scheme for rendering
    COLORS: Dict[str, Tuple[int, int, int]] = {
        'background': (255, 255, 255),  # White
        'wall': (0, 0, 0),               # Black
        'mouse': (255, 0, 0),            # Red
        'dead_end': (0, 0, 255),         # Blue
        'start': (0, 255, 0),            # Green
        'end': (255, 0, 0),              # Red
        'path': (255, 255, 0),           # Yellow
    }
    
    def __init__(self, maze: Maze, cell_size: int = 30, wall_thickness: int = 2) -> None:
        """
        Initialize display system with Pygame.
        
        Args:
            maze: Reference to maze being displayed
            cell_size: Size of each cell in pixels (default: 30)
            wall_thickness: Thickness of walls in pixels (default: 2)
        """
        self.maze = maze
        self.cell_size = cell_size
        self.wall_thickness = wall_thickness
        
        # Calculate window size based on maze dimensions
        self.width = maze.cols * cell_size
        self.height = maze.rows * cell_size
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Generator and Solver")
        
        # Create clock for frame rate control
        self.clock = pygame.time.Clock()
    
    def cell_to_pixel(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        """
        Convert cell coordinates to top-left pixel position.
        
        Args:
            cell: Cell coordinates (row, col)
            
        Returns:
            Pixel coordinates (x, y) of top-left corner of cell
        """
        row, col = cell
        x = col * self.cell_size
        y = row * self.cell_size
        return (x, y)
    
    def draw_maze(self) -> None:
        """
        Draw complete maze grid with current wall configuration.
        
        Renders:
        - White background
        - Black walls based on northWall and eastWall arrays
        - Outer boundary walls (top, right, bottom, left)
        """
        # Fill background with white
        self.screen.fill(self.COLORS['background'])
        
        # Draw north walls
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                if self.maze.north_wall[row][col] == 1:
                    # Draw horizontal line on north side of cell
                    x, y = self.cell_to_pixel((row, col))
                    pygame.draw.line(
                        self.screen,
                        self.COLORS['wall'],
                        (x, y),
                        (x + self.cell_size, y),
                        self.wall_thickness
                    )
        
        # Draw east walls
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                if self.maze.east_wall[row][col] == 1:
                    # Draw vertical line on east side of cell
                    x, y = self.cell_to_pixel((row, col))
                    pygame.draw.line(
                        self.screen,
                        self.COLORS['wall'],
                        (x + self.cell_size, y),
                        (x + self.cell_size, y + self.cell_size),
                        self.wall_thickness
                    )
        
        # Draw outer boundary walls
        # Top boundary
        pygame.draw.line(
            self.screen,
            self.COLORS['wall'],
            (0, 0),
            (self.width, 0),
            self.wall_thickness
        )
        
        # Right boundary
        pygame.draw.line(
            self.screen,
            self.COLORS['wall'],
            (self.width, 0),
            (self.width, self.height),
            self.wall_thickness
        )
        
        # Bottom boundary
        pygame.draw.line(
            self.screen,
            self.COLORS['wall'],
            (0, self.height),
            (self.width, self.height),
            self.wall_thickness
        )
        
        # Left boundary
        pygame.draw.line(
            self.screen,
            self.COLORS['wall'],
            (0, 0),
            (0, self.height),
            self.wall_thickness
        )
    
    def draw_cell(self, cell: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        Draw a single cell filled with specified color.
        
        Args:
            cell: Cell coordinates (row, col)
            color: RGB color tuple (r, g, b)
        """
        x, y = self.cell_to_pixel(cell)
        # Draw filled rectangle slightly inset to avoid covering walls
        rect = pygame.Rect(
            x + self.wall_thickness,
            y + self.wall_thickness,
            self.cell_size - 2 * self.wall_thickness,
            self.cell_size - 2 * self.wall_thickness
        )
        pygame.draw.rect(self.screen, color, rect)
    
    def draw_mouse(self, cell: Tuple[int, int]) -> None:
        """
        Draw red dot at current mouse position.
        
        Args:
            cell: Cell coordinates (row, col) of mouse position
        """
        x, y = self.cell_to_pixel(cell)
        # Draw circle at center of cell
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2
        radius = self.cell_size // 4
        pygame.draw.circle(
            self.screen,
            self.COLORS['mouse'],
            (center_x, center_y),
            radius
        )
    
    def draw_dead_end(self, cell: Tuple[int, int]) -> None:
        """
        Draw blue dot at dead end cell.
        
        Args:
            cell: Cell coordinates (row, col) of dead end
        """
        x, y = self.cell_to_pixel(cell)
        # Draw circle at center of cell
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2
        radius = self.cell_size // 4
        pygame.draw.circle(
            self.screen,
            self.COLORS['dead_end'],
            (center_x, center_y),
            radius
        )
    
    def draw_start_end(self) -> None:
        """
        Draw start (green) and end (red) cell markers.
        
        Requires maze.start_cell and maze.end_cell to be set.
        """
        if self.maze.start_cell is not None:
            self.draw_cell(self.maze.start_cell, self.COLORS['start'])
        
        if self.maze.end_cell is not None:
            self.draw_cell(self.maze.end_cell, self.COLORS['end'])
    
    def update(self) -> None:
        """
        Update display by flipping the display buffer.
        
        Call this after drawing operations to make changes visible.
        """
        pygame.display.flip()
    
    def handle_events(self) -> bool:
        """
        Handle pygame events (window close, etc.).
        
        Returns:
            False if quit event detected (window closed), True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        return True
    
    def cleanup(self) -> None:
        """
        Clean up Pygame resources.
        
        Call this when done with display to properly close Pygame.
        """
        pygame.quit()
