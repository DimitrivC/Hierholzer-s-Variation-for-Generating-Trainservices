class Track:
    """
    A class to represent a track in a graph, consisting of a sequence of edges.

    Attributes:
        G (nx.Graph): The graph object representing the network.
        edges (list): A list of edges in the track.
        necessary (bool): A boolean indicating whether the track is necessary, used for optimization.
        time (int): The total time of the track.

    Methods:
        __init__(graph): Initializes the track with a given graph.
        __hash__(): Returns a hash value for the track based on its edges.
        get_time(): Calculates the total time of the track.
        update_time(): Updates the total time of the track.
        add_edge(edge): Adds an edge to the track and updates the total time.
        add_edge_list(edge_list): Sets the edges of the track to the given list of edges.
        remove_last_edge(): Removes the last edge from the track and updates the total time.
    """
    
    def __init__(self, graph):
        """
        Initializes a track object with a given graph.

        Parameters:
            graph: The graph object representing the network.
        """
        self.G = graph.G
        self.edges = []
        self.necessary = True
        self.time = self.get_time()

    def __hash__(self):
        """
        Returns a hash value for the track based on its edges for a quick lookup.

        Returns:
            int: The hash value for the track.
        """
        if self.edges:
            return hash(tuple(self.edges))
        else:
            return 1

    def get_time(self):
        """
        Calculates the total time of the track based on its edges.
        
        Returns:
            int: The total time of the track.
        """
        time = 0
        for i in range(len(self.edges)-1):
            time += self.G[self.edges[i]][self.edges[i+1]]['weight']
        return time

    def update_time(self):
        """
        Updates the total time of the track based on its edges.
        """
        self.time = 0
        for edge in self.edges:
            station_0, station_1 = edge
            self.time += self.G[station_0][station_1]['weight']

    def add_edge(self, edge):
        """
        Adds an edge to the track and updates the total time, if it's the first edge 
        or if it connects to the last station.

        Parameters:
            edge: The edge to be added to the track.
        """
        if not self.edges or self.edges[-1][1] == edge[0]:
            self.edges.append(edge)
            self.update_time()
        else:
            print("Error: Can't add edge because the departing station of the new edge \
            doesn't match the arriving station of the last edge.")

    def add_edge_list(self, edge_list):
        """
        Sets the edges of the track to the given list of edges and updates the total time.

        Parameters:
            edge_list (list): A list of edges to be set as the edges of the track.
        """
        self.edges = edge_list
        self.update_time()

    def remove_last_edge(self):
        """
        Removes the last edge from the track and updates the total time.
        """
        self.edges = self.edges[:-1]
        self.update_time()