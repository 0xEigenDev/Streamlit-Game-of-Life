import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.signal import convolve2d
import time
from matplotlib.patches import RegularPolygon

class GameOfLife:
    def __init__(self, grid_size, live_cell_density, live_rules, birth_rules, grid_type):
        self.grid = self.random_initial_config(grid_size, live_cell_density)
        self.live_rules = live_rules
        self.birth_rules = birth_rules
        self.grid_type = grid_type
        self.kernel = self.generate_kernel(grid_type)

    def random_initial_config(self, grid_size, live_cell_density):
        grid = np.random.choice([0, 1], size=(grid_size, grid_size), p=[1 - live_cell_density, live_cell_density])
        return grid

    def generate_kernel(self, tiling_type):
        if tiling_type == 'square':
            return np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        elif tiling_type == 'hexagonal':
            return np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        else:
            raise ValueError(f"Unsupported tiling type: {tiling_type}")

    def update_grid(self):
        num_neighbors = convolve2d(self.grid, self.kernel, mode='same', boundary='wrap' if self.grid_type == 'square' else 'fill', fillvalue=0)
        live = np.isin(num_neighbors, self.live_rules) & (self.grid == 1)
        born = np.isin(num_neighbors, self.birth_rules) & (self.grid == 0)
        self.grid = (live | born).astype(int)

class SimulationParameters:
    def __init__(self):
        self.params = self.setup_simulation_parameters()

    def setup_simulation_parameters(self):
        st.sidebar.header('Configuration')
        params = {
            'grid_type': st.sidebar.selectbox("Select grid type", ['square', 'hexagonal']),
            'grid_size': st.sidebar.slider("Select grid size", 10, 100, 50),
            'live_cell_density': st.sidebar.slider("Select initial live cell density", 0.0, 1.0, 0.5, 0.01),
            'frame_update_speed': st.sidebar.slider("Select frame update speed (ms)", 50, 1000, 200),
            'on_color': st.sidebar.color_picker('Pick a color for live cells', '#ffffff'),
            'off_color': st.sidebar.color_picker('Pick a color for dead cells', '#000000'),
            'live_rules': st.sidebar.multiselect("Survival rules", range(9), (2, 3)),
            'birth_rules': st.sidebar.multiselect("Birth rules", range(9), (3,))
        }
        return params

class SimulationControls:
    def __init__(self):
        self.controls = self.setup_simulation_controls()

    def setup_simulation_controls(self):
        st.sidebar.header('Simulation Controls')
        controls = {
            'is_paused': st.sidebar.button('Play/Pause'),
            'reset': st.sidebar.button('Reset'),
            'step': st.sidebar.button('Step')
        }
        return controls

class HexGrid:
    def __init__(self, grid, on_color, off_color):
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-0.55, len(grid) - 0.45)
        self.ax.set_ylim(-0.55, len(grid) - 0.45)
        self.ax.axis('off')
        self.hexagons = np.empty(grid.shape, dtype=object)
        for (i, j), val in np.ndenumerate(grid):
            color = on_color if val else off_color
            offset = 0 if j % 2 == 0 else 0.5
            hexagon = RegularPolygon((j, i + offset), numVertices=6, radius=0.5*np.sqrt(2 / 3), facecolor=color, edgecolor=color)
            self.hexagons[i, j] = hexagon
            self.ax.add_patch(hexagon)

    def update_colors(self, grid, on_color, off_color):
        for (i, j), val in np.ndenumerate(grid):
            color = on_color if val else off_color
            self.hexagons[i, j].set_facecolor(color)
            self.hexagons[i, j].set_edgecolor(color)

def create_figure(grid, on_color, off_color, grid_type):
    if grid_type == 'square':
        c_map = colors.ListedColormap([off_color, on_color])
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(grid, cmap=c_map)
        ax.axis('off')
        return fig, ax, None
    else:
        hex_grid = HexGrid(grid, on_color, off_color)
        return hex_grid.fig, hex_grid.ax, hex_grid

def run_simulation():
    params, controls, game = setup_simulation()
    fig, ax, hex_grid = create_figure(game.grid, params.params['on_color'], params.params['off_color'], params.params['grid_type'])
    while True:
        if controls.controls['is_paused']:
            if controls.controls['reset']:
                st.experimental_rerun()
            if not controls.controls['step']:
                time.sleep(0.1)
                continue
        game.update_grid()
        if hex_grid is not None:
            hex_grid.update_colors(game.grid, params.params['on_color'], params.params['off_color'])
        else:
            ax.imshow(game.grid, cmap=colors.ListedColormap([params.params['off_color'], params.params['on_color']]))
        st.pyplot(fig)
        time.sleep(params.params['frame_update_speed'] / 1000)
        st.experimental_rerun()

def setup_simulation():
    params = SimulationParameters()
    controls = SimulationControls()
    game = GameOfLife(params.params['grid_size'], params.params['live_cell_density'], params.params['live_rules'], params.params['birth_rules'], params.params['grid_type'])
    return params, controls, game

if __name__ == "__main__":
    st.title('Conway\'s Game of Life')
    run_simulation()
