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

    def add_restrictions(self, policy: str, level: int) -> None:
        """Add the restriction level of a policy to the restrictions_level dict"""
        if policy not in self.restrictions_level:
            self.restrictions_level[policy] = level

    def calculate_weight(self, other: _WeightedVertex) -> float:
        """Calculate the weight of the edge based on how similar the countries' COVID-19
        policies are.

        The weight is calculated by (num of same policies level / total num of policies).
        The total number of policies is always 7.

        Preconditions:
            - has_same_policy(self, other) == True

        >>> c1 = _WeightedVertex('Country1', [0.1], [0.1], 100)
        >>> c1.restrictions_level['Policy'] = 2
        >>> c1.restrictions_level['Policy2'] = 3
        >>> c2 = _WeightedVertex('Country2', [0.1], [0.1], 100)
        >>> c2.restrictions_level['Policy'] = 2
        >>> c2.restrictions_level['Policy2'] = 3
        >>> c1.calculate_weight(c2) == 2/7
        True
        """
        num_same_level = 0

        for policy in self.restrictions_level:
            if self.restrictions_level[policy] == other.restrictions_level[policy]:
                num_same_level += 1

        return num_same_level / 7

    def has_same_policy(self, other: _WeightedVertex) -> bool:
        """Return whether the country has at least one same policy restriction level as
        other's country

        >>> c1 = _WeightedVertex('Country1', [0.1], [0.1], 100)
        >>> c1.restrictions_level['Policy'] = 2
        >>> c2 = _WeightedVertex('Country2', [0.1], [0.1], 100)
        >>> c2.restrictions_level['Policy'] = 2
        >>> c1.has_same_policy(c2)
        True
        """
        for policy in self.restrictions_level:
            if self.restrictions_level[policy] == other.restrictions_level[policy]:
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

        >>> s = WeightedGraph()
        >>> s.add_vertex('Country', [0.1], [0.1], 100)
        >>> 'Country' in s._vertices
        True
        >>> s._vertices['Country'].population
        100
        """
        if country not in self._vertices:
            self._vertices[country] = _WeightedVertex(country, cases, deaths, population)

    def add_vertex_restrictions(self, country: str, policy: str, level: int) -> None:
        """Add the restriction level of a policy to the restrictions_level dict of the vertex.

        This function makes use of the _WeightedVertex.restrictions_level method.

        If country is not in the graph, do nothing.

        >>> s = WeightedGraph()
        >>> s.add_vertex('Country', [0.1], [0.1], 100)
        >>> s.add_vertex_restrictions('Country', 'Policy1', 3)
        >>> s._vertices['Country'].restrictions_level['Policy1']
        3
        """
        if country in self._vertices:
            self._vertices[country].add_restrictions(policy, level)

    def find_and_add_edge(self, country: str) -> None:
        """Find and add possible edges between the country and all other countries in the graph.
        A edge can be formed when both countries have similar policy (has at least one same policy
        restriction level).

        If the country is not in the graph, do nothing.

        The main chunk of this function is done in the add_edge helper function. Refer
        to the specification of that function for more details.

        >>> s = WeightedGraph()
        >>> s.add_vertex('Country1', [0.1], [0.1], 100)
        >>> s.add_vertex('Country2', [0.1], [0.1], 100)
        >>> s.add_vertex_restrictions('Country1', 'Policy1', 3)
        >>> s.add_vertex_restrictions('Country2', 'Policy1', 3)
        >>> s.find_and_add_edge('Country1')
        >>> s._vertices['Country2'] in s._vertices['Country1'].similar_policies
        True
        >>> s._vertices['Country1'].similar_policies[s._vertices['Country2']] == 1/7
        True
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

        This function makes use of the _WeightedVertex.has_same_policy method.
        """
        v1 = self._vertices[country1]
        v2 = self._vertices[country2]

        if v2 in v1.similar_policies:
            return
        else:
            connection = v1.has_same_policy(v2)

            if connection:
                v1.similar_policies[v2] = v1.calculate_weight(v2)


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136']
    })
