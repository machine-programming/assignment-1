"""
Part 1: Geometric Shape DSL - Test Cases and Examples
This file contains test cases and examples for the geometric shape synthesis task.
Students should examine these test cases to understand the expected behavior.
"""

import unittest
import numpy as np
import random
import os

from shapes import Coordinate, Rectangle, Triangle, Circle, Union, Intersection, Mirror, Subtraction

# Set global random seed for reproducible results
RANDOM_SEED = 42

class TestPart1Shapes(unittest.TestCase):
    """Test cases for Part 1: Geometric Shape DSL"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        print(f"\n{'='*60}")
        print("PART 1: GEOMETRIC SHAPE DSL TESTS")
        print(f"{'='*60}")
        reset_random_seed()
        
        # Import required modules
        try:
            from shape_synthesizer import ShapeSynthesizer
            cls.shapes_available = True
            cls.ShapeSynthesizer = ShapeSynthesizer
        except ImportError as e:
            print(f"Warning: Required modules not available: {e}")
            cls.shapes_available = False
    
    def setUp(self):
        """Set up each individual test"""
        if not self.shapes_available:
            self.fail("Required modules not available")
    
    def test_rectangle_interpretation(self):
        rect = Rectangle(Coordinate(1, 1), Coordinate(3, 3))
        xs = np.array([0, 1, 2, 3, 4])
        ys = np.array([0, 1, 2, 3, 4])
        result = rect.interpret(xs, ys)
        expected = np.array([False, True, True, True, False])
        
        np.testing.assert_array_equal(result, expected)
    
    def test_triangle_interpretation(self):
        triangle = Triangle(Coordinate(0, 0), Coordinate(4, 4))
        xs = np.array([0, 1, 2, 3, 4])
        ys = np.array([0, 1, 2, 3, 4])
        result = triangle.interpret(xs, ys)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.dtype, bool)
        self.assertEqual(len(result), len(xs))
    
    def test_circle_interpretation(self):
        circle = Circle(Coordinate(2, 2), 2)
        xs = np.array([2, 1, 4, 0, 3])
        ys = np.array([2, 2, 2, 2, 3])
        result = circle.interpret(xs, ys)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.dtype, bool)
        self.assertEqual(len(result), len(xs))
    
    def test_union_operation(self):
        rect1 = Rectangle(Coordinate(0, 0), Coordinate(2, 2))
        rect2 = Rectangle(Coordinate(1, 1), Coordinate(3, 3))
        union = Union(rect1, rect2)
        
        xs = np.array([0, 1, 2, 3, 4])
        ys = np.array([0, 1, 2, 3, 4])
        result = union.interpret(xs, ys)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.dtype, bool)
        self.assertEqual(len(result), len(xs))
    
    def test_intersection_operation(self):
        rect1 = Rectangle(Coordinate(0, 0), Coordinate(3, 3))
        rect2 = Rectangle(Coordinate(1, 1), Coordinate(4, 4))
        intersection = Intersection(rect1, rect2)
        
        xs = np.array([0, 1, 2, 3, 4])
        ys = np.array([0, 1, 2, 3, 4])
        result = intersection.interpret(xs, ys)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.dtype, bool)
        self.assertEqual(len(result), len(xs))
    
    def test_mirror_operation(self):
        rect = Rectangle(Coordinate(0, 1), Coordinate(1, 3))
        mirror = Mirror(rect)
        
        xs = np.array([0, 1, 2])
        ys = np.array([1, 2, 0])
        result = mirror.interpret(xs, ys)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.dtype, bool)
        self.assertEqual(len(result), len(xs))
    
    def test_subtraction_operation(self):
        rect1 = Rectangle(Coordinate(0, 0), Coordinate(4, 4))
        rect2 = Rectangle(Coordinate(1, 1), Coordinate(3, 3))
        subtraction = Subtraction(rect1, rect2)
        
        xs = np.array([0, 1, 2, 3, 4])
        ys = np.array([0, 1, 2, 3, 4])
        result = subtraction.interpret(xs, ys)
        
        # Should be True for outer rectangle but False for inner rectangle
        expected = np.array([True, False, False, False, True])
        np.testing.assert_array_equal(result, expected)
    
    def test_rectangle_synthesis(self):
        examples = [
            (0, 0, False), (1, 1, True), (2, 2, True),
            (3, 3, False), (1, 2, True), (2, 1, True)
        ]
        
        xs = np.array([ex[0] for ex in examples])
        ys = np.array([ex[1] for ex in examples])
        out = np.array([ex[2] for ex in examples])
        
        self._test_synthesis(xs, ys, out, "rectangle_synthesis")
    
    def test_circle_synthesis(self):
        examples = [
            (2, 2, True), (1, 2, True), (3, 2, True),
            (2, 1, True), (2, 3, True), (1, 1, False)
        ]
        
        xs = np.array([ex[0] for ex in examples])
        ys = np.array([ex[1] for ex in examples])
        out = np.array([ex[2] for ex in examples])
        
        self._test_synthesis(xs, ys, out, "circle_synthesis")
    
    def test_union_synthesis(self):
        examples = [
            (0, 0, True), (1, 1, True), (2, 2, True),
            (3, 3, False), (0, 1, True), (2, 0, False)
        ]
        
        xs = np.array([ex[0] for ex in examples])
        ys = np.array([ex[1] for ex in examples])
        out = np.array([ex[2] for ex in examples])
        
        self._test_synthesis(xs, ys, out, "union_synthesis")
    
    def test_triangle_mirror_synthesis(self):
        examples = [
            (0, 0, True), (1, 1, True), (2, 2, True),
            (3, 3, False), (4, 4, False), (5, 5, True),
            (6, 6, True), (7, 7, True), (8, 8, False)
        ]
        
        xs = np.array([ex[0] for ex in examples])
        ys = np.array([ex[1] for ex in examples])
        out = np.array([ex[2] for ex in examples])
        
        self._test_synthesis(xs, ys, out, "triangle_mirror_synthesis")
    
    def test_circle_rectangle_intersection(self):
        examples = [
            (1, 1, False), (2, 2, True), (3, 3, True),
            (4, 4, False), (2, 1, True), (3, 1, True),
            (1, 2, True), (1, 3, False), (4, 2, False)
        ]
        
        xs = np.array([ex[0] for ex in examples])
        ys = np.array([ex[1] for ex in examples])
        out = np.array([ex[2] for ex in examples])
        
        self._test_synthesis(xs, ys, out, "circle_rectangle_intersection")
    
    def test_triangle_circle_union(self):
        examples = [
            (0, 0, True), (1, 1, True), (2, 2, True),
            (3, 3, True), (4, 4, False), (2, 0, True),
            (0, 2, True), (5, 2, True), (2, 5, False)
        ]
        
        xs = np.array([ex[0] for ex in examples])
        ys = np.array([ex[1] for ex in examples])
        out = np.array([ex[2] for ex in examples])
        
        self._test_synthesis(xs, ys, out, "triangle_circle_union")
    
    def test_mirror_circle_synthesis(self):
        examples = [
            (0, 2, True), (1, 2, True), (2, 2, True),
            (3, 2, False), (4, 2, False), (2, 0, True),
            (2, 1, True), (2, 3, True), (2, 4, False)
        ]
        
        xs = np.array([ex[0] for ex in examples])
        ys = np.array([ex[1] for ex in examples])
        out = np.array([ex[2] for ex in examples])
        
        self._test_synthesis(xs, ys, out, "mirror_circle_synthesis")
    
    def test_mirror_triangle(self):
        examples = [
            (2, 2, False), (1, 2, True), (3, 2, True),  # Center removed, sides remain
            (2, 1, True), (2, 3, True), (0, 2, False),  # Top/bottom remain, outside circle False
            (4, 2, False), (2, 0, False), (2, 4, False),  # Outside circle
            (1, 1, False), (3, 3, False), (1, 3, True), (3, 1, True)  # Corners of rectangle removed, other circle parts remain
        ]
        
        xs = np.array([ex[0] for ex in examples])
        ys = np.array([ex[1] for ex in examples])
        out = np.array([ex[2] for ex in examples])
        
        self._test_synthesis(xs, ys, out, "test_mirror_triangle")
    
    def test_rectangle_circle_subtraction(self):
        rect_x = np.array([0, 1, 2, 3, 0, 1.2, 2, 3  , 0, 1, 0, 0.9, ])
        rect_y = np.array([0, 0, 0, 0, 1, 1.2, 1, 0.9, 2, 2, 3, 3  , ])
        rect_out = np.array([True] * len(rect_x))

        circle_x, circle_y = circle_coords(3, 3, 1.9, n=10)
        circle_out = np.array([False] * len(circle_x))
        
        xs = np.concatenate([rect_x, circle_x])
        ys = np.concatenate([rect_y, circle_y])
        out = np.concatenate([rect_out, circle_out])
        
        self._test_synthesis(xs, ys, out, "rectangle_circle_subtraction")
    
    def test_circular_pie_triangle_cutoff(self):
        out_circle_x, out_circle_y = circle_coords(5, 5, 3.1, n=6)
        out_circle_labels = [False] * len(out_circle_y)

        inner_circle_x, inner_circle_y = circle_coords(5, 5, 2.9, n=6)
        inner_circle_labels = [False] + [True] * (len(inner_circle_y) - 1)

        aux_circle_x, aux_circle_y = circle_coords(5, 5, 1.5, n=6)
        aux_circle_labels = [False] + [True] * (len(aux_circle_y) - 1)

        cutoff_x, cutoff_y = [5.1, 6.1, 7.1], [5.0, 5.0, 5.0]
        cutoff_labels = [False] * len(cutoff_x)
        
        xs = np.concatenate([out_circle_x, inner_circle_x, aux_circle_x, cutoff_x])
        ys = np.concatenate([out_circle_y, inner_circle_y, aux_circle_y, cutoff_y])
        out = np.concatenate([out_circle_labels, inner_circle_labels, aux_circle_labels, cutoff_labels])
        
        self._test_synthesis(xs, ys, out, "circular_pie_triangle_cutoff")
    
    def test_ring(self):
        circle1_x, circle1_y = circle_coords(5, 5, 4.1, n=6)
        circle2_x, circle2_y = circle_coords(5, 5, 3.9, n=6)
        circle3_x, circle3_y = circle_coords(5, 5, 2.1, n=6)
        circle4_x, circle4_y = circle_coords(5, 5, 1.9, n=6)

        out1 = [False] * len(circle1_x)
        out2 = [True] * len(circle2_x)
        out3 = [True] * len(circle3_x)
        out4 = [False] * len(circle4_x) 

        xs = np.concatenate([circle1_x, circle2_x, circle3_x, circle4_x])
        ys = np.concatenate([circle1_y, circle2_y, circle3_y, circle4_y])
        out = np.concatenate([out1, out2, out3, out4])

        self._test_synthesis(xs, ys, out, "ring")
    
    def test_basic(self):
        xs = np.array([1.0, 5.0, 2.5])
        ys = np.array([1.0, 5.0, 2.5])
        out = np.array([True, True, False])
        
        self._test_synthesis(xs, ys, out, "basic_test")
    
    def test_single_circle(self):
        xs, ys, out = multi_circle_test([2], [3], [1])
        self._test_synthesis(xs, ys, out, "single_circle_test")
    
    def test_multi_circle(self):
        xs, ys, out = multi_circle_test([2, 5], [3, 5], [1, 2])
        self._test_synthesis(xs, ys, out, "multiple_circles_test")
    
    def test_half_circle(self):
        xs, ys, out = half_circle_test(2, 3, 1)
        self._test_synthesis(xs, ys, out, "half_circle_test")
    
    def test_shapes_on_both_sides(self):
        xs = np.array([1.0, 5.0, 5.0, 9.0])
        ys = np.array([9.0, 5.0, 5.0, 1.0])
        out = np.array([True, False, False, True])
        
        self._test_synthesis(xs, ys, out, "shapes_on_both_sides_test")
    
    def test_random_examples(self):
        # Reset seed before running random tests
        reset_random_seed()
        
        # Run 10 different random tests
        for i in range(1, 11):
            with self.subTest(iteration=i):
                xs, ys, out = random_test(i, 5)
                self._test_synthesis(xs, ys, out, f"random_test_{i}")
        
    def _test_synthesis(self, xs: np.ndarray, ys: np.ndarray, out: np.ndarray, test_name: str):
        """Helper method to test synthesis capabilities"""
        print(f"Synthesizing {test_name}...")

        # First, dump examples visualization before synthesis
        try:
            from shapes import ShapeVisualizer
            visualizer = ShapeVisualizer()
            # Create examples filename and path
            examples_filename = f"{test_name}_examples.png"
            examples_path = os.path.join(visualizer.output_dir, examples_filename)
            visualizer.visualize_examples(xs, ys, out, test_name, examples_path)
        except ImportError:
            print("Warning: ShapeVisualizer not available, skipping examples visualization")
        except Exception as e:
            print(f"Warning: Examples visualization failed: {e}")
        
        try:
            examples = list(zip(xs, ys, out))
            synthesizer = self.ShapeSynthesizer()
            prog = synthesizer.synthesize(examples, max_iterations=3)
            
            # Test that the synthesized program can interpret the examples and is correct
            result = prog.interpret(xs, ys)
            self.assertIsInstance(result, np.ndarray)
            self.assertEqual(result.dtype, bool)
            self.assertEqual((result == out).all(), True)

            print(f"Synthesized {test_name}: {prog}")
            
            # After successful synthesis, dump the synthesized program visualization
            try:
                if 'visualizer' not in locals():
                    from shapes import ShapeVisualizer
                    visualizer = ShapeVisualizer()
                
                # Create synthesized filename and path
                synthesized_filename = f"{test_name}_synthesized.png"
                synthesized_path = os.path.join(visualizer.output_dir, synthesized_filename)
                visualizer.visualize_synthesized(xs, ys, out, prog, test_name, synthesized_path)
                
            except Exception as e:
                print(f"Warning: Synthesized program visualization failed: {e}")
            
            # Close all plots to free memory
            try:
                if 'visualizer' in locals():
                    visualizer.close_all_plots()
            except Exception as e:
                print(f"Warning: Failed to close plots: {e}")
            
        except Exception as e:
            # Synthesis might fail, which is acceptable for some complex cases
            self.fail(f"Synthesis failed for {test_name}: {e}")

def reset_random_seed():
    """Reset random seed to ensure reproducible results"""
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

def circle_coords(x, y, r, n=6):
    """Generate n points around a circle with center (x, y) and radius r."""
    theta = np.linspace(0, 2 * np.pi, n+1)[:-1]
    xs = x + r * np.cos(theta)
    ys = y + r * np.sin(theta)
    return xs, ys

def single_circle_test(x, y, r, eps=0.1):
    """Generate test points for a single circle."""
    xs_true, ys_true = circle_coords(x, y, r * (1 - eps))
    xs_false, ys_false = circle_coords(x, y, r * (1 + eps))
    
    xs = np.concatenate([xs_true, xs_false])
    ys = np.concatenate([ys_true, ys_false])
    out = np.concatenate([
        np.full(len(xs_true), True),
        np.full(len(xs_false), False)
    ])
    
    return xs, ys, out

def half_circle_test(x, y, r, eps=0.1):
    """Generate test points for a half circle (right half only)."""
    xs_true, ys_true = circle_coords(x, y, r * (1 - eps), 12)
    xs_false, ys_false = circle_coords(x, y, r * (1 + eps), 12)
    
    xs = np.concatenate([xs_true, xs_false])
    ys = np.concatenate([ys_true, ys_false])
    out = np.concatenate([
        np.full(len(xs_true), True),
        np.full(len(xs_false), False)
    ])
    
    out[xs < x] = False
    return xs, ys, out

def multi_circle_test(xs, ys, rs):
    """Generate test points for multiple circles."""
    xs_out, ys_out, out = [], [], []
    
    for i in range(len(xs)):
        x, y, r = xs[i], ys[i], rs[i]
        xs_true, ys_true = circle_coords(x, y, r * (1 - 0.1))
        xs_false, ys_false = circle_coords(x, y, r * (1 + 0.1))
        
        xs_out.extend(xs_true)
        ys_out.extend(ys_true)
        out.extend([True] * len(xs_true))
        
        xs_out.extend(xs_false)
        ys_out.extend(ys_false)
        out.extend([False] * len(xs_false))
    
    return np.array(xs_out), np.array(ys_out), np.array(out)

def random_test(seed, amount, max_coord=9):
    """Generate random test points for synthesis."""
    # Create a separate random instance to avoid affecting global state
    local_random = random.Random(seed)
    xs = [local_random.uniform(0, max_coord) for _ in range(amount)]
    ys = [local_random.uniform(0, max_coord) for _ in range(amount)]
    out = [local_random.choice([True, False]) for _ in range(amount)]
    return np.array(xs), np.array(ys), np.array(out)

if __name__ == "__main__":
    unittest.main()
