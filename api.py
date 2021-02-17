import aiohttp
import logging
import messages as msg
from config import API_URL, USER_AGENT
from json import loads


async def get_data():
    """Функция получения данных"""
    headers = {"user-agent": USER_AGENT}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, headers=headers) as resp:
                return loads(await resp.text())
    except aiohttp.ClientError as e:
        logging.error(e)
        return False


async def prepare_data(data):
    """Подготовка данных"""
    for i in data['data']:
        return i


async def short_title_get(text):
    """Функция для создания заголовка inline истории"""
    result = text[:32]
    if len(text) > 32:
        result = result + '...'
    result = await delete_tags_from_string(result)
    return result


async def decode_story_string(array):
    """Декодер текста записи"""
    struct_array = []
    array = loads(array)
    for i in array:
        if i[1]: struct_array.append(f'<b>{i[0]}</b>')
        else: struct_array.append(f'<i>{i[0]}</i>')
    return ''.join(struct_array)


async def get_post_media_from_json(data):
    """Функция получения ID записи. Функция возвращает готовую ссылку на фото"""
    json = loads(str(data))
    json_ex = json['inline_keyboard'][0][0]['url']
    result = json_ex.replace('https://porfirevich.ru/', 'https://porfirevich.ru/media/')+'.png'
    return result


async def cut_message(message):
    """Функция для обрезания сообщения если оно слишком длинное"""
    if len(message) > 4000:
        return message[:4000] + '...'
    return message


async def delete_tags_from_string(message):
    """Функция которая удаляет теги из сообщения"""
    tags = ['i', 'b', 'u']
    text = message
    for i in tags:
        text = text.replace(f'<{i}>', '').replace(f'</{i}>', '')
    return text


async def get_final_message(inline = False):
    """Итоговый вариант сообщения"""
    data = await get_data()
    data = await prepare_data(data)
    message, link = await msg.foramatted_message(data, inline)
    message = await msg.fix_string(message)
    return message, link