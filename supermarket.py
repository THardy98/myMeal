import requests
import json
import datetime
import user

class Supermarket:

    place_detail_request = "https://maps.googleapis.com/maps/api/place/details/json?"

    def __init__(self, name, place_id, rating):
        self.__name = name
        self.__place_id = place_id
        self.__rating = rating
        self.__formatted_address = None
        self.__opening_hours = None
        self.__permanently_closed = None
        self.__website = None

    # Method called from a user object, but only pertains to supermarkets so we put it in the supermarket object
    # This is a class/static method
    def supermarket_details(api_key, supermarket_list):
        for supermarket in supermarket_list:
            place_id = { "place_id" : supermarket.get_place_id()}
            fields = { "fields" : "formatted_address,opening_hours,permanently_closed,website"}
            params = { **api_key, **place_id, **fields}
            place_detail_response = requests.get(Supermarket.place_detail_request, params = params)
            detail_dict = json.loads(place_detail_response.text)
            try:
                supermarket.set_formatted_address(detail_dict["result"]["formatted_address"])

            except KeyError as e: # Look into KeyError
                supermarket_list.remove(supermarket)
                continue

                try:
                    supermarket.set_opening_hours(detail_dict["result"]["opening_hours"]["weekday_text"])
                except KeyError as e: # Look into KeyError
                    supermarket_list.remove(supermarket)
                    continue

            # Need to look into KeyErrors and determine whether we want to store "permanently_closed" and "website"
            # Really would not like to have to do nested try/catches, need to find a way to avoid it and add the "permanently_closed" and "website" information


    #########################
    ## Getters and Setters ##
    #########################
    def get_name(self):
        return self.__name

    def get_place_id(self):
        return self.__place_id

    def get_rating(self):
        return self.__rating

    def get_formatted_address(self):
        return self.__formatted_address

    def set_formatted_address(self, formatted_address):
        self.__formatted_address = formatted_address

    def set_opening_hours(self, opening_hours):
        self.__opening_hours = opening_hours

    def set_permanently_closed(self, permanently_closed):
        self.__permanently_closed = permanently_closed

    def set_website(self, website):
        self.__website = website
