import osmnx as ox

query = 'Tachikawa, Tokyo, Japan'
type = 'drive'

G = ox.graph_from_place(query, network_type=type)

ox.save_graphml(G, filepath='data/road/tachikawa.graphml')
ox.plot_graph(G, save=True, filepath='docs/images/tachikawa.png')