"""CSC111 Project: Picturing the Power of Policy in a Pandemic

Instructions (READ THIS FIRST!)
===============================

This Python module contains functions that plots the real world data
network graphs on a world map.

Do not edit anything in this module.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and
instructors of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2021 Jia Hao Choo & Komal Saini.
"""
import csv
import networkx as nx
from classes import WeightedGraph


def convert_to_networkx(graph: WeightedGraph) -> nx.Graph:
    """Convert a WeightedGraph to a weighted Networkx graph."""
    graph_nx = nx.Graph()

    for vertex in graph.get_all_vertices():
        graph_nx.add_node(vertex)

        for v2 in graph.get_all_vertices()[vertex].similar_policies:
            graph_nx.add_node(v2.country_name)

            if v2.country_name in graph_nx.nodes:
                graph_nx.add_edge(v2.country_name, vertex,
                                  weight=graph.get_all_vertices()[vertex].similar_policies[v2])

    return graph_nx


def find_centroids_location(country: str) -> tuple[float, float]:
    """Return the central location of the country in the form of
    (longitude, latitude).

    *As a precondition, every country is in the csv file, so every
    input should have a return value. However, to satisy PyTA conditions,
    if the data is not in the file, then the tuple (0.0, 0.0) will be returned.

    Preconditions:
        - country is in datasets/centroids.csv file

    >>> find_centroids_location('Canada')
    (-98.30777028, 61.36206324)
    """
    with open('datasets/centroids.csv') as file:
        reader = csv.reader(file)

        next(reader)

        for row in reader:
            if row[0] == country:
                return (float(row[1]), float(row[2]))

    return (0.0, 0.0)


def plot_map_all(graph: nx.Graph) -> None:
    """Display a world map showing the edges between countries. The thicker the
    edge, the more similar the countries are in terms of COVID-19 policy.
    """


def plot_map_policy(graph: nx.Graph, policy: str) -> None:
    """Display a world map showing the edges between countries that has the same level
    of restrictions of the policy. Users can switch between different level by interacting
    with the buttons on the graph.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
        'public-events-cancellation','school-workplace-closures', 'stay-at-home', 'testing-policy',
         'vaccination-policy']
    """


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'allowed-io': ['find_centroids_location'],
        'extra-imports': ['classes', 'csv', 'networkx'],
        'disable': ['E1136'],
    })
