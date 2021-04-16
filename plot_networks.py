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
import plotly.graph_objects as go

from classes import WeightedGraph


def convert_policy_to_networkx(graph: WeightedGraph, policy: str, level: int) -> nx.Graph:
    """Convert a WeightedGraph with only edges corresponding to the policy and level
     to a weighted Networkx graph.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
        'public-events-cancellation','school-workplace-closures', 'stay-at-home', 'testing-policy',
         'vaccination-policy']
        - 0 <= level <= 6

    >>> g = WeightedGraph()
    >>> g.add_vertex('Country1', [0.1],[0.1],1000)
    >>> g.add_vertex('Country2', [0.1],[0.1],1000)
    >>> g.add_vertex_restrictions('Country1','face-covering-policies', 3)
    >>> g.add_vertex_restrictions('Country2','face-covering-policies', 3)
    >>> g.find_and_add_edge('Country1')
    >>> n = convert_policy_to_networkx(g, 'face-covering-policies', 3)
    >>> len(n.edges)
    1
    """
    graph_nx = nx.Graph()
    vertices = graph.get_all_vertices()
    start = None
    for vertex in vertices:
        if vertices[vertex].restrictions_level[policy] == level:
            start = vertices[vertex]

    if start is None:
        return graph_nx

    others = start.same_policy_level(policy)
    if others == []:
        graph_nx.add_node(start.country_name)
    else:
        others.insert(0, start.country_name)

        for i in range(len(others) - 1):
            graph_nx.add_node(others[i])
            graph_nx.add_node(others[i + 1])
            graph_nx.add_edge(others[i], others[i + 1])

    return graph_nx


def find_centroids_location(country: str) -> tuple[float, float]:
    """Return the central location of the country in the form of
    (longitude, latitude).

    *As a precondition, every country is in the csv file, so every
    input should have a return value. However, to satisy PyTA conditions,
    if the data is not in the file, the tuple (0.0, 0.0) will be returned.

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


def plot_face_masks(graphs: list[nx.Graph], messages: dict[int, str]) -> None:
    """Display a world map showing how countries are connected based on the level of restriction
    on a policy.

    This function is specifically for face covering policies with five levels.

    Preconditions:
        - len(graphs) == 5
    """
    fig = go.Figure()

    # Level 0
    for edge in graphs[0].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='black'),
                opacity=0.2,
            )
        )

    for country in graphs[0].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 0, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 1
    for edge in graphs[1].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='blue'),
                opacity=0.2,
            )
        )

    for country in graphs[1].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 0, 255)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 2
    for edge in graphs[2].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='red'),
                opacity=0.2,
            )
        )

    for country in graphs[2].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(255, 0, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 3
    for edge in graphs[3].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='green'),
                opacity=0.2,
            )
        )

    for country in graphs[3].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 255, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 4
    for edge in graphs[4].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='orange'),
                opacity=0.2,
            )
        )

    for country in graphs[4].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(255, 165, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    fig.update_layout(title_text='Global Comparison on the Similarities of COVID-19 Policies: '
                                 'Face Covering Policy')

    fig.update_layout(
        showlegend=False,
        geo=go.layout.Geo(
            scope='world',
            showland=True,
            showcountries=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        ),
        height=700,
    )

    fig.update_layout(
        annotations=[
            dict(text="BLACK - "
                      "Level 0: " + messages[0] + " (Total " + str(len(graphs[0].nodes)) + ")", x=0,
                 xref="paper", y=1.085, yref="paper", align="left", showarrow=False),
            dict(text="BLUE - "
                      "Level 1: " + messages[1] + " (Total " + str(len(graphs[1].nodes)) + ")", x=0,
                 xref="paper", y=1.045, yref="paper", align="left", showarrow=False),
            dict(text="RED - "
                      "Level 2: " + messages[2] + " (Total " + str(len(graphs[2].nodes)) + ")",
                 x=0.3, xref="paper", y=1.085, yref="paper", align="left", showarrow=False),
            dict(text="GREEN - "
                      "Level 3: " + messages[3] + " (Total " + str(len(graphs[3].nodes)) + ")",
                 x=0.3, xref="paper", y=1.045, yref="paper", align="left", showarrow=False),
            dict(text="ORANGE - "
                      "Level 4: " + messages[4] + " (Total " + str(len(graphs[4].nodes)) + ")",
                 x=0.9, xref="paper", y=1.085, yref="paper", align="left", showarrow=False)
        ])

    fig.show()


def plot_three_levels(graphs: list[nx.Graph], policy: str, messages: dict[int, str]) -> None:
    """Display a world map showing how countries are connected based on the level of restriction
    on a policy.

    This function is specifically for policies with three levels, and
    is similar to plot_face_masks.

    Preconditions:
        - len(graphs) == 3
        - policy in ['public-campaigns-covid', 'public-events-cancellation']
        - len(messages) == 3
    """
    fig = go.Figure()

    # Level 0
    for edge in graphs[0].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='black'),
                opacity=0.2,
            )
        )

    for country in graphs[0].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 0, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 1
    for edge in graphs[1].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='blue'),
                opacity=0.2,
            )
        )

    for country in graphs[1].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 0, 255)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 2
    for edge in graphs[2].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='red'),
                opacity=0.2,
            )
        )

    for country in graphs[2].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(255, 0, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    if policy == 'public-campaigns-covid':
        fig.update_layout(title_text='Global Comparison on the Similarities of COVID-19 Policies: '
                                     'COVID-19 Public Campaigns')
    else:
        fig.update_layout(title_text='Global Comparison on the Similarities of COVID-19 Policies: '
                                     'Public Events Cancellations')

    fig.update_layout(
        showlegend=False,
        geo=go.layout.Geo(
            scope='world',
            showland=True,
            showcountries=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        ),
        height=700,
    )

    fig.update_layout(
        annotations=[
            dict(text="BLACK - "
                      "Level 0: " + messages[0] + " (Total " + str(len(graphs[0].nodes)) + ")", x=0,
                 xref="paper", y=1.085, yref="paper", align="left", showarrow=False),
            dict(text="BLUE - "
                      "Level 1: " + messages[1] + " (Total " + str(len(graphs[1].nodes)) + ")", x=0,
                 xref="paper", y=1.045, yref="paper", align="left", showarrow=False),
            dict(text="RED - "
                      "Level 2: " + messages[2] + " (Total " + str(len(graphs[2].nodes)) + ")",
                 x=0.3, xref="paper", y=1.085, yref="paper", align="left", showarrow=False)
        ])

    fig.show()


def plot_four_levels(graphs: list[nx.Graph], policy: str, messages: dict[int, str]) -> None:
    """Display a world map showing how countries are connected based on the level of restriction
    on a policy.

    This function is specifically for policies with 4 levels, and
    is similar to plot_face_masks.

    Preconditions:
        - len(graphs) == 4
        - policy in ['school-workplace-closures', 'stay-at-home', 'testing-policy']
        - len(messages) = 4
    """
    fig = go.Figure()

    # Level 0
    for edge in graphs[0].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='black'),
                opacity=0.2,
            )
        )

    for country in graphs[0].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 0, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 1
    for edge in graphs[1].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='blue'),
                opacity=0.2,
            )
        )

    for country in graphs[1].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 0, 255)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 2
    for edge in graphs[2].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='red'),
                opacity=0.2,
            )
        )

    for country in graphs[2].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(255, 0, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 3
    for edge in graphs[3].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='green'),
                opacity=0.2,
            )
        )

    for country in graphs[3].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 255, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    if policy == 'school-workplace-closures':
        fig.update_layout(title_text='Global Comparison on the Similarities of COVID-19 Policies: '
                                     'Schools & Workplaces Closure')
    elif policy == 'stay-at-home':
        fig.update_layout(title_text='Global Comparison on the Similarities of COVID-19 Policies: '
                                     'Stay At Home Order')
    else:
        fig.update_layout(title_text='Global Comparison on the Similarities of COVID-19 Policies: '
                                     'Testing Policy')

    fig.update_layout(
        showlegend=False,
        geo=go.layout.Geo(
            scope='world',
            showland=True,
            showcountries=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        ),
        height=700,
    )

    fig.update_layout(
        annotations=[
            dict(text="BLACK - "
                      "Level 0: " + messages[0] + " (Total " + str(len(graphs[0].nodes)) + ")", x=0,
                 xref="paper", y=1.085, yref="paper", align="left", showarrow=False),
            dict(text="BLUE - "
                      "Level 1: " + messages[1] + " (Total " + str(len(graphs[1].nodes)) + ")", x=0,
                 xref="paper", y=1.045, yref="paper", align="left", showarrow=False),
            dict(text="RED - "
                      "Level 2: " + messages[2] + " (Total " + str(len(graphs[2].nodes)) + ")",
                 x=0.3, xref="paper", y=1.085, yref="paper", align="left", showarrow=False),
            dict(text="GREEN - "
                      "Level 3: " + messages[3] + " (Total " + str(len(graphs[3].nodes)) + ")",
                 x=0.3, xref="paper", y=1.045, yref="paper", align="left", showarrow=False)
        ])

    fig.show()


def plot_vaccination(graphs: list[nx.Graph], messages: dict[int, str]) -> None:
    """Display a world map showing how countries are connected based on the level of restriction
    on a policy.

    This function is specifically for vaccination policy, with six levels, and it is
    is similar to plot_face_masks.

    Preconditions:
        - len(graphs) == 6
        - len(messages) == 6
    """
    fig = go.Figure()

    # Level 0
    for edge in graphs[0].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='black'),
                opacity=0.2,
            )
        )

    for country in graphs[0].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 0, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 1
    for edge in graphs[1].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='blue'),
                opacity=0.2,
            )
        )

    for country in graphs[1].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 0, 255)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 2
    for edge in graphs[2].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='red'),
                opacity=0.2,
            )
        )

    for country in graphs[2].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(255, 0, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 3
    for edge in graphs[3].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='green'),
                opacity=0.2,
            )
        )

    for country in graphs[3].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(0, 255, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 4
    for edge in graphs[4].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='orange'),
                opacity=0.2,
            )
        )

    for country in graphs[4].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(255, 165, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    # Level 5
    for edge in graphs[5].edges:
        loc1 = find_centroids_location(edge[0])
        loc2 = find_centroids_location(edge[1])
        fig.add_trace(
            go.Scattergeo(
                locationmode='ISO-3',
                lon=[loc1[0], loc2[0]],
                lat=[loc1[1], loc2[1]],
                mode='lines',
                line=dict(width=1, color='yellow'),
                opacity=0.2,
            )
        )

    for country in graphs[5].nodes:
        loc = find_centroids_location(country)
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            lon=[loc[0]],
            lat=[loc[1]],
            mode='markers',
            hoverinfo='text',
            text=country,
            marker=dict(
                size=5,
                color='rgb(255, 255, 0)',
                line=dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                )
            )))

    fig.update_layout(title_text='Global Comparison on the Similarities of COVID-19 Policies: '
                                 'Vaccination Policy')

    fig.update_layout(
        showlegend=False,
        geo=go.layout.Geo(
            scope='world',
            showland=True,
            showcountries=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        ),
        height=700,
    )

    fig.update_layout(
        annotations=[
            dict(text="BLACK - "
                      "Level 0: " + messages[0] + " (Total " + str(len(graphs[0].nodes)) + ")", x=0,
                 xref="paper", y=1.085, yref="paper", align="left", showarrow=False),
            dict(text="BLUE - "
                      "Level 1: " + messages[1] + " (Total " + str(len(graphs[1].nodes)) + ")", x=0,
                 xref="paper", y=1.045, yref="paper", align="left", showarrow=False),
            dict(text="RED - "
                      "Level 2: " + messages[2] + " (Total " + str(len(graphs[2].nodes)) + ")",
                 x=0.3, xref="paper", y=1.085, yref="paper", align="left", showarrow=False),
            dict(text="GREEN - "
                      "Level 3: " + messages[3] + " (Total " + str(len(graphs[3].nodes)) + ")",
                 x=0.3, xref="paper", y=1.045, yref="paper", align="left", showarrow=False),
            dict(text="ORANGE - "
                      "Level 4: " + messages[4] + " (Total " + str(len(graphs[4].nodes)) + ")",
                 x=0.9, xref="paper", y=1.085, yref="paper", align="left", showarrow=False),
            dict(text="YELLOW - "
                      "Level 5: " + messages[5] + " (Total " + str(len(graphs[4].nodes)) + ")",
                 x=0.9, xref="paper", y=1.045, yref="paper", align="left", showarrow=False)
        ])

    fig.show()


def visualise(policy: str, graph: WeightedGraph) -> None:
    """Plot and show graphs of countries with the same level of policy.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
        'public-events-cancellation','school-workplace-closures', 'stay-at-home', 'testing-policy',
         'vaccination-policy']
    """
    if policy == 'face-covering-policies':
        lvl0 = convert_policy_to_networkx(graph, policy, 0)
        lvl1 = convert_policy_to_networkx(graph, policy, 1)
        lvl2 = convert_policy_to_networkx(graph, policy, 2)
        lvl3 = convert_policy_to_networkx(graph, policy, 3)
        lvl4 = convert_policy_to_networkx(graph, policy, 4)
        graphs = [lvl0, lvl1, lvl2, lvl3, lvl4]
        plot_face_masks(graphs, get_level_descriptions(policy))
    elif policy in ['public-campaigns-covid', 'public-events-cancellation']:
        lvl0 = convert_policy_to_networkx(graph, policy, 0)
        lvl1 = convert_policy_to_networkx(graph, policy, 1)
        lvl2 = convert_policy_to_networkx(graph, policy, 2)
        graphs = [lvl0, lvl1, lvl2]
        plot_three_levels(graphs, policy, get_level_descriptions(policy))
    elif policy in ['school-workplace-closures', 'stay-at-home', 'testing-policy']:
        lvl0 = convert_policy_to_networkx(graph, policy, 0)
        lvl1 = convert_policy_to_networkx(graph, policy, 1)
        lvl2 = convert_policy_to_networkx(graph, policy, 2)
        lvl3 = convert_policy_to_networkx(graph, policy, 3)
        graphs = [lvl0, lvl1, lvl2, lvl3]
        plot_four_levels(graphs, policy, get_level_descriptions(policy))
    else:
        lvl0 = convert_policy_to_networkx(graph, policy, 0)
        lvl1 = convert_policy_to_networkx(graph, policy, 1)
        lvl2 = convert_policy_to_networkx(graph, policy, 2)
        lvl3 = convert_policy_to_networkx(graph, policy, 3)
        lvl4 = convert_policy_to_networkx(graph, policy, 4)
        lvl5 = convert_policy_to_networkx(graph, policy, 5)
        graphs = [lvl0, lvl1, lvl2, lvl3, lvl4, lvl5]
        plot_vaccination(graphs, get_level_descriptions(policy))


def get_level_descriptions(policy: str) -> dict[int, str]:
    """Return a dict with the level of the policy mapped to its level description.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
        'public-events-cancellation','school-workplace-closures', 'stay-at-home', 'testing-policy',
         'vaccination-policy']

    >>> get_level_descriptions('public-campaigns-covid')[2]
    'Coordinated Public Information Campaigns on Various Platforms'
    """
    messages = {}
    if policy == 'public-campaigns-covid':
        messages[0] = 'No COVID-19 Campaigns'
        messages[1] = 'Officials Urging/Caution'
        messages[2] = 'Coordinated Public Information Campaigns on Various Platforms'
    elif policy == 'public-events-cancellation':
        messages[0] = 'No Requirement'
        messages[1] = 'Recommended Cancelling'
        messages[2] = 'Required Cancelling'
    elif policy == 'stay-at-home':
        messages[0] = 'No Requirement'
        messages[1] = 'Recommended'
        messages[2] = 'Required with Exceptions'
        messages[3] = 'Required with Minimal Exceptions'
    elif policy == 'school-workplace-closures':
        messages[0] = 'No Requirement'
        messages[1] = 'Recommended'
        messages[2] = 'Required Closure for Some Sectors'
        messages[3] = 'Required Closure for Some Sectors, except Essential Services'
    elif policy == 'testing-policy':
        messages[0] = 'No Policy'
        messages[1] = 'Only Those with Specific Criteria'
        messages[2] = 'Anyone with COVID-19 Symptoms'
        messages[3] = 'Open Public Testing'
    elif policy == 'face-covering-policies':
        messages[0] = 'No Policy'
        messages[1] = 'Recommended'
        messages[2] = 'Required in Some Public Spaces'
        messages[3] = 'Required in All Public Spaces'
        messages[4] = 'Required Always'
    else:
        messages[0] = 'No Policy'
        messages[1] = 'Available to one Key Group'
        messages[2] = 'Available to two Key Groups'
        messages[3] = 'Available to all Key Groups'
        messages[4] = 'Partial Additional Availability'
        messages[5] = 'Universal Availability'

    return messages


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'allowed-io': ['find_centroids_location'],
        'extra-imports': ['classes', 'csv', 'networkx', 'plotly.graph_objects'],
        'disable': ['E1136'],
    })
