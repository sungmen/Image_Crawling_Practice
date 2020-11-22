import requests
import urllib.request
from bs4 import BeautifulSoup
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

url = 'https://www.mycelebs.com/main/movie'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser").find_all("ol","theme-finder-vertical-ranking__item-list")

for i in enumerate(soup[0:10]):
    sheet1.col(i[0]).width = 6000
    href_src = i[1].find('a').attrs['href']
    next_src = requests.get(href_src)
    temp_data = BeautifulSoup(next_src.text, "html.parser")
    temp_data_title = temp_data.find("div", "top-profile__title").find("h4")
    sheet1.write((i[0]+1), 0, temp_data_title.get_text())
    temp_data_info = temp_data.find("dl","top-profile__info").find_all("dd")
    for _ in enumerate(temp_data_info[0:5]):
        sheet1.write((i[0]+1),(_[0]+1), _[1].get_text())

wb.save('result.xls')
