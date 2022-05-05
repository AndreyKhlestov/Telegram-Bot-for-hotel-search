import requests
import json
import re

# my_req = requests.get('')

url = "https://hotels4.p.rapidapi.com/locations/v2/search"

querystring = {"query": 'New York', "locale": "en_US", "currency": "USD"}

headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "85191b6f8amsh16080972da99f1fp1948b6jsn4ddc6a481917"
}

response = requests.request("GET", url, headers=headers, params=querystring)


# pattern = r'(?<="CITY_GROUP",).+?[\]]'
pattern = r'(?<="CITY_GROUP","entities":).+?[\]]'
find = re.search(pattern, response.text)
print(find)
if find:
    data = json.loads(find[0])

    with open('test.json', 'w') as file:
        json.dump(data, file, indent=4)




print(response.text)
