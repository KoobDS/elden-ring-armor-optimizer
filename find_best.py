import pandas as pd
from itertools import product
import time

# 1. Load the cleaned dataset
df = pd.read_csv("data/Clean.csv")

# 2. Separate armor by slot
slot_categories = ["Helm", "Chest", "Gauntlets", "Legs"]
armor_by_slot = {slot: df[df["Slot"] == slot].copy() for slot in slot_categories}

# Define Method Selection
METHOD = "3"  # Change to method, options: "1", "1b", "2", "2b", "3", "3b"

start_time = time.time() # to track runtime

# --------------------------------------------------
# Method 1: Lowest weight combination with 51+ Poise
# --------------------------------------------------
if METHOD in ["1", "1b"]:
    best_combos = []
    best_weight = float("inf")

    # Filter for base game items if using 1b
    if METHOD == "1b":
        for slot in slot_categories:
            armor_by_slot[slot] = armor_by_slot[slot][armor_by_slot[slot]["DLC"] == 0]

    # Prepare lists for combinations (including None for skipping a slot)
    helm_list = [None] + list(armor_by_slot["Helm"].to_dict("records"))
    chest_list = [None] + list(armor_by_slot["Chest"].to_dict("records"))
    gaunt_list = [None] + list(armor_by_slot["Gauntlets"].to_dict("records"))
    legs_list = [None] + list(armor_by_slot["Legs"].to_dict("records"))

    count = 0
    for helm, chest, gaunt, legs in product(helm_list, chest_list, gaunt_list, legs_list):
        chosen = [x for x in (helm, chest, gaunt, legs) if x is not None]
        if len(chosen) < 2:
            continue

        total_poise = sum(item["Poise"] for item in chosen)
        if total_poise < 51:
            continue

        total_weight = sum(item["Weight"] for item in chosen)
        
        if total_weight < best_weight:
            best_weight = total_weight
            best_combos = [chosen]
        elif total_weight == best_weight:
            best_combos.append(chosen)

        count += 1

    end_time = time.time()
    
    # Print Results
    if best_combos:
        print(f"Best combos found (Weight: {best_weight:.1f}, Poise: {sum(i['Poise'] for i in best_combos[0]):.1f}) in {end_time - start_time:.2f} seconds")
        for combo in best_combos:
            print("---")
            for item in combo:
                print(f"  - {item['Name']} ({item['Slot']}) Weight={item['Weight']} Poise={item['Poise']}")
    else:
        print(f"No valid combination found in {end_time - start_time:.2f} seconds.")

# --------------------------------------------------------
# Method 2: Highest total Power combination with 51+ poise
# --------------------------------------------------------
elif METHOD in ["2", "2b"]:
    if METHOD == "2b":
        df = df[df["DLC"] == 0]

    best_per_slot = {
        slot: df[df["Slot"] == slot].nlargest(1, "Power").iloc[0]
        for slot in slot_categories
    }

    total_weight = sum(best_per_slot[slot]["Weight"] for slot in slot_categories)
    total_poise = sum(best_per_slot[slot]["Poise"] for slot in slot_categories)
    total_power = sum(best_per_slot[slot]["Power"] for slot in slot_categories)
    end_time = time.time()

    if total_poise >= 51:
        print(f"Best Power Score Combo (Weight: {total_weight:.1f}, Poise: {total_poise}, Power: {total_power}) in {end_time - start_time:.2f} seconds")
        for slot, item in best_per_slot.items():
            print(f"  - {item['Name']} ({slot}) Power={item['Power']:.1f}")
    else:
        print(f"No valid combination found in {end_time - start_time:.2f} seconds.")

# ------------------------------------------------
# Method 3: Best Power/Weight Ratio with 51+ Poise
# ------------------------------------------------
elif METHOD in ["3", "3b"]:
    best_ratio = 0
    best_combos = []

    if METHOD == "3b":
        df = df[df["DLC"] == 0]

    df = df[df["Power"] > 0] # This is an optimization that reduces runtime by 12% when unavailable datasets are also removed

    helms = df[df["Slot"] == "Helm"]
    chests = df[df["Slot"] == "Chest"]
    gauntlets = df[df["Slot"] == "Gauntlets"]
    legs = df[df["Slot"] == "Legs"]

    for helm, chest, gauntlet, leg in product(helms.iterrows(), chests.iterrows(), gauntlets.iterrows(), legs.iterrows()):
        helm, chest, gauntlet, leg = helm[1], chest[1], gauntlet[1], leg[1]

        total_weight = helm["Weight"] + chest["Weight"] + gauntlet["Weight"] + leg["Weight"]
        total_poise = helm["Poise"] + chest["Poise"] + gauntlet["Poise"] + leg["Poise"]
        total_power = helm["Power"] + chest["Power"] + gauntlet["Power"] + leg["Power"]

        if total_poise >= 51:
            power_weight_ratio = total_power / total_weight

            if power_weight_ratio > best_ratio:
                best_ratio = power_weight_ratio
                best_combos = [(helm, chest, gauntlet, leg)]
            elif power_weight_ratio == best_ratio:
                best_combos.append((helm, chest, gauntlet, leg))

    end_time = time.time()

    if best_combos:
        print(f"Best 4-Piece Armor Combinations (51+ Poise) with Highest Power/Weight Ratio: {best_ratio:.4f} in {end_time - start_time:.2f} seconds")
        for combo in best_combos:
            print("---")
            print(f"- Helm: {combo[0]['Name']}")
            print(f"- Chest: {combo[1]['Name']}")
            print(f"- Gauntlets: {combo[2]['Name']}")
            print(f"- Legs: {combo[3]['Name']}")
    else:
        print(f"No valid armor combination found with Poise >= 51 in {end_time - start_time:.2f} seconds.")
