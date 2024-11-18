export interface Coordinate {
	lat: number;
	lng: number;
}

export interface MapPin {
	position: Coordinate;
}

export interface PinState {
	pin: MapPin;
}

export interface Citizen {
	id: string;
	message: string;
	score: number;
}

export interface CitizenState {
	citizens: Citizen[];
}