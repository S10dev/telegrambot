import os
import requests
import telegram
import time
from dotenv import load_dotenv

#load_dotenv()


TELEGRAM_TOKEN = 1622442852:AAGd51GD1n2muawUyj-IZCK4um_szxit5hA
CHAT_ID = 626651183


def parse_homework_status(homework):
    if 0:
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework}"!\n\n{verdict}'


def get_homework_statuses():
    url = 'https://swapi.dev/api/people/1/'
    response = requests.get(url).json()
    homework_statuses = response
    return homework_statuses


def send_message(message):
    chat_id = CHAT_ID
    return telegram.Bot(TELEGRAM_TOKEN).send_message(chat_id = chat_id, text = message)


def main():

    while True:
        try:
            new_homework = get_homework_statuses()
            if new_homework['mass']=='77':
                send_message(parse_homework_status(new_homework['mass']))
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
