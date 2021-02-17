import aiohttp
import logging
from config import QUOTES_API_URL
from json import loads


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


