# Hydro Cascade Simulator

Advanced hydropower cascade model with real inflow and reservoir storage.

## Setup

```bash
pip install -r requirements.txt
```

## Data fetching

```python
from src.fetch_flow import fetch_usgs_flow
df = fetch_usgs_flow('06090800', '2023-01-01', '2023-12-31')
df.to_csv('data/flow.csv', index=False)
```

## Run simulation

```bash
python src/simulate.py
```

## Visuals

- `plots/power.png`: daily power per plant
- `plots/storage.png`: reservoir storage trends
