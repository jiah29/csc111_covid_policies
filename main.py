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
import pickle

from init_graph import get_test_graph
from plot_networks import visualise
from simulations import plot_simulation


if __name__ == '__main__':

    ################################################################################
    # Valid policies & levels for the program
    ################################################################################
    #  'face-covering-policies': level 0 - 4,
    #  'public-campaigns-covid': level 0 - 2,
    #  'public-events-cancellation': level 0 - 2,
    #  'school-workplace-closures': level 0 - 3,
    #  'stay-at-home': level 0 - 3,
    #  'testing-policy': level 0 - 3,
    #  'vaccination-policy': level 0 - 5

    ################################################################################
    # Real datasets
    ################################################################################

    infile = open('datasets/saved_graph', 'rb')

    real_graph = pickle.load(infile)

    # Visualise networks - feel free to uncomment any of the function call below if you
    # do not wish to view the network graph for certain policy.
    visualise('public-events-cancellation', real_graph)
    visualise('face-covering-policies', real_graph)
    visualise('public-campaigns-covid', real_graph)
    visualise('school-workplace-closures', real_graph)
    visualise('stay-at-home', real_graph)
    visualise('testing-policy', real_graph)
    visualise('vaccination-policy', real_graph)

    # Visualise simulation graph - feel free to change the function argument below
    # 1) You can take out any policies from the dict
    # 2) You can change any policy level in the dict
    # (refer to "Valid policies & levels for the program" for a list of valid policies and levels)
    plot_simulation(real_graph, {'public-events-cancellation': 1, 'face-covering-policies': 1,
                                 'public-campaigns-covid': 1, 'school-workplace-closures': 1,
                                 'stay-at-home': 1, 'testing-policy': 1, 'vaccination-policy': 1})

    ################################################################################
    # Test datasets
    ################################################################################

    # Test graph - run this part for shorter run time to generate the complete graph
    # test_graph = get_test_graph()

    # Visualise networks - feel free to uncomment any of the function call below if you
    # do not wish to view the network graph for certain policy.
    # visualise('public-events-cancellation', test_graph)
    # visualise('face-covering-policies', test_graph)
    # visualise('public-campaigns-covid', test_graph)
    # visualise('school-workplace-closures', test_graph)
    # visualise('stay-at-home', test_graph)
    # visualise('testing-policy', test_graph)
    # visualise('vaccination-policy', test_graph)

    # Visualise simulation graph - feel free to change the function argument below
    # 1) You can take out any policies from the dict
    # 2) You can change any policy level in the dict
    # (refer to "Valid policies & levels for the program" for a list of valid policies and levels)
    # plot_simulation(test_graph, {'public-events-cancellation': 1, 'face-covering-policies': 1,
    #                              'public-campaigns-covid': 1, 'school-workplace-closures': 1,
    #                              'stay-at-home': 1, 'testing-policy': 1, 'vaccination-policy': 1})
