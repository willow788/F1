import fastf1
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import mean_absolute_error, accuracy_score

#enambling the f1 caching
fastf1.Cache.enable_cache("f1_cache")

session_24 = fastf1.get_session(2024, 3, "R")
print('Attempting to load session...')
session_24.load()
print('Australian session details loaded.')

#extracting lap times
laps_2024 = session_24.laps[["Driver", "LapTime"]].copy()
#dropping the null laps
laps_2024 = laps_2024.dropna(subset=["LapTime"])
#convert to seconds
laps_2024["LapTime(s)"] = laps_2024["LapTime"].dt.total_seconds()

#2025  qualifying daTA
qualifying_2025 = pd.DataFrame({
    "Driver": ["Lando Norris", "Oscar Piastri", "Max Verstappen", "George Russell", "Yuki Tsunoda", "Alexander Albon", "Charles Leclerc", "Lewis Hamilton", "Pierre Gasly", "Carlos Sainz", "Fernando Alonso", "Lance Stroll"],
    "QualifyingTime(s)": [75.096, 75.180, 75.489, 75.670, 75.737, 75.755, 75.973, 75.780, 75.062, 75.4, 76.5, 76.8]
})

#mapping the name
driver_mapping = {
    "Lando Norris" : "NOR",
    "Oscar Piastri" : "PIA",
    "Max Verstappen" : "VER",
    "George Russell" : "RUS",
    "Yuki Tsunoda" : "TSU",
    "Alexander Albon" : "ALB",
    "Charles Leclerc" : "LEC",
    "Lewis Hamilton" : "HAM",
    "Pierre Gasly" : "GAS",
    "Carlos Sainz" : "SAI",
    "Fernando Alonso" : "ALO",
    "Lance Stroll" : "STR"}

qualifying_2025["DriverCode"] = qualifying_2025["Driver"].map(driver_mapping)

#get average lap times per driver from 2024
laps_2024_avg = laps_2024.groupby("Driver")["LapTime(s)"].mean().reset_index()
laps_2024_avg.columns = ["Driver", "RaceLapTime(s)"]

#mergeing the data
merged_Data = qualifying_2025.merge(laps_2024_avg, left_on="DriverCode", right_on="Driver")

X = merged_Data[["QualifyingTime(s)"]]

y = merged_Data["RaceLapTime(s)"]

if X.shape[0] == 0:
    raise ValueError('dataset empty after processing')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import GradientBoostingRegressor

model = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate= 0.1,
    random_state=42
)

model.fit(X_train, y_train)

predicted_lap_times = model.predict(
    qualifying_2025[['QualifyingTime(s)']])

qualifying_2025['PredictedLapTime(s)'] = predicted_lap_times

#rank the racers
qualifying_2025 = qualifying_2025.sort_values('PredictedLapTime(s)', ascending=True)
qualifying_2025['Rank'] = range(1, len(qualifying_2025) + 1)

print("\n Predicted winner: \n")
print(qualifying_2025[['Driver', 'PredictedLapTime(s)']])
