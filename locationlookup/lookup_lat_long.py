import pandas as pd
import requests

# look up in Google
gapi_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
gapi_key = "&key=AIzaSyDVOEHJ-516VD1xOiu-HAafUxgSBjbCXBo"

def gextract_lat_lng(address):
    address_query = gapi_url + address + gapi_key
    response = requests.get(address_query)
    json_response = response.json()
    location = json_response["results"][0]["geometry"]["location"]
    glatitude = location["lat"]
    glongitude = location["lng"]
    return glatitude, glongitude

#look up in Smarty
api_url = "https://us-street.api.smartystreets.com/street-address?street="
api_key = "&key=25517015399508387&license=us-rooftop-geocoding-cloud"


def extract_lat_lng(address):
    address_query = api_url + address + api_key
    response = requests.get(address_query)
    json_response = response.json()
    if len(json_response)>0:
        latitude = json_response[0]["metadata"]["latitude"]
        longitude = json_response[0]["metadata"]["longitude"]
        rdi = json_response[0]["metadata"]["rdi"]
        return latitude, longitude, rdi
    else:
        return 0, 0

df= pd.read_csv('source_addresses.csv')


#populate lat long from both services into dataframe
df[['Latitude', 'Longitude','RDI']] = df['Address'].apply(lambda x: pd.Series(extract_lat_lng(x)))
df[['GLatitude', 'GLongitude']] = df['Address'].apply(lambda x: pd.Series(gextract_lat_lng(x)))

#dump to csv
df.to_csv('results.csv')

    
    



