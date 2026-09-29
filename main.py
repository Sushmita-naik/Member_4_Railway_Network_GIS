from gis.railway_map import create_railway_map
from gis.station_coordinates import station_coordinates

from network.graph_builder import load_train_data, build_railway_graph
from network.network_features import get_network_features
from network.delay_propagation import analyze_delay_propagation

DATA_FILE = "data/Train_ETA_Dataset_Master.xlsx"

print()
print("================================")
print(" MEMBER 4 - RAILWAY NETWORK")
print("================================")

# TRAIN 12620

print()
print("1. Loading Train 12620...")

train_12620 = load_train_data(
DATA_FILE,
"Train_12620"
)

print("Train 12620 rows:", len(train_12620))

graph_12620 = build_railway_graph(
train_12620
)

print()
print("2. Analysing Train 12620 route...")

current_station = "SL"
destination_station = "KAWR"

features_12620 = get_network_features(
graph_12620,
current_station,
destination_station
)

print()
print("================================")
print(" NETWORK FEATURES - TRAIN 12620")
print("================================")

print("Current station:", features_12620["current_station"])
print("Destination:", features_12620["destination_station"])
print("Route:", " -> ".join(features_12620["route"]))
print("Remaining distance:", features_12620["distance_remaining_km"], "km")
print(
"Scheduled travel time remaining:",
features_12620["scheduled_time_remaining_min"],
"minutes"
)
print("Network delay:", features_12620["network_delay_min"], "minutes")

print()
print("3. Analysing delay propagation for Train 12620...")

delay_analysis_12620 = analyze_delay_propagation(
graph_12620,
features_12620["route"],
current_delay=0
)

print()
print("================================")
print(" DELAY PROPAGATION - TRAIN 12620")
print("================================")

print(
"Current delay:",
delay_analysis_12620["current_delay_min"],
"minutes"
)

print(
"Section delays:",
delay_analysis_12620["section_delays"]
)

print(
"Accumulated station delays:",
delay_analysis_12620["station_delays"]
)

print(
"Estimated final accumulated delay:",
delay_analysis_12620["estimated_final_delay_min"],
"minutes"
)

# TRAIN 10108

print()
print("4. Loading Train 10108...")

train_10108 = load_train_data(
DATA_FILE,
"Train_10108"
)

print("Train 10108 rows:", len(train_10108))

graph_10108 = build_railway_graph(
train_10108
)

print()
print("5. Analysing Train 10108 route...")

features_10108 = get_network_features(
graph_10108,
current_station,
destination_station
)

print()
print("================================")
print(" NETWORK FEATURES - TRAIN 10108")
print("================================")

print("Current station:", features_10108["current_station"])
print("Destination:", features_10108["destination_station"])
print("Route:", " -> ".join(features_10108["route"]))
print("Remaining distance:", features_10108["distance_remaining_km"], "km")
print(
"Scheduled travel time remaining:",
features_10108["scheduled_time_remaining_min"],
"minutes"
)
print("Network delay:", features_10108["network_delay_min"], "minutes")

print()
print("6. Analysing delay propagation for Train 10108...")

delay_analysis_10108 = analyze_delay_propagation(
graph_10108,
features_10108["route"],
current_delay=0
)

print()
print("================================")
print(" DELAY PROPAGATION - TRAIN 10108")
print("================================")

print(
"Current delay:",
delay_analysis_10108["current_delay_min"],
"minutes"
)

print(
"Section delays:",
delay_analysis_10108["section_delays"]
)

print(
"Accumulated station delays:",
delay_analysis_10108["station_delays"]
)

print(
"Estimated final accumulated delay:",
delay_analysis_10108["estimated_final_delay_min"],
"minutes"
)

print()
print("================================")
print(" NETWORK ANALYSIS COMPLETED")
print("================================")
print()
print("8. Creating GIS map for Train 10108...")

route_10108 = features_10108["route"]

create_railway_map(
route_10108,
station_coordinates,
"outputs/train_10108_route.html"
)

print("Train 10108 GIS map created.")