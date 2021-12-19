## スケジュール

- [x] 立川市の道路ネットワークを取得・可視化
- [ ] ネットワークの基本特徴量を算出
- [ ] 交通量データを整形
- [ ] 交通量をエッジに重み付け
- [ ] 重み付けネットワークを可視化

## ディレクトリ構成

```
.
├── src
│   ├── fetch-coordinate.py         # 住所から緯度経度を取得
│   ├── fetch-road-network.py       # 道路のネットワークを取得
│   └── analyze-network.py          # ネットワークを分析
├── data
│   ├── latlng.csv                  # 特定の場所の緯度経度
│   └── tachikawa.graphml           # 立川市の道路データ
├── results
│   └── images
│       └── tachikawa.png           # 立川市の道路ネットワーク図
├── docs
│   └── schedule.md                 # ディレクトリ構成・日程など
├── requirements.txt                # インストールするパッケージ
├── README.md                       # 分析に関して
└── .gitignore
```
