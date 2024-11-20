import random

# 緯度経度の範囲を設定
lat_min, lat_max = 37.3760837, 37.4014809  # 緯度の範囲
lng_min, lng_max = 136.8894658, 136.9192275  # 経度の範囲

# ランダム点を10個生成
random_points = [
    (random.uniform(lat_min, lat_max), random.uniform(lng_min, lng_max))
    for _ in range(10)
]

# 生成された点を表示
for i, point in enumerate(random_points, 1):
    print(f"点{i}: 緯度={point[0]:.7f}, 経度={point[1]:.7f}")