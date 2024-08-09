"""
hierholzer_variation.py

This module contains the implementation of a variation of the Hierholzer algorithm
for generating and optimizing services based on a graph representing a network. The
main function, `algo`, generates multiple services, each consisting of tracks that 
traverse the graph. Additional helper functions facilitate the selection of nodes and 
edges, manage the untraversed edges, and optimize the generated services by removing 
unnecessary tracks and combining tracks where appropriate.

Modules:
    - service_class (imported as svc): Contains the Service class for generating services.
    - track_class (imported as trc): Contains the Track class for generating tracks for 
    services.
    - helpers (imported as hlp): Provides helper functions: loading bar, clearing the console.
    - random: Used for selecting random nodes.
    - collections: Used to count untraversed edges.
    - itertools: Used to simplify a loop.
"""
from classes import service_class as svc, track_class as trc
import helpers as hlp
import random
import collections
from itertools import combinations

def algo(graph, max_track_amount, max_track_length, iterator):
    '''
    Executes a variation on Hierholzer's algorithm to generate services.

    Generates a specified number of services, each consisting of tracks that
    traverse the graph based on the given parameters. Tracks are formed by
    choosing random starting nodes that have only one edge and a critical neighbor,
    if available, and then randomly selecting untraversed edges. Services are 
    optimized by removing unnecessary tracks and combining tracks that meet certain
    conditions.

    Parameters:
        graph (grc.Graph): The graph object representing the network.
        max_track_amount (int): The maximum number of tracks allowed per service.
        max_track_length (int): The maximum time allowed per track.
        iterator (int): The number of services to generate.

    Returns:
        list: A list of generated and optimized service objects.

    ''' 
    print(f"======GENERATING {iterator} SERVICES======")

    # initialize loading bar
    length = 50
    update = 1000
    hlp.loading_bar(0, iterator, length, update)

    all_services = []

    # generate 'iterator' amount of services
    for i in range(iterator):
        service = svc.Service(graph)
        untraversed_edges = list(graph.edges)

        # for each track in service
        while untraversed_edges and len(service.tracks) < max_track_amount:
            track = trc.Track(graph)
            current_node = get_one_edge_node(untraversed_edges, graph, service)

            # for each edge in each track
            while True:
                # get all untraversed edges for current node
                remaining_edges = [edge for edge in untraversed_edges if \
                current_node in edge]
                
                if not remaining_edges:
                    if track.time > max_track_length:
                        track, untraversed_edges = edge_again_untraversed(track, untraversed_edges)
                    service.add_track(track)
                    break

                elif track.time > max_track_length:
                    track, untraversed_edges = edge_again_untraversed(track, untraversed_edges)
                    service.add_track(track)
                    track = trc.Track(graph)
                
                else:
                    random_neighbor_node = get_neighbour_with_untraversed_edge(untraversed_edges, \
                    graph, current_node)

                    if (current_node, random_neighbor_node) in untraversed_edges:
                        untraversed_edges.remove((current_node, random_neighbor_node))
                    elif (random_neighbor_node, current_node) in untraversed_edges:
                        untraversed_edges.remove((random_neighbor_node, current_node))

                    track.add_edge((current_node, random_neighbor_node))                    
                    current_node = random_neighbor_node

        # optimization
        new_service = remove_unnecessary_tracks(service, graph)
        newer_service = combine_tracks(new_service, max_track_length, graph)

        all_services.append(newer_service)

        # update loading bar
        hlp.loading_bar(i, iterator, length, update)
    
    hlp.clear()
    print('Done!')
    return all_services

def get_one_edge_node(untraversed_edges, graph, service):
    """
    Selects a node with a single untraversed edge, prioritizing critical edges.

    Identifies nodes that have exactly one untraversed edge, and if available, 
    returns a node that also has a critical neighbor. If no such node exists, 
    it randomly selects a node from the graph.

    Parameters:
        untraversed_edges (list): List of untraversed edges in the graph.
        graph (grc.Graph): The graph object representing the network.
        service (svc.Service): The current service being generated.

    Returns:
        node: A node with one untraversed edge, or a random node if none found.
    """
    untraversed_edges_per_node = collections.Counter([node for edge in untraversed_edges for node in edge])

    nodes_with_one_edge = [node for node, count in untraversed_edges_per_node.items() if count == 1]
    nodes_with_one_edge_and_critical_neighbor = [
        node for node in nodes_with_one_edge if node in service.all_critical_edges
    ]

    if nodes_with_one_edge_and_critical_neighbor:
        return random.choice(nodes_with_one_edge_and_critical_neighbor)
    elif nodes_with_one_edge:
        return random.choice(nodes_with_one_edge)
    else:
        return random.choice(list(graph.nodes))

def get_neighbour_with_untraversed_edge(untraversed_edges, graph, current_node):
    """
    Selects a neighbor of the current node with an untraversed edge.

    Parameters:
        untraversed_edges (list): List of untraversed edges in the graph.
        graph (grc.Graph): The graph object representing the network.
        current_node (node): The current node in the track.
    
    Returns:
        node: A neighbor of the current node with an untraversed edge.
    """
    random_neighbor_node = random.choice(list(graph.G[current_node]))
    while (current_node, random_neighbor_node) not in untraversed_edges \
    and (random_neighbor_node, current_node) not in untraversed_edges:
        random_neighbor_node = random.choice(list(graph.G[current_node]))

    return random_neighbor_node

def edge_again_untraversed(track, untraversed_edges):
    """
    Appends the last edge of the track back to the list of untraversed edges
    and removes the edge from the track.
    
    Parameters:
        track (trc.Track): The track object currently being processed.
        untraversed_edges (list): List of untraversed edges in the graph.
    
    Returns:
        track (trc.Track): The track object with the last edge removed.
        untraversed_edges (list): The list of untraversed edges with the last edge appended.
    """
    untraversed_edges.append(track.edges[-1])
    track.remove_last_edge()

    return track, untraversed_edges

def remove_unnecessary_tracks(service, graph):
    """
    Filters out tracks from the service that do not include any edges marked as 
    critical within the graph.

    Parameters:
        service (svc.Service): The service object to be optimized.
        graph (grc.Graph): The graph object representing the network.
    
    Returns:
        service (svc.Service): The optimized service object.
    """
    service.tracks = [track for track in service.tracks if any(edge in graph.critical_edge_list \
    or tuple(reversed(edge)) in graph.critical_edge_list for edge in track.edges)]

    return service

def combine_tracks(service, max_track_length, graph):
    """
    Combines two tracks into one if certain conditions are met.

    Attempts to combine pairs of tracks within a service if the combined track 
    length does not exceed the maximum track length and the tracks share a 
    starting or ending station (or can be reversed to do so).

    Parameters:
        service (svc.Service): The service object to be optimized.
        max_track_length (int): The maximum time allowed per track.
        graph (grc.Graph): The graph object representing the network.

    Returns:
        service (svc.Service): The optimized service object.
    """
    temp_new_track_list = []

    for track_i, track_j in combinations(service.tracks, 2):
        if (track_i.time + track_j.time) < max_track_length and \
        track_i.edges and track_j.edges: # to prevent index out of range errors
            start_i = track_i.edges[0][0]
            start_j = track_j.edges[0][0]
            end_i = track_i.edges[-1][1]
            end_j = track_j.edges[-1][1]

            if start_i == start_j:
                reversed_j = [tuple(reversed(edge)) for edge in reversed(track_j.edges)]
                combined_tracks = reversed_j + track_i.edges
            elif start_i == end_j:
                combined_tracks = track_j.edges + track_i.edges
            elif end_i == start_j:
                combined_tracks = track_i.edges + track_j.edges
            elif end_i == end_j:
                reversed_i = [tuple(reversed(edge)) for edge in reversed(track_i.edges)]
                combined_tracks = track_j.edges + reversed_i
            else:
                continue

            if combined_tracks not in temp_new_track_list and list(reversed(combined_tracks)) \
            not in temp_new_track_list:
                temp_new_track_list.append(combined_tracks)
                track_i.necessary = False
                track_j.necessary = False

    if temp_new_track_list:
        for track in service.tracks[:]:
            if not track.necessary:
                service.remove_track(track)

        for new_edges in temp_new_track_list:
            new_track = trc.Track(graph)
            new_track.add_edge_list(new_edges)
            service.add_track(new_track)

    return service