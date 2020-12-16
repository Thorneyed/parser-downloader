from html2text import html2text
import requests
from bs4 import BeautifulSoup
import os

def make_con(search_input:str) -> requests.Request:
    """
    Make connection (POST) with site and return object-type "Response"
    """
    search = search_input.split()

    #data slots that needs to make a POST connection

    data = {"do":"search", "subaction":"search", "search_start":0,
            "full_search":0, "result_from":1, "story":"+".join(search)}

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = "http://mp3uk.net/index.php?do=search"

    s = requests.Session()
    req = s.post(url, headers=header, data=data)

    if not req.status_code == 200:
        print("Что-то пошло не так", req.status_code)
        s.close()

    return req


def find_track(req:requests.Request) -> str:
    """
    Generator, returns 50 first names from site
    """
    #we dont need to save all information from site, 'cause number of results
    #can be smaller than 50

    soup = BeautifulSoup(req.text, features="html.parser")
    list_of_elements = soup.find_all("a", limit=50, class_="track-desc fx-1 es-track")

    for m in list_of_elements:
        yield html2text(m.text).rstrip('\n')

def find_url(req:requests.Request, index:int) -> str:
    """
    Analog function "find_track", return download URL of selected track
    """

    soup = BeautifulSoup(req.text, features="html.parser")
    list_of_urls = soup.find_all("a", limit=50, class_="track-dl")

    return list_of_urls[index]

def save_file(filename:str, path:str, req:requests.Request, index:int) -> None:
    """
    Saving content to binary file (.mp3)
    """
    with open(str(path+'/'+filename)+".mp3", 'wb') as file:

        data = requests.get("http://mp3uk.net" + find_url(req, index).get("href"))
        file.write(data.content)
