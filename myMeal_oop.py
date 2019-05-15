import requests
import json
import datetime
import user

class myMeal:

    def __init__(self):
        self.__google_maps_api_key = {"key" :"AIzaSyBCaZfJrnuNKZlToNvIEw-e_3dr7Al84IM"}

    def run(self):
        api_key = self.get_api_key()
        test = user.User(api_key)
        print(test.get_nearby_area_code())

        for supermarket in test.get_nearby_supermarkets():
            print(supermarket.get_place_id() + ", " + supermarket.get_name() + ", " + supermarket.get_formatted_address() + ", " + str(supermarket.get_rating()))
        print(len(test.get_nearby_supermarkets()))



    #########################
    ## Getters and Setters ##
    #########################

    def get_api_key(self):
        return self.__google_maps_api_key





def main():
    trial = myMeal()
    trial.run()

main()
