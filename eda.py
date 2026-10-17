from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

#locating the project directory
project_dir = Path(__file__).resolve().parent
data_path = project_dir / "data" / "raw" / "f1_results.csv"

if not data_path.exists():
    raise FileNotFoundError("Data file not found")

df = pd.read_csv(data_path)

print('=' * 50)
print('Data loaded successfully!')
print('=' * 50)

#basic information about the dataset
print("Dataset Information:")
print(f"dataset shape: {df.shape}")
print(f"no of seasons: {df['season'].nunique()}")
print(f"no of races: {df['race_name'].nunique()}")

#inspect the no of uniqiue dirvers and teams

print(f"no of unique drivers: {df['driver_name'].nunique()}")
print(f"no of unique teams: {df['team'].nunique()}")


#check for duplicates
duplicates = df.duplicated()
if duplicates.any():
    print(f"Found {duplicates.sum()} duplicate rows. Removing duplicates...")
    df = df.drop_duplicates()

#check for missing values
missing = df.isnull().sum()
if missing.any():
    print("Missing values found:")
    print(missing[missing > 0])
    print(df.isnull().sum().sort_values(ascending=False))
    print("Filling missing values with 0...")
    df = df.fillna(0)

#inspect historical coverage
races_per_Season = (
    df.groupby('season')['race_name'].nunique()
)

print("Races per season:")
print(races_per_Season)

#inspect starting grid positions
print(df['grid_position'].value_counts().sort_index())

#inspect the race name and driver name
print(df["race_name"])
print(df["driver_name"])
print(df.groupby("season")["race_name"].nunique())

#inspect the distribution of winners
winner_distribution = df.groupby("driver_name")["winner"].sum().sort_values(ascending=False)
print("Winner distribution:")
print(winner_distribution)

#now using matplotlib to visualize the distribution of winners
plt.figure(figsize=(12, 6))
plt.bar(winner_distribution.index, winner_distribution.values)
plt.xticks(rotation=90)
plt.title("Distribution of Winners by Driver")
plt.xlabel("Driver Name")
plt.ylabel("Number of Wins")
plt.tight_layout()
plt.show()

