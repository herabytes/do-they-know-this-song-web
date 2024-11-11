import requests 
import json

def get_cover_image(mbid):
    # Making a get request and returns link to image
    response = requests.get(f'https://coverartarchive.org/release/{mbid}')
    data = response.json()
    return (data["images"][0]["image"])

def get_title(mbid):
    # Making a get request and returns link to image
    