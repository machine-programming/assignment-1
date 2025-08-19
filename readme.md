# EN.601.727 Machine Programming - Assignment 1

🎉 Welcome to your very first assignment in Machine Programming!

In this journey, you’ll get your hands dirty with inductive program synthesis, starting with a bottom-up synthesizer, and ending with a taste of LLM-powered synthesis.
Think of it as teaching a machine how to invent programs from scratch, and then inviting an AI assistant to join the fun.

### ✨ Structure

This assignment has three interconnected parts that gradually build on one another:

- **Shapes DSL (Warm-up with Geometry)**
  Explore a small domain-specific language (DSL) for geometric shapes. You’ll implement a bottom-up synthesizer that automatically generates shape expressions based on positive and negative coordinates.
- **Strings DSL (From Shapes to Strings)**
  Design a DSL for string manipulation—your own mini “string toolkit.” Then, reuse (and slightly adapt) your synthesizer from Part 1 to automatically generate string-processing programs.
- **LLM-Assisted Synthesis (Humans + Machines)**
  Put a large language model (LLM) to work! Using the DSL you designed in Part 2, craft prompts that guide the LLM to synthesize string manipulation programs. Then, analyze what it gets right—and where it stumbles.

### 📦 Deliverables and Submission

You will implement several key functions for each part:

- **Part 1: Bottom-up Synthesis for Shapes**
  - `shape_synthesizer.py`: `grow()`
  - `enumerative_synthesis.py`: `eliminate_equivalents()`
  - `enumerative_synthesis.py`: `synthesize()`
- **Part 2: Bottom-up Synthesis for Strings**
  - `strings.py`: (add your new string operations)
  - `string_synthesizer.py`: `grow()`
- **Part 3: LLM Synthesis for Strings**
  - `llm_string_synthesizer.py`: `generate_prompt()`
  - `llm_string_synthesizer.py`: `extract_program()`

### 📌 Grading criteria:

- **Parts 1 & 2**: Autograded. Full credit if you pass all tests within 30 minutes of runtime.
  (Hint: the reference solution runs most tasks in <1s, hardest ones in <10s.)
- **Part 3**: Graded manually. Your LLM must solve at least 60% of test cases.
  Upload your llm_synthesis_report.json with all prompts/responses—it’s your proof of work.

For Gradescope submission, zip the following 6 (or 7) files:
- `strings.py`
- `enumerative_synthesis.py`
- `shape_synthesizer.py`
- `string_synthesizer.py`
- `llm_string_synthesizer.py`
- `llm_synthesis_report.json`
- (Optional) `readme.md` — for notes, acknowledgements, and AI/collaboration credits.

### 🤝 Collaboration Policy

You are encouraged to discuss ideas with peers.
Do not copy code directly.
Implement your own solution.
If you collaborate (e.g., pair programming, brainstorming), credit your collaborators clearly in your `readme.md`.

### 🤖 Using AI in This Assignment

This is a Machine Programming course—of course you can use LLMs!
LLMs can be great debugging partners, but they won’t give you a working solution right away.
Prompt iteratively, and show that you understand the synthesis algorithms.
Save interesting prompts + responses, and include them in your `readme.md`.
Be explicit about which model you used.

### 🔑 LLM API Key for Part 3

We’ll provide each of you with a Google Gemini API key for Part 3.
The key is for this course only.
Please do not share it, especially outside of the class.
Typical usage for this assignment should not exceed $10.
Excessive usage will be monitored, and we may revoke keys if abused.

### 🧭 Integrity Guidelines

- **Parts 1 & 2**: It’s fine to add smart heuristics in your DSL or synthesizer, but don’t hardcode answers to test cases—that defeats the purpose.
- **Part 3**: Don’t fake the LLM’s output in your `.json` report. Both successes and failures are valuable learning outcomes in this course.

### 📚 Reference

The design of the synthesizer and the Shape DSL is adapted from [PSET1](https://people.csail.mit.edu/asolar/SynthesisCourse/Assignment1.htm) in MIT’s [Introduction to Program Synthesis](https://people.csail.mit.edu/asolar/SynthesisCourse/index.htm), taught by [Prof. Armando Solar-Lezama](https://people.csail.mit.edu/asolar/).

# 🚀 Part 0: Setting Up

First things first—let’s get your environment ready.

1. **Clone the repository**

   ```bash
   git clone https://github.com/machine-programming/assignment-1
   ```

2. **Move into the assignment directory, create virtual environments, and install dependencies**

   ```bash
   cd assignment-1
   python -m venv .venv # creating a virtual environment for this assignment
   source .venv/bin/activate # change this to other activate scripts if you use shells like fish
   pip install -r requirements.txt # install the dependencies
   ```

3. **Test your setup (don’t panic if it fails!)**

   ```bash
   python test_part1.py
   ```

   You should see the tests run but **all of them fail**.
   ✅ That’s exactly what we expect. Your job in Part 1 is to turn those failures into passes!


# 🎨 Part 1: Bottom-up Synthesis for Shapes

![ring-synthesized](docs/ring_synthesized.png)

In this part, we’ll explore a Domain-Specific Language (DSL) for shapes.
This DSL gives you a palette of basic shapes (rectangle, triangle, circle) and shape operations (union, intersection, mirror, subtraction).

At its core, a shape $f$ is just a boolean function:

$$f(x, y) \mapsto \texttt{true}~|~\texttt{false}$$

- `true` means that point $(x, y)$ falls within the shape $f$,
- `false` means that the point $(x, y)$ falls outside of the shape $f$.

### 🎯 Goal of synthesis

Given a set of points with positive/negative labels (`List[Tuple[float, float, bool]]`), synthesize a shape program such that:
- All positive points fall inside the shape
- All negative points stay outside

The image above shows an example with 12 positive and 12 negative points.
The expected synthesized program was `Subtraction(Circle(5,5,4), Circle(5,5,2))`, which produces a ring.

### 🧪 Running the Synthesizer on Test Cases

To actually apply your synthesizer to the provided test cases, run:
```
python test_part1.py
```
- At the beginning: you should see synthesis failures (don’t worry—that’s expected).
- A new folder called `shape_visualization/` will be created. Inside, you’ll find:
  - Visualization of examples: e.g., `ring_examples.png` (positive/negative coordinates)
  - Visualization of synthesized program: e.g., `ring_synthesized.png` which is the same as the image above
- If a test case fails, you’ll only see the examples file (no synthesized visualization).
- Use these visualizations to get an intuition for what kind of program your synthesizer should be generating.

Once you complete Part 1, rerun this test—you should start seeing synthesized shapes that match the examples.
It’s also helpful to peek at test_part1.py to see the full set of test cases.

### 🧩 Understanding the DSL

Shapes are implemented in shapes.py.
The base class is `Shape`, which all concrete shapes inherit from.
Each shape must implement the method `interpret(xs, ys)`, which takes two numpy arrays (`x` and `y` coordinates) and returns a boolean array.

Example: the `Circle` class inherits from `Shape`:

``` python
class Circle(Shape):
    def interpret(self, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
        return ((xs - self.center.x)**2 + (ys - self.center.y)**2) <= self.radius**2
```

The `interpret` function computes whether each coordinate lies inside the circle (using vectorized numpy operations for speed).

### 📜 Formal DSL Syntax

```
Shape ::= Circle(center: Coordinate, radius: int)
        | Rectangle(bottom_left: Coordinate, top_right: Coordinate)
        | Triangle(bottom_left: Coordinate, top_right: Coordinate)   # right triangle only
        | Mirror(Shape)  # across line y=x
        | Union(Shape, Shape)
        | Intersection(Shape, Shape)
        | Subtraction(Shape, Shape)
```

- **Terminals**: `Circle`, `Rectangle`, `Triangle` (with fixed parameters)
- **Operators**: `Mirror`, `Union`, `Intersection`, `Subtraction`

### 🔨 Part 1(a). Growing Shapes

Time to roll up your sleeves! Head to `shape_synthesizer.py` and open the `ShapeSynthesizer` class.
This synthesizer inherits from `BottomUpSynthesizer` but specializes in shapes.
Your task is to implement `grow()`, which:

- Takes a current set of shape programs.
- Applies shape operators (union, subtraction, etc.) to generate new programs one level deeper.
- Returns a set that includes both the original programs and the newly grown ones.

Once implemented, your `grow()` function will be the engine that drives bottom-up search over the DSL, which step by step builds increasingly complex shapes.

``` python
def grow(
    self,
    program_list: List[Shape],
    examples: List[Tuple[float, float, bool]]
) -> List[Shape]:
```

> 💡 **Hints & Tips**
> - Symmetry/commutativity:
>   Some operations (e.g., `Union(A, B) = Union(B, A)`) generate duplicate programs if you’re not careful. Add checks to prune equivalent programs.
> - Progress tracking:
>   When you start generating large numbers of programs, visualization helps. Use `tqdm` to show a progress bar and keep your sanity.

### 🔨 Part 1(b). Eliminating (Observationally) Equivalent Shapes

Now that you can **grow** shapes, the next challenge is to keep your search space from exploding.
For this, we’ll turn to the more general `BottomUpSynthesizer` (in `enumerative_synthesis.py`) and implement a pruning step: **eliminating observationally equivalent programs**.

Two programs are **observationally equivalent** if they produce the **same outputs** on the **same inputs**. For example, look at these two programs:
* `Union(Circle(center=(0,0), r=1), Circle(center=(0,0), r=1))`
* `Circle(center=(0,0), r=1)`
These two programs are *different syntactically* but *indistinguishable observationally* (their outputs match on all test points).

Your job is to filter out duplicates like these so the synthesizer only keeps *unique behaviors*. Please implement the `eliminate_equivalents` function:

```python
def eliminate_equivalents(
    self,
    program_list: List[T],
    test_inputs: List[Any],
    cache: Dict[T, Any],
    iteration: int
) -> Generator[T, None, Dict[T, Any]]:
```

* **`program_list`**: candidate programs to check
* **`test_inputs`**: inputs on which programs will be interpreted
* **`cache`**: a dictionary (`Dict[T, Any]`) mapping each program → its output signature (so you don’t recompute unnecessarily)
* **`iteration`**: current synthesis round (useful for debugging/logging)
* **Return**: a **generator** that yields only the *observationally unique* programs

> 💡 Hints & Tips
> - Use the provided `compute_signature()` method (already implemented) to evaluate programs and produce signatures. These signatures will be your deduplication keys.
> - Keep track of which signatures you’ve already seen using `Set` or `Dict`.
> Be careful: different programs may map to the *same* signature—yield only the first and discard the rest.
> - **Important**: use `yield` instead of returning a list. This way, the synthesizer can stop early if it finds a successful program before exhausting the search space.
> - The `cache` is your friend: store previously computed outputs there to save time when the same program shows up again.

### 🔨 Part 1(c). Bottom-up Synthesizing Shapes

Now is the time to take all that we have already and iteratively synthesize shapes.




# Part 2: Bottom-up Synthesis for Strings



# Part 3: LLM Synthesis for Strings
