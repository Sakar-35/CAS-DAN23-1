#CAS/DAN23
#GROUP MEMBERS:
#[ARYAN RAYAMAJHI]-[S385826]
#[MEENU DEVI MEENU DEVI]-[S383485]
#[RIWAJ ADHIKARI]-[S385933]
#[SAKAR KHADKA]-[S385095]

import csv

# Dictionary to store temperature data for each year
years = {}
# Dictionary to store combined station data across all years
stations = {}

# Load data from all CSV files in the directory for each year (1987 to 2004)
for year in range(1987, 2005):
    with open(f"temperature_data/stations_group_{year}.csv") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip the header row
        # Store the temperature data by station and year, converting temperatures to floats
        years[year] = {row[0]: list(map(float, row[4:])) for row in reader}

# Combine temperature data across all years by station
for year, data in years.items():
    for station, temps in data.items():
        if station not in stations:
            stations[station] = []  # Initialize station if not already in the dictionary
        # Add the station's temperatures from the current year to the combined data
        stations[station].extend(temps)

# Calculate the average temperature for each month across all stations
monthly_averages = [0] * 12  # Initialize list for monthly averages (12 months)
# For each station, add its temperature for each month to the corresponding month's total
for station_temps in stations.values():
    for i in range(12):
        monthly_averages[i] += station_temps[i]
# Divide by the number of stations to get the average, rounding to two decimal places
monthly_averages = [round(total / len(stations), 2) for total in monthly_averages]

# Define the months that make up each season
seasons = {
    "Summer": [11, 0, 1],  # Dec, Jan, Feb
    "Autumn": [2, 3, 4],   # Mar, Apr, May
    "Winter": [5, 6, 7],   # Jun, Jul, Aug
    "Spring": [8, 9, 10]   # Sep, Oct, Nov
}
# Calculate the average temperature for each season
season_averages = {
    season: round(sum(monthly_averages[m] for m in months) / len(months), 2)
    for season, months in seasons.items()
}

# Save seasonal averages to the same text file
with open('average_temp.txt', 'a') as f:
    f.write("\n\nSeasonal Average Temperatures:\n")
    # Write the average temperature for each season to the file
    for season, avg in season_averages.items():
        f.write(f"{season}: {avg}\n")

# Find the station with the largest temperature range (max - min temperature)
largest_range_station = max(
    stations.items(), key=lambda x: max(x[1]) - min(x[1])  # Compare the temperature range for each station
)
largest_range = round(max(largest_range_station[1]) - min(largest_range_station[1]), 2)

# Save the station with the largest temperature range to a file
with open('largest_temp_range_station.txt', 'w') as f:
    f.write("Station with Largest Temperature Range:\n")
    f.write(f"{largest_range_station[0]}: {largest_range}\n")

# Calculate the average temperature for each station
station_averages = {
    station: sum(temps) / len(temps) for station, temps in stations.items()
}
# Find the warmest and coolest stations based on the average temperature
warmest_station = max(station_averages.items(), key=lambda x: x[1])  # Station with the highest average temperature
coolest_station = min(station_averages.items(), key=lambda x: x[1])  # Station with the lowest average temperature

# Save the warmest and coolest stations to a text file
with open('warmest_and_coolest_stations.txt', 'w') as f:
    f.write("Warmest Station:\n")
    f.write(f"{warmest_station[0]}: {round(warmest_station[1], 2)}\n\n")
    f.write("Coolest Station:\n")
    f.write(f"{coolest_station[0]}: {round(coolest_station[1], 2)}\n")
