## 分析対象

立川市の道路ネットワーク

## データ

### 道路ネットワーク

- Open Street Map から取得した立川市道路ネットワーク

#### ノード（交差点）に含まれる情報

```
{
    y: 緯度,
    x: 経度,
    highway: {
        traffic signals: 信号機,
        crossing: 横断歩道
    },
    street_count: 交差点が繋がる道路の数
}
```

#### エッジ（道路）に含まれる情報

```
{
    osmid: Open Street Map 上の道路 ID,
    name: 道路の名前,
    highway: {
        primary: 大きな街を結ぶ道路,
        secondary: 町を結ぶ道路(primaryの次に重要),
        tertiary: 小さい町や村を結ぶ道路(secondaryの次に重要),
        unclassified: 村や村落を結ぶ道路(最も重要度の低い道路),
        residential: 住宅沿いの道路,
    },
    oneway: 一方通行かどうか(True/False),
    length: 道路の長さ,
    lanes: 車線の数,
    maxspeed: 最高時速,
}
```

### 交通量

[全国道路・街路交通情勢調査](https://www.mlit.go.jp/road/ir/ir-data/ir-data.html)

- 平成 22 年度 全国道路・街路交通情勢調査一般交通量調査 集計表
- 平成 27 年度 全国道路・街路交通情勢調査一般交通量調査 集計表

[交通量統計表 警視庁](https://www.keishicho.metro.tokyo.lg.jp/about_mpd/jokyo_tokei/tokei_jokyo/ryo.html)

- 令和元年 交通量統計表 警視庁
- 令和 2 年 交通量統計表 警視庁

## 分析方法

1. 道路ネットワークの可視化 (ノード：交差点)
2. ネットワークの基本特徴量を算出
3. 交通量をエッジに重み付けし、重みを可視化に反映

#### 基本特徴量

- [x] ノード数
- [x] エッジ数
- [x] 次数のヒストグラム
- [x] 次数分布
- [x] 平均次数
- [x] 平均ノード間距離(道路の長さが距離)
- [ ] ネットワークの直径
- [ ] エッジ密度
- [ ] クラスター係数
- [ ] 平均クラスター係数
- [ ] 次数中心性
- [ ] 固有値中心性
- [ ] 媒介中心性
- [ ] 近接中心性

#### オプション特徴量(意味を見出しにくい)

- [ ] ノード間距離の分布(各距離ごとのノード間距離の平均のグラフ)

### 実行

依存関係のインストール

```
$ pip install -r requirements.txt
```

立川市の道路データを取得

```
$ python3 fetch-road-network.py
```

## 結果
