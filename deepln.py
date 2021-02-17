import aiohttp
import logging
from json import loads
from time import time
from config import DEEP_LN_URL, USER_AGENT


async def get_data_deepln(text, source_lang = 'EN', targer_lang = 'RU'):
    """Функция получения данных от DeepLn"""
    headers = {"user-agent": USER_AGENT}
    json_cascade = {
          "jsonrpc": "2.0",
          "method": "LMT_handle_jobs",
          "params": {
            "jobs": [
              {
                "kind": "default",
                "raw_en_sentence": text,
                "raw_en_context_before": [],
                "raw_en_context_after": [],
                "preferred_num_beams": 4,
                "quality": "fast"
              }
            ],
            "lang": {
              "user_preferred_langs": [
                "DE",
                "RU",
                "EN"
              ],
              "source_lang_user_selected": source_lang,
              "target_lang": targer_lang
            },
            "priority": -1,
            "commonJobParams": {
              "formality": None
            },
            "timestamp": str(time()).replace('.', '')[:13]
          },
          "id": None
        }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(DEEP_LN_URL, headers=headers, json=json_cascade) as resp:
                return await resp.text()
    except aiohttp.ClientError as e:
        logging.error(e)
        return False


async def decode_translate_response(data):
    """Миниатюрная функция декодера"""
    data = str(data).replace('\'', '"').lower()
    json_data = loads(data)
    return json_data


async def translate(text):
    """Основная функция перевода для более удобного использования"""
    prepare = await get_data_deepln(text)
    result = await decode_translate_response(prepare)
    return result

