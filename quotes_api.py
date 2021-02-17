import aiohttp
import logging
from bs4 import BeautifulSoup
from config import QUOTES_API_URL


async def get_data_quote():
    """Функция получения данных"""
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.23 Safari/537.36"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(QUOTES_API_URL, headers=headers) as resp:
                return await resp.text()
    except aiohttp.ClientError as e:
        logging.error(e)
        return False


async def page_decoder(data):
    """Функция декодирования Unicode"""
    soup = BeautifulSoup(data, 'html.parser')
    data = soup.find_all("div", {"class": "field-item"})[0].text
    return data


async def get_quote():
    """Функция для удобного получения цитаты"""
    data = await get_data_quote()
    result = await page_decoder(data)
    quote_ = result
    qoute = "<i>„{}“</i>".format(quote_)
    final_message = '%s\n\n — Случайная цитата с ресурса citaty.info' % qoute
    return final_message