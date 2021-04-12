"""CSC111 Project: Picturing the Power of Policy in a Pandemic

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main functions for users to call and
generate output, or to interact with the program as a whole.

Do not edit any function statements in this module, unless otherwise
specified.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and
instructors of CSC111 at the University of Toronto St. George campus.
All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2021 Jia Hao Choo & Komal Saini.
"""
from init_graph import get_real_graph
from plot_networks import visualise
from computations import get_total_average_case_growth, get_total_average_deaths_growth


if __name__ == '__main__':

    #  lists of policy =
    #  ['face-covering-policies', 'public-campaigns-covid', 'public-events-cancellation',
    #  'school-workplace-closures', 'stay-at-home', 'testing-policy', 'vaccination-policy']

    real_graph = get_real_graph()

    visualise('public-events-cancellation', real_graph)
    visualise('face-covering-policies', real_graph)
    visualise('public-campaigns-covid', real_graph)
    visualise('school-workplace-closures', real_graph)
    visualise('stay-at-home', real_graph)
    visualise('testing-policy', real_graph)
    visualise('vaccination-policy', real_graph)

    # get_total_average_case_growth(real_graph, {'face-covering-policies': 2})
