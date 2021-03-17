import os
import requests
import telegram
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import datetime


load_dotenv()

MAI = os.environ.get('TELEGRAM_URL')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID_MY')


def send_message(message):
    return telegram.Bot(TELEGRAM_TOKEN).send_message(chat_id = CHAT_ID, text = message)


def parse_schedule(url):
    response = requests.get(url)
    page =  BeautifulSoup(response.text, 'lxml')
    day = page.find_all('div', class_='sc-container')[1]
    day_title = day.find('span', class_='sc-day')
    subjects_time = day.find_all('div', class_='sc-table-col sc-item-time')
    subjects = day.find_all('span', class_='sc-title')
    message = f'Добрый вечер!\nПары на {day_title.text}:'
    for subject, time in zip(subjects, subjects_time):
        message += '\n\n' + time.text + '\n' + subject.text
    return message


def check_time(time_to_sen):
    time_to_send = time_to_sen*60*60
    dt = datetime.datetime.today()
    dt_sec = dt.hour*60*60 + dt.minute*60 + dt.second
    if dt.hour == time_to_sen:
        interval = 0 
    elif dt_sec < time_to_send:
        interval = time_to_send - dt_sec
    elif dt_sec > time_to_send:
        interval = 86400 - (dt_sec - time_to_send)
    return interval


def main():

    while True:
        interval = check_time(17)
        if interval == 0:
            try:
                send_message(parse_schedule(MAI))
                print('wait 3600')
                time.sleep(3600)

            except Exception as e:
                print(f'Бот упал с ошибкой: {e}')
                time.sleep(60)
                continue
        print(f'wait {interval}')
        time.sleep(interval)
        


if __name__ == '__main__':
    main()
