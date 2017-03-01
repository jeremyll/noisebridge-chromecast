from bs4 import BeautifulSoup
import requests

def get_list():
    r = requests.get('https://noisebridge.net/wiki/Background_videos')
    soup = BeautifulSoup(r.content, 'html.parser') 
    paragraphs = soup.find_all('p')
    links = [p.get_text().strip() for p in paragraphs]
    return links


if __name__ == '__main__':
    print(get_list())
