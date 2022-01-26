## それぞれの`src`ファイルの役割

### `analize-network.py`

- `initnetwork.py`で構築されたネットワークの基本特徴量を算出
- `results/basic_feature_value.csv`に特徴量の名前と値を書き込む

実装されている基本特徴量一覧

- `is_digraph`：有向グラフかどうか
- `num_of_edges`：ノード数

- `num_of_edges`：エッジ数 1（ノードの双方向にエッジが張られている場合は 2 とカウントされる）
- `plot_degree_hist`：次数のヒストグラム（エッジ数 1 に対応）
- `plot_degree_dist`：次数分布（エッジ数 1 に対応）
- `average_degree`：平均次数（エッジ数 1 に対応）

- `未実装`：エッジ数 2（交差点が繋がっている交差点の数をエッジ数とする）
- `plot_street_count_hist`：次数のヒストグラム（エッジ数 2 に対応）
- `plot_street_count_dist`：次数分布（エッジ数 2 に対応）
- `calc_average_street_count`：平均次数（エッジ数 2 に対応）

- `average_path_length`：平均ノード間距離(道路の長さが距離)
- `retrieve_diamter`：ネットワークの直径
- `plot_diameter`：直径のプロット
- `calc_density`：エッジ密度
- `calc_cluster_coefficient`：クラスター係数（重み付き有向グラフには対応しない）
- `calc_avg_cluster_coefficient`：平均クラスター係数（重み付き有向グラフには対応しない）

### `centrality.py`

- `return_centrality_dict`：入次数中心性・出次数中心性・固有値中心性・近接中心性・媒介中心性・ページランクの値を算出
- `save _centrality _to _csv`：ノードと中心性の値を csv に保存
- `sturges_rule`：スタージェスの公式を使い中心性の値から階級数を決定
- `make_different_color_nodes_for_plotly`：階級に基づいてノードに異なる配色をする
- `plot_centrality`：中心性の値に基づいて異なる色でプロット

### `fetch-coordinate.py` （非推奨）

- `fetch_latlng`：場所の名前から緯度経度を取得し、csv に場所の名前と緯度経度を保存

### `fetch-road-network.py`

- `network_from_place`：都道府県、市区町村名から道路ネットワークを作成
- `network_from_latlng`：四端点の名前から csv ファイルで該当の場所の緯度経度を取得し長方形のネットワークを作成
- `osmnx_graph_to_graphml`：道路ネットワークを`graphml`の形で保存

### `initnetwork.py`

- クラス継承時：`graphml`ファイルを読み込んでネットワークを作成
- `__init__`：エッジの`length`を`float`型に変換

### `manipulatecsv.py`

- `write_to_csv`：csv に書き込み
- `retrieve_value_from_csv`：csv からデータを取得
- `write_header_to_csv`：csv ファイルの header を書き込む

※ `analize-network.py`で使われる

### `plot.py`

ネットワークの可視化に共通して使われるコンポーネントのまとめ

- `retrieve_coordinate`：ノードが持つデータのうち緯度経度を取得
- `node_set_to_nodes_for_plotly`：ノードセットからそれぞれのノードの緯度経度を取得し、可視化ツール`plotly`の形に整形
- `edge_set_to_edges_for_plotly`：エッジセットからそれぞれのエッジの緯度経度を取得し整形
- `whole_nodes_for_plotly`：全てのノードを可視化の形に整形
- `whole_edges_for_plotly`：全てのエッジを可視化の形に整形
- `set_color`：階級に基づいて色を指定
- `return_base_layout`：`plotly`で必要となる基本の`layout`を返す
- `plot`：ノード・エッジ・`layout`・`filename`を引数に可視化した図を`html`ファイルとして保存

### `plotmintimepath.py`

最短時間経路を可視化してプロットする際に使われるコンポーネントのまとめ

- `shape_maxspeed`：法定速度を整形
- `add_required_time_attributes`：道路の長さ・法定速度から所要時間を計算し、エッジにデータとして追加
- `retrieve_start_nodes_randomly`：出発地点をランダムに選択
- `plot_min_time_path`：最短時間経路をプロット
- `add_road`：新しい道路を設置
- `plot_new_road`：新しい道路をプロット

### `plotroadnet.py`

- `plot_road_network`：プレーンなネットワークをプロット
- `plot_koushu_kaidou/plot_chuo_expressway/plot_dest`：甲州街道/中央自動車道/目的地を赤くしたネットワークをプロット

### `plotshortestpath.py`

最短経路を可視化してプロットする際に使われるコンポーネントのまとめ

- `retrieve_start_nodes`：特定の緯度以下のノードを出発地点として取得
- `path_list_to_csv`：各出発地点から目的地への最短経路を csv に保存（一回の最短経路算出に時間を要するため、再利用可能にする）
- `make_shortest_path_list`：各出発地点から目的地への最短経路を算出
- `make_edge_used_num_dict`：各出発地点から目的地への最短経路に使われた回数（降順）を`key`、同回数使われたエッジをグループ化したエッジリストとエッジリストの大きさを`value`とした辞書を作成
- `add_different_color_edges_to_data`：エッジリストを`plotly`の形式に整形し、可視化データに追加
- `add_shortest_path_edges_for_plotly`：二つ上で述べた辞書において`key[0]`は最短経路に使われた回数のうち最大のものを表す.これをもとにスタージェスの公式を適用して階級数と階級の幅を決定する.使われた回数と階級値をもとに各階級のエッジリストを作成し、異なる配色をして`plotly`のデータに追加
- `make_shortest_path_list_from_csv`：csv に保存された最短経路を`list`として取得
- `plot_shortest_path`：最短経路をプロット
- `retrieve_motorway_nodes`：中央自動車道の IC となるノードを取得
- `plot_motorway`：中央自動車道の IC となるノードをプロット
