import httplib2
import json
import sys
import codecs

# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)

google_api_key = "AIzaSyAMW2M0uVpA5CL6tKfSQH7_S5UInoWY_y0"
foursquare_client_id = "2LJR3NZFSBMRBXGTXTU2RO42GBLDQTLPDW0LY4UK2WDEV2B4"
foursquare_client_secret = "OGZQNAGHDHJFGNJXPJXKCQPTBN132JHVEDE4ODKO3EDKDQEE"

def getGeocodeLocation(inputString):
    location_string = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (location_string, google_api_key))
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    location = result['results'][0]['geometry']['location']
    coords = [location['lat'], location['lng']]
    return coords

# print (getGeocodeLocation("Downingtown, PA"))

def getFirstRestaurant(mealType, location):
    coordinates = getGeocodeLocation(location)
    latlng = str(coordinates[0])+","+str(coordinates[1])
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20190425&query=%s&ll=%s&limit=1' % (foursquare_client_id, foursquare_client_secret, mealType, latlng))
    h = httplib2.Http()
    result = json.loads(h.request(url, "GET")[1])
    firstShop = result['response']['venues'][0]
    # print (firstShop.keys())
    return firstShop

# print (getFirstRestaurant('coffee', "Downingtown, PA"))

def getRestaurantInfo(shopObject):
    venue_id = shopObject['id']
    venue_image = getVenueImage(venue_id)
    venue_name = shopObject['name']
    venue_address = getVenueAddress(shopObject)
    
    print ("\n",venue_name)
    print (venue_address) 
    print (venue_image,"\n")
    return {
        venue_name,
        venue_address,
        venue_image
    }

def getVenueAddress(shopObject):
    address_array = shopObject['location']['formattedAddress']
    venue_address = ""
    for i in address_array:
        venue_address += i + " "
    return venue_address

def getVenueImage(venue_id):
    url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20190425' % (venue_id, foursquare_client_id, foursquare_client_secret))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result['response']['photos']['items']:
        photoObject = result['response']['photos']['items'][0]
        venue_image_url = photoObject['prefix']+"300x300"+photoObject['suffix']
    else: venue_image_url = "https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png"
    return venue_image_url

def findARestaurant(mealType, location):
    return getRestaurantInfo(getFirstRestaurant(mealType, location))
    
# findARestaurant('coffee', "Downingtown, Pennsylvania")

findARestaurant("Pizza", "Tokyo, Japan")
findARestaurant("Tacos", "Jakarta, Indonesia")
findARestaurant("Tapas", "Maputo, Mozambique")
findARestaurant("Falafel", "Cairo, Egypt")
findARestaurant("Spaghetti", "New Delhi, India")
findARestaurant("Cappuccino", "Geneva, Switzerland")
findARestaurant("Sushi", "Los Angeles, California")
findARestaurant("Steak", "La Paz, Bolivia")
findARestaurant("Gyros", "Sydney, Australia")
