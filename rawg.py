import requests
#porta id : 13536

api = 'e31adb2e63854113928b8351b55c0a7f'
api_in_url = '?key=' + api
url = 'https://api.rawg.io/api'

stores = url + '/stores' + api_in_url
game_list = url + '/games' + api_in_url + '&page_size=100'
polrtal = url + '/games/13536' + api_in_url

response = requests.get(polrtal)
print(response.json())