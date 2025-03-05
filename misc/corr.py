import pandas as pd

# Load the dataset
file_path = "data/Clean.csv"
df = pd.read_csv(file_path)

# Select relevant columns
correlation_matrix = df[["Weight", "Poise", "Power"]].corr()

# Display the correlation matrix
print(correlation_matrix)
