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
	message: string;
	score: number;
}
