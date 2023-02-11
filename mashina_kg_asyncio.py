import json
import time
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import asyncio
import aiohttp

cars_data = []
start_time = time.time()


async def get_page_data(session, page):
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    url = f'https://www.mashina.kg/search/all/all/?currency=2&price_from=4000&price_to=15000&region=1&sort_by=upped_at%20desc&time_created=1&town=2&year_from=2005&page={page}'

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")
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

async def gather_data():
    url = 'https://www.mashina.kg/search/all/all/?currency=2&price_from=4000&price_to=15000&region=1&sort_by=upped_at%20desc&time_created=1&town=2&year_from=2005'
    
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        pages_count = int(soup.find('ul', class_='pagination').find_all('a')[-1].attrs['data-page'])

        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
            
        await asyncio.gather(*tasks)
        await asyncio.sleep(1.0)


async def main():
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop().run_until_complete(gather_data())
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    with open(f"json_data/mashina_kg/{cur_time}.json", "w") as file:
        json.dump(cars_data, file, indent=4, ensure_ascii=False)
    
    df = pd.DataFrame.from_dict(cars_data)
    df.to_csv(f'csv_data/mashina_kg/{cur_time}.csv', index=False)
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")

    return df


if __name__ == '__main__':
    main()

