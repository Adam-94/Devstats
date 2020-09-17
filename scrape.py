from bs4 import BeautifulSoup, SoupStrainer
from collections import defaultdict

import grequests
import lxml
import time
import json
import os
import csv

PAGE_COUNT = 30

COUNTRY_CODE = [
    'AR','AU','AT','BE','BR','CA','CL','CO',
    'CR','CZ','DK','EC','EG','FI','FR','DE',
    'GR','HK','HU','IN','ID','IE','IT','JP', 
    'MX','NL','NZ','NG','NO','PK','PE','PH', 
    'PL','PT','RO','RU','SG','ZA','ES','SE', 
    'CH','TW','TH','TR','UA','AE','UK','US','VN',             
]
# COUNTRY LIST
cities = {
        # Argentina
        "AR": "https://ar.indeed.com",
        "Buenos Aires": "https://ar.indeed.com/jobs?q=software+developer&sort=date&l=Buenos+Aires&start=",

        # Australia
        "AU": "https://au.indeed.com",
        "Brisbane": "https://au.indeed.com/jobs?q=software+developer&sort=date&l=Brisbane&start=",
        "Perth": "https://au.indeed.com/jobs?q=software+developer&sort=date&l=Perth&start=",
        "Sydney": "https://au.indeed.com/jobs?q=software+developer&sort=date&l=Sydney&start=",

        # Austria
        "AT": "https://at.indeed.com",
        "Vienna": "https://at.indeed.com/jobs?q=software+developer&sort=date&l=Vienna&start=",
        "Graz": "https://at.indeed.com/jobs?q=software+developer&sort=date&l=Graz&start=",               

        # Belgium
        "BE": "https://be.indeed.com",
        "Antwerp": "https://be.indeed.com/jobs?q=software+developer&sort=date&l=Antwerp&start=",
        "Brussels": "https://be.indeed.com/jobs?q=software+developer&sort=date&l=Brussels&start=",

        # Brazil 
        "BR": "https://www.indeed.com.br",
        "Rio de Janeiro": "https://www.indeed.com.br/jobs?q=software+developer&sort=date&l=Rio+de+Janeiro&start=",

        # Canada
        "CA": "https://ca.indeed.com",
        "Toronto": "https://ca.indeed.com/jobs?q=software+developer&sort=date&l=Toronto&start=",
        "Vancouver": "https://ca.indeed.com/jobs?q=software+developer&sort=date&l=Vancouver&start=",
        "Calgary": "https://ca.indeed.com/jobs?q=software+developer&sort=date&l=Calgary&start=",

        # Chile
        "CL": "https://www.indeed.cl",
        "Santiago": "https://www.indeed.cl/jobs?q=software+developer&sort=date&l=Santiago&start=",
        "Antofagasta": "https://www.indeed.cl/jobs?q=software+developer&sort=date&l=Antofagasta&start=",

        # Colombia
        "CO": "https://co.indeed.com",
        "Bogota": "https://co.indeed.com/jobs?q=software+developer&sort=date&l=Bogota&start=",

        # Costa Rica
        "CR": "https://cr.indeed.com",
        "San Jose": "https://cr.indeed.com/jobs?q=software+developer&sort=date&l=San+Jose&start=",

        # Czech Republic
        "CZ": "https://cz.indeed.com",
        "Prague": "https://cz.indeed.com/jobs?q=software+developer&sort=date&l=Prague&start=",
        "Brno": "https://cz.indeed.com/jobs?q=software+developer&sort=date&l=Brno&start=",

        # Denmark
        "DK": "https://dk.indeed.com",
        "Copenhagen": "https://dk.indeed.com/jobs?q=software+developer&sort=date&l=Copenhagen&start=",
        "Aarhus": "https://dk.indeed.com/jobs?q=software+developer&sort=date&l=Aarhus&start=",

        # Ecuador
        "EC": "https://ec.indeed.com",
        "Guayaquil": "https://ec.indeed.com/jobs?q=software+developer&sort=date&l=Guayaquil&start=",
        "Quito": "https://ec.indeed.com/jobs?q=software+developer&sort=date&l=Quito&start=",

        # Egypt
        "EG": "https://eg.indeed.com",
        "Cairo": "https://eg.indeed.com/jobs?q=software+developer&sort=date&l=Cairo&start=",
        "Aswan": "https://eg.indeed.com/jobs?q=software+developer&sort=date&l=Aswan&start=",

        # Finland
        "FI": "https://www.indeed.fi",
        "Helsinki": "https://www.indeed.fi/jobs?q=software+developer&sort=date&l=Helsinki&start=",
        "Tampere": "https://www.indeed.fi/jobs?q=software+developer&sort=date&l=Tampere&start=",
        "Oulu": "https://www.indeed.fi/jobs?q=software+developer&sort=date&l=Oulu&start=",
        
        # France
        "FR": "https://www.indeed.fr",
        "Paris": "https://www.indeed.fr/jobs?q=software+developer&sort=date&l=Paris&start=",
        "Marseille": "https://www.indeed.fr/jobs?q=software+developer&sort=date&l=Marseille&start=",
        "Lyon": "https://www.indeed.fr/jobs?q=software+developer&sort=date&l=Lyon&start=",

        # Germany
        "DE": "https://de.indeed.com",
        "Munich": "https://de.indeed.com/jobs?q=software+developer&sort=date&l=Munich&start=",
        "Berlin": "https://de.indeed.com/jobs?q=software+developer&sort=date&l=Berlin&start=",
        "Hamburg": "https://de.indeed.com/jobs?q=software+developer&sort=date&l=Hamburg&start=",

        # Greece
        "GR": "https://gr.indeed.com",
        "Athens ": "https://gr.indeed.com/jobs?q=software+developer&sort=date&l=Athens&start=",
        "Thessaloniki": "https://gr.indeed.com/jobs?q=software+developer&sort=date&l=Thessaloniki&start=",

        # Hong Kong
        "HK": "https://www.indeed.hk",
        "Hong Kong": "https://www.indeed.hk/jobs?q=software+developer&sort=date&l=Hong+Kong&start=",
        "Kowloon": "https://www.indeed.hk/jobs?q=software+developer&sort=date&l=Hong+Kong&start=",

        # Hungary
        "HU": "https://hu.indeed.com",
        "Budapest": "https://hu.indeed.com/jobs?q=software+developer&sort=date&l=Budapest&start=",
        "Debrecen": "https://hu.indeed.com/jobs?q=software+developer&sort=date&l=Debrecen&start=",

        # India
        "IN": "https://www.indeed.co.in",
        "Jaipur": "https://www.indeed.co.in/jobs?q=software+developer&sort=date&l=Jaipur&start=",
        "Bengaluru": "https://www.indeed.co.in/jobs?q=software+developer&sort=date&l=Bengaluru&start=",
        "Mumbai": "https://www.indeed.co.in/jobs?q=software+developer&sort=date&l=Mumbai&start=",

        # Indonesia
        "ID": "https://id.indeed.com",
        "Jakarta": "https://id.indeed.com/jobs?q=software+developer&sort=date&l=Jakarta&start=",
        "Bandung": "https://id.indeed.com/jobs?q=software+developer&sort=date&l=Bandung&start=",

        # Ireland
        "IE": "https://ie.indeed.com",
        "Dublin": "https://ie.indeed.com/jobs?q=software+developer&sort=date&l=Dublin&start=",
        "Cork": "https://ie.indeed.com/jobs?q=software+developer&sort=date&l=Cork&start=",

        # Italy
        "IT": "https://it.indeed.com",
        "Rome": "https://it.indeed.com/jobs?q=software+developer&sort=date&l=Rome&start=",
        "Milan": "https://it.indeed.com/jobs?q=software+developer&sort=date&l=Milan&start=",

        # Japan
        "JP": "https://jp.indeed.com",
        "Fukuoka": "https://jp.indeed.com/jobs?q=software+developer&sort=date&l=Fukuoka&start=",
        "Tokyo": "https://jp.indeed.com/jobs?q=software+developer&sort=date&l=Tokyo&start=",
        "Osaka": "https://jp.indeed.com/jobs?q=software+developer&sort=date&l=Osaka&start=",

        # Mexico
        "MX": "https://www.indeed.com.mx",
        "Guadalajara": "https://www.indeed.com.mx/jobs?q=software+developer&sort=date&l=Guadalajara&start=",
        "Monterrey": "https://www.indeed.com.mx/jobs?q=software+developer&sort=date&l=Monterrey&start=",

        # Netherlands
        "NL": "https://www.indeed.nl",
        "Amsterdam": "https://www.indeed.nl/jobs?q=software+developer&sort=date&l=Rotterdam&start=",
        "Rotterdam": "https://www.indeed.nl/jobs?q=software+developer&sort=date&l=Rotterdam&start=",
        "Eindhoven": "https://www.indeed.nl/jobs?q=software+developer&sort=date&l=Eindhoven&start=",

        # New Zealand
        "NZ": "https://nz.indeed.com",
        "Wellington": "https://nz.indeed.com/jobs?q=software+developer&sort=date&l=Wellington&start=",
        "Auckland": "https://nz.indeed.com/jobs?q=software+developer&sort=date&l=Auckland&start=",
        "Christchurch": "https://nz.indeed.com/jobs?q=software+developer&sort=date&l=Christchurch&start=",

        # Nigeria
        "NG": "https://ng.indeed.com",
        "Lagos": "https://ng.indeed.com/jobs?q=software+developer&sort=date&l=Lagos&start=",

        # Norway
        "NO": "https://no.indeed.com",
        "Oslo": "https://no.indeed.com/jobs?q=software+developer&sort=date&l=Oslo&start=",
        "Bergen": "https://no.indeed.com/jobs?q=software+developer&sort=date&l=Bergen&start=",

        # Pakistan
        "PK": "https://www.indeed.com.pk",
        "Karachi": "https://www.indeed.com.pk/jobs?q=software+developer&sort=date&l=Karachi&start=",
        "Lahore": "https://www.indeed.com.pk/jobs?q=software+developer&sort=date&l=Lahore&start=",

        # Peru
        "PE": "https://www.indeed.com.pe",
        "Lima": "https://www.indeed.com.pe/jobs?q=software+developer&sort=date&l=Lima&start=",

        # Philippines
        "PH": "https://www.indeed.com.ph",
        "Makati": "https://www.indeed.com.ph/jobs?q=software+developer&sort=date&l=Makati&start=",
        "Quezon": "https://www.indeed.com.ph/jobs?q=software+developer&sort=date&l=Quezon&start=",

        # Poland
        "PL": "https://pl.indeed.com",
        "Warsaw": "https://pl.indeed.com/jobs?q=software+developer&sort=date&l=Warsaw&start=",
        "Krakow": "https://pl.indeed.com/jobs?q=software+developer&sort=date&l=Krakow&start=",

        # Portugal
        "PT": "https://www.indeed.pt",
        "Lisbon": "https://www.indeed.pt/jobs?q=software+developer&sort=date&l=Lisbon&start=",
        "Porto": "https://www.indeed.pt/jobs?q=software+developer&sort=date&l=Porto&start=",

        # Romania
        "RO": "https://ro.indeed.com",
        "Bucharest": "https://ro.indeed.com/jobs?q=software+developer&sort=date&l=Bucharest&start=",
        "Cluj": "https://ro.indeed.com/jobs?q=software+developer&sort=date&l=Cluj&start=",

        # Russia
        "RU": "https://ru.indeed.com",
        "Moscow": "https://ru.indeed.com/jobs?q=software+developer&sort=date&l=Moscow&start=",

        # Singapore
        "SG": "https://www.indeed.com.sg",
        "Singapore": "https://www.indeed.com./jobs?q=software+developer&sort=date&l=Singapore&start=",
        "Woodlands": "https://www.indeed.com./jobs?q=software+developer&sort=date&l=Woodlands&start=",
 
         # South Africa
        "ZA": "https://www.indeed.co.za",
        "Cape Town": "https://www.indeed.co.za/jobs?q=software+developer&sort=date&l=Cape+Town&start=",
        "Johannesburg": "https://www.indeed.co.za/jobs?q=software+developer&sort=date&l=Johannesburg&start=",

        # Spain
        "ES": "https://www.indeed.es",
        "Madrid": "https://www.indeed.es/jobs?q=software+developer&sort=date&l=Madrid&start=",
        "Barcelona": "https://www.indeed.es/jobs?q=software+developer&sort=date&l=Barcelona&start=",
        "Valencia": "https://www.indeed.es/jobs?q=software+developer&sort=date&l=Valencia&start=",

        # Sweden
        "SE": "https://se.indeed.com",
        "Stockholm": "https://se.indeed.com/jobs?q=software+developer&sort=date&l=Stockholm&start=",
        "Gothenburg": "https://se.indeed.com/jobs?q=software+developer&sort=date&l=Gothenburg&start=",

        # Switzerland
        "CH": "https://www.indeed.ch",
        "Zurich": "https://www.indeed.ch/jobs?q=software+developer&sort=date&l=Zurich&start=",
        "Geneva": "https://www.indeed.ch/jobs?q=software+developer&sort=date&l=Geneva&start=",
        "Lausanne": "https://www.indeed.ch/jobs?q=software+developer&sort=date&l=Lausanne&start=",

        # Taiwan
        "TW": "https://tw.indeed.com",
        "Hsinchu": "https://tw.indeed.com/jobs?q=software+developer&sort=date&l=Hsinchu&start=",
        "Taipei": "https://tw.indeed.com/jobs?q=software+developer&sort=date&l=Taipei&start=",

        # Thailand
        "TH": "https://th.indeed.com",
        "Bangkok": "https://th.indeed.com/jobs?q=software+developer&sort=date&l=Bangkok&start=",
        "Pattaya": "https://th.indeed.com/jobs?q=software+developer&sort=date&l=Pattaya&start=",

        # Turkey
        "TR": "https://tr.indeed.com",
        "Instanbul": "https://tr.indeed.com/jobs?q=software+developer&sort=date&l=Pattaya&start=",
        "Ankara": "https://tr.indeed.com/jobs?q=software+developer&sort=date&l=Ankara&start=",

        # Ukraine
        "UA": "https://ua.indeed.com",
        "Kyiv": "https://ua.indeed.com/jobs?q=software+developer&sort=date&l=Kyiv&start=",
        "Odesa": "https://ua.indeed.com/jobs?q=software+developer&sort=date&l=Odesa&start=",

        # United Arab Emirates
        "AE": "https://www.indeed.ae",
        "Dubai": "https://www.indeed.ae/jobs?q=software+developer&sort=date&l=Dubai&start=",
        "Abu Dhabi": "https://www.indeed.ae/jobs?q=software+developer&sort=date&l=Abu+Dhabi&start=",

        # United Kingdom
        "UK": "https://www.indeed.co.uk",
        "London": "https://www.indeed.co.uk/jobs?q=software+developer&sort=date&l=London&start=",
        "Cambridge": "https://www.indeed.co.uk/jobs?q=software+developer&sort=date&l=Cambridge&start=",
        "Manchester": "https://www.indeed.co.uk/jobs?q=software+developer&sort=date&l=Manchester&start=",
        "Liverpool": "https://www.indeed.co.uk/jobs?q=software+developer&sort=date&l=Liverpool&start=",
        "Birmingham": "https://www.indeed.co.uk/jobs?q=software+developer&sort=date&l=Birmingham&start=",
        "Cardiff": "https://www.indeed.co.uk/jobs?q=software+developer&sort=date&l=Cardiff&start=",
        "Wrexham": "https://www.indeed.co.uk/jobs?q=software+developer&sort=date&l=Wrexham&start=",
        "Belfast": "https://www.indeed.co.uk/jobs?q=software+developer&sort=date&l=Belfast&start=",

        # United States
        "US": "https://www.indeed.com",
        "San Francisco": "https://www.indeed.com/jobs?q=software+developer&sort=date&l=San+Francisco&start=",
        "New York": "https://www.indeed.com/jobs?q=software+developer&sort=date&l=New+York&start=",
        "Los Angeles": "https://www.indeed.com/jobs?q=software+developer&sort=date&l=Los+Angeles&start=",
        "Austin": "https://www.indeed.com/jobs?q=software+developer&sort=date&l=Austin&start=",
        "Washington D.C": "https://www.indeed.com/jobs?q=software+developer&sort=date&l=Washington+D.C&start=",

        # Vietnam
        "VN": "https://vn.indeed.com",
        "Ho Chi Minh City": "https://vn.indeed.com/jobs?q=software+developer&sort=date&l=Ho+Chi+Minh+City&start=",
        "Hanoi": "https://vn.indeed.com/jobs?q=software+developer&sort=date&l=Hanoi&start=",
   
    }


class Country():
    links = []
    descriptions = []
    all_pages = []
    country_urls = []
    current_country_url = ''
    city = ''
    url = ''

    def __init__(self, page_count, city_dict):
        self.get_country()
        self.set_city()
        self.set_url()
        self.languages, self.frameworks, self.tools = self.set_stats()
        self.page_count = page_count    

    def __repr__(self):
        return f'City: {self.city}\n URL: {self.url}\n Page count: {self.page_count}'

    def get_stats(self):
        self.all_pages = self.get_all_pages(self.url, self.page_count)
        self.links = self.job_links(self.current_country_url, self.all_pages)
        self.descriptions = self.job_descriptions(self.links)

        self.language_statistics(self.descriptions, self.languages)
        self.language_statistics(self.descriptions, self.frameworks)
        self.language_statistics(self.descriptions, self.tools)

    def print_stats(self):
        print(f'City: {self.city}\n')
        print(f'Languages: {self.languages}\n')
        print(f'Frameworks: {self.frameworks}\n')
        print(f'Tools: {self.tools}\n')

    def run(self):
        self.get_stats()
        self.print_stats()
        print('\n')
        self.write_to_file(self.languages, 'languages.csv')
        self.write_to_file(self.frameworks, 'frameworks.csv')
        self.write_to_file(self.tools, 'tools.csv')
        # self.write_to_file(self.current_country_url, self.links, 'links.txt')

    # Retrieve a city and then pop
    def get_country(self):
        for key, value in cities.items():
            if key in COUNTRY_CODE:
                # Country url is set so we have easy access and don't have to slice
                self.country_urls.append(value)
                cities.pop(key, value)
                break

    def set_city(self):
        for key, value in cities.items():
            if key not in COUNTRY_CODE:
                self.city = key
                self.url = value
                cities.pop(key, value)
                break

    def set_url(self):
        for country in self.country_urls:
            if country in self.url:
                self.current_country_url = country
    
    def get_all_pages(self, url, page_count):
        current_page = 0
        next_pages = []

        for i in range(page_count):
            next_pages.append(url + str(current_page))
            current_page += 10

        return next_pages

    # Gets all jobs links
    def job_links(self, country_url, pages):
        start_time = time.time()
        links = []

        rs = (grequests.get(u) for u in [page for page in pages])
        rs = grequests.map(rs, size=1000)

        for r, page in zip(rs, pages):
            parse_only = SoupStrainer('h2', class_='title')  
            soup = BeautifulSoup(r.text, 'lxml', parse_only=parse_only)

            titles = soup.find_all('h2', {'class': 'title'})  
            for link in titles:
                for a in link.find_all('a'):
                    # 
                    links.append(self.current_country_url + a['href']) 
                
        end_time = time.time()
        print('Links runtime: ', end_time - start_time)        
        return links

    # Go through each job in links and find all of the descriptions
    # In 30 pages theres usually 400+ jobs
    def job_descriptions(self, links):
        start_time = time.time()
        descriptions = []

        rs = (grequests.get(u) for u in [link for link in links])
        rs = grequests.map(rs, size=1000)

        for r, link in zip(rs, links):
            parse_only = SoupStrainer('div', class_='jobsearch-jobDescriptionText')  
            soup = BeautifulSoup(r.text, 'lxml', parse_only=parse_only)

            divs = soup.find_all("div", {"class": "jobsearch-jobDescriptionText"})
            for div in divs:
                for txt in div.find_all('li'):
                    contents = txt.text
                    descriptions.append(contents)
        
        end_time = time.time()
        print('Description runtime: ', end_time - start_time)
        return descriptions

    # Go through each job desciption looking for specific languages/frameworks/tools
    def language_statistics(self, descriptions, search):
        #for text, lang in enumerate(descriptions, search.key()):
        for descript in descriptions:
            for langs in search.keys():
                if langs == 'City':
                    continue
                elif langs in descript:
                    search[langs] += 1

    # These can be changed
    def set_stats(self):
        languages = {
            "City": self.city,
            "C/C++": 0,
            "C#": 0,
            "Dart": 0,
            "Golang": 0,
            "JavaScript": 0,
            "Java": 0,
            "Kotlin": 0,
            "Python": 0,
            "PHP": 0,
            "Ruby": 0,
            "Scala": 0,
            "Swift": 0,
            "Typescript": 0,
        }

        frameworks = {
            "City": self.city,
            "Angular": 0,
            ".NET": 0,
            "Django": 0,
            "Flask": 0,
            "Laravel": 0,
            "React": 0,
            "Ruby on Rails": 0,
            "Spring": 0,
            "Vue.js": 0,
        }

        tools = {
            "City": self.city,
            "AWS": 0,
            "DigitalOcean": 0,
            "Git": 0,
            "Microsoft SQL Server": 0,
            "Oracle": 0,
            "MySQL": 0,
            "PostgreSQL": 0,
            "Linux": 0,
        }

        return languages, frameworks, tools
       
    def write_to_file(self, data, output_file):#
        with open(output_file, 'a', newline='') as myfile:
            writer = csv.DictWriter(myfile, data.keys())
            if myfile.tell() == 0:
                writer.writeheader()
            writer.writerow(data)


if __name__ == '__main__':

    start_time = time.time()
    search = [Country(PAGE_COUNT, cities) for i in range(len(cities)-1)]
    for x in search:
        x.run()

    end_time = time.time()
    print('Runtime: ', end_time - start_time)