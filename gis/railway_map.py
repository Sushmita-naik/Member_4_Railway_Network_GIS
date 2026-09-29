import pandas as pd
import folium
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FILE = (
    BASE_DIR
    / "data"
    / "Train_ETA_Dataset_Master.xlsx"
)

OUTPUT = (
    BASE_DIR
    / "outputs"
    / "train_12620_route.html"
)


# ============================================================
# LOAD TRAIN DATA
# ============================================================

df = pd.read_excel(
    FILE,
    sheet_name="Train_12620"
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

df = df.sort_values(
    "timestamp"
).reset_index(drop=True)


# ============================================================
# STATION COORDINATES
# ============================================================

coordinates = {

    "MAQ": (12.8698, 74.8421),

    "SL": (12.990234, 74.805437),

    "MULK": (13.0775, 74.7937),

    "UD": (13.3409, 74.7473),

    "BKJ": (13.4557, 74.7417),

    "KUDA": (13.6295, 74.6904),

    "BYNR": (13.8585, 74.6302),

    "BTJL": (13.9716, 74.5639),

    "MRDW": (14.0911, 74.4840),

    "HNA": (14.2790, 74.4440),

    "KT": (14.4250, 74.4130),

    "GOK": (14.5500, 74.3190),

    "ANKL": (14.6600, 74.3000),

    "KAWR": (14.8120, 74.1290)
}


# ============================================================
# TRAIN ROUTE
# ============================================================

route = [

    "MAQ",
    "SL",
    "MULK",
    "UD",
    "BKJ",
    "KUDA",
    "BYNR",
    "BTJL",
    "MRDW",
    "HNA",
    "KT",
    "GOK",
    "ANKL",
    "KAWR"
]


# ============================================================
# SELECT HISTORICAL TIME
# ============================================================

target_time = pd.Timestamp(
    "2025-01-08 13:49:00"
)


# ============================================================
# FIND HISTORICAL RECORD
# ============================================================

previous_records = df[
    df["timestamp"] <= target_time
]

if previous_records.empty:

    print("No historical record found.")

    exit()


current = previous_records.iloc[-1]


# ============================================================
# CURRENT STATION
# ============================================================

current_station = str(
    current["station_code"]
).strip()


# ============================================================
# FIND NEXT STATION
# ============================================================

if current_station in route:

    station_index = route.index(
        current_station
    )

else:

    print(
        "Station not found in route:",
        current_station
    )

    exit()


if station_index < len(route) - 1:

    next_station = route[
        station_index + 1
    ]

else:

    next_station = None


# ============================================================
# READ TRAIN VALUES
# ============================================================

speed = pd.to_numeric(
    current["speed_kmph"],
    errors="coerce"
)

distance_to_next = pd.to_numeric(
    current["distance_to_next_km"],
    errors="coerce"
)

delay = pd.to_numeric(
    current["current_delay_min"],
    errors="coerce"
)


# ============================================================
# GET ACTUAL DEPARTURE TIME
# ============================================================

date_part = current["timestamp"].date()

departure_text = str(
    current["Dep. Time"]
)

departure_time = pd.to_datetime(
    str(date_part)
    + " "
    + departure_text,
    errors="coerce"
)


# ============================================================
# CALCULATE ELAPSED TIME
# ============================================================

elapsed_minutes = (
    target_time - departure_time
).total_seconds() / 60


# ============================================================
# CALCULATE TRAIN POSITION
# ============================================================

if (
    next_station is not None
    and pd.notna(speed)
    and speed > 0
    and pd.notna(distance_to_next)
    and distance_to_next > 0
):

    # Distance travelled after leaving station
    travelled_distance = (
        speed
        * elapsed_minutes
        / 60
    )

    # Percentage of section completed
    progress = (
        travelled_distance
        / distance_to_next
    )

    # Keep between 0 and 100%
    progress = max(
        0.0,
        min(progress, 1.0)
    )

else:

    travelled_distance = 0.0

    progress = 0.0


# ============================================================
# CALCULATE TRAIN LATITUDE / LONGITUDE
# ============================================================

if next_station is not None:

    lat1, lon1 = coordinates[
        current_station
    ]

    lat2, lon2 = coordinates[
        next_station
    ]

    train_lat = (
        lat1
        + progress
        * (lat2 - lat1)
    )

    train_lon = (
        lon1
        + progress
        * (lon2 - lon1)
    )

else:

    train_lat, train_lon = coordinates[
        current_station
    ]


# ============================================================
# PRINT POSITION INFORMATION
# ============================================================

print()

print("=" * 100)

print(
    "TRAIN 12620 HISTORICAL POSITION"
)

print("=" * 100)

print()

print(
    "Selected time        :",
    target_time
)

print(
    "Recorded station     :",
    current_station
)

print(
    "Next station         :",
    next_station
)

print(
    "Departure time       :",
    departure_time
)

print(
    "Elapsed time         :",
    round(elapsed_minutes, 2),
    "minutes"
)

print(
    "Speed                :",
    speed,
    "km/h"
)

print(
    "Distance to next     :",
    distance_to_next,
    "km"
)

print(
    "Distance travelled   :",
    round(travelled_distance, 3),
    "km"
)

print(
    "Section progress     :",
    round(progress * 100, 2),
    "%"
)

print(
    "Historical delay     :",
    delay,
    "minutes"
)

print(
    "Train latitude       :",
    round(train_lat, 6)
)

print(
    "Train longitude      :",
    round(train_lon, 6)
)

print()

print("=" * 100)


# ============================================================
# CREATE MAP
# ============================================================

railway_map = folium.Map(

    location=[
        train_lat,
        train_lon
    ],

    zoom_start=9,

    tiles="OpenStreetMap"
)


# ============================================================
# DRAW RAILWAY ROUTE
# ============================================================

route_coordinates = []

for station in route:

    if station in coordinates:

        route_coordinates.append(
            coordinates[station]
        )


folium.PolyLine(

    route_coordinates,

    weight=5,

    opacity=0.8,

    tooltip="12620 Railway Route"

).add_to(
    railway_map
)


# ============================================================
# ADD STATION MARKERS
# ============================================================

for station in route:

    lat, lon = coordinates[
        station
    ]

    folium.CircleMarker(

        location=[
            lat,
            lon
        ],

        radius=5,

        popup=(
            "<b>Station:</b> "
            + station
        ),

        tooltip=station,

        fill=True

    ).add_to(
        railway_map
    )


# ============================================================
# TRAIN POPUP
# ============================================================

train_popup = f"""

<div style="
    font-family: Arial;
    width: 300px;
">

<h3>🚆 Train 12620</h3>

<b>Matsyagandha Express</b>

<hr>

<b>Historical date:</b><br>
{target_time.strftime("%d-%m-%Y")}

<br><br>

<b>Selected time:</b><br>
{target_time.strftime("%H:%M")}

<br><br>

<b>Status:</b><br>
Train moving

<br><br>

<b>Section:</b><br>
{current_station} → {next_station}

<br><br>

<b>Departure:</b><br>
{departure_time.strftime("%H:%M")}

<br><br>

<b>Speed:</b><br>
{speed:.2f} km/h

<br><br>

<b>Distance travelled:</b><br>
{travelled_distance:.2f} km

<br><br>

<b>Distance to next station:</b><br>
{distance_to_next:.2f} km

<br><br>

<b>Section progress:</b><br>
{progress * 100:.2f}%

<br><br>

<b>Historical delay:</b><br>
{delay} minutes

<hr>

<b>Position type:</b><br>
Historical-data-based estimated position

<br><br>

<b>GPS:</b><br>
Not available

</div>

"""


# ============================================================
# ADD TRAIN MARKER
# ============================================================

folium.Marker(

    location=[
        train_lat,
        train_lon
    ],

    popup=folium.Popup(

        train_popup,

        max_width=350

    ),

    tooltip=(
        "🚆 12620 | "
        + current_station
        + " → "
        + str(next_station)
    ),

    icon=folium.Icon(

        color="red",

        icon="train",

        prefix="fa"

    )

).add_to(
    railway_map
)


# ============================================================
# MAP TITLE
# ============================================================

title = f"""

<div style="

    position: fixed;

    top: 10px;

    left: 50px;

    z-index: 9999;

    background: white;

    padding: 10px 15px;

    border: 2px solid black;

    border-radius: 6px;

    font-family: Arial;

    font-weight: bold;

">

🚆 12620 Matsyagandha Express

<br>

<span style="

    font-size: 12px;

    font-weight: normal;

">

Historical position:
{current_station} → {next_station}

<br>

Time:
{target_time.strftime("%H:%M")}

</span>

</div>

"""


railway_map.get_root().html.add_child(

    folium.Element(title)

)


# ============================================================
# SAVE MAP
# ============================================================

railway_map.save(
    OUTPUT
)


print()

print(
    "Map created successfully."
)

print()

print(
    "Saved at:"
)

print(
    OUTPUT
)

print()

print("=" * 100)