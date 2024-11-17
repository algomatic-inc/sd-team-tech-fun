import type React from "react";
import { useState } from "react";
import { usePinStore } from "../store";
import type { Coordinate } from "../types";

const MAP_WIDTH = 800;
const MAP_HEIGHT = 600;
const TOP_LEFT_LAT = 37.40730236719924;
const TOP_LEFT_LNG = 136.87806752835687;
const BOTTOM_RIGHT_LAT = 37.37787591257921;
const BOTTOM_RIGHT_LNG = 136.91927046609666;
const LAT_DIFF = TOP_LEFT_LAT - BOTTOM_RIGHT_LAT;
const LNG_DIFF = BOTTOM_RIGHT_LNG - TOP_LEFT_LNG;

export const Map: React.FC = () => {
	const { pin, addPin } = usePinStore();
	const [isDragging, setIsDragging] = useState(false);

	const handleMapClick = (e: React.MouseEvent<HTMLDivElement>) => {
		if (isDragging) return;

		const rect = e.currentTarget.getBoundingClientRect();
		const x = e.clientX - rect.left;
		const y = e.clientY - rect.top;

		// ピクセル座標 (x, y) から緯度経度を計算
		const lat = TOP_LEFT_LAT - (y / MAP_HEIGHT) * LAT_DIFF;
		const lng = TOP_LEFT_LNG + (x / MAP_WIDTH) * LNG_DIFF;

		addPin({ lat, lng });
	};

	const coordinateToPixel = (coord: Coordinate) => {
		// 緯度経度からピクセル座標を計算
		const x = ((coord.lng - TOP_LEFT_LNG) / LNG_DIFF) * MAP_WIDTH;
		const y = ((TOP_LEFT_LAT - coord.lat) / LAT_DIFF) * MAP_HEIGHT;

		return { x, y };
	};

	const { x, y } = coordinateToPixel(pin.position);

	return (
		<div
			className="relative bg-blue-50 border-4 border-blue-200 rounded-lg overflow-hidden cursor-crosshair"
			style={{ width: MAP_WIDTH, height: MAP_HEIGHT }}
			onClick={handleMapClick}
			onMouseDown={() => setIsDragging(false)}
			onMouseMove={() => setIsDragging(true)}
		>
			{/* Stylized map background */}
			<div className="absolute inset-0 bg-[url('map.png')] opacity-90" />

			{/* Grid lines */}
			<div className="absolute inset-0 grid grid-cols-12 grid-rows-10">
				{Array.from({ length: 144 }).map((_, i) => (
					<div key={i} className="border border-blue-100/30" />
				))}
			</div>
			<div
				key={pin.id}
				className="absolute transform -translate-x-1/2 -translate-y-1/2 group"
				style={{ left: x, top: y }}
			>
				<img src="aeon.png" className="w-8 h-8 text-red-500 cursor-pointer" />
				<div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-white rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity">
					<p className="text-xs text-gray-500">
						{pin.position.lat.toFixed(2)}°N, {pin.position.lng.toFixed(2)}°E
					</p>
				</div>
			</div>
		</div>
	);
};
