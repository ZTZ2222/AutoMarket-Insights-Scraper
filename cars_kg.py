import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import json
import time

start_time = time.time()

def collect_data():
    cur_time = datetime.datetime.now().strftime('%H_%M_%d_%m_%Y')
    page = 1
    cars_data = []
    while True:
        try:
            url = f'https://cars.kg/offers/{page}?direction=sale&price_from=4000&price_to=15000&year_from=2005&year_to=2023&city=1'
            headers = {
                'accept': '*/*',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            }
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            cars_items = soup.find('div', class_='catalog-list').find_all('a', class_='catalog-list-item')
            base_url = 'https://cars.kg'
            for ci in cars_items:
                car_link = base_url + ci.get('href')
                make_model = ci.find('span', class_='catalog-item-params').find('span', class_='catalog-item-caption').contents[0].strip().replace(' ,', '')
                year = ci.find('span', class_='catalog-item-params').find('span', class_='catalog-item-caption').find('span').text.strip()
                mileage = ci.find('span', class_='catalog-item-params').find('span', class_='catalog-item-mileage').text.strip()
                price = ci.find('span', class_='catalog-item-params').find('span', class_='catalog-item-price').text.strip()
                description = ci.find('span', class_='catalog-item-descr').text.split(',')
                descriptions=[]
                for sub in description:
                    descriptions.append(sub.strip())
                city = ci.find('span', class_='catalog-item-info').text.split(',')[-1].strip()
                cars_data.append(
                    {
                        'make_model': make_model,
                        'year': year,
                        'mileage': mileage,
                        'price': price,
                        'descriptions': descriptions,
                        'city': city,
                        'car_link': car_link
                    }
                )
            page +=1
            time.sleep(1)
        except:
            break
    with open(f'json_data/cars_kg/{cur_time}.json', 'w') as file:
        json.dump(cars_data, file, indent=4, ensure_ascii=False)
    
    df = pd.DataFrame.from_dict(cars_data)
    df.to_csv(f'csv_data/cars_kg/{cur_time}.csv', index=False)
    


def main():
    collect_data()
    finish_time = time.time() - start_time
    print(f'Затрачено времени на парсинг: {finish_time}')

if __name__ == '__main__':
    main()