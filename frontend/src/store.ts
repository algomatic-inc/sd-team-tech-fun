import { create } from "zustand";
import type { Citizen, CitizenState, MapPin, PinState } from "./types";

interface PinStore extends PinState {
	addPin: (position: { lat: number; lng: number }) => void;
}

interface CitizenStore extends CitizenState {
	addCitizen: (citizen: Citizen) => void;
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

export const useCitizenStore = create<CitizenStore>((set) => ({
	citizens: [],

	addCitizen: (citizen: Citizen) => {
		set((state) => ({ citizens: [...state.citizens, citizen] }));
	},
}));
