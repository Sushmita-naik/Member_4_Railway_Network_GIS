import pandas as pd
import networkx as nx


def load_train_data(file_path, sheet_name):
    train_data = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        engine="openpyxl"
    )

    required_columns = [
        "train_id",
        "station_code",
        "Station_full_name",
        "distance_from_origin_km",
        "distance_to_next_km",
        "scheduled_travel_min",
        "dwell_time_min",
        "current_delay_min"
    ]

    if "station_full_name" in train_data.columns:
        train_data = train_data.rename(
            columns={
                "station_full_name": "Station_full_name"
            }
        )

    missing_columns = [
        column
        for column in required_columns
        if column not in train_data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in {sheet_name}: {missing_columns}"
        )

    return train_data


def build_railway_graph(train_data):
    graph = nx.DiGraph()

    stations = train_data.drop_duplicates(
        subset=["station_code"],
        keep="first"
    ).reset_index(drop=True)

    for _, station in stations.iterrows():
        graph.add_node(
            station["station_code"],
            station_name=station["Station_full_name"],
            train_id=station["train_id"]
        )

    for i in range(len(stations) - 1):
        current_station = stations.iloc[i]
        next_station = stations.iloc[i + 1]

        distance = current_station["distance_to_next_km"]
        travel_time = current_station["scheduled_travel_min"]
        current_delay = current_station["current_delay_min"]

        if pd.isna(distance):
            distance = 0.0

        if pd.isna(travel_time):
            travel_time = 0.0

        if pd.isna(current_delay):
            current_delay = 0.0

        graph.add_edge(
            current_station["station_code"],
            next_station["station_code"],
            distance_km=float(distance),
            scheduled_travel_min=float(travel_time),
            section_delay_min=float(current_delay)
        )

    return graph


def print_graph_information(graph):
    print("\n========== RAILWAY GRAPH ==========")

    print(
        "Number of stations:",
        graph.number_of_nodes()
    )

    print(
        "Number of railway sections:",
        graph.number_of_edges()
    )

    print("\nStations:")

    for node, data in graph.nodes(data=True):
        print(
            node,
            "->",
            data["station_name"]
        )

    print("\nRailway sections:")

    for source, destination, data in graph.edges(data=True):
        print(
            source,
            "->",
            destination,
            "| Distance:",
            data["distance_km"],
            "km",
            "| Scheduled time:",
            data["scheduled_travel_min"],
            "min",
            "| Delay:",
            data["section_delay_min"],
            "min"
        )


if __name__ == "__main__":

    file_path = "data/Train_ETA_Dataset_Master.xlsx"

    print("\nLoading Train 12620...")

    train_12620 = load_train_data(
        file_path,
        "Train_12620"
    )

    print(
        "Train 12620 rows:",
        len(train_12620)
    )

    graph_12620 = build_railway_graph(
        train_12620
    )

    print("\nTrain 12620 graph:")

    print_graph_information(
        graph_12620
    )

    print("\nLoading Train 10108...")

    train_10108 = load_train_data(
        file_path,
        "Train_10108"
    )

    print(
        "Train 10108 rows:",
        len(train_10108)
    )

    graph_10108 = build_railway_graph(
        train_10108
    )

    print("\nTrain 10108 graph:")

    print_graph_information(
        graph_10108
    )