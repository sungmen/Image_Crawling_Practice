import json
import argparse
import requests as req
from urllib.request import Request, urlopen
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
    
    img_data = BeautifulSoup(driver.page_source,"html.parser").find_all("a", "serp-item__link")

    for i in enumerate(img_data[1:]):
        href_src = "https://yandex.com" + i[1].attrs['href']
        driver.get(href_src)
        temp_data = BeautifulSoup(driver.page_source,"html.parser").find_all("img","MMImage-Origin")
        
        try:
            attr_src = temp_data[0].attrs['src']
        except KeyError:
            attr_src = temp_data[0].attrs['data-src']
        request = Request(attr_src, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        t = urlopen(request).read()
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
