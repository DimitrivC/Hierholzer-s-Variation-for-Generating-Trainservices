"""
analysis.py

This module provides functions to analyze and visualize the results of the services generated
by the algorithm. The functions include generating bar charts of scores and creating graphical 
representations of tracks within a service.

Modules:
    - networkx: Used for creating the graphs.
    - matplotlib.pyplot: Used for creating the bar chart.
    - numpy: Used for creating the bar chart.
    - os: Used for file and directory operations.
    - csv: Used to save the scores to a CSV file.
    - shutil: Used to delete the content of the plots directory if it exists.
"""
import networkx as nx
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import os
import csv
import shutil

def draw_bar_chart(scores, file_path):
    """
    Creates and saves a bar chart representing the distribution of scores.

    Generates a bar chart based on the scores provided and saves the chart
    as a PNG file to the specified file path. The score intervals and categories
    are determined based on the range of the scores.

    Parameters:
        scores (list of float): The list of scores to visualize.
        file_path (str): The path to save the bar chart PNG file.

    Saves:
        bar_chart.png (file): The bar chart representing the distribution of scores.
    """
    bar_chart_file_path = f'{file_path}bar_chart.png'
    minimum = min(scores)
    maximum = max(scores)
    
    if 0.0 <= minimum <= 1.0 and 0.0 <= maximum <= 1.0:
        interval = 0.05
        categories = np.arange(0.0, 1.05, interval)
    else:
        interval = 500
        categories = np.arange(-500, 11000, interval)
        
    num_of_scores_per_cat = [sum(cat <= score < cat + interval for score in scores) \
    for cat in categories]
    objects = [f'{round(cat, 2)}-{round(cat + interval, 2)}' for cat in categories]
    y_pos = np.arange(len(objects))
    
    plt.bar(y_pos, num_of_scores_per_cat, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, rotation=90)
    plt.ylabel('Frequency')
    plt.xlabel('Score')
    plt.title('Scores')
    
    plt.savefig(bar_chart_file_path)

    print(f'Bar chart with scores saved to: {bar_chart_file_path}\n')

def draw_graph(service, graph, file_path):
    """
    Draws and saves visual representations of each track in the service.

    Generates graphical representations of each track within a service. The tracks 
    are drawn on the graph, with different colors and styles to distinguish them.
    The images are saved as PNG files in the specified directory.

    Parameters:
        service: The service object with tracks to visualize.
        graph: The graph object used to generate the service.
        file_path (str): The path to save the PNG files.
    
    Saves:
        track_0.png, track_1.png, ... (files): PNG files representing each track.
    """
    current_directory = os.getcwd()
    graph_file_path = os.path.join(current_directory, file_path, 'plots')

    # delete the contents of the plots directory if it exists to overwrite the files
    if os.path.exists(graph_file_path):
        shutil.rmtree(graph_file_path)
    os.makedirs(graph_file_path)

    G = graph.G

    node_color_map = []
    node_size_map = []
    for node in graph.nodes:
        node_color_map.append(nx.get_node_attributes(G, 'color')[node])
        node_size_map.append(nx.get_node_attributes(G, 'size')[node])

    style = ['dashed', 'dotted', 'dashdot']
    color = ['r', 'b', 'g', 'y']
    color_length = len(color)
    style_length = len(style)
    positions = nx.get_node_attributes(G, 'pos')
    edge_color_map = [nx.get_edge_attributes(G,'color')[edge] for edge in \
    G.edges()]

    for count, track in enumerate(service.tracks):
        plt.clf()
        nx.draw_networkx(G, positions, node_color = node_color_map, node_size = \
        node_size_map, edge_color = edge_color_map, with_labels = False)
        nx.draw_networkx_edges(G, positions, edgelist = track.edges, edge_color = \
            color[count % color_length], style = style[count % style_length], width = 5, arrows = True)
        plt.savefig(os.path.join(graph_file_path, f'track_{count}.png'))

    print(f'Graphs of each track of the service with the highest score are saved to: {file_path}plots/\n')

def scores_to_csv(scores, file_path):
    """
    Saves all given scores of services to a CSV file.

    Parameters:
        scores (list): The scores to save.
        file_path (str): The path to save the CSV file.

    Saves:
        scores.csv (file): CSV file containing all scores.
    """
    csv_file_path = f'{file_path}scores.csv'
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for score in scores:
            writer.writerow([score])
    print(f'The scores of all services have been saved to: {csv_file_path}\n')