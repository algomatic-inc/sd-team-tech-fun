import type { MapMouseEvent } from "@vis.gl/react-google-maps";
import {
	AdvancedMarker,
	Map as GoogleMap,
	Pin,
} from "@vis.gl/react-google-maps";
import type React from "react";
import { useCitizenStore, usePinStore } from "../store";
import type { Coordinate } from "../types";

export const SatelliteMap: React.FC = () => {
	const { pin, addPin } = usePinStore();
	const { citizens, addCitizen } = useCitizenStore();

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
			const response = await fetch(import.meta.env.VITE_API_URL, options);

			if (response.ok) {
				const result = await response.json();

				for (const res of result.response) {
					addCitizen({
						id: self.crypto.randomUUID(),
						message: res.message,
						score: res.score,
						houseLocation: res.house_location,
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
				{citizens.map((citizen) => {
					return (
						<AdvancedMarker
							key={citizen.id}
							position={{
								lat: citizen.houseLocation.lat,
								lng: citizen.houseLocation.lng,
							}}
						>
							<Pin />
						</AdvancedMarker>
					);
				})}
			</GoogleMap>
		</div>
	);
};
