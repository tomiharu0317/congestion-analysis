## Analysis target

立川市の道路ネットワーク

## Data

### Road Network

- Open Street Map から取得した立川市道路ネットワーク

### Traffic

[全国道路・街路交通情勢調査](https://www.mlit.go.jp/road/ir/ir-data/ir-data.html)

- 平成 22 年度 全国道路・街路交通情勢調査一般交通量調査 集計表
- 平成 27 年度 全国道路・街路交通情勢調査一般交通量調査 集計表

[交通量統計表 警視庁](https://www.keishicho.metro.tokyo.lg.jp/about_mpd/jokyo_tokei/tokei_jokyo/ryo.html)

- 令和元年 交通量統計表 警視庁
- 令和 2 年 交通量統計表 警視庁

## How to analyze

1. 道路ネットワークの可視化 (ノード：交差点)
2. ネットワークの基本特徴量を算出
3. 交通量をエッジに重み付けし、重みを可視化に反映

## Results

## How to analyze

### Install dependencies

```
$ pip install -r requirements.txt
```

### Analysis

立川市の道路データを取得

```
$ python3 fetch-road-network.py
```
