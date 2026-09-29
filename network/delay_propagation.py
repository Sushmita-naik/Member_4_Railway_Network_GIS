import pandas as pd


def get_section_delays(graph, route):
    section_delays = []

    for i in range(len(route) - 1):
        source = route[i]
        destination = route[i + 1]

        edge_data = graph[source][destination]

        delay = edge_data.get(
            "section_delay_min",
            0
        )

        if pd.isna(delay):
            delay = 0.0

        section_delays.append(
            float(delay)
        )

    return section_delays


def calculate_propagated_delay(
    current_delay,
    section_delays
):
    propagated_delay = float(
        current_delay
    )

    for delay in section_delays:
        propagated_delay += float(
            delay
        )

    return propagated_delay


def calculate_station_delays(
    current_delay,
    section_delays
):
    station_delays = []

    accumulated_delay = float(
        current_delay
    )

    for delay in section_delays:
        accumulated_delay += float(
            delay
        )

        station_delays.append(
            accumulated_delay
        )

    return station_delays


def estimate_future_delay(
    current_delay,
    section_delays
):
    station_delays = calculate_station_delays(
        current_delay,
        section_delays
    )

    if not station_delays:
        return float(
            current_delay
        )

    return station_delays[-1]


def analyze_delay_propagation(
    graph,
    route,
    current_delay
):
    section_delays = get_section_delays(
        graph,
        route
    )

    station_delays = calculate_station_delays(
        current_delay,
        section_delays
    )

    final_delay = estimate_future_delay(
        current_delay,
        section_delays
    )

    return {
        "current_delay_min": float(
            current_delay
        ),
        "section_delays": section_delays,
        "station_delays": station_delays,
        "estimated_final_delay_min": final_delay
    }