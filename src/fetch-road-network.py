from networkx.algorithms.shortest_paths.weighted import all_pairs_dijkstra_path_length
import pandas as pd
import osmnx as ox

class MakeNetwork():

    # query = 'Tachikawa, Tokyo, Japan'
    # type = 'drive'
    def network_from_place(self, query, type):
        G = ox.graph_from_place(query, network_type=type)

        return G

    def network_from_latlng(self, north_lat_place, south_lat_place,
                            east_lng_place, west_lng_place):

        # df = pd.read_csv('data/latlng.csv')
        # north_lat = float(df[df['place'] == north_lat_place]['lat'])
        # south_lat = float(df[df['place'] == south_lat_place]['lat'])
        # east_lng  = float(df[df['place'] == east_lng_place]['lng'])
        # west_lng  = float(df[df['place'] == west_lng_place]['lng'])
        north_lat = float(north_lat_place)
        south_lat = float(south_lat_place)
        east_lng = float(east_lng_place)
        west_lng = float(west_lng_place)
        # 35.71
        # 35.655
        # 139.55
        # 139.33


        G  = ox.graph_from_bbox(north_lat, south_lat, east_lng, west_lng, network_type='drive')

        return G

    def osmnx_graph_to_graphml(self, G, filename):
        ox.save_graphml(G, filepath=filename)

makenet = MakeNetwork()
G = makenet.network_from_latlng(35.73, 35.65, 139.55, 139.33)
makenet.osmnx_graph_to_graphml(G, 'data/road/target_region_2.graphml')