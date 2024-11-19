import type { MapMouseEvent } from "@vis.gl/react-google-maps";
import { AdvancedMarker, Map as GoogleMap } from "@vis.gl/react-google-maps";
import type React from "react";
import { useCitizenStore, usePinStore } from "../store";
import type { Citizen, Coordinate } from "../types";

const NUM_OF_CITIZENS = 6;
const TESTS = [
	"AEONは好き",
	"AEONは嫌い",
	"興味はあるけど距離を気にしている",
	"興味はあるけど混むのが嫌だ",
	"AEONで働きたい",
	"お金がなくて困っている",
];

type CitizenContent = Exclude<Citizen, "id">;

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
				const response = await fetch(import.meta.env.VITE_API_URL, options);

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

	const handleClick = async (e: MapMouseEvent) => {
		if (!e.detail.latLng) {
			console.error("LatLng is undefined");
			return;
		}

		const lat = e.detail.latLng.lat;
		const lng = e.detail.latLng.lng;

		addPin({ lat, lng });
		await updateCitizens({ lat, lng });
	};

	return (
		<div
			className="relative bg-blue-50 border-4 border-blue-200 rounded-lg overflow-hidden cursor-crosshair"
			style={{ width: 800, height: 600 }}
		>
			<GoogleMap
				defaultZoom={14}
				defaultCenter={{ lat: 37.40033202145941, lng: 136.90473918907935 }} // 輪島市付近
				mapId={import.meta.env.VITE_GOOGLE_MAP_ID}
				onClick={handleClick}
				mapTypeId="satellite"
			>
				{pin && (
					<AdvancedMarker
						position={{ lat: pin.position.lat, lng: pin.position.lng }}
					>
						<img
							src="aeon.png"
							alt="AEON"
							className="w-8 h-8 text-red-500 cursor-pointer"
						/>
					</AdvancedMarker>
				)}
			</GoogleMap>
		</div>
	);
};
