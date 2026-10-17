from pathlib import Path
import time
import pandas as pd
import requests

#project paths
PROJECT_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

#HISTORICAL WINDOW
START_YEAR = 2011
END_YEAR = 2025

#setting the base url for the fifa data
base_url = "https://api.jolpi.ca/ergast/f1"
headers = {
    "User-Agent": "F1RaceIntelligence/1.0"
}

def get_json_data(url, params=None):

    #fetching the data from the url
    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30,

    )
    response.raise_for_status()
    return response.json()

#downloading the result for each season
def load_season_data(year):

    #we have to gen the url for the season data
    season_url = f"{base_url}/{year}.json"

    season_Data = get_json_data(season_url,
                                params={"limit": 100})

    races = season_Data["MRData"]["RaceTable"]["Races"]
    season_results = []

    for race in races:
        round_no = int(race["round"])
        race_name = race["raceName"]
        circuit_name = race["Circuit"]["circuitName"]
        race_date = race["date"]

        results_url = f"{base_url}/{year}/{round_no}/results.json"

        results_data = get_json_data(
            results_url,
            params={"limit": 100}
        )

        race_results = results_data["MRData"]["RaceTable"]["Races"]

        if not race_results:
            continue

        for result in race_results[0].get("Results", []):
            driver = result["Driver"]
            constructor = result["Constructor"]

            season_results.append({
                 "season": year,
                "round": round_no,
                "race_name": race_name,
                "race_date": race_date,
                "circuit": circuit_name,
                "driver_id": driver["driverId"],
                "driver_name": (
                    f"{driver['givenName']} "
                    f"{driver['familyName']}"
                ),
                "driver_code": driver.get("code"),
                "team": constructor["name"],
                "team_id": constructor["constructorId"],
                "grid_position": result.get("grid"),
                "finish_position": result.get("position"),
                "position_text": result.get("positionText"),
                "points": result.get("points"),
                "laps_completed": result.get("laps"),
                "status": result.get("status"),
            })

        time.sleep(0.5)

    return pd.DataFrame(season_results)



def main():
    all_seasons_data = []

    for year in range(START_YEAR, END_YEAR + 1):
        print(f"Loading data for season {year}...")
        season_data = load_season_data(year)
        all_seasons_data.append(season_data)

        print(f"Data for season {year} loaded successfully.")

        #concat
        results = pd.concat(all_seasons_data, ignore_index=True)

        #convert the numeric columns to appropriate data types
        numeric_columns = [
            "round",
            "grid_position",
            "finish_position",
            "points",
            "laps_completed"
        ]

        for column in numeric_columns: 
            results[column] = pd.to_numeric(
                results[column], errors="coerce"
            )

        results["winner"]  = (
            results["finish_position"] == 1
        ).astype(int)

        output_file = RAW_DATA_DIR / "f1_results.csv"
        results.to_csv(output_file, index=False)

        print(f"All seasons data saved to {output_file}")
        print(f"Dataset shape: {results.shape}")
        print(f"Columns: {results.columns.tolist()}")
        print(f"Preview of the dataset:\n{results.head()}")

if __name__ == "__main__":
    main()

