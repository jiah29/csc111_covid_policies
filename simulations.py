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
import plotly.graph_objects as go

from classes import WeightedGraph
from computations import get_total_average_case_growth, get_total_average_deaths_growth


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

    prediction = {'Day': [], 'Total_Cases': [], 'Total_Deaths': []}
    day = 0

    while num_pop_left > 0:
        day += 1
        prediction['Day'].append(day)

        if num_not_contracted > 0:
            cumulative_cases = cumulative_cases_deaths('cases', prediction, daily_cases)

            if num_not_contracted <= daily_cases:
                prediction['Total_Cases'].append(num_not_contracted + prediction['Total_Cases'][-1])
                num_not_contracted -= num_not_contracted
            else:
                prediction['Total_Cases'].append(cumulative_cases)
                num_not_contracted -= daily_cases
        else:
            prediction['Total_Cases'].append(prediction['Total_Cases'][-1])

        if prediction['Day'][-1] >= 19:
            cumulative_deaths = cumulative_cases_deaths('deaths', prediction, daily_deaths)

            if num_pop_left < daily_deaths:
                prediction['Total_Deaths'].append(num_pop_left + prediction['Total_Deaths'][-1])
                num_pop_left -= num_pop_left
            else:
                prediction['Total_Deaths'].append(cumulative_deaths)
                num_pop_left -= daily_deaths
        else:
            prediction['Total_Deaths'].append(0)

    dataframe = pd.DataFrame(prediction, columns=['Day', 'Total_Cases', 'Total_Deaths'])
    return dataframe


def cumulative_cases_deaths(category: str, prediction: [str, list], daily_average: int) -> int:
    """Return the cumulative cases/deaths specified by the category argument. This is calculated
    by adding the average daily number of new cases/deaths to the last entry of the list of
    "Total Cases" or "Total Deaths" in the prediction mapping. If the list is empty, simply return
    the daily average.

    Preconditions:
        - 'Total_Cases' in prediction
        - 'Total_Deaths' in prediction
        - category in ['cases', 'deaths']

    >>> sample_dict = {'Day': [1, 2], 'Total_Cases': [100, 120], 'Total_Deaths': [0, 0]}
    >>> cumulative_cases_deaths('cases', sample_dict, 20)
    140
    >>> sample2 = {'Day': [1, 2], 'Total_Cases': [], 'Total_Deaths': [0, 0]}
    >>> cumulative_cases_deaths('cases', sample2, 20)
    20
    """
    if category == 'cases':
        if prediction['Total_Cases'] == []:
            return daily_average
        else:
            return daily_average + prediction['Total_Cases'][-1]
    else:
        if prediction['Total_Deaths'] == []:
            return daily_average
        else:
            return daily_average + prediction['Total_Deaths'][-1]


def plot_simulation(graph: WeightedGraph, policies: dict[str, int]) -> None:
    """Plot the simulation to an animated line graph."""
    data = create_predictions(graph, policies)
    dataframe = data[data['Day'] < 366]

    fig = go.Figure(
        layout=go.Layout(
            updatemenus=[dict(type="buttons", direction="right", x=1.05, y=0.08), ],
            xaxis=dict(range=[1, 365],
                       autorange=False, tickwidth=2,
                       title_text="Day"),
            yaxis=dict(range=[0, int(dataframe.loc[dataframe['Day'] == 365, 'Total_Cases'])],
                       autorange=False,
                       title_text="Total Number of Cases/Deaths")
        ))

    init = 1
    fig.add_trace(go.Scatter(x=dataframe.Day[:init], y=dataframe.Total_Cases[:init],
                             mode='lines',
                             name='Total Cases'))
    fig.add_trace(go.Scatter(x=dataframe.Day[:init], y=dataframe.Total_Deaths[:init],
                             mode='lines',
                             name='Total Deaths'))

    fig.update_layout(title='COVID-19 Simulation for a Year Based on Given Policies',
                      xaxis_title='Day',
                      yaxis_title='Total Number of Cases/Deaths')

    num_cases = str(int(dataframe.loc[dataframe['Day'] == 365, 'Total_Cases']))
    num_deaths = str(int(dataframe.loc[dataframe['Day'] == 365, 'Total_Deaths']))

    fig.update_layout(annotations=[
        dict(text=get_annotations(policies, 'face-covering-policies'), x=0, xref="paper",
             y=1.075, yref="paper", align="left", showarrow=False),
        dict(text=get_annotations(policies, 'public-campaigns-covid'), x=0, xref="paper",
             y=1.045, yref="paper", align="left", showarrow=False),
        dict(text=get_annotations(policies, 'public-events-cancellation'), x=0.22, xref="paper",
             y=1.075, yref="paper", align="left", showarrow=False),
        dict(text=get_annotations(policies, 'school-workplace-closures'), x=0.22, xref="paper",
             y=1.045, yref="paper", align="left", showarrow=False),
        dict(text=get_annotations(policies, 'stay-at-home'), x=0.52, xref="paper",
             y=1.075, yref="paper", align="left", showarrow=False),
        dict(text=get_annotations(policies, 'testing-policy'), x=0.52, xref="paper",
             y=1.045, yref="paper", align="left", showarrow=False),
        dict(text=get_annotations(policies, 'vaccination-policy'), x=0.8, xref="paper",
             y=1.075, yref="paper", align="left", showarrow=False),
        dict(text='<b>Total Number of Cases After 1 Year: </b>' + num_cases, x=1.1, xref="paper",
             y=1.075, yref="paper", align="left", showarrow=False),
        dict(text='<b>Total Number of Deaths After 1 Year: </b>' + num_deaths, x=1.1, xref="paper",
             y=1.045, yref="paper", align="left", showarrow=False)
    ])

    # Animation
    fig.update(frames=[
        go.Frame(
            data=[
                go.Scatter(x=dataframe.Day[:k], y=dataframe.Total_Cases[:k]),
                go.Scatter(x=dataframe.Day[:k], y=dataframe.Total_Deaths[:k])]
        )
        for k in range(init, len(dataframe) + 1)])

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label="Play",
                         method="animate",
                         args=[None, {"frame": {"duration": 50}}])
                ]))])

    fig.show()


def get_annotations(policies: dict[str, int], policy: str) -> str:
    """Return an annotation for the policy to be used in the graph plotting
    given a dict of policies. If the policy is not in policies dict, return "Not Specified"
    instead.

    Preconditions:
        - policy in ['face-covering-policies', 'public-campaigns-covid',
        'public-events-cancellation','school-workplace-closures', 'stay-at-home', 'testing-policy',
         'vaccination-policy']

    >>> get_annotations({'stay-at-home': 2}, 'stay-at-home')
    'stay-at-home: Level 2'
    >>> get_annotations({}, 'stay-at-home')
    'stay-at-home: Not Specified'
    """
    if policy in policies:
        return policy + ': Level ' + str(policies[policy])
    else:
        return policy + ": Not Specified"


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['pandas', 'computations', 'classes', 'plotly.graph_objects']
    })
