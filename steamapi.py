import requests


def app_details(appid): #get app details
    app_url = 'https://store.steampowered.com/api/appdetails?appids=' + appid
    response = requests.get(app_url).json()
    return response[appid]['data']
def app_reviews(appid): #get app reviews
    reviews_url = 'https://store.steampowered.com/appreviews/' + appid + '?json=1'
    response = requests.get(reviews_url).json()
    return response

class Game :
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.review_score = None
        self.review_score_desc = None
        self.total_reviews = None
        self.developer = None
        self.play_time_last_week = None
        self.price = None
        self.genres = None
        self.tags = None
        self.release_date = None
    def __str__(self):
        return (
            f'''
{self.name}
    Price : {self.price}
    Release date : {self.release_date}
    Developer : {', '.join(self.developer)}
    Review score : {self.review_score_desc}  ({self.review_score})
    Total reviews : {self.total_reviews}            
    Hours played last week : {self.play_time_last_week}   
    Genres : {self.genres}
    ''')
def ask_for_repeat() :
    repeat = input('Do you want to search for another game? (y/n) ')
    if repeat == 'y' or repeat == 'Y' :
        return True
    elif repeat == 'n' or repeat == 'N' :
        print('Goodbye!')
    else :
        print('Invalid input')
        ask_for_repeat()
    return False

def search() :
    amount_of_games = 5
    search_url = 'https://steamcommunity.com/actions/SearchApps/'
    search_prompt = input('Enter the game you want to search for: ')
    search_url += search_prompt
    request = requests.get(search_url).json()
    games = []
    #getting first 5 titles or less
    if len(request) > amount_of_games:
        request = request[:amount_of_games]
    for dict in request :
        games.append(Game(dict['appid'], dict['name']))
    #filling in the details
    for game in games :
        details = app_details(game.id)
        if details['is_free'] :
            game.price = 'Free'
        else :
            try :
                game.price = details['price_overview']['final_formatted']
            except :
                game.price = 'Not available'
        game.release_date = details['release_date']['date']
        game.developer = details['developers']
        game.genres = details['genres']
        genre_string = ''
        for genre in details['genres'] :
            genre_string += genre['description'] + ', '
        game.genres = genre_string[:-2]
        reviews = app_reviews(game.id)
        try :
            game.play_time_last_week = reviews['reviews'][0]['author']['playtime_last_two_weeks']
        except :
            game.play_time_last_week = 'Not available'
        game.review_score = reviews['query_summary']['review_score']
        game.review_score_desc = reviews['query_summary']['review_score_desc']
        game.total_reviews = reviews['query_summary']['total_reviews']
        print(game)
def run() :
    print('Welcome to the Steam API search engine!')
    search()
    repeat = ask_for_repeat()
    while repeat:
        search()
        repeat = ask_for_repeat()

run()