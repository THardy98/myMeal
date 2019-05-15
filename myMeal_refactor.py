import requests
import json
import datetime

#NOTE: Inaccuracy in geolocation due to geolocating via IP address
#      Using closest located supermarket as area code (causing inaccuracy)
#      Mobile version can be implemented with greater accuracy using GPS

def geolocate(api_key):
    geolocation_request = "https://www.googleapis.com/geolocation/v1/geolocate?"
    geolocation_response = requests.post(geolocation_request, params = api_key)
    geolocation_dict = json.loads(geolocation_response.text)
    lat = str(geolocation_dict["location"]["lat"])
    lng = str(geolocation_dict["location"]["lng"])
    latlng = {"latlng" : lat +","+ lng}
    return latlng

def search_supermarkets(api_key, latlng, supermarket_list):
    rankby = { "rankby" : "distance"}
    location = {"location" : latlng["latlng"]}
    type = { "type" : "supermarket"}
    params = {**location, **rankby, **type, **api_key}
    search_request = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    search_response = requests.get(search_request, params = params)
    search_dict = json.loads(search_response.text)
    for store in search_dict["results"]:
        print(store)
        if len(supermarket_list) < 10:
            try:
                supermarket_list.append({ "name" : store["name"], "place_id" : store["place_id"], "rating" : store["rating"]})
            except KeyError as e:
                pass
    return supermarket_list

def supermarket_details(api_key, supermarket_list):
    place_detail_request = "https://maps.googleapis.com/maps/api/place/details/json?"
    for supermarket in supermarket_list:
        place_id = { "place_id" : supermarket["place_id"]}
        fields = { "fields" : "formatted_address,opening_hours,permanently_closed,website"}
        params = { **api_key, **place_id, **fields}
        place_detail_response = requests.get(place_detail_request, params = params)
        detail_dict = json.loads(place_detail_response.text)
        try:
            supermarket["formatted_address"] = detail_dict["result"]["formatted_address"]
        except KeyError as e:
            supermarket_list.remove(supermarket)
            continue
            try:
                supermarket["opening_hours"] = detail_dict["result"]["opening_hours"]["weekday_text"]
            except KeyError as e:
                supermarket_list.remove(supermarket)
                continue

def closest_area(api_key, latlng, supermarket_list):
    address = {"address" : supermarket_list[0]["formatted_address"]}
    params = {**latlng, **address, **api_key}
    area_code_request = "https://maps.googleapis.com/maps/api/geocode/json?"
    area_code_response = requests.get(area_code_request, params = params)
    area_code_dict = json.loads(area_code_response.text)
    area_code = [dict for dict in area_code_dict["results"][0]["address_components"] if dict["types"] == ["postal_code"]]
    area_code = area_code[0]["long_name"]
    area_code = area_code.replace(" ", "")
    return area_code

def get_flyers(area_code):
    flyers_response = requests.get("https://gateflipp.flippback.com/bf/flipp/data?locale=en-us&postal_code=" + area_code)
    dict = json.loads(flyers_response.text)
    flyers = []
    for key in dict["flyers"]:
        if key["valid_from"][:10] > str(datetime.date.today()):
            continue
        if "Groceries" in key["categories"]:
            flyer = {"merchant" : key["merchant"], "id" : key["id"], "valid_to" : key["valid_to"]}
            flyers.append(flyer)
    return flyers

def get_flyer_items(flyers):
    for flyer in flyers:
        items = []
        items_response = requests.get("https://gateflipp.flippback.com/bf/flipp/flyers/" +str(flyer["id"])+ "?locale=en-ca")
        dict = json.loads(items_response.text)
        for item in dict["items"]:
            item = {"name" : item["name"], "id" : item["id"], "price" : item["price"], "discount" : item["discount"]}
            items.append(item)
        flyer["items"] = items

def local_flyers_only(supermarkets, flyers):
    local_stores = [store["name"] for store in supermarkets]
    flyer_stores = [flyer["merchant"] for flyer in flyers]
    for merchant in flyer_stores:
        if merchant not in local_stores:
            for flyer in flyers:
                if flyer["merchant"] == merchant:
                    flyers.remove(flyer)
'''
def product_to_ingr(flyers):
    ingrs = []
    food_api_id = {"app_id" : "010b53d0"}
    food_api_key = {"app_key" : "a28f261e8d4f2c5456fb86f99459a20b"}
    edamam_food_request = "https://api.edamam.com/api/food-database/parser?"
    for item in flyers[0]["items"]:
        ingr = {"ingr" : item["name"]}
        params = {**ingr, **food_api_id, **food_api_key}
        try:
            food_response = requests.get(edamam_food_request, params = params)
            food_dict = json.loads(food_response.text)
            ingrs.append(food_dict["hints"][0]["food"]["label"])
            #print(food_dict["hints"][0]["food"]["label"])
        except Exception as e:
            continue
    return ingrs
'''

def main():
    api_key = {"key": "AIzaSyBCaZfJrnuNKZlToNvIEw-e_3dr7Al84IM"}
    supermarkets = []
    latlng = geolocate(api_key)
    search_supermarkets(api_key, latlng, supermarkets)
    supermarket_details(api_key, supermarkets)
    area_code = closest_area(api_key, latlng, supermarkets)
    flyers = get_flyers(area_code)
    get_flyer_items(flyers)
    local_flyers_only(supermarkets, flyers)
    #ingredients = product_to_ingr(flyers)
    #print(len(flyers[0]["items"]))
    #print(len(ingredients))

    '''
        try:
            for item in flyer["items"]:
                print(item["name"])
        except Exception as e:
            print(e)
        '''

main()
