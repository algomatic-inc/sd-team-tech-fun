import type React from "react";
import { useCitizenStore, usePinStore } from "../store";
import type { Citizen, Coordinate } from "../types";

const MAP_WIDTH = 800;
const MAP_HEIGHT = 600;
const TOP_LEFT_LAT = 37.40730236719924;
const TOP_LEFT_LNG = 136.87806752835687;
const BOTTOM_RIGHT_LAT = 37.37787591257921;
const BOTTOM_RIGHT_LNG = 136.91927046609666;
const LAT_DIFF = TOP_LEFT_LAT - BOTTOM_RIGHT_LAT;
const LNG_DIFF = BOTTOM_RIGHT_LNG - TOP_LEFT_LNG;
const API_URL =
	"https://jtpimcb3u7.execute-api.ap-northeast-1.amazonaws.com/prod";
const NUM_OF_CITIZENS = 6;
const TESTS = [
	"AEONは好き", "AEONは嫌い", "興味はあるけど距離を気にしている", "興味はあるけど混むのが嫌だ", "AEONで働きたい", "お金がなくて困っている"
]

type CitizenContent = Exclude<Citizen, "id">

export const SatelliteMap: React.FC = () => {
	const { pin, addPin } = usePinStore();
	const { addCitizen } = useCitizenStore();

	const updateCitizens = async (coord: Coordinate) => {
		// 市民の数だけGeminiとスコアを出力する
		for (let i = 0; i < NUM_OF_CITIZENS; i++) {
			const data = {
				prompt: `
				あなたの役割：
					あなたは、与えられた情報の住民として振舞ってください。
		      次の緯度経度にAEONが出店された場合に、
					その緯度経度付近に住んでいる住民のお気持ちを、30文字から50文字程度で考えてください。
					市民の気持ちのメッセージと、実際に行く確率をスコアとして出力してください。

				情報：
					AEONの出店緯度経度：
     				${coord.lat.toFixed(5)}°N, ${coord.lng.toFixed(5)}°E
     			住民が住んでいる場所の緯度経度：
     				${coord.lat.toFixed(5)}°N, ${coord.lng.toFixed(5)}°E
					住民の情報：
						・男性
						・妻と子どもの3人家族
						・年収600万円
						・週末はドライブに行く
						・${TESTS[i]}

				制約：
					・JSON形式で出力してください
					・messageは30文字から50文字にしてください
					・scoreは0から10までで設定してください
					・scoreは0に近いほどAEONに行きたくなく、10に近いほどAEONに行きたいことを示します

				出力フォーマット：
					{
						message: string,
						score: number
					}
      `,
			};

			const options = {
				method: "POST",
				headers: {
					"Content-Type": "application/json; charset=utf-8",
				},
				body: JSON.stringify(data),
			};

			try {
				const response = await fetch(API_URL, options);

				if (response.ok) {
					const result = await response.json();

					// JSON部分を取り出してパースする
					let jsonObject = {} as CitizenContent;
					const jsonString = result.response.match(/{[\s\S]*}/)?.[0];

					if (jsonString) {
						try {
							jsonObject = JSON.parse(jsonString);
						} catch (error) {
							console.error("JSONのパースに失敗しました:", error);
						}
					} else {
						console.error("JSON部分が見つかりません");
					}

					addCitizen({
						id: self.crypto.randomUUID(),
						message: jsonObject.message,
						score: jsonObject.score,
					});
				} else {
					console.error(
						"Failed to fetch data:",
						response.status,
						response.statusText,
					);
				}
			} catch (error) {
				console.error("Error during fetch:", error);
			}
		}
	};

	const handleMapClick = async (e: React.MouseEvent<HTMLDivElement>) => {
		const rect = e.currentTarget.getBoundingClientRect();
		const x = e.clientX - rect.left;
		const y = e.clientY - rect.top;

		// ピクセル座標 (x, y) から緯度経度を計算
		const lat = TOP_LEFT_LAT - (y / MAP_HEIGHT) * LAT_DIFF;
		const lng = TOP_LEFT_LNG + (x / MAP_WIDTH) * LNG_DIFF;

		addPin({ lat, lng });
		await updateCitizens({ lat, lng });
	};

	const coordinateToPixel = (coord: Coordinate) => {
		// 緯度経度からピクセル座標を計算
		const x = ((coord.lng - TOP_LEFT_LNG) / LNG_DIFF) * MAP_WIDTH;
		const y = ((TOP_LEFT_LAT - coord.lat) / LAT_DIFF) * MAP_HEIGHT;

		return { x, y };
	};

	const { x, y } = coordinateToPixel(pin.position);

	return (
		// biome-ignore lint/a11y/useKeyWithClickEvents: <explanation>
		<div
			className="relative bg-blue-50 border-4 border-blue-200 rounded-lg overflow-hidden cursor-crosshair"
			style={{ width: MAP_WIDTH, height: MAP_HEIGHT }}
			onClick={handleMapClick}
		>
			<div className="absolute inset-0 bg-[url('map.png')] opacity-90" />
			<div className="absolute inset-0 grid grid-cols-12 grid-rows-10">
				{Array.from({ length: 144 }).map((_) => (
					<div
						key={self.crypto.randomUUID()}
						className="border border-blue-100/30"
					/>
				))}
			</div>
			<div
				className="absolute transform -translate-x-1/2 -translate-y-1/2 group"
				style={{ left: x, top: y }}
			>
				<img
					src="aeon.png"
					alt="AEON"
					className="w-8 h-8 text-red-500 cursor-pointer"
				/>
				<div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-white rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity">
					<p className="text-xs text-gray-500">
						{pin.position.lat.toFixed(2)}°N, {pin.position.lng.toFixed(2)}°E
					</p>
				</div>
			</div>
		</div>
	);
};
