import sys
sys.path.append("../src")

from initnetwork import InitNetwork
from plot import PlotFunc
from plotshortestpath import PlotShortestPath


class TestPlotShortestPath():

    initnet = InitNetwork()
    plot = PlotFunc()
    plot_s_path = PlotShortestPath()

    def __init__(self):
        self.initnet.__init__()

    def test_make_shortest_path_list(self):

        source_node_set = set()
        source_node_set.add("190197656")
        source_node_set.add("190197656")

        target_node = '912045522'

        shortest_path_list = self.plot_s_path.make_shortest_path_list(source_node_set, target_node)

        print(shortest_path_list)

test = TestPlotShortestPath()
test.test_make_shortest_path_list()