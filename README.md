# Railway Network / GIS / Delay Propagation

This module is responsible for representing the railway route as a graph,
calculating network-level features, estimating delay propagation, and
visualizing the railway route using GIS.

## Responsibilities

### 1. Railway Network

The railway network is represented as a directed graph.

- Station = Node
- Railway section = Edge

### 2. Network Features

The module calculates features such as:

- Current station
- Destination station
- Route
- Distance remaining
- Scheduled travel time remaining
- Network delay

### 3. Delay Propagation

The module estimates accumulated delay across upcoming railway sections
using verified or derived delay information.

### 4. GIS Visualization

The railway route is displayed on an interactive map using Folium.

The map can display:

- Railway stations
- Railway route
- Train location
- Train delay
- Network information

## Project Structure

```text
MEMBER_4_Railway_Network_GIS/
│
├── data/
│   └── Train_ETA_Dataset.xlsx
│
├── network/
│   ├── __init__.py
│   ├── graph_builder.py
│   ├── network_features.py
│   └── delay_propagation.py
│
├── gis/
│   ├── __init__.py
│   └── railway_map.py
│
├── outputs/
│
├── main.py
│
├── requirements.txt
│
└── README.md