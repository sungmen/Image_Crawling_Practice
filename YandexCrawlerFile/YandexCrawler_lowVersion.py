import json
import argparse
import requests as req
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver

#  ex) python YandexCrawler -name dog
parser = argparse.ArgumentParser()
parser.add_argument("-name", "--searchWord", required=True)
args = parser.parse_args()
searchWord = args.searchWord

# Yandex that Parsing Google Image
def YandexImageCrawler():
    url_info = "https://yandex.com/images/search?text="
    
    # Store Image URL to JSON File
    image_json = {"IMAGE":[]}
    json_data = image_json["IMAGE"]

    # Chromedriver Option
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('--disable-gpu')

    # Chromedriver 
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    driver.get(url_info + searchWord)

    for i in range(600):
        driver.execute_script('window.scrollBy(0,10000)')
    
    img_data = BeautifulSoup(driver.page_source,"html.parser").find_all("img")

    for i in enumerate(img_data[1:]):
        try:
            attr_src = "https:" + i[1].attrs['src']
        except KeyError:
            attr_src = "https:" + i[1].attrs['data-src']
        t = urlopen(attr_src).read()
        filename = searchWord+str(i[0]+1)+'.jpg'
        json_data.append({'URL':attr_src})
        with open(filename,"wb") as f:
            f.write(t)

        # ex) print <SEARCH WORD>.jpg : <attr_src>
        print(filename + " : " + attr_src) 
        
    print("Done.")
    # Write ImageURL.json File
    with open('ImageURL.json', 'w') as f:
        json.dump(json_data, f)
    print("Write ImageURL.json")

# Main
if __name__ == "__main__":
    YandexImageCrawler()
