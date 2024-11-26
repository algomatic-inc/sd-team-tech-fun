import {
	AdvancedMarker,
	InfoWindow,
	useAdvancedMarkerRef,
} from "@vis.gl/react-google-maps";
import { useCallback, useState } from "react";
import type { Citizen } from "../types";

interface Props {
	citizen: Citizen;
}

export const SatelliteMapCitizen = (props: Props) => {
	const { citizen } = props;
	const [markerRef, marker] = useAdvancedMarkerRef();
	const [infoWindowShown, setInfoWindowShown] = useState(false);

	const handleMarkerEnter = useCallback(
		() => setInfoWindowShown((isShown) => !isShown),
		[],
	);

	const handleClose = useCallback(() => setInfoWindowShown(false), []);

	return (
		<AdvancedMarker
			ref={markerRef}
			key={citizen.id}
			position={{
				lat: citizen.houseLocation.lat,
				lng: citizen.houseLocation.lng,
			}}
			onMouseEnter={handleMarkerEnter}
			onMouseLeave={handleClose}
		>
			<img
				src={citizen.imgUrl}
				alt={citizen.score.toString()}
				className="w-12 h-12 cursor-pointer"
			/>
			{infoWindowShown && (
				<InfoWindow anchor={marker} onClose={handleClose}>
					<h2>〇〇さん：{citizen.score}点</h2>
					<p>{citizen.message}</p>
					<br />
					<p>年齢：{citizen.age}</p>
					<p>性別：{citizen.gender}</p>
					<p>職業：{citizen.job}</p>
					<p>趣味：{citizen.hobby}</p>
					<p>車がある：{citizen.hasCar ? "あり" : "なし"}</p>
				</InfoWindow>
			)}
		</AdvancedMarker>
	);
};
