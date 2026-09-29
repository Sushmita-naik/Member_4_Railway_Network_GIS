import networkx as nx
import pandas as pd


def get_route(graph, current_station, destination_station):
    try:
        route = nx.shortest_path(
            graph,
            source=current_station,
            target=destination_station
        )
        return route

    except nx.NetworkXNoPath:
        return []


def calculate_remaining_distance(graph, route):
    total_distance = 0.0

    for i in range(len(route) - 1):
        source = route[i]
        destination = route[i + 1]

        distance = graph[source][destination].get(
            "distance_km",
            0
        )

        if pd.notna(distance):
            total_distance += float(distance)

    return total_distance


def calculate_remaining_travel_time(graph, route):
    total_time = 0.0

    for i in range(len(route) - 1):
        source = route[i]
        destination = route[i + 1]

        travel_time = graph[source][destination].get(
            "scheduled_travel_min",
            0
        )

        if pd.notna(travel_time):
            total_time += float(travel_time)

    return total_time


def calculate_route_delay(graph, route):
    total_delay = 0.0

    for i in range(len(route) - 1):
        source = route[i]
        destination = route[i + 1]

        delay = graph[source][destination].get(
            "section_delay_min",
            0
        )

        if pd.notna(delay):
            total_delay += float(delay)

    return total_delay


def get_network_features(
    graph,
    current_station,
    destination_station
):
    route = get_route(
        graph,
        current_station,
        destination_station
    )

    if not route:
        return None

    distance = calculate_remaining_distance(
        graph,
        route
    )

    travel_time = calculate_remaining_travel_time(
        graph,
        route
    )

    delay = calculate_route_delay(
        graph,
        route
    )

    features = {
        "current_station": current_station,
        "destination_station": destination_station,
        "route": route,
        "distance_remaining_km": round(
            distance,
            3
        ),
        "scheduled_time_remaining_min": round(
            travel_time,
            2
        ),
        "network_delay_min": round(
            delay,
            2
        )
    }

    return features


def create_network_feature_dataset(
    train_data,
    graph,
    destination_station
):
    output_rows = []

    for index, row in train_data.iterrows():
        current_station = row["station_code"]

        features = get_network_features(
            graph,
            current_station,
            destination_station
        )

        if features is None:
            continue

        output_row = row.to_dict()

        output_row["network_distance_remaining_km"] = (
            features["distance_remaining_km"]
        )

        output_row["network_scheduled_time_remaining_min"] = (
            features["scheduled_time_remaining_min"]
        )

        output_row["network_delay_min"] = (
            features["network_delay_min"]
        )

        output_row["network_route"] = (
            " -> ".join(features["route"])
        )

        output_rows.append(output_row)

    return pd.DataFrame(output_rows)