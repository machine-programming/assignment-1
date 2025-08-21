
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, TypeVar, Generic, Generator
import numpy as np
from tqdm import tqdm

from enumerative_synthesis import BottomUpSynthesizer
from shapes import Shape, Rectangle, Triangle, Circle, Union, Intersection, Mirror, Subtraction, Coordinate, MAX_COORD

class ShapeSynthesizer(BottomUpSynthesizer[Shape]):
    """Bottom-up enumerative synthesizer for geometric shapes"""
    
    def generate_terminals(self, examples: List[Tuple[float, float, bool]]) -> List[Shape]:
        """Generate all terminal shapes (rectangles, triangles, circles)"""
        shapes = []
        
        # Generate all coordinates
        coords = [Coordinate(x, y) for x in range(MAX_COORD + 1) for y in range(MAX_COORD + 1)]
        
        # Generate rectangles and triangles
        total_rect_tri = len(coords) * len(coords)
        with tqdm(total=total_rect_tri, desc="[Generating Teminals] Rectangles & Triangles", unit="shape") as pbar:
            for bottom_left in coords:
                for top_right in coords:
                    if bottom_left.x < top_right.x and bottom_left.y < top_right.y:
                        shapes.append(Rectangle(bottom_left, top_right))
                        shapes.append(Triangle(bottom_left, top_right))
                    pbar.update(1)
        
        # Generate circles
        total_circles = len(coords) * MAX_COORD
        with tqdm(total=total_circles, desc="[Generating Teminals] Circles", unit="circle") as pbar:
            for center in coords:
                for radius in range(1, MAX_COORD + 1):
                    shapes.append(Circle(center, radius))
                    pbar.update(1)
        
        return shapes
    
    def grow(self, program_list: List[Shape], examples: List[Any]) -> List[Shape]:
        """Grow the program list by one level using all possible operations"""
        
        ###################################################################################################
        #                                                                                                 #
        # Part 1 (a): Synthesizing Geometric Shapes (`grow`)                                              #
        #                                                                                                 #
        # TODO: Add your implementation here.                                                             #
        #                                                                                                 #
        # NOTE: Below is a placeholder implementation that does not grow the program list. You need to    #
        #       implement the actual growth logic here.                                                   #
        #                                                                                                 #
        ###################################################################################################             

        new_programs = []
        
        return new_programs
    
    def is_correct(self, program: Shape, examples: List[Tuple[float, float, bool]]) -> bool:
        """Check if a program produces the expected output on all examples"""
        try:
            xs = np.array([ex[0] for ex in examples])
            ys = np.array([ex[1] for ex in examples])
            expected = np.array([ex[2] for ex in examples])
            
            result = program.interpret(xs, ys)
            return np.array_equal(result, expected)
        except Exception:
            return False
    
    def extract_test_inputs(self, examples: List[Tuple[float, float, bool]]) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Extract test inputs from examples for equivalence elimination"""
        xs = np.array([ex[0] for ex in examples])
        ys = np.array([ex[1] for ex in examples])
        return [(xs, ys)]

    def compute_signature(self, program: Shape, test_inputs: List[Tuple[np.ndarray, np.ndarray]]) -> Any:
        """Compute a signature for a geometric shape on test inputs for equivalence checking"""
        try:
            xs, ys = test_inputs[0]
            return tuple(program.interpret(xs, ys))
        except Exception:
            return None # Indicate failure to interpret
