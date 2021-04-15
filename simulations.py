"""CSC111 Project: Picturing the Power of Policy in a Pandemic

Instructions (READ THIS FIRST!)
===============================

This Python module contains functions that produces a simulation
to visualise how the cases and deaths change overtime in a pandemic when
different level of restrictions/policies are implemented.

Do not edit anything in this module.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and
instructors of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2021 Jia Hao Choo & Komal Saini.
"""
import pandas as pd

from computations import get_total_average_case_growth, get_total_average_deaths_growth
from classes import WeightedGraph


def create_predictions(graph: WeightedGraph, policies: dict[str, int]) -> pd.DataFrame:
    """Create predictions of the total number of daily cases and deaths based on
    the given policies. The result is returned in the form of a pandas dataframe:

    Day | Total Cases | Total Deaths
    ----------------------------------
    1   | 1000        | 0
    2   | 2000        | 0

    The total cases and total deaths are cumulative. The starting population is 7,800,000,000
    (7.8 billion) - the total population on Earth in March 2020, around the time when the pandemic
    starts. Note that the total deaths count will remain 0 until day 19, which is the average
    time to death for coronavirus.

    The simulation will predict how long it take for all 7.8 billion people to die of COVID-19,
    so the dataframe row ends as soon as all 7.8 billion people die. Note that this simulation
    only consider linear growth of number of cases and deaths, which may not be represent the
    real life accurately.
    """
    average_daily_cases = get_total_average_case_growth(graph, policies)
    daily_cases = round(7800000000 * average_daily_cases)
    average_daily_deaths = get_total_average_deaths_growth(graph, policies)
    daily_deaths = round(7800000000 * average_daily_deaths)

    num_pop_left = 7800000000
    num_not_contracted = 7800000000

    prediction = {'Day': [], 'Total Cases': [], 'Total Deaths': []}
    day = 0

    while num_pop_left > 0:
        day += 1
        prediction['Day'].append(day)

        if num_not_contracted > 0:
            cumulative_cases = cumulative_cases_deaths('cases', prediction, daily_cases)

            if num_not_contracted <= daily_cases:
                prediction['Total Cases'].append(num_not_contracted + prediction['Total Cases'][-1])
                num_not_contracted -= num_not_contracted
            else:
                prediction['Total Cases'].append(cumulative_cases)
                num_not_contracted -= daily_cases
        else:
            prediction['Total Cases'].append(prediction['Total Cases'][-1])

        if prediction['Day'][-1] >= 19:
            cumulative_deaths = cumulative_cases_deaths('deaths', prediction, daily_deaths)

            if num_pop_left < daily_deaths:
                prediction['Total Deaths'].append(num_pop_left + prediction['Total Deaths'][-1])
                num_pop_left -= num_pop_left
            else:
                prediction['Total Deaths'].append(cumulative_deaths)
                num_pop_left -= daily_deaths
        else:
            prediction['Total Deaths'].append(0)

    df = pd.DataFrame(prediction, columns=['Day', 'Total Cases', 'Total Deaths'])
    return df


def cumulative_cases_deaths(category: str, prediction: [str, list], daily_average: int) -> int:
    """Return the cumulative cases/deaths specified by the category argument. This is calculated
    by adding the average daily number of new cases/deaths to the last entry of the list of
    "Total Cases" or "Total Deaths" in the prediction mapping. If the list is empty, simply return
    the daily average.

    Preconditions:
        - 'Total Cases' in prediction
        - 'Total Deaths' in prediction
        - category in ['cases', 'deaths']

    >>> sample_dict = {'Day': [1, 2], 'Total Cases': [100, 120], 'Total Deaths': [0, 0]}
    >>> cumulative_cases_deaths('cases', sample_dict, 20)
    140
    >>> sample2 = {'Day': [1, 2], 'Total Cases': [], 'Total Deaths': [0, 0]}
    >>> cumulative_cases_deaths('cases', sample2, 20)
    20
    """
    if category == 'cases':
        if prediction['Total Cases'] == []:
            return daily_average
        else:
            return daily_average + prediction['Total Cases'][-1]
    else:
        if prediction['Total Deaths'] == []:
            return daily_average
        else:
            return daily_average + prediction['Total Deaths'][-1]


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['pandas', 'computations', 'classes']
    })
