# Cell_EnvironmentV2
## Summary
This package aims to create a computationally modeled environment for cellular behavior. The main file is `source/run_simulation.py` and can be imported via python and run via the main method `run_simulation()`. Package can also be run via the command line interface through `python -c "from source.run_simulation import run_simulation; run_simulation()"`.

Files needed for this package and reproducibility are within the `reproducibility/` folder, and detailed directory structure follows.
## Directory Structure
- `source`: all source files needed to run the program
- `tests`: unittests for the source files
- `reproducibility`: YAML and TXT files needed to utilize the program