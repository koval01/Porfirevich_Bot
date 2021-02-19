import aiohttp
import logging
from json import loads
from config import FACTS_API_URL, USER_AGENT


async def get_data_quote() -> str:
    """Функция получения данных"""
    headers = {"user-agent": USER_AGENT, 'X-Requested-With': 'XMLHttpRequest'}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(FACTS_API_URL, headers=headers) as resp:
                return await resp.text()
    except aiohttp.ClientError as e:
        logging.error(e)
        return False


async def resp_decoder(data) -> str:
    """Функция декодирования ответа сервера"""
    data = loads(data)
    data = data['fact']['text']
    return data


async def get_fact() -> str:
    """Функция для удобного получения факта"""
    data = await get_data_quote()
    result = await resp_decoder(data)
    fact = f"<i>{result}</i>"
    return fact