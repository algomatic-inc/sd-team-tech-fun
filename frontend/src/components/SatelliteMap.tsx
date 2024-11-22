import type { MapMouseEvent } from "@vis.gl/react-google-maps";
import { AdvancedMarker, Map as GoogleMap } from "@vis.gl/react-google-maps";
import { useCitizenStore, usePinStore } from "../store";
import type { Coordinate } from "../types";
import { SatelliteMapCitizen } from "./SatelliteMapCitizen";
import { useState } from "react";

export const SatelliteMap = () => {
	const { pin, addPin } = usePinStore();
	const { citizens, addCitizen } = useCitizenStore();
	const [loading, setLoading] = useState(false);

	const updateCitizens = async (coord: Coordinate) => {
		const options = {
			method: "POST",
			headers: {
				"Content-Type": "application/json; charset=utf-8",
			},
			body: JSON.stringify({
				lat: coord.lat,
				lng: coord.lng,
			}),
		};

		try {
			setLoading(true);
			const response = await fetch(import.meta.env.VITE_API_URL, options);

			if (response.ok) {
				const result = await response.json();

				for (const res of result) {
					addCitizen({
						id: self.crypto.randomUUID(),
						message: res.message,
						score: res.score,
						houseLocation: res.house_location,
						imgUrl:
							res.score >= 9
								? "man_score_9-10.png"
								: res.score >= 6
									? "man_score_6-8.png"
									: res.score >= 4
										? "man_score_4-5.png"
										: res.score >= 2
											? "man_score_2-3.png"
											: "man_score_0-1.png",
					});
				}
			} else {
				console.error(
					"Failed to fetch data:",
					response.status,
					response.statusText,
				);
			}
		} catch (error) {
			console.error("Error during fetch:", error);
		} finally {
			setLoading(false);
		}
	};

	const handleMapClick = async (e: MapMouseEvent) => {
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
		<div>
			<div className="relative bg-blue-50 border-4 border-blue-200 rounded-lg overflow-hidden cursor-crosshair w-full h-[calc(70vh)]">
				<GoogleMap
					defaultZoom={14}
					defaultCenter={{ lat: 37.40033202145941, lng: 136.90473918907935 }} // 輪島市付近
					mapId={import.meta.env.VITE_GOOGLE_MAP_ID}
					onClick={handleMapClick}
					mapTypeId="satellite"
					mapTypeControl={false}
					zoomControl={false}
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
					{citizens.map((citizen) => (
						<SatelliteMapCitizen key={citizen.id} citizen={citizen} />
					))}
				</GoogleMap>
			</div>
			{loading && (
				<div className="text-white">
					生成AIが、出店箇所付近の住民のお気持ちを考えています...
				</div>
			)}
			{citizens.length > 0 && (
				<div className="text-white">
					{`この箇所に出店した場合の、住民の平均スコア： ${Number(citizens.map((c) => c.score).reduce((a, b) => a + b, 0) / citizens.length).toFixed(2)}`}
				</div>
			)}
		</div>
	);
};
