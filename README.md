# Sport plots

## Installation

__Requires Python >=3.6.1__

`pip install git+https://github.com/seppedelanghe/sports-plots.git`

## Football

__Name:__ FootballPitch <br>
__Options:__
- Custom colors
    - Background
    - Players
    - Links
    - Text color

- Plots
    - Position plot
    - Link plots

- Plot options:
    - Custom dot size

- Output
    - Matplotlib
    - Image
    - Numpy

### example
```python
import numpy as np

# positions in X and Y coordinates between 0 and 1
positions = np.array([
    (0.02, 0.53), # GK
    (0.24, 0.15), (0.2, 0.38), (0.2, 0.65), (0.26, 0.85), # Defenders
    (0.35, 0.5), (0.40, 0.25), (0.40, 0.75), # Midfielders
    (0.5, 0.50), (0.5, 0.46), (0.5, 0.8), # Attackers
])

# set player names (optional)
names = [
    'Donnarumma',
    'Hakimi', 'Kimpembe', 'Marquinhos', 'Bernat',
    'Verratti', 'Sanches', 'Vitinha',
    'Messi', 'Neymar', 'Mbappe'
]

# add custom colors (optional)
colors = [
    'orange',
    'red', 'red', 'red', 'red',
    'blue', 'blue', 'blue',
    '#aa0bff', '#aa0bff', '#aa0bff'
]

from src import FootballPitch

# init FootballPitch
fp = FootballPitch(
    playerscolor='red', 
    bg='darkgreen', 
    textcolor='white')

# plot
fp.plot(positions, names, colors)

# show plot
fp.show()

# save as image
fp.save('./plot.png')

# convert plot to numpy array image (RGB)
out = fp.to_numpy()

# Close matplotlib figure
fp.close()
```

# Plots

## Positions 
__This is the output of the example code:__
<img src="./plots/football.png" />
<br>

## Links
__plot links between players with custom dotsize and link colors:__
<img src="./plots/links.png" />