"""CSC111 Project: Picturing the Power of Policy in a Pandemic

Instructions (READ THIS FIRST!)
===============================

This Python module contains functions that initialise a graph
based on real world data in the datasets folder. It also contains
a exception class that inherits from CountryNotInGraphError class from
classes.py.

Do not edit anything in this module.

Comment out python_ta.contracts.check_all_contracts() with
the function get_real_graph(), else it would take a long time to run since
the sizes of the datasets are huge.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and
instructors of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2021 Jia Hao Choo & Komal Saini.
"""
from typing import Union
import csv
import math
import statistics
from classes import WeightedGraph, CountryNotInGraphError


def convert_data_type(data: str) -> Union[str, float]:
    """Convert a str data to either a float data, or keep it
    as a str data if the data is an empty string.

    >>> convert_data_type('123')
    123.0
    """
    if data == '':
        return data
    else:
        return float(data)


def get_main_data(filename: str, data: str) -> dict[str, list[Union[str, float]]]:
    """Return a mapping of a country to a list of numbers corresponding to the
    data argument from the csv file. Each number either represent the daily new cases
    or new deaths from a specific starting data to March 13, 2021.

    If any data is unavailable, it will be represented with an empty string: ''.

    Preconditions:
        - filename.startswith('datasets/')
        - filename.endswith('.csv')
        - data in ['new_cases', 'new_deaths']

    >>> s = get_main_data('datasets/main_data.csv', 'new_deaths')
    >>> sample = s['Afghanistan']
    >>> len(sample)
    357
    """
    with open(filename) as data_file:
        reader = csv.reader(data_file)

        next(reader)

        return_dict = {}

        if data == 'new_cases':
            for row in reader:
                if row[1] not in return_dict and row[3] != '':
                    return_dict[row[1]] = [convert_data_type(row[3])]
                elif row[1] in return_dict and row[3] != '':
                    return_dict[row[1]].append(convert_data_type(row[3]))
                else:
                    pass
        else:
            for row in reader:
                if row[1] not in return_dict and row[4] != '':
                    return_dict[row[1]] = [convert_data_type(row[4])]
                elif row[1] in return_dict and row[4] != '':
                    return_dict[row[1]].append(convert_data_type(row[4]))
                else:
                    pass

        return return_dict


def get_population(filename: str, country: str) -> int:
    """Get the population of a country from the given file. If country not in filename, raise
    an CountryNotFound error.

    Preconditions:
        - filename.startswith('datasets/')
        - filename.endswith('.csv')

    >>> get_population('datasets/main_data.csv', 'Afghanistan')
    38928341
    """
    with open(filename) as data_file:
        reader = csv.reader(data_file)

        next(reader)

        for row in reader:
            if row[1] == country:
                return int(float(row[5]))

        raise CountryNotFound(country)


def get_policy_restrictions(policy: str, country: str) -> Union[int, str]:
    """Get the average level of restrictions for a specific policy for the country.

    If the data is not available, return ''.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
        'public-events-cancellation','school-workplace-closures', 'stay-at-home', 'testing-policy',
         'vaccination-policy']

    >>> get_policy_restrictions('stay-at-home','Canada')
    1
    >>> get_policy_restrictions('vaccination-policy','Random')
    ''
    >>> get_policy_restrictions('school-workplace-closures','Andorra')
    1
    >>> get_policy_restrictions('public-campaigns-covid', 'Argentina')
    2
    >>> get_policy_restrictions('face-covering-policies', 'Afghanistan')
    2
    """
    levels = []
    filename = 'datasets/' + policy + '.csv'
    with open(filename) as policy_levels:
        reader = csv.reader(policy_levels)

        next(reader)

        for row in reader:
            if row[0] == country:
                levels.append(int(row[3]))

    filtered_levels = []

    for level in levels:
        if level != '':
            filtered_levels.append(level)

    if filtered_levels == []:
        return ''
    else:
        if math.ceil(statistics.mean(filtered_levels)) - statistics.mean(filtered_levels) < 0.5:
            return math.ceil(statistics.mean(filtered_levels))
        else:
            return math.floor(statistics.mean(filtered_levels))


def get_real_graph() -> WeightedGraph:
    """Initialise a WeightedGraph based on real world datasets."""
    countries_cases = get_main_data('datasets/main_data.csv', 'new_cases')
    countries_deaths = get_main_data('datasets/main_data.csv', 'new_deaths')
    graph = WeightedGraph()

    for country in countries_cases:
        population = get_population('datasets/main_data.csv', country)
        graph.add_vertex(country, countries_cases[country], countries_deaths[country], population)

        graph.add_vertex_restrictions(country, 'face-covering-policies',
                                      get_policy_restrictions('face-covering-policies', country))
        graph.add_vertex_restrictions(country, 'public-campaigns-covid',
                                      get_policy_restrictions('public-campaigns-covid', country))
        graph.add_vertex_restrictions(country, 'public-events-cancellation',
                                      get_policy_restrictions('public-events-cancellation',
                                                              country))
        graph.add_vertex_restrictions(country, 'school-workplace-closures',
                                      get_policy_restrictions('school-workplace-closures', country))
        graph.add_vertex_restrictions(country, 'stay-at-home',
                                      get_policy_restrictions('stay-at-home', country))
        graph.add_vertex_restrictions(country, 'testing-policy',
                                      get_policy_restrictions('testing-policy', country))
        graph.add_vertex_restrictions(country, 'vaccination-policy',
                                      get_policy_restrictions('vaccination-policy', country))

    all_vertices = graph.get_all_vertices()

    for country in all_vertices:
        graph.find_and_add_edge(country)

    return graph


def get_modified_graph() -> WeightedGraph:
    """Initialise a WeightedGraph based on a modified, smaller datasets.
    Run this function instead of get_real_graph for quicker run time."""
    # TODO


class CountryNotFound(CountryNotInGraphError):
    """Exceptions raised when the country is not found in a file. This class inherit from
    CountryNotInGraphError"""

    def __init__(self, country: str) -> None:
        CountryNotInGraphError.__init__(self, country)
        self.message = country + ' is not in the file.'


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'allowed-io': ['get_main_data', 'get_population', 'get_policy_restrictions'],
        'extra-imports': ['classes', 'csv', 'math', 'statistics'],
        'disable': ['E1136'],
    })
