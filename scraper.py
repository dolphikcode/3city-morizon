import time
import requests
import numpy as np
from slugify import slugify
from bs4 import BeautifulSoup
import csv
import json
import random

class PageScrapper:

    def __init__(self, url):

        self.url = url
        self.last_page = self.get_last_page_number()
        self.data_dict = {}
        self.licznik = 1

        print(f"Total number of pages: {self.last_page}")

    def get_last_page_number(self):
        page = self.read_page_content(self.url)
        pagination_block = page.find("ul", {"class": "nav nav-pills mz-pagination-number"})
        pagination_hrefs = pagination_block.findAll("a")
        last_page_element = pagination_hrefs[len(pagination_hrefs)-2]
        return int(last_page_element.text)

    def find_advertisements(self):

        #with open(csv_file_name, mode='w') as csv_file:
        #    writer = csv.DictWriter(csv_file, fieldnames=csv_fieldnames, delimiter=';')
        #    writer.writeheader()

            for page_number in range(5):#self.last_page + 1):

                print(f"Page {page_number+1}/{self.last_page} processing...")

                page = self.read_page_content(self.url + f'?page={page_number+1}')
                advertisements = page.findAll("a", {"class": "property_link property-url"})

                for advertisement_index in range(len(advertisements)):
                    data = self.parse_advertisement(advertisements[advertisement_index]['href'])
                    self.data_dict[self.licznik] = data
                    self.licznik += self.licznik
                    print(data)
        #            writer.writerow(data)
                    sleep_time = random.uniform(0.2, 5) #generowanie float z przedzialu od 0.2 do 5
                    time.sleep(sleep_time) #przerwa zeby nie zostac zablokowanym

        #    csv_file.close()

    def parse_advertisement(self, url):

        data = {}

        page = self.read_page_content(url)
        parse_top = page.find('h1').findAll('span')

        data['miasto'] = parse_top[0].get_text().strip().replace(',', '')
        data['dzielnica'] = parse_top[1].get_text().strip().replace(',', '')
        try:
            data['ulica'] = parse_top[2].get_text()#.strip()
        except:
            data['ulica'] = np.nan

        parse_content = page.find("ul", {"class": "list-unstyled list-inline paramIcons"})

        print("=================================")
        print(url)
        print(data['miasto'])
        print(data['dzielnica'])
        print(data['ulica'])

        try:
            data['cena'] = float(parse_content.find("li", {"class": "paramIconPrice"}).find("em").get_text().replace('zł', '').replace(' ', ''))
        except ValueError:
            data['cena'] = np.nan
        print(data['cena'])
        data['powierzchnia'] = float(parse_content.find("li", {"class": "paramIconLivingArea"}).find("em").get_text().strip()[:-3].replace(',', '.'))
        print(data['powierzchnia'])
        try:
            data['cena_m2'] = float(parse_content.find("li", {"class": "paramIconPriceM2"}).find("em").get_text().replace('zł', '').replace(' ', ''))#.strip()[:-3]
            print(data['cena_m2'])
        except:
            data['cena_m2'] = np.NaN

        data['pokoje'] = parse_content.find("li", {"class": "paramIconNumberOfRooms"}).find("em").get_text()#.strip()
        print(data['pokoje'])

        parse_content = page.find("section", {"class": "propertyParams"})
        parse_content2 = parse_content.findAll("tr")

        for tr in range(len(parse_content2)):
            key = parse_content2[tr].find("th").get_text().split(':')[0]
            value = parse_content2[tr].find("td").get_text()
            data[slugify(key)] = value

        try:
            parse_content = page.find("div", {"class": "description"}).findAll('p')
            opis=''
            for i in range (len(parse_content)):
                opis=opis+parse_content[i].get_text()#.replace('m²','').replace('\n','').strip(' ')
            data['tresc']=opis
            print(opis)
        except:
            data['tresc']= np.NaN


        return data

    def read_page_content(self, url):
        page = requests.get(url)
        return BeautifulSoup(page.content, "html.parser")

    def create_json(self):
        with open('data.json', 'w') as fp:
            json.dump(self.data_dict, fp)


URL = 'https://www.morizon.pl/mieszkania/gdansk/'

scraper = PageScrapper(URL)
scraper.find_advertisements()
scraper.create_json()
