'''
----    Ход работы    ----
Получение слов:
    + открыть файл
    + считать текст и разбить на слова

Что нужно в итоге:
1) C сайта OXFORD -> https://www.oxfordlearnersdictionaries.com/
    + транскрипцию,
    + определение,
    + аудио.
2) С сайта WooordHunt -> https://wooordhunt.ru/
    + варианты перевода для разных частей речи

Способ вывода результата:
    + создать текстовый файл
    + записать в правильном порядке нужные слова

Хранение выученных слов:
    - Подключение БД

--------------------------------------------------------------
usefull stuff:
- https://www.dataquest.io/blog/web-scraping-tutorial-python/
- https://www.dataquest.io/blog/python-api-tutorial/
--------------------------------------------------------------
'''
from bs4 import BeautifulSoup
import requests
from json import dump


def get_words(file):
    with open(file) as text:
        words = text.read().split('\n')
        return words


def make_result_file(res_dict):
    with open('result.txt', 'w', encoding='utf-8') as f:
        n = 0
        len_d = len(res_dict)
        for word in res_dict:
            try:
                n += 1
                f.writelines(f'{n}. ')
                f.writelines(
                    word + ' - ' + res_dict[word]['transcription'] + ' ' + res_dict[word]['translation'] + '\n' + \
                    res_dict[word]['pronounce'] + '\n' + \
                    res_dict[word]['senses'][0] + '\n----    ----    ----    ----\n' * bool(not n == len_d) \
                    )
            except:
                f.writelines(
                            word + ' - ' + 'Error while making result file' + '\n\n')


def url_serch(word='test'):
    # решение проблеммы с ошибкой запроса https://www.cyberforum.ru/python-web/thread2723731.html
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate, lzma, sdch',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    }

    essential_data = {'transcription': 'not found',
                      'senses': 'not found',
                      'translation': 'not found', 
                      'pronounce': 'not found',
                     }

    Ox_url = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + word
    Wooord_url = 'https://wooordhunt.ru/word/' + word

    Ox_page = requests.get(Ox_url, headers=headers)
    Wooord_page = requests.get(Wooord_url, headers=headers)

    # page.status_code выдаёт значение 200, если страница получена
    if Ox_page.status_code == 200:
        Ox_soup = BeautifulSoup(Ox_page.content, 'html.parser')
        # выбор нужной информации
        try:
            transcription = Ox_soup.find_all('span', class_='phon')[0].get_text()
            senses = [meaning.get_text() for meaning in Ox_soup.find_all('span', class_='def')]
            pronounce_links = Ox_soup.find_all('div', class_="sound audio_play_button pron-uk icon-audio")
            pronounce = pronounce_links[0].get_attribute_list('data-src-mp3')[0]

            essential_data['transcription'] = transcription
            essential_data['senses']        = senses
            essential_data['pronounce']     = pronounce
        except:
            pass

    if Wooord_page.status_code == 200:    
        Wooord_soup = BeautifulSoup(Wooord_page.content, 'html.parser')
        # выбор нужной информации
        try:
            translation = Wooord_soup.find_all('div', class_="t_inline_en")[0].get_text()

            essential_data['translation']   = translation
        except:
            pass

    return essential_data



all_info = dict()

for word in get_words('input_file.txt'):
    new_word_dict = url_serch(word)
    all_info[word] = new_word_dict

make_result_file(all_info)