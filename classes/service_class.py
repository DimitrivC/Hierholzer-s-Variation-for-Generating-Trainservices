import helpers as hlp
import networkx as nx

class Service:
    """
    A class to represent a service consisting of multiple tracks traversing a graph.
    
    Attributes:
        tracks (list): A list of Track objects in the service.
        all_critical_edges (list): A list of all critical edges in the graph.
        critical_edges_traversed (list): A list of critical edges traversed by the service.
        time (int): The total time of all tracks in the service.
        percen_critical_edges_traversed (float): The percentage of critical edges traversed by 
        the service.
        score (float): The score of the service based on the percentage of critical edges 
        traversed, number of tracks, and time taken.

    Methods:
        __init__(graph): Initializes the service with a given graph.
        add_track(track): Adds a track to the service and updates relevant attributes.
        remove_track(track): Removes a track from the service and updates relevant attributes.
        add_traversed_critical_edge(track): Adds the critical edges traversed by a track to the 
        service's record.
        remove_traversed_critical_edge(): Recalculates the list of traversed critical edges based 
        on current tracks.
        update_scores(): Updates the percentage of critical edges traversed and the service's score.
    """
    
    def __init__(self, graph):
        """
        Initializes the service object with a given graph.

        Parameters:
            graph: The graph object representing the network.
        """
        self.tracks = []
        self.all_critical_edges = graph.critical_edge_list
        self.critical_edges_traversed = []
        self.time = 0
        self.percen_critical_edges_traversed = 0
        self.score = 0

    def add_track(self, track):
        """
        Adds a track to the service and updates the service's traversed critical 
        edges, total track time, and score.
        
        Parameters:
            track: The track object to be added to the service.
        """
        self.tracks.append(track)
        self.add_traversed_critical_edge(track)
        self.time = self.time + track.time
        self.update_scores()

    def remove_track(self, track):
        """
        Removes a track from the service and updates the service's traversed critical
        edges, total track time, and score.

        Parameters:
            track: The track object to be removed from the service.
        """
        self.tracks.remove(track)
        self.remove_traversed_critical_edge()
        self.time -= track.time
        self.update_scores()

    def add_traversed_critical_edge(self, track):
        """
        Adds the critical edges traversed by a track to the service's record.

        Parameters:
            track: The track object currently being processed.
        """
        for edge in track.edges:
            if edge in self.all_critical_edges or (edge[1], edge[0]) in self.all_critical_edges:
                if edge not in self.critical_edges_traversed and (edge[1], edge[0]) not in self.critical_edges_traversed:
                    self.critical_edges_traversed.append(edge)

    def remove_traversed_critical_edge(self):
        """
        Recalculates the list of traversed critical edges based on the current tracks in the service.
        """
        self.critical_edges_traversed.clear()
        for track in self.tracks:
            self.add_traversed_critical_edge(track)

    def update_scores(self):
        """
        Updates the percentage of critical edges traversed and the service's score.
        """
        self.percen_critical_edges_traversed = hlp.get_percentage_critical_edges_traversed(self.critical_edges_traversed, \
            self.all_critical_edges)
        self.score = hlp.get_score(self.percen_critical_edges_traversed, len(self.tracks),self.time)