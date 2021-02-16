import aiohttp
import messages as msg
from config import API_URL
from json import loads


async def get_data():
    """Функция получения данных"""
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.23 Safari/537.36"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, headers=headers) as resp:
                return loads(await resp.text())
    except aiohttp.ClientError as e:
        return False


async def prepare_data(data):
    """Подготовка данных"""
    for i in data['data']:
        return i


async def decode_story_string(array):
    """Декодер текста записи"""
    struct_array = []
    array = loads(array)
    for i in array:
        if i[1]: struct_array.append(f'<b>{i[0]}</b>')
        else: struct_array.append(f'<i>{i[0]}</i>')
    return ''.join(struct_array)


async def get_post_id_from_json(data):
    """Функція для отримання ID запису з JSON структури сутностей повідомлення"""
    json = loads(str(data))
    json_ex = json['inline_keyboard'][0][0]['url']
    result = json_ex.replace('https://porfirevich.ru/', 'https://porfirevich.ru/media/')+'.png'
    return result


async def get_final_message():
    data = await get_data()
    data = await prepare_data(data)
    message, link = await msg.foramatted_message(data)
    message = await msg.fix_string(message)
    return message, link