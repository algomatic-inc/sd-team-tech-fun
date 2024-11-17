import os
from pathlib import Path

import boto3
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import rasterio.windows as windows
from rasterio.plot import show

# S3の設定
bucket_name = "infrastack-sdimages2ef5ecbb-xxamroebaqha"
tif_file_key = "中解像度衛星データ/光学(Pleades)/tiff/IMG_PHR1A_PMS_202404140150581_ORT_7105349101_R1C1.TIF"
input_dir = Path(__file__).parent / "input"
local_tif_file = input_dir / "tmp.tif"
output_dir = Path(__file__).parent / "output"

tile_height = 1024
tile_width = 1024

os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# S3からTIFFファイルをダウンロード
session = boto3.Session(profile_name="knowledge")
s3 = session.client("s3")
s3.download_file(bucket_name, tif_file_key, local_tif_file)

# rasterioを使用してTIFFファイルを読み込む
with rasterio.open(local_tif_file) as src:
    width = src.width
    height = src.height

    print(f"{width=}, {height=}")
    data = src.read()
    meta = src.meta
    print(meta)
    print(data.shape)

    os.makedirs(output_dir, exist_ok=True)

    # タイル毎に分割
    for row in range(0, height, tile_height):
        for col in range(0, width, tile_width):
            # 分割されたウィンドウのサイズを計算
            window = windows.Window(
                col, row, min(tile_width, width - col), min(tile_height, height - row)
            )

            # タイルのデータを読み込む
            transform = src.window_transform(window)
            tile_data = src.read(window=window)

            # TODO: データが`uint16`だが、uint16 -> uint8に変換するために256で割ると暗すぎるため適当に調整した
            # TODO: tile_dataの最大値が1万くらいっぽい。。。なんで？
            tile_data_normalized = np.clip(tile_data / 32, 0, 255).astype(np.uint8)
            # print(tile_data[0])
            # print(tile_data_normalized[0])

            tile_to_save = tile_data_normalized[:3]

            top_left_x, top_left_y = transform * (0, 0)
            tile_filename = f"{output_dir}/tile_{top_left_x}_{top_left_y}.png"
            # print(f"{tile_filename}")

            plt.imsave(tile_filename, tile_to_save.transpose((1, 2, 0)), cmap="brg")

            # # 新しいメタデータの設定
            # tile_meta = meta.copy()
            # tile_meta.update(
            #     {
            #         "height": tile_data.shape[1],
            #         "width": tile_data.shape[2],
            #         "transform": transform,
            #     }
            # )

            # # タイルのファイル名を作成
            # tile_filename = f"{output_dir}/tile_{row}_{col}.tif"

            # # 新しいTIFFファイルとして保存
            # with rasterio.open(tile_filename, "w", **tile_meta) as dest:
            #     dest.write(tile_data)

    # # 画像を表示
    # show(data[0])  # 1バンド目を表示 (必要に応じてバンドを変更)
    # plt.title("Raster Image")
    # plt.show()

# ローカルファイルの削除（必要に応じて）
# os.remove(local_tif_file)
