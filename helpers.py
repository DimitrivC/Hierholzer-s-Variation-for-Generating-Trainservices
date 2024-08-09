"""
helpers.py

This module provides utility functions used across the project.
"""
import os

def clear():
    """
    Clears console screen, using "cls" for Windows and "clear" for Unix-based systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_percentage_critical_edges_traversed(critical_edges_traversed, all_critical_edges):
    """
    Calculates the percentage of traversed critical edges.

    Parameters:
        critical_edges_traversed (list): A list of critical edges that have been traversed.
        all_critical_edges (list): A list of all critical edges.

    Returns:
        float: The percentage of critical edges traversed.
    """
    return len(critical_edges_traversed) / len(all_critical_edges)

def get_score(percen_critical_edges_traversed, track_amount, total_track_time):
    """
    Computes a score based on the percentage of critical edges traversed, the number 
    of tracks, and the total track time. A higher score indicates better performance.
    The score function is taken from: http://heuristieken.nl/wiki/index.php?title=RailNL

    Parameters:
        percen_critical_edges_traversed (float): The percentage of critical edges traversed.
        track_amount (int): The number of tracks.
        total_track_time (int): The total track time.

    Returns:
        float: The computed score.
    """
    return percen_critical_edges_traversed * 10000 - (track_amount * 20 + total_track_time / 100000)

def loading_bar(iteration, total, length=50, update=100):
    """
    Displays a dynamic loading bar to indicate the progress of the algorithm.

    The loading bar updates at fixed intervals or every iteration, depending on 
    the total number of iterations.

    Parameters:
        iteration (int): The current iteration number.
        total (int): The total number of iterations.
        length (int, optional): The length of the loading bar.
        update (int, optional): The number of updates to display the loading bar.
    """
    switch = 100
    
    if total >= switch:
        update_step = total / update
        if iteration % update_step < 1 or iteration == total:
            display_loading_bar(iteration, total, length)
    else:
        display_loading_bar(iteration, total, length)

    if iteration == total:
        print()

def display_loading_bar(iteration, total, length):
    """
    Actually prints the loading bar to the console. This function is called by the
    loading_bar function to display the loading bar.

    Parameters:
        iteration (int): The current iteration number.
        total (int): The total number of iterations.
        length (int): The length of the loading bar.
    """
    iteration += 1
    prefix = "Progress"
    suffix = "Complete"
    decimals = 1
    fill = '█'

    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)

    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
