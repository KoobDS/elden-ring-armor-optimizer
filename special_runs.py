"""

Templates for specific playthroughs, constrained by given pieces or weight maximums!

"""


import pandas as pd
from itertools import product


### 1. Rune Level 1 Challenge

"""
Find best Gauntlets + Legs for RL1 if Omensmirk Mask, Raptor Black Feathers already selected, with certain wgt constraint
"""

# Load the cleaned dataset
df = pd.read_csv("data/Clean.csv")

# Filter for base game only (DLC = 0) --also without this constraint
# df = df[df["DLC"] == 0]

# Filter gauntlets and legs separately
gauntlets = df[df["Slot"] == "Gauntlets"]
legs = df[df["Slot"] == "Legs"]

# Initialize tracking variables
best_combinations = []
best_power = 0

# Generate all gauntlet-leg armor combinations
for gauntlet, leg in product(gauntlets.iterrows(), legs.iterrows()):
    gauntlet, leg = gauntlet[1], leg[1]

    # Calculate total weight and poise **first**
    total_weight = gauntlet["Weight"] + leg["Weight"]
    total_poise = gauntlet["Poise"] + leg["Poise"]

    # **Check constraints early** (skip unnecessary calculations)
    if total_poise < 30 or total_weight > 20.6:
        continue

    # Now calculate total power only for valid combos
    total_power = gauntlet["Power"] + leg["Power"]

    # **Update best combinations (handling ties)**
    if total_power > best_power:
        best_power = total_power
        best_combinations = [(gauntlet, leg, total_weight, total_poise, total_power)]
    elif total_power == best_power:
        best_combinations.append((gauntlet, leg, total_weight, total_poise, total_power))

# Display results
if best_combinations:
    print("Best Base Game Gauntlet-Leg Combination(s) (>=30 Poise, <=20.6 Weight):")
    for gauntlet, leg, total_weight, total_poise, total_power in best_combinations:
        print(f"- Gauntlets: {gauntlet['Name']} (Weight: {gauntlet['Weight']}, Poise: {gauntlet['Poise']}, Power: {gauntlet['Power']})")
        print(f"- Legs: {leg['Name']} (Weight: {leg['Weight']}, Poise: {leg['Poise']}, Power: {leg['Power']})")
        print(f"Total Weight: {total_weight:.1f}, Total Poise: {total_poise}, Total Power: {total_power}")
        print("-" * 60)
else:
    print("No valid gauntlet-leg combination found that meets the criteria.")

"""
Results:
    Base Game: Bull-Goat Gauntlets, Tree Sentinel Greaves
    Full Game: Verdigris Gauntlets, Tree Sentinel Greaves
"""


### 2. Main Playthrough

"""
Find best Chest + Gauntlets + Legs if White Mask is already selected, no specific wgt constraint
"""

# Load full dataset
df = pd.read_csv("data/Clean.csv")

# Ensure White Mask exists
white_mask = df[(df["Slot"] == "Helm") & (df["Name"] == "White Mask")]
if white_mask.empty:
    raise ValueError("White Mask not found in dataset.")
white_mask = white_mask.iloc[0]

# Separate other slots
chests = df[df["Slot"] == "Chest"]
gauntlets = df[df["Slot"] == "Gauntlets"]
legs = df[df["Slot"] == "Legs"]

# Tracking best
best_combinations = []
best_ratio = 0

# Generate all combinations of 3 remaining pieces
for chest, gauntlet, leg in product(chests.iterrows(), gauntlets.iterrows(), legs.iterrows()):
    chest, gauntlet, leg = chest[1], gauntlet[1], leg[1]

    # Calculate totals

    total_poise = white_mask["Poise"] + chest["Poise"] + gauntlet["Poise"] + leg["Poise"]

    # Check Poise requirement early
    if total_poise < 51:
        continue

    total_power = white_mask["Power"] + chest["Power"] + gauntlet["Power"] + leg["Power"]
    total_weight = white_mask["Weight"] + chest["Weight"] + gauntlet["Weight"] + leg["Weight"]

    power_weight_ratio = total_power / total_weight

    # Track best
    if power_weight_ratio > best_ratio:
        best_ratio = power_weight_ratio
        best_combinations = [(white_mask, chest, gauntlet, leg, total_weight, total_poise, total_power, power_weight_ratio)]
    elif power_weight_ratio == best_ratio:
        best_combinations.append((white_mask, chest, gauntlet, leg, total_weight, total_poise, total_power, power_weight_ratio))

# Display results
if best_combinations:
    print("Best 4-Piece Armor Set(s) (51+ Poise, Power/Weight optimized) with White Mask:")
    for helm, chest, gauntlet, leg, weight, poise, power, ratio in best_combinations:
        print(f"- Helm: {helm['Name']} (Weight: {helm['Weight']}, Poise: {helm['Poise']}, Power: {helm['Power']})")
        print(f"- Chest: {chest['Name']} (Weight: {chest['Weight']}, Poise: {chest['Poise']}, Power: {chest['Power']})")
        print(f"- Gauntlets: {gauntlet['Name']} (Weight: {gauntlet['Weight']}, Poise: {gauntlet['Poise']}, Power: {gauntlet['Power']})")
        print(f"- Legs: {leg['Name']} (Weight: {leg['Weight']}, Poise: {leg['Poise']}, Power: {leg['Power']})")
        print(f"Total Weight: {weight:.2f}, Total Poise: {poise}, Total Power: {power:.2f}, Power/Weight Ratio: {ratio:.4f}")
        print("-" * 60)
else:
    print("No valid combination found with White Mask and 51+ poise.")

"""
Results:
    Crucible Tree Armor, Ascetic's Wrist Guards, Ronin's Greaves
"""