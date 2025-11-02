This project presents a fully modular interactive evolution simulation implemented in Python, modeling ecological and evolutionary processes via individual, trait-driven organisms within a spatially explicit environment. The ecosystem unfolds on a two-dimensional grid spanning coordinates 0–1000 on both axes, creating a dynamic setting where autonomous organisms and food resources coexist and interact under realistic biological and ecological constraints.

Organism Traits and Behavior:
Each organism is characterized by spatial coordinates (pos_x, pos_y) and biological traits including:
Speed: controls movement rate.
Size: influences energy capacity and survival trade-offs.
Energy: variable resource pool for survival and reproduction.
Health: vitality decreasing with low energy.
Sensory range: radius within which organisms detect food.
Min reproduction energy threshold: minimum energy required to reproduce.
Energy transfer ratio: fraction of parent energy transferred to offspring.

Traits evolve through random Gaussian mutations applied during reproduction, driving phenotypic diversity and natural selection.

Organisms’ behavioral decisions are encapsulated within a per-organism step() method, defining their life cycle at each simulation tick. Behavior includes:
Perception of food within sensory range.
Purposeful movement toward detected food with optional zig-zag pattern for realism.
Random wandering using cardinal directions, also supporting zig-zag movement.
Energy-based decision to reproduce, transferring a portion of energy to the offspring.
Energy cost computations scaling with speed and size, with health degradation under energy scarcity.
Death triggered by critically low health or energy.

Food Resources:
Food items are implemented as objects with spatial coordinates and discrete energy values contributing to organism energy upon consumption. Food regenerate periodically via a manager class distributing new resources randomly, introducing spatial and temporal heterogeneity.

Simulation Parameters:
Grid Size: 1000×1000 spatial units.
Initial Population: 120 organisms, identical initial traits but randomized start positions.
Trait Mutation Rate: 0.02 (2% standard deviation Gaussian noise applied to inherited traits).

Initial Organism Traits:
Speed: 3.5 units/tick
Size: 10 units
Sensory Range: 40 units
Energy: 150 units
Health: 90 units
Minimum reproduction energy: 50% of max energy (derived from size^2 × 35)
Energy transfer ratio: 0.5 (50% energy passed to offspring)

Food Initial Count: 500 units distributed randomly.
Food Respawn Rate: 40 units every 14 simulation steps.

Simulation Step Rate (FPS cap): 30 frames per second.

Graphical User Interface:
Implemented with pygame and matplotlib, the GUI includes:
Left Panel: Displays spatial distributions of organisms (blue circles scaled by size) and food (green dots).
Right Panel: Features large histograms tracking distributions of speed, size, and max energy traits updating every frame.
Numeric Counters: Real-time display of simulation step count, number of living organisms, and food items at the top right.
The window resolution is configured as 1400×1000 pixels to accommodate grid plus histogram and counters area.

Code Structure and Modules:
src/organism.py: Defines the Organism class with traits, mutation, and comprehensive behavior logic within the step() method including movement, energy update, reproduction, and death condition.
src/food.py: Implements Food class for resource units and FoodManager for food spawning and regeneration.
src/gui.py: Contains all rendering logic: drawing grid, organisms, food items, histograms, and counters.
src/simulation.py: Orchestrates simulation loop, manages population and food lifecycle, integrates GUI, and controls timestep pacing.
main/main.py: Launches the simulation by initializing EvolutionSimulation object and executing its run loop.

Environment Setup:
Python 3.10+ recommended.
Virtual environment created with: python -m venv venv

Activate environment:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

Required Python packages installed from requirements.txt:
numpy
pygame
matplotlib
Pillow

Run simulation with python main.py

Usage and Extensibility:
The project supports experimentation by tuning:
Mutation rates
Initial population size
Trait thresholds (reproduction energy, transfer ratios)
Food regeneration parameters
Movement patterns (toggle zig-zag)

Its modular design enables integration of additional ecological phenomena such as predation, resource competition, or AI-based behavior modules.


Steps to Run:

python -m venv venv

venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

python main.py


git init
git config --global user.name "Jane Doe"
git config --global user.email "jane.doe@example.com"