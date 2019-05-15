import requests
import json
import datetime
import supermarket

class User:

    geolocation_request = "https://www.googleapis.com/geolocation/v1/geolocate?"
    search_request = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    area_code_request = "https://maps.googleapis.com/maps/api/geocode/json?"

    def __init__(self, api_key):
        self.__lat = None
        self.__lng = None
        self.__latlng = None
        self.__nearby_supermarkets = []
        self.__nearby_area_code = None
        self.geolocate(api_key)
        self.search_supermarkets(api_key)
        self.closest_area(api_key)

    def geolocate(self, api_key):
        geolocation_response = requests.post(User.geolocation_request, params = api_key)
        geolocation_dict = json.loads(geolocation_response.text)
        lat = str(geolocation_dict["location"]["lat"])
        self.set_lat(lat)
        lng = str(geolocation_dict["location"]["lng"])
        self.set_lng(lng)
        self.set_latlng(lat +","+ lng)

    def search_supermarkets(self, api_key):
        latlng = self.get_latlng()
        rankby = { "rankby" : "distance"}
        location = {"location" : latlng}
        type = { "type" : "supermarket"}
        params = {**location, **rankby, **type, **api_key}
        search_response = requests.get(User.search_request, params = params)
        search_dict = json.loads(search_response.text)
        for store in search_dict["results"]:
            try:
                name = store["name"]
                place_id = store["place_id"]
                rating = store["rating"]
                store = supermarket.Supermarket(name, place_id, rating)
                self.add_nearby_supermarkets(store)

            except KeyError as e: # Look into this KeyError
                pass

        nearby_supermarkets = self.get_nearby_supermarkets()
        supermarket.Supermarket.supermarket_details(api_key, nearby_supermarkets)
        # ^ Goes into supermarket module/file, and uses the Class method supermarket_details

    def closest_area(self, api_key):
        supermarket_list = self.get_nearby_supermarkets()
        latlng = {'latlng': self.get_latlng()}
        address = {"address" : supermarket_list[0].get_formatted_address()}
        params = {**latlng, **address, **api_key}
        area_code_response = requests.get(User.area_code_request, params = params)
        area_code_dict = json.loads(area_code_response.text)
        area_code = [dict for dict in area_code_dict["results"][0]["address_components"] if dict["types"] == ["postal_code"]]
        area_code = area_code[0]["long_name"].replace(" ", "")
        #area_code = area_code.replace(" ", "")
        self.set_nearby_area_code(area_code)

    #########################
    ## Getters and Setters ##
    #########################

    #Latitude getter and setter
    def get_lat(self):
        return self.__lat

    def set_lat(self, lat):
        self.__lat = lat

    #Longitude getter and setter
    def get_lng(self):
        return self.__lng

    def set_lng(self, lng):
        self.__lng = lng

    #Latlng getter and setter
    def get_latlng(self):
        return self.__latlng

    def set_latlng(self, latlng):
        self.__latlng = latlng

    #Nearby supermarkets getter and setter
    def get_nearby_supermarkets(self):
        return self.__nearby_supermarkets

    def set_nearby_supermarkets(self, nearby_supermarkets):
        self.__nearby_supermarkets = nearby_supermarkets

    def add_nearby_supermarkets(self, supermarket):
        self.__nearby_supermarkets.append(supermarket)

    #Neaby area code setter and getter
    def get_nearby_area_code(self):
        return self.__nearby_area_code

    def set_nearby_area_code(self, area_code):
        self.__nearby_area_code = area_code
