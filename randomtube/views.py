from django.shortcuts import render
import rstr
import requests
import random


def home(request):
    return render(request, 'index.html')


def output(request):
    v, title, desc = scoped_random()
    if desc != "error":
        return render(request, 'index.html', {'v': v, 'title': title, 'description': desc})
    else:
        return render(request, 'index.html', {'error': v, 'message': title})


def scoped_random():
    """
     This function will create a search on the youtube api. By randomising the search paramaters
     this function will be able to randomise the video choice.
     Out of the videos returned from the search one will be chosen at random.
    :return: data: dict
    """
    yt_api = 'AIzaSyCreQMZWpIA7ngzKzHd5SOp8drWkVCeAUE'
    order = random.choice(["date", "rating", "relevance", "title"])
    safe_search = random.choice(["strict", "moderate", "none"])
    check_url = 'https://youtube.googleapis.com/youtube/v3/search?safeSearch='+safe_search+'&order='+order+'&maxResults=50&key='+yt_api
    response = requests.get(check_url)
    print(response.status_code)
    data = response.json()
    if "error" in data:
        return data["error"]["code"], data["error"]["message"], 'error'
    else:
        data = data["items"]
        random_choice = random.randint(0,50)
        chosen = data[random_choice]
        v = chosen["id"]["videoId"]
        check_url = 'https://www.googleapis.com/youtube/v3/videos?id=' + v + '&key=' + yt_api + '&part=snippet'
        response = requests.get(check_url)
        data = response.json()
        title = data["items"][0]["snippet"]["title"]
        desc = data["items"][0]["snippet"]["description"]
        return v, title, desc


def completely_random():
    """
    DO NOT USE
    This will run in an endless loop as youtube has too many possible videos that
    don't actually exist in the public domain.
    :return: data: dict
    """

    yt_api = 'AIzaSyCreQMZWpIA7ngzKzHd5SOp8drWkVCeAUE'
    v = rstr.xeger(r'[0-9A-Za-z_-]{10}[048AEIMQUYcgkosw]')
    check_url = 'https://www.googleapis.com/youtube/v3/videos?id=' + v + '&key=' + yt_api + '&part=snippet'
    response = requests.get(check_url)
    data = response.json()
    while data["pageInfo"]["totalResults"] == 0:
        v = rstr.xeger(r'[0-9A-Za-z_-]{10}[048AEIMQUYcgkosw]')
        check_url = 'https://www.googleapis.com/youtube/v3/videos?id=' + v + '&key=' + yt_api + '&part=snippet'
        response = requests.get(check_url)
        data = response.json()
    title = data["items"][0]["snippet"]["title"]
    desc = data["items"][0]["snippet"]["description"]
    return v, title, desc