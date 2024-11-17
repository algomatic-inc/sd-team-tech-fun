import type React from "react";
import { useEffect, useState } from "react";
import { usePinStore } from "../store";
import type { Citizen } from "../types";

const API_URL =
	"https://jtpimcb3u7.execute-api.ap-northeast-1.amazonaws.com/prod";

export const PopulationChart: React.FC = () => {
	const { pin } = usePinStore();
	const [citizens, setCitizens] = useState<Citizen[]>([]);

	async function callGemini() {
		const data = {
			prompt: `
      次の緯度経度にAEONが出店された場合に、その緯度経度付近に住んでいる住民のお気持ちを30文字から50文字程度で考えてください。:
      AEONの出店緯度経度：
      ${pin.position.lat.toFixed(5)}°N, ${pin.position.lng.toFixed(5)}°E
      住民が住んでいる場所の緯度経度：
      ${pin.position.lat.toFixed(5)}°N, ${pin.position.lng.toFixed(5)}°E
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
				citizens.push({
					message: result.response,
					score: Math.floor(Math.random() * 11),
				});
				setCitizens(citizens);
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

	useEffect(() => {
		if (pin) {
			setCitizens([]);
			[...Array(5)].map(() => {
				callGemini();
			});
		}
	}, [pin]);

	return (
		<div className="bg-white p-4 rounded-lg shadow-md">
			<h3 className="text-lg font-semibold mb-4">AEONの出店位置</h3>
			<div className="space-y-2">
				<div className="space-y-1">
					<div className="flex justify-between text-sm">
						<span>
							{pin.position.lat.toFixed(5)}°N, {pin.position.lng.toFixed(5)}°E
						</span>
					</div>
				</div>
			</div>
			<hr />
			<h3 className="text-lg font-semibold mb-4">市民（LLM）のお気持ち</h3>
			<div className="space-y-4">
				{citizens.map((citizen) => (
					<div className="space-y-1">
						<div>
							<p>{citizen.message}</p>
						</div>
						<div className="h-2 bg-gray-100 rounded-full">
							<div
								className="h-full bg-blue-500 transition-all duration-500"
								style={{
									width: `${(citizen.score / 10) * 100}%`,
								}}
							/>
							<div className="text-sm text-right">{citizen.score}</div>
						</div>
					</div>
				))}
			</div>
		</div>
	);
};
