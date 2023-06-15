# Streamlit-Game-of-Life
This is a Streamlit application that simulates Conway's Game of Life on both square and hexagonal grids.

# Conway's Game of Life with Streamlit

This is a Python application using [Streamlit](https://streamlit.io) to simulate Conway's Game of Life, a cellular automaton devised by mathematician John Horton Conway. This implementation supports both square and hexagonal grids.

The game evolves in real-time and you can control various parameters like the grid size, live cell density, and frame update speed. You can also select survival and birth rules, and choose colors for the live and dead cells.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This project requires Python 3.6 or above. You also need the following Python packages:

- Streamlit
- Numpy
- Matplotlib
- Scipy

### Installing

First, clone the repository to your local machine:

```bash
git clone https://github.com/your_username/your_repo.git

Navigate to the project folder:
cd your_repo

Install the required dependencies:
pip install -r requirements.txt

Finally, run the Streamlit application:
streamlit run game_of_life.py

**Please replace `your_username` and `your_repo` with your actual GitHub username and the name of your repository. If you choose a different license, be sure to update the License section accordingly.**

Usage
The control panel is located in the left sidebar. You can pause/resume the simulation, reset it, or manually step it forward. Experiment with different configurations and observe the results! Or so that would happen if everything worked as expected, button's don't really work, feel free to figure out why and put in PR!

License
This project is licensed under the MIT License

Acknowledgments
John Horton Conway, for inventing the Game of Life.
The Streamlit team, for their awesome app framework.
ChatGPT, for providing all of the debugging help.
