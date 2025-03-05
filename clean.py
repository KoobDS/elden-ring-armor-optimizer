import pandas as pd
import ast
import numpy as np


# 1. Load the CSV file
file_path = "data/Raw.csv"
df = pd.read_csv(file_path)


# 2. Define mappings for Damage_Negation and Resistance keys
damage_key_map = {
    'Phy': 'Physical',
    'VS Str.': 'Strike',
    'VS Str': 'Strike',
    'VS Sla.': 'Slash',
    'VS Sla': 'Slash',
    'VS Pie.': 'Pierce',
    'VS Pie': 'Pierce',
    'Mag': 'Magic',
    'Fir': 'Fire',
    'Lit': 'Lightning',
    'Hol': 'Holy'
}

resist_key_map = {
    'Imm.': 'Immunity',
    'Imm': 'Immunity',
    'Rob.': 'Robustness',
    'Robu.': 'Robustness',
    'Rob': 'Robustness',
    'Foc.': 'Focus',
    'Foc': 'Focus',
    'Vit.': 'Vitality',
    'Vita.': 'Vitality',
    'Vit': 'Vitality',
    'Poi.': 'Poise',
    'Poi': 'Poise'
}


# 3. Initialize our final columns (fill with 0.0 by default)
final_cols = [
    'Physical','Strike','Slash','Pierce','Magic','Fire','Lightning','Holy',
    'Immunity','Robustness','Focus','Vitality','Poise'
]

for col in final_cols:
    df[col] = 0.0


# 4. Define and run function to parse and extract values from the string fields
def extract_armor_stats(row):
    # Parse Damage_Negation
    if pd.notnull(row['damage negation']):
        try:
            damage_list = ast.literal_eval(row['damage negation'])
            if isinstance(damage_list, list) and len(damage_list) > 0:
                dmg_dict = damage_list[0]  # We only expect one dict in the list
                for k, v in dmg_dict.items():
                    # Standardize the key if it exists in damage_key_map
                    if k in damage_key_map:
                        final_col = damage_key_map[k]
                        # Convert to float, default 0.0 if conversion fails
                        try:
                            row[final_col] = float(v)
                        except ValueError:
                            row[final_col] = 0.0
        except (SyntaxError, ValueError):
            pass  # If parsing fails, just leave defaults

    # Parse Resistance
    if pd.notnull(row['resistance']):
        try:
            resist_list = ast.literal_eval(row['resistance'])
            if isinstance(resist_list, list) and len(resist_list) > 0:
                res_dict = resist_list[0]
                for k, v in res_dict.items():
                    # Standardize the key if it exists in resist_key_map
                    if k in resist_key_map:
                        final_col = resist_key_map[k]
                        # Convert to float, default 0.0 if conversion fails
                        try:
                            row[final_col] = float(v)
                        except ValueError:
                            row[final_col] = 0.0
        except (SyntaxError, ValueError):
            pass

    return row

# Run
df = df.apply(extract_armor_stats, axis=1)


# 5. Scale selected columns to a 0-100 reference
scale_cols = [
    'Physical','Strike','Slash','Pierce','Magic','Fire','Lightning','Holy',
    'Immunity','Robustness','Focus','Vitality'
]

for col in scale_cols:
    max_val = df[col].max()
    if max_val > 0:
        df[col] = ((df[col] / max_val) * 100.0).round(2)  # Scaling and rounding
    else:
        df[col] = 0.0  # Keep as zero if no valid data


# 6. Drop unavailable armor sets and 0-fill dlc (in-game region data is incorrect)

# drop unavailable
df = df[df["in-game section"] != 0]

# 0-fill dlc
df['dlc'] = df['dlc'].fillna(0)

# 7. Add "Power" column by weighting negation/resistance importance by commonality amongst major bosses

df["Power"] = 26*df["Physical"] +10*df["Fire"] +10*df["Magic"] +8*df["Pierce"] +8*df["Strike"] +7*df["Holy"] +7*df["Slash"] +6*df["Robustness"] +5*df["Lightning"] +3*df["Immunity"] +df["Focus"] +df["Vitality"]
df["Power"] = df["Power"].round(2)

# 8. Save to a new cleaned CSV

# drop columns
df = df.drop(columns={"id", "image", "description", "damage negation", "resistance", "how to acquire", "in-game section"})
# rename columns
df = df.rename(columns={"name":"Name", "type":"Slot", "weight":"Weight", "special effect": "Special", "dlc": "DLC"})
# rename slots
df['Slot'] = df['Slot'].replace({"helm":"Helm", "chest armor":"Chest", "gauntlets":"Gauntlets", "leg armor":"Legs"})

output_file = "data/Clean.csv"
df.to_csv(output_file, index=False)

print(f"Processed CSV saved as {output_file}")
