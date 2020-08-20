import googlemaps, folium, what3words, requests

geocoder = what3words.Geocoder("") #Enter your own What3Words API key here

with open('apikey.txt') as f: #Store your own Googlemaps API Key as a .txt file
    api_key = f.readline()
    f.close()

m = folium.Map(location=[51.540791,-0.023175],tiles='OpenStreetMap',zoom_start=6)#Set your coordinates for where your map view will load and the zoom scale

gmaps = googlemaps.Client(key=api_key)

url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

query = input('Search query: ')

r = requests.get(url + 'query=' + query + '&key=' + api_key)

x = r.json()
for place in x['results']: #Gets information about the search query from Googlemaps(coordinates, name,full address)
    s_place_id = place['place_id']
    s_fields = ['geometry/location','name','formatted_address']
    s_details = gmaps.place(place_id = s_place_id, fields=s_fields)

    name = s_details['result']['name']
    address = s_details['result']['formatted_address']
    slat = s_details['result']['geometry']['location']['lat']
    slng = s_details['result']['geometry']['location']['lng']

    w3a = geocoder.convert_to_3wa(what3words.Coordinates(slat, slng)) #Takes the gmaps coordinates and runs them through the W3W API
    w3as =(list(w3a.values())[-3]) #Outputs just the what3words

    for marker in s_details['result']:
        folium.Marker([slat,slng],popup=name + '\n '+ address + '\n ' + w3as).add_to(m) #assigns the above values to their respective markers on the map

m.save('FinalWeb.html') #Saves search as .html file which can be opened in the browser
