# Simple Test Movie Info Crawling

import argparse
import requests as req
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import xlwt
from xlwt import Workbook

wb = Workbook()
sheet1 = wb.add_sheet('MOVIE', cell_overwrite_ok = True)
sheet1.write(0,0,'TITLE')
sheet1.write(0,1,'GENRE')
sheet1.write(0,2,'DATE')
sheet1.write(0,3,'Production')
sheet1.write(0,4,'RUNTIME' )
sheet1.write(0,5,'GRADE')

url_info = "https://www.mycelebs.com/main/movie"

# Chromedriver Option
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')

# Chromedriver
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
driver.get(url_info)

movie_data = BeautifulSoup(driver.page_source, "html.parser").find_all("ol", "theme-finder-vertical-ranking__item-list")

for i in enumerate(movie_data[0:10]):
    sheet1.col(i[0]).width = 6000
    href_src = i[1].find('a').attrs['href']
    driver.get(href_src)
    temp_data = BeautifulSoup(driver.page_source, "html.parser")
    temp_data_title = temp_data.find("div", "top-profile__title").find("h4")
    sheet1.write((i[0]+1), 0, temp_data_title.get_text())
    temp_data_info = temp_data.find("dl","top-profile__info").find_all("dd")
    for _ in enumerate(temp_data_info[0:5]):
        sheet1.write((i[0]+1),(_[0]+1), _[1].get_text())

wb.save('result.xls')