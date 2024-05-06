# Car Ads Scraper

![fastapi-scikitlearn-pandas](/static/tech-stack2.jpg)

<a name="readme-top"></a>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
  </ol>
</details>

## About The Project

Car Ads Scraper is a project designed to scrape data from multiple car advertisements boards, focusing on a wide range of vehicles. The bot collects data from various sources and stores it in a PostgreSQL database. It offers endpoints to access the scraped data based on different parameters such as make, model, year, and price.

### Built With

[![aiohttp][aiohttp.org]][aiohttp-url]
[![aiogram][aiogram.dev]][aiogram-url]
[![pandas][pandas.pydata.org]][pandas-url]
[![scikit-learn][scikit-learn.org]][scikit-learn-url]
[![scipy][scipy.org]][scipy-url]
[![FastAPI][fastapi.tiangolo.com]][fastapi-url]
[![SQLAlchemy][sqlalchemy.org]][sqlalchemy-url]
[![asyncpg][asyncpg.github.io]][asyncpg-url]
[![docker][hub.docker.com]][docker-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Features

- Scrapes data from various car advertisements boards
- Collects information on a wide range of vehicles
- Capable of creating and filling CSV files with scraped data or stores scraped data in a PostgreSQL database
- Provides an API to access the collected data using FastAPI
- Supports filtering and querying of data based on parameters like make, model, year, and price

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Installation

1. Clone the repository:

```bash
git clone https://github.com/ZTZ2222/car_ads_scraper.git
```

2. Navigate into the project directory:

```bash
cd car_ads_scraper
```

3. Create a .env file in the project root directory and add the necessary environment variables. Here's an example:

```plaintext
POSTGRES_DB=car_db
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
BOT_TOKEN="BOT_TOKEN"
USER_ID="USER_ID"
SCHEDULE_TIME="SCHEDULE_TIME"
```

4. Build and run the project with Docker Compose:

```bash
docker-compose up --build -d
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Usage

Once the server is running, you can access the API endpoints to retrieve scraped data:

- List all cars:

```bash
GET /cars
```

- Filter cars by make:

```bash
GET /cars?make={make}
```

- Filter cars by model:

```bash
GET /cars?model={model}
```

- Filter cars by year:

```bash
GET /cars?min_year={min_year}
```

- Filter cars by discount percentage:

```bash
GET /cars?min_discount={min_discount}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[aiohttp.org]: https://img.shields.io/badge/aiohttp-3.8.3-e92063?style=for-the-badge&logo=aiohttp&logoColor=white
[aiohttp-url]: https://docs.aiohttp.org/en/stable/
[aiogram.dev]: https://img.shields.io/badge/aiogram-2.24.0-6BA81E?style=for-the-badge&logo=telegram&logoColor=white
[aiogram-url]: https://docs.aiogram.dev/en/latest/
[pandas.pydata.org]: https://img.shields.io/badge/pandas-1.5.3-6BA81E?style=for-the-badge&logo=pandas&logoColor=white
[pandas-url]: https://pandas.pydata.org/docs/
[scikit-learn.org]: https://img.shields.io/badge/scikitlearn-1.2.1-009485?style=for-the-badge&logo=scikitlearn&logoColor=white
[scikit-learn-url]: https://scikit-learn.org/stable/
[scipy.org]: https://img.shields.io/badge/scipy-1.10.0-bb0000?style=for-the-badge&logo=scipy&logoColor=white
[scipy-url]: https://docs.scipy.org/doc/scipy/
[fastapi.tiangolo.com]: https://img.shields.io/badge/FastAPI-0.104.1-009485?style=for-the-badge&logo=fastapi&logoColor=white
[fastapi-url]: https://fastapi.tiangolo.com/
[sqlalchemy.org]: https://img.shields.io/badge/SQLAlchemy-2.0.28-bb0000?color=bb0000&style=for-the-badge&logo=sqlalchemy&logoColor=white
[sqlalchemy-url]: https://docs.sqlalchemy.org/en/20/
[asyncpg.github.io]: https://img.shields.io/badge/asyncpg-0.29.0-2e6fce?style=for-the-badge&logo=postgresql&logoColor=white
[asyncpg-url]: https://magicstack.github.io/asyncpg/current/
[hub.docker.com]: https://img.shields.io/badge/docker-26.1.1-2094f3?style=for-the-badge&logo=docker&logoColor=white
[docker-url]: https://docs.docker.com/
