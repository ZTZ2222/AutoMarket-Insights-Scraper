import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import json
import time

start_time = time.time()

def collect_data():
    cur_time = datetime.datetime.now().strftime('%H_%M_%d_%m_%Y')
    url = 'https://www.mashina.kg/search/all/all/?currency=2&price_from=4000&price_to=15000&region=1&sort_by=upped_at%20desc&town=2&year_from=2005'
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    pages_count = int(soup.find('ul', class_='pagination').find_all('a')[-1].attrs['data-page'])
    cars_data = []
    for page in range(1, pages_count + 1):
        url = f'https://www.mashina.kg/search/all/all/?currency=2&price_from=4000&price_to=15000&region=1&sort_by=upped_at%20desc&town=2&year_from=2005&page={page}'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        cars_items = soup.find('div', class_='table-view-list').find_all('div', class_='list-item')
        base_url = 'https://www.mashina.kg'
        for ci in cars_items:
            car_link = base_url + ci.find('a').get('href')
            car_data = ci.find('a')
            make_model = car_data.find('div', class_='block title').find('h2').text.strip()
            price_usd = car_data.find('div', class_='block price').find('p').find('strong').text.strip()
            price_som = car_data.find('div', class_='block price').find('p').contents[3].strip()
            year = car_data.find('div', class_='item-info-wrapper').find('p', class_='year-miles').find('span').text.strip()
            engine_cap = car_data.find('div', class_='item-info-wrapper').find('p', class_='year-miles').contents[2].replace(', ', '').strip()
            color = car_data.find('div', class_='item-info-wrapper').find('p', class_='year-miles').find('i')['title']
            body_type = car_data.find('div', class_='item-info-wrapper').find('p', class_='body-type').text.split(', ', 1)[0].strip()
            engine_type = car_data.find('div', class_='item-info-wrapper').find('p', class_='body-type').text.split(', ', 1)[1].strip()
            wheel_pos = car_data.find('div', class_='item-info-wrapper').find('p', class_='volume').text.split(', ')[0].strip()
            city = car_data.find('div', class_='block city').find('p').contents[0].strip()
            try:
                transmission = car_data.find('div', class_='item-info-wrapper').find('p', class_='year-miles').contents[4].strip().replace(', ', '')
            except:
                transmission = ''
            try:
                mileage = car_data.find('div', class_='item-info-wrapper').find('p', class_='volume').text.split(', ')[1].strip()
            except:
                mileage = ''
            cars_data.append(
                {
                    'make_model': make_model,
                    'year': year,
                    'price_usd': price_usd,
                    'price_som': price_som,
                    'transmission': transmission,
                    'color': color,
                    'body_type': body_type,
                    'engine_cap': engine_cap,
                    'engine_type': engine_type,
                    'wheel_pos': wheel_pos,
                    'mileage': mileage,
                    'city': city,
                    'car_link': car_link
                }
            )

        time.sleep(1)
    
    with open(f'json_data/mashina_kg/{cur_time}.json', 'w') as file:
        json.dump(cars_data, file, indent=4, ensure_ascii=False)
    
    df = pd.DataFrame.from_dict(cars_data)
    df.to_csv(f'csv_data/mashina_kg/{cur_time}.csv', index=False)
    

def main():
    collect_data()
    finish_time = time.time() - start_time
    print(f'Затрачено времени на парсинг: {finish_time}')

if __name__ == '__main__':
    main()