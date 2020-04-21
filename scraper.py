import time
import requests
from slugify import slugify
from bs4 import BeautifulSoup
import csv

class PageScrapper:

    def __init__(self, url):

        self.url = url
        self.last_page = self.get_last_page_number()

        print(f"Total number of pages: {self.last_page}")

    def get_last_page_number(self):
        page = self.read_page_content(self.url)
        pagination_block = page.find("ul", {"class": "nav nav-pills mz-pagination-number"})
        pagination_hrefs = pagination_block.findAll("a")
        last_page_element = pagination_hrefs[len(pagination_hrefs)-2]
        return int(last_page_element.text)

    def find_advertisements(self):

        with open(csv_file_name, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_fieldnames, delimiter=';')
            writer.writeheader()

            for page_number in range(self.last_page + 1):

                print(f"Page {page_number+1}/{self.last_page} processing...")

                page = self.read_page_content(self.url + f'?page={page_number+1}')
                advertisements = page.findAll("a", {"class": "property_link property-url"})

                for advertisement_index in range(len(advertisements)):
                    data = self.parse_advertisement(advertisements[advertisement_index]['href'])
                    print(data)
                    writer.writerow(data)
                    time.sleep(1)

            csv_file.close()

    def parse_advertisement(self, url):

        data = {}

        page = self.read_page_content(url)
        parse_top = page.find('h1').findAll('span')

        data['miasto'] = parse_top[0].get_text().strip()[:-1]
        data['dzielnica'] = parse_top[1].get_text().strip()[:-1]
        try:
            data['ulica'] = parse_top[2].get_text().strip()
        except:
            data['ulica'] = ''

        parse_content = page.find("ul", {"class": "list-unstyled list-inline paramIcons"})

        print("=================================")
        print(url)
        print(data['miasto'])
        print(data['dzielnica'])
        print(data['ulica'])

        data['cena'] = parse_content.find("li", {"class": "paramIconPrice"}).find("em").get_text().strip()[:-3]
        print(data['cena'])
        data['powierzchnia'] = parse_content.find("li", {"class": "paramIconLivingArea"}).find("em").get_text().strip()[:-3]
        print(data['powierzchnia'])
        try:
            data['cena_m2'] = parse_content.find("li", {"class": "paramIconPriceM2"}).find("em").get_text().strip()[:-3]
            print(data['cena_m2'])
        except:
            data['cena_m2'] = ''

        data['pokoje'] = parse_content.find("li", {"class": "paramIconNumberOfRooms"}).find("em").get_text().strip()
        print(data['pokoje'])

        # Parse rest of content
        ## define columns to save later
        # data['pietro'] = ''
        # data['liczba_pieter'] = ''
        # data['liczba_poziomow'] = ''
        # data['liczba_lazienek'] = ''
        # data['lazienka_powierzchnia'] = ''
        # data['laziekna_wc'] = ''
        # data['rynek'] = ''
        # data['rok_budowy'] = ''
        # data['liczba_sypialni'] = ''
        # data['balkon'] = ''
        # data['taras'] = ''
        # data['balkon_powierzchnia'] = ''
        # data['kuchnia_powierzchnia'] = ''
        # data['kuchnia_typ'] = ''
        # data['ogrodek_powierzchnia'] = ''
        # data['typ_budynku'] = ''
        # data['material_budowlany'] = ''
        # data['stan_budynku'] = ''
        # data['stan_nieruchomosci'] = ''

        parse_content = page.find("section", {"class": "propertyParams"})
        parse_content2 = parse_content.findAll("tr")

        for tr in range(len(parse_content2)):
            if (parse_content2[tr].find("th").get_text().strip() == "Piętro:"):
                data['pietro'] = parse_content2[tr].find("td").get_text().strip()
                print(data['pietro'])

            if (parse_content2[tr].find("th").get_text().strip() == "Liczba pięter:"):
                data['liczba_pieter'] = parse_content2[tr].find("td").get_text().strip()
                print(data['liczba_pieter'])

            if (parse_content2[tr].find("th").get_text().strip() == "Liczba poziomów mieszkania:"):
                data['liczba_poziomow'] = parse_content2[tr].find("td").get_text().strip()
                print(data['liczba_poziomow'])

            if (parse_content2[tr].find("th").get_text().strip() == "Liczba łazienek:"):
                data['liczba_lazienek'] = parse_content2[tr].find("td").get_text().strip()
                print(data['liczba_lazienek'])

            if (parse_content2[tr].find("th").get_text().strip() == "Powierzchnia łazienki:"):
                data['lazienka_powierzchnia'] = parse_content2[tr].find("td").get_text().strip()[:-3]
                print(data['lazienka_powierzchnia'])

            if (parse_content2[tr].find("th").get_text().strip() == "Czy łazienka z WC:"):
                data['lazienka_wc'] = parse_content2[tr].find("td").get_text().strip()
                print(data['lazienka_wc'])

            if (parse_content2[tr].find("th").get_text().strip() == "Rynek:"):
                data['rynek'] = parse_content2[tr].find("td").get_text().strip()
                print(data['rynek'])

            if (parse_content2[tr].find("th").get_text().strip() == "Rok budowy:"):
                data['rok_budowy'] = parse_content2[tr].find("td").get_text().strip()
                print(data['rok_budowy'])

            if (parse_content2[tr].find("th").get_text().strip() == "Liczba sypialni:"):
                data['liczba_sypialni'] = parse_content2[tr].find("td").get_text().strip()
                print(data['liczba_sypialni'])

            if (parse_content2[tr].find("th").get_text().strip() == "Balkon:"):
                data['balkon'] = parse_content2[tr].find("td").get_text().strip()
                print(data['balkon'])

            if (parse_content2[tr].find("th").get_text().strip() == "Taras:"):
                data['taras'] = parse_content2[tr].find("td").get_text().strip()
                print(data['taras'])

            if (parse_content2[tr].find("th").get_text().strip() == "Powierzchnia balkonu:"):
                data['balkon_powierzchnia'] = parse_content2[tr].find("td").get_text().strip()[:-3]
                print(data['balkon_powierzchnia'])

            if (parse_content2[tr].find("th").get_text().strip() == "Powierzchnia kuchni:"):
                data['kuchnia_powierzchnia'] = parse_content2[tr].find("td").get_text().strip()[:-3]
                print(data['kuchnia_powierzchnia'])

            if (parse_content2[tr].find("th").get_text().strip() == "Typ kuchni:"):
                data['kuchnia_typ'] = parse_content2[tr].find("td").get_text().strip()
                print(data['kuchnia_typ'])

            if (parse_content2[tr].find("th").get_text().strip() == "Powierzchnia ogródka:"):
                data['ogrodek_powierzchnia'] = parse_content2[tr].find("td").get_text().strip()[:-3]
                print(data['ogrodek_powierzchnia'])

            if (parse_content2[tr].find("th").get_text().strip() == "Typ budynku:"):
                data['typ_budynku'] = parse_content2[tr].find("td").get_text().strip()
                print(data['typ_budynku'])

            if (parse_content2[tr].find("th").get_text().strip() == "Materiał budowlany:"):
                data['material_budowlany'] = parse_content2[tr].find("td").get_text().strip()
                print(data['material_budowlany'])

            if (parse_content2[tr].find("th").get_text().strip() == "Stan budynku:"):
                data['stan_budynku'] = parse_content2[tr].find("td").get_text().strip()
                print(data['stan_budynku'])

            if (parse_content2[tr].find("th").get_text().strip() == "Stan nieruchomości:"):
                data['stan_nieruchomosci'] = parse_content2[tr].find("td").get_text().strip()
                print(data['stan_nieruchomosci'])

        return data

    def read_page_content(self, url):
        page = requests.get(url)
        return BeautifulSoup(page.content, "html.parser")


URL = 'https://www.morizon.pl/mieszkania/gdansk/'
csv_file_name = "nieruchomosci.csv"
csv_fieldnames = ['miasto', 'dzielnica', 'ulica', 'cena', 'powierzchnia', 'cena_m2', 'pokoje', 'pietro', 'liczba_pieter',
                'liczba_poziomow', 'liczba_lazienek', 'lazienka_powierzchnia', 'lazienka_wc', 'rynek', 'rok_budowy', 'liczba_sypialni',
                'balkon', 'taras', 'balkon_powierzchnia', 'kuchnia_powierzchnia', 'kuchnia_typ', 'ogrodek_powierzchnia', 'typ_budynku',
                'material_budowlany', 'stan_budynku', 'stan_nieruchomosci']


scraper = PageScrapper(URL)
scraper.find_advertisements()
