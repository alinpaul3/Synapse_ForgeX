import pandas as pd

# Load your dataset
df = pd.read_csv("ocean_training_data.csv")

# Keep only required columns
df = df[["text", "O", "C", "E", "A", "N"]]

# Ensure numeric format
for col in ["O", "C", "E", "A", "N"]:
    df[col] = df[col].astype(float)

# Save cleaned dataset
df.to_csv("data/training/ocean_training_data.csv", index=False)

print("Dataset prepared successfully!")
print(df.head())