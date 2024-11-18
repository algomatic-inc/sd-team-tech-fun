import { Chart } from "./components/Chart";
import { SatelliteMap } from "./components/SatelliteMap";

export const App = () => {
	return (
		<div className="min-h-screen bg-black p-8">
			<div className="max-w-6xl mx-auto space-y-6">
				<header className="text-center mb-8">
					<h1 className="text-3xl font-bold text-gray-200">SateLLMity</h1>
					<p className="text-gray-400 mt-2">
						AEONを出店したい場所をクリックしてください。
					</p>
				</header>
				<div className="flex gap-4">
					<div className="max-w-full">
						<SatelliteMap />
					</div>
					<div className="min-w-96">
						<Chart />
					</div>
				</div>
			</div>
		</div>
	);
};
