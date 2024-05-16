from aiogram import Bot, Dispatcher, executor, types
import os
import asyncio
import pandas as pd
from aiogram.utils.markdown import hbold, hitalic, hlink
from datetime import datetime
from bs4 import BeautifulSoup
import aiohttp
import os

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def get_page_data(session, page):
    """
    Asynchronously fetches data from a webpage based on the provided session and page number.

    Args:
        session: The session to use for the HTTP request.
        page: The page number to fetch data from.

    Returns:
        None
    """
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }

    url = f"https://www.mashina.kg/search/all/all/?currency=2&price_from=3000&price_to=20000&region=1&sort_by=upped_at%20desc&time_created=1&town=2&year_from=2003&page={page}"

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")
        cars_items = soup.find("div", class_="table-view-list").find_all(
            "div", class_="list-item"
        )
        base_url = "https://www.mashina.kg"
        for ci in cars_items:
            car_link = base_url + ci.find("a").get("href")
            car_data = ci.find("a")
            make_model = (
                car_data.find("div", class_="block title").find("h2").text.strip()
            )
            price_usd = (
                car_data.find("div", class_="block price")
                .find("p")
                .find("strong")
                .text.strip()
            )
            year = (
                car_data.find("div", class_="item-info-wrapper")
                .find("p", class_="year-miles")
                .find("span")
                .text.strip()
            )
            engine_cap = (
                car_data.find("div", class_="item-info-wrapper")
                .find("p", class_="year-miles")
                .contents[2]
                .replace(", ", "")
                .strip()
            )
            color = (
                car_data.find("div", class_="item-info-wrapper")
                .find("p", class_="year-miles")
                .find("i")["title"]
            )
            body_type = (
                car_data.find("div", class_="item-info-wrapper")
                .find("p", class_="body-type")
                .text.split(", ", 1)[0]
                .strip()
            )
            engine_type = (
                car_data.find("div", class_="item-info-wrapper")
                .find("p", class_="body-type")
                .text.split(", ", 1)[1]
                .strip()
            )
            wheel_pos = (
                car_data.find("div", class_="item-info-wrapper")
                .find("p", class_="volume")
                .text.split(", ")[0]
                .strip()
            )
            city = (
                car_data.find("div", class_="block city").find("p").contents[0].strip()
            )
            try:
                transmission = (
                    car_data.find("div", class_="item-info-wrapper")
                    .find("p", class_="year-miles")
                    .contents[4]
                    .strip()
                    .replace(", ", "")
                )
            except:
                transmission = ""
            try:
                mileage = (
                    car_data.find("div", class_="item-info-wrapper")
                    .find("p", class_="volume")
                    .text.split(", ")[1]
                    .strip()
                )
            except:
                mileage = ""
            cars_data.append(
                {
                    "make_model": make_model,
                    "year": year,
                    "price_usd": price_usd,
                    "transmission": transmission,
                    "color": color,
                    "body_type": body_type,
                    "engine_cap": engine_cap,
                    "engine_type": engine_type,
                    "wheel_pos": wheel_pos,
                    "mileage": mileage,
                    "city": city,
                    "car_link": car_link,
                    "date": datetime.now().strftime("%m_%d_%Y"),
                }
            )


async def gather_data():
    """
    Asynchronously gathers data from a specific URL, extracts the number of pages, and creates tasks for each page to retrieve data using aiohttp and BeautifulSoup.
    """
    global cars_data
    cars_data = []
    url = "https://www.mashina.kg/search/all/all/?currency=2&price_from=3000&price_to=20000&region=1&sort_by=upped_at%20desc&time_created=1&town=2&year_from=2005"

    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        pages_count = int(
            soup.find("ul", class_="pagination").find_all("a")[-1].attrs["data-page"]
        )

        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)
        await asyncio.sleep(1.0)


async def convert_data():
    await gather_data()
    cur_time = datetime.now().strftime("%d_%m_%Y_%H_%M")

    # with open(f"json_data/mashina_kg/{cur_time}.json", "w") as file:
    #     json.dump(cars_data, file, indent=4, ensure_ascii=False)

    df = pd.DataFrame.from_dict(cars_data)
    df.to_csv(f"csv_data/mashina_kg/{cur_time}.csv", index=False)

    return df


#######################################################################################################################################


async def check_notif(df):
    """
    Check notifications based on the input DataFrame and return a DataFrame with notifications to send.

    Parameters:
    - df: DataFrame containing car data

    Returns:
    - DataFrame: Notifications to send
    """
    df_mean = pd.read_csv("csv_data/sorted_dfs/mean_prices.csv")
    df = pd.DataFrame(df)
    df = df.replace("Land Rover", "Land-Rover", regex=True)
    df.year = df.year.apply(lambda x: int(x.split(" ")[0]))
    df["age"] = [datetime.now().year] - df["year"]
    df.mileage = df.mileage.fillna("0 км").replace("", "0 км")
    df.drop_duplicates(inplace=True)
    df.transmission = df.transmission.fillna(df.engine_cap).replace("", "электро")
    df.engine_cap = (
        df.engine_cap.replace("автомат", 2)
        .replace("вариатор", 1.5)
        .replace("электро", 1.5)
    )
    df.price_usd = (
        df.price_usd.str.slice(1).str.strip().replace(" ", "", regex=True).astype(int)
    )
    df.engine_cap = df.engine_cap.astype(float)
    df = df[df["transmission"] != "механика"]
    df_new = df.merge(df_mean, how="left", on=["make_model", "year"])
    df_new.dropna(inplace=True)
    df_new["deviation"] = round(1 - (df_new.price_usd / df_new.mean_price), 2)
    df_notifications = df_new[df_new.deviation > 0.15]

    if len(df_notifications) > 0:
        df_notif_sent = pd.read_csv("csv_data/sorted_dfs/df_notif_sent.csv")
        df_notif_sent = df_notif_sent.loc[
            :, ~df_notif_sent.columns.str.contains("_merge")
        ]
        df_notif_sent = df_notif_sent.loc[
            :, ~df_notif_sent.columns.str.contains("^Unnamed")
        ]
        df_notif_to_send_1 = pd.merge(
            df_notifications, df_notif_sent, how="outer", indicator=True
        )
        df_notif_to_send_2 = df_notif_to_send_1[
            df_notif_to_send_1["_merge"] == "left_only"
        ].reset_index(drop=True)
        pd.concat(
            [df_notifications, df_notif_sent], ignore_index=True
        ).drop_duplicates().to_csv("csv_data/sorted_dfs/df_notif_sent.csv", index=False)
        return df_notif_to_send_2
    return pd.DataFrame()


async def concat_hdata():
    """
    Concatenates data from multiple CSV files, performs various data manipulation operations, and saves the results to CSV files.
    """
    file_path = "csv_data/mashina_kg/"
    file_list = os.listdir(file_path)
    df = pd.concat(
        [pd.read_csv(f"csv_data/mashina_kg/{f}") for f in file_list], ignore_index=True
    )
    df = df.replace("Land Rover", "Land-Rover", regex=True)
    df.year = df.year.apply(lambda x: int(x.split(" ")[0]))
    df["age"] = [datetime.now().year] - df["year"]
    df.mileage = df.mileage.fillna("0 км").replace("", "0 км")
    df.drop_duplicates(inplace=True)
    df.transmission = df.transmission.fillna(df.engine_cap)
    df.engine_cap = df.engine_cap.replace("автомат", 2).replace("вариатор", 1.5)
    df.price_usd = (
        df.price_usd.str.slice(1).str.strip().replace(" ", "", regex=True).astype(int)
    )
    df.engine_cap = df.engine_cap.astype(float)
    last_sorted = pd.read_csv("csv_data/sorted_dfs/df_sorted_upd.csv")
    df_c = pd.concat([df, last_sorted], ignore_index=True)
    df_c.to_csv(f"csv_data/sorted_dfs/df_sorted_upd.csv", index=False)
    df_c = df_c[df_c["transmission"] != "механика"]
    multi_color = df_c["color"].value_counts() > 5
    df_c = df_c[df_c["color"].isin(multi_color[multi_color].index)]
    multi_body_type = df_c["body_type"].value_counts() > 5
    df_c = df_c[df_c["body_type"].isin(multi_body_type[multi_body_type].index)]
    multi_age = df_c["age"].value_counts() > 5
    df_c = df_c[df_c["age"].isin(multi_age[multi_age].index)]
    multi_engine_cap = df_c["engine_cap"].value_counts() > 5
    df_c = df_c[df_c["engine_cap"].isin(multi_engine_cap[multi_engine_cap].index)]
    multi_make_model = df_c["make_model"].value_counts() > 5
    df_c = df_c[df_c["make_model"].isin(multi_make_model[multi_make_model].index)]
    df_c.reset_index(drop=True, inplace=True)
    df_group = df_c.groupby(["make_model", "year"]).describe()
    df_group.columns = ["__".join(col).strip() for col in df_group.columns.values]
    dfn = df_group[["price_usd__count", "price_usd__mean"]]
    dfn = dfn[dfn["price_usd__count"] > 3]
    dfn.reset_index(inplace=True)
    dfn.rename(
        columns={"price_usd__count": "count", "price_usd__mean": "mean_price"},
        inplace=True,
    )
    dfn.to_csv("csv_data/sorted_dfs/mean_prices.csv", index=False)
    for f in file_list:
        path_to_file = os.path.join(file_path, f)
        os.remove(path_to_file)


async def new_loads_notification():
    """
    Async function that checks for new loads notification, prepares a notification card with specific details,
    and sends it to the user. If there are no notifications, it sends a default message.
    It includes a sleep of 180 seconds between iterations.
    """
    if len(os.listdir("csv_data/mashina_kg")) > 30:
        await concat_hdata()
    while True:
        df = await convert_data()
        df_notif_to_send = await check_notif(df)

        if df_notif_to_send.empty is False:
            for i in range(len(df_notif_to_send)):
                card = (
                    f"{hlink(df_notif_to_send['make_model'].iloc[i], df_notif_to_send['car_link'].iloc[i])}\n"
                    f"{hbold('Цена:')} ${df_notif_to_send['price_usd'].iloc[i]} ({df_notif_to_send['mileage'].iloc[i]})\n"
                    f"{hbold('Ниже на:')} {int(df_notif_to_send['deviation'].iloc[i]*100)}%🔥🔥🔥\n"
                    f"{hbold('Средняя цена:')} {int(df_notif_to_send['mean_price'].iloc[i])} ({int(df_notif_to_send['count'].iloc[i])})\n"
                    f"{hitalic(df_notif_to_send['year'].iloc[i])}, {hitalic(df_notif_to_send['body_type'].iloc[i])}, {hitalic(df_notif_to_send['transmission'].iloc[i])}, {hitalic(df_notif_to_send['engine_type'].iloc[i])}, {hitalic(df_notif_to_send['engine_cap'].iloc[i])}, {hitalic(df_notif_to_send['wheel_pos'].iloc[i])}\n"
                )

                await bot.send_message(os.getenv("USER_ID"), card)

        else:
            pass
            # await bot.send_message(user_id, "nothing...")
        await asyncio.sleep(180)


if __name__ == "__main__":
    try:
        asyncio.run(new_loads_notification())
    except KeyboardInterrupt:
        pass
    executor.start_polling(dp)
