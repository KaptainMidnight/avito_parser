import requests
from bs4 import BeautifulSoup as bs
import csv


class Bot:
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)"
    }

    def __init__(self):
        self.get_html()

    def get_html(self):  # Get HTML pages
        url = "https://m.avito.ru/rossiya/nedvizhimost?owner[]=private&sort=default&withImagesOnly=false"
        with requests.Session() as session:
            response = session.get(url, headers=self.headers)
        return response.text

    def parse_html(self, html):  # Get data from HTML code(links to ads)
        ads = []
        urls = {}
        data_user = {}
        data = []
        soup = bs(html, 'lxml')
        main_div = soup.find_all('div', {'class': '_328WR'})
        for i in main_div:
            try:
                a = i.find('a', {'class': 'MBUbs'}).get('href')
                link = f"https://m.avito.ru{a}"
                urls = {
                    'href': link
                }
                ads.append(urls)
            except:
                pass
        for j in ads:  # We receive user contacts(Name: Phone)
            with requests.Session() as session:
                response = session.get(j['href'], headers=self.headers)
                soup = bs(response.text, 'lxml')
                contact = soup.find_all('div', {'class': '_3U_HU'})
                for l in contact:
                    try:
                        name = l.find('span', {'class': 'ZvfUX'}).text
                        phone = l.find('a', {'class': '_2MOUQ'}).get('href')
                        phone = phone[4::1]
                        data_user = {
                            'name': name,
                            'phone': phone,
                        }
                        data.append(data_user)
                    except:
                        pass
        print(f"Received: {len(data)}")
        return data

    def write_csv(self, data):
        with open('data.csv', 'w') as file:
            wrtr = csv.writer(file)
            wrtr.writerow(("Имя", "Телефон"))
            for i in data:
                wrtr.writerow((i['name'], i['phone']))
            print("Saved!")


bot = Bot()
html = bot.get_html()
result = bot.parse_html(html)
bot.write_csv(result)
