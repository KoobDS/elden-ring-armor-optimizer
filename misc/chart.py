import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned dataset
df = pd.read_csv("data/Clean.csv")

# List of unique selected armor pieces from any of the 6 methods
selected_armor = {
    "Circlet of Light", "Fingerprint Armor (Altered)", "Ascetic's Wrist Guards", "Crucible Greaves",
    "Battlemage Manchettes", "Omensmirk Mask", "Gold Bracelets", "Champion Headband",
    "Mausoleum Knight Armor (Altered)", "Greatjar", "Verdigris Armor", "Verdigris Gauntlets",
    "Verdigris Greaves", "Bull-Goat Helm", "Bull-Goat Armor", "Bull-Goat Gauntlets", "Bull-Goat Greaves",
    "Crucible Tree Armor", "Ronin's Greaves", "Marais Mask", "Godskin Noble Bracelets"
}

# Ensure no duplicates
selected_armor = set(selected_armor)

# Assign a color based on whether an armor piece is selected
df["Selected"] = df["Name"].apply(lambda x: "Selected" if x in selected_armor else "Not Selected")

# Create scatter plot
plt.figure(figsize=(10, 6))

for category, color in zip(["Not Selected", "Selected"], ["gray", "red"]):
    subset = df[df["Selected"] == category]
    plt.scatter(subset["Weight"], subset["Power"], label=category, alpha=0.7, color=color)

# Labels and title
plt.xlabel("Weight")
plt.ylabel("Power")
plt.title("Weight vs. Power of Elden Ring Armor Pieces (Optimal Armor Highlighted)")
plt.legend()
plt.grid(True)

# Save the plot as an image
output_path = "scatter_plot.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Scatter plot saved as {output_path}")
