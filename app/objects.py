class Locations:
    def __init__(self, locations: dict) -> None:
        self.locations: dict = locations
    
    def __iter__(self) -> list:
        for key, value in self.locations.items():
            yield value["name"]
    
    def Details(self, location_name) -> dict:
        for key, value in self.locations.items():
            if value["name"] == location_name:
                return {key: value}

    def Location(self, location_id: str) -> str:
        location: str = self.locations[location_id]
        return location["name"]
    
    def Id(self, location_name: str) -> str:
        for key, value in self.locations.items():
            if value["name"] == location_name:
                return key

# -----------------------------------------------------------
class Location:
    def __init__(self, location_details: dict, available_fishes: list) -> None:
        self.location: dict = location_details
        self.location_id: str = next(iter(self.location))
        self.location_name: str = self.location[self.location_id]["name"]
        self.badge_id: int = self.location[self.location_id]["badge_id"]
        self.additional_location_type: str | None = self.__AdditionalLocationType()
        self.additional_locations: dict | None = self.__AdditionalLocations()
        self.available_fishes: list = available_fishes

    def __AdditionalLocationType(self) -> str | None:
            if "sublocations" in self.location[self.location_id]:
                return "sublocations"
            elif "special_location" in self.location[self.location_id]:
                return "special_location"
            return None
    
    def __AdditionalLocations(self) -> dict | None:
        if self.additional_location_type:
            return self.location[self.location_id][self.additional_location_type]
        return None
    
    def AdditionalLocations(self) -> list | None:
        if self.additional_locations:
            additional_locations: list = []
            for additional_location in self.additional_locations:
                additional_locations.append(additional_location)
            return additional_locations
        return None
    
    def AvailableFishes(self, additional_location_name) -> list:
        available_fishes: list = []
        additional_location_key: int | list = self.additional_locations[additional_location_name]
        if self.additional_location_type == "sublocations":
            if type(additional_location_key) == list:
                return self.available_fishes
            elif type(additional_location_key) == int:
                for available_fish in self.available_fishes:
                    available_fish_location_ids: int = available_fish["catch_req"]["location_ids"]
                    if additional_location_key in available_fish_location_ids:
                        available_fishes.append(available_fish)
        elif self.additional_location_type == "special_location":
            if type(additional_location_key) == list:
                return self.available_fishes
            elif type(additional_location_key) == int:
                for available_fish in self.available_fishes:
                    try:
                        available_fish_fishing_place: str = available_fish["catch_req"]["fishing_place"]
                    except:
                        available_fish_location_ids: int = available_fish["catch_req"]["location_ids"]
                        if additional_location_key in available_fish_location_ids:
                            available_fishes.append(available_fish)
            else:
                for available_fish in self.available_fishes:
                    try:
                        available_fish_fishing_place: str = available_fish["catch_req"]["fishing_place"]
                        if additional_location_key in available_fish_fishing_place:
                            available_fishes.append(available_fish)
                    except:
                        pass
        return available_fishes

# -----------------------------------------------------------
class Fishes:
    def __init__(self, fishes: list):
        self.fishes: list = fishes
    
    def Fish(self, fish_name: str) -> dict:
        for fish in self.fishes:
            if fish["name"] == fish_name:
                return fish
            
    def AvailableFishes(self, location_id: str | int) -> list:
        available_fishes: list = []
        for fish in self.fishes:
            if int(location_id) == 1:
                fish_location_ids: str = fish["catch_req"]["location_ids"]
                if (int(location_id) in fish_location_ids) or (101 in fish_location_ids):
                    available_fishes.append(fish)
            elif int(location_id) == 5:
                fish_location_ids: str = fish["catch_req"]["location_ids"]
                if (int(location_id) in fish_location_ids) or (104 in fish_location_ids):
                    available_fishes.append(fish)
            else:
                fish_location_ids: str = fish["catch_req"]["location_ids"]
                if int(location_id) in fish_location_ids:
                    available_fishes.append(fish)
        return sorted(available_fishes, key = lambda x: x["name"])

if __name__ == "__main__":
    import json
    
    with open("assets/json/location.json", "r") as file:
        LOCATIONS: dict = json.load(file)
        file.close()


    with open("assets/json/fishao-data.json", "r") as file:
        FISH: dict = json.load(file)
        file.close()
    

    obj = Locations(LOCATIONS)
    obj.Select("Palm Island")
    location_id = obj.Id("Palm Island")
    details = obj.Details()

    av_fish = Fishes(FISH).AvailableFishes(location_id)
    print(Location(details, av_fish).AvailableFishes("All"))