"""CSC111 Project: Picturing the Power of Policy in a Pandemic

Instructions (READ THIS FIRST!)
===============================

This Python module contains functions that does the computations
on the WeightedGraph for simulations and graphs plotting.

Do not edit anything in this module.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and
instructors of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2021 Jia Hao Choo & Komal Saini.
"""
import random
import statistics
from typing import Optional

from classes import _WeightedVertex, WeightedGraph


def get_new_cases_growth_rate(graph: WeightedGraph, start: Optional[_WeightedVertex],
                              policy: str, level: int, visited: set[_WeightedVertex]) -> float:
    """Return the average daily new cases rate for the specific level of the policy.

    tuple[0]: starting vertex name
    tuple[1]: the average

    This is calculated by traversing through the graph starting from the start vertex without
    visiting any vertex in visited and collecting the average number of new cases for countries
    that meet the specific policy level. The specific weight of each edge will also be taken
    into account (Refer to _WeightedVertex.get_neighbour_average_cases for more details.
    If no start vertex is provided, find a vertex randomly that meets the criteria to begin.

    If there is no country with the specific policy level, calculate the average for
    the level of policy that is one above and one below (if available), then get the average of
    the two.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
            'public-events-cancellation','school-workplace-closures', 'stay-at-home',
            'testing-policy', 'vaccination-policy']
        - 0 <= level <= 6

    >>> g = WeightedGraph()
    >>> g.add_vertex('c1', [0.1], [0.1], 10000)
    >>> g.add_vertex('c2', [0.1], [0.1], 10000)
    >>> g.add_vertex_restrictions('c1', 'face-covering-policies', 2)
    >>> g.add_vertex_restrictions('c2', 'face-covering-policies', 2)
    >>> g.find_and_add_edge('c1')
    >>> average = get_new_cases_growth_rate(g, None, 'face-covering-policies', 2, set())
    >>> average == statistics.mean([0.1/10000 * 1/7, 0.1/10000])
    True
    """
    if start is None:
        for country in graph.get_all_vertices():
            if (graph.get_all_vertices()[country] not in visited) and \
                    (graph.get_all_vertices()[country].restrictions_level[policy] == level):
                start = graph.get_all_vertices()[country]

    if start is None:
        return get_new_cases_special(graph, policy, level)

    lst = start.get_neighbour_averages_cases(policy, level, set())
    lst.append(get_average(start.new_cases) / start.population)

    return get_average(lst)


def get_new_cases_special(graph: WeightedGraph, policy: str, level: int) -> float:
    """Calculate the average new cases for the specific policy level if there is no country
    that meets the criteria. This function will calculate the average new cases for the policy
    by calculating the averages for the policy level that is one higher and one lower, then take
    the average of the two.

    If the policy level above or below is not available, keep going higher or lower
    until finding one that is available.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
            'public-events-cancellation','school-workplace-closures', 'stay-at-home',
            'testing-policy', 'vaccination-policy']
        - 0 <= level <= 6

    >>> g = WeightedGraph()
    >>> g.add_vertex('c1', [0.1], [0.1], 10000)
    >>> g.add_vertex('c2', [0.1], [0.1], 10000)
    >>> g.add_vertex_restrictions('c1', 'face-covering-policies', 2)
    >>> g.add_vertex_restrictions('c2', 'face-covering-policies', 2)
    >>> g.find_and_add_edge('c1')
    >>> average = get_new_cases_special(g, 'face-covering-policies', 0)
    >>> average == statistics.mean([0.1/10000 * 1/7, 0.1/10000])
    True
    """
    vertices = graph.get_all_vertices()

    lower = level
    while lower >= 0:
        available = any(vertices[vertex].restrictions_level[policy] == lower
                        for vertex in vertices)
        if available is True:
            break
        else:
            lower -= 1

    upper_limit = get_upper_limit(policy)

    higher = level
    while higher <= upper_limit:
        available = any(vertices[vertex].restrictions_level[policy] == higher
                        for vertex in vertices)
        if available is True:
            break
        else:
            higher += 1

    if lower == -1:
        return get_new_cases_growth_rate(graph, None, policy, higher, set())
    elif higher > upper_limit:
        return get_new_cases_growth_rate(graph, None, policy, lower, set())
    else:
        lower_bound = get_new_cases_growth_rate(graph, None, policy, lower, set())
        upper_bound = get_new_cases_growth_rate(graph, None, policy, higher, set())
        return get_average([upper_bound, lower_bound])


def get_final_case_average(graph: WeightedGraph, policy: str, level: int) -> float:
    """This function make use of get_new_cases_growth_rate between 5 to 10 times (chosen randomly)
    to get a final average of the number of new cases based on the given policy level.

    This is done because there is an element of randomness for get_new_cases_growth_rate,
    as the starting country for traversal is chosen at random from the dict, and this will affect
    the weight of the edges as the graph is traversed. To mitigate this, we will do
    between 5 - 10 traversals and get the average from it.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
            'public-events-cancellation','school-workplace-closures', 'stay-at-home',
            'testing-policy', 'vaccination-policy']
        - 0 <= level <= 6
    """
    num_times = random.randint(5, 10)

    averages = list()

    for _ in range(num_times):
        returned = get_new_cases_growth_rate(graph, None, policy, level, set())
        averages.append(returned)

    return get_average(averages)


def get_new_deaths_growth_rate(graph: WeightedGraph, start: Optional[_WeightedVertex],
                               policy: str, level: int, visited: set[_WeightedVertex]) -> float:
    """Return the average daily new deaths rate for the specific level of the policy.

    tuple[0]: starting vertex name
    tuple[1]: the average

    This is calculated by traversing through the graph starting from the start vertex without
    visiting any vertex in visited and collecting the average number of new cases for countries
    that meet the specific policy level. The specific weight of each edge will also be taken
    into account (Refer to _WeightedVertex.get_neighbour_average_cases for more details.
    If no start vertex is provided, find a vertex randomly that meets the criteria to begin.

    If there is no country with the specific policy level, calculate the average for
    the level of policy that is one above and one below (if available), then get the average of
    the two.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
            'public-events-cancellation','school-workplace-closures', 'stay-at-home',
            'testing-policy', 'vaccination-policy']
        - 0 <= level <= 6

    >>> g = WeightedGraph()
    >>> g.add_vertex('c1', [0.1], [0.2], 10000)
    >>> g.add_vertex('c2', [0.1], [0.2], 10000)
    >>> g.add_vertex_restrictions('c1', 'face-covering-policies', 2)
    >>> g.add_vertex_restrictions('c2', 'face-covering-policies', 2)
    >>> g.find_and_add_edge('c1')
    >>> average = get_new_deaths_growth_rate(g, None, 'face-covering-policies', 2, set())
    >>> average == statistics.mean([0.2/10000 * 1/7, 0.2/10000])
    True
    """
    if start is None:
        for country in graph.get_all_vertices():
            if (graph.get_all_vertices()[country] not in visited) and \
                    (graph.get_all_vertices()[country].restrictions_level[policy] == level):
                start = graph.get_all_vertices()[country]

    if start is None:
        return get_new_deaths_special(graph, policy, level)

    lst = start.get_neighbour_averages_deaths(policy, level, set())
    lst.append(get_average(start.new_deaths) / start.population)

    return get_average(lst)


def get_new_deaths_special(graph: WeightedGraph, policy: str, level: int) -> float:
    """Calculate the average new cases for the specific policy level if there is no country
    that meets the criteria. This function will calculate the average new cases for the policy
    by calculating the averages for the policy level that is one higher and one lower, then take
    the average of the two.

    If the policy level above or below is not available, keep going higher or lower
    until finding one that is available.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
            'public-events-cancellation','school-workplace-closures', 'stay-at-home',
            'testing-policy', 'vaccination-policy']
        - 0 <= level <= 6

    >>> g = WeightedGraph()
    >>> g.add_vertex('c1', [0.1], [0.2], 10000)
    >>> g.add_vertex('c2', [0.1], [0.2], 10000)
    >>> g.add_vertex_restrictions('c1', 'face-covering-policies', 2)
    >>> g.add_vertex_restrictions('c2', 'face-covering-policies', 2)
    >>> g.find_and_add_edge('c1')
    >>> average = get_new_deaths_special(g, 'face-covering-policies', 0)
    >>> average == statistics.mean([0.2/10000 * 1/7, 0.2/10000])
    True
    """
    vertices = graph.get_all_vertices()

    lower = level
    while lower >= 0:
        available = any(vertices[vertex].restrictions_level[policy] == lower
                        for vertex in vertices)
        if available is True:
            break
        else:
            lower -= 1

    upper_limit = get_upper_limit(policy)

    higher = level
    while higher <= upper_limit:
        available = any(vertices[vertex].restrictions_level[policy] == higher
                        for vertex in vertices)
        if available is True:
            break
        else:
            higher += 1

    if lower == -1:
        return get_new_deaths_growth_rate(graph, None, policy, higher, set())
    elif higher > upper_limit:
        return get_new_deaths_growth_rate(graph, None, policy, lower, set())
    else:
        lower_bound = get_new_deaths_growth_rate(graph, None, policy, lower, set())
        upper_bound = get_new_deaths_growth_rate(graph, None, policy, higher, set())
        return get_average([upper_bound, lower_bound])


def get_final_deaths_average(graph: WeightedGraph, policy: str, level: int) -> float:
    """This function make use of get_new_cases_growth_rate between 5 to 10 times (chosen randomly)
    to get a final average of the number of new cases based on the given policy level.

    This is done because there is an element of randomness for get_new_cases_growth_rate,
    as the starting country for traversal is chosen at random from the dict, and this will affect
    the weight of the edges as the graph is traversed. To mitigate this, we will do
    between 5 - 10 traversals and get the average from it.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
            'public-events-cancellation','school-workplace-closures', 'stay-at-home',
            'testing-policy', 'vaccination-policy']
        - 0 <= level <= 6
    """
    num_times = random.randint(5, 10)

    averages = list()

    for _ in range(num_times):
        returned = get_new_deaths_growth_rate(graph, None, policy, level, set())
        averages.append(returned)

    return get_average(averages)


def get_average(lst: list[float]) -> float:
    """Return the average given a list of floating numbers.

    >>> get_average([1,2,3])
    2.0
    """
    return float(statistics.mean(lst))


def get_upper_limit(policy: str) -> int:
    """Return the upper limit of the policy (the maximum level of the policy).

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
            'public-events-cancellation','school-workplace-closures', 'stay-at-home',
            'testing-policy', 'vaccination-policy']

    >>> get_upper_limit('vaccination-policy')
    6
    """
    if policy == 'face-covering-policies':
        upper_limit = 5
    elif policy in ['public-campaigns-covid', 'public-events-cancellation']:
        upper_limit = 3
    elif policy in ['school-workplace-closures', 'stay-at-home', 'testing-policy']:
        upper_limit = 4
    else:
        upper_limit = 6

    return upper_limit


def get_total_average_case_growth(graph: WeightedGraph, policies: dict[str, int]) -> float:
    """Return the total average new cases every day given a range of policies and their
    respective level in the dict of the form of {policies: level}.

    This is calculated by calculating the case average of each policies, then taking the average
    of that.

    Preconditions:
        - 0 < len(policies) <= 6

    >>> g = WeightedGraph()
    >>> g.add_vertex('c1', [0.1], [0.1], 10000)
    >>> g.add_vertex('c2', [0.1], [0.1], 10000)
    >>> g.add_vertex_restrictions('c1', 'face-covering-policies', 2)
    >>> g.add_vertex_restrictions('c2', 'face-covering-policies', 2)
    >>> g.find_and_add_edge('c1')
    >>> average = get_total_average_case_growth(g, {'face-covering-policies': 2})
    >>> average == statistics.mean([0.1/10000 * 1/7, 0.1/10000])
    True
    """
    growths = []

    for policy in policies:
        growths.append(get_final_case_average(graph, policy, policies[policy]))

    return get_average(growths)


def get_total_average_deaths_growth(graph: WeightedGraph, policies: dict[str, int]) -> float:
    """Return the total average new deaths every day given a range of policies and their
    respective level in the dict of the form of {policies: level}.

    This is calculated by calculating the death average of each policies, then taking the average
    of that.

    Preconditions:
        - 0 < len(policies) <= 6

    >>> g = WeightedGraph()
    >>> g.add_vertex('c1', [0.1], [0.2], 10000)
    >>> g.add_vertex('c2', [0.1], [0.2], 10000)
    >>> g.add_vertex_restrictions('c1', 'face-covering-policies', 2)
    >>> g.add_vertex_restrictions('c2', 'face-covering-policies', 2)
    >>> g.find_and_add_edge('c1')
    >>> average = get_total_average_deaths_growth(g, {'face-covering-policies': 0})
    >>> average == statistics.mean([0.2/10000 * 1/7, 0.2/10000])
    True
    """
    growths = []

    for policy in policies:
        growths.append(get_final_deaths_average(graph, policy, policies[policy]))

    return get_average(growths)


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['statistics', 'random', 'classes']
    })
