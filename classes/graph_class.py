import csv
import networkx as nx

class Graph:
    """
    A class to represent a graph using NetworkX, loaded from CSV files containing 
    nodes and edges.

    Attributes:
        G (nx.Graph): The NetworkX graph instance.
        critical_station_list (list): A list of critical stations in the graph.
        nodes (list): A list of nodes in the graph.
        edges (list): A list of edges in the graph.
        critical_edge_list (list): A list of critical edges in the graph.
    
    Methods:
        __init__(node_file, edge_file): Initializes the graph with nodes and edges from CSV files.
        add_csv_nodes(node_file): Adds nodes from the CSV file to the graph.
        add_csv_edges(edge_file): Adds edges from the CSV file to the graph.
        get_critical_edges(): Returns the critical edges in the graph.
    """

    def __init__(self, node_file, edge_file):
        """
        Initializes the graph object with nodes and edges from the provided CSV files.

        Parameters:
            node_file (str): The path to the CSV file containing node data.
            edge_file (str): The path to the CSV file containing edge data.
        """
        self.G = nx.Graph()

        # load csv files into this specific instance of nx
        self.critical_station_list = self.add_csv_nodes(node_file)
        self.add_csv_edges(edge_file)

        # force iterator object from nx to list
        self.nodes = list(self.G.nodes())
        self.edges = list(self.G.edges())
        self.critical_edge_list = [edge for edge, color in nx.get_edge_attributes(self.G, \
        'color').items() if color == 'r']

    def add_csv_nodes(self, node_file):
        """
        Adds nodes from the CSV file to the graph and identifies critical stations.

        Parameters:
            node_file (str): The path to the CSV file containing node data.

        Returns:
            critical_station_list (list): A list of critical stations in the graph.
        """
        critical_station_list = []

        with open(node_file) as csvfile:
            rows = csv.reader(csvfile)

            for row in rows:
                if row[3] == "Critical":
                    critical_station_list.append(row[0])
                    self.G.add_node(row[0],
                        pos = (float(row[2]), float(row[1])), 
                        color = 'r',
                        size = 40)
                else:
                    self.G.add_node(row[0], 
                        pos = (float(row[2]), float(row[1])),
                        color = 'k',
                        size = 10)

            return critical_station_list

    
    def add_csv_edges(self, edge_file):
        """
        Adds edges from the CSV file to the graph and identifies critical edges.

        Parameters:
            edge_file (str): The path to the CSV file containing edge data.
        """
        with open(edge_file) as csvfile:
            rows = csv.reader(csvfile)

            for row in rows:
                station_0, station_1, weight = row

                if station_0 in self.critical_station_list or station_1 in self.critical_station_list:
                    self.G.add_edge(station_0, station_1, 
                        weight = int(weight), color = 'r', visited = 'n')
                else:
                    self.G.add_edge(station_0, station_1, 
                        weight = int(weight), color = 'k', visited = 'n')

    def get_critical_edges(self):
        """
        Retrieves the list of critical edges in the graph.

        Returns:
            critical_edge_list (list): A list of critical edges in the graph.
        """
        return self.critical_edge_list