# Sport plots

### Football

__code example:__
```python
import numpy as np

postions = np.array([
    (0.02, 0.53),
    
    (0.24, 0.15),
    (0.2, 0.38),
    (0.2, 0.65),
    (0.26, 0.85),

    (0.35, 0.5),
    (0.40, 0.25),
    (0.40, 0.75),
    
    (0.5, 0.50),
    (0.5, 0.46),
    (0.5, 0.8),
])

names = [
    'Donnarumma',

    'Hakimi',
    'Kimpembe',
    'Marquinhos',
    'Bernat',

    'Verratti',
    'Sanches',
    'Vitinha',

    'Messi',
    'Neymar',
    'Mbappe'
]

colors = [
    'orange',

    'red',
    'red',
    'red',
    'red',
    
    'blue',
    'blue',
    'blue',
    
    '#aa0bff',
    '#aa0bff',
    '#aa0bff'
]

from src import FootballPitch

fp = FootballPitch('red', 'darkgreen', textcolor='white')
fp.plot(postions, names, colors)
```
__plot example:__

<img src="./plots/football.png" />