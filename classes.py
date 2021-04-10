"""CSC111 Project: Picturing the Power of Policy in a Pandemic

Instructions (READ THIS FIRST!)
===============================

This Python module contains the information and methods of
the two main classes used in this project.

Do not edit any function in this module.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and
instructors of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2021 Jia Hao Choo & Komal Saini.
"""
from __future__ import annotations
from typing import Union


class _WeightedVertex:
    """A vertex in a graph representing a country.

        Instance Attributes:
            - country_name: The name of the country
            - new_cases: The list of number of new cases every day from February 24, 2020
                         to March 13, 2021
            - new_deaths: The list of number of new deaths every day from February 24, 2020
                          to March 13, 2021
            - vaccinations_count: The list of the total number of vaccinations per hundred
                                  every day from February 24, 2020 to March 13, 2021
            - population: The size of the population
            - restrictions_level: The mapping of each policy to its level of restriction
            - similar_policies: The neighbours of the country in the graph, and their corresponding
                                edge weight representing how similar their policies are

        Representation Invariants:
            - self not in self.neighbours
            - all(self in u.neighbours for u in self.neighbours)
    """
    country_name: str
    new_cases: list[float]
    new_deaths: list[float]
    vaccinations_count: list[float]
    population: int
    restrictions_level: dict[str, int]
    similar_policies: dict[_WeightedVertex, Union[int, float]]

    def __init__(self, country: str, cases: list[float],
                 deaths: list[float], population: int) -> None:
        self.country_name = country
        self.new_cases = cases
        self.new_deaths = deaths
        self.population = population
        self.restrictions_level = {}
        self.similar_policies = {}

    def add_restrictions(self, policy: str, level: int):
        """Add the restriction level of a policy to the restrictions_level dict"""
        if policy not in self.restrictions_level:
            self.restrictions_level[policy] = level

    def calculate_weight(self, other: _WeightedVertex) -> float:
        """Calculate the weight of the edge based on how similar the countries' COVID-19
        policies are.

        Preconditions:
            - has_same_policy(self, other) == True
        """
        num_same_level = 0

        for policy in self.similar_policies:
            if self.similar_policies[policy] == other.similar_policies[policy]:
                num_same_level += 1

        return num_same_level / len(self.similar_policies)

    def has_same_policy(self, other: _WeightedVertex) -> bool:
        """Return whether the country has at least one same policy restriction level as
        other's country"""
        for policy in self.similar_policies:
            if self.similar_policies[policy] == other.similar_policies[policy]:
                return True

        return False


class WeightedGraph:
    """A weighted graph representing a network linking countries with similar COVID-19 policies"""
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps a country to its corresponding _WeightedVertex object.
    _vertices: dict[str, _WeightedVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, country: str, cases: list[float],
                   deaths: list[float], population: int) -> None:
        """Add a country weighted vertex to this graph.

        The vertex is not adjacent to any other vertex when added. Do
        nothing if the vertex is already in the graph.
        """
        if country not in self._vertices:
            self._vertices[country] = _WeightedVertex(country, cases, deaths, population)

    def add_vertex_restrictions(self, country: str, policy: str, level: int) -> None:
        """Add the restriction level of a policy to the restrictions_level dict of the vertex.

        If country is not in the graph, do nothing.
        """
        if country in self._vertices:
            self._vertices[country].add_restrictions(policy, level)

    def find_and_add_edge(self, country: str) -> None:
        """Find and add possible edges between the country and all other countries in the graph.
        A edge cam be formed when both countries have similar policy (has at least one same policy
        restriction level).

        If the country is not in the graph, do nothing.

        The main chunk of this function is done in the add_edge helper function. Refer
        to the specification that function for more details.
        """
        if country in self._vertices:
            v1 = self._vertices[country]

            for country2 in self._vertices:
                v2 = self._vertices[country2]
                if v1 != v2:
                    self.add_edge(v1.country_name, v2.country_name)

    def add_edge(self, country1: str, country2: str) -> None:
        """Helper function for find_and_add_edge. This helper function add edge between the
        two countries if the countries have similar policy (has at least one same policy
        restriction level).

        If an edge already exists between two countries, do nothing. The function will also
        call the vertex's calculate_weight method to calculate the weight of the edge.
        """
        v1 = self._vertices[country1]
        v2 = self._vertices[country2]

        if v2 in v1.similar_policies:
            return
        else:
            connection = any(v1.restrictions_level[policy] == v2.restrictions_level[policy]
                             for policy in v1.restrictions_level)

            if connection:
                v1.similar_policies[v2] = v1.calculate_weight(v2)
