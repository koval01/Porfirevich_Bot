import aiohttp
import logging
from bs4 import BeautifulSoup
from config import QUOTES_API_URL, USER_AGENT


async def get_data_quote() -> str:
    """Функция получения данных"""
    headers = {"user-agent": USER_AGENT}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(QUOTES_API_URL, headers=headers) as resp:
                return await resp.text()
    except aiohttp.ClientError as e:
        logging.error(e)
        return False


async def page_decoder(data) -> str:
    """Функция декодирования ответа от сервера"""
    soup = BeautifulSoup(data, 'html.parser')
    data = soup.find_all("div", {"class": "field-item"})[0].text
    return data


async def get_quote() -> str:
    """Функция для удобного получения цитаты"""
    data = await get_data_quote()
    result = await page_decoder(data)
    qoute = f"<i>„{result}“</i>"
    return qoute