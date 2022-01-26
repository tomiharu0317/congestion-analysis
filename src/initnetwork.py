import networkx as nx
class InitNetwork:

    # FIXME: __init__でファイルを指定してそこから読み込み
    # G = nx.read_graphml('data/road/tachikawa.graphml')
    G = nx.read_graphml('data/road/target_region_2.graphml')

    def __init__(self):
        length_dict = nx.get_edge_attributes(self.G, name='length')

        # 'length' attributesがstrなのでfloatに変換
        for key, value in length_dict.items():
            length_dict[key] = {'length': round(float(value), 3)}

        nx.set_edge_attributes(self.G, length_dict)