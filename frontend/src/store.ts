import { create } from "zustand";
import type { MapPin, PinState } from "./types";

interface PinStore extends PinState {
	addPin: (position: { lat: number; lng: number }) => void;
}

export const usePinStore = create<PinStore>((set) => ({
	pin: {
		position: {
			lat: 0,
			lng: 0,
		},
	},

	addPin: (position) => {
		const newPin: MapPin = {
			position,
		};
		set(() => ({ pin: newPin }));
	},
}));
