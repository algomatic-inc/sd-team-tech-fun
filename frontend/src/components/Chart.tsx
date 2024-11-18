import type React from "react";
import { useCitizenStore, usePinStore } from "../store";

export const Chart: React.FC = () => {
	const { pin } = usePinStore();
	const { citizens } = useCitizenStore();

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
					<div key={citizen.id} className="space-y-1">
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
