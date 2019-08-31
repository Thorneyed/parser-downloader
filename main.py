import requests
from html2text import html2text
from bs4 import BeautifulSoup

def main():

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# ввод и разбивка по словам ENG: input and spliting by words
    search_input = input("Input song name: ")
    search = search_input.split()
    
# создание поискового url ENG: creating search url
    url = "http://music.я.ws/search/"+"-".join(search)
    s = requests.Session()
    req = s.get(url, headers=header)

    if not req.status_code == 200:
        print("Something went wrong!", req.status_code)
        s.close()

    else:
        soup = BeautifulSoup(req.text, features="html.parser")

        list_of_elements = soup.find_all("li", limit=50, class_="track")
        list_of_urls = soup.find_all("a", limit=50, class_="playlist-btn-down no-ajaxy")

# вывод номера, длины и назваиния трека ENG: output song numbmer, length and name
        for m in list_of_elements:
            print(str(list_of_elements.index(m)) +" : "+ html2text(m.text))

        track = int(input("Select song number "))
        name_track = html2text(list_of_elements[track].text).split()

        print("Downloading..")
        
#запись в файл ENG: creating file
        with open(name_track[-1]+".mp3", 'wb') as file:
            req = requests.get("http://music.я.ws" + list_of_urls[track].get("href"))
            file.write(req.content)

        print("Done!")
        s.close()


if __name__ == '__main__':
    main()
