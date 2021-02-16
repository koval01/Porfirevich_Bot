from api import decode_story_string as decoder
import regex as re


help_message = 'Проект разработан вполне сознательно. Разработчикам хотелось выглядеть успешными. Но что сделано, \
то сделано. Теперь вы можете пользоваться трудами авторов совершенно свободно, без потерь. И не надо с сожалением перечитывать \
то, что написано под прикрытием редактирования.\n\
Мы не несем ни какой ответственности, но у нас нет средств получить ее! И на это есть причина!\n\
Обязательно найдите нас. Это ваш единственный шанс. Иначе все пропало. Здесь нет нужных людей, нет документов...\n\
Вопросы, жалобы и предложения принимаются тут: @mgrankin'


start_message = 'Этот Telegram бот умеет не очень много, только отправлять случайные записи с сайта porfirevich.ru\n@koval_yaroslav and @mgrankin'

rate_limit = 'Не могу так быстро работать.'

error_command = 'Что-что? Я тебя не понял...'

info_text = 'Для того, чтобы опубликовать свою историю, перейдите пожалуйста на сайт Порфирьевича.'

website_link = '{"inline_keyboard": [[{"text": "Перейти на сайт", "url": "https://porfirevich.ru/"}], [{"text": "Получить фото", "callback_data": "get_photo_button"}]]}'


async def foramatted_message(data):
    """Формирование сообщения для пользователя"""
    text = await decoder(data['content'])
    likes = data['likesCount']
    link = '{"inline_keyboard": [[{"text": "Посмотреть на сайте", "url": "https://porfirevich.ru/'+data['id']+'"}], [{"text": "Получить фото", "callback_data": "get_photo_button"}]]}'
    if len(text) > 4000: text[:4000]+'...'
    result = f'{text}\n{likes}❤️'
    return result, link


async def fix_string(string):
    """Удаления лишних отступов"""
    out_string = re.findall(r'\w[-]\s\w', string)
    for i in out_string:
        a=i[:1];b=i[3:4];string = string.replace(i, a+'-'+b)
    symbl = ['«', '(', '[', '{', '"', '\'', '“']
    for i in symbl:
        string = string.replace(f' {i} ', f' {i}')
    return string