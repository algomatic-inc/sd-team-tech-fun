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
	houseLocation: Coordinate;
	imgUrl: string;
}

export interface CitizenState {
	citizens: Citizen[];
}
