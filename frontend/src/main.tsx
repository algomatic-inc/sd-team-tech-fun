import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App.tsx";
import "./index.css";
import { APIProvider } from "@vis.gl/react-google-maps";

// biome-ignore lint/style/noNonNullAssertion: vite initした時にこの書き方なので、良いでしょう
createRoot(document.getElementById("root")!).render(
	<StrictMode>
		<APIProvider
			apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}
			onLoad={() => console.log("Maps API has loaded.")}
		>
			<App />
		</APIProvider>
	</StrictMode>,
);
