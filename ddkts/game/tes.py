
import requests

# just a testing file to fetch an image.

def get_cover_image(mbid):
    
  
    # Making a get request 
    response = requests.get(f'https://coverartarchive.org/release/{mbid}')
    data = response.json()
    print(data["images"][0]["image"])
get_cover_image("76df3287-6cda-33eb-8e9a-044b5e15ffdd")
