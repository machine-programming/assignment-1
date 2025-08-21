"""
Geometric Shape DSL Implementation
This module defines the domain-specific language for 2D geometric shapes.
"""

from abc import ABC, abstractmethod
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
import os
import inspect

MAX_COORD = 9

@dataclass(frozen=True)
class Coordinate:
    """Represents a 2D coordinate with integer values in range [0, MAX_COORD]"""
    x: int
    y: int
    
    def __post_init__(self):
        assert 0 <= self.x <= MAX_COORD, f"x coordinate {self.x} out of range"
        assert 0 <= self.y <= MAX_COORD, f"y coordinate {self.y} out of range"

class Shape(ABC):
    """Abstract base class for all shapes in our DSL"""
    
    @abstractmethod
    def interpret(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        """Interpret the shape at given coordinates, returning boolean array"""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

class Rectangle(Shape):
    """Rectangle shape defined by bottom-left and top-right coordinates"""
    
    def __init__(self, bottom_left: Coordinate, top_right: Coordinate):
        assert bottom_left.x < top_right.x and bottom_left.y < top_right.y, \
            "bottom_left must be below and to the left of top_right"
        self.bottom_left = bottom_left
        self.top_right = top_right
    
    def interpret(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        return ((self.bottom_left.x <= xs) & (xs <= self.top_right.x) &
                (self.bottom_left.y <= ys) & (ys <= self.top_right.y))
    
    def __str__(self) -> str:
        return f"Rect({self.bottom_left.x},{self.bottom_left.y},{self.top_right.x},{self.top_right.y})"
    
    def __hash__(self) -> int:
        return hash(('rect', self.bottom_left.x, self.bottom_left.y, self.top_right.x, self.top_right.y))
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, Rectangle) and 
                self.bottom_left == other.bottom_left and 
                self.top_right == other.top_right)

class Triangle(Shape):
    """Right triangle shape defined by bottom-left and top-right coordinates"""
    
    def __init__(self, bottom_left: Coordinate, top_right: Coordinate):
        assert bottom_left.x < top_right.x and bottom_left.y < top_right.y, \
            "bottom_left must be below and to the left of top_right"
        self.bottom_left = bottom_left
        self.top_right = top_right
    
    def interpret(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        width = self.top_right.x - self.bottom_left.x
        height = self.top_right.y - self.bottom_left.y
        m = height / width
        b = self.bottom_left.y - m * self.bottom_left.x
        
        below_line = ys <= m * xs + b
        return ((self.bottom_left.x <= xs) & (xs <= self.top_right.x) &
                (self.bottom_left.y <= ys) & (ys <= self.top_right.y) &
                below_line)
    
    def __str__(self) -> str:
        return f"Triangle({self.bottom_left.x},{self.bottom_left.y},{self.top_right.x},{self.top_right.y})"
    
    def __hash__(self) -> int:
        return hash(('triangle', self.bottom_left.x, self.bottom_left.y, self.top_right.x, self.top_right.y))
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, Triangle) and 
                self.bottom_left == other.bottom_left and 
                self.top_right == other.top_right)

class Circle(Shape):
    """Circle shape defined by center coordinate and radius"""
    
    def __init__(self, center: Coordinate, radius: int):
        assert 1 <= radius <= MAX_COORD, f"radius {radius} out of range"
        self.center = center
        self.radius = radius
    
    def interpret(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        return ((xs - self.center.x)**2 + (ys - self.center.y)**2) <= self.radius**2
    
    def __str__(self) -> str:
        return f"Circle({self.center.x},{self.center.y},{self.radius})"
    
    def __hash__(self) -> int:
        return hash(('circle', self.center.x, self.center.y, self.radius))
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, Circle) and 
                self.center == other.center and 
                self.radius == other.radius)

class Union(Shape):
    """Union of two shapes"""
    
    def __init__(self, first: Shape, second: Shape):
        self.first = first
        self.second = second
    
    def interpret(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        return self.first.interpret(xs, ys) | self.second.interpret(xs, ys)
    
    def __str__(self) -> str:
        return f"Union({self.first}, {self.second})"
    
    def __hash__(self) -> int:
        return hash(('union', hash(self.first), hash(self.second)))
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, Union) and 
                self.first == other.first and 
                self.second == other.second)

class Intersection(Shape):
    """Intersection of two shapes"""
    
    def __init__(self, first: Shape, second: Shape):
        self.first = first
        self.second = second
    
    def interpret(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        return self.first.interpret(xs, ys) & self.second.interpret(xs, ys)
    
    def __str__(self) -> str:
        return f"Intersection({self.first}, {self.second})"
    
    def __hash__(self) -> int:
        return hash(('intersection', hash(self.first), hash(self.second)))
    
    def __eq__(self, other) -> bool:
        return (isinstance(other, Intersection) and 
                self.first == other.first and 
                self.second == other.second)

class Mirror(Shape):
    """Mirror a shape across the line y=x"""
    
    def __init__(self, shape: Shape):
        self.shape = shape
    
    def interpret(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        return self.shape.interpret(xs, ys) | self.shape.interpret(ys, xs)
    
    def __str__(self) -> str:
        return f"Mirror({self.shape})"
    
    def __hash__(self) -> int:
        return hash(('mirror', hash(self.shape)))
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Mirror) and self.shape == other.shape

class Subtraction(Shape):
    """Subtraction of two shapes"""
    
    def __init__(self, first: Shape, second: Shape):
        self.first = first
        self.second = second
    
    def interpret(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        return self.first.interpret(xs, ys) & ~self.second.interpret(xs, ys)
    
    def __str__(self) -> str:
        return f"Subtraction({self.first}, {self.second})"
    
    def __hash__(self) -> int:
        return hash(('subtraction', hash(self.first), hash(self.second)))
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Subtraction) and self.first == other.first and self.second == other.second

class ShapeVisualizer:
    """Visualization tools for shape synthesis results."""
    
    def __init__(self, output_dir=None):
        """Initialize the visualizer with output directory.
        
        If output_dir is not specified, automatically creates a 'shape_visualization'
        folder in the same directory as the calling script (e.g., test_part1.py).
        """
        if output_dir is None:
            # Get the directory of the calling script (e.g., test_part1.py)
            caller_frame = inspect.currentframe().f_back
            caller_file = caller_frame.f_globals.get('__file__', '')
            if caller_file:
                caller_dir = os.path.dirname(os.path.abspath(caller_file))
                output_dir = os.path.join(caller_dir, "shape_visualization")
            else:
                # Fallback to current working directory if we can't determine caller
                output_dir = "shape_visualization"
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up matplotlib style for non-interactive backend
        plt.ioff()  # Turn off interactive mode
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (10, 10)  # Make figures square
        plt.rcParams['font.size'] = 12
        
    def visualize_examples(self, xs, ys, out, test_name, save_path=None):
        """Visualize only the positive and negative example points."""
        fig, ax = plt.subplots(figsize=(10, 10))  # Square figure
        
        # Separate positive and negative points
        pos_mask = out == True
        neg_mask = out == False
        
        # Plot positive points in green
        if np.any(pos_mask):
            ax.scatter(xs[pos_mask], ys[pos_mask], c='green', s=100, 
                      marker='o', label='Positive Examples', alpha=0.8, edgecolors='black')
        
        # Plot negative points in red
        if np.any(neg_mask):
            ax.scatter(xs[neg_mask], ys[neg_mask], c='red', s=100, 
                      marker='x', label='Negative Examples', alpha=0.8, linewidths=2)
        
        # Set up the plot
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title(f'{test_name} - Example Points')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Set equal aspect ratio and fixed bounds from 0 to 10
        ax.set_aspect('equal')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        
        # Add point coordinates as annotations for small datasets
        if len(xs) <= 20:
            for i, (x, y) in enumerate(zip(xs, ys)):
                ax.annotate(f'({x:.1f}, {y:.1f})', (x, y), 
                           xytext=(5, 5), textcoords='offset points', 
                           fontsize=8, alpha=0.7)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        # Close the figure instead of showing it
        plt.close(fig)
        
    def visualize_synthesized(self, xs, ys, out, program, test_name, save_path=None):
        """Visualize the synthesized program with example points overlaid."""
        fig, ax = plt.subplots(figsize=(10, 10))  # Square figure
        
        # Create a grid for visualization with fixed bounds from 0 to 10
        grid_size = 200
        x_grid = np.linspace(0, 10, grid_size)
        y_grid = np.linspace(0, 10, grid_size)
        X, Y = np.meshgrid(x_grid, y_grid)
        
        # Evaluate the program on the grid
        try:
            Z = program.interpret(X.flatten(), Y.flatten())
            Z = Z.reshape(X.shape)
            
            # Plot the synthesized shape
            ax.contourf(X, Y, Z, levels=[0, 0.5, 1], 
                       colors=['white', 'lightblue'], alpha=0.6)
            ax.contour(X, Y, Z, levels=[0.5], colors='blue', linewidths=2)
            
        except Exception as e:
            print(f"Warning: Could not visualize program: {e}")
            # If program visualization fails, just show the background
            ax.set_facecolor('lightgray')
        
        # Separate positive and negative points
        pos_mask = out == True
        neg_mask = out == False
        
        # Plot positive points in green
        if np.any(pos_mask):
            ax.scatter(xs[pos_mask], ys[pos_mask], c='green', s=100, 
                      marker='o', label='Positive Examples', alpha=0.8, edgecolors='black')
        
        # Plot negative points in red
        if np.any(neg_mask):
            ax.scatter(xs[neg_mask], ys[neg_mask], c='red', s=100, 
                      marker='x', label='Negative Examples', alpha=0.8, linewidths=2)
        
        # Set up the plot
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title(f'{test_name} - Synthesized Program')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Set equal aspect ratio and fixed bounds from 0 to 10
        ax.set_aspect('equal')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        
        # Add program description
        if program:
            program_str = str(program)
            if len(program_str) > 50:
                program_str = program_str[:47] + "..."
            ax.text(0.02, 0.98, f"Program: {program_str}", 
                   transform=ax.transAxes, fontsize=10, 
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        # Close the figure instead of showing it
        plt.close(fig)
        
    def visualize_test_case(self, xs, ys, out, test_name, program=None):
        """Generate both visualizations for a test case."""
        # Create filenames
        examples_filename = f"{test_name}_examples.png"
        synthesized_filename = f"{test_name}_synthesized.png"
        
        examples_path = os.path.join(self.output_dir, examples_filename)
        synthesized_path = os.path.join(self.output_dir, synthesized_filename)
        
        # Generate examples visualization
        self.visualize_examples(xs, ys, out, test_name, examples_path)
        
        # Generate synthesized visualization if program is provided
        if program:
            self.visualize_synthesized(xs, ys, out, program, test_name, synthesized_path)
        else:
            print(f"No program provided for {test_name}, skipping synthesized visualization")
            
    def close_all_plots(self):
        """Close all matplotlib plots to free memory."""
        plt.close('all')
