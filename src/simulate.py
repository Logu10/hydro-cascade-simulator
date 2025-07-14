import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Simple reservoir & plant simulation logic for demo
def run(flow, plants):
    for plant in plants:
        plant['storage'] = []
        plant['power'] = []
        plant['capacity'] = plant.get('capacity', 1_000_000)  # m³, example capacity
        plant['storage_current'] = plant['capacity'] * 0.5  # start at 50% full

    for _, row in flow.iterrows():
        q_in = row['flow']  # inflow in m³/s
        for plant in plants:
            # Update storage with inflow (simplified logic)
            plant['storage_current'] += q_in * 3600  # inflow per hour (m³)
            if plant['storage_current'] > plant['capacity']:
                plant['storage_current'] = plant['capacity']  # spill overflow
            
            # Calculate power output: P = ρghQη
            # ρ = 1000 kg/m³, g = 9.81 m/s², h = head height in meters (example 100m), η = efficiency (0.9)
            rho = 1000
            g = 9.81
            h = plant.get('head', 100)
            eta = 0.9

            # Turbine flow = min(storage outflow capacity, storage_current)
            turbine_flow = min(q_in, plant['storage_current'] / 3600)  # m³/s based on storage
            power = rho * g * h * turbine_flow * eta / 1e6  # MW

            # Update storage after turbine discharge
            plant['storage_current'] -= turbine_flow * 3600
            if plant['storage_current'] < 0:
                plant['storage_current'] = 0

            # Record current storage and power output
            plant['storage'].append(plant['storage_current'])
            plant['power'].append(power)

            # The outflow of this plant is inflow for the next
            q_in = turbine_flow

def plot_power(plants, flow):
    dates = flow['date']
    plt.figure(figsize=(16, 8))

    for plant in plants:
        plt.plot(dates, plant['power'], label=f"{plant['name']} Power (MW)")
    total_power = np.sum([p['power'] for p in plants], axis=0)
    plt.plot(dates, total_power, 'k--', label='Total Power', linewidth=2)

    total_power_series = pd.Series(total_power, index=dates)
    rolling_avg = total_power_series.rolling(window=7, min_periods=1).mean()
    plt.plot(dates, rolling_avg, 'r-', label='7-Day Rolling Avg (Total Power)')

    plt.title("Hydropower Generation Over Time")
    plt.xlabel("Date")
    plt.ylabel("Power (MW)")
    plt.legend()
    plt.grid(True)

    os.makedirs('../plots', exist_ok=True)
    plt.savefig('../plots/power.png')
    plt.close()

def plot_storage(plants, flow):
    dates = flow['date']
    plt.figure(figsize=(16, 8))

    for plant in plants:
        storage_pct = 100 * np.array(plant['storage']) / plant['capacity']
        plt.plot(dates, storage_pct, label=f"{plant['name']} Storage (%)")

    plt.fill_between(dates, 20, 80, color='lightblue', alpha=0.1, label='Operational range (20%-80%)')
    plt.axhline(20, color='r', linestyle='--', alpha=0.7)
    plt.axhline(80, color='g', linestyle='--', alpha=0.7)

    plt.title("Reservoir Storage Level Over Time")
    plt.xlabel("Date")
    plt.ylabel("Storage (% of Capacity)")
    plt.ylim(0, 110)
    plt.grid(True)
    plt.legend()

    os.makedirs('../plots', exist_ok=True)
    plt.savefig('../plots/storage.png')
    plt.close()

def main():
    # Read flow data
    flow = pd.read_csv('../data/flow.csv', parse_dates=['date'])

    # Define cascade plants (example with 3 plants)
    plants = [
        {'name': 'Plant A', 'capacity': 2_000_000, 'head': 120},
        {'name': 'Plant B', 'capacity': 1_500_000, 'head': 90},
        {'name': 'Plant C', 'capacity': 1_000_000, 'head': 70},
    ]

    run(flow, plants)
    plot_power(plants, flow)
    plot_storage(plants, flow)

if __name__ == '__main__':
    main()
